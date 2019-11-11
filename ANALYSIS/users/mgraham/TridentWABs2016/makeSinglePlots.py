#!/usr/bin/python

import sys
import math
import ROOT 
import argparse
import os
import numpy as np
from subprocess import Popen, PIPE

def makePretty(h, xname, yname,  color = 1, lwid = 3 , ltype=1) : 
     h.SetLineColor(color)
     h.SetLineWidth(lwid)
     h.SetLineStyle(ltype)
     h.SetXTitle(xname)
     h.SetYTitle(yname)
     h.SetMinimum(0.0)
     h.SetTitle("")


def plotOverlay(l1,l2,xname,yname,leg1,leg2,outName,noScale=False):
    if type(l1) is not ROOT.TH1D : 
        print "what?  l1 is not a TH1D?"
        print type(l1)
        return 
    if type(l2) is not ROOT.TH1D : 
        print "what?  l2 is not a TH1D?"
        print type(l2)
        return

    if not noScale: 
         l2.Scale(l1.GetEntries()/l2.GetEntries())

    max=1.2*l1.GetMaximum()
    if l2.GetMaximum() > l1.GetMaximum: 
        max=1.2*l2.GetMaximum()

    l1.SetMaximum(max)
    makePretty(l1,xname,yname)
    makePretty(l2,xname,yname,2)
    
    leg=ROOT.TLegend(0.1,0.9,0.3,0.8)               
    leg.AddEntry(l1,leg1,"l")
    leg.AddEntry(l2,leg2,"l")
    
    ct=ROOT.TCanvas()
    l1.Draw()   
    l2.Draw("same")
    leg.Draw()
    ct.SaveAs("SinglePlots/"+outName+".pdf")


def plotOverlayLists(pList,xname,yname,legList,outName,noScale=False):     
     arbScale=1000
     maxVal=-999999.0
     for i in range(0,len(pList)) :           
          if type(pList[i]) is not ROOT.TH1D : 
               print "what?  plot  is not a TH1D?"
               print type(pList[i])
               return           
          if not noScale:
               pList[i].Scale(arbScale/pList[i].Integral())
          maxi=1.2*pList[i].GetMaximum()
          if maxi > maxVal :
               maxVal=maxi
          makePretty(pList[i],xname,yname,i+1)

     ct=ROOT.TCanvas()
     leg=ROOT.TLegend(0.1,0.9,0.3,0.8)               
     for i in range(0,len(pList)) :           
          pList[i].SetMaximum(maxVal)    
          leg.AddEntry(pList[i],legList[i],"l")
          if i == 0 : 
               pList[i].Draw()
          else : 
               pList[i].Draw("same")
     leg.Draw()
     ct.SaveAs("SinglePlots/"+outName+".pdf")


def plotOverlayNormToXS(pList,xname,yname,legList,outName,xsScales): 
     arbScale=1000
     maxVal=-999999.0
     for i in range(0,len(pList)) :           
          if type(pList[i]) is not ROOT.TH1D : 
               print "what?  plot  is not a TH1D?"
               print type(pList[i])
               return           
          pList[i].SetStats(False)
          pList[i].Sumw2()
          pList[i].Scale(xsScales[i])
          maxi=1.2*pList[i].GetMaximum()
          if maxi > maxVal :
               maxVal=maxi
          makePretty(pList[i],xname,yname,i+1)

     ct=ROOT.TCanvas()
     leg=ROOT.TLegend(0.1,0.9,0.3,0.8)               
     for i in range(0,len(pList)) :           
          pList[i].SetMaximum(maxVal)    
          leg.AddEntry(pList[i],legList[i],"el")
          if i == 0 : 
               pList[i].Draw("ehist")
          else : 
               pList[i].Draw("esame")
     leg.Draw()
     ct.SaveAs("SinglePlots/"+outName+".pdf")


def sumPlots(h1,h2):
     sum=h1.Clone()
     sum.SetDirectory(0)
     sum.Add(h2.Clone())
     return sum

def main()  :    
    ROOT.gROOT.SetBatch(True) 
    dataPath="OutputHistograms/Data/"
    label="_pass6_WABs_PureAndConverted_NoESumCut"
#    label="_pass6_WABs_PureAndConverted"
    mcTag=["","_TrackKiller_Momentum","_TrackKiller_Position"]
    mcTag=["_WeighInEclVsY_ElePosSame"]
#    dataNorm=[1/iLumi]
    mcPath="OutputHistograms/MC/"
    mcLabel="_HPS-EngRun2015-Nominal-v5-0"
    prefix="fromscratch_"
    run="hps_005772"
#
    alphaFixWAB=0.81
    alphaFixTri=0.76
    fudge=0.8
    wabFudge=0.89#  this comes from the observed WAB XS data-MC difference, even after track killing
#    wabFudge=1.0#  this comes from the observed WAB XS data-MC difference, even after track killing
#
    iLumi=4403638.0/1000.0 # ub^-1  run 5772
    wabBeamTriMG5FixDtLumi=100*100*8004.68/1e6 #ub^-1
    wabBeamLumi=100*100*8004.68/1e6 #ub^-1
    triBeamLumi=100*99*8004.68/1e6 #ub^-1
#
    mcSamples=["wab-beam","tri-beam","wab-beam-tri-MG5-fixECalTiming"]    
#    evtToXS=[1/iLumi, 1/wabBeamLumi*alphaFixWAB*fudge,1/triBeamLumi*alphaFixTri*fudge,1/wabBeamTriMG5FixDtLumi*alphaFixWAB*fudge] 
    evtToXS=[1/iLumi, 1/wabBeamLumi*alphaFixWAB*wabFudge,1/triBeamLumi*alphaFixTri,1/wabBeamTriMG5FixDtLumi*alphaFixWAB*wabFudge] 
     
    dataFile=ROOT.TFile(dataPath+prefix+run+label+".root")
    dataFile.cd()

    mcFile=[]
    
#    for sample in mcSamples:     
#        print 'loading '+mcPath+prefix+sample+mcLabel+label+mcTag+".root"
#        mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+label+mcTag+".root"))

#    tagNum=-1
#    for tag in mcTag :
#         mcFile.append([])
#         tagNum+=1
    for sample in mcSamples:     
         print 'loading '+mcPath+prefix+sample+mcLabel+label+mcTag[0]+".root"
         mcFile.append(ROOT.TFile(mcPath+prefix+sample+mcLabel+label+mcTag[0]+".root"))


#########################
    drawPlots=["GamEmL1TB-p1d0","GamEmL2TB-p1d0"]        
    dataFile.cd()
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"electron d0 (mm)","Arbitrary","gamma e- L1 Data","gamma e- L2 Data","emgamma-electrond0-L1vsL2-data")

########################
    drawPlots=["EpEmL1L1TB-p2d0","EpEmL1L2TB-p2d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"electron d0 (mm)","Arbitrary","e+e- electron L1 Data","e+e- electron L2 Data","e+e--electrond0-L1vsL2-data")

########################
    drawPlots=["EpEmL2L1TB-p2d0","EpEmL2L2TB-p2d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"electron d0 (mm)","Arbitrary","e+e- electron L1 Data","e+e- electron L2 Data","e+e--electrond0-L1vsL2-positronMissL2data")

########################
    drawPlots=["EpEmL1L1TB-p1d0","EpEmL2L1TB-p1d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"positron d0 (mm)","Arbitrary","e+e- positron L1 Data","e+e- positron L2 Data","e+e--positrond0-L1vsL2-data")

########################
    drawPlots=["EpEmL1L1TB-p1d0","EpEmL1L1TB-p2d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"d0 (mm)","Arbitrary","e+e- positron L1 Data, electron L1","e+e- electron L1 Data, positronL1","e+e--d0-electronVspositron-data")

########################
    drawPlots=["EpEmL1L1TB-p2d0","EpEmL2L1TB-p2d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"d0 (mm)","Arbitrary","e+e- electron L1 Data, positron L1","e+e- electron L1 Data, positron L2","e+e--electrond0-positronL1vsL2-data")


########################
    drawPlots=["EpEmL1L2TB-p1d0","EpEmL2L2TB-p1d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"d0 (mm)","Arbitrary","e+e- positron L1 Data","e+e- positron L2 Data","e+e--positrond0-L1vsL2-electronMissL2data")

########################
    drawPlots=["EpEmL1L2TB-p1d0","EpEmL2L2TB-p1d0"]
    l1=dataFile.Get(drawPlots[0])
    l2=dataFile.Get(drawPlots[1])
    plotOverlay(l1,l2,"d0 (mm)","Arbitrary","e+e- positron L1 Data","e+e- positron L2 Data","e+e--positrond0-L1vsL2-electronMissL2data")

########################
    var="V0PyTimesP2Py"
    drawPlots=["GamEmL1TB-"+var,"EpEmL2L1TB-"+var,"EpEmL2L2TB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(dataFile.Get(drawPlots[1]))
    pList.append(dataFile.Get(drawPlots[2]))
    lList=["gamma e- L1 Data"]
    lList.append("e+e-  L2L1 Data")
    lList.append("e+e-  L2L2 Data")
    plotOverlayLists(pList,"Py(V0) x Py(e-) ","Arbitrary",lList,"v0xe-Py-emgammaVsEpEm-WABs")

########################
    var="V0PyTimesP2Py"
    drawPlots=["GamEmL1TB-"+var,"EpEmL2L1TB-"+var,"EpEmL1L1TB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(dataFile.Get(drawPlots[1]))
    pList.append(dataFile.Get(drawPlots[2]))
    lList=["gamma e- L1 Data"]
    lList.append("e+e-  L2L1 Data")
    lList.append("e+e-  L1L1 Data")
    plotOverlayLists(pList,"Py(V0) x Py(e-) ","Arbitrary",lList,"v0xe-Py-emgammaVsEpEm-TriWABs")


########################
    var="p2slope"
    drawPlots=["GamEmL1TB-"+var,"GamEmL2TB-"+var,"EpEmL2L1TB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(dataFile.Get(drawPlots[1]))
#    pList.append(dataFile.Get(drawPlots[2]))
    lList=["gamma e- L1 Data"]
    lList.append("gamma e-  L2 Data")
#    lList.append("e+e-  L2L1 Data")
    plotOverlayLists(pList,"electron slope","Arbitrary",lList,"electronslope-emgammaVsEpEm-WABs",True)


########################
    var="p2slope"
    drawPlots=["GamEmL1TB-"+var,"EpEmL1L1TB-"+var,"EpEmL2L1TB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(dataFile.Get(drawPlots[1]))
    pList.append(dataFile.Get(drawPlots[2]))
    lList=["gamma e- L1 Data"]
    lList.append("e+e-  L1L1 Data")
    lList.append("e+e-  L2L1 Data")
    plotOverlayLists(pList,"electron slope","Arbitrary",lList,"electronslope-emgammaVsEpEm-TriWABs")
########################
###    gammae- data vs MC
########################
    var="eSum"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    lList=["gamma e- Data"]
    lList.append("gamma e- WAB-beam")
    lList.append("gamma e- Tri-beam")  
    lList.append("gamma e- WAB-beam-tri")
    plotOverlayNormToXS(pList,"E(#gamma+e^{-}) (GeV)","#sigma (#mub)",lList,"eSum-emgamma-data-vs-MC",evtToXS)
########################
    var="pairMass"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"M(#gamma+e^{-}) (GeV)","#sigma (#mub)",lList,"mass-emgamma-data-vs-MC",evtToXS)
########################
    var="p1Mom"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"E(#gamma) (GeV)","#sigma (#mub)",lList,"Egamma-emgamma-data-vs-MC",evtToXS)
########################
    var="p2Mom"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"p(e^{-}) (GeV)","#sigma (#mub)",lList,"Pele-emgamma-data-vs-MC",evtToXS)
########################
    var="p1ClusterSlope"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"#theta_{y}(#gamma) (GeV)","#sigma (#mub)",lList,"slopegamma-emgamma-data-vs-MC",evtToXS)
########################
    var="p2slope"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"#theta_{y}(e^{-}) (GeV)","#sigma (#mub)",lList,"slopeele-emgamma-data-vs-MC",evtToXS)
########################
    var="V0PyXSignP1"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"V0(py) (GeV)","#sigma (#mub)",lList,"v0pygamma-emgamma-data-vs-MC",evtToXS)
########################
    var="p2d0"
    drawPlots=["GamEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"d0 (mm)","#sigma (#mub)",lList,"d0ele-emgamma-data-vs-MC",evtToXS)

########################
###    e+e- data vs MC
########################
    var="eSum"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    lList=["e+e- Data"]
    lList.append("e+e- WAB-beam")
    lList.append("e+e- Tri-beam")  
    lList.append("e+e- MC Sum")
    plotOverlayNormToXS(pList,"E(e^{+}+e^{-}) (GeV)","#sigma (#mub)",lList,"eSum-emep-data-vs-MC",evtToXS)
########################
    var="pairMass"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"M(e^{+}+e^{-}) (GeV)","#sigma (#mub)",lList,"mass-emep-data-vs-MC",evtToXS)
########################
    var="p1Mom"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#   pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"p(e^{+}) (GeV)","#sigma (#mub)",lList,"ppos-emep-data-vs-MC",evtToXS)
########################
    var="p2Mom"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"p(e^{-}) (GeV)","#sigma (#mub)",lList,"pele-emep-data-vs-MC",evtToXS)
########################
    var="p1slope"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#   pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"#theta_{y}(e^{+}) (GeV)","#sigma (#mub)",lList,"slopepos-emep-data-vs-MC",evtToXS)########################
    var="p2slope"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#   pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"#theta_{y}(e^{-}) (GeV)","#sigma (#mub)",lList,"slopeele-emep-data-vs-MC",evtToXS)
########################
    var="V0PyXSignP1"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
#    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"V0(py) (GeV)","#sigma (#mub)",lList,"v0pypos-emep-data-vs-MC",evtToXS)
########################
    var="p2d0"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"d0 (mm)","#sigma (#mub)",lList,"d0ele-emep-data-vs-MC",evtToXS)
########################
    var="p1d0"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
#    pList.append(mcFile[2].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
    plotOverlayNormToXS(pList,"d0 (mm)","#sigma (#mub)",lList,"d0pos-emep-data-vs-MC",evtToXS)


########################
    var="p2z0"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"z0 (mm)","#sigma (#mub)",lList,"z0ele-emep-data-vs-MC",evtToXS)
########################
    var="p1z0"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
#    pList.append(mcFile[2].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
    plotOverlayNormToXS(pList,"z0 (mm)","#sigma (#mub)",lList,"z0pos-emep-data-vs-MC",evtToXS)

########################
    var="p2phi0"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
    pList.append(mcFile[2].Get(drawPlots[0]))
    plotOverlayNormToXS(pList,"phi0 (mm)","#sigma (#mub)",lList,"phi0ele-emep-data-vs-MC",evtToXS)
########################
    var="p1phi0"
    drawPlots=["EpEmTB-"+var]
    pList=[dataFile.Get(drawPlots[0])]
    pList.append(mcFile[0].Get(drawPlots[0]))
    pList.append(mcFile[1].Get(drawPlots[0]))
#    pList.append(mcFile[2].Get(drawPlots[0]))
    pList.append(sumPlots(mcFile[0].Get(drawPlots[0]),mcFile[1].Get(drawPlots[0])))  
    plotOverlayNormToXS(pList,"phi0 (mm)","#sigma (#mub)",lList,"phi0pos-emep-data-vs-MC",evtToXS)

if __name__ == "__main__":
     main()
