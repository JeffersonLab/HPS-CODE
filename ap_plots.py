#!/usr/bin/env python
import sys
import getopt
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1

def print_usage():
    print "\nUsage: {0} <output file basename> <recon A' ROOT file> <slic A' ROOT file".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=1.056
mass=0.030

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=3:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
gStyle.SetOptFit(1)
inFile = TFile(remainder[1])
inFile2 = TFile(remainder[2])
#outFile = TFile(remainder[0]+".root","RECREATE")
isFullTuple = False
events = inFile.Get("cut")
if events==None:
    isFullTuple = True
    events = inFile.Get("ntuple")
events2 = inFile2.Get("ntuple")

c = TCanvas("c","c",1200,900);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

#exppol3=TF1("exppol3","exp(pol3(0))",-5,100)
exppol4=TF1("exppol4","min(exp(pol3(0)),2)",-5,100)
#exppol4.SetParameters(-5,0,-0.001,0)

c.Clear()
c.Divide(1,2)
c.cd(1)
gPad.SetLogy(1)
events2.Draw("triEndZ>>prodZ(50,-5,100)","triP>0.8*1.056","colz,goff")
prodZ = gDirectory.Get("prodZ")
prodZ.GetXaxis().SetTitle("vertex Z [mm]");
prodZ.GetYaxis().SetTitle("generated events");
prodZ.Fit("expo","L")
prodZ.Draw()
prodZ.Write("prodz")
c.cd(2)
events2.Draw("triP>>hnew(100,0,1.5)","","colz,goff")
hnew = gDirectory.Get("hnew")
hnew.GetXaxis().SetTitle("p(A') [GeV]");
hnew.GetYaxis().SetTitle("generated events");
hnew.Draw()
hnew.Write("esum")
c.Print(remainder[0]+".pdf","Title:top_yz")


c.Clear()
c.Divide(1,2)
c.cd(1)
#gPad.SetLogy(1)
events.Draw("triEndZ>>hnew(50,-5,100)","triP>0.8*1.056&&uncP>0.8*1.056","colz,goff")
hnew = gDirectory.Get("hnew")
hnew.GetXaxis().SetTitle("vertex Z [mm]");
hnew.GetYaxis().SetTitle("reconstructed events");
hnew.Draw()
c.cd(2)
eff=hnew.Clone("eff")
eff.Sumw2()
eff.Divide(prodZ)
eff.Fit("exppol4","QL")
eff.Fit("exppol4","QLN")
eff.Fit("exppol4","IM")
effAtZero=exppol4.Eval(-5)
eff.Write("eff_all_unscaled")
eff.Scale(1.0/effAtZero)
eff.Fit("exppol4","QL")
eff.Fit("exppol4","QLN")
eff.Fit("exppol4","IM")
eff.GetXaxis().SetTitle("vertex Z [mm]");
eff.GetYaxis().SetTitle("efficiency");
eff.Draw()
eff.GetYaxis().SetRangeUser(0,1.2)
eff.Write("eff_all")
c.Print(remainder[0]+".pdf","Title:top_yz")

c.Clear()
c.Divide(1,2)
c.cd(1)
gPad.SetLogz(1)
events.Draw("uncVZ-triEndZ:triEndZ>>hnew(50,-5,100,50,-20,20)","triP>0.8*1.056&&uncP>0.8*1.056","colz")
hnew = gDirectory.Get("hnew")
hnew.GetXaxis().SetTitle("vertex Z [mm]");
hnew.GetYaxis().SetTitle("vertex Z residual [mm]");
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_2")
c.cd(2)
hnew_1.GetXaxis().SetTitle("vertex Z [mm]");
hnew_1.GetYaxis().SetTitle("vertex Z resolution [mm]");
hnew_1.Draw()
hnew_1.Fit("pol1","","",-5,100)
hnew_1.GetYaxis().SetRangeUser(0,20)
hnew_1.Write("zres_all")
c.Print(remainder[0]+".pdf","Title:top_yz")

c.Clear()
c.Divide(1,2)
c.cd(1)
gPad.SetLogz(1)
events.Draw("uncM-triM:triEndZ>>hnew(50,-5,100,50,-0.02,0.02)","triP>0.8*1.056&&uncP>0.8*1.056","colz")
hnew = gDirectory.Get("hnew")
hnew.GetXaxis().SetTitle("vertex Z [mm]");
hnew.GetYaxis().SetTitle("mass residual [GeV]");
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_2")
c.cd(2)
hnew_1.GetXaxis().SetTitle("vertex Z [mm]");
hnew_1.GetYaxis().SetTitle("mass resolution [GeV]");
hnew_1.Draw()
hnew_1.Fit("pol1","","",-5,100)
hnew_1.GetYaxis().SetRangeUser(0,0.01)
hnew_1.Write("mres_all")
c.Print(remainder[0]+".pdf","Title:top_yz")

if isFullTuple:
    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    events.Draw("uncM-triM>>hnew_1(50,-0.02,0.02)","triP>0.8*1.056&&uncP>0.8*1.056&&abs(triEndZ-30)<5","colz")
    hnew_1 = gDirectory.Get("hnew_1")
    hnew_1.GetXaxis().SetTitle("mass residual [GeV]");
    #hnew_1.GetYaxis().SetTitle("mass resolution [GeV]");
    hnew_1.Draw()
    c.cd(2)
    events.Draw("uncM-triM:elePX/eleP-posPX/posP>>hnew(50,-0.1,0.1,50,-0.02,0.02)","triP>0.8*1.056&&uncP>0.8*1.056&&abs(triEndZ-30)<5","colz")
    hnew = gDirectory.Get("hnew")
    hnew.GetXaxis().SetTitle("opening angle in X [rad]");
    hnew.GetYaxis().SetTitle("mass residual [GeV]");
    c.Print(remainder[0]+".pdf","Title:top_yz")

    c.Clear()
    c.Divide(1,2)
    c.cd(1)
    gPad.SetLogz(1)
    events.Draw("uncM-0.15e-3*(elePX/eleP-posPX/posP)*triEndZ/triM-triM:triEndZ>>hnew(50,-5,100,50,-0.02,0.02)","triP>0.8*1.056&&uncP>0.8*1.056","colz")
    hnew = gDirectory.Get("hnew")
    hnew.GetXaxis().SetTitle("vertex Z [mm]");
    hnew.GetYaxis().SetTitle("mass residual [GeV]");
    hnew.FitSlicesY()
    hnew_1 = gDirectory.Get("hnew_2")
    c.cd(2)
    hnew_1.GetXaxis().SetTitle("vertex Z [mm]");
    hnew_1.GetYaxis().SetTitle("mass resolution [GeV]");
    hnew_1.Draw()
    hnew_1.Fit("pol1","","",-5,100)
    hnew_1.GetYaxis().SetRangeUser(0,0.01)
    hnew_1.Write("mres_all")
    c.Print(remainder[0]+".pdf","Title:top_yz")

c.Print(remainder[0]+".pdf]")

outfile.Write()
outfile.Close()

