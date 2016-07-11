#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList

scale_factor = 1
lumi = 1
lumi_total = 1165.7
rad_fraction = 0.15

massres_a = 0.032 #sigma = a*mass + b
massres_b = 0.001 #units of GeV

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file> [cuts ROOT file]".format(sys.argv[0])
    print "Arguments: "
    print "\t-l: luminosity for normalization"
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'l:t:c:h')

cutfile=""

for opt, arg in options:
    if opt=='-l':
        lumi = float(arg)
        scale_factor = lumi/lumi_total
    if opt=='-t':
        lumi_total = float(arg)
        scale_factor = lumi/lumi_total
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)<2):
        print_usage()
        sys.exit()

cuts="bscChisq<5&&minIso>0.5&&eleFirstHitX-posFirstHitX<2&&abs(eleP-posP)/(eleP+posP)<0.4&&abs(bscPY)<0.01&&abs(bscPX)<0.01"

c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
events = inFile.Get("ntuple")
if events==None:
    events = inFile.Get("cut")
events.Print()
events.Draw("uncVZ:uncM>>hnew(100,0,0.1,100,-50,50)","","goff,colz")

hasCutFile = False
if len(remainder)==3:
    hasCutFile=True
    events.AddFriend("cut",remainder[2])

totalH = gDirectory.Get("hnew")

outfile.cd()
totalH.Sumw2()
print "scaling data by {0}".format(1/scale_factor)
totalH.Scale(1/scale_factor)
totalH.Draw("colz")
c.Print(remainder[0]+".pdf","Title:zvsmass")
profilehist=totalH.ProfileX("profile")
profilehist.Draw()
c.Print(remainder[0]+".pdf","Title:profile")
masshist=totalH.ProjectionX("mass")
masshist.SetTitle("Radiative vertex mass")
masshist.Draw()
c.Print(remainder[0]+".pdf","Title:mass")

#acceptance = TF1("acceptance","(x>1.05*0.019)/(acos((x>1.05*0.019)*0.019/(x/1.05))/(pi/2))")
acceptance = TF1("acceptance","(x>[0]*[1])/(acos((x>[0]*[1])*[0]/(x/[1]))/(pi/2))")
acceptance.SetParameters(1.05,0.0195)
#acceptance.Draw()
#c.SaveAs(remainder[0]+"-acceptance.png")
masshistscaled=masshist.Clone("massscaled")
masshistscaled.Multiply(acceptance)
masshistscaled.Draw()
c.Print(remainder[0]+".pdf","Title:massscaled")

#sys.exit(0)

gStyle.SetOptFit(1)
gStyle.SetOptStat(1111)
c.SetLogy(1)
#fitfunc = TF1("fitfunc","[0]*exp((x-[1])<[3]?-(x-[1])^2/(2*[2]^2):[3]^2/(2*[2]^2)-[3]*(x-[1])/([2]^2))")
fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))")
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")
#fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*((x-[1])<[3]+[4])*(0.5*(x-[1]-[3])^2*(-[5]+[3]/[2])/[4] - (x-[1]-[3])*[3]/[2] - 0.5*[3]^2/[2]^2) +  ((x-[1])>=[3]+[4])*(0.5*[4]*(-[3]/[2]-[5]) -0.5*[3]^2/[2]^2 -[5]*(x-[1]-[3]-[4])))")
#fitfunc.SetParLimits(4,0,100)

#x0 = [1]+[3]
#dx = [4]
#f(x0) = -0.5*[3]^2/[2]^2
#f'(x0) = -[3]/[2]
#f'(x0+dx) = -[5]

#g''=(f'(x0+dx)-f'(x0))/(dx)
#g' =(x-x0)*(f'(x0+dx)-f'(x0))/(dx)+f'(x0)
#g  =0.5(x-x0)^2*(f'(x0+dx)-f'(x0))/(dx)+(x-x0)*f'(x0) +f(x0)
#0.5*(x-[1]-[3])^2*(-[5]+[3]/[2])/[4] - (x-[1]-[3])*[3]/[2] - 0.5*[3]^2/[2]^2

#g(x0+dx)  =0.5+dx*(f'(x0+dx)-f'(x0))+(dx)*f'(x0) +f(x0)
#g(x0+dx)  =0.5+dx*(f'(x0+dx)+f'(x0))+f(x0)
#0.5*[4]*(-[3]/[2]-[5]) -0.5*[3]^2/[2]^2

#fitfunc = TF1("fitfunc","[0]*(exp(-0.5*((x-[1])/[2])^2) + (x-[1]>[2])*[3]*exp(-(x-[1])*[4]))")
#fitfunc = TF1("fitfunc","exp(pol5(0))")
#fitfunc = TF1("fitfunc","[0]*exp(max(-(x-[1])^2/(2*[2]^2),[3]))")
#fitfunc.SetParLimits(0,0,1000000)
#fitfunc.SetParLimits(1,-10,10)
#fitfunc.SetParLimits(2,0,100)
#fitfunc.SetParLimits(3,0,100)
#fitfunc.SetParLimits(4,0,100)

masses=array.array('d')
masserrors=array.array('d')
sigmas=array.array('d')
sigmaerrors=array.array('d')
integrals=array.array('d')
hightails=array.array('d')
lowtails=array.array('d')

highcutz=array.array('d')
lowcutz=array.array('d')

zcutmasses=array.array('d')
zerobackgroundzcut=array.array('d')
#h1mass=TH1I(

#yieldhist=TH2D("yield","yield",totalH.GetNbinsX(),totalH.GetXaxis().GetXmin(),totalH.GetXaxis().GetXmax(),30,-10,-7)
n_massbins=20
minmass=0.015
maxmass=0.06
yieldhist=TH2D("yield","yield",n_massbins,minmass,maxmass,30,-10,-7)

w = RooWorkspace("w")
w.factory("uncM[0,0.1]")
w.factory("uncVZ[-100,100]")
w.factory("uncP[0,10]")
w.factory("bscChisq[-100,100]")
w.factory("minIso[-100,100]")
w.factory("eleFirstHitX[-100,100]")
w.factory("posFirstHitX[-100,100]")
w.factory("eleP[-100,100]")
w.factory("posP[-100,100]")
w.factory("bscPY[-100,100]")
w.factory("bscPX[-100,100]")
w.factory("cut[0,1]")

#uncM = RooRealVar("uncM","uncM",0,0.1)
#uncVZ = RooRealVar("uncVZ","uncVZ",-100,100)
w.defineSet("allVars","uncM,uncVZ,uncP,bscChisq,minIso,eleFirstHitX,posFirstHitX,eleP,posP,bscPY,bscPX")
w.defineSet("myVars","uncM,uncVZ,cut")
myVars = w.set("myVars")
#myVars = RooArgSet(uncM,uncVZ)
#cutVar = w.factory("expr::cutFunc('bscChisq<5&&minIso>0.5&&eleFirstHitX-posFirstHitX<2&&abs(eleP-posP)/(eleP+posP)<0.4&&abs(bscPY)<0.01&&abs(bscPX)<0.01',bscChisq,minIso,eleFirstHitX,posFirstHitX,eleP,posP,bscPY,bscPX)")
#cutVar = w.factory("expr::cutFunc('bscChisq<5&&minIso>0.5',bscChisq,minIso,eleFirstHitX,posFirstHitX,eleP,posP,bscPY,bscPX)")
#cutVar = w.function("cutFunc")
w.Print()
#cutVar = RooFormulaVar("cut","","bscChisq<5&&minIso>0.5&&eleFirstHitX-posFirstHitX<2&&abs(eleP-posP)/(eleP+posP)<0.4&&abs(bscPY)<0.01&&abs(bscPX)<0.01",RooArgList(
#dataset = RooDataSet("data","data",events,myVars,cutVar)
#dataset = RooDataSet("data","data",events,w.set("allVars"),cuts)

#RooDataSet.setDefaultStorageType(RooAbsData.Tree)

dataset = RooDataSet("data","data",events,w.set("myVars"),"cut==1")

#frame=w.var("uncVZ").frame()
#c.SetLogy()
#dataset.plotOn(frame)
#frame.Draw()
#c.SaveAs("test.png")
#binning=3
w.factory("Gaussian::vtx_model(uncVZ,mean[-50,50],sigma[0,50])")
gauss_pdf = w.pdf("vtx_model")
w.factory("EXPR::gaussExp('exp( ((@0-@1)<@3)*(-0.5*(@0-@1)^2/@2^2) + ((@0-@1)>=@3)*(-0.5*@3^2/@2^2-(@0-@1-@3)/@4))',uncVZ,gauss_mean[-5,-20,20],gauss_sigma[5,1,50],exp_breakpoint[10,0,50],exp_length[3,0.5,20])")
gaussexp_pdf = w.pdf("gaussExp")
w.defineSet("obs_1d","uncVZ")
obs=w.set("obs_1d")
uncVZ = w.var("uncVZ")
uncVZ.setBins(1000)
gauss_params = gauss_pdf.getParameters(obs)
gaussexp_params = gaussexp_pdf.getParameters(obs)

for i in range(1,n_massbins):
#for i in range(0,totalH.GetXaxis().GetNbins()-binning+2,binning):
    print i
    centermass=yieldhist.GetXaxis().GetBinCenter(i)
    massrange=2.5*(massres_a*centermass + massres_b)
    lowedge = centermass-massrange/2.0
    highedge = centermass+massrange/2.0
    name="Radiative vertex Z, mass [{}, {}] GeV".format(lowedge,highedge)
    #dataset = RooDataSet("data","data",events,w.set("myVars"),"abs(uncM-{0})<{1}".format(centermass,massrange/2))
    dataInRange = dataset.reduce(obs,"abs(uncM-{0})<{1}".format(centermass,massrange/2))
    if dataInRange.sumEntries()<100:
        continue

    frame=uncVZ.frame()
    frame.SetTitle(name)

    binnedData = dataInRange.binnedClone()
    binnedData.plotOn(frame)
    mean = binnedData.mean(uncVZ)
    sigma = binnedData.sigma(uncVZ)
    print "before gaussian fit: mean={0}, sigma={1}".format(mean,sigma)
    uncVZ.setRange("fitRange",mean-3*sigma,mean+3*sigma)
    gauss_params.setRealValue("mean",mean)
    gauss_params.setRealValue("sigma",sigma)
    #gauss_params.printLatex()
    gauss_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
    #gauss_params.printLatex()
    #gauss_pdf.plotOn(frame)
    mean= gauss_params.getRealValue("mean")
    sigma= gauss_params.getRealValue("sigma")
    print "after gaussian fit: mean={0}, sigma={1}".format(mean,sigma)
    gaussexp_params.setRealValue("gauss_mean",mean)
    gaussexp_params.setRealValue("gauss_sigma",sigma)
    gaussexp_params.setRealValue("exp_breakpoint",10)
    gaussexp_params.setRealValue("exp_length",10/sigma)
    uncVZ.setRange("fitRange",mean-2*sigma,50)
    result = gaussexp_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1),RooFit.Minimizer("Minuit","Minimize"),RooFit.Save())
    print result.status()
    result.printValue(ROOT.cout)
    #gaussexp_pdf.fitTo(binnedData,RooFit.Range("fitRange"),RooFit.PrintLevel(-1))
    gaussexp_pdf.plotOn(frame,RooFit.Range("fitRange"),RooFit.NormRange("fitRange"),RooFit.LineColor(result.status()+1))

    func = gaussexp_pdf.createCdf(obs).asTF(RooArgList(obs),RooArgList(gaussexp_params))
    zcut_frac = 0.5/(dataInRange.sumEntries()/scale_factor)
    print func.GetX(1-zcut_frac,0,50)

    #dataInRange.plotOn(frame)
    #gauss_params.setRealValue("mean",dataInRange.mean(uncVZ))
    #gauss_params.setRealValue("sigma",dataInRange.sigma(uncVZ))
    #gauss_pdf.fitTo(dataInRange,RooFit.PrintLevel(-1))
    #gauss_params.printLatex()
    #mean= gauss_params.getRealValue("mean")
    #sigma= gauss_params.getRealValue("sigma")
    #gaussexp_params.setRealValue("gauss_mean",mean)
    #gaussexp_params.setRealValue("gauss_sigma",sigma)
    #gaussexp_params.setRealValue("exp_breakpoint",10)
    #gaussexp_params.setRealValue("exp_length",5)
    #gaussexp_params.printLatex()
    #uncVZ.setRange("fitRange",mean-2*sigma,50)
    #result = gaussexp_pdf.fitTo(dataInRange,RooFit.Range("fitRange"),RooFit.PrintLevel(-1),RooFit.Save())
    #gaussexp_params.printLatex()
    gaussexp_pdf.paramOn(frame)
    #gaussexp_pdf.plotOn(frame,RooFit.Range("fitRange"),RooFit.NormRange("fitRange"))
    #gaussexp_pdf.plotOn(frame,RooFit.Range("fitRange"),RooFit.NormRange("fitRange"),RooFit.LineColor(result.status()+1))

    frame.SetAxisRange(-50,50)
    frame.SetMinimum(0.5)
    frame.Draw()
    c.Print(remainder[0]+".pdf","Title:slice_"+str(i)+"_roofit")


    #h1d = dataInRange.createHistogram("data_in_range",w.var("uncVZ"),"Binning(100,-50,50)")
    #h1d = dataInRange.createHistogram("data_in_range",w.var("uncVZ"))
    h1d = RooAbsData.createHistogram(dataInRange,"data_in_range",w.var("uncVZ"),RooFit.Binning(100,-50,50))
    print h1d.GetEntries()
    #events.Draw("uncVZ>>hnew(100,-50,50)",cuts+"&&uncM>{0}&&uncM<{1}".format(lowedge,highedge),"goff")
    #h1d = gDirectory.Get("hnew")
    h1d.Sumw2()
    h1d.Scale(1/scale_factor)

    #h1d=totalH.ProjectionY("slice_{}".format(i),i,i+binning-1)
    #h1d=h1d.Rebin(2,"slice")
    integrals.append(h1d.Integral())
    h1d.SetTitle(name)
    print name
    if (h1d.GetEntries()>100):
        fit=h1d.Fit("gaus","QS")
        peak=fit.Get().Parameter(0)
        mean=fit.Get().Parameter(1)
        sigma=fit.Get().Parameter(2)
        #print '{}, {}, {}'.format(peak,mean,sigma)
        fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
        #fit=h1d.Fit("expo","LQS+","",mean+2*sigma,mean+6*sigma)
        if fit.Get().IsValid():
            masses.append(centermass)
            masserrors.append(massrange)
            lowtails.append(h1d.Integral(0,h1d.FindBin(mean-3*sigma)))
            hightails.append(h1d.Integral(h1d.FindBin(mean+3*sigma),h1d.GetNbinsX()))
            mean=fit.Get().Parameter(1)
            sigma=fit.Get().Parameter(2)
            sigmas.append(sigma)
            sigmaerrors.append(fit.Get().Error(2))
            highcutz.append(mean+3*sigma)
            lowcutz.append(mean-3*sigma)
            #fitfunc.SetParameters(peak,mean,sigma,0.5,0.2);
            fitfunc.SetParameters(peak,mean,sigma,3*sigma,5);
            #fitfunc.SetParameters(peak,mean,sigma,2.5*sigma,sigma,0.3);
            fit=h1d.Fit(fitfunc,"LSQM","",mean-2*sigma,mean+10*sigma)
            #for j in range(1,h1d.GetNbinsX()+1):
                #resid.SetBinContent(j,h1d.GetBinContent(j) - h1d.GetFunction("fitfunc").Eval(h1d.GetBinCenter(j)));
            #c.SetLogy(0)
            #resid.Draw()
            #c.SaveAs(remainder[0]+"-"+str(i)+"_resid.png")
            #c.SetLogy(1)

            if fit.Get().IsValid():
                zcutmasses.append(centermass)
                zcut=fitfunc.GetX(0.5/fit.Get().Parameter(4),mean,200)
                #zcut=35
		print "zcut {0}".format(zcut)
		#print 
		#(log([0]/0.5)-0.5*[3]^2/[2]^2)*[4]-(-[1]-[3]) = x
                zerobackgroundzcut.append(zcut)
                h1d.Draw("E")
                c.Print(remainder[0]+".pdf","Title:slice_"+str(i))
		for i in range(0,yieldhist.GetYaxis().GetNbins()):
			eps = yieldhist.GetYaxis().GetBinCenter(i)
		#for eps in frange(-10,-7,0.1):
			#print 10**eps
			ct = 80e-3*1e-8/(10**eps)*(0.1/centermass)
			gammact = 8*(1.05/10)*1e-8/(10**eps)*(0.1/centermass)**2
			#print gammact
			ap_yield= 3*math.pi*10**eps/(2*(1/137.0))*h1d.Integral()*(centermass/massrange)*rad_fraction
			#print ap_yield
			#print ap_yield*math.exp(-zcut/gammact)
                        if ap_yield*math.exp(-zcut/gammact)>0.1:
                            print "{0} {1} {2} {3} {4} {5}".format(centermass,10**eps,ct,gammact,ap_yield,ap_yield*math.exp(-zcut/gammact))
			yieldhist.Fill(centermass,eps,ap_yield*math.exp(-zcut/gammact))
    for func in h1d.GetListOfFunctions():
        func.Delete()
    h1d.Delete()

c.SetLogy(0)
c.SetLogx(1)
yieldhist.Draw("colz")
c.Print(remainder[0]+".pdf","Title:yield")
c.SetLogy(1)
c.SetLogx(0)
cutmasses=masses[:]

cutmasses.append(10)
highcutz.append(highcutz[-1])
lowcutz.append(lowcutz[-1])
cutmasses.append(10)
highcutz.append(100)
lowcutz.append(-100)
cutmasses.append(0)
highcutz.append(100)
lowcutz.append(-100)
cutmasses.append(0)
highcutz.append(highcutz[0])
lowcutz.append(lowcutz[0])
cutmasses.append(cutmasses[0])
highcutz.append(highcutz[0])
lowcutz.append(lowcutz[0])

highcut=TCutG("highzcut",len(cutmasses),cutmasses,highcutz)
lowcut=TCutG("lowzcut",len(cutmasses),cutmasses,lowcutz)

masshist.SetTitle("Radiative vertex mass, +Z tail")
masshist.Draw("E")
hightails=totalH.ProjectionX("hightails",0,-1,"[highzcut]")
hightails.Draw("E SAME")
c.Print(remainder[0]+".pdf","Title:hightails")


masshist.SetTitle("Radiative vertex mass, -Z tail")
masshist.Draw("E")
lowtails=totalH.ProjectionX("lowtails",0,-1,"[lowzcut]")
lowtails.Draw("E SAME")
c.Print(remainder[0]+".pdf","Title:lowtails")

c.SetLogy(0)

#masshist.SetTitle("Radiative vertex mass")
#masshist.Draw("")
#c.SaveAs(remainder[0]+"-massnorm.png")


sigmagraph=TGraphErrors(len(masses),masses,sigmas,masserrors,sigmaerrors)
sigmagraph.SetTitle("Radiative vertex sigma vs. mass")
sigmagraph.SetName("sigma")
sigmagraph.Write()

sigmafitfunc = TF1("sigmafitfunc","[0]*x^[1]",0.01,0.08)
sigmafitfunc.SetParameters(1,-0.5);

sigmagraph.Draw("AP")
sigmagraph.Fit("sigmafitfunc","","",0.015,0.06)
#sigmagraph.Fit("pol5","","",0.02,0.08)
c.Print(remainder[0]+".pdf","Title:sigmas")

zcutgraph=TGraph(len(zcutmasses),zcutmasses,zerobackgroundzcut)
zcutgraph.SetTitle("Z cut for 0.5 background events")
zcutgraph.SetName("zcut")
zcutgraph.GetXaxis().SetTitle("Mass [GeV]")
zcutgraph.GetXaxis().SetRangeUser(0.015,0.06)
zcutgraph.GetYaxis().SetTitle("Z cut [mm]")
zcutgraph.GetYaxis().SetRangeUser(0,60)
zcutgraph.Write()
zcutgraph.Draw("AC")
#zcutgraph.Fit("pol4")
c.Print(remainder[0]+".pdf","Title:zcut")
c.Print(remainder[0]+".pdf]")

outfile.Write()
outfile.Close()

#raw_input("Press Enter to continue...")
