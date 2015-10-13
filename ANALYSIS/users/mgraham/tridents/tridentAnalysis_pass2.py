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
    from ROOT import HpsEvent, SvtTrack, EcalCluster, EcalHit, TChain, TTree, HpsParticle




#################################
#       Event Selection
################################
    ebeam=1.05
#clean up event first
    nTrkMax=5
    nPosMax=2
 #v0 cuts   
    v0Chi2=10
    v0PzMax=1.25*ebeam
 #   v0PzMax=0.8*ebeam
    v0PzMin=0.6
#    v0PzMin=0.8*ebeam
    v0PyMax=0.2 #absolute value
    v0PxMax=0.2 #absolute value
    v0VzMax=25.0# mm from target
    v0VyMax=1.0# mm from target
    v0VxMax=2.0# mm from target
 #  track quality cuts
    trkChi2=10
#    beamCut=0.9
    beamCut=0.8
    minPCut=0.05
    trkPyMax=0.2
    trkPxMax=0.2
    slopeCut=0.02

    radCut=0.8*ebeam

    requireECalMatch = True
    useGBL=True
    #-----------------------------#
    #--- Setup ROOT histograms ---#
    #-----------------------------#

    # Create a canvas and set its characteristics
    #    canvas = ROOT.TCanvas("canvas", "Data Summary Tape Plots", 700, 700)
    #    setupCanvas(canvas)
  
    nCand = ROOT.TH1F("NCand","Number of Candidates", 4, 0, 4 );
    tridentMass = ROOT.TH1F("TridentMass","Trident Mass (GeV)", 500, 0, 0.100);
    tridentMassVtxCut = ROOT.TH1F( "TridentMassBeforeVertex", "Trident Mass (GeV): Before  VtxCut", 500, 0, 0.100);
    tridentVx = ROOT.TH1F("Vx", "Trident Vx (mm)", 100, -4, 4);
    tridentVy = ROOT.TH1F("Vy","Trident Vy (mm)", 100, -2, 2);
    tridentVz =  ROOT.TH1F("Vz", "Trident Vz (mm)", 100, -50, 50);
    eSum =  ROOT.TH1F("eSum", "Energy Sum", 100, 0.3, 1.2);
    eDiff =  ROOT.TH1F("eDiffoverESum", "Energy Difference", 100, -0.8, 0.8);    
    vertChi2 =  ROOT.TH1F("vertChi2", "V0 Chi2", 100, 0, 10);    
    ePosvseEle=ROOT.TH2F("ePosvseEle","Positron vs Electron Energy",100,0.1,0.9,50,0.1,0.9);
    tanopenY =  ROOT.TH1F("tanopenY", "tanopenY", 100, 0., 0.16);
    tanopenYThresh =  ROOT.TH1F("tanopenYThresh", "tanopenYThresh", 100, 0.025, 0.06);
    minAngle = ROOT.TH1F("minAngle","Minimum Track Angle",100,0.01,0.03)
    
    
    eleMom = ROOT.TH1F("eleMom","Electron Momentum (GeV)", 100, 0, 1.);
    posMom = ROOT.TH1F("posMom","Positron Momentum (GeV)", 100, 0, 1.);
    
    eled0 = ROOT.TH1F("eled0","Electron d0 (mm)", 100, -3, 3);
    posd0 = ROOT.TH1F("posd0","Positron d0 (mm)", 100, -3, 3);
    
    elez0 = ROOT.TH1F("elez0","Electron z0 (mm)", 100, -1.5, 1.5);
    posz0 = ROOT.TH1F("posz0","Positron z0 (mm)", 100, -1.5, 1.5);


    elephi0 = ROOT.TH1F("elephi0","Electron phi0", 100, -0.1, 0.1);
    posphi0 = ROOT.TH1F("posphi0","Positron phi0", 100, -0.1, 0.1);

    eleslope = ROOT.TH1F("eleslope","Electron slope", 100, -0.08, 0.08);
    posslope = ROOT.TH1F("posslope","Positron slope", 100, -0.08, 0.08);

    trkTimeDiff = ROOT.TH1F("trkTimeDiff","Ele-Pos Time Difference (ns)", 100, -6, 6);

    tHitTop=[]
    tHitBot=[]
    
    nlayers=6
    pre="time (ns) for layer ";
    for  i in range(1, nlayers) :
        topName=pre+" "+str(i)+" Top"
        tHitTop.append(ROOT.TH1F(topName,topName,100,-16,16))
        botName=pre+" "+str(i)+" Bot"
        tHitBot.append(ROOT.TH1F(botName,botName,100,-16,16))
   
   


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
    nPassV0Cuts=0;
    nPassTrkCuts=0;
    nPassNCand=0
    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
        # Print the event number every 500 events
        if (entry+1)%10000 == 0 : print "Event " + str(entry+1)

        # Read the ith entry from the tree.  This "fills" HpsEvent and allows 
        # access to all collections
#        entryNumber = tree.GetEntryNumber(entry);
#        localEntry = fTree.LoadTree(entryNumber);
#        print localEntry
#        if localEntry < 0: 
#            continue
#        tree.GetEntry(localEntry)
        tree.GetEntry(entry)
#        print "checking trigger"
        if not hps_event.isPair1Trigger() and not isMC : continue
        nEvents+=1
#        print "found a pair1 trigger"
        # Loop over all tracks in the event
        npositrons=0
        n_tracks=0
#        print "Found "+str( hps_event.getNumberOfTracks()) +" tracks in event"
#        if  hps_event.getNumberOfTracks() > 10 : continue
        for track_n in xrange(0, hps_event.getNumberOfTracks()) :             
            track = hps_event.getTrack(track_n)
            if track is None : 
                continue
#            if not (useGBL ^ track.type<32)  : continue
            n_tracks+=1
            if track.getCharge()>0 :
                npositrons+=1

#        print "nTracks = "+str(n_tracks)+"; nPositrons = "+str(npositrons)
        if n_tracks/2.0>nTrkMax : continue   #do this very dumb thing (divide by 2 to un-double count GBL tracks)
        if n_tracks/2.0<2:  continue        
        if npositrons<1 or npositrons>nPosMax : continue
        nPassBasicCuts+=1
#        print "passed basic cuts"
        candidateList=[]
        bestCandidate=-99
        nCandidate=0
        # loop over all v0 candidates...
        for uc_index in xrange(0, hps_event.getNumberOfParticles(HpsParticle.UC_V0_CANDIDATE)):
            particle = hps_event.getParticle(HpsParticle.UC_V0_CANDIDATE, uc_index)
            if not (useGBL ^ particle.getType()<32)  : continue
            vchi2=particle.getVertexFitChi2();
            vposition=particle.getVertexPosition();
            vmomentum=particle.getMomentum();
            if vchi2>v0Chi2 :  continue
            if vmomentum[2]>v0PzMax : continue
            if vmomentum[2]<v0PzMin : continue
            if abs(vposition[0])>v0VxMax : continue
            if abs(vposition[1])>v0VyMax :continue
#            if abs(vposition[2])>v0VzMax :continue
            nPassV0Cuts+=1
#            print "Passed v0 cuts"
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

            if pMag(pEle)>beamCut or pMag(pPos)>beamCut : continue
            if pMag(pEle)<minPCut or pMag(pPos)<minPCut : continue            
            if pEle[1]*pPos[1]>0 : continue
            if requireECalMatch: 
                if positron.getClusters().GetEntries() == 0 :
                    continue
                if electron.getClusters().GetEntries() == 0 :
                    continue
            eleTrk=electron.getTracks().At(0)
            posTrk=positron.getTracks().At(0)
            if abs(eleTrk.getTanLambda())<slopeCut or abs(posTrk.getTanLambda())<slopeCut :
                continue
                
            
#            print "Passed track cuts"
            nPassTrkCuts+=1
            #Passed the cuts..append the candidate index
            candidateList.append(uc_index)

        #########################        
        #   found some candidates...lets fill plots...
        #########################        
        nCand.Fill(len(candidateList))
        for index in range(0,len(candidateList)) :
            particle = hps_event.getParticle(HpsParticle.UC_V0_CANDIDATE, candidateList[index])
            vchi2=particle.getVertexFitChi2();
            vposition=particle.getVertexPosition();
            vmomentum=particle.getMomentum();

            daughter_particles = particle.getParticles()
            electron =  daughter_particles.At(0)
            positron =  daughter_particles.At(1)
            
            if daughter_particles.At(0).getCharge()>0:
                electron =  daughter_particles.At(1)
                positron =  daughter_particles.At(0)
            pEle=electron.getMomentum()
            pPos=positron.getMomentum()

            #fill the plots
            tridentVx.Fill(vposition[0])
            tridentVy.Fill(vposition[1])
            tridentVz.Fill(vposition[2])

            ePosvseEle.Fill(pMag(pEle),pMag(pPos))
#            eSum.Fill(pMag(pEle)+pMag(pPos))
            eSum.Fill(pMag(vmomentum)) #fill with the fitted momentum instead
            eDiff.Fill(pMag(pEle)-pMag(pPos))/(pMag(pEle)+pMag(pPos))
            tridentMass.Fill(particle.Mass());

            eleMom.Fill(pMag(pEle));
            posMom.Fill(pMag(pPos));
      
     
            eleTrk=electron.getTracks().At(0)
            posTrk=positron.getTracks().At(0)

            eled0.Fill(eleTrk.getD0())
            elez0.Fill(eleTrk.getZ0())
            elephi0.Fill(math.sin(eleTrk.getPhi0()))
            eleslope.Fill(eleTrk.getTanLambda())

            posd0.Fill(posTrk.getD0())
            posz0.Fill(posTrk.getZ0())
            posphi0.Fill(math.sin(posTrk.getPhi0()))
            posslope.Fill(posTrk.getTanLambda())
            
            trkTimeDiff.Fill(eleTrk.getTrackTime()-posTrk.getTrackTime())
            vertChi2.Fill(particle.getVertexFitChi2())
      
            topenAngle=abs(eleTrk.getTanLambda()) +abs(posTrk.getTanLambda())

            tanopenY.Fill(topenAngle);
            tanopenYThresh.Fill(topenAngle);
            minAngle.Fill(min(abs(eleTrk.getTanLambda()),abs(posTrk.getTanLambda())))
            
    out=ROOT.TFile(output_file,"RECREATE");
    tridentMass.Write()
    tridentVx.Write()
    tridentVy.Write()
    tridentVz.Write()
    tridentMassVtxCut.Write()
    ePosvseEle.Write()
    vertChi2.Write()
    eSum.Write()
    eDiff.Write()
    eleMom.Write() 
    eled0.Write() 
    elez0.Write()
    elephi0.Write()
    eleslope.Write()
    posMom.Write() 
    posd0.Write() 
    posz0.Write()
    posphi0.Write()
    posslope.Write()
    trkTimeDiff.Write()
    tanopenYThresh.Write()
    tanopenY.Write()
    nCand.Write()
    minAngle.Write()
    out.Close()

    print "\t\t\tTrident Selection Summary"
    print "******************************************************************************************"
    print "Number of Events:\t\t",nEvents,"\t\t\t",float(nEvents)/nEvents,"\t\t\t",float(nEvents)/nEvents
    print "N(particle) Cuts:\t\t",nPassBasicCuts,"\t\t\t",float(nPassBasicCuts)/nEvents,"\t\t\t",float(nPassBasicCuts)/nEvents
    print "V0 Vertex   Cuts:\t\t",nPassV0Cuts,"\t\t\t",float(nPassV0Cuts)/nPassBasicCuts,"\t\t\t",float(nPassV0Cuts)/nEvents
    print "Tracking    Cuts:\t\t",nPassTrkCuts,"\t\t\t",float(nPassTrkCuts)/nPassV0Cuts,"\t\t\t",float(nPassTrkCuts)/nEvents
                      
#            for(int i=0i<n_svt_hitsi++){
#                int layer = svt_hits_layer[i]
#                if(svt_hits_z[i]<0)
#                tHitBot[layer].Fill(svt_hits_time[i])
#                else
#                tHitTop[layer].Fill(svt_hits_time[i])         
#                }

if __name__ == "__main__":
    main()



