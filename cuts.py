#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
print sys.argv[1]
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print sys.argv[2:]
gStyle.SetOptStat(0)
chain = TChain("ntuple")
for i in sys.argv[2:]:
	chain.Add(i)
#chain.Merge(sys.argv[1])


outFile = TFile(sys.argv[1]+".root","RECREATE")
c = TCanvas("c","c",800,600);
c.cd()
events = chain.CopyTree("")
#events = chain.CopyTree("uncM>0.03&&uncM<0.04")
goodEvents = events.CopyTree("abs(uncVZ)<10")
badEvents = events.CopyTree("uncVZ>15")


cut0="bscChisq<5"
cut1="max(eleTrkChisq,posTrkChisq)<25"
cut2="minIso>0.5"
cut3="abs(uncPX/uncP)<0.05"
cut4="abs(uncPY/uncP)<0.05"

def makePlots(var,nbins,xmin,xmax,cut,forward):
    #c.Clear()
    goodEvents.Draw("{}>>good({},{},{})".format(var,nbins,xmin,xmax),cut,"goff")
    badEvents.Draw("{}>>bad({},{},{})".format(var,nbins,xmin,xmax),cut,"goff")
    goodHist = gDirectory.Get("good")
    badHist = gDirectory.Get("bad")
    goodEfficiency=0
    badEfficiency=0
    goodEfficiencies=array.array('d')
    badEfficiencies=array.array('d')
    goodEfficiencies.append(0)
    badEfficiencies.append(0)
    nbins=goodHist.GetXaxis().GetNbins()
    goodTotal=goodHist.Integral()+goodHist.GetBinContent(0)+goodHist.GetBinContent(nbins+1)
    badTotal=badHist.Integral()+badHist.GetBinContent(0)+badHist.GetBinContent(nbins+1)
    if forward:
        start=0
        end=nbins+2
        step=1
    else:
        start=nbins+1
        end=-1
        step=-1
    for i in xrange(start,end,step):
        goodEfficiency+=goodHist.GetBinContent(i)/goodTotal
        badEfficiency+=badHist.GetBinContent(i)/badTotal
        goodEfficiencies.append(goodEfficiency)
        badEfficiencies.append(badEfficiency)
        #print "{0}, {1}".format(badEfficiency,goodEfficiency)
    rocGraph = TGraph(len(goodEfficiencies),badEfficiencies,goodEfficiencies)
    rocGraph.SetName(var)
    rocGraph.SetTitle(var)
    rocGraph.SetLineColor(1)
    #rocGraph.Write()
    #c.cd()
    #c.Update()
    rocGraph.Draw("AL*")
    #c.cd()
    c.Update()
    #c.Modified()

    #goodHist.AddBinContent(1,goodHist.GetBinContent(0))
    #goodHist.SetBinContent(0,0)
    #badHist.AddBinContent(1,badHist.GetBinContent(0))
    #badHist.SetBinContent(0,0)
    #goodHist.AddBinContent(nbins,goodHist.GetBinContent(nbins+1))
    #goodHist.SetBinContent(nbins+1,0)
    #badHist.AddBinContent(nbins,badHist.GetBinContent(nbins+1))
    #badHist.SetBinContent(nbins+1,0)
    #goodHist.Scale(1.0/goodHist.Integral())
    #goodHist.GetYaxis().SetRangeUser(0,1)
    #goodHistIntegral = goodHist.GetCumulative(forward)
    #goodHistIntegral.Draw("")
    #badHist.SetLineColor(2)
    #badHist.Scale(1.0/badHist.Integral())
    #badHistIntegral = badHist.GetCumulative(forward)
    #badHistIntegral.Draw("same")

makePlots("bscChisq",100,0,50,"{0}&&{1}&&{2}&&{3}".format(cut1,cut2,cut3,cut4),True)
c.SaveAs(sys.argv[1]+"_bscChisq.png")

makePlots("max(eleTrkChisq,posTrkChisq)",100,0,50,"{0}&&{1}&&{2}&&{3}".format(cut0,cut2,cut3,cut4),True)
c.SaveAs(sys.argv[1]+"_trkChisq.png")

makePlots("minIso",200,0,1,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut3,cut4),False)
c.SaveAs(sys.argv[1]+"_minIso.png")

makePlots("abs(uncPX/uncP)",100,0,0.05,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
c.SaveAs(sys.argv[1]+"_uncPX.png")

makePlots("abs(uncPY/uncP)",100,0,0.025,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
c.SaveAs(sys.argv[1]+"_uncPY.png")

makePlots("(bscChisq/5.0)+(0.5/minIso)",100,0,10,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)
c.SaveAs(sys.argv[1]+"_fda.png")

makePlots("max(bscChisq/5.0,0.5/minIso)",100,0,5,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)
c.SaveAs(sys.argv[1]+"_cut.png")


makePlots("minPositiveIso",200,0,5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut3,cut4),False)
c.SaveAs(sys.argv[1]+"_minPosIso.png")

makePlots("minNegativeIso>100?-9999:minNegativeIso",200,-5,0,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut3,cut4),True)
c.SaveAs(sys.argv[1]+"_minNegIso.png")
