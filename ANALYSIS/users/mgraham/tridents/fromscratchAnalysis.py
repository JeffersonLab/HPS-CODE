#!/usr/bin/python

#
# @file tridentAnalysis.py
# @section purpose:
#       A PyRoot analysis for the DST selecting trident events and making some plots
# @author Matt Graham <mgraham@slac.stanford.edu>
#  based on Omar Moreno's example <omoreno1@ucsc.edu>
#         Santa Cruz Institute for Particle Physics
#         University of California, Santa Cruz
# @date March 29, 2013
#

#---------------#
#--- imports ---#
#---------------#
import sys
import math
import argparse
import os
import numpy as np
import random
from  utilsAndPlots import utilsAndPlots

# Load the HpsEvent library.  In this example, this is done by finding the
# path to the HpsEvent shared library via the environmental variable
# HPS_DST_PATH.  The HPS_DST_PATH environmental variable points to the
# location of the build directory containing all binaries and libraries.
# In general, the location of the library can be anywhere a user wants it
# to be as long as the proper path is specified. 
if os.getenv('HPS_DST_PATH') is None: 
    print "[ HPS ANALYSIS ]: Error! Environmental variable HPS_DST_HOME is not set."
    print "\n[ HPS ANALYSIS ]: Exiting ..."
    sys.exit(2)

hps_dst_path = os.environ['HPS_DST_PATH']
hps_dst_path += "/build/lib/libHpsEvent.so"
print "Loading HpsEvent Library from "+hps_dst_path
# Load the library in ROOT
import ROOT
ROOT.gSystem.Load(hps_dst_path)

# import the modules used by HpsEvent i.e. HpsEvent, 
# SvtTrack, EcalCluster ...
from ROOT import HpsEvent, SvtTrack, GblTrack, EcalCluster, EcalHit, TChain, TTree, HpsParticle
from ROOT import RooHistPdf, RooDataHist

beamEnergy=1.05 #GeV
beamAngle = 0.0305 #30.5 mrad (nominally)
phot_nom_x = 42.52  #nominal photon position (px=0)
myhist=utilsAndPlots(beamEnergy)     #make this global because I am lazy and a bad programmer
#ROOT.PyConfig.IgnoreCommandLineOptions = True

#-----------------#
#--- Functions ---#
#-----------------#

def setupCanvas(canvas):
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetBorderSize(0)
    canvas.SetFrameFillColor(0)
    canvas.SetFrameBorderMode(0)

def getEffTH1(hfile, hname) : 
    print 'Getting Efficiency Graph...converting to TH1'
    effGraph=hfile.Get(hname)
    xmin=effGraph.GetXaxis().GetXmin()
    xmax=effGraph.GetXaxis().GetXmax()
    nbins=effGraph.GetN()
    x=ROOT.Double(0.0)
    y=ROOT.Double(0.0)
    print nbins
    effHist=ROOT.TH1D(effGraph.GetName(),effGraph.GetTitle(),nbins,xmin,xmax)
    for i in range(0,nbins) : 
        effGraph.GetPoint(i,x,y)
        print str(x)+' ' +str(y)        
        effHist.SetBinContent(i,y)    

    return effHist



def getEffTH2(hfile, hname) : 
    print 'Getting efficiency TH2 '+hname    
    effHist=hfile.Get(hname)
    return effHist



def setup1DHistogram(histo, x_axis_title):
    histo.SetStats(0)
    histo.GetXaxis().SetTitle(x_axis_title)
    histo.GetXaxis().SetTitleSize(0.03)
    histo.GetXaxis().SetLabelSize(0.03)
    histo.GetYaxis().SetTitleSize(0.03)
    histo.GetYaxis().SetLabelSize(0.03)

def setup2DHistogram(histo, x_axis_title, y_axis_title):
    histo.GetYaxis().SetTitle(y_axis_title)
    setup1DHistogram(histo, x_axis_title)

def pMag(p1) :
    return  math.sqrt(p1[0]*p1[0] + p1[1]*p1[1] + p1[2]*p1[2])

def pSum(p1,p2) :
    sum= [p1[0]+p2[0],p1[1]+p2[1],p1[2]+p2[2]]
    return sum 

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    stolen from http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
    """
    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


def getPolarAngle(p): 
    pt = math.sqrt(p[0]*p[0]+p[1]*p[1])
    pmag=pMag(p)
    return math.asin(pt/pmag)

def trkMomentum(trk,pmin,pmax) :
    if pMag(trk.getMomentum())>pmax    : return False
    if pMag(trk.getMomentum())<pmin    : return False
    return True

def trkMatchAndFiducial(trk, requireSuperFiducial) :
    if trk.getClusters().GetEntries() == 0 : return False
    trkCluster=trk.getClusters().First()    
    if requireSuperFiducial and not utilsAndPlots.inSuperFiducialRegion(trkCluster.getPosition()[0],trkCluster.getPosition()[1]) : return False
    return True

def checkClusterFiducialAndTiming(fspCl, requireSuperFiducial) : 
    if fspCl.getClusters().GetEntries()==0 : return False 
#    print 'found a cluster' 
    cl= fspCl.getClusters().First()
    if requireSuperFiducial and not utilsAndPlots.inSuperFiducialRegion(cl.getPosition()[0],cl.getPosition()[1]) : return False
#    print 'pass super fiducial' 
    if not myhist.clusterTimingCut(cl.getClusterTime()) : return False
#    print 'passed all cuts' 
    return True


#given an e+e- pair, try to find a recoil electron; return the recoil track if found
def findRecoilElectron(v0,particleList) :
    return None

#given an electron particle, see if the electron+ unassociated photon looks like a WAB pair
def findWABPair(electron,  hps_event): 
    radian = ROOT.TMath.RadToDeg()
    eleEnergy=pMag(electron.getMomentum())
    elePhi=electron.getTracks().At(0).getPhi0() - beamAngle #x angle - beam angle
    eleSlope=electron.getTracks().At(0).getTanLambda() #sin(y angle)
    print beamEnergy
    projPhotonEnergy=beamEnergy-eleEnergy
    projPhotonPhi = math.asin(-math.sin(elePhi)*eleEnergy/projPhotonEnergy)
    projPhotonTheta = math.asin(-eleSlope*eleEnergy/projPhotonEnergy)
    if electron.getClusters().GetEntries == 0 : 
        return 
    eleCluster= electron.getClusters().First()
#    print str(projPhotonPhi)+" "+str(projPhotonTheta)
    for uc_index in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)):
        particle = hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE, uc_index)  
#        print 'Found Particle'
        if particle.getTracks().GetEntries()>0 : continue # no tracks!
#        print 'Found Particle with No Tracks'
        if particle.getClusters().GetEntries() == 0 : continue # yes clusters!        
#        print 'Found Cluster'
        potentialWABCluster=particle.getClusters().First()
        if potentialWABCluster.getPosition()[1]*eleSlope>0 : continue  #make sure they are on the opposite sides
#        print 'Found Cluster in right half!!!'
#        myhist.wabESum.Fill(eleEnergy+potentialWABCluster.getEnergy())
#        myhist.wabPredictedVsMeasuredE.Fill(potentialWABCluster.getEnergy(),projPhotonEnergy)
        projPhotonXPosition=potentialWABCluster.getPosition()[2]*math.tan(projPhotonPhi+beamAngle)
        projPhotonYPosition=potentialWABCluster.getPosition()[2]*math.tan(projPhotonTheta)
#        myhist.wabDeltaX.Fill( potentialWABCluster.getPosition()[0]-projPhotonXPosition)
#        myhist.wabDeltaY.Fill( potentialWABCluster.getPosition()[1]-projPhotonYPosition)
#        myhist.wabPredictedVsMeasuredX.Fill( potentialWABCluster.getPosition()[0],projPhotonXPosition)
#        myhist.wabPredictedVsMeasuredY.Fill( potentialWABCluster.getPosition()[1],projPhotonYPosition)
        
        if eleCluster.getPosition()[1] >0 : 
            topX=eleCluster.getPosition()[0]
            topY=eleCluster.getPosition()[1]
            botX=potentialWABCluster.getPosition()[0]
            botY=potentialWABCluster.getPosition()[1]
        else : 
            botX=eleCluster.getPosition()[0]
            botY=eleCluster.getPosition()[1]
            topX=potentialWABCluster.getPosition()[0]
            topY=potentialWABCluster.getPosition()[1]
            
        cl_impact_angleTop = math.atan2(topY, topX - phot_nom_x)*radian;
        cl_impact_angleBottom = math.atan2(botY,botX - phot_nom_x)*radian;
        if cl_impact_angleTop < 0. :
            cl_impact_angleTop = cl_impact_angleTop + 360. 
        if cl_impact_angleBottom < 0. :
            cl_impact_angleBottom = cl_impact_angleBottom + 360.
#        print  str(cl_impact_angleTop)+'   '+str(cl_impact_angleBottom)
        coplanarity=  cl_impact_angleBottom -  cl_impact_angleTop  
#        myhist.wabCoplanarity.Fill(coplanarity)
#        myhist.wabCoplanarityVsESum.Fill(eleEnergy+potentialWABCluster.getEnergy(),coplanarity)
    return None
    

#------------------#

#------------#
#--- Main ---#
#------------#

def main():
    global beamEnergy
    # Parse all command line arguments using the argparse module.
    parser = argparse.ArgumentParser(description='PyRoot analysis demostrating the us of a DST.')
    parser.add_argument("dst_file",  help="ROOT DST file to process")
    parser.add_argument("-o", "--output",  help="Name of output pdf file")
    parser.add_argument("-m", "--mc",  help="is MonteCarlo")
    parser.add_argument("-p", "--pulser",  help="is Pulser")
    parser.add_argument("-e","--energy",help="beam energy")
    args = parser.parse_args()

    # If an output file name was not specified, set a default name and warn
    # the user 
    if args.output:
        output_file = args.output
    else: 
        output_file = "analysis_output.root"
        print "[ HPS ANALYSIS ]: An output file name was not specified. Setting the name to " 
        print output_file


    print "[ HPS ANALYSIS ]:  Output file is "+output_file
    isMC=False
    if args.mc:
        print  "[ HPS ANALYSIS ]: Setting to run as MC"
        isMC=True


    isPulser=False
    if args.pulser:
        print  "[ HPS ANALYSIS ]: Setting to run from a pulser file"
        isPulser=True

#    if args.energy : 
#        print 'Setting beam energy to '+args.energy
#       beamEnergy=float(args.energy)
#        myhist.setEnergyScales(beamEnergy)


#################################
#       Event Selection
################################
#clean up event first
#### nominal selection
    nTrkMax=10
    nTrkMin=2
    nPosMax=3
######  two tracks (e+/e-) exactly
#    nTrkMax=2
#    nTrkMin=2
#    nPosMax=1
###### more than 1 electron
#    nTrkMax=10
#    nTrkMin=3
#    nPosMax=1
###################
    #v0 cuts   
    v0Chi2=10
    #ESum -- full region
    v0PzMax=1.2*beamEnergy
    v0PzMin=0.55*beamEnergy
    #ESum -- Radiative region
#    v0PzMax=1.2
#    v0PzMin=0.80

    v0PyMax=0.2 #absolute value
    v0PxMax=0.2 #absolute value
    v0VzMax=25.0# mm from target
    v0VyMax=1.0# mm from target
    v0VxMax=2.0# mm from target
 #  track quality cuts
    trkChi2=10
    beamCut=0.8*beamEnergy
    minPCut=0.05
    trkPyMax=0.2
    trkPxMax=0.2
#    slopeCut=0.03
    slopeCut=0.0
    trkDeltaT=4#ns
    cluDeltaT=2#ns
    cluTrkDeltaT=4#ns
##############
#  ESum slices; upper limits    
    nSlicesESum=5 
    esumMin=0.55
    esumMax=1.2
    sliceSizeESum=0.1 #100MeV starting at esumMin
##############
    trackKiller=True
    killInMomentum=False
    killInClusterPosition=True
#    tkThreshold=0.5 #GeV, below this start killing tracks
#    tkThreshEff=1.0
#    tkLowPoint=0.20
#    tkLowPointEff=0.40
#    tkSlope=2.6 
#    tkIntercept=-0.04
    #calculate tkSlope and Intercept   
#    tkSlope=(tkThreshEff-tkLowPointEff)/(tkThreshold-tkLowPoint)
#    tkIntercept=tkThreshEff-tkSlope*tkThreshold
#    effFileName='/u/br/mgraham/hps-analysis/TrackEfficiency/cop180_EfficiencyResults.root'
#    effDataName='h_Ecl_hps_005772_eleEff'
#    effMCName='h_Ecl_tritrig-NOSUMCUT_HPS-EngRun2015-Nominal-v5-0_eleEff'


    effFileName='/u/br/mgraham/hps-analysis/TrackEfficiency/cop180_midESum_TwoD-EfficiencyResults.root'
    effDataName='h_XvsY_hps_005772_eleEff'
    effMCName='h_XvsY_tritrig-NOSUMCUT_HPS-EngRun2015-Nominal-v5-0_eleEff'


    effFile=ROOT.TFile(effFileName)
    print 'Getting data efficiency' 
#    effData=getEffTH1(effFile,effDataName)
#    effMC=getEffTH1(effFile,effMCName)
    effData=getEffTH2(effFile,effDataName)
    effMC=getEffTH2(effFile,effMCName)
    effData.Print("v")
    effMC.Print("v")
    effData.Divide(effMC)  # this will be the killing factor
    effData.Print("V")
#    for i in range(0,effData.GetNbinsX()) : 
#        print 'efficiency ratio '+str(i)+'   '+str(effData.GetBinCenter(i))+' '+str(effData.GetBinContent(i))
##############
    requireECalMatch = True
    requireECalFiducial = False
    requireECalSuperFiducial = False
    requireECalTimingCoincidence = True
    useGBL=True


     # Open the ROOT file
    #    root_file = ROOT.TFile(str(args.dst_file))
    # Get the TTree "HPS_EVENT" containing the HpsEvent branch and all
    # other colletions
    #    tree = root_file.Get("HPS_Event")
    #use a TChain
    print "[ HPS ANALYSIS ]: Reading in root chain from "+args.dst_file
    tree=ROOT.TChain("HPS_Event")
    tree.Add(str(args.dst_file)+"*")    
    # Create an HpsEvent object in order to read the TClonesArray 
    # collections
    hps_event = HpsEvent()

    b_hps_event = tree.SetBranchAddress("Event", ROOT.AddressOf(hps_event))

    #--- Analysis ---#
    #----------------#

    #counters
    nEvents=0;
    nPassBasicCuts=0;
    nPassV0Cuts=0;
    nPassTrkCuts=0;
    nPassNCand=0
    nPassECalMatch=0;
    nFakeTri=0
    
    seedCnt=0
    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
                 
        nEpEmTB=0
        nEpEpTB=0
        nEmEmTB=0
        nEpEmTT=0
        nEpEpTT=0
        nEmEmTT=0
        nEpEmBB=0
        nEpEpBB=0
        nEmEmBB=0
        nEpGamTB=0
        nEpGamTT=0
        nEpGamBB=0
        nEmGamTB=0
        nEmGamTT=0
        nEmGamBB=0    
#        print "Next event..."
        # Print the event number every 500 events
        if (entry+1)%100 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
        if not hps_event.isPair1Trigger() and not isMC and not isPulser: continue
        nEvents+=1
      
    
        # Loop over all tracks in the event
        goodtrk=[]
        gamList=[]
        eleList=[]
        posList=[]
        for fsp_n in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)) :             
            fsp = hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE,fsp_n)
            if fsp.getType() == 0 :  #might be good photon 
                if not checkClusterFiducialAndTiming(fsp,requireECalSuperFiducial) :                     continue
                gamList.append(fsp)
            else : #maybe a good track? 
                if useGBL and  fsp.getType()<32  : continue
                if not useGBL and  fsp.getType()>31  : continue
                track=fsp.getTracks()[0]
                if track is None : continue #this shouldn't happen
                if requireECalMatch and not trkMatchAndFiducial(track.getParticle(),requireECalSuperFiducial) : continue
                if not trkMomentum(track,minPCut,beamCut):  continue
                if trackKiller and isMC and requireECalMatch: # use the ECAL cluster to do this!!! 
                    if killInMomentum : 
#                    p=pMag(fsp.getMomentum())
                        p=fsp.getEnergy()
                        bin=effData.FindBin(p)                    
                        tkEff=effData.GetBinContent(bin)
                        print str(p)+ ' '+str(bin)+' '+str(tkEff)
                        if random.random()>tkEff  :  #high ratio of efficiencies, this hardly  kills...low, kills a lot
                            print "REJECTING THIS TRACK!!! "+str(p)
                            continue
                    if killInClusterPosition:  
                        clEle=fsp.getClusters()[0]
                        clX=clEle.getPosition()[0]
                        clY=clEle.getPosition()[1]
                        if fsp.getCharge()<0 : 
                            bin=effData.FindBin(clX,clY)
                        else: 
                            bin=effData.FindBin(-clX+80,clY) # flip sign +80mm for positron side (this isn't strictly correct)!!!
                        tkEff=effData.GetBinContent(bin)
                        if random.random()>tkEff  and tkEff!=0.0:  
                            print str(clX)+ ' '+str(clY)+' '+str(bin)+' '+str(tkEff)
                            print "REJECTING THIS ELECTRON TRACK!!! "+str(clX)
                            continue

            # check to see if we already found this track
                if myhist.checkIfShared(goodtrk,fsp): 
#                    print 'fromscratch::now goodtrk is '+str(len(goodtrk))+' tracks long'
#                    for trk in goodtrk: 
#                        print len(trk.getTracks()[0].getSvtHits())
                    continue
            #otherwise this is a new track
                else : 
                    goodtrk.append(fsp)


        if len(goodtrk) > nTrkMax: continue # too many tracks

        for fsp in goodtrk :
            if fsp.getCharge() < 0 : 
                eleList.append(fsp)
            else : 
                posList.append(fsp)
                
        if len(posList) > nPosMax: continue # too many positrons!

#        print 'found '+str(len(goodtrk))+' tracks in this event'
#        print '\t\t\t   # electrons = ' +str(len(eleList))
#        print '\t\t\t   # positrons = ' +str(len(posList))
#        print '\t\t\t   # photons = ' +str(len(gamList))

#do analysis for e+e- pairs
        for pos in posList : 
            for ele in eleList: 
                if  requireECalTimingCoincidence and not myhist.clusterCoincidence(ele,pos) :
                    continue
                if ele.getMomentum()[1]*pos.getMomentum()[1] <0:
                    myhist.fillTwoBody(ele,pos,'EpEm','TB')
                elif ele.getMomentum()[1]>0 and pos.getMomentum()[1]>0:
                    myhist.fillTwoBody(ele,pos,'EpEm','TT')
                elif ele.getMomentum()[1]<0 and pos.getMomentum()[1]<0:
                    myhist.fillTwoBody(ele,pos,'EpEm','BB')
#do analysis for e-e- pairs
        for i in range(0,len(eleList)) : 
            ele1=eleList[i]
            for k in range(i+1,len(eleList)):
                ele2=eleList[k]                
                if  requireECalTimingCoincidence and not myhist.clusterCoincidence(ele1,ele2) :
                    continue
                if ele1.getMomentum()[1]*ele2.getMomentum()[1] <0:
                    myhist.fillTwoBody(ele1,ele2,'EmEm','TB')#potentially comes from WABs
                elif ele1.getMomentum()[1]>0 and ele2.getMomentum()[1]>0:
                    myhist.fillTwoBody(ele1,ele2,'EmEm','TT')
                elif ele1.getMomentum()[1]<0 and ele2.getMomentum()[1]<0:
                    myhist.fillTwoBody(ele1,ele2,'EmEm','BB')
#do analysis for e+e+ pairs
        for i in range(0,len(posList)) : 
            pos1=posList[i]
            for k in range(i+1,len(posList)):
                pos2=posList[k]                
                if  requireECalTimingCoincidence and not myhist.clusterCoincidence(pos1,pos2) :
                    continue
                if pos1.getMomentum()[1]*pos2.getMomentum()[1] <0:
                    myhist.fillTwoBody(pos1,pos2,'EpEp','TB')
                elif pos1.getMomentum()[1]>0 and pos2.getMomentum()[1]>0:
                    myhist.fillTwoBody(pos1,pos2,'EpEp','TT')
                elif pos1.getMomentum()[1]<0 and pos2.getMomentum()[1]<0:
                    myhist.fillTwoBody(pos1,pos2,'EpEp','BB')

#do analysis for e-gamma pairs 
        for ele in eleList : 
            for gam in gamList: 
                gamY=gam.getClusters().First().getPosition()[1]
                if  requireECalTimingCoincidence and not myhist.clusterCoincidence(ele,gam) :
                    continue
                if ele.getMomentum()[1]*gamY<0 : #(these could be WABS!)
                    myhist.fillTwoBody(ele,gam,'EmGam','TB')
                elif  ele.getMomentum()[1] >0 : 
                    myhist.fillTwoBody(ele,gam,'EmGam','TT')
                elif  ele.getMomentum()[1] <0 : 
                    myhist.fillTwoBody(ele,gam,'EmGam','BB')

#do analysis for e+gamma pairs ... these could be ???  
        for pos in posList : 
            for gam in gamList: 
                gamY=gam.getClusters().First().getPosition()[1]
                if  requireECalTimingCoincidence and not myhist.clusterCoincidence(pos,gam) :
                    continue
                if pos.getMomentum()[1]*gamY<0 : 
                    myhist.fillTwoBody(pos,gam,'EpGam','TB')
                elif  pos.getMomentum()[1] >0 : 
                    myhist.fillTwoBody(pos,gam,'EpGam','TT')
                elif  pos.getMomentum()[1] <0 : 
                    myhist.fillTwoBody(pos,gam,'EpGam','BB')

#do analysis for e+e-e- triplets...
        for pos in posList: 
            for i in range(0,len(eleList)) : 
                ele1=eleList[i]
                if  requireECalTimingCoincidence and not myhist.clusterCoincidence(ele1,pos) :
                    continue
                for k in range(i+1,len(eleList)):
                    ele2=eleList[k]                
                    if  requireECalTimingCoincidence and not myhist.clusterCoincidence(ele2,pos) :
                        continue
                    if pos.getMomentum()[1]>0 and ele1.getMomentum()[1]>0 and ele2.getMomentum()[1]>0  : 
                        myhist.fillThreeBody(pos,ele1,ele2,'EpEmEm','TTT')#all top?
                    elif ((pos.getMomentum()[1]>0 and ele1.getMomentum()[1]>0 and ele2.getMomentum()[1]<0)  or 
                          (pos.getMomentum()[1]<0 and ele1.getMomentum()[1]<0 and ele2.getMomentum()[1]>0)  or
                          (pos.getMomentum()[1]<0 and ele1.getMomentum()[1]>0 and ele2.getMomentum()[1]<0)  or
                          (pos.getMomentum()[1]>0 and ele1.getMomentum()[1]<0 and ele2.getMomentum()[1]>0) ): 
                        myhist.fillThreeBody(pos,ele1,ele2,'EpEmEm','TTB')#electrons on opposite halves...possible trident or WAB
                    elif ( (pos.getMomentum()[1]>0 and ele1.getMomentum()[1]<0 and ele2.getMomentum()[1]<0)  or 
                           (pos.getMomentum()[1]<0 and ele1.getMomentum()[1]>0 and ele2.getMomentum()[1]>0) ): 
                        myhist.fillThreeBody(pos,ele1,ele2,'EpEmEm','TBB')#electrons on same halves....possible trident (not WAB)
                    elif pos.getMomentum()[1]<0 and ele1.getMomentum()[1]<0 and ele2.getMomentum()[1]<0  : 
                        myhist.fillThreeBody(pos,ele1,ele2,'EpEmEm','BBB')#all bottom?

    myhist.saveHistograms(output_file)   

#    print "******************************************************************************************"
#    print "Number of Events:\t\t",nEvents,"\t\t\t",float(nEvents)/nEvents,"\t\t\t",float(nEvents)/nEvents
#    print "N(particle) Cuts:\t\t",nPassBasicCuts,"\t\t\t",float(nPassBasicCuts)/nEvents,"\t\t\t",float(nPassBasicC#uts)/nEvents
#    print "V0 Vertex   Cuts:\t\t",nPassV0Cuts,"\t\t\t",float(nPassV0Cuts)/nPassBasicCuts,"\t\t\t",float(nPassV0Cuts)/nEvents
#    print "Tracking    Cuts:\t\t",nPassTrkCuts,"\t\t\t",float(nPassTrkCuts)/nPassV0Cuts,"\t\t\t",float(nPassTrkCuts)/nEvents
#    print "ECal Match  Cuts:\t\t",nPassECalMatch,"\t\t\t",float(nPassECalMatch)/nPassTrkCuts,"\t\t\t",float(nPassECalMatch)/nEvents

#    print "Number of Fake Events Added:  \t\t",nFakeTri,"\t\t\t",float(nFakeTri)/nPassECalMatch
                      
#            for(int i=0i<n_svt_hitsi++){
#                int layer = svt_hits_layer[i]
#                if(svt_hits_z[i]<0)
#                tHitBot[layer].Fill(svt_hits_time[i])
#                else
#                tHitTop[layer].Fill(svt_hits_time[i])         
#                }

if __name__ == "__main__":
    main()



