#!/usr/bin/env python
import sys,os,array
import getopt
from ROOT import TFile, TTree, TChain
print "good events: "+sys.argv[1]
print "bad events: "+sys.argv[2]
chain = TChain("ntuple")
for i in sys.argv[3:]:
	chain.Add(i)

goodOutFile = TFile(sys.argv[1],"RECREATE")
goodEvents = chain.CopyTree("abs(uncVZ)*uncM<0.1")
goodOutFile.Write()
goodOutFile.Close()
badOutFile = TFile(sys.argv[2],"RECREATE")
badEvents = chain.CopyTree("uncVZ*uncM>0.5")
badOutFile.Write()
badOutFile.Close()
