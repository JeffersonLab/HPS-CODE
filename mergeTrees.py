#!/usr/bin/env python
import sys
import getopt
from ROOT import gROOT, TFile, TTree, TChain, gDirectory

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file names>".format(sys.argv[0])
    print "Arguments: "
    print '\t-t: apply default trident cuts'
    print '\t-o: apply Omar\'s trident cuts'
    print '\t-v: apply default vertexing cuts'
    print '\t-m: apply default Moller cuts'
    print '\t-e: use this beam energy'
    print '\t-h: this help message'
    print

ebeam=1.056
triCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<4&&abs(eleClT-posClT)<1.6&&eleClY*posClY<0&&max(eleTrkChisq,posTrkChisq)<25&&uncChisq<10&&eleP<{0}*0.8"
omarTriCut = "isPair1&&nPos==1&&max(eleMatchChisq,posMatchChisq)<3&&abs(eleClT-posClT)<1.6&&eleClY*posClY<0"
vertCut = "eleP<{0}*0.85&&posP<{0}*0.85&&elePY*posPY<0&&eleP>{0}*0.05&&posP>{0}*0.05&&uncP<{0}*1.25&&abs(eleClT-posClT)<2&&(eleHasL1&&posHasL1)&&(eleHasL2&&posHasL2)&&max(eleMatchChisq,posMatchChisq)<10&&max(eleTrkChisq,posTrkChisq)<100"
mollerCut = "topP<{0}*0.85&&botP<{0}*0.85&&uncP>{0}*0.85&&uncP<{0}*1.1&&abs(topTrkT-botTrkT)<5&&abs(uncPX)<{0}*0.02&&abs(uncPY)<{0}*0.01&&vzcChisq<20"
cut=""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tovme:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-t':
            cut=triCut
        if opt=='-o':
            cut=omarTriCut
        if opt=='-v':
            cut=vertCut
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
	chain.Add(i,0)
print chain.GetEntries()
outFile = TFile(remainder[0],"RECREATE")
events = chain.CopyTree(cut.format(ebeam))
print events.GetEntries()
#outFile = TFile(remainder[0],"RECREATE")
#events.Write()
events.Write("ntuple",TTree.kOverwrite)
gDirectory.ls()
