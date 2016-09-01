#!/usr/bin/env python
import sys,os,array,math
import getopt
from ROOT import TFile, TTree, TChain


def print_usage():
    print "\nUsage: {0} <output ROOT file, good events> <output ROOT file, bad events> <input ROOT file(s)>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-t: cut type (bumphunt, vertexing) - bumphunt is default'
    print '\t-h: this help message'
    print

ebeam=1.056

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:h')

cutType = "bumphunt"
cutOutput = False

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-t':
            cutType=arg
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)<3:
    print_usage()
    sys.exit(0)
print "good: "+remainder[0]
print "bad: "+remainder[1]

if cutType=="bumphunt":
    baseCut="isPair1&&max(eleMatchChisq,posMatchChisq)<30&&eleClY*posClY<0&&tarP>0.8*{0}".format(ebeam)
    goodCut=baseCut+"&&abs(eleClT-posClT)<1"
    badCut=baseCut+"&&abs(eleClT-posClT)>3"
elif cutType=="moller":
    molmass=math.sqrt(2.0*5.11e-4*ebeam)
    basecut="max(topP,botP)<0.85*{0}".format(ebeam)
    goodCut="abs(vzcM*{0}/vzcP - {1})<0.003".format(ebeam,molmass)
    badCut="abs(vzcM*{0}/vzcP - {1})>0.005".format(ebeam,molmass)
elif cutType=="vertexing":
    baseCut="uncP>0.8*{0}".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&uncVZ*uncM>0.5"
elif cutType=="vertexing_L1":
    baseCut="isPair1&&max(eleMatchChisq,posMatchChisq)<30&&eleClY*posClY<0&&uncP>0.8*{0}&&uncVZ<80&&eleHasL1&&posHasL1".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&(uncVZ+5)*uncM>0.5"
elif cutType=="vertexing_L1_08":
    baseCut="isPair1&&max(eleMatchChisq,posMatchChisq)<30&&eleClY*posClY<0&&uncP>0.8*{0}&&uncVZ<80&&eleHasL1&&posHasL1".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&(uncVZ+5)*uncM>0.8"
elif cutType=="vertexing_L1_10":
    baseCut="isPair1&&max(eleMatchChisq,posMatchChisq)<30&&eleClY*posClY<0&&uncP>0.8*{0}&&uncVZ<80&&eleHasL1&&posHasL1".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&(uncVZ+5)*uncM>1.0"
elif cutType=="vertexing_noL1":
    baseCut="uncP>0.8*{0}&&uncVZ<80&&!eleHasL1&&!posHasL1".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&(uncVZ+5)*uncM>0.5"
elif cutType=="vertexing_eleL1":
    baseCut="uncP>0.8*{0}&&uncVZ<80&&eleHasL1&&!posHasL1".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&(uncVZ+5)*uncM>0.5"
elif cutType=="vertexing_posL1":
    baseCut="uncP>0.8*{0}&&uncVZ<80&&!eleHasL1&&posHasL1".format(ebeam)
    goodCut=baseCut+"&&abs(uncVZ)*uncM<0.1"
    badCut=baseCut+"&&(uncVZ+5)*uncM>0.5"
else:
    print "invalid cut type"
    sys.exit(-1)



chain = TChain("ntuple")
for i in remainder[2:]:
	chain.Add(i)

#maincut = "uncP>0.8*1.056&&bscChisq<5&&minIso>0.5&&max(eleTrkChisq,posTrkChisq)<20"

goodOutFile = TFile(remainder[0],"RECREATE")
goodEvents = chain.CopyTree(goodCut)
goodOutFile.Write()
goodOutFile.Close()
badOutFile = TFile(remainder[1],"RECREATE")
badEvents = chain.CopyTree(badCut)
badOutFile.Write()
badOutFile.Close()
