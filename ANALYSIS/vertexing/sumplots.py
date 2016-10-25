#!/usr/bin/env python
import sys, array,math
import getopt
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'yzh', ['luminosity','help',])

logy = False
logz = False
for opt, arg in options:
    if opt in ('-l', '--luminosity'):
        lumi = float(arg)
        scale_factor = lumi/lumi_total
    elif opt in ('-y'):
        logy = True
    elif opt in ('-z'):
        logz = True
    elif opt in ('-h', '--help'):
        print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
        print "Arguments: "
        print "\t-l, --luminosity: luminosity for normalization"
        print "\n"
        sys.exit(0)


if (len(remainder)<3):
        print sys.argv[0]+' <output basename> <path> <root files>'
        sys.exit()

c = TCanvas("c","c",800,600);
outfile = TFile(remainder[0]+".root","RECREATE")
plotpath = remainder[1]
print plotpath
totalH = None
for filename in remainder[2:]:
    f=TFile(filename)
    print filename
    h=f.Get(plotpath)
    if totalH is None:
        #totalH=TH2D(h)
        totalH=h.Clone("")
        totalH.SetDirectory(outfile)
    else:
        totalH.Add(h)


outfile.cd()
#totalH.Sumw2()
#totalH.Scale(1/scale_factor)
if logy:
    c.SetLogy(1)
if logz:
    c.SetLogz(1)
totalH.Draw("colz")
c.SaveAs(sys.argv[1]+"-sum.png")
outfile.Write()
outfile.Close()
sys.exit(0)




