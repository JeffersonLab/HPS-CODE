#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, TLegend
from cut_utils import makePlots, allBut, makeCutString, flipCut
print sys.argv[2]
inFile = TFile(sys.argv[2])
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
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

cuts=["abs(uncM-0.03)<0.0026&&eleHasL1&&posHasL1&&uncP>0.8*1.056",
        "max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&uncP<1.15*1.056&&eleP<0.75*1.056",
        "max(eleTrkChisq,posTrkChisq)<30",
        "bscChisq<10&&bscChisq-uncChisq<5",
        "min(eleMinPositiveIso+0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0-5*posPY/posP)*sign(posPY))>0",
        "abs(eleP-posP)/(eleP+posP)<0.4",
        "posTrkD0-5*posPX/posP<1.5"
        ]
cutnames=["selection cuts",
        "base cuts",
        "track chisq",
        "vertex chisq",
        "isolation",
        "momentum asymmetry",
        "positron DOCA"
        ]

c.Print(sys.argv[1]+".pdf[")

#events.Draw("triEndZ>>base1d(100,-5,100)",cuts[0],"colz,goff")
#base1d = gDirectory.Get("base1d")

def plotstuff(cut1,cut2,cut3,cutname):
    events.Draw("uncVZ>>h1(150,-50,100)",cut1,"colz")
    events.Draw("uncVZ>>h2(150,-50,100)",cut2,"colz,same")
    events.Draw("uncVZ>>h3(150,-50,100)",cut3,"colz,same")

    leg = TLegend(0.7,0.75,0.9,0.9)
    leg.AddEntry(gDirectory.Get("h1"),"passed all but this cut")
    leg.AddEntry(gDirectory.Get("h2"),"passed all cuts")
    leg.AddEntry(gDirectory.Get("h3"),"failed this cut")
    leg.Draw()
    gDirectory.Get("h1").SetLineColor(1)
    gDirectory.Get("h2").SetLineColor(4)
    gDirectory.Get("h3").SetLineColor(2)
    gDirectory.Get("h1").SetTitle(cutname)
    gDirectory.Get("h1").GetXaxis().SetTitle("vertex Z [mm]")
    c.Print(sys.argv[1]+".pdf")

def plotstuff2(cut1,cut2,cutname):
    events.Draw("uncVZ>>h1(150,-50,100)",cut1,"colz")
    events.Draw("uncVZ>>h2(150,-50,100)",cut2,"colz,same")

    leg = TLegend(0.7,0.75,0.9,0.9)
    leg.AddEntry(gDirectory.Get("h1"),"after base cuts")
    leg.AddEntry(gDirectory.Get("h2"),"after vertexing cuts")
    leg.Draw()
    gDirectory.Get("h1").SetLineColor(1)
    gDirectory.Get("h2").SetLineColor(2)
    gDirectory.Get("h1").SetTitle(cutname)
    gDirectory.Get("h1").GetXaxis().SetTitle("vertex Z [mm]")
    c.Print(sys.argv[1]+".pdf")

def plotstuff3(cuts,cutname):
    leg = TLegend(0.7,0.75,0.9,0.9)
    events.Draw("uncVZ>>h1(150,-50,100)",makeCutString(cuts[0:2]),"colz")
    leg.AddEntry(gDirectory.Get("h1"),"after base cuts")
    gDirectory.Get("h1").SetLineColor(1)
    gDirectory.Get("h1").SetTitle(cutname)
    for i in range(2,len(cuts)):
        events.Draw("uncVZ>>h{0}(150,-50,100)".format(i),makeCutString(cuts[0:i+1]),"colz,same")
        leg.AddEntry(gDirectory.Get("h{0}".format(i)),"after {0} cut".format(cutnames[i]))
        gDirectory.Get("h{0}".format(i)).SetLineColor(i)

    leg.Draw()
    gDirectory.Get("h1").SetTitle(cutname)
    gDirectory.Get("h1").GetXaxis().SetTitle("vertex Z [mm]")
    c.Print(sys.argv[1]+".pdf")

c.SetLogy(1)
plotstuff2(makeCutString(cuts[0:2]),makeCutString(cuts),"|m(e+e-)-0.03|<0.0026")
#plotstuff(makeCutString(cuts),"allcuts")
plotstuff3(cuts,"cuts")

for i in range(2,len(cuts)):
    cutstring = flipCut(cuts,i)
    cutname = cutnames[i]
    plotstuff(makeCutString(cuts,i),makeCutString(cuts),flipCut(cuts,i),cutname)

c.Print(sys.argv[1]+".pdf]")
