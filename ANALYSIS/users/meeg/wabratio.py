#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend, RooFit, RooWorkspace, RooDataHist, RooArgList, THStack

def plotStuff(plotList,plotstring, cutstring, plotfile, plotname, xlabel, ylabel, unitnorm):
    isFirst = True
    w = RooWorkspace("w")
    w.factory("x[-100,100]")
    for dataset in plotList:
        dataset[0].Draw(plotstring.format(dataset[1]),cutstring,"goff")
        hist = gDirectory.Get(dataset[1])
        data=RooDataHist(dataset[1],dataset[1],RooArgList(w.var("x")),hist)
        getattr(w,'import')(data)
    w.factory("HistPdf::triPdf(x,tri)")
    w.factory("HistPdf::wabPdf(x,wab)")
    w.factory("prod::triscale(a[0.3,0,10],{0})".format(w.data("tri").sum(False)))
    w.factory("prod::wabscale(b[0.1,0,10],{0})".format(w.data("wab").sum(False)))
    w.factory("SUM::sumModel(triscale*triPdf,wabscale*wabPdf)")

    w.pdf("sumModel").fitTo(w.data("data"),RooFit.SumW2Error(True),RooFit.Extended(True))
    #w.pdf("sumModel").fitTo(w.data("data"),RooFit.Extended(True))
    #w.pdf("sumModel").fitTo(w.data("data"))
    frame=w.var("x").frame()
    w.data("data").plotOn(frame)
    #w.pdf("triPdf").plotOn(frame)
    #w.pdf("wabPdf").plotOn(frame)
    w.pdf("sumModel").plotOn(frame)
    w.pdf("sumModel").paramOn(frame)
    frame.Draw()
    c.Print(plotfile,plotname)
    c.Clear()

    leg = TLegend(0.0,0.75,0.2,0.9)
    hs = THStack("hs","");
    for dataset in plotList:
        hist = gDirectory.Get(dataset[1])
        #hist.Sumw2()
        if unitnorm:
            hist.Scale(1.0/hist.Integral())
        else:
            hist.Scale(1.0/dataset[2])
            print "{0} {1} {2}".format(plotname,dataset[4],hist.Integral())
        hist.SetLineColor(dataset[3])
        leg.AddEntry(hist,dataset[4])
        hs.Add(hist)
        hist.GetXaxis().SetTitle(xlabel)
        hist.GetYaxis().SetTitle(ylabel)

        #if isFirst:
            #hist.GetXaxis().SetTitle(xlabel)
            #hist.GetYaxis().SetTitle(ylabel)
            #hist.Draw()
        #else:
            #hist.Draw("same")
        isFirst = False




    dataHist = gDirectory.Get("data")
    triHist = gDirectory.Get("tri")
    wabHist = gDirectory.Get("wab")
    sumHist = triHist.Clone("sum")
    sumHist.Add(wabHist)
    if unitnorm:
        sumHist.Scale(1.0/sumHist.Integral())
    sumHist.SetLineColor(6)
    leg.AddEntry(sumHist,"sum")
    hs.Add(sumHist)
    hs.Draw("nostack")
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
wabEvents.SetWeight(1.0/(1.248e-5*100))
#wabEvents.SetWeight(1.0/(2.95e-5*993))

plotList = []
#plotList.append((triEvents, "tri", 5.65e-3*4862, 2, "tritrig-beam-tri"))
#plotList.append((dataEvents, "data", 119.3, 1, "golden runs"))
plotList.append((dataEvents, "data", 1.0, 1, "golden runs"))
#plotList.append((wabEvents, "wab", 1.248e-5*100, 4, "WAB"))
plotList.append((triEvents, "tri", 1/0.246, 2, "tritrig-beam-tri"))
plotList.append((wabEvents, "wab", 1/0.087, 4, "WAB"))

c.Print(remainder[0]+".pdf[")

plotStuff(plotList,"tarP>>{0}(20,0.5,1.2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(20,-3,3)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(20,-0.02,0.02)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(20,0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(20,0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVX>>{0}(100,-2,2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVY>>{0}(100,-1,1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVZ>>{0}(100,-30,30)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)

plotStuff(plotList,"tarP>>{0}(20,0.5,1.2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(20,-3,3)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(20,-0.02,0.02)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(20,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(20,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVX>>{0}(100,-2,2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVY>>{0}(100,-1,1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVZ>>{0}(100,-30,30)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
c.Print(remainder[0]+".pdf]")
