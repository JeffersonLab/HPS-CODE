#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\n"
        sys.exit(0)


if (len(remainder)!=2):
        print sys.argv[0]+' <output basename> <MC>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <MC ROOT file>".format(sys.argv[0])
dataFile = TFile(remainder[1])
dataEvents = dataFile.Get("ntuple")
#dataEvents.SetWeight(1.0/1)

c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")
dataEvents.Draw("triEle1P:triPosP>>(100,0,1,100,0,1)","triEle1P>0","colz")
c.Print(remainder[0]+".pdf","Title:pair1")
dataEvents.Draw("triEle2P:triPosP>>(100,0,1,100,0,1)","triEle2P>0","colz")
c.Print(remainder[0]+".pdf","Title:pair2")
dataEvents.Draw("sign(posPY)*tarPY:tarP>>(100,0.5,1.2,100,-0.01,0.01)","","colz")
c.Print(remainder[0]+".pdf","Title:pt")
dataEvents.Draw("triEle1P:atan2(sqrt(triEle1PX**2+triEle1PY**2),triEle1PZ)>>(100,0,0.05,100,0,1.2)","triEle1P>0","colz")
c.Print(remainder[0]+".pdf","Title:e_theta_ele1")
dataEvents.Draw("triEle2P:atan2(sqrt(triEle2PX**2+triEle2PY**2),triEle2PZ)>>(100,0,0.05,100,0,1.2)","triEle2P>0","colz")
c.Print(remainder[0]+".pdf","Title:e_theta_ele2")
dataEvents.Draw("triPosP:atan2(sqrt(triPosPX**2+triPosPY**2),triPosPZ)>>(100,0,0.05,100,0,1.2)","triPosP>0","colz")
c.Print(remainder[0]+".pdf","Title:e_theta_pos")
c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

