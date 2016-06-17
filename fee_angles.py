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

#c.Divide(4,2)
#for i in xrange(1,5):
    #energy=0.3+(i-1)*0.1
    #events.Draw("acos(topPZ/topP)-acos(1-0.511e-3*(1/topP-1/1.056)):atan2(topPX,topPY)>>hnew(30,-1,1,50,-0.01,0.01)","abs(uncM*1.056/uncP-0.033)<0.003&&abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(topP-{0})<0.05".format(energy),"goff,colz")
    #hnew = gDirectory.Get("hnew")
    #c.cd(i)
    #hnew.DrawCopy("colz")
    #hnew.FitSlicesY()
    #hnew_1 = gDirectory.Get("hnew_1")
    #c.cd(i+4)
    #hnew_1.GetYaxis().SetRangeUser(-0.005,0.005)
    #hnew_1.Fit("pol1","","",-0.4,0.4)
    #hnew_1.DrawCopy()
#c.Print(remainder[0]+".pdf","Title:top_etheta")
#
#c.Clear()
#c.Divide(4,2)
#for i in xrange(1,5):
    #energy=0.3+(i-1)*0.1
    #events.Draw("acos(botPZ/botP)-acos(1-0.511e-3*(1/botP-1/1.056)):atan2(botPX,-botPY)>>hnew(30,-1,1,50,-0.01,0.01)","abs(uncM*1.056/uncP-0.033)<0.003&&abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(botP-{0})<0.05".format(energy),"goff,colz")
    #hnew = gDirectory.Get("hnew")
    #c.cd(i)
    #hnew.DrawCopy("colz")
    #hnew.FitSlicesY()
    #hnew_1 = gDirectory.Get("hnew_1")
    #c.cd(i+4)
    #hnew_1.GetYaxis().SetRangeUser(-0.005,0.005)
    #hnew_1.Fit("pol1","","",-0.4,0.4)
    #hnew_1.DrawCopy()
#c.Print(remainder[0]+".pdf","Title:bot_etheta")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,0,0.1,100,-1,1)","(isSingle0||isSingle1)&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*{0}&&abs(fspPX/fspP)<0.01&&fspPY>0".format(ebeam),"colz")
hnew = gDirectory.Get("hnew")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_1")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",0.03,0.05)
hnew_1.GetYaxis().SetRangeUser(0,0.4)
c.Print(remainder[0]+".pdf","Title:top_yz")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspTrkZ0:fspPY/fspP>>hnew(100,-0.1,0,100,-1,1)","(isSingle0||isSingle1)&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*{0}&&abs(fspPX/fspP)<0.01&&fspPY<0".format(ebeam),"colz")
hnew = gDirectory.Get("hnew")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_1")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",-0.05,-0.03)
hnew_1.GetYaxis().SetRangeUser(-0.4,0)
c.Print(remainder[0]+".pdf","Title:bot_yz")

c.Clear()
c.Divide(1,2)
c.cd(1)
#events.Draw("fspP>>hnew(100,0.75,1.5)","fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.9&&fspPY>0","colz")
events.Draw("fspP:fspPX/fspP>>hnew(100,-0.1,0.15,100,{0},{1})".format(0.7*ebeam,1.3*ebeam),"(isSingle0||isSingle1)&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*{0}&&fspPY/fspP>0.03".format(ebeam),"colz")
hnew = gDirectory.Get("hnew")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_1")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",-0.06,0.01)
hnew_1.GetYaxis().SetRangeUser(0.95*ebeam,1.05*ebeam)
c.Print(remainder[0]+".pdf","Title:top_px")

c.Clear()
c.Divide(1,2)
c.cd(1)
events.Draw("fspP:fspPX/fspP>>hnew(100,-0.1,0.15,100,{0},{1})".format(0.7*ebeam,1.3*ebeam),"(isSingle0||isSingle1)&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*{0}&&fspPY/fspP<-0.03".format(ebeam),"colz")
hnew = gDirectory.Get("hnew")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_1")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",-0.06,0.01)
hnew_1.GetYaxis().SetRangeUser(0.95*ebeam,1.05*ebeam)
c.Print(remainder[0]+".pdf","Title:bot_px")

c.Clear()
c.Divide(1,2)
c.cd(1)
#events.Draw("fspP>>hnew(100,0.75,1.5)","fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.9&&fspPY>0","colz")
events.Draw("fspP:fspPY/fspP>>hnew(100,0,0.1,100,{0},{1})".format(0.7*ebeam,1.3*ebeam),"(isSingle0||isSingle1)&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*{0}&&abs(fspPX/fspP)<0.01&&fspPY>0".format(ebeam),"colz")
hnew = gDirectory.Get("hnew")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_1")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",0.03,0.05)
hnew_1.GetYaxis().SetRangeUser(0.95*ebeam,1.05*ebeam)
c.Print(remainder[0]+".pdf","Title:top_py")

c.Clear()
c.Divide(1,2)
c.cd(1)
#events.Draw("fspP>>hnew(100,0.75,1.5)","fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.9&&fspPY>0","colz")
events.Draw("fspP:fspPY/fspP>>hnew(100,-0.1,0,100,{0},{1})".format(0.7*ebeam,1.3*ebeam),"(isSingle0||isSingle1)&&fspTrkHits==6&&fspMatchChisq<3&&fspClE>0.85*{0}&&abs(fspPX/fspP)<0.01&&fspPY<0".format(ebeam),"colz")
hnew = gDirectory.Get("hnew")
hnew.FitSlicesY()
hnew_1 = gDirectory.Get("hnew_1")
c.cd(2)
hnew_1.Draw()
hnew_1.Fit("pol1","","",-0.05,-0.03)
hnew_1.GetYaxis().SetRangeUser(0.95*ebeam,1.05*ebeam)
c.Print(remainder[0]+".pdf)","Title:bot_py")

#c.Clear()
#c.Divide(4,2)
#for i in xrange(1,5):
    #energy=0.3+(i-1)*0.1
    #events.Draw("topTrkD0:topPX/topP>>hnew(100,-0.05,0.05,100,-2,2)","abs(uncM*1.056/uncP-0.033)<0.003&&abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(topP-{0})<0.05".format(energy),"goff,colz")
    #hnew = gDirectory.Get("hnew")
    #c.cd(i)
    #hnew.DrawCopy("colz")
    #hnew.FitSlicesY()
    #hnew_1 = gDirectory.Get("hnew_1")
    #c.cd(i+4)
    #hnew_1.GetYaxis().SetRangeUser(-0.5,0.5)
    #hnew_1.Fit("pol1","","",-0.01,0.01)
    #hnew_1.DrawCopy()
#c.Print(remainder[0]+".pdf","Title:top_xz")
#
#c.Clear()
#c.Divide(4,2)
#for i in xrange(1,5):
    #energy=0.3+(i-1)*0.1
    #events.Draw("botTrkD0:botPX/botP>>hnew(100,-0.05,0.05,100,-2,2)","abs(uncM*1.056/uncP-0.033)<0.003&&abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(botP-{0})<0.05".format(energy),"goff,colz")
    #hnew = gDirectory.Get("hnew")
    #c.cd(i)
    #hnew.DrawCopy("colz")
    #hnew.FitSlicesY()
    #hnew_1 = gDirectory.Get("hnew_1")
    #c.cd(i+4)
    #hnew_1.GetYaxis().SetRangeUser(-0.5,0.5)
    #hnew_1.Fit("pol1","","",-0.01,0.01)
    #hnew_1.DrawCopy()
#c.Print(remainder[0]+".pdf","Title:bot_xz")
#
#c.Clear()
#c.Divide(1,2)
#c.cd(1)
#events.Draw("topTrkD0:topP>>hnew(100,0,1,100,-1,1)","abs(uncM*1.056/uncP-0.033)<0.003&&abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(topPX/topP)<0.01","colz")
#hnew = gDirectory.Get("hnew")
#hnew.FitSlicesY()
#hnew_1 = gDirectory.Get("hnew_1")
#c.cd(2)
#hnew_1.Draw()
#hnew_1.Fit("pol1","","",0.4,0.7)
#hnew_1.GetYaxis().SetRangeUser(-0.5,0.5)
#c.Print(remainder[0]+".pdf","Title:top_xp")
#
#c.Clear()
#c.Divide(1,2)
#c.cd(1)
#events.Draw("botTrkD0:botP>>hnew(100,0,1,100,-1,1)","abs(uncM*1.056/uncP-0.033)<0.003&&abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(botPX/botP)<0.01","colz")
#hnew = gDirectory.Get("hnew")
#hnew.FitSlicesY()
#hnew_1 = gDirectory.Get("hnew_1")
#c.cd(2)
#hnew_1.Draw()
#hnew_1.Fit("pol1","","",0.4,0.7)
#hnew_1.GetYaxis().SetRangeUser(-0.5,0.5)
#c.Print(remainder[0]+".pdf","Title:bot_xp")
#
#c.Clear()
#c.Divide(1,2)
#c.cd(1)
#events.Draw("(uncM*1.056/uncP):atan2(topPY-botPY,topPX-botPX)>>hnew(100,0,3,100,0.03,0.04)","abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(topP-botP)<0.1","colz")
#hnew = gDirectory.Get("hnew")
#hnew.FitSlicesY()
#hnew_1 = gDirectory.Get("hnew_1")
#c.cd(2)
#hnew_1.Draw()
#hnew_1.Fit("pol1","","",1,2)
#hnew_1.GetYaxis().SetRangeUser(0.03,0.04)
#c.Print(remainder[0]+".pdf","Title:m_phi")
#
#c.Clear()
#c.Divide(1,2)
#c.cd(1)
#events.Draw("(uncM*1.056/uncP):topP-botP>>hnew(100,-1,1,100,0.03,0.04)","abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(atan2(topPY-botPY,topPX-botPX)-TMath::Pi()/2)<0.1","colz")
#hnew = gDirectory.Get("hnew")
#hnew.FitSlicesY()
#hnew_1 = gDirectory.Get("hnew_1")
#c.cd(2)
#hnew_1.Draw()
#hnew_1.Fit("pol1","","",-0.4,0.4)
#hnew_1.GetYaxis().SetRangeUser(0.03,0.04)
#c.Print(remainder[0]+".pdf","Title:m_theta")
#
#c.Clear()
#c.Divide(1,2)
#c.cd(1)
#events.Draw("uncPY:uncPX>>hnew(100,-0.01,0.01,100,-0.01,0.01)","abs(topTrkT-botTrkT)<3&&abs(uncPY)<0.005&&abs(uncPX)<0.005&&abs(uncM*1.056/uncP-0.033)<0.003","colz")
#c.cd(2)
#events.Draw("uncM:uncP>>(100,0.9,1.15,100,0.025,0.04)","","colz")
#c.Print(remainder[0]+".pdf)","Title:vtx")

#c.Print(remainder[0]+".pdf]")
