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

cuts=["triP>0.8*1.056&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<30&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&uncP>0.8*1.056",
        "bscChisq<10",
        "max(eleTrkChisq,posTrkChisq)<30",
        "minPositiveIso-0.02*bscChisq>0.5",
        "eleP<0.8",
        "abs(eleFirstHitX-posFirstHitX+2)<7",
        "abs(eleP-posP)/(eleP+posP)<0.4",
        "posTrkD0<1.5"]

c.Print(sys.argv[1]+".pdf[")
events.Draw("uncVZ:triEndZ>>(100,-5,100,100,-50,100)",cuts[0],"colz")
c.Print(sys.argv[1]+".pdf")
events.Draw("uncVZ:triEndZ>>(100,-5,100,100,-50,100)",makeCutString(cuts),"colz")
c.Print(sys.argv[1]+".pdf")
for i in range(1,len(cuts)):
    events.Draw("uncVZ:triEndZ>>(100,-5,100,100,-50,100)",flipCut(cuts,i),"colz")
    c.Print(sys.argv[1]+".pdf")

c.Print(sys.argv[1]+".pdf]")
