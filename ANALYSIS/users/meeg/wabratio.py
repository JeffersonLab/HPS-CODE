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
    triHist = gDirectory.Get("tri")
    wabHist = gDirectory.Get("wab")
    sumHist = triHist.Clone("sum")
    sumHist.Add(wabHist)
    if unitnorm:
        sumHist.Scale(1.0/sumHist.Integral())
    sumHist.SetLineColor(6)
    leg.AddEntry(sumHist,"sum")
    sumHist.Draw("same")
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
        print sys.argv[0]+' <output basename> <data> <tritrig> <WAB>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
dataFile = TFile(remainder[1])
triFile = TFile(remainder[2])
wabFile = TFile(remainder[3])
dataEvents = dataFile.Get("ntuple")
triEvents = triFile.Get("ntuple")
wabEvents = wabFile.Get("ntuple")
dataEvents.SetWeight(1.0/119.3)
triEvents.SetWeight(1.0/(5.65e-3*4862))
wabEvents.SetWeight(1.0/(2.95e-5*993))

plotList = []
#plotList.append((wabEvents, "wab", 2.95e-5*993, 4, "WAB"))
#plotList.append((triEvents, "tri", 5.65e-3*4862, 2, "tritrig-beam-tri"))
#plotList.append((dataEvents, "data", 119.3, 1, "golden runs"))
plotList.append((dataEvents, "data", 0.206, 1, "golden runs"))
plotList.append((wabEvents, "wab", 2.1, 4, "WAB"))
plotList.append((triEvents, "tri", 1.0, 2, "tritrig-beam-tri"))

c.Print(remainder[0]+".pdf[")

plotStuff(plotList,"tarP>>{0}(100,0.5,1.2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(100,-3,3)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(100,-0.02,0.02)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(100,0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVX>>{0}(100,-2,2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVY>>{0}(100,-1,1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVZ>>{0}(100,-30,30)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)

plotStuff(plotList,"tarP>>{0}(100,0.5,1.2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(100,-3,3)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(100,-0.02,0.02)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(100,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVX>>{0}(100,-2,2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVY>>{0}(100,-1,1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVZ>>{0}(100,-30,30)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
c.Print(remainder[0]+".pdf]")
