#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList, gPad

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 't:e:z:ch')

cutfile=""
tupleName = "ntuple"
massVar = "uncM"
applyCut=False
ebeam=1.056
ztarg=0.5

for opt, arg in options:
    if opt=='-t':
        tupleName= str(arg)
    if opt=='-e':
        ebeam= float(arg)
    if opt=='-z':
        ztarg= float(arg)
    if opt=='-c':
        applyCut= True
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)!=2):
        print_usage()
        sys.exit()

cut = "isPair1&&eleClY*posClY<0&&uncP>0.8*{0}&max(eleTrkChisq,posTrkChisq)<60&&eleP<0.75*{0}&&bscChisq<10\
&&bscChisq-uncChisq<5&&uncP<1.15*{0}&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-eleTrkT-43)<4\
&&abs(posClT-posTrkT-43)<4&&abs(eleClT-posClT)<2&&eleHasL2&&posHasL2&&eleHasL1&&posHasL1\
&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{1}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{1}*posPY/posP)*sign(posPY))>0\
&&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0+{1}*posPX/posP<1.5".format(ebeam,ztarg)

if(applyCut):
    cut = ""


gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(1111)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

inFile = TFile(remainder[1])
events = inFile.Get("{0}".format(tupleName))
#events.Print()
events.Draw("uncVZ:{0}>>(100,0,{1},100,-50,50)".format(massVar,ebeam*0.1),"{0}".format(cut),"colz")
c.Print(remainder[0]+".pdf")

#acceptanceFile = TFile(remainder[2])

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))")
#fitfunc.SetParName(0,"Amplitude")
#fitfunc.SetParName(1,"Mean")
#fitfunc.SetParName(2,"Sigma")
#fitfunc.SetParName(3,"Tail Z")
#fitfunc.SetParName(4,"Tail length")

#massarray=array.array('d')
#zeroArr=array.array('d')
#breakzarray=array.array('d')
#lengtharray=array.array('d')
#breakzErr=array.array('d')
#lengthErr=array.array('d')
n_massbins=50
#minmass=0.021
#maxmass=0.06

#masscut_nsigma = 2.80

#for i in range(0,n_massbins):
#    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
#    massarray.append(mass)
#    zeroArr.append(0)
#    mres_p0 = acceptanceFile.Get("mres_l1_p0").GetFunction("pol1").Eval(mass)
#    mres_p1 = acceptanceFile.Get("mres_l1_p1").GetFunction("pol1").Eval(mass)
#    if correct_mres:
#        mres_p1 = 0
#    c.Clear()
#    c.Divide(1,2)
#    c.cd(1)
#events.Draw("uncVZ:{0}>>hnew2d(100,0,{1},100,-50,50)".format(massVar,ebeam*0.1),cut,"colz")
#c.cd(2)
gPad.SetLogy(1)
events.Draw("uncVZ>>hnew1d(200,-50,50)",cut,"")

h1d = gDirectory.Get("hnew1d")
fit=h1d.Fit("gaus","QS")
peak=fit.Get().Parameter(0)
mean=fit.Get().Parameter(1)
sigma=fit.Get().Parameter(2)
#print '{}, {}, {}'.format(peak,mean,sigma)
fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
mean=fit.Get().Parameter(1)
sigma=fit.Get().Parameter(2)
fitfunc.SetParameters(peak,mean,sigma,3*sigma,5);
fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
#breakzarray.append(fit.Get().Parameter(3))
#lengtharray.append(fit.Get().Parameter(4))
#breakzErr.append(fit.Get().ParError(3))
#lengthErr.append(fit.Get().ParError(4))

c.Print(remainder[0]+".pdf","")

#c.Clear()
#outfile.cd()
#graph=TGraph(len(massarray),massarray,breakzarray)
#graph=TGraphErrors(len(massarray),massarray,breakzarray,zeroArr,breakzErr)
#graph.Draw("A*")
#graph.SetTitle("Tail Z")
#graph.GetXaxis().SetTitle("mass [GeV]")
#graph.GetYaxis().SetTitle("tail Z [mm]")
#graph.Fit("pol3")
#graph.Write("breakz")
#c.Print(remainder[0]+".pdf","Title:tailz")

#graph=TGraphErrors(len(massarray),massarray,lengtharray,zeroArr,lengthErr)
#graph.Draw("A*")
#graph.SetTitle("Tail length")
#graph.GetXaxis().SetTitle("mass [GeV]")
#graph.GetYaxis().SetTitle("tail length [mm]")
#graph.Fit("pol3")
#graph.Write("length")
#c.Print(remainder[0]+".pdf","Title:length")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

