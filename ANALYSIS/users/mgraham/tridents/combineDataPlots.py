#!/usr/bin/python

import sys
import math
import ROOT 
import argparse
import os
import numpy as np
from subprocess import Popen, PIPE
from  histograms import myHistograms


myhist=myHistograms()

goodRuns='golden-runs-Feb10-2016.txt'
with open(goodRuns,"r") as tmp:
    lines = tmp.readlines()

passNumber="pass4"
#dataPath="OutputHistograms/Data/pass4/"
label="_useGBL_ECalMatch"

dataPath="VertexHistograms/Data/pass4/"
label="_IsoCut_1pt0_v0chi2_10_useGBL_ECalMatch"  
prefix="hps_00"

outputFile=dataPath+"/hps_GoldenRuns"+label+".root" 

run=[]
charge=[]
for line in lines:
    line=line.strip()
    columns=line.split()
    run.append(str(columns[0]))
    charge.append(float(columns[1]))
    fname=dataPath+prefix+columns[0]+label+".root"
#    print fname
    rfile=ROOT.TFile(fname)
    
    if not rfile.IsZombie() :
        print "Adding " + fname
        myhist.addHistograms(rfile)


myhist.saveHistograms(outputFile)
