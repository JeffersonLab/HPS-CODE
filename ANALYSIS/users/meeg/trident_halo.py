#!/usr/bin/env python
import sys
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <input ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=1.056

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)

gStyle.SetOptFit(1)
inFile = TFile(remainder[1])
#outFile = TFile(remainder[0]+".root","RECREATE")
events = inFile.Get("ntuple")

c = TCanvas("c","c",1200,900);
c.Print(remainder[0]+".pdf[")
gPad.SetLogz()

c.Clear()
events.Draw("uncVZ:uncM>>hnew(100,0,0.1,100,-100,150)","bscChisq<10&&uncP>0.5","colz")
c.Print(remainder[0]+".pdf","Title:mz_all")

c.Clear()
events.Draw("uncVZ:uncM>>hnew(100,0,0.1,100,-100,150)","bscChisq<10&&uncP>0.5&&(eleHasL1&&posHasL1)","colz")
c.Print(remainder[0]+".pdf","Title:mz_L1")

c.Clear()
events.Draw("uncVZ:uncM>>hnew(100,0,0.1,100,-100,150)","bscChisq<10&&uncP>0.5&&(eleHasL1+posHasL1==1)","colz")
c.Print(remainder[0]+".pdf","Title:mz_oneL1")

c.Clear()
events.Draw("uncVZ:uncM>>hnew(100,0,0.1,100,-100,150)","bscChisq<10&&uncP>0.5&&!eleHasL1&&!posHasL1","colz")
c.Print(remainder[0]+".pdf","Title:mz_noL1")

c.Clear()
events.Draw("uncVZ:uncVY>>hnew(100,-3,3,100,-100,150)","bscChisq<10&&uncP>0.5","colz")
c.Print(remainder[0]+".pdf","Title:yz_all")

c.Clear()
events.Draw("uncVZ:uncVY>>hnew(100,-3,3,100,-100,150)","bscChisq<10&&uncP>0.5&&(eleHasL1&&posHasL1)","colz")
c.Print(remainder[0]+".pdf","Title:yz_L1")

c.Clear()
events.Draw("uncVZ:uncVY>>hnew(100,-3,3,100,-100,150)","bscChisq<10&&uncP>0.5&&(eleHasL1+posHasL1==1)","colz")
c.Print(remainder[0]+".pdf","Title:yz_oneL1")

c.Clear()
events.Draw("uncVZ:uncVY>>hnew(100,-3,3,100,-100,150)","bscChisq<10&&uncP>0.5&&!eleHasL1&&!posHasL1","colz")
c.Print(remainder[0]+".pdf)","Title:yz_noL1")
