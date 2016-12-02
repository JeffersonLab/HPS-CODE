#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend

def plotStuff(plotList,plotstring, cutstring, plotfile, plotname, xlabel, ylabel, unitnorm):
    leg = TLegend(0.4,0.75,0.6,0.9)
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


if (len(remainder)!=5):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
dataFile = TFile(remainder[1])
mcFile = TFile(remainder[2])
mc2File = TFile(remainder[3])
mc3File = TFile(remainder[4])
dataEvents = dataFile.Get("ntuple")
mcEvents = mcFile.Get("ntuple")
mc2Events = mc2File.Get("ntuple")
mc3Events = mc3File.Get("ntuple")

plotList = []
plotList.append((mcEvents, "mc", 5.65e-3*4862, 2, "tritrig-beam-tri"))
plotList.append((dataEvents, "data", 119.3, 1, "golden runs"))
plotList.append((mc2Events, "mc2", 0.0176*81, 3, "tritrig_NOSUMCUT"))
plotList.append((mc3Events, "mc3", 0.00176*973, 4, "tritrig-wab-beam-tri_NOSUMCUT"))

dataEvents.Draw("tarP>>data(100,0.5,1.2)","","")
mcEvents.Draw("tarP>>mc(100,0.5,1.2)","","")

c.Print(remainder[0]+".pdf[")

plotStuff(plotList,"tarP>>{0}(100,0,1.2)","", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarP>>{0}(100,0.5,1.2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0.0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:eleP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(100,0.0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:posP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarM", "Mass [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:elePT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:posPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:eleTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:posTheta", "pT [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarP>>{0}(100,0.5,1.2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP_unitnorm", "Esum [GeV]", "Unit normalized", True)
plotStuff(plotList,"eleP>>{0}(100,0.0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:eleP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"posP>>{0}(100,0.0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:posP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarM_unitnorm", "Mass [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:elePT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:posPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:eleTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:posTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarP>>{0}(100,0.8,1.2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0.0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:eleP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(100,0.0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:posP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarM", "Mass [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:elePT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:posPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:eleTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:posTheta", "pT [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarP>>{0}(100,0.8,1.2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP_unitnorm", "Esum [GeV]", "Unit normalized", True)
plotStuff(plotList,"eleP>>{0}(100,0.0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:eleP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"posP>>{0}(100,0.0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:posP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarM_unitnorm", "Mass [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:elePT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:posPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:eleTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:posTheta_unitnorm", "pT [GeV]", "Unit normalized", True)

c.Print(remainder[0]+".pdf]")
