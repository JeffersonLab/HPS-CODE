#!/usr/bin/python

#
# @file analysis_pyroot_example.py
# @section purpose:
#       A simple PyRoot analysis demonstrating the use of a DST to make simple
#       plots of Ecal, SVT and Particle objects
#
# @author Omar Moreno <omoreno1@ucsc.edu>
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

#################################
#       Event Selection
################################
    ebeam=1.05
#clean up event first
    nTrkMax=5
    nPosMax=2
# vertex quality cuts for vertexing 
    v0Chi2=10.0
    v0PzMax=1.2
    v0PzMin=0.8
    v0PyMax=0.2 #absolute value
    v0PxMax=0.2 #absolute value
    v0VyMax=1.0# mm from target
    v0VxMax=2.0# mm from target
 #  track quality cuts    
    trkChi2=20.0
#    trkChi2=100.0
    beamCut=0.8
    isoCut=1.0
    minPCut=0.25
    trkPyMax=0.2
    trkPxMax=0.2
    slopeCut=0.0
    z0Cut=0.5

##############
#  ESum slices; upper limits    
    nSlicesESum=5 
    esumMin=0.55
    esumMax=1.2
    sliceSizeESum=0.1 #100MeV starting at esumMin
##############
    trackKiller=False
    tkEnergy=0.3
    tkEff=0.75 

##############
    requireECalMatch = True
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

    # Get the HpsEvent branch from the TTree 
#    b_hps_event = tree.GetBranch("Event")
#    b_hps_event.SetAddress(ROOT.AddressOf(hps_event))

    #--- Analysis ---#
    #----------------#

    #counters
    nEvents=0;
    nPassBasicCuts=0;
    nPassESumCuts=0;
    nPassV0Cuts=0;
    nPassTrkCuts=0;
    nPassIsoCuts=0;
    nPassNCand=0
    nPassECalMatch=0;
    myhist=myHistograms()
    for entry in xrange(0, tree.GetEntries()) : 
        # Print the event number every 500 events
        if (entry+1)%10000 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
        if not hps_event.isPair1Trigger() and not isMC : continue
        nEvents+=1
        # Loop over all tracks in the event
        npositrons=0
        n_tracks=0
        for track_n in xrange(0, hps_event.getNumberOfTracks()) :             
            track = hps_event.getTrack(track_n)
            if track is None : 
                continue
#            if not (useGBL ^ track.type<32)  : continue
            n_tracks+=1
            if track.getCharge()>0 :
                npositrons+=1

#        print "nTracks = "+str(n_tracks)+"; nPositrons = "+str(npositrons)
        if n_tracks>nTrkMax : continue  
        if n_tracks<2:  continue        
        if npositrons<1 or npositrons>nPosMax : continue
        nPassBasicCuts+=1
#        print "passed basic cuts"
        candidateList=[]
        bestCandidate=-99
        nCandidate=0
        # loop over all v0 candidates...
        for bsc_index in xrange(0, hps_event.getNumberOfParticles(HpsParticle.BSC_V0_CANDIDATE)):
            particle = hps_event.getParticle(HpsParticle.BSC_V0_CANDIDATE, bsc_index)
            if useGBL and  particle.getType()<32  : continue
            if not useGBL and  particle.getType()>31  : continue
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
            
            if v0Sum>v0PzMax : continue
            if v0Sum<v0PzMin : continue
            nPassESumCuts+=1

            vchi2=particle.getVertexFitChi2();
            vposition=particle.getVertexPosition();
            vmomentum=particle.getMomentum();
            if vchi2>v0Chi2 :  continue

            if abs(vposition[0])>v0VxMax : continue
            if abs(vposition[1])>v0VyMax :continue

            nPassV0Cuts+=1

#            print "Passed v0 cuts"

            if pMag(pEle)>beamCut or pMag(pPos)>beamCut : continue
            if pMag(pEle)<minPCut or pMag(pPos)<minPCut : continue            
            if pEle[1]*pPos[1]>0 : continue
           
#            print particle.getTracks().At(0).GetEntries()

#            eleTrk=GblTrack(particle.getTracks().At(0))
#            posTrk=GblTrack(particle.getTracks().At(1))

#            if eleTrk.getCharge()>0 :
#                eleTrk=GblTrack(particle.getTracks().At(1))
#                posTrk=GblTrack(particle.getTracks().At(0))

            eleTrk=electron.getTracks().At(0)
            posTrk=positron.getTracks().At(0)

            if eleTrk.getChi2()>trkChi2 or posTrk.getChi2()>trkChi2 :
                continue

            
            if abs(eleTrk.getZ0())>z0Cut or abs(posTrk.getZ0())>z0Cut :
                continue
#            if abs(eleTrk.getTanLambda())<slopeCut or abs(posTrk.getTanLambda())<slopeCut :
#                continue

            if isMC and trackKiller : 
                if pMag(pEle) <tkEnergy and random.random()>tkEff  :
                    continue
            
            nPassTrkCuts+=1
            if requireECalMatch: 
                if positron.getClusters().GetEntries() == 0 :
                    continue
                if electron.getClusters().GetEntries() == 0 :
                    continue
            nPassECalMatch+=1

            if abs(eleTrk.getIsolation(0))<isoCut or abs(eleTrk.getIsolation(1))< isoCut :
                continue
            if abs(posTrk.getIsolation(0))<isoCut or abs(posTrk.getIsolation(1))< isoCut :
                continue
            nPassIsoCuts+=1
            #Passed the cuts..append the candidate index
            candidateList.append(bsc_index)

        #########################        
        #   found some candidates...lets fill plots...
        #########################        
        for index in range(0,len(candidateList)) :
            particle = hps_event.getParticle(HpsParticle.BSC_V0_CANDIDATE, candidateList[index])
            ucparticle= hps_event.getParticle(HpsParticle.UC_V0_CANDIDATE, candidateList[index])
            myhist.fillCandidateHistograms(particle,ucparticle)
         
    if nPassIsoCuts > 0 :
        myhist.saveHistograms(output_file)   
 

    print "\t\t\tTrident Selection Summary"
    print "******************************************************************************************"
    print "Number of Events:\t\t",nEvents,"\t\t\t",float(nEvents)/nEvents,"\t\t\t",float(nEvents)/nEvents
    print "N(particle) Cuts:\t\t",nPassBasicCuts,"\t\t\t",float(nPassBasicCuts)/nEvents,"\t\t\t",float(nPassBasicCuts)/nEvents
    print "ESum        Cuts:\t\t",nPassESumCuts,"\t\t\t",float(nPassESumCuts)/nPassBasicCuts,"\t\t\t",float(nPassESumCuts)/nEvents
    print "V0 Vertex   Cuts:\t\t",nPassV0Cuts,"\t\t\t",float(nPassV0Cuts)/nPassESumCuts,"\t\t\t",float(nPassV0Cuts)/nEvents
    print "Tracking    Cuts:\t\t",nPassTrkCuts,"\t\t\t",float(nPassTrkCuts)/nPassV0Cuts,"\t\t\t",float(nPassTrkCuts)/nEvents
    print "ECal Match  Cuts:\t\t",nPassECalMatch,"\t\t\t",float(nPassECalMatch)/nPassTrkCuts,"\t\t\t",float(nPassECalMatch)/nEvents
    print "Isolation    Cuts:\t\t",nPassIsoCuts,"\t\t\t",float(nPassIsoCuts)/nPassECalMatch,"\t\t\t",float(nPassIsoCuts)/nEvents
                      

if __name__ == "__main__":
    main()



