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
 #v0 cuts   
    v0Chi2=10
    v0PzMax=1.2
#    v0PzMax=0.8
    v0PzMin=0.55
#    v0PzMin=0.8
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
    requireECalMatch = False
    useGBL=False
    #-----------------------------#
    #--- Setup ROOT histograms ---#
    #-----------------------------#

    # Create a canvas and set its characteristics
    #    canvas = ROOT.TCanvas("canvas", "Data Summary Tape Plots", 700, 700)
    #    setupCanvas(canvas)
  
    nCand = ROOT.TH1F("NCand","Number of Candidates", 4, 0, 4 );
    tridentMass = ROOT.TH1F("TridentMass","Trident Mass (GeV)", 500, 0, 0.100);
    tridentMassVtxCut = ROOT.TH1F( "TridentMassBeforeVertex", "Trident Mass (GeV): Before  VtxCut", 500, 0, 0.100);
    tridentVx = ROOT.TH1F("Vx", "Trident Vx (mm)", 50, -4, 4);
    tridentVy = ROOT.TH1F("Vy","Trident Vy (mm)", 50, -2, 2);
    tridentVz =  ROOT.TH1F("Vz", "Trident Vz (mm)", 50, -50, 50);
    eSum =  ROOT.TH1F("eSum", "Energy Sum", 50, 0.3, 1.2);
    eSumEhnHenry =  ROOT.TH1F("eSumEhnHenry", "Energy Sum with cuts from Ehn and Henry", 50, 0.3, 1.2);
    eDiff =  ROOT.TH1F("eDiffoverESum", "Energy Difference", 50, -0.8, 0.8);    
    vertChi2 =  ROOT.TH1F("vertChi2", "V0 Chi2", 50, 0, 10);    
    ePosvseEle=ROOT.TH2F("ePosvseEle","Positron vs Electron Energy",50,0.1,0.9,50,0.1,0.9);
    ESumvsEDiff=ROOT.TH2F("ESumvsEDiff","Energy difference (normalized) vs Energy Sum",50,0.55,1.2,50,-1,1.0);
    tanopenY =  ROOT.TH1F("tanopenY", "tanopenY", 50, 0., 0.16);
    tanopenYThresh =  ROOT.TH1F("tanopenYThresh", "tanopenYThresh", 50, 0.025, 0.06);
    minAngle = ROOT.TH1F("minAngle","Minimum Track Angle",50,0.01,0.03)
    coplan=ROOT.TH1F("coplanarity","Coplanarity",50,-0.004,0.004)
    copVseSum=ROOT.TH2F("coplanarity vs eSum", "coplanarity vs eSum", 50,0.3,1.2,50,-0.004,0.004)

    deltaPhi=ROOT.TH1F("deltaPhi","DeltaPhi",50,-2,2)
    deltaTheta=ROOT.TH1F("deltaTheta","DeltaTheta",50,-0.1,0.1)
    
    eleMom = ROOT.TH1F("eleMom","Electron Momentum (GeV)", 50, 0, 1.);
    posMom = ROOT.TH1F("posMom","Positron Momentum (GeV)", 50, 0, 1.);
    
    eled0 = ROOT.TH1F("eled0","Electron d0 (mm)", 50, -3, 3);
    posd0 = ROOT.TH1F("posd0","Positron d0 (mm)", 50, -3, 3);
    
    elez0 = ROOT.TH1F("elez0","Electron z0 (mm)", 50, -1.5, 1.5);
    posz0 = ROOT.TH1F("posz0","Positron z0 (mm)", 50, -1.5, 1.5);


    elephi0 = ROOT.TH1F("elephi0","Electron phi0", 50, -0.1, 0.1);
    posphi0 = ROOT.TH1F("posphi0","Positron phi0", 50, -0.1, 0.1);

    elephibeam = ROOT.TH1F("elephibeam","Electron phibeam", 50, -3.15, 3.15);
    posphibeam = ROOT.TH1F("posphibeam","Positron phibeam", 50, -3.15, 3.15);

    elepolarangle = ROOT.TH1F("elepolarangle","Electron Polar Angle", 50, 0.0, 0.1);
    pospolarangle = ROOT.TH1F("pospolarangle","Positron Polar Angle", 50, 0.0, 0.1);

    eleslope = ROOT.TH1F("eleslope","Electron slope", 50, -0.08, 0.08);
    posslope = ROOT.TH1F("posslope","Positron slope", 50, -0.08, 0.08);

    trkTimeDiff = ROOT.TH1F("trkTimeDiff","Ele-Pos Time Difference (ns)", 50, -6, 6);
    cluTimeDiff = ROOT.TH1F("cluTimeDiff","Cluster Time Difference (ns)", 50, -2, 2);

#plots in slices of ESum
    eleMomESum=[]
    posMomESum=[]
    eleThetaESum=[]
    posThetaESum=[]
    elePhi0ESum=[]
    posPhi0ESum=[]
    coplanESum=[]
    eDiffESum=[]
    polarAngleESum=[]#polar angle of the V0
    phiV0ESum=[]  #phi of the V0


    post=" ESum Slice "
    for i in range(1, nSlicesESum+1) :
        name="eleMom "+post+str(i)
        eleMomESum.append(ROOT.TH1F(name,name,50,0,1.0))
        name="posMom "+post+str(i)
        posMomESum.append(ROOT.TH1F(name,name,50,0,1.0))
        name="eleTheta "+post+str(i)
        eleThetaESum.append(ROOT.TH1F(name,name,50,-0.08,0.08))
        name="posTheta "+post+str(i)
        posThetaESum.append(ROOT.TH1F(name,name,50,-0.08,0.08))
        name="elePhi0 "+post+str(i)
        elePhi0ESum.append(ROOT.TH1F(name,name,50,-0.1,0.1))
        name="posPhi0 "+post+str(i)
        posPhi0ESum.append(ROOT.TH1F(name,name,50,-0.1,0.1))
        name="Coplanarity "+post+str(i)
        coplanESum.append(ROOT.TH1F(name,name,50,-0.004,0.004))
        name="Ediff "+post+str(i)
        eDiffESum.append(ROOT.TH1F(name,name,50,-0.8,0.8))
        name="V0PolarAngle "+post+str(i)
        polarAngleESum.append(ROOT.TH1F(name,name,50,0,0.05))
        name="V0Phi "+post+str(i)
        phiV0ESum.append(ROOT.TH1F(name,name,50,0,3.15))



    tHitTop=[]
    tHitBot=[]
    
    nlayers=6
    pre="time (ns) for layer "
    for  i in range(1, nlayers) :
        topName=pre+" "+str(i)+" Top"
        tHitTop.append(ROOT.TH1F(topName,topName,50,-16,16))
        botName=pre+" "+str(i)+" Bot"
        tHitBot.append(ROOT.TH1F(botName,botName,50,-16,16))
   
   


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
    beam=[np.sin(0.0305),0,np.cos(0.0305)]
    beamRotAxis=[0,1,0]
    rotAngle=-0.0305
    toBeamFrame=rotation_matrix(beamRotAxis,rotAngle)
    print "Rotation Matrix:  "
    print str(toBeamFrame)
    # Loop over all events in the file
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
#        if n_tracks/2.0>nTrkMax : continue   #do this very dumb thing (divide by 2 to un-double count GBL tracks)
#        if n_tracks/2.0<2:  continue        
        if n_tracks>nTrkMax : continue  
        if n_tracks<2:  continue        
        if npositrons<1 or npositrons>nPosMax : continue
        nPassBasicCuts+=1
#        print "passed basic cuts"
        candidateList=[]
        bestCandidate=-99
        nCandidate=0
        # loop over all v0 candidates...
        for uc_index in xrange(0, hps_event.getNumberOfParticles(HpsParticle.UC_V0_CANDIDATE)):
            particle = hps_event.getParticle(HpsParticle.UC_V0_CANDIDATE, uc_index)
#            print "useGBL = "+str(useGBL)+"; particle.getType() = +"+str(particle.getType())
#            if not (useGBL ^ particle.getType()<32)  : continue  # not sure why this doesn't work
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

            if v0Sum>v0PzMax : continue
            if v0Sum<v0PzMin : continue
            nPassV0Cuts+=1
#            print "Passed v0 cuts"


            if pMag(pEle)>beamCut or pMag(pPos)>beamCut : continue
            if pMag(pEle)<minPCut or pMag(pPos)<minPCut : continue            
            if pEle[1]*pPos[1]>0 : continue
            if requireECalMatch: 
                if positron.getClusters().GetEntries() == 0 :
                    continue
                if electron.getClusters().GetEntries() == 0 :
                    continue
            eleTrk=SvtTrack(electron.getTracks().At(0))
            posTrk=SvtTrack(positron.getTracks().At(0))
            if abs(eleTrk.getTanLambda())<slopeCut or abs(posTrk.getTanLambda())<slopeCut :
                continue

            if isMC and trackKiller : 
                if pMag(pEle) <tkEnergy and random.random()>tkEff  :
                    continue
            
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


            # calculate the coplanarity of the e+, e-, and the beam
            normEle=np.linalg.norm(pEle)
            normPos=np.linalg.norm(pPos)
            peleArray=np.asarray(pEle)
            pposArray=np.asarray(pPos)            
            coplanarity=np.dot(beam,(np.cross(peleArray,pposArray)))/normEle/normPos;
            coplan.Fill(coplanarity)

            # calculate the polar angle and azimuthal angle of the v0 (wrt beam)
            normpV0=np.linalg.norm(vmomentum)
            pv0Array=np.asarray(vmomentum)
            rotatedpv0=np.dot(toBeamFrame,pv0Array)            
#            v0PolarAngle=math.acos(np.dot(beam,pv0Array)/normpV0)
            v0PolarAngle=getPolarAngle(rotatedpv0)
#            print str(rotatedpv0)
#            print str(pv0Array)
            v0Phi=abs(math.atan2(rotatedpv0[1],rotatedpv0[0]))

            #fill the vertex position plots
            tridentVx.Fill(vposition[0])
            tridentVy.Fill(vposition[1])
            tridentVz.Fill(vposition[2])

            ePosvseEle.Fill(pMag(pEle),pMag(pPos))

            v0Sum=pMag(pSum(pEle,pPos))
            eSum.Fill(v0Sum)
#            eSum.Fill(pMag(vmomentum)) #fill with the fitted momentum instead
            ediff=(pMag(pEle)-pMag(pPos))/(pMag(pEle)+pMag(pPos))
            eDiff.Fill(ediff)
            ESumvsEDiff.Fill(pMag(pSum(pEle,pPos)), ediff)
            tridentMass.Fill(particle.Mass())
            copVseSum.Fill(pMag(vmomentum),coplanarity)
            eleMom.Fill(pMag(pEle))
            posMom.Fill(pMag(pPos))

            peleArray=np.asarray(pEle)
            rotatedpele=np.dot(toBeamFrame,peleArray)    
#            print "original electron momentum:  "+str(peleArray)
#            print "rotated electron momentum:  "+str(rotatedpele)
            pelePhi=math.atan2(rotatedpele[1],rotatedpele[0])            
            elephibeam.Fill(pelePhi)
            elepolarangle.Fill(getPolarAngle(rotatedpele))

            pposArray=np.asarray(pPos)
            rotatedppos=np.dot(toBeamFrame,pposArray)  
            pposPhi=math.atan2(rotatedppos[1],rotatedppos[0])
            posphibeam.Fill(pposPhi)
            pospolarangle.Fill(getPolarAngle(rotatedppos))
     
            deltaTheta.Fill(getPolarAngle(rotatedppos)-getPolarAngle(rotatedpele))
            deltaPhi.Fill(pposPhi+pelePhi) 

            eleTrk=electron.getTracks().At(0)
            posTrk=positron.getTracks().At(0)

            eled0.Fill(eleTrk.getD0())
            elez0.Fill(eleTrk.getZ0())
            elephi0.Fill(math.sin(eleTrk.getPhi0()))
            eleslope.Fill(eleTrk.getTanLambda())
#            print "phi0 = "+str(eleTrk.getPhi0())+"; phi_beam = "+str(pelePhi)
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

#          make similar cuts to D. C. Ehn and G. R. Henry, physical review 162, 1967
            thetaRegion=0.04 # this was 0.13 in the paper...we don't get that far out though
            thetaCut=0.01  # symmetric about this...
            deltaPhiCut=0.25
            if (abs(getPolarAngle(rotatedppos)-thetaRegion)<thetaCut and \
                    abs(getPolarAngle(rotatedpele)-thetaRegion)<thetaCut and \
                    abs(pposPhi+pelePhi)<deltaPhiCut) : 
                eSumEhnHenry.Fill(v0Sum)

            if requireECalMatch: 
                pTime=positron.getClusters().At(0).getClusterTime();
                eTime=electron.getClusters().At(0).getClusterTime();
                cluTimeDiff.Fill(eTime-pTime);
            #fill the slices in ESum
            esumBin=int((v0Sum-esumMin)/sliceSizeESum)            
            if(esumBin>=nSlicesESum) :
                esumBin = nSlicesESum-1
#            print "esumBin = "+str(esumBin)
            eleMomESum[esumBin].Fill(pMag(pEle))
            posMomESum[esumBin].Fill(pMag(pPos))
            eleThetaESum[esumBin].Fill(eleTrk.getTanLambda())
            posThetaESum[esumBin].Fill(posTrk.getTanLambda())
            elePhi0ESum[esumBin].Fill(math.sin(eleTrk.getPhi0()))
            posPhi0ESum[esumBin].Fill(math.sin(posTrk.getPhi0()))
            coplanESum[esumBin].Fill(coplanarity)
            eDiffESum[esumBin].Fill(ediff)
            polarAngleESum[esumBin].Fill(v0PolarAngle)
            phiV0ESum[esumBin].Fill(v0Phi)
#      

            
    out=ROOT.TFile(output_file,"RECREATE");
    tridentMass.Write()
    tridentVx.Write()
    tridentVy.Write()
    tridentVz.Write()
    tridentMassVtxCut.Write()
    ePosvseEle.Write()
    ESumvsEDiff.Write()
    vertChi2.Write()
    eSum.Write()
    eSumEhnHenry.Write()
    eDiff.Write()
    eleMom.Write() 
    eled0.Write() 
    elez0.Write()
    elephi0.Write()
    elephibeam.Write()
    elepolarangle.Write()
    eleslope.Write()
    copVseSum.Write()
    coplan.Write()    
    posMom.Write() 
    posd0.Write() 
    posz0.Write()
    posphi0.Write()
    posphibeam.Write()
    pospolarangle.Write()
    posslope.Write()
    deltaTheta.Write()
    deltaPhi.Write()
    trkTimeDiff.Write()
    cluTimeDiff.Write()    
    tanopenYThresh.Write()
    tanopenY.Write()
    nCand.Write()
    minAngle.Write()
    for i in range(0, nSlicesESum) :
        eleMomESum[i].Write()
        posMomESum[i].Write()
        eleThetaESum[i].Write()
        posThetaESum[i].Write()
        elePhi0ESum[i].Write()
        posPhi0ESum[i].Write()
        coplanESum[i].Write()
        eDiffESum[i].Write()
        polarAngleESum[i].Write()
        phiV0ESum[i].Write()
        

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



