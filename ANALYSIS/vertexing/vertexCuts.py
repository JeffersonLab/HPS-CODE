#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from ROOT import gROOT, TFile, TTree, TChain, gDirectory
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file names>".format(sys.argv[0])
    print "Arguments: "

    print '\t-v: apply default vertexing cuts'
    print '\t-w: apply default L1L1 vertexing cuts'
    print '\t-x: apply default L1L2 vertexing cuts'
    print '\t-y: apply default L2L2vertexing cuts'
    print '\t-e: use this beam energy (default 1.056)'
    print '\t-c: use this cluster-track deltaT (default 43.0)'
    print '\t-z: use this target Z (default -5.0)'
    print '\t-h: this help message'
    print

ebeam=1.056
clusterT = 43.0
targetZ = 0.5

vertCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<20&&bscChisq-uncChisq<10&&max(eleTrkChisq,posTrkChisq)<30&&abs(eleP-posP)/(eleP+posP)<0.5&&posTrkD0+{2}*posPX/posP<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>0.8&&eleHasL2&&posHasL2"

trkExtrpCutL1L2 = "uncP>-9999"

trkExtrpCutL2L2 = "uncP>-9999"

vertCutL1L1 = "eleHasL1&&posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0" + "&&" + vertCut

vertCutL1L2 = "((!eleHasL1&&posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0)||(eleHasL1&&!posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0))" + "&&" + vertCut + "&&" + trkExtrpCutL1L2

vertCutL2L2 = "!eleHasL1&&!posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0" + "&&" + vertCut + "&&" + trkExtrpCutL2L2

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'vwxye:c:z:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-v':
            cut=vertCut
        if opt=='-w':
            cut=vertCutL1L1
        if opt=='-x':
            cut=vertCutL1L2
        if opt=='-y':
            cut=vertCutL2L2
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-c':
            clusterT=float(arg)
        if opt=='-z':
            targetZ=float(arg)
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
events = chain.CopyTree(cut.format(ebeam,clusterT,targetZ))
print events.GetEntries()
#outFile = TFile(remainder[0],"RECREATE")
#events.Write()
events.Write("ntuple",TTree.kOverwrite)
gDirectory.ls()