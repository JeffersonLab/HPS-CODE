#!/usr/bin/env python
import sys
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, TF1
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <input ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=1.056

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
inFile = TFile(remainder[1])
#outFile = TFile(remainder[0]+".root","RECREATE")
events = inFile.Get("ntuple")

c = TCanvas("c","c",1200,900);
c.Print(remainder[0]+".pdf[")

fitfunc =TF1("fitfunc","[0]/x+[1]")

def plotstuff(var,cut,maxsig,plotname):
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw(var,cut,"colz")
    hnew = gDirectory.Get("hnew")
    hnew.FitSlicesY()
    hnew.SetTitle(plotname)
    hnew.GetXaxis().SetTitle("momentum [GeV]")
    hnew.GetYaxis().SetTitle("DOCA [mm]")
    hnew_1 = gDirectory.Get("hnew_2")
    c.cd(2)
    hnew_1.Draw()
    hnew_1.Fit("fitfunc","","",0.2,0.7)
    hnew_1.GetYaxis().SetRangeUser(0,maxsig)
    hnew_1.GetXaxis().SetTitle("momentum [GeV]")
    hnew_1.GetYaxis().SetTitle("DOCA resolution [mm]")
    c.Print(remainder[0]+".pdf","Title:top_yz")

plotstuff("eleTrkZ0-5*elePY/eleP:eleP>>hnew(100,0,1,100,-3,3)","",0.5,"Electron Y DOCA")
plotstuff("posTrkZ0-5*posPY/posP:posP>>hnew(100,0,1,100,-3,3)","",0.5,"Positron Y DOCA")
plotstuff("eleTrkZ0-5*elePY/eleP:eleP>>hnew(100,0,1,100,-3,3)","elePY>0",0.5,"Top Electron Y DOCA")
plotstuff("posTrkZ0-5*posPY/posP:posP>>hnew(100,0,1,100,-3,3)","posPY>0",0.5,"Top Positron Y DOCA")
plotstuff("eleTrkZ0-5*elePY/eleP:eleP>>hnew(100,0,1,100,-3,3)","elePY<0",0.5,"Bottom Electron Y DOCA")
plotstuff("posTrkZ0-5*posPY/posP:posP>>hnew(100,0,1,100,-3,3)","posPY<0",0.5,"Bottom Positron Y DOCA")

plotstuff("eleTrkD0-5*elePX/eleP:eleP>>hnew(100,0,1,100,-3,3)","",1.0,"Electron X DOCA")
plotstuff("posTrkD0-5*posPX/posP:posP>>hnew(100,0,1,100,-3,3)","",1.0,"Positron X DOCA")
plotstuff("eleTrkD0-5*elePX/eleP:eleP>>hnew(100,0,1,100,-3,3)","elePY>0",1.0,"Top Electron X DOCA")
plotstuff("posTrkD0-5*posPX/posP:posP>>hnew(100,0,1,100,-3,3)","posPY>0",1.0,"Top Positron X DOCA")
plotstuff("eleTrkD0-5*elePX/eleP:eleP>>hnew(100,0,1,100,-3,3)","elePY<0",1.0,"Bottom Electron X DOCA")
plotstuff("posTrkD0-5*posPX/posP:posP>>hnew(100,0,1,100,-3,3)","posPY<0",1.0,"Bottom Positron X DOCA")

gStyle.SetOptStat(0)
c.Clear()

events.Draw("eleP:posP>>h2d(100,0,1.0,100,0,1.0)","","colz")
hnew = gDirectory.Get("h2d")
hnew.SetTitle("all pairs")
hnew.GetXaxis().SetTitle("p(e-) [GeV]")
hnew.GetYaxis().SetTitle("p(e+) [GeV]")
c.Print(remainder[0]+".pdf")

c.SetLogz()
events.Draw("uncVZ:uncVY>>h2d(100,-5,5,100,-100,100)","uncP>0.8*1.056","colz")
hnew = gDirectory.Get("h2d")
hnew.SetTitle("p(e+e-)>0.8*E_beam")
hnew.GetXaxis().SetTitle("vertex Y [mm]")
hnew.GetYaxis().SetTitle("vertex Z [mm]")
c.Print(remainder[0]+".pdf")

events.Draw("uncVZ:uncM>>h2d(100,0,0.1,100,-100,100)","uncP>0.8*1.056","colz")
hnew = gDirectory.Get("h2d")
hnew.SetTitle("p(e+e-)>0.8*E_beam")
hnew.GetXaxis().SetTitle("m(e+e-) [GeV]")
hnew.GetYaxis().SetTitle("vertex Z [mm]")
c.Print(remainder[0]+".pdf")

c.Print(remainder[0]+".pdf]")

