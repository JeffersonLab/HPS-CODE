#!/usr/bin/env python
import sys
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
inFile = TFile(sys.argv[2])
events = inFile.Get("cut")

outfile = TFile(sys.argv[1]+".root","RECREATE")
events.SetLineColor(1)
events.Draw("tarM>>mass200(200,0,0.1)","rank==1&&tarP>0.8*1.056","goff")
events.Draw("tarM>>mass500(500,0,0.1)","rank==1&&tarP>0.8*1.056","goff")
events.Draw("tarM>>mass1000(1000,0,0.1)","rank==1&&tarP>0.8*1.056","goff")
events.Draw("tarM>>mass2000(2000,0,0.1)","rank==1&&tarP>0.8*1.056","goff")
#gDirectory.Get("mass200").Write()
#massHist = gDirectory.Get("mass")
#massHist.Write()
outfile.Write()
outfile.Close()
