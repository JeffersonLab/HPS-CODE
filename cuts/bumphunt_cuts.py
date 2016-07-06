#!/usr/bin/env python
import sys,os,array
import getopt
import ROOT
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
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


cuts=["max(abs(eleClT-eleTrkT-43),abs(posClT-posTrkT-43))<4",
        "max(eleMatchChisq,posMatchChisq)<5",
        "tarChisq<50",
        "max(eleTrkChisq,posTrkChisq)<50",
        "eleP<0.8",
        "tarP<1.2",
        "abs(tarPX)/tarP<0.025",
        "abs(tarPY)/tarP<0.015"]

c.Print(sys.argv[1]+".pdf[")

makePlots(c,goodEvents,badEvents,sys.argv[1],"matchDt","max(abs(eleClT-eleTrkT-43),abs(posClT-posTrkT-43))",100,0,20,makeCutString(allBut(cuts,0)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"eleMatchDt","abs(eleClT-eleTrkT-43)",100,0,20,makeCutString(allBut(cuts,0)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posMatchDt","abs(posClT-posTrkT-43)",100,0,20,makeCutString(allBut(cuts,0)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"matchChisq","max(eleMatchChisq,posMatchChisq)",100,0,20,makeCutString(allBut(cuts,1)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"eleMatchChisq","eleMatchChisq",100,0,20,makeCutString(allBut(cuts,1)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posMatchChisq","posMatchChisq",100,0,20,makeCutString(allBut(cuts,1)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"tarChisq","tarChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"bscChisq","bscChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"vzcChisq","vzcChisq",200,0,100,makeCutString(allBut(cuts,2)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"uncChisq","uncChisq",200,0,100,makeCutString(allBut(cuts,2)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"tar-uncChisq","tarChisq-uncChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"tar-bscChisq","tarChisq-bscChisq",200,0,100,makeCutString(allBut(cuts,2)),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"vzc-uncChisq","vzcChisq-uncChisq",200,0,100,makeCutString(allBut(cuts,2)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"trkChisq","max(eleTrkChisq,posTrkChisq)",100,0,200,makeCutString(allBut(cuts,3)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"eleTrkChisq","eleTrkChisq",100,0,200,makeCutString(allBut(cuts,3)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posTrkChisq","posTrkChisq",100,0,200,makeCutString(allBut(cuts,3)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"trkP_ele","eleP",200,0,1.5,makeCutString(allBut(cuts,4)),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"abstrkP_ele","abs(eleP-1.05*0.5)",200,0,0.5,makeCutString(allBut(cuts,4)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"tarP","tarP",100,0.5,1.5,makeCutString(allBut(cuts,5)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"uncP","uncP",100,0.5,1.5,makeCutString(allBut(cuts,5)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"tarPX/tarP","abs(tarPX)/tarP",100,0,0.04,makeCutString(allBut(cuts,6)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"bscPX/bscP","abs(bscPX)/bscP",100,0,0.04,makeCutString(allBut(cuts,6)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"tarPY/tarP","abs(tarPY)/tarP",100,0,0.025,makeCutString(allBut(cuts,7)),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"bscPY/bscP","abs(bscPY)/bscP",100,0,0.025,makeCutString(allBut(cuts,7)),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"tarP_XY_ellipse","sqrt((tarPX/0.04)^2+(tarPY/0.025)^2)/tarP",100,0,1,makeCutString(cuts[:6]),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"tarP_XY_rect","max(abs(tarPX/0.04),abs(tarPY/0.025))/tarP",100,0,1,makeCutString(cuts[:6]),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"tarP_XY_diamond","(abs(tarPX/0.04)+abs(tarPY/0.025))/tarP",100,0,1,makeCutString(cuts[:6]),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"abs_uncVZ","abs(uncVZ+5)",100,0,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"uncVZ","uncVZ",100,-20,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"vzcVX","abs(vzcVX)",100,0,2,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"vzcVY","abs(vzcVY)",100,0,2,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"eleTrkD0","abs(eleTrkD0)",100,0,5,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"eleTrkZ0","abs(eleTrkZ0)",100,0,5,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posTrkD0","abs(posTrkD0)",100,0,5,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posTrkZ0","abs(posTrkZ0)",100,0,5,makeCutString(cuts),True)


#makePlots("bscPX","abs(bscPX/bscP)",100,0,0.05,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("bscPY","abs(bscPY/bscP)",100,0,0.025,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("fda","(bscChisq/5.0)+(0.5/minIso)",100,0,10,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

#makePlots("cut","max(bscChisq/5.0,0.5/minIso)",100,0,5,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"minIso","minIso",200,0,5,makeCutString(cuts),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","minPositiveIso",200,0,5,makeCutString(cuts),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minNegIso","minNegativeIso",200,0,5,makeCutString(cuts),False)

makePlots(c,goodEvents,badEvents,sys.argv[1],"hitX","eleFirstHitX-posFirstHitX",200,-20,20,makeCutString(cuts),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"abs_hitX","abs(eleFirstHitX-posFirstHitX+2)",200,-20,20,makeCutString(cuts),True)
#makePlots("bscVX","abs(bscVX)",200,0,2,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
#makePlots("bscVY","abs(bscVY)",200,0,0.5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"elePhiKink","abs(elePhiKink2+elePhiKink3)",200,0,0.01,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"pdiff","abs(eleP-posP)/(eleP+posP)",200,0,1,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"trkP_pos","posP",200,0,1.5,makeCutString(cuts),False)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"abstrkP_pos","abs(posP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)
c.Print(sys.argv[1]+".pdf]")
