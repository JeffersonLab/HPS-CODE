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

beamEnergy=1.05 #GeV
beamAngle = 0.0305 #30.5 mrad (nominally)
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
    eleEnergy=pMag(electron.getMomentum())
    elePhi=electron.getTracks().At(0).getPhi0() - beamAngle #x angle - beam angle
    eleSlope=electron.getTracks().At(0).getTanLambda() #sin(y angle)
    projPhotonEnergy=beamEnergy-eleEnergy
    projPhotonPhi = math.asin(-math.sin(elePhi)*eleEnergy/projPhotonEnergy)
    projPhotonTheta = math.asin(-eleSlope*eleEnergy/projPhotonEnergy)
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
        myhist.wabPredictedVsMeasuredX.Fill( potentialWABCluster.getPosition()[0],projPhotonXPosition)
        myhist.wabPredictedVsMeasuredY.Fill( potentialWABCluster.getPosition()[1],projPhotonYPosition)
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
  

    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
        # Print the event number every 500 events
        if (entry+1)%10000 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
#        print str(hps_event.isPulserTrigger())+ ' ' +str(hps_event.isSingle1Trigger())
        if hps_event.isPulserTrigger() :
            print 'found pulser event' 
                
#        if not hps_event.isPair1Trigger() and not isMC: continue
#        if not hps_event.isPulserTrigger() and not isMC: continue
        nEvents+=1
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

        print "nTracks = "+str(n_tracks)+"; nPositrons = "+str(npositrons)
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


    myhist.saveHistograms(output_file)   

    print "******************************************************************************************"
#    print "Number of Events:\t\t",nEvents,"\t\t\t",float(nEvents)/nEvents,"\t\t\t",float(nEvents)/nEvents
#    print "N(particle) Cuts:\t\t",nPassBasicCuts,"\t\t\t",float(nPassBasicCuts)/nEvents,"\t\t\t",float(nPassBasicCuts)/nEvents
#    print "V0 Vertex   Cuts:\t\t",nPassV0Cuts,"\t\t\t",float(nPassV0Cuts)/nPassBasicCuts,"\t\t\t",float(nPassV0Cuts)/nEvents
#    print "Tracking    Cuts:\t\t",nPassTrkCuts,"\t\t\t",float(nPassTrkCuts)/nPassV0Cuts,"\t\t\t",float(nPassTrkCuts)/nEvents
#    print "ECal Match  Cuts:\t\t",nPassECalMatch,"\t\t\t",float(nPassECalMatch)/nPassTrkCuts,"\t\t\t",float(nPassECalMatch)/nEvents

#                }

if __name__ == "__main__":
    main()



