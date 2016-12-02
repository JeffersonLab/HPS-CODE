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
     iLumi=4403638.0/1000.0 # ub^-1  run 5772
     #wabv2
     #  Average generated XS = 7.06874167417  (E11, pb)from 1111 jobs
     wabXS=7.06874167417e11/1e6 #ub 
     tritrigXS=1.76*1000.0 #ub
#ifarm1101> python parseAndAverageXS.py
#Average generated XS = 6772813555.56 pb from 900 jobs  ... 
     tritrigNOSUMCUTXS= 6772813555.56/1e6 #ub
#hps@ifarm1102> python parseAndGetEvents.py 
#Number Passed = 2909346.0 out of 76289361.0
#Average Efficiency = 0.0381356713684 from 1000 jobs
     wabNGen=76289361.0*995/1000 #5 dst files missing
#hps@ifarm1102> python parseAndGetEvents.py 
#Number Passed = 8654274.0 out of 45123760.0
#Average Efficiency = 0.191789735607 from 376 jobs
     tritrigNGen= 45123760.0 # got all jobs here
#     ifarm1101> python parseAndGetEvents.py
#     Number Passed = 2066549.0 out of 35380271.0
#     Average Efficiency = 0.0584096430465 from 299 jobs
     tritrigNOSUMCUTNGen=35380271.0*244/299.0 #missed some dsts
#     wabBeamTriNBunches=500000*10*1000 # number of bunches
#     wabBeamTriLumi=86.1 #ub^-1
     wabBeamTriLumi=410.0 #ub^-1
     wabBeamTriZipFixLumi=75.0 #ub^-1
     wabBeamTriZipFixT0OffsetLumi=67.4 #ub^-1

     ROOT.gROOT.SetBatch(True) 
#myhist=myHistograms()

#goodRuns='golden-runs-Feb10-2016.txt'
#with open(goodRuns,"r") as tmp:
#    lines = tmp.readlines()
    
     dataPath="OutputHistograms/Data/"
     label="_engrun2015_pass6_TopBot_LeftRight"
#     label="_pass6_useGBL_ECalMatch_ECalCoincidence"
#     mcTag="_TrackKiller_Position"
     mcTag="_TrackKiller_Momentum"
#     mcTag=""
     dataNorm=[1/iLumi]
     mcPath="OutputHistograms/MC/"
     mcLabel="_HPS-EngRun2015-Nominal-v5-0"
     prefix=""
     run="hps_005772"
#     mcSamples=["wab","tritrig","wab-beam-tri"]
#     mcSamples=["wab","tritrig"]
#     mcNorm=[wabXS/wabNGen, tritrigXS/tritrigNGen,1/wabBeamTriLumi]
     
#     mcSamples=["wab","tritrig-NOSUMCUT","wab-beam-tri-zipFix","wab-beam-tri-zipFix-T0Offset"]
     mcSamples=["wab","tritrig-NOSUMCUT","wab-beam-tri-zipFix"]
     mcNorm=[wabXS/wabNGen, tritrigNOSUMCUTXS/tritrigNOSUMCUTNGen,1/wabBeamTriZipFixLumi,1/wabBeamTriZipFixT0OffsetLumi]

#     mcScale=[1,1,1,1]
     mcScale=[0.65,0.65,0.65,0.65]
     dataFile=ROOT.TFile(dataPath+prefix+run+label+".root")
     dataFile.cd()
     allKeys = ROOT.gDirectory.GetListOfKeys()

     mcFile=[]
     for sample in mcSamples:     
          print 'loading '+mcPath+prefix+sample+mcLabel+label+mcTag+".root"
          mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+label+mcTag+".root"))
#          print 'loading '+mcPath+prefix+sample+mcLabel+label+".root"
#          mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+label+".root"))
          
     plotFileName="SummaryPlots/allplots"+label+mcTag+".pdf"
#loop through all of the histograms
     cnt=0     
     for key in allKeys : 
          canvas=ROOT.TCanvas("Dumb Canvas")
          h = key.ReadObj()
          if not h.GetEntries() > 0  : continue
          is2D =False
#          if type(h) is ROOT.TH2D: continue
          if type(h) is ROOT.TH2D: is2D=True
          if is2D : 
               canvas.Divide(2,2)     
          canvas.cd(1)
#         h.Scale(10000.0/h.GetEntries())                
          h.Scale(dataNorm[0])
          max=h.GetMaximum()
          makePretty(h,"foo","#sigma (#mub)")
          hname=h.GetName()    
          mchList=[]
          mchLabList=[]
          mchScaleList=[]
          print hname+' ' +str(len(mcFile))
          for ii in range(len( mcFile)) :
               mcf=mcFile[ii]
               mch=mcf.Get(hname)
               if not mch: 
                    print hname+' '+str(ii)+ ' does not exist!'
                    continue
#               mch.Scale(10000.0/mch.GetEntries())                
               mch.Scale(mcNorm[ii]*mcScale[ii])                
               print mch.Integral()
               mchList.append(mch)
               mchLabList.append(mcSamples[ii])
               mchScaleList.append(mcScale[ii])
               makePretty(mch,"foo","bar",ii+2)
               tm=mch.GetMaximum()
               if tm > max : 
                    max=tm
            #do something to them...
          leg=ROOT.TLegend(0.1,0.9,0.3,0.8)               
          leg.AddEntry(h,"Run 5772","l")
          if not is2D: 
               h.SetMaximum(1.2*max)
          if is2D: 
               h.SetTitle(h.GetTitle()+' Data')
               h.Draw("colz")
          else:
               h.Draw()
          for i in range(0,len(mchList)) :
               mch= mchList[i]  
               if is2D : 
                    canvas.cd(i+2)                         
                    mch.SetTitle(mch.GetTitle()+' '+mchLabList[i]+' x'+str(mchScaleList[i]))
                    mch.Draw("colz")
               else: 
                    mch.Draw("same")
                    leg.AddEntry(mch,mchLabList[i]+' x'+str(mchScaleList[i]),"l")
                    i+=1
               if not is2D: 
                    leg.Draw()

          if key == allKeys.First(): 
               canvas.Print(plotFileName+"(")
          elif key == allKeys.Last() : 
               print "Closing File"
               canvas.Print(plotFileName+")")
          else :
               canvas.Print(plotFileName)

if __name__ == "__main__":
     main()
