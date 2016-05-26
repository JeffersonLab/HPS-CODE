#!/usr/bin/env python
import sys
import getopt
from ROOT import gROOT, TFile, TTree, TChain

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file names>".format(sys.argv[0])
    print "Arguments: "
    print '\t-t: apply default trident cuts'
    print '\t-m: apply default Moller cuts'
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=1.056
triCut = "eleP<{0}*0.85&&posP<{0}*0.85&&elePY*posPY<0&&eleP>{0}*0.05&&posP>{0}*0.05&&uncP<{0}*1.25&&abs(eleClT-posClT)<2&&(eleHasL1&&posHasL1)&&(eleHasL2&&posHasL2)&&max(eleMatchChisq,posMatchChisq)<10&&max(eleTrkChisq,posTrkChisq)<100"
mollerCut = "topP<{0}*0.85&&botP<{0}*0.85&&uncP>{0}*0.85&&uncP<{0}*1.1&&abs(topTrkT-botTrkT)<5&&abs(uncPX)<{0}*0.02&&abs(uncPY)<{0}*0.01&&(topHasL1&&botHasL1)&&(topHasL2&&botHasL2)&&vzcChisq<3"
cut=""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tme:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-t':
            cut=triCut
        if opt=='-m':
            cut=mollerCut
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

print remainder[0]
#treeFile = TFile(sys.argv[1],"RECREATE")
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print remainder[1:]
chain = TChain("ntuple")
for i in remainder[1:]:
	chain.Add(i)
#chain.Merge(sys.argv[1])
outFile = TFile(remainder[0],"RECREATE")

events = chain.CopyTree(cut.format(ebeam))
events.Write()
#print tree.ReadFile(sys.argv[2])
#tree.Write()

