#!/usr/bin/env python
import sys
import getopt
import math
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1

def print_usage():
    print "\nUsage: {0} <output file basename> <recon A' ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=2.3
mass=0.030

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        elif opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
inFile = TFile(remainder[1])
events = inFile.Get("cut")

c = TCanvas("c","c",1200,900)
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

#exppol4=TF1("exppol4","min(exp(pol3(0)),2)",-5,100)

c.Clear()
c.Divide(1,2)
c.cd(1)
gPad.SetLogz(1)
events.Draw("uncVZ-triEndZ:triEndZ>>hnew(50,-5,100,50,-20,20)","","colz")
hnew = gDirectory.Get("hnew")
hnew.GetXaxis().SetTitle("vertex Z [mm]")
hnew.GetYaxis().SetTitle("vertex Z residual [mm]")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_2")
c.cd(2)
hnew_1.GetXaxis().SetTitle("vertex Z [mm]")
hnew_1.GetYaxis().SetTitle("vertex Z resolution [mm]")
hnew_1.Draw()
hnew_1.Fit("pol1","","",-5,100)
hnew_1.GetYaxis().SetRangeUser(0,20)
hnew_1.Write("zres_all")
c.Print(remainder[0]+".pdf","Title:top_yz")

c.Clear()
c.Divide(1,2)
c.cd(1)
gPad.SetLogz(1)
events.Draw("uncM-triM:triEndZ>>hnew(50,-5,100,50,-0.02,0.02)","","colz")
hnew = gDirectory.Get("hnew")
hnew.SetTitle("Mass resolution, true and reconstructed")
hnew.GetXaxis().SetTitle("vertex Z [mm]")
hnew.GetYaxis().SetTitle("mass residual [GeV]")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_2")
c.cd(2)
hnew_1.SetTitle("")
hnew_1.GetXaxis().SetTitle("vertex Z [mm]")
hnew_1.GetYaxis().SetTitle("mass resolution [GeV]")
hnew_1.Draw()
hnew_1.Fit("pol1","","",-5,100)
hnew_1.GetYaxis().SetRangeUser(0,0.01)
hnew_1.Write("mres_all")
c.Print(remainder[0]+".pdf","Title:top_yz")

#hnew_3 = gDirectory.Get("hnew_3")
#c.cd(1)
c2 = TCanvas("c2","c2",1200,900)
events.Draw("uncM-triM>>hnew3(50,-0.02,0.02)")
hnew3 = ROOT.gROOT.FindObject("hnew3")
hnew3.SetTitle("Mass Residual")
hnew3.GetXaxis().SetTitle("mass residual [GeV]")
hnew3.Fit("gaus")
c2.Print(remainder[0]+".pdf","Title:top_yz")

c.Print(remainder[0]+".pdf]")

outfile.Write()
outfile.Close()

