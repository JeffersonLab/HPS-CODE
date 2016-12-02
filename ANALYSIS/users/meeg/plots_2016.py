#!/usr/bin/env python
import sys, array
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend

def makenormplots(files,path,name,c):
	c.Clear()
	color=1
	for f in files:
	    h=f.Get(path)#.Clone()
	    #h.SetDirectory(0)
	    h.SetLineColor(color)
	    h.Scale(1/h.Integral())
	    if color==1:
                    #h.SetName("slice_36")
                    h.GetXaxis().SetTitle("Vertex Z [mm]")
                    h.GetYaxis().SetTitle("Arbitrary units")
		    h.DrawCopy("")
	    else:
                nbins = h.GetXaxis().GetNbins()
                shiftedH = TH1D("shiftedH","test",h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax())
                for i in range(0,nbins-1):
                    shiftedH.SetBinContent(i,h.GetBinContent(i+1))
                    shiftedH.SetBinError(i,h.GetBinError(i+1))
                shiftedH.SetLineColor(color)
                shiftedH.DrawCopy("same")
	    color+=1
	c.SaveAs(sys.argv[1]+"-"+name+".png")

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])

for opt, arg in options:
    if opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\n"
        sys.exit(0)


if (len(remainder)!=3):
        print sys.argv[0]+' <output basename> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
print "\nUsage: {0} <output basename> <data ROOT file> <MC ROOT file>".format(sys.argv[0])
dataFile = TFile(sys.argv[2])
mcFile = TFile(sys.argv[3])
dataEvents = dataFile.Get("ntuple")
mcEvents = mcFile.Get("ntuple")
dataEvents.Draw("uncVZ+5.1>>data(100,-25,25)","bscChisq<5&&uncP>0.8*2.306&&minIso>0.5&&eleHasL1&&posHasL1&&abs(uncM-0.06)<0.01&&run>7700","colz")
mcEvents.Draw("uncVZ>>mc(100,-25,25)","bscChisq<5&&uncP>0.8*2.306&&minIso>0.5&&eleHasL1&&posHasL1&&abs(uncM-0.06)<0.01","colz")

dataH = gDirectory.Get("data")
dataH.GetXaxis().SetTitle("Vertex Z [mm]")
dataH.GetYaxis().SetTitle("Arbitrary units")
dataH.Sumw2()
dataH.Scale(1/dataH.Integral())
mcH = gDirectory.Get("mc")
mcH.Sumw2()
mcH.Scale(1/mcH.Integral())
mcH.SetLineColor(2)
c.SetLogy(1)
dataH.Draw()
mcH.Draw("same")
leg = TLegend(0.1,0.75,0.3,0.9)
leg.AddEntry(dataH,"data")
leg.AddEntry(mcH,"MC")
leg.Draw()
c.SaveAs(sys.argv[1]+".png")
