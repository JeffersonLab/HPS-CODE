#!/usr/bin/env python
import sys
import getopt
#from ROOT import gROOT, TFile, TTree, TChain, TTreeFormula
import root_numpy, numpy

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-e: use this beam energy'
    print '\t-t: cut type (bumphunt, vertexing) - bumphunt is default'
    print '\t-c: only write events that pass cuts'
    print '\t-h: this help message'
    print

ebeam=1.056
#sortkey="tarChisq"
#highestBest=False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:ch')


cutType = "bumphunt"
cutOutput = False

# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-t':
            cutType=arg
        if opt=='-c':
            cutOutput = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)
print remainder[0]
print remainder[1]

if cutType=="bumphunt":
    events = root_numpy.root2array(remainder[1],branches=["event",
        "uncP",
        "uncM",
        "uncVZ",
        "tarChisq",
        "isPair1",
        "eleMatchChisq",
        "posMatchChisq",
        "eleClY",
        "posClY",
        "eleClT",
        "posClT",
        "nPos"])
elif cutType=="vertexing":
    events = root_numpy.root2array(remainder[1],branches=["event",
        "uncP",
        "uncM",
        "uncVZ",
        "bscChisq",
        "isPair1",
        "eleP",
        "posP",
        "eleMatchChisq",
        "posMatchChisq",
        "eleClY",
        "posClY",
        "eleClT",
        "posClT",
        "minIso",
        "bscPX",
        "bscPY",
        "bscP",
        "eleHasL1",
        "posHasL1",
        "eleHasL2",
        "posHasL2",
        "eleFirstHitX",
        "posFirstHitX",
        "nPos"])
else:
    print "invalid cut type"
    sys.exit(-1)

n = events.size

#cut = numpy.row_stack((events["isPair1"]==1,
#    events["eleMatchChisq"]<3,
#    events["posMatchChisq"]<3,
#    abs(events["eleClT"]-events["posClT"])<1.6,
#    events["eleClY"]*events["posClY"]<0,
#    events["nPos"]==1)).all(0)


if cutType=="bumphunt":
    #cut = numpy.ones(n)
    cut = events["uncP"]>0.8*ebeam
    output = numpy.core.records.fromarrays([
        events["uncP"],
        events["uncM"],
        events["uncVZ"],
        cut,
        numpy.zeros(n),
        numpy.zeros(n)
        ], dtype=[
            ("uncP",events.dtype["uncP"]),
            ("uncM",events.dtype["uncM"]),
            ("uncVZ",events.dtype["uncVZ"]),
            ("cut",numpy.int8),
            ("nPass",numpy.int8),
            ("rank",numpy.int8)])
elif cutType=="vertexing":
    cut = numpy.row_stack((events["isPair1"]==1,
        events["eleHasL1"]==1,
        events["posHasL1"]==1,
        events["eleHasL2"]==1,
        events["posHasL2"]==1,
        events["eleMatchChisq"]<3,
        events["posMatchChisq"]<3,
        abs(events["eleClT"]-events["posClT"])<2,
        events["eleClY"]*events["posClY"]<0,
        abs(events["bscPY"]/events["bscP"])<0.01,
        abs(events["bscPX"]/events["bscP"])<0.01,
        events["eleFirstHitX"]-events["posFirstHitX"]<2,
        events["bscChisq"]<5,
        events["minIso"]>0.5,
        events["eleP"]<0.8*ebeam,
        events["uncP"]>0.8*ebeam)).all(0)
    output = numpy.core.records.fromarrays([
        events["run"],
        events["event"],
        events["uncP"],
        events["uncM"],
        events["uncVZ"],
        cut,
        numpy.zeros(n),
        numpy.zeros(n)
        ], dtype=[
            ("run",events.dtype["run"]),
            ("event",events.dtype["event"]),
            ("uncP",events.dtype["uncP"]),
            ("uncM",events.dtype["uncM"]),
            ("uncVZ",events.dtype["uncVZ"]),
            ("cut",numpy.int8),
            ("nPass",numpy.int8),
            ("rank",numpy.int8)])
else:
    print "invalid cut type"
    sys.exit(-1)

currentevent = 0
candidates = []

for i in xrange(0,n):
    if events[i]["event"]!=currentevent:
        if cutType=="bumphunt":
            candidates.sort(key=lambda x:events[x]["tarChisq"],reverse=False)
        elif cutType=="vertexing":
            candidates.sort(key=lambda x:events[x]["bscChisq"],reverse=False)
        else:
            print "invalid cut type"
            sys.exit(-1)
#        ranked_candidates = sorted(candidates, key=lambda x:events[x][sortkey],reverse=highestBest)
        rank=1
        for j in candidates:
            output[j]["nPass"]=len(candidates)
            output[j]["rank"]=rank
            rank+=1
        del candidates[:]
        currentevent = events[i]["event"]
    if output[i]["cut"]!=0:
        candidates.append(i)

if cutOutput:
    output = output[output["cut"]!=0]

root_numpy.array2root(output,remainder[0],mode="recreate",treename="cut")
#newtree=root_numpy.array2tree(output)
#newtree.Scan()
