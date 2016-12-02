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
gROOT.SetBatch(True)
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

cuts=["bscChisq<10",
        "max(eleTrkChisq,posTrkChisq)<30",
        #"minPositiveIso-0.02*bscChisq>-10",
        "eleP<0.8",
        #"abs(eleFirstHitX-posFirstHitX+2)<700",
        "abs(eleP-posP)/(eleP+posP)<0.4",
        "posTrkD0-5*posPX/posP<1.5",
        "min(eleMinPositiveIso+0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0-5*posPY/posP)*sign(posPY))>0",
        "bscChisq-uncChisq<5"]

c.Print(sys.argv[1]+".pdf[")
makePlots(c,goodEvents,badEvents,sys.argv[1],"bscChisq","bscChisq",100,0,50,makeCutString(cuts,0),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"bsc-uncChisq","bscChisq-uncChisq",200,0,50,makeCutString(cuts,6),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"uncChisq","uncChisq",100,0,50,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"trkChisq","max(eleTrkChisq,posTrkChisq)",100,0,50,makeCutString(cuts,1),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","minPositiveIso",200,0,5,makeCutString(cuts),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso_sloped","minPositiveIso-0.02*bscChisq",200,0,5,makeCutString(cuts),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"slope","(minPositiveIso-0.5)/bscChisq",200,-0.1,0.1,makeCutString(cuts),False)

#makePlots(c,goodEvents,badEvents,sys.argv[1],"minEleIso","eleMinPositiveIso-max(0,-0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY))",200,-5,5,makeCutString(cuts,6),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minEleIso","eleMinPositiveIso+0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY)",200,-2,2,makeCutString(cuts,5),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minEleIso","2*eleMinPositiveIso+(eleTrkZ0-5*elePY/eleP)*sign(elePY)",200,-2,2,makeCutString(cuts,5),False)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","posMinPositiveIso-max(0,-0.5*(posTrkZ0-5*posPY/posP)*sign(posPY))",200,-5,5,makeCutString(cuts,6),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","posMinPositiveIso+0.5*(posTrkZ0-5*posPY/posP)*sign(posPY)",200,-2,2,makeCutString(cuts,5),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","2*posMinPositiveIso+(posTrkZ0-5*posPY/posP)*sign(posPY)",200,-2,2,makeCutString(cuts,5),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","min(eleMinPositiveIso-max(0,-0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY)),posMinPositiveIso-max(0,-0.5*(posTrkZ0-5*posPY/posP)*sign(posPY)))",200,-2,2,makeCutString(cuts,5),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minPosIso","min(eleMinPositiveIso+0.5*(eleTrkZ0-5*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0-5*posPY/posP)*sign(posPY))",200,-2,2,makeCutString(cuts,5),False)

makePlots(c,goodEvents,badEvents,sys.argv[1],"minIso","minIso",200,0,5,makeCutString(cuts),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"minNegIso","minNegativeIso",200,0,5,makeCutString(cuts),False)

makePlots(c,goodEvents,badEvents,sys.argv[1],"bscPX","abs(bscPX/bscP)",100,0,0.05,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"bscPY","abs(bscPY/bscP)",100,0,0.025,makeCutString(cuts),True)


makePlots(c,goodEvents,badEvents,sys.argv[1],"eleP","eleP",200,0,1.5,makeCutString(cuts,3),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posP","posP",200,0,1.5,makeCutString(cuts,3),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"pdiff","abs(eleP-posP)/(eleP+posP)",200,0,1,makeCutString(cuts,3),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"pdiff","(eleP-posP)/(eleP+posP)",200,-1,1,makeCutString(cuts,3),True)
#cut_utils.makePlots(c,goodEvents,badEvents,sys.argv[1],"abs(eleP)","abs(eleP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)
#cut_utils.makePlots(c,goodEvents,badEvents,sys.argv[1],"abs(posP)","abs(posP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"abs_hitXDiff","abs(eleFirstHitX-posFirstHitX+2)",200,-20,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"hitXDiff","eleFirstHitX-posFirstHitX",200,-20,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"abs_hitXDiff","abs(eleFirstHitX-posFirstHitX+2)/uncM",200,-400,400,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"hitXDiff","(eleFirstHitX-posFirstHitX)/uncM",200,-400,400,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"deltaPX","abs(elePX/eleP-posPX/posP)",100,0,0.1,makeCutString(cuts),True)

#makePlots(c,goodEvents,badEvents,sys.argv[1],"fda","(bscChisq/5.0)+(0.5/minIso)",100,0,10,makeCutString(cuts[:2]),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"cut","max(bscChisq/5.0,0.5/minIso)",100,0,5,makeCutString(cuts[:2]),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"matchDt","max(abs(eleClT-eleTrkT-43),abs(posClT-posTrkT-43))",100,0,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"matchChisq","max(eleMatchChisq,posMatchChisq)",100,0,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"eleMatchChisq","eleMatchChisq",100,0,20,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posMatchChisq","posMatchChisq",100,0,20,makeCutString(cuts),True)

#makePlots("bscVX","abs(bscVX)",200,0,2,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
#makePlots("bscVY","abs(bscVY)",200,0,0.5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"elePhiKink","abs(elePhiKink2+elePhiKink3)",200,0,0.01,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"lambdaKink","abs((eleLambdaKink1+eleLambdaKink2)-(posLambdaKink1+posLambdaKink2))",200,0,0.01,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"pt","bscPY*sign(posPY)",100,-0.02,0.02,makeCutString(cuts),False)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posTrkD0","posTrkD0",100,-5,5,makeCutString(cuts,4),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"posTrkD0","posTrkD0-5*posPX/posP",100,-5,5,makeCutString(cuts,4),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"eleTrkD0","eleTrkD0",100,-5,5,makeCutString(cuts),True)

makePlots(c,goodEvents,badEvents,sys.argv[1],"nTrk","nTrk",10,0.5,10.5,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"nEle","nTrk-nPos",10,0.5,10.5,makeCutString(cuts),True)
makePlots(c,goodEvents,badEvents,sys.argv[1],"nPos","nPos",10,0.5,10.5,makeCutString(cuts),True)

#makePlots(c,goodEvents,badEvents,sys.argv[1],"hitXSum","eleFirstHitX+posFirstHitX",200,-20,20,makeCutString(cuts,7),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"hitYSum","eleFirstHitY+posFirstHitY",200,-20,20,makeCutString(cuts,7),True)
#makePlots(c,goodEvents,badEvents,sys.argv[1],"hitYDiff","abs(eleFirstHitY-posFirstHitY)",200,-20,20,makeCutString(cuts,7),True)
c.Clear()
goodEvents.Draw("bscChisq:min(minPositiveIso,4.9)>>good2d(100,0,5,100,0,50)",makeCutString(cuts,0),"colz")
c.Print(sys.argv[1]+".pdf")
badEvents.Draw("bscChisq:min(minPositiveIso,4.9)>>bad2d(100,0,5,100,0,50)",makeCutString(cuts,0),"colz")
c.Print(sys.argv[1]+".pdf")
goodEvents.Draw("eleP+posP:eleP-posP>>good2d(100,-1,1,100,0.7,1.3)",makeCutString(cuts,3,4),"colz")
gDirectory.Get("good2d").SetTitle("Good events (all but WAB cuts)")
gDirectory.Get("good2d").GetXaxis().SetTitle("p(e-)-p(e+) [GeV]")
gDirectory.Get("good2d").GetYaxis().SetTitle("p(e-)+p(e+) [GeV]")
c.Print(sys.argv[1]+".pdf")
badEvents.Draw("eleP+posP:eleP-posP>>bad2d(100,-1,1,100,0.7,1.3)",makeCutString(cuts,3,4),"colz")
gDirectory.Get("bad2d").SetTitle("Bad events (all but WAB cuts)")
gDirectory.Get("bad2d").GetXaxis().SetTitle("p(e-)-p(e+) [GeV]")
gDirectory.Get("bad2d").GetYaxis().SetTitle("p(e-)+p(e+) [GeV]")
c.Print(sys.argv[1]+".pdf")
c.Print(sys.argv[1]+".pdf]")
