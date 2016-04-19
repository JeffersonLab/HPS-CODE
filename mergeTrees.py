#!/usr/bin/env python
import sys
import getopt
from ROOT import gROOT, TFile, TTree, TChain
print sys.argv[1]
#treeFile = TFile(sys.argv[1],"RECREATE")
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print sys.argv[2:]
chain = TChain("ntuple")
for i in sys.argv[2:]:
	chain.Add(i)
chain.Merge(sys.argv[1])
#print tree.ReadFile(sys.argv[2])
#tree.Write()

