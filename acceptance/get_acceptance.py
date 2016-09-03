#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <accpetance ROOT file>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=1.056
mass=0.030

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
c = TCanvas("c","c",1200,900);
gStyle.SetOptFit(1)
#outfile = TFile(remainder[0]+".root","RECREATE")
c.Print(remainder[0]+".pdf[")

infile = TFile(remainder[1])

exppol4=TF1("exppol4","exp(pol4(0))",-5,100)
#infile.cd()
#infile.ls()
#plot = gDirectory.Get("l1_p0")
p0= infile.Get("l1_p0").GetFunction("pol4").Eval(mass)
p1= infile.Get("l1_p1").GetFunction("pol4").Eval(mass)
p2= infile.Get("l1_p2").GetFunction("pol4").Eval(mass)
p3= infile.Get("l1_p3").GetFunction("pol4").Eval(mass)
p4= infile.Get("l1_p4").GetFunction("pol4").Eval(mass)
exppol4.SetParameters(p0,p1,p2,p3,p4)
exppol4.Draw()
c.Print(remainder[0]+".pdf","Title:test")
c.Print(remainder[0]+".pdf]")
sys.exit(0)

#masses = [0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
masses = [0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.035, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
massArr=array.array('d')
effTargetArr=array.array('d')
effL1p0Arr=array.array('d')
effL1p1Arr=array.array('d')
effL1p2Arr=array.array('d')
effL1p3Arr=array.array('d')
effL1p4Arr=array.array('d')
effP1p0Arr=array.array('d')
effP1p1Arr=array.array('d')
effP1p2Arr=array.array('d')
effP1p3Arr=array.array('d')
effP1p4Arr=array.array('d')
for filenum in range(0,len(remainder)-1):
    filename = remainder[filenum+1]
    massArr.append(masses[filenum])
    print masses[filenum]
    inFile = TFile(filename)
    inFile.cd()
    effAll = gDirectory.Get("eff_all")
    effAtTarget = effAll.GetFunction("exppol4").Eval(-5.0)
    effTargetArr.append(effAtTarget)

    effL1 = gDirectory.Get("eff_L1")
    effL1.Draw()
    func = effL1.GetFunction("exppol4")
    effL1p0Arr.append(func.GetParameter(0))
    effL1p1Arr.append(func.GetParameter(1))
    effL1p2Arr.append(func.GetParameter(2))
    effL1p3Arr.append(func.GetParameter(3))
    effL1p4Arr.append(func.GetParameter(4))
    c.Print(remainder[0]+".pdf","Title:test")

    effP1 = gDirectory.Get("eff_posL1")
    effP1.Draw()
    func = effP1.GetFunction("exppol4")
    effP1p0Arr.append(func.GetParameter(0))
    effP1p1Arr.append(func.GetParameter(1))
    effP1p2Arr.append(func.GetParameter(2))
    effP1p3Arr.append(func.GetParameter(3))
    effP1p4Arr.append(func.GetParameter(4))
    c.Print(remainder[0]+".pdf","Title:test")


outfile.cd()
graph=TGraph(len(massArr),massArr,effL1p0Arr)
graph.Draw("AL*")
graph.SetTitle("L1 p0")
graph.Fit("pol4")
graph.Write("l1_p0")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effL1p1Arr)
graph.Draw("AL*")
graph.SetTitle("L1 p1")
graph.Fit("pol4")
graph.Write("l1_p1")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effL1p2Arr)
graph.Draw("AL*")
graph.SetTitle("L1 p2")
graph.Fit("pol4")
graph.Write("l1_p2")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effL1p3Arr)
graph.Draw("AL*")
graph.SetTitle("L1 p3")
graph.Fit("pol4")
graph.Write("l1_p3")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effL1p4Arr)
graph.Draw("AL*")
graph.SetTitle("L1 p4")
graph.Fit("pol4")
graph.Write("l1_p4")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(massArr),massArr,effP1p0Arr)
graph.SetTitle("P1 p0")
graph.Draw("AL*")
graph.Fit("pol4")
graph.Write("p1_p0")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effP1p1Arr)
graph.SetTitle("P1 p1")
graph.Draw("AL*")
graph.Fit("pol4")
graph.Write("p1_p1")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effP1p2Arr)
graph.SetTitle("P1 p2")
graph.Draw("AL*")
graph.Fit("pol4")
graph.Write("p1_p2")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effP1p3Arr)
graph.SetTitle("P1 p3")
graph.Draw("AL*")
graph.Fit("pol4")
graph.Write("p1_p3")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,effP1p4Arr)
graph.SetTitle("P1 p4")
graph.Draw("AL*")
graph.Fit("pol4")
graph.Write("p1_p4")
c.Print(remainder[0]+".pdf","Title:test")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

