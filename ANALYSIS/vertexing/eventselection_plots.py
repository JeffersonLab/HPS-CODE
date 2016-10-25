#!/usr/bin/env python
import sys
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
gStyle.SetOptFit(1)
inFile = TFile(sys.argv[2])
#outFile = TFile(sys.argv[1]+".root","RECREATE")
events = inFile.Get("ntuple")
events.AddFriend("cut",sys.argv[3])

c = TCanvas("c","c",1200,900);
c.Print(sys.argv[1]+".pdf[")

events.SetLineColor(1)
events.Draw("eleTrkChisq>>(200,0,60)","rank==1","")
events.SetLineColor(2)
events.Draw("eleTrkChisq","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:eleTrkChisq")

events.SetLineColor(1)
events.Draw("posTrkChisq>>(200,0,60)","rank==1","")
events.SetLineColor(2)
events.Draw("posTrkChisq","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:posTrkChisq")

events.SetLineColor(1)
events.Draw("eleP>>(200,0,1.6)","rank==1","")
events.SetLineColor(2)
events.Draw("eleP","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:eleP")

events.SetLineColor(1)
events.Draw("posP>>(200,0,1.6)","rank==1","")
events.SetLineColor(2)
events.Draw("posP","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:posP")

events.SetLineColor(1)
events.Draw("tarVX>>(200,-0.5,0.5)","rank==1","")
events.SetLineColor(2)
events.Draw("tarVX","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:tarVX")

events.SetLineColor(1)
events.Draw("tarVY>>(200,-0.1,0.1)","rank==1","")
events.SetLineColor(2)
events.Draw("tarVY","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:tarVY")

events.SetLineColor(1)
events.Draw("tarP>>(200,0,1.6)","rank==1","")
events.SetLineColor(2)
events.Draw("tarP","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf","Title:tarP")

events.SetLineColor(1)
events.Draw("tarM>>(200,0,0.1)","rank==1","")
events.SetLineColor(2)
events.Draw("tarM","rank==1&&tarP>0.8*1.056","same")
c.Print(sys.argv[1]+".pdf)","Title:tarM")


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
