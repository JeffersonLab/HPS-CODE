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


if (len(remainder)!=3):
        print sys.argv[0]+' <output basename> <data> <tritrig> <WAB>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
dataFile = TFile(remainder[1])
triFile = TFile(remainder[2])
dataEvents = dataFile.Get("ntuple")
triEvents = triFile.Get("ntuple")
dataEvents.SetWeight(1.0/119.3)
triEvents.SetWeight(1.0/(5.65e-3*4862))

c.Print(sys.argv[1]+".pdf[")
outfile = TFile(sys.argv[1]+".root","RECREATE")
dataEvents.Draw("tarP>>(30,0,1.5)","isPulser&&run==5774&&abs(eleTrkT-posTrkT)<3&&eleP<0.8&&elePY*posPY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50&&max(eleMatchChisq,posMatchChisq)>5","colz")
dataEvents.Draw("tarP>>(30,0,1.5)","isPulser&&run==5774&&abs(eleTrkT-posTrkT)<3&&eleP<0.8&&elePY*posPY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50&&max(eleMatchChisq,posMatchChisq)<5","colz")
dataEvents.Draw("tarP>>(30,0,1.5)","isPulser&&run==5774&&abs(eleTrkT-posTrkT)<3&&eleP<0.8&&elePY*posPY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50","colz")
dataEvents.Draw("eleTrkEcalY:eleTrkEcalX>>(50,-400,0,50,-100,100)","isPulser&&run==5774&&tarP>0.5*1.056&&abs(eleTrkT-posTrkT)<3&&eleP<0.8&&elePY*posPY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50&&max(eleMatchChisq,posMatchChisq)>5","colz")
dataEvents.Draw("eleTrkEcalY:eleTrkEcalX>>(50,-400,0,50,-100,100)","isPulser&&run==5774&&tarP>0.5*1.056&&abs(eleTrkT-posTrkT)<3&&eleP<0.8&&elePY*posPY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50&&max(eleMatchChisq,posMatchChisq)<5","colz")
c.Print(sys.argv[1]+".pdf","Title:data_1d")
dataEvents.Draw("eleP:posP>>data2d(100,0,1.0,100,0,1.0)","abs(elePX/eleP)<0.005&&abs(posPX/posP)<0.005&&abs(abs(elePY/eleP)-0.04)<0.005&&abs(abs(posPY/posP)-0.04)<0.005&&elePY*posPY<0","colz")
c.Print(sys.argv[1]+".pdf","Title:data_sd")
triEvents.Draw("tarP>>tritrig1d(100,0,1.5)","abs(elePX/eleP)<0.005&&abs(posPX/posP)<0.005&&abs(abs(elePY/eleP)-0.04)<0.005&&abs(abs(posPY/posP)-0.04)<0.005&&elePY*posPY<0","colz")
c.Print(sys.argv[1]+".pdf","Title:tritrig_1d")
triEvents.Draw("eleP:posP>>tritrig2d(100,0,1.0,100,0,1.0)","abs(elePX/eleP)<0.005&&abs(posPX/posP)<0.005&&abs(abs(elePY/eleP)-0.04)<0.005&&abs(abs(posPY/posP)-0.04)<0.005&&elePY*posPY<0","colz")
c.Print(sys.argv[1]+".pdf)","Title:tritrig_2d")
outfile.Write()
outfile.Close()

