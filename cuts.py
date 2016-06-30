#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
import cut_utils
from cut_utils import makePlots, allBut, makeCutString
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

cuts=["bscChisq<5",
        "max(eleTrkChisq,posTrkChisq)<30",
        "minIso>0.5",
        "abs(bscPX)<0.5",
        "abs(bscPY)<0.1",
        "eleP<0.7",
        "posP>0.3",
        "abs(eleFirstHitX-posFirstHitX+2)<10"]

c.Print(sys.argv[1]+".pdf[")
makePlots(c,goodEvents,badEvents,sys.argv[1],"bscChisq","bscChisq",100,0,50,makeCutString(allBut(cuts,0)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"trkChisq","max(eleTrkChisq,posTrkChisq)",100,0,50,makeCutString(allBut(cuts,1)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"minIso","minIso",200,0,5,makeCutString(allBut(cuts,2)),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","minPositiveIso",200,0,5,makeCutString(allBut(cuts,2)),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minNegIso","minNegativeIso",200,0,5,makeCutString(allBut(cuts,2)),False)

makePlots(c,goodEvents,badEvents,sys.argv[1],"bscPX","abs(bscPX/bscP)",100,0,0.05,makeCutString(allBut(cuts,3)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"bscPY","abs(bscPY/bscP)",100,0,0.025,makeCutString(allBut(cuts,4)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"eleP","eleP",200,0,1.5,makeCutString(allBut(cuts,5)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posP","posP",200,0,1.5,makeCutString(allBut(cuts,6)),False)
#cut_utils.makePlots(c,goodEvents,badEvents,sys.argv[1],"abs(eleP)","abs(eleP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)
#cut_utils.makePlots(c,goodEvents,badEvents,sys.argv[1],"abs(posP)","abs(posP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"abs_hitX","abs(eleFirstHitX-posFirstHitX+2)",200,-20,20,makeCutString(allBut(cuts,7)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"hitX","eleFirstHitX-posFirstHitX",200,-20,20,makeCutString(allBut(cuts,7)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"fda","(bscChisq/5.0)+(0.5/minIso)",100,0,10,makeCutString(cuts[:2]),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"cut","max(bscChisq/5.0,0.5/minIso)",100,0,5,makeCutString(cuts[:2]),True)


#makePlots("bscVX","abs(bscVX)",200,0,2,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
#makePlots("bscVY","abs(bscVY)",200,0,0.5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"elePhiKink","abs(elePhiKink2+elePhiKink3)",200,0,0.01,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"pdiff","abs(eleP-posP)/(eleP+posP)",200,0,1,makeCutString(cuts),True)
c.Print(sys.argv[1]+".pdf]")
