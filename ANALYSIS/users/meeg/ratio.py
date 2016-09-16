#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
print sys.argv[2]
print sys.argv[3]
file1 = TFile(sys.argv[2])
file2 = TFile(sys.argv[3])
file3 = TFile(sys.argv[1]+".root","RECREATE")
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
gStyle.SetOptStat(0)
#chain = TChain("ntuple")
#for i in sys.argv[2:]:
#	chain.Add(i)
#chain.Merge(sys.argv[1])

cuts="uncP>0.5*1.056&&posP>0.2&&eleP>0.2&&posP<0.8&&eleP<0.8"
tweak="&&0.8+12.5*(eleP-0.033)^2>(event%10000)/1000&&7+3*posP>(event%100000)/10000"
#tweak="1"
c = TCanvas("c","c",1200,900);
#c.cd()
#events = chain
#events = chain.CopyTree("uncM>0.03&&uncM<0.04")
events1 = file1.Get("ntuple")
events2 = file2.Get("ntuple")
#goodEvents = events.CopyTree("abs(uncVZ)*uncM<0.1")
#badEvents = events.CopyTree("uncVZ*uncM>0.5")
events1.Draw("eleP>>eleh1(100,0.1,1)",cuts)
events2.Draw("eleP>>eleh2(100,0.1,1)",cuts+tweak)
h1=gDirectory.Get("eleh1")
h2=gDirectory.Get("eleh2")
h1.Divide(h2)
h1.Draw()
c.SaveAs(sys.argv[1]+"_ele.png")


events1.Draw("posP>>h1(100,0.1,1)",cuts)
events2.Draw("posP>>h2(100,0.1,1)",cuts+tweak)
h1=gDirectory.Get("h1")
h2=gDirectory.Get("h2")
h1.Divide(h2)
h1.Draw()
c.SaveAs(sys.argv[1]+"_pos.png")

events1.Draw("uncP>>h1(100,0.1,1.2)",cuts)
events2.Draw("uncP>>h2(100,0.1,1.2)",cuts+tweak)
h1=gDirectory.Get("h1")
h2=gDirectory.Get("h2")
h1.Divide(h2)
h1.Draw()
c.SaveAs(sys.argv[1]+"_esum.png")

events1.Draw("eleP:posP>>h1(100,0.1,1,100,0.1,1)",cuts)
events2.Draw("eleP:posP>>h2(100,0.1,1,100,0.1,1)",cuts+tweak)
h1=gDirectory.Get("h1")
h2=gDirectory.Get("h2")
h1.Divide(h2)
h1.Draw("colz")
c.SaveAs(sys.argv[1]+"_2d.png")
file3.Write()
file3.Close()
