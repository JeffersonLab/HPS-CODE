#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TChain, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooWorkspace, RooAbsData, RooGlobalFunc, RooFit, RooAbsReal, RooArgList, gPad

#author Sho Uemera
#author Matt Solt
#This script plots vertex resolution as a function of mass
def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-t: tuple name (default "ntuple")'
    print '\t-m: number of mass bins'
    print '\t-e: beam energy'
    print '\t-z: position of target in z'
    print '\t-w: width of mass bins'
    print '\t-c: apply cuts'
    print '\t-h: this help message'
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 't:m:e:z:w:ch')

#Default parameters
tupleName = "ntuple"
massVar = "uncM"
applyCut=False
ebeam=1.056
ztarg=0.5
n_massbins=10
masscut=0.005

for opt, arg in options:
    if opt=='-t':
        tupleName= str(arg)
    if opt=='-m':
        n_massbins= int(arg)
    if opt=='-e':
        ebeam= float(arg)
    if opt=='-z':
        ztarg= float(arg)
    if opt=='-w':
        masscut= float(arg)
    if opt=='-c':
        applyCut= True
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder) < 2):
        print_usage()
        sys.exit()

cut = "isPair1"

#If apply cut, apply the cut below
#This can be adjusted manually
if(applyCut):
    cut = "isPair1&&eleClY*posClY<0&&uncP>0.8*{0}&&max(eleTrkChisq,posTrkChisq)<60&&eleP<0.75*{0}&&bscChisq<10\
    &&bscChisq-uncChisq<5&&uncP<1.15*{0}&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-eleTrkT-43)<4\
    &&abs(posClT-posTrkT-43)<4&&abs(eleClT-posClT)<2&&eleHasL2&&posHasL2&&eleHasL1&&posHasL1\
    &&min(eleMinPositiveIso+0.5*(eleTrkZ0+{1}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{1}*posPY/posP)*sign(posPY))>0\
    &&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0+{1}*posPX/posP<1.5".format(ebeam,ztarg)

events = TChain(tupleName)
for i in range(1,len(remainder)):
    events.Add(remainder[i])

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
gStyle.SetOptStat(1111)
c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

#Draw 2D vertex plot
events.Draw("uncVZ:{0}>>hnew(100,0,{1},100,-50,50)".format(massVar,ebeam*0.1),cut,"colz")
hnew = ROOT.gROOT.FindObject("hnew")
hnew.SetTitle("Vertex Z vs Mass")
hnew.GetXaxis().SetTitle("mass [GeV]")
hnew.GetYaxis().SetTitle("Vertex [mm]")
gStyle.SetOptStat(0)
hnew.Write("2D_vertex_plot")
c.Print(remainder[0]+".pdf")

#Define fit function
fitfunc = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))")
fitfunc.SetParName(0,"Amplitude")
fitfunc.SetParName(1,"Mean")
fitfunc.SetParName(2,"Sigma")
fitfunc.SetParName(3,"Tail Z")
fitfunc.SetParName(4,"Tail length")

gPad.SetLogy(1)
events.Draw("uncVZ>>total_fit_params(200,-50,50)",cut,"")
total_fit_params = ROOT.gROOT.FindObject("total_fit_params")
total_fit_params.SetTitle("Vertex Z")
total_fit_params.GetXaxis().SetTitle("Vertex [mm]")

h1d = gDirectory.Get("total_fit_params")
fit=h1d.Fit("gaus","QS")
peak=fit.Get().Parameter(0)
mean=fit.Get().Parameter(1)
sigma=fit.Get().Parameter(2)
fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
mean=fit.Get().Parameter(1)
sigma=fit.Get().Parameter(2)
fitfunc.SetParameters(peak,mean,sigma,3*sigma,5);
fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
total_fit_params.Write("total_fit_params")
c.Print(remainder[0]+".pdf")

#Setup arrays
massarray=array.array('d')
zeroArr=array.array('d')
sigmaarray=array.array('d')
breakzarray=array.array('d')
lengtharray=array.array('d')
sigmaErr=array.array('d')
breakzErr=array.array('d')
lengthErr=array.array('d')
minmass=0.02
maxmass=0.06

#Loop over masses
for i in range(0,n_massbins):
    mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
    massarray.append(mass)
    zeroArr.append(0)
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw("uncVZ:{0}>>hnew2d(100,0,{1},100,-50,50)".format(massVar,ebeam*0.1),"abs({0}-{1})<{2}/2&&{3}".format(massVar,mass,masscut,cut),"colz")
    hnew2d = ROOT.gROOT.FindObject("hnew2d")
    hnew2d.SetTitle("Vertex Z vs Mass (mass in {0} - {1} GeV)".format(mass-masscut/2.,mass+masscut/2.))
    hnew2d.GetXaxis().SetTitle("mass [GeV]")
    hnew2d.GetYaxis().SetTitle("Vertex [mm]")
    gStyle.SetOptStat(0)
    c.cd(2)
    gPad.SetLogy(1)
    events.Draw("uncVZ>>fit_params(200,-50,50)","abs({0}-{1})<{2}/2&&{3}".format(massVar,mass,masscut,cut),"")
    fit_params = ROOT.gROOT.FindObject("fit_params")
    fit_params.SetTitle("Vertex Z (mass in {0} - {1} GeV)".format(mass-masscut/2.,mass+masscut/2.))
    fit_params.GetXaxis().SetTitle("Vertex [mm]")

    h1d = gDirectory.Get("fit_params")
    fit=h1d.Fit("gaus","QS")
    peak=fit.Get().Parameter(0)
    mean=fit.Get().Parameter(1)
    sigma=fit.Get().Parameter(2)
    fit=h1d.Fit("gaus","QS","",mean-3*sigma,mean+3*sigma)
    mean=fit.Get().Parameter(1)
    sigma=fit.Get().Parameter(2)
    fitfunc.SetParameters(peak,mean,sigma,3*sigma,5);
    fit=h1d.Fit(fitfunc,"LSQIM","",mean-2*sigma,mean+10*sigma)
    sigmaarray.append(fit.Get().Parameter(2))
    breakzarray.append(fit.Get().Parameter(3))
    lengtharray.append(fit.Get().Parameter(4))
    sigmaErr.append(fit.Get().ParError(2))
    breakzErr.append(fit.Get().ParError(3))
    lengthErr.append(fit.Get().ParError(4))

    fit_params.Write("fit {0} GeV".format(mass))
    c.Print(remainder[0]+".pdf","Title:mass_{0}".format(mass))

c.Clear()
outfile.cd()

gPad.SetLogy(0)
graph=TGraphErrors(len(massarray),massarray,sigmaarray,zeroArr,sigmaErr)
graph.Draw("A*")
graph.SetTitle("Vertex Resolution")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("sigma [mm]")
graph.Write("sigmaz")
c.Print(remainder[0]+".pdf","Title:sigmaz")

graph=TGraphErrors(len(massarray),massarray,breakzarray,zeroArr,breakzErr)
graph.Draw("A*")
graph.SetTitle("Tail Z")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("tail Z [mm]")
graph.Write("breakz")
c.Print(remainder[0]+".pdf","Title:tailz")

graph=TGraphErrors(len(massarray),massarray,lengtharray,zeroArr,lengthErr)
graph.Draw("A*")
graph.SetTitle("Tail length")
graph.GetXaxis().SetTitle("mass [GeV]")
graph.GetYaxis().SetTitle("tail length [mm]")
graph.Write("length")
c.Print(remainder[0]+".pdf","Title:length")

c.Print(remainder[0]+".pdf]")
outfile.Close()
sys.exit(0)