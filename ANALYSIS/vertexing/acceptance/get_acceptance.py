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
mass=0.050

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
p0= infile.Get("l1_p0").GetFunction("pol1").Eval(mass)
p1= infile.Get("l1_p1").GetFunction("pol1").Eval(mass)
p2= infile.Get("l1_p2").GetFunction("pol3").Eval(mass)
p3= infile.Get("l1_p3").GetFunction("pol3").Eval(mass)
#p4= infile.Get("l1_p4").GetFunction("pol4").Eval(mass)
p4= 0
exppol4.SetParameters(p0,p1,p2,p3,p4)
exppol4.Draw()
exppol4.SetTitle("Efficiency for 50 MeV heavy photon")
exppol4.GetXaxis().SetTitle("decay z [mm]")
exppol4.GetYaxis().SetTitle("eff(z)/eff(target)")
c.Print(remainder[0]+".pdf","Title:test")

targetz = -5
gammact = 30

exppol4.SetParameters(targetz/gammact-math.log(gammact),0-1.0/gammact,0,0,0)
exppol4.Draw()
exppol4.SetTitle("Decay distribution, 50 MeV heavy photon, gammact=30 mm")
exppol4.GetXaxis().SetTitle("decay z [mm]")
exppol4.GetYaxis().SetTitle("dN/dz")
c.Print(remainder[0]+".pdf","Title:test")

exppol4.SetParameters(p0+targetz/gammact-math.log(gammact),p1-1.0/gammact,p2,p3,p4)
exppol4.Draw()
exppol4.SetTitle("Decay distribution, 50 MeV heavy photon, gammact=30 mm")
exppol4.GetXaxis().SetTitle("decay z [mm]")
exppol4.GetYaxis().SetTitle("dN/dz")
c.Print(remainder[0]+".pdf","Title:test")

c.Print(remainder[0]+".pdf]")
sys.exit(0)

