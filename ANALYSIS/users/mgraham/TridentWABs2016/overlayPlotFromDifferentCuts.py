#!/usr/bin/python

import sys
import math
import ROOT 
import argparse
import os
import numpy as np
from subprocess import Popen, PIPE

def makePretty(h, xname, yname,  color = 1, lwid = 3 , ltype=1) : 
     h.SetLineColor(color);
     h.SetLineWidth(lwid);
     h.SetLineStyle(ltype);
     h.SetXTitle(xname);
     h.SetYTitle(yname);
     h.SetMinimum(0.0);

def main() : 

     normToArea=False

     iLumi=4403638.0/1000.0 # ub^-1  run 5772
     #wabv2
     #  Average generated XS = 7.06874167417  (E11, pb)from 1111 jobs
     wabXS=7.06874167417e11/1e6 #ub 
     tritrigXS=1.76*1000.0 #ub
#wab with the spinfix 
#Average generated XS = 5.99895197803e+11 from 32229 jobs
#Number Passed = 12176634.0 out of 315552135.0
#Average Efficiency = 0.0385883429374 from 1354 jobs
     wabSpinFixXS=5.99895197803e+11/1e6
     wabSpinFixNGen= 315552135.0 *1582/1200  #some log files are missing?
#####  tritrig MG5 with ECut>0.4 GeV...this had some funny things in the generation...we are redoing with ECut>0.5 GeV
#Average generated XS = 1.32505069e+12 from 1000 jobs
#Number Passed = 400934.0 out of 2662717.0
#Average Efficiency = 0.150573267831 from 79 jobs
#     tritrigMG5XS = 1.32505069e+12/1e6 #ub ... this is totally screwed!  
     tritrigMG5XS = 2000.0  #ub .. this is roughly what Takashi sees with cut at 0.5GeV
     tritrigMG5NGen=35380271.0*100/79 #some of the log files were corrupt...
######  RAD MG5  (no xchange)
#Average generated XS = 55678238.342 from 386 jobs
#Number Passed = 1179350.0 out of 3900390.0
#Average Efficiency = 0.302367199178 from 39 jobs
     radMG5XS = 55678238.342/1e6 #ub = 55. ub
     radMG5NGen = 3900390.0*50/39  #some of the log files were corrupt...
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
     label="_pass6_WABs_PureAndConverted"
#     mcTag="_TrackKiller_Position"
#     mcTag="_TrackKiller_Momentum"
     mcTag=""
     plotTags=["L1","L2","L1L2","L2L1","L2L2"]
     dataNorm=[1/iLumi]
     mcPath="OutputHistograms/MC/"
     mcLabel="_HPS-EngRun2015-Nominal-v5-0"
     prefix="fromscratch_"
     run="hps_005772"
#     mcSamples=["wab","tritrig","wab-beam-tri"]
#     mcSamples=["wab","tritrig"]
#     mcNorm=[wabXS/wabNGen, tritrigXS/tritrigNGen,1/wabBeamTriLumi]
     
#     mcSamples=["wab","tritrig-NOSUMCUT","wab-beam-tri-zipFix","wab-beam-tri-zipFix-T0Offset"]
#     mcSamples=["wab","tritrig-NOSUMCUT","wab-beam-tri-zipFix"]

#     mcSamples=["wab-spinfix","wab","wab-beam-tri-zipFix",'tritrig-MG5']
     mcSamples=["wab-spinfix"]
     mcNorm=[wabSpinFixXS/wabSpinFixNGen, wabXS/wabNGen,1/wabBeamTriZipFixLumi,radMG5XS/radMG5NGen]

#     mcScale=[1,1,1,1]
     mcScale=[1.52,0.58,0.58,50,1,1]
#     mcScale=[0.65,0.65,0.65,0.65]
     dataFile=ROOT.TFile(dataPath+prefix+run+label+".root")
     dataFile.cd()
     allKeys = ROOT.gDirectory.GetListOfKeys()
     basePlots=[]
          #check to see if this is the base key...no modifier
     for key in allKeys: 
          isBase=True
          h = key.ReadObj()
          hname=h.GetName()
          for tag in plotTags :
               if tag in hname : 
                    isBase=False
          if isBase: 
               print "Found base = "+hname
               basePlots.append(hname)       

     mcFile=[]
     is2D=False
     for sample in mcSamples:     
          print 'loading '+mcPath+prefix+sample+mcLabel+label+mcTag+".root"
          mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+label+mcTag+".root"))
          
     plotFileName="SummaryPlots/allplots"+label+"LayerComparison"+".pdf"
#loop through all of the histograms
     cnt=0     
     plotTags.insert(0,"")
     for bn in basePlots : 
          canvas=ROOT.TCanvas("Dumb Canvas")
          dataList=[]
          dataLabList=[]
          mchList=[]
          mchLabList=[]
          mchScaleList=[]
          max=-99999
          for ii in range(len( plotTags)) :
               dataFile.cd()
               hname=bn.replace("TB",plotTags[ii]+"TB")
               print "Processing "+hname
               h = dataFile.Get(hname)
               if type(h) is not  ROOT.TH1D  : continue
               canvas.cd(1)
               totalCrossSection=h.GetEntries()*dataNorm[0]
               print "data cross-section = "+str(totalCrossSection)+" ub"
               if normToArea : 
                    h.Scale(10000.0/h.GetEntries())                
               else: 
                    h.Scale(dataNorm[0])

               tm=h.GetMaximum()
               if tm > max : 
                    max=tm

               dataList.append(h)
               dataLabList.append("run5772 "+plotTags[ii])
               if normToArea : 
                    makePretty(h,"foo","Arbitrary",ii)
               else: 
                    makePretty(h,"foo","#sigma (#mub)",ii+1)
               for kk in range(len( mcSamples)) :
                    mcf=mcFile[kk]
                    mch=mcf.Get(hname)
                    if not mch: 
                         print hname+' '+str(ii)+ ' does not exist!'
                         continue
                    if normToArea: 
                         mch.Scale(10000.0/mch.GetEntries())                
                    else : 
                         mch.Scale(mcNorm[kk]*mcScale[kk])                   
                    print 'MC integral = '+str(mch.Integral())
                    mchList.append(mch)
                    lab=str(plotTags[ii])+"_"+str(mcSamples[kk])
                    mchLabList.append(lab)
                    mchScaleList.append(mcScale[kk])
                    makePretty(mch,"foo","bar",kk+(ii+1)*10+1)
                    tm=mch.GetMaximum()
                    if tm > max : 
                         max=tm
            #do something to them...
          leg=ROOT.TLegend(0.1,0.9,0.3,0.8)               
          for k in range(0,len(dataList)): 
               h=dataList[k]
               leg.AddEntry(h,dataLabList[k],"l")
               h.SetMaximum(1.2*max)
               print 'plotting data  '+h.GetName()
               if k==0: 
                    h.Draw()
               else : 
                    h.Draw("same")
                    
          for i in range(0,len(mchList)) :
               mch= mchList[i]  
               print 'plotting '+mch.GetName()+'; mc label '+mchLabList[i]
               mch.Draw("same")
               leg.AddEntry(mch,mchLabList[i]+' x'+str(mchScaleList[i]),"l")
          leg.Draw()
               
          print bn+' ' +basePlots[0]+' ' +basePlots[-1]
          if bn == basePlots[0]: 
               canvas.Print(plotFileName+"(")
          elif bn == basePlots[-1] : 
               print "Closing File"
               canvas.Print(plotFileName+")")
          else :
               canvas.Print(plotFileName)

if __name__ == "__main__":
     main()
