import sys
import shutil
import re
import string
import os
import glob
import array
from subprocess import Popen, PIPE
import ROOT 

chargeToLumi=2.75541e-14 #1/nb
nCtoEle=6.25e9
analysis_postfix='08242015' 
goodRuns='goodRuns.txt'
data_dir='pass1-dst/'
data_prefix='hps_00'
data_postfix='_dst_R3321.root'
log_dir='logs/'
out_dir='OutputHistograms/'


with open(goodRuns,"r") as tmp:
    lines = tmp.readlines()

runs=array.array('d')
lumis=array.array('d')
xs=array.array('d')
eff=array.array('d')
for line in lines:
    print '##################################################'
    line=line.strip()
    columns=line.split()
    run=columns[0]
    runs.append(float(run))
    nfilesTot=float(columns[1])
    charge=float(columns[2])*nCtoEle
    lumi=chargeToLumi*float(charge)
    lumis.append(lumi)
    dstfile=data_dir+data_prefix+columns[0]+"*" #glob onto this
    nfiles=len(glob.glob(dstfile))
    print run+' has '+str(nfiles)+' files out of '+str(nfilesTot)+'; total Run Lumi='+str(lumi)+' nb' 
    logfile=log_dir+data_prefix+columns[0]+'_'+analysis_postfix+'.log'
    foundCuts=False
    with open(logfile,"r") as tmp:
        loglines = tmp.readlines()
    for logline in loglines:
        if re.search("^\s*Tracking\s*Cuts",logline) != None:
            matchMe=re.search("(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)",logline)
            if matchMe != None:
                foundCuts=True
                nPass=matchMe.group(1)
                relEff=matchMe.group(2)
                absEff=matchMe.group(3)
                print "Total events passing = "+str(nPass)+" for eff = "+str(absEff)
                blindFrac=(float(nfiles)/float(nfilesTot))
                print "Lumi = "+str(lumi)+"; blind Frac = "+str(blindFrac)
                measuredXS=(float(nPass)/float(lumi*blindFrac))/1000.0
                print "Raw Measured Cross-section = "+str(measuredXS)+" ub"
                xs.append(measuredXS)
                eff.append(float(absEff))
    if foundCuts == False :
        xs.append(0)
        eff.append(0)

gRunVXS=ROOT.TGraph(len(xs),runs, xs)
gRunVXS.SetMinimum(0.0)
gRunVXS.SetMaximum(50.0)
gRunVXS.SetMarkerStyle(20)
gRunVXS.GetXaxis().SetTitle("Run Number")
gRunVXS.GetYaxis().SetTitle("#sigma (#mu b)")

f=ROOT.TFile("xsVRun.root","RECREATE")
gRunVXS.Write()
f.Close()
    


