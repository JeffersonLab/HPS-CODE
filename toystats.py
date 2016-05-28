#!/usr/bin/env python
import sys, array,math
import getopt
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D#, RooWorkspace, RooDataSet

c = TCanvas("c","c",800,600);
w = ROOT.RooWorkspace("w")

w.factory("Gaussian::bkg(x[-50,50],0,3)")

w.factory("Exponential::signal_decay(x,-0.2)")
w.factory("EXPR::signal_step('x>0?1:0',x)")
w.factory("Gaussian::signal_res(x,0,3)")
w.factory("PROD::signal(signal_decay,signal_step)")
#w.factory("FCONV::signal(x,signal_truth,signal_res)")
w.factory("SUM::model(strength[0.1,0,1]*signal,bkg)")
w.defineSet("obs","x")
w.defineSet("poi","strength")

pdf = w.pdf("model")

data= pdf.generate(w.set("obs"),1000)
frame=w.var("x").frame()
c.SetLogy()
data.plotOn(frame)
fitresult = pdf.fitTo(data)
pdf.plotOn(frame)
frame.Draw()
c.SaveAs("test.png")
#data = w.pdf("g").generate(w.set("
