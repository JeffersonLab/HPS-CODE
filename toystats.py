#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D#, RooWorkspace, RooDataSet
from ROOT.RooStats import ModelConfig, ProfileLikelihoodCalculator, LikelihoodIntervalPlot, FrequentistCalculator

c = TCanvas("c","c",800,600);
w = ROOT.RooWorkspace("w")

w.factory("Exponential::bkg(x[0,100],-0.5)")
#w.factory("Gaussian::bkg(x[-50,50],0,3)")

w.factory("Exponential::signal(x,-0.05)")
#w.factory("EXPR::signal_step('x>0?1:0',x)")
#w.factory("Gaussian::signal_res(x,0,3)")
#w.factory("PROD::signal(signal_decay,signal_step)")
#w.factory("FCONV::signal(x,signal_truth,signal_res)")
w.factory("SUM::model(strength[0.001,0,1]*signal,bkg)")
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

data= pdf.generateBinned(w.set("obs"),10000)

plc = ProfileLikelihoodCalculator(data,modelConfig)
plc.SetConfidenceLevel(0.95)
#plc.GetInterval()
likelihoodPlot = LikelihoodIntervalPlot(plc.GetInterval())
likelihoodPlot.SetNPoints(100)
likelihoodPlot.SetRange(0,0.005)
likelihoodPlot.Draw()
c.SaveAs("test2.png")


frame=w.var("x").frame()
c.SetLogy()
data.plotOn(frame)
fitresult = pdf.fitTo(data)
pdf.plotOn(frame)
frame.SetMinimum(0.1)
frame.Draw()
c.SaveAs("test.png")
#data = w.pdf("g").generate(w.set("

fcalc = FrequentistCalculator(data,"signal","bkg")
