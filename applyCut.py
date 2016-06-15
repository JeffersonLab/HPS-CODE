#!/usr/bin/env python
import sys
import getopt
#from ROOT import gROOT, TFile, TTree, TChain, TTreeFormula
import root_numpy, numpy

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    #print '\t-c: rank by tarChisq (lowest best)'
    print '\t-p: rank by uncP (highest best)'
    print '\t-h: this help message'
    print

ebeam=1.056
sortkey="tarChisq"
highestBest=False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'pe:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-p':
            sortkey="uncP"
            highestBest = False
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)
print remainder[0]
print remainder[1]

events = root_numpy.root2array(remainder[1],branches=["event",
    "uncP",
    "tarChisq",
    "isPair1",
    "eleMatchChisq",
    "posMatchChisq",
    "eleClY",
    "posClY",
    "eleClT",
    "posClT",
    "nPos"])

n = events.size

#cut = numpy.row_stack((events["isPair1"]==1,
#    events["eleMatchChisq"]<3,
#    events["posMatchChisq"]<3,
#    abs(events["eleClT"]-events["posClT"])<1.6,
#    events["eleClY"]*events["posClY"]<0,
#    events["nPos"]==1)).all(0)

#cut = events["uncP"]>0.8*ebeam

cut = numpy.ones(n)
output = numpy.core.records.fromarrays( [cut, numpy.zeros(n), numpy.zeros(n)], dtype=[("cut",numpy.int8),("nPass",numpy.int8),("rank",numpy.int8)])

currentevent = 0
candidates = []

for i in xrange(0,n):
    if events[i]["event"]!=currentevent:
        ranked_candidates = sorted(candidates, key=lambda x:events[x][sortkey],reverse=highestBest)
        rank=1
        for j in ranked_candidates:
            output[j]["nPass"]=len(ranked_candidates)
            output[j]["rank"]=rank
            rank+=1
        del candidates[:]
        currentevent = events[i]["event"]
    if output[i]["cut"]!=0:
        candidates.append(i)

root_numpy.array2root(output,remainder[0],mode="recreate",treename="cut")
#newtree=root_numpy.array2tree(output)
#newtree.Scan()
