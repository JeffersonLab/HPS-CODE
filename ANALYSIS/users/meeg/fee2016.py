#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend

def plotStuff(plotList,plotstring, cutstring, plotfile, plotname, xlabel, ylabel, unitnorm):
    leg = TLegend(0.0,0.85,0.2,1.0)
    isFirst = True
    for dataset in plotList:
        dataset[0].Draw(plotstring.format(dataset[1]),cutstring,"goff")
        hist = gDirectory.Get(dataset[1])
        hist.Sumw2()
        if unitnorm:
            hist.Scale(1.0/hist.Integral())
        else:
            hist.Scale(1.0/dataset[2])
            print "{0} {1} {2}".format(plotname,dataset[4],hist.Integral())
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


if (len(remainder)!=4):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <7807> <7808> <7809> <tritrig-beam-tri ROOT file> <tritrig lowerESum ROOT file> <tritrig ROOT file>".format(sys.argv[0])
print "{0} rate2016 7807_tri.root 7808_tri.root 7809_tri.root tritrig2016-beam-tri_tri.root tritrig2016_lowerESum_tri.root tritrig2016_tri.root"
data1File = TFile(sys.argv[2])
data2File = TFile(sys.argv[3])
data3File = TFile(sys.argv[4])
data1Events = data1File.Get("ntuple")
data2Events = data2File.Get("ntuple")
data3Events = data3File.Get("ntuple")

plotList = []
plotList.append((data3Events, "data3", 0.98*28230*0.00002562/0.1602, 4, "run 7809 (50 nA)"))
plotList.append((data1Events, "data1", 0.835*89719*0.00002562/0.1602, 1, "run 7807 (200 nA)"))
plotList.append((data2Events, "data2", 0.61*26617*0.00002562/0.1602, 2, "run 7808 (300 nA)"))

c.Print(remainder[0]+".pdf[")

c.SetLogy(1)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.1)","isSingle0&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.1)","isSingle0&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP_unitnorm", "angle [GeV]", "Unit normalized", True)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.1)","isSingle0&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.1)","isSingle0&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP_unitnorm", "angle [GeV]", "Unit normalized", True)

plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.2)","isSingle1&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.2)","isSingle1&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP_unitnorm", "angle [GeV]", "Unit normalized", True)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.2)","isSingle1&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.2)","isSingle1&&fspMatchChisq<3&&fspClE>0.85*2.306", remainder[0]+".pdf","Title:tarP_unitnorm", "angle [GeV]", "Unit normalized", True)
plotStuff(plotList,"fspPX/fspP>>{0}(20,-0.1,0.2)","isSingle1&&fspMatchChisq<3&&fspClE>0.85*2.306&&abs(fspPY/fspP)>0.03", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"fspPX/fspP>>{0}(20,-0.1,0.2)","isSingle1&&fspMatchChisq<3&&fspClE>0.85*2.306&&abs(fspPY/fspP)>0.03", remainder[0]+".pdf","Title:tarP_unitnorm", "angle [GeV]", "Unit normalized", True)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.2)","isSingle1&&fspMatchChisq<3&&fspClE>0.85*2.306&&abs(fspPY/fspP)>0.03", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"acos(fspPZ/fspP)>>{0}(20,0.03,0.1)","isSingle0&&fspMatchChisq<3&&fspClE>0.85*2.306&&abs(fspPY/fspP)>0.03", remainder[0]+".pdf","Title:tarP", "angle [GeV]", "Normalized rate [nb]", False)

c.Print(remainder[0]+".pdf]")
