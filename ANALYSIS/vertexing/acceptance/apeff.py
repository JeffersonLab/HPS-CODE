#!/usr/bin/env python
import sys
import array, math
from ROOT import gROOT, gStyle, TFile, TTree, TChain, TMVA, TCut, TCanvas, gDirectory, TH1, TGraph, gPad, TF1, TGraphErrors
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
gStyle.SetStatW(0.2)
gStyle.SetStatH(0.1)
outfile = TFile(remainder[0]+".root","RECREATE")
c.Print(remainder[0]+".pdf[")

#masses = [0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
#masses = [0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.035, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
masses = [0.022, 0.024, 0.026, 0.028, 0.030, 0.035, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090]
massArr=array.array('d')
zeroArr=array.array('d')
gammaArr=array.array('d')
mresL1p0Arr=array.array('d')
mresL1p1Arr=array.array('d')
mresL1p0Err=array.array('d')
mresL1p1Err=array.array('d')
effTargetArr=array.array('d')
effL1p0Arr=array.array('d')
effL1p1Arr=array.array('d')
effL1p2Arr=array.array('d')
effL1p3Arr=array.array('d')
effL1p4Arr=array.array('d')
effL1p0Err=array.array('d')
effL1p1Err=array.array('d')
effL1p2Err=array.array('d')
effL1p3Err=array.array('d')
effL1p4Err=array.array('d')
for filenum in range(0,len(remainder)-1):
    filename = remainder[filenum+1]
    massArr.append(masses[filenum])
    zeroArr.append(0)
    print masses[filenum]
    inFile = TFile(filename)

    prodz = inFile.Get("prodz")
    gammaArr.append((-1.0/prodz.GetFunction("expo").GetParameter(1))/(1.056/masses[filenum]))

    mres = inFile.Get("mres_all")
    mresL1p0Arr.append(mres.GetFunction("pol1").GetParameter(0))
    mresL1p1Arr.append(mres.GetFunction("pol1").GetParameter(1))
    mresL1p0Err.append(mres.GetFunction("pol1").GetParError(0))
    mresL1p1Err.append(mres.GetFunction("pol1").GetParError(1))

    effAll = inFile.Get("eff_all")
    effAtTarget = effAll.GetFunction("exppol4").Eval(-5.0)
    effTargetArr.append(effAtTarget)

    effAll.Draw()
    effAll.SetTitle("Efficiency vs. Z, m_A'={0}".format(masses[filenum]))
    func = effAll.GetFunction("exppol4")
    effL1p0Arr.append(func.GetParameter(0))
    effL1p1Arr.append(func.GetParameter(1))
    effL1p2Arr.append(func.GetParameter(2))
    effL1p3Arr.append(func.GetParameter(3))
    effL1p4Arr.append(func.GetParameter(4))
    effL1p0Err.append(func.GetParError(0))
    effL1p1Err.append(func.GetParError(1))
    effL1p2Err.append(func.GetParError(2))
    effL1p3Err.append(func.GetParError(3))
    effL1p4Err.append(func.GetParError(4))
    c.Print(remainder[0]+".pdf","Title:test")

outfile.cd()

graph=TGraph(len(massArr),massArr,gammaArr)
graph.Draw("A*")
graph.SetTitle("p(A')/E0")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.Fit("pol0")
graph.Write("gamma")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraphErrors(len(massArr),massArr,mresL1p0Arr,zeroArr,mresL1p0Err)
graph.Draw("A*")
graph.SetTitle("Mass resolution at z=0")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.GetYaxis().SetTitle("constant term [GeV]");
graph.Fit("pol1")
graph.Write("mres_l1_p0")
c.Print(remainder[0]+".pdf","Title:test")

molmassArr=array.array('d')
molmresArr=array.array('d')
molmassArr.append(0.03285)
molmresArr.append(0.002168)
molgraph=TGraph(len(molmassArr),molmassArr,molmresArr)
molgraph.SetMarkerColor(4)
molgraph.Draw("*")
c.Update()
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraphErrors(len(massArr),massArr,mresL1p1Arr,zeroArr,mresL1p1Err)
graph.Draw("A*")
graph.SetTitle("Slope of mass resolution vs. Z")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.GetYaxis().SetTitle("linear term [GeV/mm]");
graph.Fit("pol1")
graph.Write("mres_l1_p1")
c.Print(remainder[0]+".pdf","Title:test")

graph=TGraphErrors(len(massArr),massArr,effL1p0Arr,zeroArr,effL1p0Err)
graph.Draw("A*")
graph.SetTitle("Efficiency fit, p0")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.GetYaxis().SetTitle("constant term");
graph.Fit("pol1")
graph.Write("l1_p0")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraphErrors(len(massArr),massArr,effL1p1Arr,zeroArr,effL1p1Err)
graph.Draw("A*")
graph.SetTitle("Efficiency fit, p1")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.GetYaxis().SetTitle("linear term [mm^-1]");
graph.Fit("pol1")
graph.Write("l1_p1")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraphErrors(len(massArr),massArr,effL1p2Arr,zeroArr,effL1p2Err)
graph.Draw("A*")
graph.SetTitle("Efficiency fit, p2")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.GetYaxis().SetTitle("quadratic term [mm^-2]");
graph.Fit("pol3")
graph.Write("l1_p2")
c.Print(remainder[0]+".pdf","Title:test")
graph=TGraphErrors(len(massArr),massArr,effL1p3Arr,zeroArr,effL1p3Err)
graph.Draw("A*")
graph.SetTitle("Efficiency fit, p3")
graph.GetXaxis().SetTitle("A' mass [GeV]");
graph.GetYaxis().SetTitle("cubic term [mm^-3]");
graph.Fit("pol3")
graph.Write("l1_p3")
c.Print(remainder[0]+".pdf","Title:test")

c.Print(remainder[0]+".pdf]")
outfile.Write()
outfile.Close()

