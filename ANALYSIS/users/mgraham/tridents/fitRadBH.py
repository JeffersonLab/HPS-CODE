#---------------#
#--- imports ---#
#---------------#
import sys
import math
import argparse
import os
import ROOT
import re, array

def makeHistPdf(fName, hName, label, argList,argSet):
    f=ROOT.TFile(fName)
    hist=f.Get(hName)
#    hist.Print("V")
    dataHist=ROOT.RooDataHist(hName+label+"DH",hName+label+"DH",argList,hist)
#    histPdf=ROOT.RooHistPdf(hName+label+"PDF",hName+label+"PDF",ROOT.RooArgSet(argList),dataHist)
    histPdf=ROOT.RooHistPdf(hName+label+"PDF",hName+label+"PDF",argSet,dataHist)
    return histPdf

def main():

    fdirMC='OutputHistograms/MC/'
    fdirData='OutputHistograms/Data/'
    
    radPref='Rad_HPS-EngRun2015-Nominal-v3_10022015_BeamEle0pt8_ECal_GBL'
    bhPref='BH_HPS-EngRun2015-Nominal-v3_10022015_BeamEle0pt8_ECal_GBL'
    dataLabel='hps_005772_10022015_BeamEle0pt8_ECal_GBL'
    postFix='.root'

    minE=0.3
    maxE=1.2
    
    esumName="eSum"

#dependent variable
    eSum=ROOT.RooRealVar("eSum","Energy Sum",0.8,minE,maxE)
#yields
    nRad=ROOT.RooRealVar("nRad","Number of Radiative Events",1000,0,1000000);
    nBH=ROOT.RooRealVar("nBH","Number of BH Events",10000,0,1000000);
#get histogram PDFs

#    radPdf=makeHistPdf(fdirMC+radPref+postFix,esumName,'Rad',ROOT.RooArgList(eSum),ROOT.RooArgSet(eSum))
#    radPdf.Print("v")

#    bhPdf=makeHistPdf(fdirMC+bhPref+postFix,esumName,'BH',ROOT.RooArgList(eSum),ROOT.RooArgSet(eSum))
#    bhPdf.Print("v")

    hName=esumName
    label="Rad"
    argList=ROOT.RooArgList(eSum)
    argSet=ROOT.RooArgSet(eSum)
    f=ROOT.TFile(fdirMC+radPref+postFix)
    radhist=f.Get(hName)
    radDH=ROOT.RooDataHist(hName+label+"DH",hName+label+"DH",argList,radhist)
    radPdf=ROOT.RooHistPdf(hName+label+"PDF",hName+label+"PDF",argSet,radDH)

    label="BH"
    f=ROOT.TFile(fdirMC+bhPref+postFix)
    bhhist=f.Get(hName)
    bhDH=ROOT.RooDataHist(hName+label+"DH",hName+label+"DH",argList,bhhist)
    bhPdf=ROOT.RooHistPdf(hName+label+"PDF",hName+label+"PDF",argSet,bhDH)

 #total PDF
    totalPdf=ROOT.RooAddPdf("totalPdf","Total PDF",ROOT.RooArgList(radPdf,bhPdf),ROOT.RooArgList(nRad,nBH))
    totalPdf.Print("v")

  #get the data histogram
    f=ROOT.TFile(fdirData+dataLabel+postFix)
    dataHist=f.Get(esumName)
    dataHist.Print("V")
    dataDH=ROOT.RooDataHist("dataDH","dataDH",ROOT.RooArgList(eSum),dataHist)
    dataDH.Print("V")
   ########
    #draw the toy & pdf
    ct=ROOT.TCanvas("ct")
    frame=eSum.frame()
#    ROOT.gPad.SetLogy()
    dataDH.plotOn(frame)

    fitResult=totalPdf.fitTo(dataDH,ROOT.RooFit.Extended(),ROOT.RooFit.Range(0.5,maxE),ROOT.RooFit.Save(True))
#    fitResult=totalPdf.fitTo(dataDH,ROOT.RooFit.Extended())
    totalPdf.plotOn(frame)
    radPdf.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Normalization(nRad.getVal()/dataDH.numEntries(),0))
    frame.Draw()
    ct.SaveAs("radBHFit.pdf")

if __name__ == "__main__":
    main()
