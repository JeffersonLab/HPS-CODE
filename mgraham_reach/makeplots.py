#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TFile, gStyle, TH1D, TCutG, TH2D, gDirectory, gPad, TMath

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def print_usage():
    print "\nUsage: {0} <output basename> <input ROOT file> <acceptance ROOT file> <tails ROOT file> <radfrac ROOT file>".format(sys.argv[0])
    print "./fitvtx.py stuff ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails.root ../frac.root -u"
    print "Arguments: "
    print '\t-h: this help message'
    print "\n"

outputname = "mgraham_signal"
gROOT.SetBatch(True)
c = TCanvas("c","c",800,600);
c.Print(outputname+".pdf[")
outfile = TFile(outputname+".root","RECREATE")
n_massbins=10
minmass=0.010
maxmass=0.028
n_epsbins=10
mineps=-10.0
maxeps=-7.5
firsteps = 0.00001
epsstep = 0.0000306228


xedges = array.array('d')
yedges = array.array('d')
for i in range(0,n_massbins+1):
    print minmass+(i)*(maxmass-minmass)/(n_massbins-1)
    xedges.append(minmass+(i-0.5)*(maxmass-minmass)/(n_massbins-1))
for j in range(0,n_epsbins+1):
    #yedges.append(10**(mineps+(j-0.5)*(maxeps-mineps)/(n_epsbins-1)))
    print (firsteps + (j)*epsstep)
    yedges.append((firsteps + (j-0.5)*epsstep)**2)

yedges[0] = 0.8*(firsteps**2)
xedges[n_massbins] = 0.03
xedges.append(0.06)
n_massbins+=1
print xedges
print yedges
detectableHist=TH2D("detectable","detectable",n_massbins,xedges,n_epsbins,yedges)

f = open("data.txt")
for line in f:
    linesplit = line.split()
    mass = float(linesplit[0])
    eps = float(linesplit[2])
    detectable = float(linesplit[4])
    detectableHist.Fill(mass,eps**2,detectable)

def drawContour(hist,nlevels):
    #minValue = hist.GetBinContent(hist.GetMinimumBin())
    minValue = hist.GetMinimum(0)
    bottom = int(math.floor(math.log10(minValue)))
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [GeV]")
    hist.GetYaxis().SetTitle("epsilon^2")
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))
def drawMaxContour(hist,nlevels):
    maxValue = hist.GetBinContent(hist.GetMaximumBin())
    bottom = int(math.floor(math.log10(maxValue)))-nlevels+1
    limitLevels = array.array('d')
    for i in range(bottom,bottom+nlevels):
        for j in range(1,10):
            limitLevels.append((10**i)*j)
    hist.SetContour(len(limitLevels),limitLevels)
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [GeV]")
    hist.GetYaxis().SetTitle("epsilon^2")
    hist.Draw("cont1z")
    hist.GetZaxis().SetRangeUser(10**bottom,10**(bottom+nlevels))
def drawHist(hist,nlevels,minz,maxz):
    hist.SetContour(nlevels)
    hist.Draw("colz")
    hist.GetXaxis().SetMoreLogLabels()
    hist.GetXaxis().SetTitle("mass [GeV]")
    hist.GetYaxis().SetTitle("epsilon^2")
    hist.GetZaxis().SetRangeUser(minz,maxz)


gStyle.SetOptStat(0)
c.SetLogx(1)
c.SetLogy(1)
c.SetLogz(1)
detectableHist.GetXaxis().SetRangeUser(0.01,0.03)
drawMaxContour(detectableHist,3)
c.Print(outputname+".pdf","Title:tada")
drawHist(detectableHist,20,1e-2,2.4)
c.Print(outputname+".pdf","Title:tada")

detectableHist.GetXaxis().SetRangeUser(0.02,0.06)
drawMaxContour(detectableHist,3)
c.Print(outputname+".pdf","Title:tada")
drawHist(detectableHist,20,1e-2,2.4)
c.Print(outputname+".pdf","Title:tada")

c.Print(outputname+".pdf]")
outfile.Write()
outfile.Close()
sys.exit(0)

