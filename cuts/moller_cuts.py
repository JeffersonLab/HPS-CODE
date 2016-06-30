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
    c.cd(4)
    rocGraph.Draw("ALP")
    c.Modified()
    c.Print(sys.argv[1]+".pdf".format(name),"Title:"+name)


def allBut(cuts,i):
    return cuts[:i]+cuts[i+1:]
def makeCutString(cuts):
    return reduce(lambda a,b:a+"&&"+b,[str(i) for i in cuts])

cuts=["uncP>0.85",
        "uncP<1.2",
        "tarChisq<50",
        "max(topTrkChisq,botTrkChisq)<50",
        "abs(topTrkT-botTrkT)<4",
        "abs(tarPX)/tarP<0.005",
        "abs(tarPY)/tarP<0.003"]

c.Print(sys.argv[1]+".pdf[")

makePlots("uncP","uncP",100,0.5,1.5,makeCutString(cuts[2:]),True)
makePlots("tarP","tarP",100,0.5,1.5,makeCutString(cuts[2:]),True)
makePlots("abs(uncP)","abs(uncP-1.056)",100,0,1,makeCutString(cuts[2:]),True)
makePlots("abs(vzcP)","abs(vzcP-1.056)",100,0,1,makeCutString(cuts[2:]),True)
makePlots("abs(tarP)","abs(tarP-1.056)",100,0,1,makeCutString(cuts[2:]),True)



makePlots("tarChisq","tarChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots("bscChisq","bscChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots("vzcChisq","vzcChisq",200,0,100,makeCutString(allBut(cuts,2)),True)
makePlots("uncChisq","uncChisq",200,0,100,makeCutString(allBut(cuts,2)),True)
makePlots("tar-uncChisq","tarChisq-uncChisq",200,0,200,makeCutString(allBut(cuts,2)),True)
makePlots("tar-bscChisq","tarChisq-bscChisq",200,0,100,makeCutString(allBut(cuts,2)),True)

makePlots("trkChisq","max(topTrkChisq,botTrkChisq)",100,0,100,makeCutString(allBut(cuts,3)),True)

makePlots("trkDt","abs(topTrkT-botTrkT)",100,0,10,makeCutString(allBut(cuts,4)),True)

makePlots("tarPX/tarP","abs(tarPX)/tarP",100,0,0.04,makeCutString(allBut(cuts,5)),True)
makePlots("vzcPX/vzcP","abs(vzcPX)/vzcP",100,0,0.04,makeCutString(allBut(cuts,5)),True)
makePlots("uncPX/uncP","abs(uncPX)/uncP",100,0,0.04,makeCutString(allBut(cuts,5)),True)

makePlots("tarPY/tarP","abs(tarPY)/tarP",100,0,0.025,makeCutString(allBut(cuts,6)),True)
makePlots("vzcPY/vzcP","abs(vzcPY)/vzcP",100,0,0.025,makeCutString(allBut(cuts,6)),True)
makePlots("uncPY/uncP","abs(uncPY)/uncP",100,0,0.025,makeCutString(allBut(cuts,6)),True)

makePlots("tarP_XY_ellipse","sqrt((tarPX/0.005)^2+(tarPY/0.003)^2)/tarP",100,0,10,makeCutString(cuts[:5]),True)
makePlots("tarP_XY_rect","max(abs(tarPX/0.005),abs(tarPY/0.003))/tarP",100,0,10,makeCutString(cuts[:5]),True)
makePlots("tarP_XY_diamond","(abs(tarPX/0.005)+abs(tarPY/0.003))/tarP",100,0,10,makeCutString(cuts[:5]),True)


makePlots("matchChisq","max(topMatchChisq,botMatchChisq)",100,0,30,makeCutString(cuts),True)
makePlots("matchDt","max(abs(topClT-topTrkT-43),abs(botClT-botTrkT-43))",100,0,20,makeCutString(cuts),True)
makePlots("topMatchDt","abs(topClT-topTrkT-43)",100,0,20,makeCutString(cuts),True)
makePlots("botMatchDt","abs(botClT-botTrkT-43)",100,0,20,makeCutString(cuts),True)


makePlots("clDt","abs(topClT-botClT)",100,0,10,makeCutString(cuts),True)

makePlots("abs_uncVZ","abs(uncVZ+5)",100,0,20,makeCutString(cuts),True)
makePlots("uncVZ","uncVZ",100,-20,20,makeCutString(cuts),True)
makePlots("vzcVX","abs(vzcVX)",100,0,2,makeCutString(cuts),True)
makePlots("vzcVY","abs(vzcVY)",100,0,2,makeCutString(cuts),True)

makePlots("topTrkD0","abs(topTrkD0)",100,0,5,makeCutString(cuts),True)
makePlots("topTrkZ0","abs(topTrkZ0)",100,0,5,makeCutString(cuts),True)
makePlots("botTrkD0","abs(botTrkD0)",100,0,5,makeCutString(cuts),True)
makePlots("botTrkZ0","abs(botTrkZ0)",100,0,5,makeCutString(cuts),True)

makePlots("minIso","minIso",200,0,5,makeCutString(cuts),False)

#makePlots("bscPX","abs(bscPX/bscP)",100,0,0.05,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("bscPY","abs(bscPY/bscP)",100,0,0.025,"{0}&&{1}&&{2}&&{3}&&{4}".format(cut0,cut1,cut2,cut3,cut4),True)

#makePlots("fda","(bscChisq/5.0)+(0.5/minIso)",100,0,10,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

#makePlots("cut","max(bscChisq/5.0,0.5/minIso)",100,0,5,"{0}&&{1}&&{2}".format(cut1,cut3,cut4),True)

makePlots("minPosIso","minPositiveIso",200,0,5,makeCutString(cuts),False)

makePlots("minNegIso","minNegativeIso",200,0,5,makeCutString(cuts),False)

makePlots("hitX","topFirstHitX-botFirstHitX",200,-20,20,makeCutString(cuts),True)
makePlots("abs_hitX","abs(topFirstHitX-botFirstHitX+2)",200,-20,20,makeCutString(cuts),True)
#makePlots("bscVX","abs(bscVX)",200,0,2,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut4),True)
#makePlots("bscVY","abs(bscVY)",200,0,0.5,"{0}&&{1}&&{2}&&{3}".format(cut0,cut1,cut2,cut3),True)
makePlots("topPhiKink","abs(topPhiKink2+topPhiKink3)",200,0,0.01,makeCutString(cuts),True)

makePlots("pdiff","abs(topP-botP)/(topP+botP)",200,0,1,makeCutString(cuts),True)
makePlots("trkP_top","topP",200,0,1.5,makeCutString(cuts),True)
makePlots("abstrkP_top","abs(topP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)
makePlots("abstrkP_bot","abs(botP-1.05*0.5)",200,0,0.5,makeCutString(cuts),True)
makePlots("trkP_bot","botP",200,0,1.5,makeCutString(cuts),False)
c.Print(sys.argv[1]+".pdf]")
