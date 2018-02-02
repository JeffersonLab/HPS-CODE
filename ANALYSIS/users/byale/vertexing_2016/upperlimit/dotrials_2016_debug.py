#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, TLegend, TMath, TRandom
import time
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot, FrequentistCalculator, FeldmanCousins, AsymptoticCalculator
import numpy

def print_usage():
    print "\nUsage: {0} <output basename>".format(sys.argv[0])
    print "Arguments: "
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'n:h')

cutfile=""

n = 10000
#fitBackground = False
#nEvents = 0
#pdf = TF1("eventpdf","1/pol1(0)",0.0,0.1)
#pdf.SetParameters(0.0007153,0.03768)
fitBackground = True
#nEvents = 95
#nEvents = 17
nEvents = 16
#nEvents = 175
pdf = TF1("eventpdf","max(0.0,pol2)",0.0,0.170)
# pre-vtxPatch
#pdf.SetParameters(-4.12,110.2,-613.3)
# vtxPatch
#pdf.SetParameters(-0.4111,15.8,-83.12)
#pdf.SetParameters(2.78,-53.43,490)
# vtxPatch (30% higher, from Mollers in data)
#pdf.SetParameters(-0.05553,4.692,-26.55)
# withBeam
#pdf.SetParameters(-1.445,41.56,-242)
#pdf.SetParameters(3.191,-83.67,723.1)
# x-WBT
pdf.SetParameters(-4.903,115.3,-445.1)
# x-WBT (to120MeV)
#pdf.SetParameters(-10.2,260.6,-1379)

for opt, arg in options:
    if opt=='-n':
        n = int(arg)
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)!=1):
        print_usage()
        sys.exit()

print "{0} datasets".format(n)

mres = TF1("mres","pol1",0.045,0.170)
# pre-vtxPatch
#mres.SetParameters(0.001221,0.01706)
# pre-vtxPatch, denser mass spectrum
#mres.SetParameters(0.0004055,0.02187)
# vtxPatch
#mres.SetParameters(0.0008956,0.01794)
# vtxPatch (30% higher, from Mollers in data)
#mres.SetParameters(0.00116428,0.01794)
# withBeam
#mres.SetParameters(0.0009409,0.01811)
# x-WBT
mres.SetParameters(0.0009572,0.017)


#xval = 0.10483
xval = 0.104213
sigmaAtX = mres.Eval(xval)
print "SigmaAtX: {0}".format(sigmaAtX)
blahh=0
print pdf.IntegralOneDim(xval-1.4*sigmaAtX,xval+1.4*sigmaAtX,1e-12,1e-12,ROOT.Double(blahh))
pdfIntegral = pdf.Integral(0.0,0.130)
print "pdf Integral: {0}".format(pdfIntegral)

if (nEvents==0):
    nEvents = pdfIntegral*0.5/2.8
print nEvents

fullRange = pdf.Integral(0.045 - 1.4*mres.Eval(0.045),0.170+1.4*mres.Eval(0.170))/2.8
print "full range has {0} independent regions".format(fullRange)
rand = TRandom()

c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
outfile = TFile(remainder[0]+".root","RECREATE")
c.SetLogy(0)

n_massbins=90
minmass=0.045
maxmass=0.130

data = TH1D("data","data",100,0.0,0.170)
#pvalHist = TH1D("pval","pval",100000,0,1.0)
#allpvalHist = TH1D("allpval","allpval",100000,0,1.0)
#pvalCdfHist = TH1D("pvalCdf","pvalCdf",100000,0,1.0)
pvalHist = TH1D("pval","pval",100000,1e-5,1.0)
allpvalHist = TH1D("allpval","allpval",100000,1e-5,1.0)
pvalCdfHist = TH1D("pvalCdf","pvalCdf",100000,1e-5,1.0)

lastTime = time.time()
for runnum in xrange(0,n):
    newTime = time.time()
    if newTime-lastTime>10:
        print runnum
        lastTime = newTime
    #print runnum
    data.Reset()
    massArr=array.array('d')
    massWindowArr=array.array('d')
    candArr=array.array('d')
    data.FillRandom("eventpdf",rand.Poisson(nEvents))
    for i in range(0,n_massbins):
        mass = minmass+i*(maxmass-minmass)/(n_massbins-1)
        massArr.append(mass)
        massWindowArr.append(1.4*mres.Eval(mass))
        minbin = data.GetXaxis().FindBin(mass-1.4*mres.Eval(mass))
        maxbin = data.GetXaxis().FindBin(mass+1.4*mres.Eval(mass))
        candArr.append(data.Integral(minbin,maxbin))

    minPval = 1.0
    nbkg = 0.5
    for i in xrange(0,len(massArr)):
        if fitBackground:
            mass = massArr[i]
            sigMassArr = array.array('d')
            sigCandArr = array.array('d')
            hasLowSide = False
            hasHighSide = False
            for j in xrange(0,len(massArr)):
                if abs(mass-massArr[j])>massWindowArr[i]+massWindowArr[j]:
                    if j<i:
                        hasLowSide = True
                    if i<j:
                        hasHighSide = True
                    sigMassArr.append(massArr[j])
                    sigCandArr.append(candArr[j])
            if (hasLowSide and hasHighSide):
                graph=TGraph(len(sigMassArr),sigMassArr,sigCandArr)
                graph.Fit("pol2","Q")
                nbkg = graph.GetFunction("pol2").Eval(mass)
                if nbkg<0.5:
                    nbkg = 0.5
        pval = 1.0-TMath.Prob(2*nbkg,2*int(candArr[i]))
        if pval>0.5:
            pval = 0.5
        allpvalHist.Fill(pval)
        if pval<minPval:
            minPval = pval
    pvalHist.Fill(minPval)

total = 0.0
for i in xrange(0,pvalHist.GetXaxis().GetNbins()+1):
    total+=pvalHist.GetBinContent(i)
    center = pvalHist.GetXaxis().GetBinCenter(i)
    pvalCdfHist.SetBinContent(i,total/n)

c.SetLogx()
c.SetLogy()
pvalHist.Draw()
c.Print(remainder[0]+".pdf")
allpvalHist.Draw()
c.Print(remainder[0]+".pdf")
c.SetLogy(0)
pvalHist.Draw()
c.Print(remainder[0]+".pdf")
allpvalHist.Draw()
c.Print(remainder[0]+".pdf")

gStyle.SetOptStat(0)
pvalCdfHist.Draw()
pvalCdfHist.SetTitle("")
pvalCdfHist.GetXaxis().SetTitle("local p-value")
pvalCdfHist.GetYaxis().SetTitle("global p-value")
pvalCdfHist.GetXaxis().SetRangeUser(1e-5,0.5)
pvalCdfHist.GetYaxis().SetRangeUser(1e-5,1)
c.Print(remainder[0]+".pdf")
pvalCdfHist.GetXaxis().SetRangeUser(1e-5,1.0)
pvalCdfHist.GetYaxis().SetRangeUser(1e-5,1.0)
c.SetLogy()
c.SetLogx()
pvalCdfHist.Draw()
c.Print(remainder[0]+".pdf")

c.SetLogy(0)
c.SetLogx(0)
gStyle.SetOptStat(1)

#ncand = TF1("fitfunc","[0]*exp( ((x-[1])<[3])*(-0.5*(x-[1])^2/[2]^2) + ((x-[1])>=[3])*(-0.5*[3]^2/[2]^2-(x-[1]-[3])/[4]))",-50,50)
mres.Draw()
c.Print(remainder[0]+".pdf")
pdf.Draw()
c.Print(remainder[0]+".pdf")
data.Draw()
c.Print(remainder[0]+".pdf")

graph=TGraph(len(massArr),massArr,candArr)
graph.SetTitle("candidate events")
graph.Draw("A*")
graph.GetXaxis().SetMoreLogLabels()
c.Print(remainder[0]+".pdf","Title:test")
graph.Fit("pol2")
c.Print(remainder[0]+".pdf","Title:test")

#graph=TGraph(len(poiMassArr),poiMassArr,poiSigArr)
#graph.SetTitle("cut-and-count significance")
#graph.Draw("A*")
#graph.GetXaxis().SetMoreLogLabels()
#c.Print(remainder[0]+".pdf","Title:test")

#graph=TGraph(len(poiMassArr),poiMassArr,poiBkgArr)
#graph.SetTitle("cut-and-count estimated background")
#graph.Draw("A*")
#graph.GetXaxis().SetMoreLogLabels()
#c.Print(remainder[0]+".pdf","Title:test")

#c.SetLogy(1)
#graph=TGraph(len(poiMassArr),poiMassArr,poiPvalArr)
#graph.SetTitle("cut-and-count p-value")
#graph.Draw("A*")
#graph.GetXaxis().SetMoreLogLabels()
#c.Print(remainder[0]+".pdf","Title:test")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()
