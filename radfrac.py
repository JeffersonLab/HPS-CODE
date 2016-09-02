#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\n"
        sys.exit(0)


if (len(remainder)!=4):
        print sys.argv[0]+' <output basename> <RAD> <tritrig> <WAB>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
radFile = TFile(remainder[1])
triFile = TFile(remainder[2])
wabFile = TFile(remainder[3])
radEvents = radFile.Get("cut")
triEvents = triFile.Get("cut")
wabEvents = wabFile.Get("cut")
radEvents.SetWeight(1.0/((10e4/0.154e6)*10))
triEvents.SetWeight(1.0/(0.0682*375))
wabEvents.SetWeight(1.0/((9.5e4/0.7e9)*995))

c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")


radEvents.Draw("uncM>>rad(100,0,0.1)","triPair1P>0.8*1.056")
c.Print(remainder[0]+".pdf","Title:data_1d")
triEvents.Draw("uncM>>tri(100,0,0.1)","")
c.Print(remainder[0]+".pdf","Title:data_1d")
wabEvents.Draw("uncM>>wab(100,0,0.1)","")
c.Print(remainder[0]+".pdf","Title:data_1d")
radHist = gDirectory.Get("rad")
triHist = gDirectory.Get("tri")
wabHist = gDirectory.Get("wab")
totalHist = triHist.Clone("total")
totalHist.Add(wabHist)
totalHist.Draw()
c.Print(remainder[0]+".pdf","Title:data_1d")
radfracHist = radHist.Clone("radfrac")
radfracHist.Divide(totalHist)
radfracHist.Draw()
radfracHist.GetYaxis().SetRangeUser(0,0.5)
radfracHist.Fit("pol3","","",0.015,0.08)
c.Print(remainder[0]+".pdf","Title:data_1d")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

