#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D

scale_factor = 1
lumi_total = 1240

massres_a = 0.032 #sigma = a*mass + b
massres_b = 0.001 #units of GeV

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'l:h', ['luminosity','help',])

for opt, arg in options:
    if opt in ('-l', '--luminosity'):
        lumi = float(arg)
        scale_factor = lumi/lumi_total
    elif opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\t-l, --luminosity: luminosity for normalization"
        print "\n"
        sys.exit(0)


if (len(remainder)<2):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
outfile = TFile(remainder[0]+"-plots.root","RECREATE")
totalH = None
for filename in remainder[1:]:
    f=TFile(filename)
    print filename
    h=f.Get("TridentMonitoring/GBLTrack/pairs1/Radiative vertex: Vertex Z vs. mass;1")
    if totalH is None:
        totalH=TH2D(h)
        totalH.SetDirectory(outfile)
    else:
        totalH.Add(h)

outfile.cd()
totalH.Sumw2()
totalH.Scale(1/scale_factor)
totalH.Draw("colz")
c.SaveAs(sys.argv[1]+"-zvsmass.png")
profilehist=totalH.ProfileX("profile")
profilehist.Draw()
c.SaveAs(sys.argv[1]+"-profile.png")
masshist=totalH.ProjectionX("mass")
masshist.SetTitle("Radiative vertex mass")
masshist.Draw()
c.SaveAs(sys.argv[1]+"-mass.png")
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

#resid = TH1D("resid","resid",totalH.GetNbinsY(),totalH.GetXaxis().GetXmin(),totalH.GetXaxis().GetXmax())
binning=4
for i in range(0,totalH.GetXaxis().GetNbins()-binning+2):
#for i in range(0,totalH.GetXaxis().GetNbins()-binning+2,binning):
    print i
    lowedge = totalH.GetXaxis().GetBinLowEdge(i)
    highedge = totalH.GetXaxis().GetBinUpEdge(i+binning-1)
    massrange=highedge-lowedge
    reslimited_massrange=2.5*(massres_a*(highedge+lowedge)/2 + massres_b)
    h1d=totalH.ProjectionY("slice_"+str(i),i,i+binning-1)
    #h1d=h1d.Rebin(2,"slice")
    integrals.append(h1d.Integral())
    name="Radiative vertex Z, mass [{}, {}] GeV".format(lowedge,highedge)
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

            masses.append((highedge+lowedge)/2)
            masserrors.append((highedge-lowedge)/2)
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

            if fit.Get().IsValid() and fit.Get().Parameter(4)<10:
                zcutmasses.append((highedge+lowedge)/2)
                zcut=fitfunc.GetX(0.5*massrange/reslimited_massrange/fit.Get().Parameter(4),mean,200)
		#print zcut
		#print 
		#(log([0]/0.5)-0.5*[3]^2/[2]^2)*[4]-(-[1]-[3]) = x
                zerobackgroundzcut.append(zcut)
                h1d.Draw("E")
                c.SaveAs(remainder[0]+"-"+str(i)+".png")

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
c.SaveAs(sys.argv[1]+"-hightails.png")


masshist.SetTitle("Radiative vertex mass, -Z tail")
masshist.Draw("E")
lowtails=totalH.ProjectionX("lowtails",0,-1,"[lowzcut]")
lowtails.Draw("E SAME")
c.SaveAs(sys.argv[1]+"-lowtails.png")

c.SetLogy(0)

#masshist.SetTitle("Radiative vertex mass")
#masshist.Draw("")
#c.SaveAs(sys.argv[1]+"-massnorm.png")


sigmagraph=TGraphErrors(len(masses),masses,sigmas,masserrors,sigmaerrors)
sigmagraph.SetTitle("Radiative vertex sigma vs. mass")
sigmagraph.SetName("sigma")
sigmagraph.Write()

sigmafitfunc = TF1("sigmafitfunc","[0]*x^[1]",0.02,0.08)
sigmafitfunc.SetParameters(1,-0.5);

sigmagraph.Draw("AP")
sigmagraph.Fit("sigmafitfunc","","",0.02,0.06)
#sigmagraph.Fit("pol5","","",0.02,0.08)
c.SaveAs(sys.argv[1]+"-sigmas.png")

zcutgraph=TGraph(len(zcutmasses),zcutmasses,zerobackgroundzcut)
zcutgraph.SetTitle("Z cut for 0.5 background events")
zcutgraph.SetName("zcut")
zcutgraph.Write()
zcutgraph.Draw("A*")
zcutgraph.Fit("pol4")
c.SaveAs(sys.argv[1]+"-zcut.png")

outfile.Write()
outfile.Close()

#raw_input("Press Enter to continue...")
