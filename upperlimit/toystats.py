#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, RooDataSet, TFeldmanCousins
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot, FrequentistCalculator, FeldmanCousins, AsymptoticCalculator
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
signal_strength = 0.001
CL = 0.9


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
w.factory("SUM::model(strength[{0},0,0.005]*signal,bkg)".format(signal_strength))
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

plc = ProfileLikelihoodCalculator(data,modelConfig)

nullParams = w.set("poi").snapshot()
nullParams.setRealValue("strength",0)
plc.SetNullParameters(nullParams)

hypo = plc.GetHypoTest()
#hypo.SetPValueIsRightTail(True)
print "PLR p-value {0}, significance {1}".format(hypo.NullPValue(),hypo.Significance())


plc.SetConfidenceLevel(CL)
interval = plc.GetInterval()
interval.Print()
print "likelihood interval: [{0}, {1}]".format(interval.LowerLimit(w.var("strength")), interval.UpperLimit(w.var("strength")))
#likelihoodPlot = LikelihoodIntervalPlot(interval)
#likelihoodPlot.SetNPoints(100)
#likelihoodPlot.SetRange(0,0.005)
#likelihoodPlot.Draw()
#c.Print(remainder[0]+".pdf","Title:test")

zcutArr=array.array('d')
limitArr=array.array('d')
fractionArr=array.array('d')
countArr=array.array('d')
expectArr=array.array('d')
fcLowerArr=array.array('d')
fcUpperArr=array.array('d')

fc = TFeldmanCousins()
fc.SetCL(CL)
signalCdf = w.pdf("signal").createCdf(w.set("obs"))
for i in xrange(0,120):
    #zcut_count = 0.1+0.1*i
    #zcut = bkg_lambda*math.log(n/zcut_count)

    zcut = 11+0.5*i
    zcut_count = n/math.exp(zcut/bkg_lambda)
    eventsPastZcut = data.sumEntries("x>{0}".format(zcut))
    fcLower = fc.CalculateLowerLimit(eventsPastZcut,zcut_count)
    fcUpper = fc.CalculateUpperLimit(eventsPastZcut,zcut_count)

    #print "zcut {0} for {1} past zcut, got {2} past zcut, FC limits [{3} {4}]".format(zcut,zcut_count,eventsPastZcut,fcLower,fcUpper)

    #w.factory("n[0,100]")
    #w.defineSet("n","n")

    #w.factory("b[{0}]".format(zcut_count))
    #w.factory("prod::yield(strength,{0})".format(n*math.exp(-zcut/sig_lambda)))
    #w.factory("sum::mean(b,yield)")
    #w.factory("Poisson::pois(n,mean)")
    #w.var("n").setVal(eventsPastZcut)
    #countData = RooDataSet("countData","countData",w.set("n"))
    #countData.add(w.set("n"))

    #countData.Print("v")

    #fcModel = ModelConfig("fcProblem",w)
    #fcModel.SetPdf(w.pdf("pois"))
    #fcModel.SetParametersOfInterest("strength")
    #fcModel.SetObservables(w.set("n"))
    #fc = FeldmanCousins(countData,fcModel)
    #fc.SetTestSize(0.05)
    #fc.UseAdaptiveSampling(True)
    #fc.FluctuateNumDataEntries(False)
    #fc.SetNBins(100)
    #fcInterval = fc.GetInterval()
    #print "F-C interval: [{0},{1}]".format(fcInterval.LowerLimit(w.var("strength")),fcInterval.UpperLimit(w.var("strength")))

    w.var("x").setVal(zcut)
    cdfAtZcut = signalCdf.getVal()
    dataPastCut = data.reduce(w.set("obs"),"x>{0}".format(zcut))
    dataArray=numpy.zeros(dataPastCut.numEntries()+2)
    dataArray[0] = 0.0
    for i in xrange(0,dataPastCut.numEntries()):
        thisX = dataPastCut.get(i).getRealValue("x")
        w.var("x").setVal(thisX)
        dataArray[i+1]=(signalCdf.getVal()-cdfAtZcut)
    dataArray[dataPastCut.numEntries()+1] = 1.0-cdfAtZcut
    dataArray/= (1.0-cdfAtZcut)
    dataArray.sort()
    #print dataArray
    output = upperlimit.upperlim(CL, 1, dataArray, 0., dataArray)
    limit = output[0]/(1.0-cdfAtZcut)/n

    #if output[1]==0:
    zcutArr.append(zcut)
    countArr.append(eventsPastZcut)
    expectArr.append(zcut_count)
    limitArr.append(limit)
    fractionArr.append(1.0-cdfAtZcut)
    fcLowerArr.append(fcLower/(1.0-cdfAtZcut)/n)
    fcUpperArr.append(fcUpper/(1.0-cdfAtZcut)/n)
    #print output
    #print "zcut = {0}, expect {1} past zcut, got {2} past zcut, signal fraction past zcut = {3}, limit = {4}".format(zcut,zcut_count,eventsPastZcut,1.0-cdfAtZcut,limit)

graph=TGraph(len(zcutArr),zcutArr,fcUpperArr)
graph.SetTitle("Feldman-Cousins upper limit")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,fcLowerArr)
graph.SetTitle("Feldman-Cousins lower limit")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,limitArr)
graph.SetTitle("Optimum interval limit")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,countArr)
graph.SetTitle("Events past zcut")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(zcutArr),zcutArr,fractionArr)
graph.SetTitle("Signal efficiency")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")

c.SetLogy(1)
graph=TGraph(len(zcutArr),zcutArr,expectArr)
graph.SetTitle("Expected events past zcut")
graph.Draw("AL*")
c.Print(remainder[0]+".pdf","Title:test")
c.SetLogy(0)


frame=w.var("x").frame()
c.SetLogy()
data.plotOn(frame)
#fitresult = pdf.fitTo(data)
pdf.plotOn(frame)
frame.SetMinimum(0.1)
frame.Draw()
c.Print(remainder[0]+".pdf","Title:test2")
#data = w.pdf("g").generate(w.set("

#fcalc = FrequentistCalculator(data,"signal","bkg")
c.Print(remainder[0]+".pdf]")
