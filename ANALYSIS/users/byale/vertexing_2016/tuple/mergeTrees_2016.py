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
    print '\t-t: apply default trident cuts'
    print '\t-p: apply pulser trident cuts'
    print '\t-o: apply Omar\'s trident cuts'
    print '\t-l: apply loose trident cuts'
    print '\t-V: apply trident cuts without a vertex chisq requirement'
    print '\t-v: apply default vertexing cuts'
    print '\t-m: apply default Moller cuts'
    print '\t-w: apply default WAB cuts'
    print '\t-e: use this beam energy (default 1.056)'
    print '\t-c: use this cluster-track deltaT (default 43.0)'
    print '\t-z: use this target Z (default -5.0)'
    print '\t-h: this help message'
    print

ebeam=2.3
#THIS CLUSTER TIME IS FOR rotaionFix MC!
#clusterT = 43.0
#THIS CLUSTER TIME IS FOR MG_alphaFixMC!
clusterT = 52.0
#THIS CLUSTER TIME IS FOR DATA!
#clusterT = 56.0
targetZ = 0.5
triCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<5&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50&&eleP<{0}*0.75&&tarP<{0}*1.15"
pulserTriCut = "isPulser&&max(eleMatchChisq,posMatchChisq)<5&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&max(eleTrkChisq,posTrkChisq)<50&&tarChisq<50&&eleP<{0}*0.75&&tarP<{0}*1.15"
omarTriCut = "isPair1&&nPos==1&&max(eleMatchChisq,posMatchChisq)<3&&abs(eleClT-posClT)<1.6&&eleClY*posClY<0"
looseTriCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<30&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&max(eleTrkChisq,posTrkChisq)<50"
noVertTriCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<5&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&max(eleTrkChisq,posTrkChisq)<50&&eleP<{0}*0.75&&tarP<{0}*1.15"

vertCut = "isPair1&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0+{2}*posPX/posP<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15"

#vertCut = "isPair1&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&max(eleTrkChisq,posTrkChisq)<30&&minPositiveIso-0.02*bscChisq>0.5&&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15"
#vertCut = "isPair1&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&max(eleTrkChisq,posTrkChisq)<30&&minPositiveIso-0.02*bscChisq>0.5&&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15"
allVertCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&abs(eleP-posP)/(eleP+posP)<0.4&&posTrkD0+{2}*posPX/posP<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15"
mollerCut = "topP<{0}*0.85&&botP<{0}*0.85&&uncP>{0}*0.85&&uncP<{0}*1.1&&abs(topTrkT-botTrkT)<5&&abs(uncPX)<{0}*0.02&&abs(uncPY)<{0}*0.01&&vzcChisq<20"
wabCut = "isPair1&&abs(phoClT-eleTrkT-{1})<3"
cut=""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'tpolVvamwe:c:z:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-t':
            cut=triCut
        if opt=='-p':
            cut=pulserTriCut
        if opt=='-o':
            cut=omarTriCut
        if opt=='-l':
            cut=looseTriCut
        if opt=='-V':
            cut=noVertTriCut
        if opt=='-v':
            cut=vertCut
        if opt=='-a':
            cut=allVertCut
        if opt=='-m':
            cut=mollerCut
        if opt=='-w':
            cut=wabCut
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
