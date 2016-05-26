#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
print sys.argv[2]
print sys.argv[3]
goodFile = TFile(sys.argv[2])
badFile = TFile(sys.argv[3])
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
gStyle.SetOptStat(0)
#chain = TChain("ntuple")
#for i in sys.argv[2:]:
#	chain.Add(i)
#chain.Merge(sys.argv[1])


c = TCanvas("c","c",1200,900);
#c.cd()
#events = chain
#events = chain.CopyTree("uncM>0.03&&uncM<0.04")
goodEvents = goodFile.Get("ntuple")
badEvents = badFile.Get("ntuple")
#goodEvents = events.CopyTree("abs(uncVZ)*uncM<0.1")
#badEvents = events.CopyTree("uncVZ*uncM>0.5")
outFile = TFile(sys.argv[1]+".root","RECREATE")

def makePlots(name,var,nbins,xmin,xmax,cut,forward):
    c.Clear()
    c.Divide(2,2)
    c.cd(1)
    goodEvents.Draw("{}>>good({},{},{})".format(var,nbins,xmin,xmax),cut,"")
    #c.SaveAs(sys.argv[1]+"_{0}_good.png".format(name))
    c.cd(2)
    badEvents.Draw("{}>>bad({},{},{})".format(var,nbins,xmin,xmax),cut,"")
    #c.SaveAs(sys.argv[1]+"_{0}_bad.png".format(name))
    goodHist = gDirectory.Get("good")
    badHist = gDirectory.Get("bad")
    goodEfficiency=0
    badEfficiency=0
    cuts=array.array('d')
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
        cuts.append(goodHist.GetXaxis().GetBinLowEdge(start))
    else:
        start=nbins+1
        end=-1
        step=-1
        cuts.append(goodHist.GetXaxis().GetBinUpEdge(start))
    for i in xrange(start,end,step):
        if forward:
            cuts.append(goodHist.GetXaxis().GetBinUpEdge(i))
        else:
            cuts.append(goodHist.GetXaxis().GetBinLowEdge(i))
        goodEfficiency+=goodHist.GetBinContent(i)/goodTotal
        badEfficiency+=badHist.GetBinContent(i)/badTotal
        goodEfficiencies.append(goodEfficiency)
        badEfficiencies.append(badEfficiency)
        #print "{0}, {1}".format(badEfficiency,goodEfficiency)
    goodEffGraph = TGraph(len(cuts),cuts,goodEfficiencies)
    badEffGraph = TGraph(len(cuts),cuts,badEfficiencies)
    c.cd(3)
    goodEffGraph.Draw("AL")
    badEffGraph.SetLineColor(2)
    badEffGraph.Draw("L")

    rocGraph = TGraph(len(goodEfficiencies),badEfficiencies,goodEfficiencies)
    rocGraph.SetName(var)
    #rocGraph.SetTitle(var)
    #rocGraph.SetLineColor(1)
    c.cd(4)
    rocGraph.Draw("ALP")
    #c.cd()
    #c.Update()
    #c.SaveAs(sys.argv[1]+"_{0}_roc.png".format(name))
    c.Modified()
    c.SaveAs(sys.argv[1]+"_{0}.png".format(name))

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

cut0="bscChisq<5"
cut1="max(eleTrkChisq,posTrkChisq)<20"
cut2="minIso>0.5"
cut3="abs(bscPX)<0.5"
cut4="abs(bscPY)<0.1"

makePlots("bscChisq","bscChisq",100,0,50,"{0}&&{1}&&{2}&&{3}".format(cut1,cut2,cut3,cut4),True)

makePlots("trkChisq","max(eleTrkChisq,posTrkChisq)",100,0,50,"{0}&&{1}&&{2}&&{3}".format(cut0,cut2,cut3,cut4),True)

makePlots("minIso","minIso",200,0,5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut3,cut4),False)

#makePlots("bscPX","abs(bscPX/bscP)",100,0,0.05,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
makePlots("bscPX","abs(bscPX)",100,0,0.05,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("bscPY","abs(bscPY/bscP)",100,0,0.025,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
makePlots("bscPY","abs(bscPY)",100,0,0.025,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

makePlots("fda","(bscChisq/5.0)+(0.5/minIso)",100,0,10,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

makePlots("cut","max(bscChisq/5.0,0.5/minIso)",100,0,5,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

makePlots("minPosIso","minPositiveIso",200,0,5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut3,cut4),False)

makePlots("minNegIso","minNegativeIso>100?-9999:minNegativeIso",200,-5,0,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut3,cut4),True)

makePlots("hitX","eleFirstHitX-posFirstHitX",200,-20,20,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
makePlots("abs_hitX","abs(eleFirstHitX-posFirstHitX+2)",200,-20,20,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
#makePlots("bscVX","abs(bscVX)",200,0,2,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
#makePlots("bscVY","abs(bscVY)",200,0,0.5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
makePlots("elePhiKink","abs(elePhiKink2+elePhiKink3)",200,0,0.01,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

makePlots("pdiff","abs(eleP-posP)/(eleP+posP)",200,0,1,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
makePlots("trkP_ele","abs(eleP-1.05*0.5)",200,0,0.5,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
makePlots("trkP_pos","abs(posP-1.05*0.5)",200,0,0.5,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)
