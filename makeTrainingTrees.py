#!/usr/bin/env python
import sys,os,array
import getopt
from ROOT import TFile, TTree, TChain

print "good events: "+sys.argv[1]
print "bad events: "+sys.argv[2]
chain = TChain("ntuple")
for i in sys.argv[3:]:
	chain.Add(i)

#maincut = "uncP>0.8*1.056&&bscChisq<5&&minIso>0.5&&max(eleTrkChisq,posTrkChisq)<20"
maincut = "1"

goodOutFile = TFile(sys.argv[1],"RECREATE")
goodEvents = chain.CopyTree(maincut+"&&abs(uncVZ)*uncM<0.1")
goodOutFile.Write()
goodOutFile.Close()
badOutFile = TFile(sys.argv[2],"RECREATE")
badEvents = chain.CopyTree(maincut+"&&uncVZ*uncM>0.5")
badOutFile.Write()
badOutFile.Close()
