import sys
import shutil
import re
import string
import os
import glob
import ROOT
from subprocess import Popen, PIPE

runno="8099"
label="pass4_NoESumCut_OmarsBase"
instring="OutputHistograms/Data/fromscratch_hps_00"+runno+".*"+label+".root"
outputname="OutputHistograms/Data/fromscratch_hps_00"+runno+label+".root"
inFiles=glob.glob(instring)
#print(inFiles)
newHistList={}
outputFile=ROOT.TFile(outputname,"recreate")
for file in inFiles: 
    print(file)
    thisFile=ROOT.TFile(file)
    thisFile.cd()
    allKeys=ROOT.gDirectory.GetListOfKeys()
#    print(newHistList)
    for key in allKeys: 
        thisFile.cd()
        h=key.ReadObj()
        if not h.GetEntries() > 0: continue
        hname=h.GetName()
        if not (hname in newHistList): #this is the first time we saw this histogram
            print("Adding new histogram "+hname+" to list")
            outputFile.cd()
            newHist=h.Clone()
            newHistList[hname]=newHist            
            print(newHistList)
        else :
            outputFile.cd()
            print("Adding "+hname+":  previous size = "+str(newHistList[hname].GetEntries())) 
            newHistList[hname].Add(h.Clone())
            print("Adding "+hname+":  new size = "+str(newHistList[hname].GetEntries())) 


outputFile.cd()
for hist in newHistList.itervalues(): 
    hist.Write()

outputFile.Close()            
