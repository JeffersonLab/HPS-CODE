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
    print '\t-c: only write candidates that pass cuts'
    print '\t-b: only keep best candidate'
    print '\t-o: only keep candidate if it\'s the only one'
    print '\t-m: use MC information'
    print '\t-h: this help message'
    print

ebeam=1.056
#sortkey="tarChisq"
#highestBest=False


cutType = "none"
cutOutput = False
onlyBest = False
onlyOnly = False
useMC = False
tweakVertex = False

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'e:t:cbomvh')
# Parse the command line arguments
for opt, arg in options:
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-t':
            cutType=arg
        if opt=='-c':
            cutOutput = True
        if opt=='-b':
            onlyBest = True
        if opt=='-o':
            onlyOnly = True
        if opt=='-m':
            useMC = True
        if opt=='-v':
            tweakVertex = True
        if opt=='-h':
            print_usage()
            sys.exit(0)

if len(remainder)!=2:
    print_usage()
    sys.exit(0)
print remainder[0]
print remainder[1]
print cutType

#blah = root_numpy.root2array(remainder[1],branches=["triEndZ"])
if cutType=="bumphunt":
    branchlist=["event",
        "run",
        "tarP",
        "tarM",
        "uncVZ",
        "tarChisq",
        "isPair1",
        "eleMatchChisq",
        "posMatchChisq",
        "eleClY",
        "posClY",
        "eleClT",
        "posClT",
        "nPos"]
elif cutType=="vertexing":
    branchlist=["event",
        "run",
        "uncP",
        "uncM",
        "uncVZ",
        "bscChisq",
        "eleP",
        "posP",
        "elePX",
        "posPX",
        "eleMatchChisq",
        "posMatchChisq",
        "eleTrkChisq",
        "posTrkChisq",
        "eleTrkT",
        "posTrkT",
        "eleClY",
        "posClY",
        "eleClT",
        "posClT",
        "minIso",
        "minPositiveIso",
        "posTrkD0",
        "bscP",
        "eleHasL1",
        "posHasL1",
        "eleHasL2",
        "posHasL2",
        "eleFirstHitX",
        "posFirstHitX",
        "nPos"]
elif cutType=="none":
    branchlist=["event",
        "run",
        "tarP",
        "tarM",
        "uncVZ",
        "tarChisq",
        "isPair1",
        "eleMatchChisq",
        "posMatchChisq",
        "eleClY",
        "posClY",
        "eleClT",
        "posClT",
        "nPos"]
else:
    raise Exception("invalid cut type")

if useMC:
    branchlist.append("triP")
    branchlist.append("triPair1P")
    branchlist.append("triM")
    branchlist.append("triEndZ")
events = root_numpy.root2array(remainder[1],branches=branchlist)

n = events.size

if cutType=="bumphunt":
    #cut = numpy.ones(n)
    cut = events["tarP"]>0.8*ebeam
    names = ["run",
            "event",
            "tarP",
            "tarM",
            "uncVZ"]
elif cutType=="vertexing":
    cut = numpy.row_stack((#events["isPair1"]==1,
        events["eleHasL1"]==1,
        events["posHasL1"]==1,
        #events["eleHasL2"]==1,
        #events["posHasL2"]==1,
        #events["eleMatchChisq"]<10,
        #events["posMatchChisq"]<10,
        #abs(events["eleClT"]-events["eleTrkT"]-43)<4,
        #abs(events["posClT"]-events["posTrkT"]-43)<4,
        #abs(events["eleClT"]-events["posClT"])<2,
        #events["eleClY"]*events["posClY"]<0,
        #events["bscChisq"]<10,
        #events["eleTrkChisq"]<30,
        #events["posTrkChisq"]<30,
        #abs(events["bscPY"]/events["bscP"])<0.01,
        #abs(events["bscPX"]/events["bscP"])<0.01,
        #events["minPositiveIso"]-0.02*events["bscChisq"]>0.5,
        #abs(events["eleFirstHitX"]-events["posFirstHitX"]+2)<7,
        #abs((events["eleP"]-events["posP"])/(events["eleP"]+events["posP"]))<0.4,
        #events["posTrkD0"]<1.5,
        #events["eleP"]<0.75*ebeam,
        #events["uncP"]<1.15*ebeam,
        events["uncP"]>0.8*ebeam)).all(0)
    names = ["run",
            "event",
            "eleHasL1",
            "posHasL1",
            "uncP",
            "uncM",
            "uncVZ"]
elif cutType=="none":
    cut = numpy.ones(n)
    names = ["run",
            "event",
            "tarP",
            "tarM",
            "uncVZ"]
else:
    raise Exception("invalid cut type")

if useMC:
    names.append("triP")
    names.append("triPair1P")
    names.append("triM")
    names.append("triEndZ")

stuff = [[events[i],(i,events.dtype[i])] for i in names]
stuff.append([cut,("cut",numpy.int8)])
stuff.append([numpy.zeros(n),("nPass",numpy.int8)])
stuff.append([numpy.zeros(n),("rank",numpy.int8)])
if tweakVertex:
    corrM = events["uncM"]-0.15e-3*(events["elePX"]/events["eleP"]-events["posPX"]/events["posP"])*events["uncVZ"]/events["uncM"]
    stuff.append([corrM,("corrM",events.dtype["uncM"])])
dataarray = [i[0] for i in stuff]
typearray = [i[1] for i in stuff]
output = numpy.core.records.fromarrays(dataarray,dtype=typearray)
currentevent = 0
candidates = []

for i in xrange(0,n):
    if events[i]["event"]!=currentevent:
        if cutType=="bumphunt":
            candidates.sort(key=lambda x:events[x]["tarChisq"],reverse=False)
        elif cutType=="vertexing":
            candidates.sort(key=lambda x:events[x]["bscChisq"],reverse=False)
        elif cutType=="none":
            candidates.sort(key=lambda x:events[x]["tarChisq"],reverse=False)
        else:
            raise Exception("invalid cut type")
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
if onlyBest:
    output = output[output["rank"]==1]
if onlyOnly:
    output = output[output["nPass"]==1]

root_numpy.array2root(output,remainder[0],mode="recreate",treename="cut")
#newtree=root_numpy.array2tree(output)
#newtree.Scan()
