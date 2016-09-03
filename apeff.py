#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1
import getopt


def print_usage():
    print "\nUsage: {0} <output file basename> <recon A' ROOT file> <slic A' ROOT file".format(sys.argv[0])
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

if len(remainder)<3:
    print_usage()
    sys.exit(0)

gROOT.SetBatch(True)
c = TCanvas("c","c",1200,900);
gStyle.SetOptFit(1)
outfile = TFile(remainder[0]+".root","RECREATE")
c.Print(remainder[0]+".pdf[")

#masses = [0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
masses = [0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.035, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
massArr=array.array('d')
gammaArr=array.array('d')
mresL1p0Arr=array.array('d')
mresL1p1Arr=array.array('d')
mresP1p0Arr=array.array('d')
mresP1p1Arr=array.array('d')
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

    prodz = inFile.Get("prodz")
    gammaArr.append((-1.0/prodz.GetFunction("expo").GetParameter(1))/(1.056/masses[filenum]))

    mres = inFile.Get("mres_L1")
    mresL1p0Arr.append(mres.GetFunction("pol1").GetParameter(0))
    mresL1p1Arr.append(mres.GetFunction("pol1").GetParameter(1))

    #mres = inFile.Get("mres_posL1")
    #mresP1p0Arr.append(mres.GetFunction("pol1").GetParameter(0))
    #mresP1p1Arr.append(mres.GetFunction("pol1").GetParameter(1))

    effAll = inFile.Get("eff_all")
    effAtTarget = effAll.GetFunction("exppol4").Eval(-5.0)
    effTargetArr.append(effAtTarget)

    effL1 = inFile.Get("eff_L1")
    effL1.Draw()
    func = effL1.GetFunction("exppol4")
    effL1p0Arr.append(func.GetParameter(0))
    effL1p1Arr.append(func.GetParameter(1))
    effL1p2Arr.append(func.GetParameter(2))
    effL1p3Arr.append(func.GetParameter(3))
    effL1p4Arr.append(func.GetParameter(4))
    c.Print(remainder[0]+".pdf","Title:test")

    #effP1 = inFile.Get("eff_posL1")
    #effP1.Draw()
    #func = effP1.GetFunction("exppol4")
    #effP1p0Arr.append(func.GetParameter(0))
    #effP1p1Arr.append(func.GetParameter(1))
    #effP1p2Arr.append(func.GetParameter(2))
    #effP1p3Arr.append(func.GetParameter(3))
    #effP1p4Arr.append(func.GetParameter(4))
    #c.Print(remainder[0]+".pdf","Title:test")


outfile.cd()

graph=TGraph(len(massArr),massArr,gammaArr)
graph.Draw("AL*")
graph.SetTitle("gamma")
graph.Fit("pol0")
graph.Write("gamma")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraph(len(massArr),massArr,mresL1p0Arr)
graph.Draw("AL*")
graph.SetTitle("mres L1 p0")
graph.Fit("pol1")
graph.Write("mres_l1_p0")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraph(len(massArr),massArr,mresL1p1Arr)
graph.Draw("AL*")
graph.SetTitle("mres L1 p1")
graph.Fit("pol1")
graph.Write("mres_l1_p1")
c.Print(remainder[0]+".pdf","Title:test")
#graph=TGraph(len(massArr),massArr,mresP1p0Arr)
#graph.Draw("AL*")
#graph.SetTitle("mres P1 p0")
#graph.Fit("pol1")
#graph.Write("mres_p1_p0")
#c.Print(remainder[0]+".pdf","Title:test")
#graph=TGraph(len(massArr),massArr,mresP1p1Arr)
#graph.Draw("AL*")
#graph.SetTitle("mres P1 p1")
#graph.Fit("pol1")
#graph.Write("mres_p1_p1")
#c.Print(remainder[0]+".pdf","Title:test")

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

#graph=TGraph(len(massArr),massArr,effP1p0Arr)
#graph.SetTitle("P1 p0")
#graph.Draw("AL*")
#graph.Fit("pol4")
#graph.Write("p1_p0")
#c.Print(remainder[0]+".pdf","Title:test")
#graph=TGraph(len(massArr),massArr,effP1p1Arr)
#graph.SetTitle("P1 p1")
#graph.Draw("AL*")
#graph.Fit("pol4")
#graph.Write("p1_p1")
#c.Print(remainder[0]+".pdf","Title:test")
#graph=TGraph(len(massArr),massArr,effP1p2Arr)
#graph.SetTitle("P1 p2")
#graph.Draw("AL*")
#graph.Fit("pol4")
#graph.Write("p1_p2")
#c.Print(remainder[0]+".pdf","Title:test")
#graph=TGraph(len(massArr),massArr,effP1p3Arr)
#graph.SetTitle("P1 p3")
#graph.Draw("AL*")
#graph.Fit("pol4")
#graph.Write("p1_p3")
#c.Print(remainder[0]+".pdf","Title:test")
#graph=TGraph(len(massArr),massArr,effP1p4Arr)
#graph.SetTitle("P1 p4")
#graph.Draw("AL*")
#graph.Fit("pol4")
#graph.Write("p1_p4")
#c.Print(remainder[0]+".pdf","Title:test")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

