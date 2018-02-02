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
#print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
radFile = TFile(remainder[1])
triFile = TFile(remainder[2])
wabFile = TFile(remainder[3])
radFile_old = TFile(remainder[4])
triFile_old = TFile(remainder[5])
wabFile_old = TFile(remainder[6])

radEvents = radFile.Get("cut")
triEvents = triFile.Get("cut")
wabEvents = wabFile.Get("cut")
radEvents_old = radFile_old.Get("cut")
triEvents_old = triFile_old.Get("cut")
wabEvents_old = wabFile_old.Get("cut")

#nbins = 50
#width = 0.1
#scaling = nbins/width#500

# weight= (*/(n_gen/XS)*n_files)
#radEvents.SetWeight(500e-6/((10e4/0.154e6)*10))
#triEvents.SetWeight(500e-6/(0.0682*375))
#wabEvents.SetWeight(500e-6/((9.5e4/0.7e9)*995))
#1.056GeV
#radEvents.SetWeight(500e-6/((10e4/0.05565822e6)*99))

# 2016 rotationFix
#radEvents_old.SetWeight(500e-6/((10e4/0.023850e6/0.75962615429)*99))
#triEvents_old.SetWeight(500e-6/((10e4/0.495271980e6/0.75962615429)*100))
#wabEvents_old.SetWeight(500e-6/((15.785e4/0.163739790600e9/0.81367305033)*498))

# 2016 MG_alphaFix
#radEvents_old.SetWeight(500e-6/((10e4/0.06636e6)*10))
#radEvents.SetWeight(500e-6/((10e4/0.0667e6)*10))
#triEvents_old.SetWeight(500e-6/((10e4/1.1416e6)*100))
#triEvents.SetWeight(500e-6/((10e4/1.1416e6)*100))
#wabEvents.SetWeight(500e-6/((10e4/181.7e6)*1000))
#wabEvents_old.SetWeight(500e-6/((10e4/220.6e6)*1000))

# 2016 MG_alphaFix
radEvents_old.SetWeight(500e-6/((10e4/0.0667e6)*100))
radEvents.SetWeight(500e-6/((10e4/0.0667e6)*100))
triEvents_old.SetWeight(500e-6/((10e4/1.1416e6)*1000))
triEvents.SetWeight(500e-6/((10e4/1.1416e6)*900))
wabEvents.SetWeight(500e-6/((10e4/220.6e6)*9898))
wabEvents_old.SetWeight(500e-6/((10e4/220.6e6)*10000))

c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")


radEvents.Draw("uncM>>rad(50,0.0,0.2)","triPair1P>0.8*2.3","E1")
c.Print(remainder[0]+".pdf","Title:data_1d")
triEvents.Draw("uncM>>tri(50,0.0,0.2)","","E1")
c.Print(remainder[0]+".pdf","Title:data_1d")
wabEvents.Draw("uncM>>wab(50,0.0,0.2)","","E1")
c.Print(remainder[0]+".pdf","Title:data_1d")

radEvents_old.Draw("uncM>>rad_old(50,0.0,0.2)","triPair1P>0.8*2.3","E1")
c.Print(remainder[0]+".pdf","Title:data_1d")
triEvents_old.Draw("uncM>>tri_old(50,0.0,0.2)","","E1")
c.Print(remainder[0]+".pdf","Title:data_1d")
wabEvents_old.Draw("uncM>>wab_old(50,0.0,0.2)","","E1")
c.Print(remainder[0]+".pdf","Title:data_1d")

radHist = gDirectory.Get("rad")
triHist = gDirectory.Get("tri")
wabHist = gDirectory.Get("wab")
totalHist = triHist.Clone("total")
totalHist.Add(wabHist)
totalHist.Draw("E1")
c.Print(remainder[0]+".pdf","Title:data_1d")

totalHist.Draw("E1")
totalHist.SetLineColor(1)
totalHist.SetTitle("Pair cross-sections")
totalHist.GetXaxis().SetTitle("pair invariant mass [GeV]")
totalHist.GetYaxis().SetTitle("cross-section [mb/GeV]")
radHist.Draw("same")
radHist.SetLineColor(2)
wabHist.Draw("same")
wabHist.SetLineColor(3)
othertriHist = triHist.Clone("othertri")
othertriHist.Add(radHist,-1)
othertriHist.Draw("same")
othertriHist.SetLineColor(4)
leg = TLegend(0.5,0.75,0.9,0.9)
leg.AddEntry(totalHist,"Combined rate")
leg.AddEntry(radHist,"Radiative tridents")
leg.AddEntry(wabHist,"Wide-angle bremsstrahlung conversions")
leg.AddEntry(othertriHist,"Non-radiative tridents")
leg.Draw()
c.Print(remainder[0]+".pdf","Title:data_1d")

radfracHist = radHist.Clone("radfrac")
radfracHist.SetLineColor(1)
radfracHist.SetTitle("Radiative fraction")
radfracHist.Divide(totalHist)
radfracHist.GetXaxis().SetRangeUser(0,0.17)
radfracHist.GetYaxis().SetRangeUser(0,0.5)
radfracHist.GetXaxis().SetTitle("pair invariant mass [GeV]")
radfracHist_ratio = radfracHist.Clone("radfrac_xWBT/xBeam")
radfracHist.GetYaxis().SetTitle("radiative fraction")
radfracHist.Fit("pol3","","",0.027,0.18)
c.Print(remainder[0]+".pdf","Title:data_1d")

# new/old ratios
radHist_ratio = radHist.Clone("rad_new_old")
radHist_ratio.SetTitle("Radiatives new/old")
radHist_old = gDirectory.Get("rad_old")
radHist_ratio.Divide(radHist_old)
radHist_ratio.Draw("E1")
c.Print(remainder[0]+".pdf","Title:ratio")

trifracHist_ratio = triHist.Clone("tri_new_old")
trifracHist_ratio.SetTitle("tritrig new/old")
triHist_old = gDirectory.Get("tri_old")
trifracHist_ratio.Draw("E1")
trifracHist_ratio.Divide(triHist_old)
c.Print(remainder[0]+".pdf","Title:ratio")

wabfracHist_ratio = wabHist.Clone("wab_new_old")
wabfracHist_ratio.SetTitle("wab new/old")
wabHist_old = gDirectory.Get("wab_old")
wabfracHist_ratio.Draw("E1")
wabfracHist_ratio.Divide(wabHist_old)
c.Print(remainder[0]+".pdf","Title:ratio")

#radfracHist_old = radHist_old.Clone("radfrac_old")
#totalHist_old = triHist_old.Clone("total_old")
#totalHist_old.Add(wabHist_old)
#radfracHist_old.Divide(totalHist_old)
#radfracHist_ratio.Divide(radfracHist_old)
#radfracHist_ratio.SetTitle("Radiative fraction new/old")
#radfracHist_ratio.GetYaxis().SetRangeUser(0,2)
#radfracHist_ratio.Draw("E1")
#c.Print(remainder[0]+".pdf","Title:data_1d")

radfracHist_worst = radHist_old.Clone("radfrac_worst")
#radfracHist.SetTitle("Radiative fraction")
#radfracHist.GetXaxis().SetTitle("pair invariant mass [GeV]")
#radfracHist.GetYaxis().SetTitle("radiative fraction")
totalHist_worst = triHist_old.Clone("total_worst")
totalHist_worst.Add(wabHist_old)
radfracHist_worst.Divide(totalHist_worst)

radfracHist_ratio.Divide(radfracHist_worst)
radfracHist_ratio.SetTitle("Radiative fraction x-WBT/x-beam")
#radfracHist_ratio.GetXaxis().SetRangeUser(0,0.17)
radfracHist_ratio.GetYaxis().SetRangeUser(0.5,1.5)
#radfracHist.Fit("pol3","","",0.027,0.18)
radfracHist_ratio.Draw("E1")
c.Print(remainder[0]+".pdf","Title:data_1d")


c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

