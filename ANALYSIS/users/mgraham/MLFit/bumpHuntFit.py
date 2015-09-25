#---------------#
#--- imports ---#
#---------------#
import sys
import math
import argparse
import os
import ROOT
import re, array

def main():

    minMass=0.03
    maxMass=0.1
    stepSize=0.0025
    windowSize=0.01

    #dependent variable
    m=ROOT.RooRealVar("m","mass",0.0,0.1)
    deps=ROOT.RooArgSet(m)
    #yeilds 
    nSig=ROOT.RooRealVar("nSig","Number of Signal Events",0,-1000,100000)
#    nSig=ROOT.RooRealVar("nSig","Number of Signal Events",0)
    nBkg=ROOT.RooRealVar("nBkg","Number of Background Events",10000,-1000,10000000)

    #signal parameters
    gmean=ROOT.RooRealVar("gmean","Signal Gaussian Mean",0.07)
    gsigma=ROOT.RooRealVar("gsigma","Signal Gaussian Sigma",0.003)
    #signal PDF
    sigPdf=ROOT.RooGaussian("sigPdf","Signal Gaussian",m,gmean,gsigma)

    #background parameters
    p0=ROOT.RooRealVar("p0","Background p0",0.0,-10,2.0)
    p1=ROOT.RooRealVar("p1","Background p1",0.0,-2,2)
    p2=ROOT.RooRealVar("p2","Background p2",0.0,-2,2)
    #background PDF
#    bkgPdf=ROOT.RooPolynomial("bkgPdf","Background Polynomial",m,ROOT.RooArgList(p0,p1,p2),0)
#    bkgPdf=ROOT.RooPolynomial("bkgPdf","Background Polynomial",m,ROOT.RooArgList(p0,p1),0)
    bkgPdf=ROOT.RooChebychev("bkgPdf","Background Polynomial",m,ROOT.RooArgList(p0,p1,p2))
    
    #total PDF
    totalPdf=ROOT.RooAddPdf("totalPdf","Total PDF",ROOT.RooArgList(sigPdf,bkgPdf),ROOT.RooArgList(nSig,nBkg))

    #generate some toy data
    toyData=totalPdf.generate(deps,nSig.getVal()+nBkg.getVal())
    toyData.Print("V")

    #get the data histogram
    f=ROOT.TFile("./hps_005772+08242015.root")
    dataMassHist=f.Get("TridentMass")
    dataMassHist.Print("V")
    dataMassDH=ROOT.RooDataHist("dataMassDH","dataMassDH",ROOT.RooArgList(m),dataMassHist)
    dataMassDH.Print("V")
    ########
    #draw the toy & pdf
    ct=ROOT.TCanvas("ct")
    frame=m.frame()
    ROOT.gPad.SetLogy()
    dataMassDH.plotOn(frame)
    #fit to the data 
    i=0
    while minMass + windowSize < maxMass :        
        p0.setVal(0.0)
        p1.setVal(0.0)
        nSig.setVal(0.0)
        nBkg.setVal(1000.0)
        p2.setVal(0.0)
        gmean.setVal(minMass+windowSize/2.0)
        gsigma.setVal(gmean.getVal()*0.05)#5% resolution
        print "Setting mean to "+str(gmean.getVal())+"; setting sigma to "+str(gsigma.getVal())
        newPdf0=totalPdf.clone("newpdf"+str(i))
        fitResult=newPdf0.fitTo(dataMassDH,ROOT.RooFit.Extended(),ROOT.RooFit.Range(minMass,minMass+windowSize),ROOT.RooFit.Save(True))
        print  "Covariance Quality is "+str(fitResult.covQual())
        ct.cd()
        #        if fitResult.covQual() > 2: 
        newPdf0.plotOn(frame)
        
        cTemp=ROOT.TCanvas("cTemp")
        cTemp.cd()
        frameTemp=m.frame(minMass,minMass+windowSize)
        dataMassDH.plotOn(frameTemp)
        newPdf0.plotOn(frameTemp)
        sigPdf.plotOn(frameTemp,ROOT.RooFit.Normalization(100,NumEvent)
        frameTemp.Draw()
        cTemp.SaveAs("allFits/fit"+str(i)+".pdf")
        del cTemp
        del frameTemp
        minMass=minMass+stepSize
        i+=1

    #    toyData.plotOn(frame)
    ct.cd()
    frame.Draw()
    ct.SaveAs("foobar.pdf")
    print "Ok...done"    


if __name__ == "__main__":
    main()
