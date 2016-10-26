#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, TLegend, THStack
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

cuts=["isPair1&&max(eleMatchChisq,posMatchChisq)<30&&eleClY*posClY<0&&eleHasL1&&posHasL1&&uncP>0.8*1.056",
        "max(abs(eleClT-eleTrkT-43),abs(posClT-posTrkT-43))<4",
        "max(eleMatchChisq,posMatchChisq)<10",
        "max(eleTrkChisq,posTrkChisq)<50",
        "eleP<0.8",
        "tarP<1.2"
        ]
cutnames=["selection cuts",
        "time match",
        "position match",
        "track chisq",
        "elastics",
        "momentum sum"
        ]

c.Print(sys.argv[1]+".pdf[")

#events.Draw("triEndZ>>base1d(100,-5,100)",cuts[0],"colz,goff")
#base1d = gDirectory.Get("base1d")

def plotstuff(cut1,cut2,cut3,cutname):
    events.Draw("eleClT-posClT>>h1(200,-10,10)",cut1,"goff")
    events.Draw("eleClT-posClT>>h2(200,-10,10)",cut2,"goff")
    events.Draw("eleClT-posClT>>h3(200,-10,10)",cut3,"goff")

    hs = THStack("hs","Effect of "+cutname+" cut");
    hs.Add(gDirectory.Get("h1"))
    hs.Add(gDirectory.Get("h2"))
    hs.Add(gDirectory.Get("h3"))
    hs.Draw("nostack")
    leg = TLegend(0.6,0.75,0.9,0.9)
    leg.AddEntry(gDirectory.Get("h1"),"passed all but this cut")
    leg.AddEntry(gDirectory.Get("h2"),"passed all cuts")
    leg.AddEntry(gDirectory.Get("h3"),"failed this cut")
    leg.Draw()
    gDirectory.Get("h1").SetLineColor(1)
    gDirectory.Get("h2").SetLineColor(4)
    gDirectory.Get("h3").SetLineColor(2)
    hs.GetXaxis().SetTitle("tEle-tPos [ns]")
    hs.GetYaxis().SetTitle("events/(0.1 ns)")
    c.Print(sys.argv[1]+".pdf")

def plotstuff2(cut1,cut2,cutname):
    events.Draw("eleClT-posClT>>h1(200,-10,10)",cut1,"goff")
    events.Draw("eleClT-posClT>>h2(200,-10,10)",cut2,"goff")

    hs = THStack("hs",cutname);
    hs.Add(gDirectory.Get("h1"))
    hs.Add(gDirectory.Get("h2"))
    hs.Draw("nostack")
    leg = TLegend(0.6,0.75,0.9,0.9)
    leg.AddEntry(gDirectory.Get("h1"),"after base cuts")
    leg.AddEntry(gDirectory.Get("h2"),"after vertexing cuts")
    leg.Draw()
    gDirectory.Get("h1").SetLineColor(1)
    gDirectory.Get("h2").SetLineColor(2)
    hs.GetXaxis().SetTitle("tEle-tPos [ns]")
    hs.GetYaxis().SetTitle("events/(0.1 ns)")
    c.Print(sys.argv[1]+".pdf")

def plotstuff3(cuts,cutname):
    hs = THStack("hs",cutname);
    hs.Add(gDirectory.Get("h1"))
    leg = TLegend(0.6,0.75,0.9,0.9)
    events.Draw("eleClT-posClT>>h0(200,-10,10)",cuts[0],"goff")
    leg.AddEntry(gDirectory.Get("h0"),"after base cuts")
    hs.Add(gDirectory.Get("h0"))
    gDirectory.Get("h0").SetLineColor(1)
    #gDirectory.Get("h1").SetTitle(cutname)
    for i in range(1,len(cuts)):
        events.Draw("eleClT-posClT>>h{0}(100,-10,10)".format(i),makeCutString(cuts[0:i+1]),"goff")
        leg.AddEntry(gDirectory.Get("h{0}".format(i)),"after {0} cut".format(cutnames[i]))
        hs.Add(gDirectory.Get("h{0}".format(i)))
        gDirectory.Get("h{0}".format(i)).SetLineColor(i+1)

    hs.Draw("nostack")
    leg.Draw()
    hs.GetXaxis().SetTitle("tEle-tPos [ns]")
    hs.GetYaxis().SetTitle("events/(0.1 ns)")
    c.Print(sys.argv[1]+".pdf")

c.SetLogy(1)
plotstuff2(cuts[0],makeCutString(cuts),"Effect of cuts")
#plotstuff(makeCutString(cuts),"allcuts")
plotstuff3(cuts,"Effect of cuts")

for i in range(1,len(cuts)):
    cutstring = flipCut(cuts,i)
    cutname = cutnames[i]
    plotstuff(makeCutString(cuts,i),makeCutString(cuts),flipCut(cuts,i),cutname)

c.Print(sys.argv[1]+".pdf]")
