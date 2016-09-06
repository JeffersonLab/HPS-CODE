#!/usr/bin/env python
import sys, array,math
import getopt
import upperlimit
import numpy
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooFit, RooAbsReal, RooArgList, gPad, TFeldmanCousins
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file> <acceptance ROOT file> <tails ROOT file> <radfrac ROOT file>".format(sys.argv[0])
    print "./fitvtx.py stuff ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails.root ../frac.root -u"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"


cutfile=""
uniform_efficiency = False
no_candidates = False
scale_factor = 1.0
correct_mres = False

n_massbins=50
minmass=0.015
maxmass=0.06
n_epsbins=50
mineps=-10.0
maxeps=-7.5

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'unms:b:h')
for opt, arg in options:
    if opt=='-u':
        uniform_efficiency = True
    if opt=='-n':
        no_candidates = True
    if opt=='-m':
        correct_mres= True
    if opt=='-s':
        scale_factor = float(arg)
    if opt=='-b':
        n_massbins = int(arg)
        n_epsbins = int(arg)
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)!=5):
        print_usage()
        sys.exit()

CL = 0.9

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(1111)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
events = inFile.Get("cut")
#events.Print()
events.Draw("uncVZ:uncM>>hnew(100,0,0.1,100,-50,50)","","colz")
c.Print(remainder[0]+".pdf")

acceptanceFile = TFile(remainder[2])
tailsFile = TFile(remainder[3])
radfracFile = TFile(remainder[4])

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")


targetz = -5.0
maxz = 100 #max Z out to where we have acceptance (fitted acceptance curve may blow up past this)
zcut_count = 0.5

masscut_nsigma = 2.80
masscut_eff = 0.838

xedges = array.array('d')
yedges = array.array('d')
for i in range(0,n_massbins+1):
    xedges.append(minmass+(i-0.5)*(maxmass-minmass)/(n_massbins-1))
for j in range(0,n_epsbins+1):
    yedges.append(10**(mineps+(j-0.5)*(maxeps-mineps)/(n_epsbins-1)))

outfile.cd()
massArr = array.array('d')
zcutArr = array.array('d')
limitHist=TH2D("limit","limit",n_massbins,xedges,n_epsbins,yedges)
detectableHist=TH2D("detectable","detectable",n_massbins,xedges,n_epsbins,yedges)
gammactHist=TH2D("gammact","gammact",n_massbins,xedges,n_epsbins,yedges)
allzHist=TH2D("detectable_allz","detectable_allz",n_massbins,xedges,n_epsbins,yedges)
prodHist=TH2D("production","production",n_massbins,xedges,n_epsbins,yedges)
candHist=TH1D("candidates","candidates",n_massbins,xedges)
fcLowerHist=TH2D("fcLowerLimit","fcLowerLimit",n_massbins,xedges,n_epsbins,yedges)
fcUpperHist=TH2D("fcUpperLimit","fcUpperLimit",n_massbins,xedges,n_epsbins,yedges)

w = RooWorkspace("w")
w.factory("uncM[0,0.1]")
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("cut[0,1]")

w.defineSet("allVars","uncM,uncVZ,uncP")
w.defineSet("myVars","uncM,uncVZ")
myVars = w.set("myVars")

dataset = RooDataSet("data","data",events,w.set("myVars"),"")

w.factory("Gaussian::vtx_model(uncVZ,mean[-50,50],sigma[0,50])")
gauss_pdf = w.pdf("vtx_model")
w.factory("EXPR::gaussExp('exp( ((@0-@1)<@3)*(-0.5*(@0-@1)^2/@2^2) + ((@0-@1)>=@3)*(-0.5*@3^2/@2^2-(@0-@1-@3)/@4))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50],exp_length[3,0.5,20])")
gaussexp_pdf = w.pdf("gaussExp")
w.defineSet("obs_1d","uncVZ")
obs=w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(200)
gauss_params = gauss_pdf.getParameters(obs)
gaussexp_params = gaussexp_pdf.getParameters(obs)

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)
w.factory("EXPR::signal('(@0>{0})*exp(@1 + @2*@0 + @3*@0^2 + @4*@0^3 + @5*@0^4)',uncVZ,eff_p0[-1,1],eff_p1[-1,1],eff_p2[-1,1],eff_p3[-1,1],eff_p4[-1,1])".format(targetz))
w.factory("SUM::model(strength[0,1]*signal,gaussExp)")

pdf = w.pdf("model")
modelConfig = ModelConfig("test")
modelConfig.SetWorkspace(w)
modelConfig.SetPdf("model")
modelConfig.SetParametersOfInterest("strength")
modelConfig.SetObservables("uncVZ")

fc = TFeldmanCousins()
fc.SetCL(CL)

for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massArr.append(mass)
    mres_p0 = acceptanceFile.Get("mres_l1_p0").GetFunction("pol1").Eval(mass)
    mres_p1 = acceptanceFile.Get("mres_l1_p1").GetFunction("pol1").Eval(mass)
    if correct_mres:
        mres_p1 = 0
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw("uncVZ:uncM>>hnew2d(100,0,0.1,100,-50,50)","abs(uncM-{0})<{1}/2*({2}+{3}*uncVZ)".format(mass,masscut_nsigma,mres_p0,mres_p1),"colz")
    c.cd(2)
    #gPad.SetLogy(1)
    
    deltaM = 0.001
    events.Draw("uncM>>mass(100,{0}-{1},{0}+{1})".format(mass,0.5*deltaM),"abs(uncM-{0})<{1}".format(mass,0.5*deltaM),"")
    c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))
    num_pairs = gDirectory.Get("mass").GetEntries()*scale_factor
    radfrac = radfracFile.Get("radfrac").GetFunction("pol3").Eval(mass)
    num_rad = radfrac*num_pairs
    ap_yield= 3*math.pi/(2*(1/137.0))*num_rad*(mass/deltaM)
    print "{0} pairs, {1} radfrac, {2} rad, {3} A'".format(num_pairs,radfrac,num_rad,ap_yield)


    #events.Draw("uncVZ>>hnew1d(100,-50,50)","abs(uncM-{0})<1.25*({1}+{2}*uncVZ)".format(mass,mres_p0,mres_p1),"colz")
    #h1d = gDirectory.Get("hnew1d")
    #fit=h1d.Fit("gaus","QSN")
    #peak=fit.Get().Parameter(0)
    #mean=fit.Get().Parameter(1)
    #sigma=fit.Get().Parameter(2)
    #fit=h1d.Fit("gaus","QSN","",mean-3*sigma,mean+3*sigma)
    #peak=fit.Get().Parameter(0)
    #mean=fit.Get().Parameter(1)
    #sigma=fit.Get().Parameter(2)
    breakz = tailsFile.Get("breakz").GetFunction("pol3").Eval(mass)
    length = tailsFile.Get("length").GetFunction("pol3").Eval(mass)
    #fitfunc.SetParameters(peak,mean,sigma,breakz,length);
    #fitfunc.Draw("same")
    #zcut=fitfunc.GetX(0.5/length,mean,200)
    #print fitfunc.Eval(zcut)

    c.cd(1)
    gPad.SetLogy()
    frame=uncVZ.frame()
    dataInRange = dataset.reduce(obs,"abs(uncM-{0})<{1}/2*({2}+{3}*uncVZ)".format(mass,masscut_nsigma,mres_p0,mres_p1))
    binnedData = dataInRange.binnedClone()
    binnedData.plotOn(frame)
    mean = binnedData.mean(uncVZ)
    sigma = binnedData.sigma(uncVZ)
    uncVZ.setRange("fitRange",mean-3*sigma,mean+3*sigma)
    gauss_params.setRealValue("mean",mean)
    gauss_params.setRealValue("sigma",sigma)
    gauss_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
    mean= gauss_params.getRealValue("mean")
    sigma= gauss_params.getRealValue("sigma")
    gaussexp_params.setRealValue("gauss_mean",mean)
    gaussexp_params.setRealValue("gauss_sigma",sigma)
    gaussexp_params.setRealValue("exp_breakpoint",breakz)
    gaussexp_params.setRealValue("exp_length",length)
    w.var("gauss_mean").setConstant(True)
    w.var("gauss_sigma").setConstant(True)
    w.var("exp_breakpoint").setConstant(True)
    w.var("exp_length").setConstant(True)
    func = gaussexp_pdf.createCdf(obs).asTF(RooArgList(obs),RooArgList(gaussexp_params))
    zcut_frac = zcut_count/(dataInRange.sumEntries()*scale_factor)
    zcut = func.GetX(1-zcut_frac,0,50)
    print "zcut {}".format(zcut)
    dataPastCut = dataInRange.reduce(w.set("obs_1d"),"uncVZ>{0}".format(zcut))
    zcutArr.append(zcut)

    gaussexp_pdf.plotOn(frame)
    frame.SetAxisRange(-50,50)
    frame.SetMinimum(0.5)
    name="Radiative vertex Z, mass {0} GeV, zcut {1} mm".format(mass,zcut)
    frame.SetTitle(name)
    frame.Draw()
#
    c.cd(2)
    gPad.SetLogy(0)

    #zcut2_frac = 20.0/(dataInRange.sumEntries()/scale_factor)
    #zcut2 = func.GetX(1-zcut2_frac,0,50)
    #dataPastCut2 = dataInRange.reduce(w.set("obs_1d"),"uncVZ>{0}".format(zcut2))

    n_candidates = dataPastCut.numEntries()
    if (no_candidates):
        n_candidates = 0
    print n_candidates
    for k in range(0,n_candidates):
        candHist.Fill(mass)
    #candHist.Fill(mass,n_candidates)
    fcLower = fc.CalculateLowerLimit(n_candidates,zcut_count)
    fcUpper = fc.CalculateUpperLimit(n_candidates,zcut_count)

    gamma = acceptanceFile.Get("gamma").GetFunction("pol0").Eval(mass)
    eff_p0= acceptanceFile.Get("l1_p0").GetFunction("pol1").Eval(mass)
    eff_p1= acceptanceFile.Get("l1_p1").GetFunction("pol1").Eval(mass)
    eff_p2= acceptanceFile.Get("l1_p2").GetFunction("pol3").Eval(mass)
    eff_p3= acceptanceFile.Get("l1_p3").GetFunction("pol3").Eval(mass)
    #eff_p4= acceptanceFile.Get("l1_p4").GetFunction("pol4").Eval(mass)
    eff_p4= 0
    exppol4.SetParameters(eff_p0,eff_p1,eff_p2,eff_p3,eff_p4)
    exppol4.Draw()
    exppol4.GetYaxis().SetRangeUser(0,2)
    c.Print(remainder[0]+".pdf","Title:mass {0} zcut {1}".format(mass,zcut))
    for j in range(0,n_epsbins):
        c.Clear()
        eps = mineps+j*(maxeps-mineps)/(n_epsbins-1)
        #ct = 80e-3*1e-8/(10**eps)*(0.1/mass)
        #gammact = 8*(1.05/10)*1e-8/(10**eps)*(0.1/mass)**2
        hbar_c = 1.973e-13
        ct = hbar_c*3.0/(mass*(1/137.036)*10**eps)
        gammact = hbar_c*3.0*1.056*gamma/(mass*mass*(1/137.036)*10**eps)
        #print "epsq {0} ct {1} gammact {2}".format(eps,ct,gammact)

        #exppol4.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact,0,0,0)
        #exppol4.Draw()
        #c.Print(remainder[0]+".pdf","Title:mass_{0}_eps_{1}".format(mass,eps))
        blahh = 0
        #print "decay integral {0}".format(exppol4.IntegralOneDim(targetz,100,1e-12,1e-12,ROOT.Double(blahh)))
        
        exppol4.SetParameters(eff_p0+targetz/gammact-math.log(gammact),eff_p1-1.0/gammact,eff_p2,eff_p3,eff_p4)
        if (uniform_efficiency):
            exppol4.SetParameters(targetz/gammact-math.log(gammact),-1.0/gammact,0,0,0)
        #c.SetLogy(0)
        #exppol4.Draw()
        #c.Print(remainder[0]+".pdf","Title:mass_{0}_eps{1}".format(mass,eps))
        sig_integral = exppol4.IntegralOneDim(targetz,maxz,1e-12,1e-12,ROOT.Double(blahh))
        #print "signal integral {0}".format(sig_integral) #this is production-weighted efficiency


        #w.var("eff_p0").setVal(eff_p0+targetz/gammact-math.log(gammact))
        #w.var("eff_p1").setVal(eff_p1-1.0/gammact)
        #w.var("eff_p2").setVal(eff_p2)
        #w.var("eff_p3").setVal(eff_p3)
        #w.var("eff_p4").setVal(eff_p4)
        #w.var("eff_p0").setConstant(True)
        #w.var("eff_p1").setConstant(True)
        #w.var("eff_p2").setConstant(True)
        #w.var("eff_p3").setConstant(True)
        #w.var("eff_p4").setConstant(True)
        #c.SetLogy()

        #uncVZ.setRange("fitRange",zcut,50)
        #frame=uncVZ.frame()
        #frame.SetTitle(name)
        #binnedData.plotOn(frame)
        #dataPastCut2.plotOn(frame)
        #fitresult = pdf.fitTo(binnedData)
        #fitresult = pdf.fitTo(dataPastCut2,RooFit.Range("fitRange"))
        #pdf.plotOn(frame)
        #frame.SetMinimum(0.1)
        #frame.Draw()
        #c.Print(remainder[0]+".pdf","Title:test2")



        #signalCdf = w.pdf("signal").createCdf(w.set("obs_1d"))
        #w.var("uncVZ").setVal(zcut)
        #cdfAtZcut = signalCdf.getVal()
        cdfAtZcut = exppol4.IntegralOneDim(zcut,maxz,1e-12,1e-12,ROOT.Double(blahh))
        if (no_candidates):
            dataArray=numpy.zeros(2)
            dataArray[1] = cdfAtZcut
        else:
            dataArray=numpy.zeros(dataPastCut.numEntries()+2)
            dataArray[0] = 0.0
            for i in xrange(0,dataPastCut.numEntries()):
                thisX = dataPastCut.get(i).getRealValue("uncVZ")
                w.var("uncVZ").setVal(thisX)
                #dataArray[i+1]=(signalCdf.getVal()-cdfAtZcut)
                dataArray[i+1]=(cdfAtZcut-exppol4.IntegralOneDim(thisX,maxz,1e-12,1e-12,ROOT.Double(blahh)))
                #print "thisX={0}, cdf={1}".format(thisX,dataArray[i+1])
            dataArray[dataPastCut.numEntries()+1] = cdfAtZcut
        dataArray/= (cdfAtZcut)
        dataArray.sort()
        #print dataArray
        output = upperlimit.upperlim(CL, 1, dataArray, 0., dataArray)

        prodHist.Fill(mass,10**eps,ap_yield*10**eps)
        allzHist.Fill(mass,10**eps,ap_yield*10**eps*sig_integral)
        detectableHist.Fill(mass,10**eps,ap_yield*10**eps*sig_integral*cdfAtZcut)
        gammactHist.Fill(mass,10**eps,gammact)
        limit_detectable = output[0] # this is a limit on number of detectable A'
        limit_allz = limit_detectable/(cdfAtZcut*masscut_eff) # this is a limit on number of detectable A' if we didn't have zcut or mass cut
        limit_production = limit_allz/sig_integral # limit on number of produced A'
        limit_eps = limit_production/ap_yield
        limit_scaled = limit_eps/10**eps
        print "{0} {1} {2} {3} {4}".format(limit_detectable,limit_allz,limit_production,limit_eps,limit_scaled)
        limitHist.Fill(mass,10**eps,limit_scaled)
        fcLowerHist.Fill(mass,10**eps,fcLower/cdfAtZcut/masscut_eff/sig_integral/ap_yield/10**eps)
        fcUpperHist.Fill(mass,10**eps,fcUpper/cdfAtZcut/masscut_eff/sig_integral/ap_yield/10**eps)


c.Clear()

c.Print(remainder[0]+".pdf]")

c.Print(remainder[0]+"_output.pdf[")
gStyle.SetOptStat(0)
c.SetLogy(0)
graph=TGraph(len(massArr),massArr,zcutArr)
graph.SetTitle("zcut")
graph.Draw("AL*")
graph.Write("zcut")
c.Print(remainder[0]+"_output.pdf","Title:test")

def drawContour(hist,nlevels):
    minValue = hist.GetBinContent(hist.GetMinimumBin())
    bottom = int(math.floor(math.log10(minValue)))
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))
def drawMaxContour(hist,nlevels):
    maxValue = hist.GetBinContent(hist.GetMaximumBin())
    bottom = int(math.floor(math.log10(maxValue)))-nlevels+1
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))

c.SetLogy(1)
c.SetLogz(1)
fcLowerHist.Draw("colz")
fcLowerHist.GetZaxis().SetRangeUser(1,1e3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(fcUpperHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(limitHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawMaxContour(detectableHist,3)
c.Print(remainder[0]+"_output.pdf","Title:tada")
detectableHist.SetContour(20)
detectableHist.Draw("colz")
detectableHist.GetZaxis().SetRangeUser(1e-2,2.4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
allzHist.Draw("colz")
allzHist.GetZaxis().SetRangeUser(1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")
drawContour(gammactHist,4)
c.Print(remainder[0]+"_output.pdf","Title:tada")
prodHist.Draw("colz")
prodHist.GetZaxis().SetRangeUser(1e-2,1e2)
c.Print(remainder[0]+"_output.pdf","Title:tada")
c.SetLogy(0)
candHist.Draw()
c.Print(remainder[0]+"_output.pdf","Title:tada")
outfile.cd()


c.Print(remainder[0]+"_output.pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

