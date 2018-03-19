#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <recon A' ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=2.3
mass=0.030

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)<2:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
c = TCanvas("c","c",1200,900);
gStyle.SetOptFit(1)
gStyle.SetStatW(0.2)
gStyle.SetStatH(0.1)
outfile = TFile(remainder[0]+".root","RECREATE")
c.Print(remainder[0]+".pdf[")

masses = [0.042,0.048,0.054,0.060,0.066,0.072,0.078,0.084]
massArr=array.array('d')
zeroArr=array.array('d')
gammaArr=array.array('d')
mresL1p0Arr=array.array('d')
mresL1p1Arr=array.array('d')
mresL1p0Err=array.array('d')
mresL1p1Err=array.array('d')
mmean=array.array('d')
mresArr=array.array('d')
mmeanErr=array.array('d')
mresArrErr=array.array('d')

for filenum in range(0,len(remainder)-1):
    filename = remainder[filenum+1]
    massArr.append(masses[filenum])
    zeroArr.append(0)
    print masses[filenum]
    inFile = TFile(filename)
    mres = inFile.Get("mres_all")
    mresL1p0Arr.append(mres.GetFunction("pol1").GetParameter(0))
    mresL1p1Arr.append(mres.GetFunction("pol1").GetParameter(1))
    mresL1p0Err.append(mres.GetFunction("pol1").GetParError(0))
    mresL1p1Err.append(mres.GetFunction("pol1").GetParError(1))
    inFile.Get("hnew3").Draw()
    c.Print(remainder[0]+".pdf","Title:test")
    mmean.append(inFile.Get("hnew3").GetFunction("gaus").GetParameter(1))
    mresArr.append(inFile.Get("hnew3").GetFunction("gaus").GetParameter(2))
    mmeanErr.append(inFile.Get("hnew3").GetFunction("gaus").GetParError(1))
    mresArrErr.append(inFile.Get("hnew3").GetFunction("gaus").GetParError(2))

outfile.cd()

graph=TGraphErrors(len(massArr),massArr,mresL1p0Arr,zeroArr,mresL1p0Err)
graph.Draw("A*")
graph.SetTitle("Mass resolution at z=0")
graph.GetXaxis().SetTitle("A' mass [GeV]")
graph.GetYaxis().SetTitle("constant term [GeV]")
graph.Fit("pol1")
graph.Write("mres_l1_p0")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraphErrors(len(massArr),massArr,mresL1p1Arr,zeroArr,mresL1p1Err)
graph.Draw("A*")
graph.SetTitle("Slope of mass resolution vs. Z")
graph.GetXaxis().SetTitle("A' mass [GeV]")
graph.GetYaxis().SetTitle("linear term [GeV/mm]")
graph.Fit("pol1")
graph.Write("mres_l1_p1")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraphErrors(len(massArr),massArr,mmean,zeroArr,mmeanErr)
graph.Draw("A*")
graph.SetTitle("Mean Mass")
graph.GetXaxis().SetTitle("Vector mass [GeV]")
graph.Fit("pol1")
graph.Write("mmean")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraphErrors(len(massArr),massArr,mresArr,zeroArr,mresArrErr)
graph.Draw("A*")
graph.SetTitle("Mass Resolution")
graph.GetXaxis().SetTitle("Vector mass [GeV]")
graph.Fit("pol1")
graph.Write("mres")
c.Print(remainder[0]+".pdf","Title:test")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

