#!/usr/bin/env python
import sys
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph
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

c.Clear()
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,-0.1,0.1,100,-5,5)","!fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
c.Print(remainder[0]+".pdf","Title:yz_noL1")

c.Clear()
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,-0.1,0.1,100,-5,5)","fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
c.Print(remainder[0]+".pdf","Title:yz_L1")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,0,0.1,100,-5,1)","!fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
hnew = gDirectory.Get("hnew")
hnew.ProfileX()
hnew_1 = gDirectory.Get("hnew_pfx")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",0.025,0.04)
hnew_1.GetYaxis().SetRangeUser(-5,1)
c.Print(remainder[0]+".pdf","Title:top_yz_noL1")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,-0.1,0,100,-1,5)","!fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
hnew = gDirectory.Get("hnew")
hnew.ProfileX()
hnew_1 = gDirectory.Get("hnew_pfx")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",-0.04,-0.025)
hnew_1.GetYaxis().SetRangeUser(-1,5)
c.Print(remainder[0]+".pdf","Title:bot_yz_noL1")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,0,0.1,100,-5,1)","fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
hnew = gDirectory.Get("hnew")
hnew.ProfileX()
hnew_1 = gDirectory.Get("hnew_pfx")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",0.02,0.04)
hnew_1.GetYaxis().SetRangeUser(-5,1)
c.Print(remainder[0]+".pdf","Title:top_yz_L1")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,-0.1,0,100,-1,5)","fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
hnew = gDirectory.Get("hnew")
hnew.ProfileX()
hnew_1 = gDirectory.Get("hnew_pfx")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",-0.04,-0.02)
hnew_1.GetYaxis().SetRangeUser(-1,5)
c.Print(remainder[0]+".pdf","Title:bot_yz_L1")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspFirstHitY:fspFirstHitX>>hasL1(100,-5,5,100,-5,5)","fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
#hnew = gDirectory.Get("hnew")
c.cd(2)
events.Draw("fspTrkZ0+100*fspPY/fspP:fspTrkD0+100*fspPX/fspP>>noL1(100,-3,3,100,-3,3)","!fspHasL1&&fspMatchChisq<5&&fspTrkChisq<25","colz")
c.Print(remainder[0]+".pdf)","Title:l1_position")
