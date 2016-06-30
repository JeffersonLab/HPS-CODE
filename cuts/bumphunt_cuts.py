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
    gDirectory.Get("good").SetTitle(var+", good events")
    #c.SaveAs(sys.argv[1]+"_{0}_good.png".format(name))
    c.cd(2)
    badEvents.Draw("{}>>bad({},{},{})".format(var,nbins,xmin,xmax),cut,"")
    gDirectory.Get("bad").SetTitle(var+", bad events")
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
    goodEffGraph.SetTitle("Efficiency vs. cut value")
    goodEffGraph.Draw("AL")
    goodEffGraph.GetXaxis().SetRangeUser(xmin,xmax)
    goodEffGraph.GetYaxis().SetRangeUser(0,1)
    badEffGraph.SetLineColor(2)
    badEffGraph.Draw("L")

    rocGraph = TGraph(len(goodEfficiencies),badEfficiencies,goodEfficiencies)
    rocGraph.SetName(var)
    rocGraph.SetTitle("ROC curve")
    rocGraph.GetXaxis().SetRangeUser(0,1)
    rocGraph.GetYaxis().SetRangeUser(0,1)
    #rocGraph.SetLineColor(1)
    c.cd(4)
    rocGraph.Draw("ALP")
    #c.cd()
    #c.Update()
    #c.SaveAs(sys.argv[1]+"_{0}_roc.png".format(name))
    c.Modified()
    c.Print(sys.argv[1]+".pdf".format(name),"Title:"+name)

def allBut(cuts,i):
    return cuts[:i]+cuts[i+1:]
def makeCutString(cuts):
    return reduce(lambda a,b:a+"&&"+b,[str(i) for i in cuts])

cuts=["max(abs(eleClT-eleTrkT-43),abs(posClT-posTrkT-43))<4",
        "max(eleMatchChisq,posMatchChisq)<5",
        "tarChisq<50",
        "max(eleTrkChisq,posTrkChisq)<50",
        "eleP<0.8",
        "uncP<1.2",
        "abs(tarPX)/tarP<0.025",
        "abs(tarPY)/tarP<0.015"]

c.Print(sys.argv[1]+".pdf[")

makePlots("matchDt","max(abs(eleClT-eleTrkT-43),abs(posClT-posTrkT-43))",100,0,20,makeCutString(allBut(cuts,0)),True)
makePlots("eleMatchDt","abs(eleClT-eleTrkT-43)",100,0,20,makeCutString(allBut(cuts,0)),True)
makePlots("posMatchDt","abs(posClT-posTrkT-43)",100,0,20,makeCutString(allBut(cuts,0)),True)

makePlots("matchChisq","max(eleMatchChisq,posMatchChisq)",100,0,10,makeCutString(allBut(cuts,1)),True)

makePlots("tarChisq","tarChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots("bscChisq","bscChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots("uncChisq","uncChisq",200,0,100,makeCutString(allBut(cuts,2)),True)
makePlots("tar-uncChisq","tarChisq-uncChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots("tar-bscChisq","tarChisq-bscChisq",200,0,100,makeCutString(allBut(cuts,2)),True)

makePlots("trkChisq","max(eleTrkChisq,posTrkChisq)",100,0,100,makeCutString(allBut(cuts,3)),True)

makePlots("trkP_ele","eleP",200,0,1.5,makeCutString(allBut(cuts,4)),True)
makePlots("abstrkP_ele","abs(eleP-1.05*0.5)",200,0,0.5,makeCutString(allBut(cuts,4)),True)

makePlots("uncP","uncP",100,0.5,1.5,makeCutString(allBut(cuts,5)),True)
makePlots("tarP","tarP",100,0.5,1.5,makeCutString(allBut(cuts,5)),True)

makePlots("tarPX/tarP","abs(tarPX)/tarP",100,0,0.04,makeCutString(allBut(cuts,6)),True)
makePlots("bscPX/bscP","abs(bscPX)/bscP",100,0,0.04,makeCutString(allBut(cuts,6)),True)

makePlots("tarPY/tarP","abs(tarPY)/tarP",100,0,0.025,makeCutString(allBut(cuts,7)),True)
makePlots("bscPY/bscP","abs(bscPY)/bscP",100,0,0.025,makeCutString(allBut(cuts,7)),True)

makePlots("tarP_XY_ellipse","sqrt((tarPX/0.04)^2+(tarPY/0.025)^2)/tarP",100,0,1,makeCutString(cuts[:6]),True)
makePlots("tarP_XY_rect","max(abs(tarPX/0.04),abs(tarPY/0.025))/tarP",100,0,1,makeCutString(cuts[:6]),True)
makePlots("tarP_XY_diamond","(abs(tarPX/0.04)+abs(tarPY/0.025))/tarP",100,0,1,makeCutString(cuts[:6]),True)

makePlots("abs_uncVZ","abs(uncVZ+5)",100,0,20,makeCutString(cuts),True)
makePlots("uncVZ","uncVZ",100,-20,20,makeCutString(cuts),True)
makePlots("vzcVX","abs(vzcVX)",100,0,2,makeCutString(cuts),True)
makePlots("vzcVY","abs(vzcVY)",100,0,2,makeCutString(cuts),True)

makePlots("eleTrkD0","abs(eleTrkD0)",100,0,5,makeCutString(cuts),True)
makePlots("eleTrkZ0","abs(eleTrkZ0)",100,0,5,makeCutString(cuts),True)
makePlots("posTrkD0","abs(posTrkD0)",100,0,5,makeCutString(cuts),True)
makePlots("posTrkZ0","abs(posTrkZ0)",100,0,5,makeCutString(cuts),True)

makePlots("minIso","minIso",200,0,5,makeCutString(cuts),False)

#makePlots("bscPX","abs(bscPX/bscP)",100,0,0.05,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("bscPY","abs(bscPY/bscP)",100,0,0.025,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("fda","(bscChisq/5.0)+(0.5/minIso)",100,0,10,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

#makePlots("cut","max(bscChisq/5.0,0.5/minIso)",100,0,5,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

makePlots("minPosIso","minPositiveIso",200,0,5,makeCutString(cuts),False)

makePlots("minNegIso","minNegativeIso",200,0,5,makeCutString(cuts),False)

makePlots("hitX","eleFirstHitX-posFirstHitX",200,-20,20,makeCutString(cuts),True)
makePlots("abs_hitX","abs(eleFirstHitX-posFirstHitX+2)",200,-20,20,makeCutString(cuts),True)
#makePlots("bscVX","abs(bscVX)",200,0,2,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
#makePlots("bscVY","abs(bscVY)",200,0,0.5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
makePlots("elePhiKink","abs(elePhiKink2+elePhiKink3)",200,0,0.01,makeCutString(cuts),True)

makePlots("pdiff","abs(eleP-posP)/(eleP+posP)",200,0,1,makeCutString(cuts),True)
makePlots("abstrkP_pos","abs(posP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)
makePlots("trkP_pos","posP",200,0,1.5,makeCutString(cuts),False)
c.Print(sys.argv[1]+".pdf]")
