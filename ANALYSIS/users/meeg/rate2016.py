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
    #leg.Draw()
    data1Hist = gDirectory.Get("data1")
    data2Hist = gDirectory.Get("data2")
    data3Hist = gDirectory.Get("data3")
    data1Hist.Divide(data3Hist)
    data2Hist.Divide(data3Hist)
    data1Hist.Draw()
    data2Hist.Draw("same")

    c.Print(plotfile,plotname)

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\n"
        sys.exit(0)


if (len(remainder)!=7):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <7807> <7808> <7809> <tritrig-beam-tri ROOT file> <tritrig lowerESum ROOT file> <tritrig ROOT file>".format(sys.argv[0])
print "{0} rate2016 7807_tri.root 7808_tri.root 7809_tri.root tritrig2016-beam-tri_tri.root tritrig2016_lowerESum_tri.root tritrig2016_tri.root"
data1File = TFile(sys.argv[2])
data2File = TFile(sys.argv[3])
data3File = TFile(sys.argv[4])
mc1File = TFile(sys.argv[5])
mc2File = TFile(sys.argv[6])
mc3File = TFile(sys.argv[7])
data1Events = data1File.Get("ntuple")
data2Events = data2File.Get("ntuple")
data3Events = data3File.Get("ntuple")
mc1Events = mc1File.Get("ntuple")
mc2Events = mc2File.Get("ntuple")
mc3Events = mc3File.Get("ntuple")

plotList = []
plotList.append((mc2Events, "mc2", 0.302*76, 5, "tritrig (lower ESum)"))
plotList.append((data1Events, "data1", 0.835*89719*0.00002562/0.1602, 1, "run 7807 (200 nA)"))
plotList.append((data2Events, "data2", 0.61*26617*0.00002562/0.1602, 2, "run 7808 (300 nA)"))
plotList.append((data3Events, "data3", 0.98*28230*0.00002562/0.1602, 4, "run 7809 (50 nA)"))
plotList.append((mc1Events, "mc1", 0.0788*976, 3, "tritrig-beam-tri"))
plotList.append((mc3Events, "mc3", 2*0.851*100, 6, "tritrig"))

c.Print(remainder[0]+".pdf[")

#c.SetLogy(1)
plotStuff(plotList,"tarP>>{0}(100,1.0,2.5)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0.0,2.0)","tarP>0.5*2.306", remainder[0]+".pdf","Title:eleP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(100,0.0,2.0)","tarP>0.5*2.306", remainder[0]+".pdf","Title:posP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.2)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarM", "Mass [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:elePT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:posPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:eleTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:posTheta", "pT [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarP>>{0}(100,1.0,2.5)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarP_unitnorm", "Esum [GeV]", "Unit normalized", True)
plotStuff(plotList,"eleP>>{0}(100,0.0,2.0)","tarP>0.5*2.306", remainder[0]+".pdf","Title:eleP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"posP>>{0}(100,0.0,2.0)","tarP>0.5*2.306", remainder[0]+".pdf","Title:posP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.2)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarM_unitnorm", "Mass [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:elePT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:posPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:tarTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:eleTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.5*2.306", remainder[0]+".pdf","Title:posTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarP>>{0}(100,1.5,2.5)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(100,0.0,2.0)","tarP>0.8*2.306", remainder[0]+".pdf","Title:eleP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(100,0.0,2.0)","tarP>0.8*2.306", remainder[0]+".pdf","Title:posP", "p [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.2)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarM", "Mass [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:elePT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:posPT", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:eleTheta", "pT [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:posTheta", "pT [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarP>>{0}(100,1.5,2.5)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarP_unitnorm", "Esum [GeV]", "Unit normalized", True)
plotStuff(plotList,"eleP>>{0}(100,0.0,2.0)","tarP>0.8*2.306", remainder[0]+".pdf","Title:eleP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"posP>>{0}(100,0.0,2.0)","tarP>0.8*2.306", remainder[0]+".pdf","Title:posP_unitnorm", "p [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.2)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarM_unitnorm", "Mass [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(tarPX**2+tarPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(elePX**2+elePY**2)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:elePT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"sqrt(posPX**2+posPY**2)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:posPT_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(tarPZ/tarP)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:tarTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(elePZ/eleP)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:eleTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
#plotStuff(plotList,"acos(posPZ/posP)>>{0}(100,0.0,0.1)","tarP>0.8*2.306", remainder[0]+".pdf","Title:posTheta_unitnorm", "pT [GeV]", "Unit normalized", True)
plotStuff(plotList,"tarP>>{0}(100,1.0,2.5)","tarP>0.5*2.306&&abs(elePY/eleP)>0.03&&abs(posPY/posP)>0.03", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarM>>{0}(100,0.0,0.2)","tarP>0.5*2.306&&abs(elePY/eleP)>0.03&&abs(posPY/posP)>0.03", remainder[0]+".pdf","Title:tarM", "Mass [GeV]", "Normalized rate [nb]", False)

c.Print(remainder[0]+".pdf]")
