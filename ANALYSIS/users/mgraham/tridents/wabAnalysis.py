#!/usr/bin/python

#
# @file tridentAnalysis_pass4.py
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
from  histograms import myHistograms

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
myhist=myHistograms()     #make this global because I am lazy and a bad programmer
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

def trkMatchAndFiducial(trk) :
    if trk.getClusters().GetEntries() == 0 : return False
    trkCluster=trk.getClusters().First()    
    if not myHistograms.inSuperFiducialRegion(trkCluster.getPosition()[0],trkCluster.getPosition()[1]) : return False
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
        myhist.wabESum.Fill(eleEnergy+potentialWABCluster.getEnergy())
        myhist.wabPredictedVsMeasuredE.Fill(potentialWABCluster.getEnergy(),projPhotonEnergy)
        projPhotonXPosition=potentialWABCluster.getPosition()[2]*math.tan(projPhotonPhi+beamAngle)
        projPhotonYPosition=potentialWABCluster.getPosition()[2]*math.tan(projPhotonTheta)
        myhist.wabDeltaX.Fill( potentialWABCluster.getPosition()[0]-projPhotonXPosition)
        myhist.wabDeltaY.Fill( potentialWABCluster.getPosition()[1]-projPhotonYPosition)
        myhist.wabPredictedVsMeasuredX.Fill( potentialWABCluster.getPosition()[0],projPhotonXPosition)
        myhist.wabPredictedVsMeasuredY.Fill( potentialWABCluster.getPosition()[1],projPhotonYPosition)
        
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
        print  str(cl_impact_angleTop)+'   '+str(cl_impact_angleBottom)
        coplanarity=  cl_impact_angleBottom -  cl_impact_angleTop  
        myhist.wabCoplanarity.Fill(coplanarity)
        myhist.wabCoplanarityVsESum.Fill(eleEnergy+potentialWABCluster.getEnergy(),coplanarity)
    return None
    

#------------------#

#------------#
#--- Main ---#
#------------#

def main():
    # Parse all command line arguments using the argparse module.
    parser = argparse.ArgumentParser(description='PyRoot analysis demostrating the us of a DST.')
    parser.add_argument("dst_file",  help="ROOT DST file to process")
    parser.add_argument("-o", "--output",  help="Name of output pdf file")
    parser.add_argument("-m", "--mc",  help="is MonteCarlo")
    parser.add_argument("-p", "--pulser",  help="is Pulser")
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
    v0PzMax=1.2
    v0PzMin=0.55
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
    beamCut=0.8
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
    trackKiller=False
    tkThreshold=0.5 #GeV, below this start killing tracks
    tkThreshEff=1.0
    tkLowPoint=0.20
    tkLowPointEff=0.40
#    tkSlope=2.6 
#    tkIntercept=-0.04
    #calculate tkSlope and Intercept   
    tkSlope=(tkThreshEff-tkLowPointEff)/(tkThreshold-tkLowPoint)
    tkIntercept=tkThreshEff-tkSlope*tkThreshold

##############
    requireECalMatch = True
    requireECalFiducial = False
    requireECalSuperFiducial = True
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


    if 1==0 : 
        extraElectronProb=0.0
        dataNele=170.0;
        btNele=1.4;
        hf=ROOT.TFile("OutputHistograms/Data/hps_005772_pass6_useGBL_ECalMatch_SuperFiducialCut.root")
        hfMC=ROOT.TFile("OutputHistograms/MC/beam-tri_HPS-EngRun2015-Nominal-v4-4_pass6_useGBL_ECalMatch_SuperFiducialCut.root")
        pele=ROOT.RooRealVar("pele","pele",0,1)
        peleHist=hf.Get("raweleMom")
        peleMCHist=hfMC.Get("raweleMom")
        peleHist.Scale(1/dataNele)
        peleMCHist.Scale(1/btNele)
        peleHist.Add(peleMCHist,-1.0)  #subtract the MC from the data to get the distribution of extra tracks...this is cheating!
        for i in xrange(0,peleHist.GetNbinsX()) :
            print "Electron Momentum bin i = " +str( peleHist.GetBinContent(i) )
            if peleHist.GetBinContent(i) <0 :
                peleHist.SetBinContent(i,0)
        peleHist.Print("V")
        peleDH=RooDataHist("peleDH","peleDH",ROOT.RooArgList(pele),peleHist)
        peleDH.Print("V")
        extraElectronPdf=RooHistPdf("extraElectronPdf","extraElectronPdf",ROOT.RooArgSet(pele),peleDH)
        print 'pdf is made...printing info' 
        extraElectronPdf.Print("V")
        #    if isMC and random.random()<extraElectronProb : 
        #add an extra electron based on electron momentum
        print 'generating events' 
        newElePData=extraElectronPdf.generate(ROOT.RooArgSet(pele),1000000.0,True, False)
        newElePData.Print("V")
    
    seedCnt=0
    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
                 
        # Print the event number every 500 events
        if (entry+1)%10000 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
        if not hps_event.isPair1Trigger() and not isMC and not isPulser: continue
        nEvents+=1
        addFakeEle=False
        if 1==0 :
            if isMC and random.random()<extraElectronProb : 
        #add an extra electron based on electron momentum
                addFakeEle=True
                newEleP=newElePData.get(seedCnt).find("pele").getVal()
                seedCnt=seedCnt+1
                #            print 'Inserting an electron with momentum = '+str(newEleP)
                #            newEleCluster=hps_event.addEcalCluster();
                #            newEleTrack=hps_event.addTrack();
                #            print 'numbe of HpsParticles before = '+str(hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE))
                #            newEle=hps_event.addParticle(HpsParticle.FINAL_STATE_PARTICLE)
                #            print 'numbe of HpsParticles after = '+str(hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE))
                newEle=HpsParticle()
                newEle.setCharge(-1)
                newEle.setPDG(11)
                newEle.setEnergy(newEleP)
                sign=1
                if random.random()<0.5 : 
                    sign=-1
                newEleMom=[math.sin(0.03)*newEleP,sign*math.sin(0.04)*newEleP,math.cos(0.04)*newEleP]
                newEle.setMomentum(np.array(newEleMom))
            #fake track info
                newEleTrack=SvtTrack()
                newEleTrack.setTrackParameters(0.0,0.03,0.0001,sign*0.04,0.0)
                newEleTrack.setTrackTime(40.0)
                newEleTrack.setParticle(newEle)
                newEleTrack.setChi2(3.0)
                newEleTrack.setPositionAtEcal(np.array([300.0,sign*50.0,1350.0]))
            #fake cluster info
                newEleCluster=EcalCluster()
                newEleCluster.setEnergy(newEleP)
                foobar=[300.0,sign*50.0,1350.0]
                newEleCluster.setPosition(np.array(foobar,dtype='float32'))
                newEle.addTrack(newEleTrack)
                newEle.addCluster(newEleCluster)
#            print 'fake electron cluster x ' + str(newEle.getClusters().First().getPosition()[0])            
                                                                           

        # Loop over all tracks in the event
        npositrons=0
        n_tracks=0
        for track_n in xrange(0, hps_event.getNumberOfTracks()) :             
            track = hps_event.getTrack(track_n)
            if track is None : 
                continue
#            if useGBL and track.getParticle().getType()<32  : continue
#            if not useGBL and track.getParticle().getType()>31  : continue
            if trkMatchAndFiducial(track.getParticle()) and trkMomentum(track,minPCut,beamCut): # count only matched tracks in defined fiducial region
                n_tracks+=1
                if track.getCharge()>0 :
                    npositrons+=1
                    myhist.rawposMom.Fill(pMag(track.getMomentum()))
                else :
                    myhist.raweleMom.Fill(pMag(track.getMomentum()))
#                    findWABPair(track.getParticle(),hps_event)

        if addFakeEle :
            myhist.raweleMom.Fill(newEle.getEnergy())
            n_tracks=n_tracks+1
#        print "nTracks = "+str(n_tracks)+"; nPositrons = "+str(npositrons)
#        if n_tracks/2.0>nTrkMax : continue   #do this very dumb thing (divide by 2 to un-double count GBL tracks)
#        if n_tracks/2.0<2:  continue        
        myhist.nTrk.Fill(n_tracks);
        myhist.nPos.Fill(npositrons);
        myhist.nEle.Fill(n_tracks-npositrons);
        myhist.nClust.Fill(hps_event.getNumberOfEcalClusters())

        if n_tracks>nTrkMax : continue  
        if n_tracks<nTrkMin:  continue        
        if npositrons<1 or npositrons>nPosMax : continue
        nPassBasicCuts+=1
#        print "passed basic cuts"
        candidateList=[]
        bestCandidate=-99
        nCandidate=0
        # loop over all v0 candidates...
        for uc_index in xrange(0, hps_event.getNumberOfParticles(HpsParticle.UC_V0_CANDIDATE)):
            particle = hps_event.getParticle(HpsParticle.UC_V0_CANDIDATE, uc_index)
            if useGBL and  particle.getType()<32  : continue
            if not useGBL and  particle.getType()>31  : continue
#            print "found one..."
            vchi2=particle.getVertexFitChi2();
            vposition=particle.getVertexPosition();
            vmomentum=particle.getMomentum();
            if vchi2>v0Chi2 :  continue
            # use the measured sum of momentum 
#            if vmomentum[2]>v0PzMax : continue
#            if vmomentum[2]<v0PzMin : continue
             #recon'ed vertex position cuts
            if abs(vposition[0])>v0VxMax : continue
            if abs(vposition[1])>v0VyMax :continue

#            if abs(vposition[2])>v0VzMax :continue
            # Only look at particles that have two daugther particles...
            daughter_particles = particle.getParticles()
            if daughter_particles.GetSize() != 2 : continue
            # Only look at particles that are composed of e+e- pairs
            if daughter_particles.At(0).getCharge()*daughter_particles.At(1).getCharge() > 0 : continue
#            print "Passed daughter number cuts"

            electron =  daughter_particles.At(0)
            positron =  daughter_particles.At(1)
            
            if daughter_particles.At(0).getCharge()>0:
                electron =  daughter_particles.At(1)
                positron =  daughter_particles.At(0)

            pEle=electron.getMomentum()
            pPos=positron.getMomentum()

            v0Sum=pMag(pSum(pEle,pPos))
            #total momentum sum cuts
            if v0Sum>v0PzMax : continue
            if v0Sum<v0PzMin : continue
            nPassV0Cuts+=1
            print "Passed v0 cuts"
#############   tracking cuts
            #momentum cuts...get rid of very soft or very hard tracks
            if pMag(pEle)>beamCut or pMag(pPos)>beamCut : continue
            if pMag(pEle)<minPCut or pMag(pPos)<minPCut : continue   
            #top+bottom requirement
            if pEle[1]*pPos[1]>0 : continue

            print 'looking at tracks now' 
            print len(electron.getTracks())
            
            if  len(electron.getTracks()) == 0 or  len(positron.getTracks()) == 0: continue
            eleTrk=electron.getTracks().At(0)
            posTrk=positron.getTracks().At(0)
            if eleTrk is None or posTrk is None : continue
            eleTrk.Print("v")
            #track timing
            if eleTrk.getTrackTime() - posTrk.getTrackTime()> trkDeltaT :
                continue
            #track slope (if any cut)
            if abs(eleTrk.getTanLambda())<slopeCut or abs(posTrk.getTanLambda())<slopeCut :
                continue
            print 'satisfied timing cuts...'
            ##############
            # track killer part
            if isMC and trackKiller : 
                if pMag(pEle) <tkThreshold : #electron
                    tkEff=tkSlope*pMag(pEle)+tkIntercept 
                    if random.random()>tkEff  :
                        continue
                elif random.random()>tkThreshEff :  #allow for a flat killer above threshold
                    continue
                if pMag(pPos) <tkThreshold :   # positron
                    tkEff=tkSlope*pMag(pPos)+tkIntercept 
                    if random.random()>tkEff  :
                        continue
                elif random.random()>tkThreshEff : #allow for a flat killer above threshold
                    continue
            #  end of track killer
            ##############
            nPassTrkCuts+=1

            ##############
            #   ECAL matching and timing cuts...also fiducial region cuts...
            if requireECalMatch: 
                if positron.getClusters().GetEntries() == 0 :
                    continue
                if electron.getClusters().GetEntries() == 0 :
                    continue
                posCluster=positron.getClusters().First()
                eleCluster=electron.getClusters().First()
                
                if eleCluster.getClusterTime()- posCluster.getClusterTime() > cluDeltaT:
                    continue
                
                if eleTrk.getTrackTime() - eleCluster.getClusterTime()+43.5 > cluTrkDeltaT : 
                    continue

                if posTrk.getTrackTime() - posCluster.getClusterTime()+43.5 > cluTrkDeltaT : 
                    continue
                
                if requireECalFiducial:
                    #ANTI-fiducial cut
                    #                    if  myhist.inFiducialRegion(posCluster.getPosition()[0],posCluster.getPosition()[1]) :
                    #                        continue
                    #                    if  myhist.inFiducialRegion(eleCluster.getPosition()[0],eleCluster.getPosition()[1]) :
                    #                        continue
                    #Fiducial cut
                    if not myhist.inFiducialRegion(posCluster.getPosition()[0],posCluster.getPosition()[1]) :
                        continue
                    if not myhist.inFiducialRegion(eleCluster.getPosition()[0],eleCluster.getPosition()[1]) :
                        continue
                if requireECalSuperFiducial :
                    if not myhist.inSuperFiducialRegion(posCluster.getPosition()[0],posCluster.getPosition()[1]) :
                        continue
                    if not myhist.inSuperFiducialRegion(eleCluster.getPosition()[0],eleCluster.getPosition()[1]) :
                        continue
            nPassECalMatch+=1
            ##############
            #Passed the cuts..append the candidate index
            findWABPair(electron,hps_event)
            candidateList.append(uc_index)
      

        numCands=len(candidateList)
        if addFakeEle :
            for track_n in xrange(0, hps_event.getNumberOfTracks()) :             
                track = hps_event.getTrack(track_n)
                if track is None : 
                    continue
                if trkMatchAndFiducial(track.getParticle()) and trkMomentum(track,minPCut,beamCut) and track.getCharge>0 and newEle.getMomentum()[1]*track.getMomentum()[1]<0: # get positron in fudicial region; make sure it's in opposite quadrant
                    myhist.eSum.Fill(newEle.getEnergy()+pMag(track.getMomentum()))
                    numCands+=1
                    if len(candidateList) == 0 : 
                        print 'made a new trident event' 
                        nFakeTri+=1
                    
        myhist.nCand.Fill(numCands)
      
        #########################        
        #   found some candidates...lets fill plots...
        #########################        
        for index in range(0,len(candidateList)) :
            particle = hps_event.getParticle(HpsParticle.TC_V0_CANDIDATE, candidateList[index])
            myhist.fillCandidateHistograms(particle)
            myhist.nTrkCand.Fill(n_tracks);
            myhist.nPosCand.Fill(npositrons);
            myhist.nEleCand.Fill(n_tracks-npositrons);
            myhist.nClustCand.Fill(hps_event.getNumberOfEcalClusters())
            

#    if(nPassTrkCuts>0): 
    myhist.saveHistograms(output_file)   

    print "******************************************************************************************"
    print "Number of Events:\t\t",nEvents,"\t\t\t",float(nEvents)/nEvents,"\t\t\t",float(nEvents)/nEvents
    print "N(particle) Cuts:\t\t",nPassBasicCuts,"\t\t\t",float(nPassBasicCuts)/nEvents,"\t\t\t",float(nPassBasicCuts)/nEvents
    print "V0 Vertex   Cuts:\t\t",nPassV0Cuts,"\t\t\t",float(nPassV0Cuts)/nPassBasicCuts,"\t\t\t",float(nPassV0Cuts)/nEvents
    print "Tracking    Cuts:\t\t",nPassTrkCuts,"\t\t\t",float(nPassTrkCuts)/nPassV0Cuts,"\t\t\t",float(nPassTrkCuts)/nEvents
    print "ECal Match  Cuts:\t\t",nPassECalMatch,"\t\t\t",float(nPassECalMatch)/nPassTrkCuts,"\t\t\t",float(nPassECalMatch)/nEvents

    print "Number of Fake Events Added:  \t\t",nFakeTri,"\t\t\t",float(nFakeTri)/nPassECalMatch
                      
#            for(int i=0i<n_svt_hitsi++){
#                int layer = svt_hits_layer[i]
#                if(svt_hits_z[i]<0)
#                tHitBot[layer].Fill(svt_hits_time[i])
#                else
#                tHitTop[layer].Fill(svt_hits_time[i])         
#                }

if __name__ == "__main__":
    main()



