#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend

def plotStuff(plotList,plotstring, cutstring, plotfile, plotname, xlabel, ylabel, unitnorm):
    leg = TLegend(0.0,0.75,0.2,0.9)
    isFirst = True
    for dataset in plotList:
        dataset[0].Draw(plotstring.format(dataset[1]),cutstring,"goff")
        hist = gDirectory.Get(dataset[1])
        #hist.Sumw2()
        if unitnorm:
            hist.Scale(1.0/hist.Integral())
        else:
            hist.Scale(1.0/dataset[2])
        hist.SetLineColor(dataset[3])
        leg.AddEntry(hist,dataset[4])
        if isFirst:
            hist.GetXaxis().SetTitle(xlabel)
            hist.GetYaxis().SetTitle(ylabel)
            hist.Draw()
        else:
            hist.Draw("same")
        isFirst = False
    leg.Draw()
    c.Print(plotfile,plotname)

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\n"
        sys.exit(0)


if (len(remainder)!=3):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
mcFile = TFile(remainder[2])
dataFile = TFile(remainder[1])
mcEvents = mcFile.Get("ntuple")
dataEvents = dataFile.Get("ntuple")

plotList = []
plotList.append((mcEvents, "mc", (9.5e4/0.7e9)*899, 2, "wabv2-4062dz"))
plotList.append((dataEvents, "data", 4.40, 1, "5772"))

c.Print(remainder[0]+".pdf[")

dataEvents.Draw("eleP:phoClE>>(100,0,1.2,100,0,1.2)","eleP<0.85&&eleMatchChisq<5&&abs(eleClT-phoClT)<2&&phoClHits>=3","colz")
c.Print(remainder[0]+".pdf")
mcEvents.Draw("eleP:phoClE>>(100,0,1.2,100,0,1.2)","eleP<0.85&&eleMatchChisq<5&&abs(eleClT-phoClT)<2&&phoClHits>=3","colz")
c.Print(remainder[0]+".pdf")

plotStuff(plotList,"eleP+phoClE>>{0}(100,0.5,1.5)","eleP<0.85&&eleMatchChisq<5&&abs(eleClT-phoClT)<2&&phoClHits>=3", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0.0,1.2)","eleP<0.85&&eleMatchChisq<5&&abs(eleClT-phoClT)<2&&phoClHits>=3", remainder[0]+".pdf","Title:eleP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"phoClE>>{0}(100,0.0,1.0)","eleP<0.85&&eleMatchChisq<5&&abs(eleClT-phoClT)<2&&phoClHits>=3", remainder[0]+".pdf","Title:eleP", "p [GeV]", "Normalized rate [nb]", False)

c.Print(remainder[0]+".pdf]")
