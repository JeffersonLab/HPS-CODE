#!/usr/bin/python

import sys
import math
import ROOT 
import argparse
import os
import numpy as np
from subprocess import Popen, PIPE
from  histograms import myHistograms

def makePretty(h, xname, yname,  color = 1, lwid = 3 , ltype=1) : 
     h.SetLineColor(color);
     h.SetLineWidth(lwid);
     h.SetLineStyle(ltype);
     h.SetXTitle(xname);
     h.SetYTitle(yname);
     h.SetMinimum(0.0);
     
def main() : 
    ROOT.gROOT.SetBatch(True) 
#myhist=myHistograms()

#goodRuns='golden-runs-Feb10-2016.txt'
#with open(goodRuns,"r") as tmp:
#    lines = tmp.readlines()

#dataPath="OutputHistograms/Data/pass4/"
#label="_useGBL_ECalMatch"
#dataPath="VertexHistograms/Data/pass4/"
    dataPath="VertexHistograms/Data/"
    mcPath = "VertexHistograms/MC/";
    label="_pass4_IsoCut_1pt0_v0chi2_10_useGBL_ECalMatch"  
    prefix="hps_00"
    run="5772"
    mcSamples=["tritrig-beam-tri"]
    mcLabel="_HPS-EngRun2015-Nominal-v3-4"

    dataFile=ROOT.TFile(dataPath+prefix+run+label+".root")
    dataFile.cd()
    allKeys = ROOT.gDirectory.GetListOfKeys()

    mcFile=[]
    for sample in mcSamples:     
        mcFile.append(ROOT.TFile(mcPath+sample+mcLabel+label+".root"))

    plotFileName="SummaryPlots/out.pdf";
#loop through all of the histograms
    canvas=ROOT.TCanvas("Dumb Canvas")
    cnt=0
    for key in allKeys : 
        h = key.ReadObj()
        if h.GetEntries() > 0 : 
           h.Scale(10000.0/h.GetEntries())
           max=h.GetMaximum()
        makePretty(h,"foo","bar")
        hname=h.GetName()    
        mchList=[]
        for mcf in mcFile :
            mch=mcf.Get(hname)
            if mch.GetEntries() > 0 :
                mch.Scale(10000.0/mch.GetEntries())                
            mchList.append(mch)
            makePretty(mch,"foo","bar",2)
            tm=mch.GetMaximum()
            if tm > max : 
                max=tm
            #do something to them...
        h.SetMaximum(1.2*max)
        h.Draw()
        for mch in mchList : 
            mch.Draw("same")

        if key == allKeys.First(): 
            canvas.Print(plotFileName+"(")
        elif key == allKeys.Last() : 
            print "Closing File"
            canvas.Print(plotFileName+")")
        else :
            canvas.Print(plotFileName)

if __name__ == "__main__":
    main()
