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


#if (len(remainder)!=4):
#        print sys.argv[0]+' <output basename> <RAD> <tritrig> <WAB>'
#        sys.exit()

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600);
#print "\nUsage: {0} <output basename> <MC ROOT tuple> <data ROOT tuple>".format(sys.argv[0])
mcFile = TFile(remainder[1])
dataFile = TFile(remainder[2])
#wabFile = TFile(remainder[3])
mcEvents = mcFile.Get("ntuple")
dataEvents = dataFile.Get("ntuple")
#wabEvents = wabFile.Get("cut")

#nbins = 50
#width = 0.1
#scaling = nbins/width#500

# Moller Normalizations
mcEvents.SetWeight(1000/(74*(2e6)*(2500)*(4.062e-4)*(6.306e-2)*1000)) # MC XS (mb)
dataEvents.SetWeight(1000*4097/(74*112.166690534e9)) # Data XS, 10% 798* golden runs (mb)

c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")

########################## CUTS #######################
#massVar = "uncM"
massVar = "bscM"
#massVar = "tarM"
#massVar = "mRefitUnc"

#pair1 = ""
#pair1 = "isSingle0&&topTrkLambda*botTrkLambda<0"
#pair1 = "topClY*botClY<0"
#pair1 = "isSingle0&&topClY*botClY<0"

#pair1 = "isSingle0&&topTrkLambda*botTrkLambda<0"
pair1 = "topTrkLambda*botTrkLambda<0"
#pair1 = "isPair1&&eleSlope*posSlope<0"
#L1L1 = "&&topHasL1&&botHasL1"
L1L1 = "&&(topHasL1&&botHasL1)&&(topHasL2||botHasL2)"
#Chi2 = "&&(topClY-topTrkEcalY)>-10&&(topClY-topTrkEcalY)<10&&(botClY-botTrkEcalY)<10&&(botClY-botTrkEcalY)>-10"
#Chi2 = ""
Chi2 = "&&topMatchChisq+botMatchChisq<10000"
#Chi2 = "&&topMatchChisq+botMatchChisq<30&&topTrkChisq+botTrkChisq<50"
#Chi2 = "&&topMatchChisq+botMatchChisq<40&&topTrkChisq+botTrkChisq<70"
#Chi2 = "&&max(topMatchChisq,botMatchChisq)<10&&bscChisq<10&&bscChisq-uncChisq<5&&max(topTrkChisq,botTrkChisq)<30"
#Chi2 = "&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30"
#time=""
time = "&&abs(topTrkT-botTrkT)<2"
#time = "&&abs(topClT-botClT)<2"
#time = "&&max(abs(topClT-topTrkT-151.2),abs(botClT-botTrkT-151.2))<4&&abs(topClT-botClT)<2"
#time = "&&max(abs(eleClT-eleTrkT)-10000,abs(posClT-posTrkT)-10000)<4&&abs(eleClT-posClT)<2"
#isolation = "&&min(eleMinPositiveIso+0.5*(eleTrkZ0+0*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+0*posPY/posP)*sign(posPY))>0"
#isolation = ""
isolation = "&&min(topMinPositiveIso+0.5*(topTrkZ0+0.5*topPY/topP)*sign(topPY),botMinPositiveIso+0.5*(botTrkZ0+0.5*botPY/botP)*sign(botPY))>0"
asymmetry = ""
#asymmetry = "&&abs(topP-botP)/(topP+botP)<0.4"
#doca  = ""
#doca = "&&posTrkD0+0*posPX/posP<1.5"
#doca = "&&botTrkD0+0.5*botPX/botP<1.5"
#doca = "&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.040&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.048&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)>0.016&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)<0.028&&atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.016&&atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.028"
doca = "&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)<0.048&&atan2(sqrt(topPX*topPX + topPY*topPY),topPZ)+atan2(sqrt(botPX*botPX + botPY*botPY),botPZ)>0.030"
#energy = ""
energy = "&&topP<2.3*0.75&&botP<2.3*0.75"
rad = "&&bscP>0.75*2.3&&bscP<2.3*1.15"
#rad = "&&bscP>0.75*2.3"

##############################################################################################

mcEvents.Draw(massVar+">>mc(200,0.03,0.1)",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad,"")
c.Print(remainder[0]+".pdf","Title:data_1d")
dataEvents.Draw(massVar+">>data(200,0.03,0.1)",pair1+energy+L1L1+time+isolation+asymmetry+doca+Chi2+rad+"&&isSingle0","")
c.Print(remainder[0]+".pdf","Title:data_1d")

mcHist = gDirectory.Get("mc")
dataHist = gDirectory.Get("data")
#wabHist = gDirectory.Get("wab")

mcHist.SetLineColor(1)
mcHist.Draw()
c.Print(remainder[0]+".pdf","Title:data_1d")

dataHist.SetLineColor(2)
dataHist.Draw("same")

leg = TLegend(0.5,0.75,0.9,0.9)
leg.AddEntry(mcHist,"MC")
leg.AddEntry(dataHist,"Data")
leg.Draw()
c.Print(remainder[0]+".pdf","Title:data_1d")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()
