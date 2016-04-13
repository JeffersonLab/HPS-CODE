#!/usr/bin/env python
import sys, array,math
import getopt
import tempfile
import os
from ROOT import gROOT, TCanvas, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D,TTree
print sys.argv[1]
treeFile = TFile(sys.argv[1],"RECREATE")
tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print sys.argv[2:]

inputfile = tempfile.NamedTemporaryFile(delete=False)
print inputfile.name
firstfile = True
for filename in sys.argv[2:]:
    f = open(filename)
    firstline = True
    for i in f:
        if firstline:
            if firstfile:
                branchdescriptor = i
                inputfile.write(i)
            else:
                if branchdescriptor != i:
                    print "branch descriptor doesn't match"
                    sys.exit(-1)
        else:
            inputfile.write(i)
        firstline = False
    f.close()
    firstfile = False
inputfile.close()
print tree.ReadFile(inputfile.name)
os.remove(inputfile.name)
tree.Write()

