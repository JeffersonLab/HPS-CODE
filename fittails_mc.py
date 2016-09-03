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
    print "\nUsage: {0} <output basename> <input ROOT file> <acceptance ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

cutfile=""

for opt, arg in options:
    if opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)!=3):
        print_usage()
        sys.exit()


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

fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))")
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")

massarray=array.array('d')
breakzarray=array.array('d')
lengtharray=array.array('d')
n_massbins=50
minmass=0.021
maxmass=0.06
for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massarray.append(mass)
    p0 = acceptanceFile.Get("mres_l1_p0").GetFunction("pol1").Eval(mass)
    p1 = acceptanceFile.Get("mres_l1_p1").GetFunction("pol1").Eval(mass)
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw("uncVZ:uncM>>hnew2d(100,0,0.1,100,-50,50)","abs(uncM-{0})<1.25*({1}+{2}*uncVZ)".format(mass,p0,p1),"colz")
    c.cd(2)
    gPad.SetLogy(1)
    events.Draw("uncVZ>>hnew1d(200,-50,50)","abs(uncM-{0})<1.25*({1}+{2}*uncVZ)".format(mass,p0,p1),"colz")

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
    breakzarray.append(fit.Get().Parameter(3))
    lengtharray.append(fit.Get().Parameter(4))


    c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))

c.Clear()
outfile.cd()
graph=TGraph(len(massarray),massarray,breakzarray)
graph.Draw("AL*")
graph.SetTitle("Tail Z")
graph.Fit("pol3")
graph.Write("breakz")
c.Print(remainder[0]+".pdf","Title:tailz")

graph=TGraph(len(massarray),massarray,lengtharray)
graph.Draw("AL*")
graph.SetTitle("Tail length")
graph.Fit("pol3")
graph.Write("length")
c.Print(remainder[0]+".pdf","Title:length")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

