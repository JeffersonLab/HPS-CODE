#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, RooDataSet
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot, FrequentistCalculator, FeldmanCousins
import upperlimit
import numpy

def print_usage():
    print "\nUsage: {0} <output basename>".format(sys.argv[0])
    print "Arguments: "
    print "\n"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

cutfile=""

for opt, arg in options:
    if opt=='-h':
        print_usage()
        sys.exit(0)


if (len(remainder)!=1):
        print_usage()
        sys.exit()

n = 10000
bkg_lambda = 2
sig_lambda = 20


c = TCanvas("c","c",800,600);
c.Print(remainder[0]+".pdf[")
w = ROOT.RooWorkspace("w")

w.factory("Exponential::bkg(x[0,100],{0})".format(-1.0/bkg_lambda))
#w.factory("Gaussian::bkg(x[-50,50],0,3)")

w.factory("Exponential::signal(x,{0})".format(-1.0/sig_lambda))
#w.factory("EXPR::signal_step('x>0?1:0',x)")
#w.factory("Gaussian::signal_res(x,0,3)")
#w.factory("PROD::signal(signal_decay,signal_step)")
#w.factory("FCONV::signal(x,signal_truth,signal_res)")
w.factory("SUM::model(strength[0.001,0,0.005]*signal,bkg)")
w.defineSet("obs","x")
w.defineSet("poi","strength")

modelConfig = ModelConfig("test")
modelConfig.SetWorkspace(w)
modelConfig.SetPdf("model")
modelConfig.SetParametersOfInterest("strength")
modelConfig.SetObservables("x")

bkgModel = modelConfig.Clone()
bkgModel.SetName("bkg only")


pdf = w.pdf("model")


data= pdf.generate(w.set("obs"),n)

zcut = bkg_lambda*math.log(n/0.5)

w.factory("n[0,100]")
w.defineSet("n","n")

w.factory("b[0.5]")
w.factory("prod::yield(strength,{0})".format(n*math.exp(-zcut/sig_lambda)))
w.factory("sum::mean(b,yield)")
w.factory("Poisson::pois(n,mean)")
fcModel = ModelConfig("fcProblem",w)
fcModel.SetPdf(w.pdf("pois"))
fcModel.SetParametersOfInterest("strength")
fcModel.SetObservables(w.set("n"))

countData = RooDataSet("countData","countData",w.set("n"))
eventsPastZcut = data.sumEntries("x>{0}".format(zcut))
w.var("n").setVal(eventsPastZcut)
countData.add(w.set("n"))

countData.Print("v")
print "zcut {0} past zcut {1}".format(zcut,eventsPastZcut)

fc = FeldmanCousins(countData,fcModel)
fc.SetTestSize(0.05)
fc.UseAdaptiveSampling(True)
fc.FluctuateNumDataEntries(False)
fc.SetNBins(100)
#fcInterval = fc.GetInterval()
#print "F-C interval: [{0},{1}]".format(fcInterval.LowerLimit(w.var("strength")),fcInterval.UpperLimit(w.var("strength")))

print w.pdf("signal")
signalCdf = w.pdf("signal").createCdf(w.set("obs"))
w.var("x").setVal(zcut)
cdfAtZcut = signalCdf.getVal()
print cdfAtZcut
dataPastCut = data.reduce(w.set("obs"),"x>{0}".format(zcut))
dataArray=numpy.zeros(dataPastCut.numEntries()+2)
dataArray[0] = 0.0
for i in xrange(0,dataPastCut.numEntries()):
    thisX = dataPastCut.get(i).getRealValue("x")
    w.var("x").setVal(thisX)
    dataArray[i+1]=(signalCdf.getVal()-cdfAtZcut)/(1.0-cdfAtZcut)
dataArray[dataPastCut.numEntries()+1] = 1.0
dataArray.sort()
print dataArray
output = upperlimit.upperlim(0.9, 1, dataArray, 0., dataArray)
print output
print output[0]/(1.0-cdfAtZcut)


plc = ProfileLikelihoodCalculator(data,modelConfig)
plc.SetConfidenceLevel(0.95)
#plc.GetInterval()
likelihoodPlot = LikelihoodIntervalPlot(plc.GetInterval())
likelihoodPlot.SetNPoints(100)
likelihoodPlot.SetRange(0,0.005)
likelihoodPlot.Draw()
c.Print(remainder[0]+".pdf","Title:test")


frame=w.var("x").frame()
c.SetLogy()
data.plotOn(frame)
fitresult = pdf.fitTo(data)
pdf.plotOn(frame)
frame.SetMinimum(0.1)
frame.Draw()
c.Print(remainder[0]+".pdf","Title:test2")
#data = w.pdf("g").generate(w.set("

#fcalc = FrequentistCalculator(data,"signal","bkg")
c.Print(remainder[0]+".pdf]")
