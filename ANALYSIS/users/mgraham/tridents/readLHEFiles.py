import sys
import shutil
import re
import string
import os
import glob
import array
from subprocess import Popen, PIPE
from ROOT import TLorentzVector, TH1, TH2
import gzip
from  histograms import myHistograms

me=0.000000511 #kev

def doSomeGoodStuff(pE,pP,pR): 
    
    print "good stuff" 

        
def getFourMomentum(mcParticle):
    p=TLorentzVector(0,0,0,me)
    p.SetPx(float(mcParticle[6]))
    p.SetPy(float(mcParticle[7]))
    p.SetPz(float(mcParticle[8]))
    p.SetE(float(mcParticle[9]))
#    p.Print()
    return p 

def main(): 
    global me
    chargeToLumi=2.75541e-14 #1/nb
    nCtoEle=6.25e9
    lhe_dir='/nfs/slac/g/hps3/data/engrun2015/mc_1pt05/lhe'
#    evt_type='RAD'
#    file_pre='RADv1_'
    evt_type='tritrig'
    file_pre='tritrigv1_'
    file_post='.lhe.gz'
    out_dir='OutputHistograms/Truth'
    isFullTri=False
    
    myhist=myHistograms()
    
    sumXS=0
    nfile=0
    indir=lhe_dir+"/"+evt_type

    files = glob.glob(indir+"/*49*")

    for lheFile in files :
        print lheFile
        inEvent=False
        foundEle=False
        foundPos=False
        foundRec=False
        with gzip.open(lheFile,"r") as tmp:        
            lines = tmp.readlines()
            for line in lines:            
                line=line.strip()
            #find the integrated cross section
                matchMe=re.search('Integrated.*(\.\d*E\+\d*)', line)
                if matchMe is not None:  
                    print 'Found cross-section = ' +matchMe.group(1)
                    nfile+=1
                    xs=float(matchMe.group(1))
                    sumXS+=xs
            #find the event            
                matchMe=re.search('<event>',line)            
                if matchMe is not None: 
                    inEvent=True
                    pEle=TLorentzVector(0,0,0,me)
                    pPos=TLorentzVector(0,0,0,me)
                    pRec=TLorentzVector(0,0,0,me)
            #find the electron from virtual photon 
                mcParticle=line.split()
                if len(mcParticle)== 13 and inEvent : 
                    if float(mcParticle[0])== 11 and float(mcParticle[1])==1: 
                        if foundRec and not foundEle:  # we've already found the recoil electron!  this must be the full trident MC...fill pEle
                            pEle=getFourMomentum(mcParticle)
                            if pEle.E()!= me :
                                foundEle = True                                            
                        else  :
                            pRec=getFourMomentum(mcParticle)
                            if pRec.E()!= me :
                                foundRec = True                            
                    elif float(mcParticle[0])== 611 :
                        pEle=getFourMomentum(mcParticle)
                        if pEle.E()!= me :
                            foundEle = True
                    elif float(mcParticle[0])== -611 or  float(mcParticle[0])== -11: 
                        pPos=getFourMomentum(mcParticle)
                        if pPos.E()!= me :
                            foundPos = True
            #find the end of event            
                matchMe=re.search('</event>',line)            
                if matchMe is not None: 
                    inEvent=False
                    if foundPos and foundEle and foundRec : #found everything...now do something
                        if  myhist.truthAcceptanceCuts(pEle,pPos) : 
                            myhist.fillHistograms(pEle,pPos,pRec)
                        #Check if the "recoil" electron-positron passes 
                        if  myhist.truthAcceptanceCuts(pRec,pPos) : 
                            myhist.fillHistograms(pRec,pPos,pEle)
                            
#                        doSomeGoodStuff(pEle,pPos,pRec)
                    else :
                        print "Didn't find all final states!!!"
                #reset everything for next event
                    foundEle=False
                    foundPos=False
                    foundRec=False

    myhist.saveHistograms(out_dir+"/"+file_pre+"truth.root")
    print 'Average Generated Cross-Section: ' +str(sumXS/nfile)+' pb' 
            
if __name__ == "__main__":
    main()

