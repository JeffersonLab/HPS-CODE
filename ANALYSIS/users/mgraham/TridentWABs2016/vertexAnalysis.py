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
    xsize=effGraph.GetErrorXhigh(0)*2
    nbins=effGraph.GetN()
    nbinsHist=(int)((xmax-xmin)/xsize)
    x=ROOT.Double(0.0)
    y=ROOT.Double(0.0)
    print nbins
    effHist=ROOT.TH1D(effGraph.GetName(),effGraph.GetTitle(),nbinsHist,xmin,xmax)
    for i in range(0,nbins) : 
        effGraph.GetPoint(i,x,y)
        histBin=effHist.FindBin(x)
        print str(x)+' ' +str(y) + ' '+str(i)+ '  '+str(histBin)
        effHist.SetBinContent(histBin,y)    

    return effHist

def getEffRatio(hfile,hname) :
    return hfile.Get(hname)

def getEffTH2(hfile, hname) : 
    print 'Getting efficiency TH2 '+hname    
    effHist=hfile.Get(hname)
    return effHist

def fixTH1EffBins(hist) :
    nbins=hist.GetNbinsX()
    for i in range(0,nbins): 
        print 'bin '+str(i)+':  '+str(hist.GetBinContent(i))

def fixTH2EffBins(hist) :
    nbinsX=hist.GetNbinsX()
    nbinsY=hist.GetNbinsY()
    for i in range(0,nbinsX): 
        for j in range(0,nbinsY): 
            print 'bin '+str(i)+','+str(j)+':  '+str(hist.GetBinContent(i,j))
            if hist.GetBinContent(i,j)==0: 
                print 'fixing 0 bin' 
                hist.SetBinContent(i,j,1.0) 
            if hist.GetBinContent(i,j)>2.0: 
                print 'fixing high bin' 
                hist.SetBinContent(i,j,1.0) 
                               

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
    parser.add_argument("-r","--rad",help="radiative cut")
    parser.add_argument("-w","--weigh",help="track efficiency weighing")
    
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

    doRadRegion=False
    if args.rad: 
        print "[ HPS ANALYSIS ]: Setting to run with Radiative Region Cut" 
        doRadRegion=True

    weightTracks=False
    if args.weigh: 
        print "[ HPS ANALYSIS ]: Setting to run with track efficiency weighing" 
        weightTracks=True

    if args.energy : 
        print 'Setting beam energy to '+args.energy
        beamEnergy=float(args.energy)
        myhist.setEnergyScales(beamEnergy)

    doTB=True
    doTT=False #or BB
    doEpEm=True
    doEmEm=False
    doEpEp=False
    doEpGam=True
    doEmGam=True
    doGamGam=False
    do3Body=False
    


#################################
#       Event Selection
################################
# Define cuts
#  mg...these cuts are from Omar's bump hunt selection (as of 1/10/17)
#  he has already selected events with top/bottom e+e- tracks with track momentum <0.8 GeV
# Accidentals
#    radiative_cut = v0_p > 0.8*1.056
#    v0_p_cut = v0_p < 1.2*1.056
#    chi2_cut = (electron_chi2 < 40) & (positron_chi2 < 40)

#    top_track_cluster_dt = top_cluster_time - top_time
#    bot_track_cluster_dt = bot_cluster_time - bot_time
#    track_cluster_dt_cut = ((np.absolute(top_track_cluster_dt - 43) < 4.5) 
#                            & (np.absolute(bot_track_cluster_dt - 43) < 4.5))
#    cluster_time_diff_cut = np.absolute(cluster_time_diff) < 2
#    
#    base_selection = radiative_cut & v0_p_cut & chi2_cut & track_cluster_dt_cut & cluster_time_diff_cut

    # e+ converted WABS
#    l1_cut      = (positron_has_l1 == 1)
#    l2_cut      = (positron_has_l2 == 1)
#    positron_d0_cut = positron_d0 < 1.1
#    asym = (electron_pt - positron_pt)/(electron_pt + positron_pt)
#    asym_cut = asym < .47
#
#    wab_cuts = l1_cut & l2_cut & positron_d0_cut & asym_cut
#
#    selection = base_selection & wab_cuts
###########################################


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
    v0PzMax=1.1*beamEnergy    
    v0PzMin=0.5*beamEnergy
    if doRadRegion: 
        v0PzMin=0.8*beamEnergy
 #  track quality cuts
    trkChi2=40
    beamCut=0.8*beamEnergy
    minPCut=0.05*beamEnergy    
    slopeCut=0.0
#    if isMC: 
#        cluDeltaT=4
#    else:
    cluDeltaT=2#ns
#    cluDeltaT=10#ns
    cluTrkDeltaT=4.5#ns
    cluTrkOffset=43#ns

    # non-converted WAB coplanarity cut: 
    wabCoplanMean=150 #degrees
    wabCoplanCut=15  #degrees

    trackKiller=False
    killInMomentum=False
    killInClusterPosition=False
    killInTrackSlope=False
    weighInEclVsY=True

    effMomFileName='/u/br/mgraham/hps-analysis/TrackEfficiency/cop180_EfficiencyResults.root'
    effRatioName='h_Ecl_hps_005772_eleEff_ratio'
    effMomFile=ROOT.TFile(effMomFileName)
    effMomData=getEffRatio(effMomFile,effRatioName)
    effMomData.Print("v")
    print 'Efficiency vs Momentum:  MC' 
    fixTH1EffBins(effMomData) 
    for i in range(0,effMomData.GetNbinsX()) : 
        print 'efficiency ratio '+str(i)+'   '+str(effMomData.GetBinCenter(i))+' '+str(effMomData.GetBinContent(i))

    effEclVsYFileName='/u/br/mgraham/hps-analysis/TrackEfficiency/cop180_TwoD-EfficiencyResults.root'
    effEclVsYFile=ROOT.TFile(effEclVsYFileName)
    eff2DEleRatioName='data_over_wab_plus_tritig_eleEffRatio'
    eff2DEleRatio=getEffTH2(effEclVsYFile,eff2DEleRatioName)
    eff2DEleRatio.Print("V")
    fixTH2EffBins(eff2DEleRatio)

    eff2DPosRatioName='data_over_wab_plus_tritig_posEffRatio'
#    eff2DPosRatio=getEffTH2(effEclVsYFile,eff2DPosRatioName)
    eff2DPosRatio=getEffTH2(effEclVsYFile,eff2DEleRatioName)
    eff2DPosRatio.Print("V")
    fixTH2EffBins(eff2DPosRatio)

###############
    requireECalMatch = True
    requireECalFiducial = False
    requireECalSuperFiducial = False
    requireECalTimingCoincidence = False
    requireECalTrackTiming = False
    requireWABCoplanarity = False
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

    nKilled=0
    nTrks=0

    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
                 
        nEpEmTB=0
        nEmEmTB=0
        nEmGamTB=0
#        print "Next event..."
        # Print the event number every 500 events
        if (entry+1)%100 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
        if not hps_event.isPair1Trigger() and not isMC and not isPulser: continue
        nEvents+=1
      
        #kill tracks by killing L1 hits (and then checking if they have enough hits)
        survivingFSP=[]
        for fsp_n in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)) :             
            fsp = hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE,fsp_n)
            if fsp.getType()==0 : # is a photon...            
                survivingFSP.append(fsp)
                continue
            if useGBL and  fsp.getType()<32 : continue
            if not useGBL and  fsp.getType()>31  : continue
            trk=fsp.getTracks()[0]
            yesL1Hit=myhist.hasL1Hit(trk)
            nHits=len(trk.getSvtHits())
            slp=trk.getTanLambda()
#            print "This track has #nhits = "+str(nHits)
            if not yesL1Hit : 
                survivingFSP.append(fsp)
                continue #this track doesn't have an L1 hit to kill
            if nHits>5 : 
                survivingFSP.append(fsp)
                continue #even if we kill L1 hit, this track will survive
#            bin=effSlopeData.FindBin(slp)
#            eff=1-effSlopeData.GetBinContent(bin) #the slope "efficiecny" is actually an inefficiency
#            rndm=random.random()
#            print 'found a 5 hit track with slope = '+str(slp)+'; eff = '+str(eff)+"; rndm = "+str(rndm)
#            if isMC and trackKiller and killInTrackSlope and rndm>eff : 
#            if rndm>eff : 
                # L1 hit got killed!  Since we already checked nHits==5, this track is dead
#                print 'killing track with slope = ' +str(slp)
#                continue
#            else : 
            survivingFSP.append(fsp)


#        print "number of surviving particles = "+str(len(survivingFSP))
        # Loop over all tracks in the event
        goodtrk=[]
        gamList=[]
        eleList=[]
        posList=[]
#        for fsp_n in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)) :             
#            fsp = hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE,fsp_n)
        for fsp in survivingFSP: 
            if fsp.getType() == 0 :  #might be good photon 
                if not checkClusterFiducialAndTiming(fsp,requireECalSuperFiducial) :  continue
                gamList.append(fsp)
            else : #maybe a good track? 
                if useGBL and  fsp.getType()<32  : continue
                if not useGBL and  fsp.getType()>31  : continue
                track=fsp.getTracks()[0]
                if track is None : continue #this shouldn't happen
                if requireECalMatch and not trkMatchAndFiducial(track.getParticle(),requireECalSuperFiducial) : continue
                if not trkMomentum(track,minPCut,beamCut):  continue
                if myhist.checkIfShared(goodtrk,fsp): 
#                    print 'fromscratch::now goodtrk is '+str(len(goodtrk))+' tracks long'
#                    for trk in goodtrk: 
                    #                        print len(trk.getTracks()[0].getSvtHits())
                    continue
                nTrks+=1            # check to see if we already found this track
                if trackKiller and isMC and requireECalMatch: # use the ECAL cluster to do this!!! 
                    if killInMomentum : 
#                        p=pMag(fsp.getMomentum())
                        p=fsp.getEnergy()
                        bin=effMomData.FindBin(p)                    
                        tkEff=effMomData.GetBinContent(bin)
#                        print str(p)+ ' '+str(bin)+' '+str(tkEff)
                        if random.random()>tkEff and tkEff!=0.0  :  #high ratio of efficiencies, this hardly  kills...low, kills a lot
                            print "REJECTING THIS TRACK!!! "+str(p)
                            nKilled+=1
                            continue
#                    if killInClusterPosition:  
#                        clEle=fsp.getClusters()[0]
#                        clX=clEle.getPosition()[0]
#                        clY=clEle.getPosition()[1]
#                        if fsp.getCharge()<0 : 
#                            bin=effData.FindBin(clX,clY)
#                        else: 
#                            bin=effData.FindBin(-clX+42.55,clY) # flip sign +42.55mm for positron side (this isn't strictly correct)!!!
#                        tkEff=effData.GetBinContent(bin)
#                        if random.random()>tkEff  and tkEff!=0.0:  
#                            print str(clX)+ ' '+str(clY)+' '+str(bin)+' '+str(tkEff)
#                            print "REJECTING THIS ELECTRON TRACK!!! "+str(clX)
#                            continue
                    

            #otherwise this is a new track
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
        if doEpEm : 
            for pos in posList : 
                if (requireECalTrackTiming and not myhist.clusterTrackCoincidence(pos,cluTrkDeltaT,cluTrkOffset) ):  
                    continue                
                for ele in eleList: 
                    if (requireECalTrackTiming and not myhist.clusterTrackCoincidence(ele,cluTrkDeltaT,cluTrkOffset) ):  
                        continue
                    if  (requireECalTimingCoincidence and not myhist.simpleClusterCoincidence(ele,pos,cluDeltaT)) or pMag(pSum(ele.getMomentum(),pos.getMomentum()))<v0PzMin :
                        continue
                    eleHitInL1=myhist.hasL1Hit(ele.getTracks()[0])
                    posHitInL1=myhist.hasL1Hit(pos.getTracks()[0])
                    eleHitInL2=myhist.hasLXHit(ele.getTracks()[0],2)
                    posHitInL2=myhist.hasLXHit(pos.getTracks()[0],2)
                    eleWgt=1.0
                    posWgt=1.0
                    if weightTracks and isMC and requireECalMatch: 
                        clEle=ele.getClusters()[0]
                        clEcl=clEle.getEnergy()
                        clY=clEle.getPosition()[1]                
                        eleWgt=eff2DEleRatio.GetBinContent(eff2DEleRatio.FindBin(clEcl,clY))
                        clPos=pos.getClusters()[0]
                        clEcl=clPos.getEnergy()
                        clY=clPos.getPosition()[1]                
                        posWgt=eff2DPosRatio.GetBinContent(eff2DPosRatio.FindBin(clEcl,clY))
                    if doTB and ele.getMomentum()[1]*pos.getMomentum()[1] <0 : 
                        myhist.fillTwoBody(pos,ele,'EpEm','TB',eleWgt*posWgt)
                        if eleHitInL1 and posHitInL1 :  
                            myhist.fillTwoBody(pos,ele,'EpEmL1L1','TB',eleWgt*posWgt) 
#                            if not eleHitInL2 and not posHitInL2:
#                                myhist.fillTwoBody(pos,ele,'EpEmL1NoL2L1NoL2','TB') 
#                            elif not eleHitInL2 : 
#                                myhist.fillTwoBody(pos,ele,'EpEmL1NoL2L1L2','TB') 
#                            elif not posHitInL2 : 
#                                myhist.fillTwoBody(pos,ele,'EpEmL1L2L1NoL2','TB') 
#                            else: 
#                                myhist.fillTwoBody(pos,ele,'EpEmL1L2L1L2','TB') 
                        elif eleHitInL1 : 
                            myhist.fillTwoBody(pos,ele,'EpEmL2L1','TB',eleWgt*posWgt)
 #                           if not eleHitInL2 :
 #                               myhist.fillTwoBody(pos,ele,'EpEmNoL1L2L1NoL2','TB') 
 #                           else:
 #                               myhist.fillTwoBody(pos,ele,'EpEmNoL1L2L1L2','TB')                                 
                        elif posHitInL1 : 
                            myhist.fillTwoBody(pos,ele,'EpEmL1L2','TB',eleWgt*posWgt)
 #                           if not posHitInL2 :
 #                               myhist.fillTwoBody(pos,ele,'EpEmL1NoL2NoL1L2','TB') 
 #                           else:
 #                               myhist.fillTwoBody(pos,ele,'EpEmL1L2NoL1L2','TB')                                 
                        else: 
                            myhist.fillTwoBody(pos,ele,'EpEmL2L2','TB',eleWgt*posWgt)                
#do analysis for e-e- pairs
        if doEmEm : 
            for i in range(0,len(eleList)) : 
                ele1=eleList[i]
                if (requireECalTrackTiming and not myhist.clusterTrackCoincidence(ele1,cluTrkDeltaT,cluTrkOffset) ):  
                    continue
                for k in range(i+1,len(eleList)):
                    ele2=eleList[k]
                    if (requireECalTrackTiming and not myhist.clusterTrackCoincidence(ele2,cluTrkDeltaT,cluTrkOffset) ):  
                        continue
                    if  (requireECalTimingCoincidence and not myhist.simpleClusterCoincidence(ele1,ele2,cluDeltaT)) or pMag(pSum(ele1.getMomentum(),ele2.getMomentum()))<v0PzMin :
                        continue                     
                    ele1HitInL1=myhist.hasL1Hit(ele1.getTracks()[0])
                    ele2HitInL1=myhist.hasL1Hit(ele2.getTracks()[0])
                    if doTB and ele1.getMomentum()[1]*ele2.getMomentum()[1] <0:
                        myhist.fillTwoBody(ele1,ele2,'EmEm','TB')#potentially comes from WABs
                        if ele1HitInL1 and ele2HitInL1 :  
                            myhist.fillTwoBody(ele1,ele2,'EmEmL1L1','TB') 
                        elif ele1HitInL1 : 
                            myhist.fillTwoBody(ele1,ele2,'EmEmL2L1','TB')
                        elif ele2HitInL1 : 
                            myhist.fillTwoBody(ele1,ele2,'EmEmL1L2','TB')
                        else: 
                            myhist.fillTwoBody(ele1,ele2,'EmEmL2L2','TB')                    
#do analysis for e-gamma pairs 
        if doEmGam: 
            for ele in eleList : 
                if (requireECalTrackTiming and not myhist.clusterTrackCoincidence(ele,cluTrkDeltaT,cluTrkOffset) ):  
                    continue
                for gam in gamList: 
                    gamY=gam.getClusters().First().getPosition()[1]
                    if  requireECalTimingCoincidence and not myhist.clusterCoincidence(ele,gam) :
                        continue
                    if requireWABCoplanarity and not myhist.cutCoplanarity(ele,gam,wabCoplanCut,wabCoplanMean): 
                        continue
                    if pMag(pSum(ele.getMomentum(),gam.getMomentum()))<v0PzMin: 
                        continue
                    eleHitInL1=myhist.hasL1Hit(ele.getTracks()[0])
                    eleHitInL2=myhist.hasLXHit(ele.getTracks()[0],2)
                    eleHitInL3=myhist.hasLXHit(ele.getTracks()[0],3)
                    eleWgt=1.0
                    if weightTracks and isMC and requireECalMatch: 
                        clEle=ele.getClusters()[0]
                        clEcl=clEle.getEnergy()
                        clY=clEle.getPosition()[1]                
                        eleWgt=eff2DEleRatio.GetBinContent(eff2DEleRatio.FindBin(clEcl,clY))
                    if doTB and ele.getMomentum()[1]*gamY<0 : #(these could be WABS!)
                        myhist.fillTwoBody(gam,ele,'GamEm','TB',eleWgt)
                        if eleHitInL1:  
                            myhist.fillTwoBody(gam,ele,'GamEmL1','TB',eleWgt) 
                            if not eleHitInL2 : 
                                myhist.fillTwoBody(gam,ele,'GamEmL1NoL2','TB',eleWgt)
                            else:
                                myhist.fillTwoBody(gam,ele,'GamEmL1L2','TB',eleWgt) 
                        else: 
                            myhist.fillTwoBody(gam,ele,'GamEmL2','TB',eleWgt)  
                    elif  doTT and ele.getMomentum()[1] >0 : 
                        myhist.fillTwoBody(gam,ele,'GamEm','TT',eleWgt)
                    elif  doTT and ele.getMomentum()[1] <0 : 
                        myhist.fillTwoBody(gam,ele,'GamEm','BB',eleWgt)

#do analysis for e-gamma pairs 
        if doEpGam: 
            for pos in posList : 
                if (requireECalTrackTiming and not myhist.clusterTrackCoincidence(pos,cluTrkDeltaT,cluTrkOffset) ):  
                    continue
                for gam in gamList: 
                    gamY=gam.getClusters().First().getPosition()[1]
                    if  requireECalTimingCoincidence and not myhist.clusterCoincidence(pos,gam) :
                        continue
                    if requireWABCoplanarity and not myhist.cutCoplanarity(pos,gam,wabCoplanCut,wabCoplanMean): 
                        continue
                    if pMag(pSum(pos.getMomentum(),gam.getMomentum()))<v0PzMin: 
                        continue
                    posHitInL1=myhist.hasL1Hit(pos.getTracks()[0])
                    posHitInL2=myhist.hasLXHit(pos.getTracks()[0],2)
                    posHitInL3=myhist.hasLXHit(pos.getTracks()[0],3)
                    posWgt=1.0
                    if weightTracks and isMC and requireECalMatch: 
                        clPos=pos.getClusters()[0]
                        clEcl=clPos.getEnergy()
                        clY=clPos.getPosition()[1]                
                        posWgt=eff2DPosRatio.GetBinContent(eff2DPosRatio.FindBin(clEcl,clY))
                    if doTB and pos.getMomentum()[1]*gamY<0 : #(these could be WABS!)
                        myhist.fillTwoBody(gam,pos,'GamEp','TB',posWgt)
                        if posHitInL1:  
                            myhist.fillTwoBody(gam,pos,'GamEpL1','TB',posWgt) 
                            if not posHitInL2 : 
                                myhist.fillTwoBody(gam,pos,'GamEpL1NoL2','TB',posWgt)
                            else:
                                myhist.fillTwoBody(gam,pos,'GamEpL1L2','TB',posWgt) 
                        else: 
                            myhist.fillTwoBody(gam,pos,'GamEpL2','TB',posWgt)  
                    elif  doTT and pos.getMomentum()[1] >0 : 
                        myhist.fillTwoBody(gam,pos,'GamEp','TT',posWgt)
                    elif  doTT and pos.getMomentum()[1] <0 : 
                        myhist.fillTwoBody(gam,pos,'GamEp','BB',posWgt)


    myhist.saveHistograms(output_file)   



    print "******************************************************************************************"
    print "Number of tracks killed = "+str(nKilled)+" out of "+str(nTrks)+" total = "+str(float(nKilled)/nTrks)
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



