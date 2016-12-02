#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
from cut_utils import makePlots, allBut, makeCutString, flipCut
print sys.argv[2]
inFile = TFile(sys.argv[2])
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
gROOT.SetBatch(True)
gStyle.SetOptStat(1)
#chain = TChain("ntuple")
#for i in sys.argv[2:]:
#	chain.Add(i)
#chain.Merge(sys.argv[1])


c = TCanvas("c","c",1200,900);
#c.cd()
#events = chain
#events = chain.CopyTree("uncM>0.03&&uncM<0.04")
events = inFile.Get("ntuple")
#goodEvents = events.CopyTree("abs(uncVZ)*uncM<0.1")
#badEvents = events.CopyTree("uncVZ*uncM>0.5")
outFile = TFile(sys.argv[1]+".root","RECREATE")

cuts=["triP>0.8*1.056&&eleHasL1&&posHasL1&&uncP>0.8*1.056",
        "max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&uncP<1.15*1.056",
        "bscChisq<10",
        "max(eleTrkChisq,posTrkChisq)<30",
        #"minPositiveIso-0.02*bscChisq>0.5",
        "eleP<0.8",
        #"abs(eleFirstHitX-posFirstHitX+2)<7",
        "abs(eleP-posP)/(eleP+posP)<0.4",
        "posTrkD0-5*posPX/posP<1.5",
        "min(eleMinPositiveIso+0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0-5*posPY/posP)*sign(posPY))>0",
        "bscChisq-uncChisq<5"]

c.Print(sys.argv[1]+".pdf[")

events.Draw("triEndZ>>base1d(100,-5,100)",cuts[0],"colz,goff")
base1d = gDirectory.Get("base1d")

def plotstuff(cutstring,cutname):
    c.Clear()
    c.Divide(1,3)
    c.cd(1)
    events.Draw("uncVZ:triEndZ>>plot2d(100,-5,100,100,-50,100)",cutstring,"colz")
    c.cd(2)
    events.Draw("triEndZ>>plot1d(100,-5,100)",cutstring,"colz")
    eff=gDirectory.Get("plot1d").Clone("effloss")
    eff.Sumw2()
    eff.Divide(base1d)
    c.cd(3)
    eff.Draw()
    c.Modified()
    c.Print(sys.argv[1]+".pdf","Title:"+cutname)

plotstuff(cuts[0],"basecuts")
plotstuff(makeCutString(cuts),"allcuts")

for i in range(1,len(cuts)):
    cutstring = flipCut(cuts,i)
    cutname = cuts[i]
    plotstuff(cutstring,cutname)

c.Print(sys.argv[1]+".pdf]")
