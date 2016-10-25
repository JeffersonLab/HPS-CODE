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

    w.pdf("sumModel").fitTo(w.data("data"),RooFit.SumW2Error(True),RooFit.Extended(True), RooFit.Verbose(False),RooFit.PrintLevel(-1))
    #w.pdf("sumModel").fitTo(w.data("data"),RooFit.Extended(True))
    #w.pdf("sumModel").fitTo(w.data("data"))
    frame=w.var("x").frame()
    w.data("data").plotOn(frame)
    #w.pdf("triPdf").plotOn(frame)
    #w.pdf("wabPdf").plotOn(frame)
    w.pdf("sumModel").plotOn(frame)
    w.pdf("sumModel").paramOn(frame)
    frame.SetTitle(gDirectory.Get("data").GetTitle())
    frame.Draw()
    c.Print(plotfile)
    c.Clear()

    dataHist = gDirectory.Get("data")
    triHist = gDirectory.Get("tri")
    wabHist = gDirectory.Get("wab")
    if legendright:
        leg = TLegend(0.7,0.75,0.9,0.9)
    else:
        leg = TLegend(0.1,0.75,0.3,0.9)
    hs = THStack("hs",plotname);
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
        #hist.GetXaxis().SetTitle(xlabel)
        hist.GetYaxis().SetTitle(ylabel)

        #if isFirst:
            #hist.GetXaxis().SetTitle(xlabel)
            #hist.GetYaxis().SetTitle(ylabel)
            #hist.Draw()
        #else:
            #hist.Draw("same")
        isFirst = False
    sumHist = triHist.Clone("sum")
    sumHist.Add(wabHist)
    if unitnorm:
        sumHist.Scale(1.0/sumHist.Integral())
    sumHist.SetLineColor(6)
    leg.AddEntry(sumHist,"MC sum")
    hs.Add(sumHist)
    hs.Draw("nostack")
    hs.GetXaxis().SetTitle(xlabel)
    hs.GetYaxis().SetTitle(ylabel)
    leg.Draw()
    c.Print(plotfile)

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

gROOT.SetBatch(True)
c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
print "./wabratio_thesisplots.py temp golden_tri.root old/tritrig-wab-beam-tri_NOSUMCUT_tri.root wabv2-4062dz_tri.root"
dataFile = TFile(remainder[1])
triFile = TFile(remainder[2])
wabFile = TFile(remainder[3])
dataEvents = dataFile.Get("ntuple")
triEvents = triFile.Get("ntuple")
wabEvents = wabFile.Get("ntuple")
dataEvents.SetWeight(1.0/119.3)
triEvents.SetWeight(1.0/(0.00176*973))
#triEvents.SetWeight(1.0/(0.0682*375))
wabEvents.SetWeight(1.0/((9.5e4/0.7e9)*995))
#wabEvents.SetWeight(1.0/((1.9e5/0.7e9)*993))

#wabEvents.SetWeight(1.0/(2*(1.45e5/0.6e9)*993)) #Rafo's wabv1 normalization

plotList = []
#plotList.append((triEvents, "tri", 5.65e-3*4862, 2, "tritrig-beam-tri"))
#plotList.append((dataEvents, "data", 119.3, 1, "golden runs"))
#plotList.append((wabEvents, "wab", 1.248e-5*100, 4, "WAB"))

#plotList.append((dataEvents, "data", 1/8.13e-3, 1, "golden runs"))
#plotList.append((triEvents, "tri", 1/8.13e-3, 2, "tritrig-beam-tri"))
#plotList.append((wabEvents, "wab", 1/8.13e-3, 4, "WAB"))

plotList.append((dataEvents, "data", 1.0, 1, "data"))

#plotList.append((triEvents, "tri", 1.0, 2, "tritrig-beam-tri"))
#plotList.append((triEvents, "tri", 1/0.65, 2, "trident MC"))
#plotList.append((wabEvents, "wab", 1/0.67, 4, "WAB MC"))
plotList.append((triEvents, "tri", 1.0, 2, "trident MC"))
plotList.append((wabEvents, "wab", 1.0, 4, "WAB MC"))

#plotList.append((triEvents, "tri", 1/0.3, 2, "tritrig-beam-tri"))
#plotList.append((wabEvents, "wab", 1/0.9, 4, "WAB"))

#plotList.append((triEvents, "tri", 1/0.314, 2, "tritrig-beam-tri"))
#plotList.append((wabEvents, "wab", 1/0.644, 4, "WAB"))
#plotList.append((wabEvents, "wab", 1/0.5, 4, "WAB"))

c.Print(remainder[0]+".pdf[")

legendright = True
plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","", remainder[0]+".pdf","All pairs", "momentum sum [GeV]", "Normalized rate [nb]", False)
plotList[0]=(dataEvents, "data", 0.65, 1, "data/0.65")
legendright = False
plotStuff(plotList,"posHasL1>>{0}(2,-0.5,1.5)","tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam", "positron L1 hit", "Normalized rate [nb]", False)
plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam", "momentum sum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","tarP>0.8*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","tarP>0.8*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.030", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam", "positron X DOCA [mm]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam", "p(e+e-)_y towards positron side [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(50,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam", "Electron momentum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(50,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam", "Positron momentum [GeV]", "Normalized rate [nb]", False)

plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with L1 positron hit", "momentum sum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","posHasL1&&tarP>0.8*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","posHasL1&&tarP>0.8*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.030", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with L1 positron hit", "positron X DOCA [mm]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with L1 positron hit", "p(e+e-)_y towards positron side [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(50,0,1.0)","posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with L1 positron hit", "Electron momentum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(50,0,1.0)","posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with L1 positron hit", "Positron momentum [GeV]", "Normalized rate [nb]", False)

plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","!posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with no L1 positron hit", "momentum sum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","!posHasL1&&tarP>0.8*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","!posHasL1&&tarP>0.8*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.030", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","!posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with no L1 positron hit", "positron X DOCA [mm]", "Normalized rate [nb]", False)
plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","!posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with no L1 positron hit", "p(e+e-)_y towards positron side [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"eleP>>{0}(50,0,1.0)","!posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with no L1 positron hit", "Electron momentum [GeV]", "Normalized rate [nb]", False)
plotStuff(plotList,"posP>>{0}(50,0,1.0)","!posHasL1&&tarP>0.8*1.056", remainder[0]+".pdf","p(e+e-)>0.8E_beam with no L1 positron hit", "Positron momentum [GeV]", "Normalized rate [nb]", False)

legendright = True
plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","", remainder[0]+".pdf","All pairs", "momentum sum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(70,0.4,1.1)","min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(70,0.4,1.1)","min(abs(elePY/eleP),abs(posPY/posP))>0.030", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"eleP>>{0}(50,0,1.0)","", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posP>>{0}(50,0,1.0)","", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)

plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","posHasL1", remainder[0]+".pdf","Pairs with L1 positron hit", "momentum sum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(70,0.4,1.1)","posHasL1&&min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(70,0.4,1.1)","posHasL1&&min(abs(elePY/eleP),abs(posPY/posP))>0.030", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"eleP>>{0}(50,0,1.0)","posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posP>>{0}(50,0,1.0)","posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)

legendright = False
plotStuff(plotList,"tarP>>{0}(80,0.4,1.2)","!posHasL1", remainder[0]+".pdf","Pairs with no L1 positron hit", "momentum sum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(70,0.4,1.1)","!posHasL1&&min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarP>>{0}(70,0.4,1.1)","!posHasL1&&min(abs(elePY/eleP),abs(posPY/posP))>0.030", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","!posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","!posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"eleP>>{0}(50,0,1.0)","!posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posP>>{0}(50,0,1.0)","!posHasL1", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)

#plotStuff(plotList,"tarP>>{0}(70,0.5,1.2)","tarP>0.5*1.056&&min(abs(elePY/eleP),abs(posPY/posP))>0.025", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posTrkD0>>{0}(50,-3,3)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarPY*sign(posPY)>>{0}(50,-0.02,0.02)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"eleP>>{0}(50,0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posP>>{0}(50,0,1.0)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVX>>{0}(100,-2,2)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVY>>{0}(100,-1,1)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVZ>>{0}(100,-30,30)","tarP>0.5*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)

#plotStuff(plotList,"tarP>>{0}(20,0.5,1.2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posTrkD0>>{0}(20,-3,3)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"tarPY*sign(posPY)>>{0}(20,-0.02,0.02)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"eleP>>{0}(20,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"posP>>{0}(20,0,1.0)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVX>>{0}(100,-2,2)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVY>>{0}(100,-1,1)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
#plotStuff(plotList,"uncVZ>>{0}(100,-30,30)","tarP>0.8*1.056", remainder[0]+".pdf","Title:tarP", "Esum [GeV]", "Normalized rate [nb]", False)
c.Print(remainder[0]+".pdf]")
