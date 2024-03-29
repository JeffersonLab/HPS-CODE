#!/usr/bin/python

#
# @file tridentEfficiencyAnalysis.py
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
from  effHistograms import myHistograms

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
#hps_dst_path += "/libHpsEvent.so"
print "Loading HpsEvent Library from "+hps_dst_path
# Load the library in ROOT
import ROOT
ROOT.gSystem.Load(hps_dst_path)

# import the modules used by HpsEvent i.e. HpsEvent, 
# SvtTrack, EcalCluster ...
from ROOT import HpsEvent, SvtTrack, GblTrack, EcalCluster, EcalHit, TChain, TTree, HpsParticle
from ROOT import RooHistPdf, RooDataHist

#beamEnergy=1.05 #GeV
beamEnergy=2.3 #GeV
beamAngle = 0.0305 #30.5 mrad (nominally)
phot_nom_x = 42.52  #nominal photon position (px=0)
radian = ROOT.TMath.RadToDeg();
#ROOT.PyConfig.IgnoreCommandLineOptions = True

#-----------------#
#--- Functions ---#
#-----------------#


def fixTH1EffBins(hist) :
    nbins=hist.GetNbinsX()
    for i in range(0,nbins):
        print 'bin '+str(i)+':  '+str(hist.GetBinContent(i))


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

def ecalMatchTrack(particleList,ecalCluster) :    
    for particle in particleList :
        if len(particle.getTracks())==0  : continue
#        print 'track charge = '+str(particle.getTracks()[0].getCharge())+'; track phi0 = '+str(particle.getTracks()[0].getPhi0())
        if len(particle.getClusters())==0 : continue
        if particle.getClusters()[0] is ecalCluster : 
#            print 'found track match to cluster'
            return particle
#    print 'Did not find track match' 
    return None 
        

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
    if requireSuperFiducial and not myHistograms.inSuperFiducialRegion(trkCluster.getPosition()[0],trkCluster.getPosition()[1]) : return False
    return True


#given an e+e- pair, try to find a recoil electron return the recoil track if found
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
    for uc_index in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)):
        particle = hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE, uc_index)  
        if particle.getTracks().GetEntries()>0 : continue # no tracks!
        if particle.getClusters().GetEntries() == 0 : continue # yes clusters!        
        potentialWABCluster=particle.getClusters().First()
        if potentialWABCluster.getPosition()[1]*eleSlope>0 : continue  #make sure they are on the opposite sides
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
            
        cl_impact_angleTop = math.atan2(topY, topX - phot_nom_x)*radian
        cl_impact_angleBottom = math.atan2(botY,botX - phot_nom_x)*radian
        if cl_impact_angleTop < 0. :
            cl_impact_angleTop = cl_impact_angleTop + 360. 
        if cl_impact_angleBottom < 0. :
            cl_impact_angleBottom = cl_impact_angleBottom + 360.
        coplanarity=  cl_impact_angleBottom -  cl_impact_angleTop  
    return None
    
#------------------#

def findTridentClusterPair(hps_event): 
    
    return None


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

    if args.energy : 
        print 'Setting beam energy to '+args.energy
        beamEnergy=float(args.energy)

    myhist=myHistograms(beamEnergy) 

#################################
#       Event Selection
################################
#clean up event first
#### nominal selection

    requireECalFiducial = False
    requireECalSuperFiducial = False # this is included as separate histograms now...leave false!
    positronMomentumFromPositionCut = False # this is included as separate histograms now...leave false!
    requireTopBottomCut = True
    requireLeftRightCut = True

    if isMC : 
        smearEnergy=False
        smearRes=0.05
        myhist.setSmearEnergy(smearEnergy,smearRes)


    L1Ele = True  # require L1 hit for Ele
    L1Pos = False # require L1 hit for Pos
    L6Ele = False  # require L1 hit for Ele
    L6Pos = False # require L1 hit for Pos
    trackKiller=True
    killInMomentum=False
    killInClusterPosition=False
    killInTrackSlope = True
#    effFileName='/u/br/mgraham/hps-analysis/TrackEfficiency/cop180_EfficiencyResults.root'
#    effDataName='h_Ecl_hps_005772_eleEff'
#    effMCName='h_Ecl_tritrig-NOSUMCUT_HPS-EngRun2015-Nominal-v5-0_eleEff'

    effFileName='/u/br/mgraham/hps-analysis/TrackEfficiency/cop180_midESum_TwoD-EfficiencyResults.root'
    effDataName='h_XvsY_hps_005772_eleEff'
    effMCName='h_XvsY_tritrig-NOSUMCUT_HPS-EngRun2015-Nominal-v5-0_eleEff'
    
    if isMC and trackKiller and killInClusterPosition : 
        effFile=ROOT.TFile(effFileName)
        print 'Getting data efficiency from '+effFileName 
        #    effData=getEffTH1(effFile,effDataName)
        #    effMC=getEffTH1(effFile,effMCName)
        effData=getEffTH2(effFile,effDataName)
        effMC=getEffTH2(effFile,effMCName)
        effData.Print("v")
        effMC.Print("v")
        effData.Divide(effMC)  # this will be the killing factor
        effData.Print("V")


    if isMC and trackKiller and killInTrackSlope: 
#        effSlopeFileName='/u/br/mgraham/hps-analysis/WABs/EmGamma-L1HitEfficiencyResults.root'
        effSlopeFileName='/u/home/mgraham/HPS-CODE/ANALYSIS/users/mgraham/TridentWABs2016/EmGamma-L1HitEfficiencyResults-2016.root'
        effRatioName='p2slopehps_007963.1GamEm_L1HitInefficiency'
        effSlopeFile=ROOT.TFile(effSlopeFileName)
        effSlopeFile.ls()
        effSlopeData=getEffTH1(effSlopeFile,effRatioName)
        effSlopeData.Print("v")
        print 'L1 Hit Efficiency vs Slope:  MC' 
        fixTH1EffBins(effSlopeData) 


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
    nEvents=0
    nPassBasicCuts=0
    

    
#   //================ Time coincidence ======================================
    coincide_pars_mean = [0.289337,   -2.81998,   9.03475, -12.93,   8.71476,   -2.26969]
    coincide_pars_sigm = [4.3987,   -24.2371,   68.9567, -98.2586,   67.562,   -17.8987]
   
    formula_pol5 = "[0] + x*( [1] + x*( [2] + x*( [3] + x*( [4] + x*( [5] ) ) ) ) ) "
    f_coincide_clust_mean = ROOT.TF1("f_coincide_clust_mean", formula_pol5, 0., 1.4)
    f_coincide_clust_sigm = ROOT.TF1("f_coincide_clust_sigm", formula_pol5, 0., 1.4)
    f_coincide_clust_mean.SetParameters(np.array(coincide_pars_mean))
    f_coincide_clust_sigm.SetParameters(np.array(coincide_pars_sigm))
#   //The cut is            === mean - 3sigma < dt < mean + 3sigma ===

    clTimeMin = 30
    clTimeMax = 50

    if beamEnergy == 2.3 : 
        clTimeMin = 40
        clTimeMax = 65
    energyRatio=beamEnergy/1.05 #ratio of beam energies references to 1.05 GeV (2015 run)
        
    print("Total number of events in tree = "+str(tree.GetEntries()))
    seedCnt=0
    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
                 
        # Print the event number every 500 events
        if (entry+1)%100 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
        if not hps_event.isPair1Trigger() and not isMC and not isPulser: continue
        nEvents+=1
       
      
        nPassBasicCuts+=1
#        print "passed basic cuts"
        pairList=[]
        bestCandidate=-99
        pairsFound=0
        for  i in range(0,hps_event.getNumberOfEcalClusters()) :
            cl1=hps_event.getEcalCluster(i)
            cl1Position=cl1.getPosition()
            cl_xi=cl1Position[0]
            cl_yi=cl1Position[1]
            cl_zi=cl1Position[2]
            cl_ti=cl1.getClusterTime()
            cl_Ei=cl1.getEnergy()
            myhist.h_clTime1vsclE.Fill(cl_Ei,cl_ti)
            cl_di = math.sqrt( (cl_xi - phot_nom_x)*(cl_xi - phot_nom_x) + cl_yi*cl_yi )       
#            print 'looking at clusters' 
            #if(!fid_ECal(cl_xi,cl_yi))
            #        continue            
            if requireECalFiducial and not myhist.inFiducialRegion(cl_xi, cl_yi)  :
                continue
            if requireECalSuperFiducial and not myhist.inSuperFiducialRegion(cl_xi, cl_yi)  :
                continue
            if not (cl_ti > clTimeMin and cl_ti < clTimeMax ):
                continue
            if positronMomentumFromPositionCut and not myhist.momFromPositionEclUpperCut(cl_Ei,myhist.momFromECalPosition(cl_xi,cl_zi,beamAngle,myhist.BEff)) : 
                continue
#            print 'Found first good cluster'
            for  j in range(i+1,hps_event.getNumberOfEcalClusters()) :
                cl2=hps_event.getEcalCluster(j)
                cl2Position=cl2.getPosition()
                cl_xj=cl2Position[0]
                cl_yj=cl2Position[1]
                cl_zj=cl2Position[2]
                cl_tj=cl2.getClusterTime()
                cl_Ej=cl2.getEnergy()

                cl_dj =math.sqrt( (cl_xj - phot_nom_x)*(cl_xj - phot_nom_x) + cl_yj*cl_yj )
                Esum = cl_Ei + cl_Ej
                if  requireECalFiducial and not myhist.inFiducialRegion(cl_xj,cl_yj): 
                    continue
                if  requireECalSuperFiducial and not myhist.inSuperFiducialRegion(cl_xj,cl_yj): 
                    continue
                if not (cl_tj > clTimeMin and cl_tj < clTimeMax ):
                    continue
                if positronMomentumFromPositionCut and not myhist.momFromPositionEclUpperCut(cl_Ej,myhist.momFromECalPosition(cl_xj,cl_zj,beamAngle,myhist.BEff)) : 
                    continue
#                print 'Passed the probable positron cut'
                                
                myhist.h_clTime1vsclTime2.Fill(cl_ti,cl_tj)

                dt = cl_ti - cl_tj
#                delt_t_mean = f_coincide_clust_mean.Eval(Esum)
#                delt_t_sigm = f_coincide_clust_sigm.Eval(Esum) 
#      divide by 2 since these parameters were extracted from 1.05GeV Data (this is kludgy!)    
                delt_t_mean = f_coincide_clust_mean.Eval(Esum/energyRatio)
                delt_t_sigm = f_coincide_clust_sigm.Eval(Esum/energyRatio)         
                if not  (dt < delt_t_mean + 3*delt_t_sigm and dt > delt_t_mean - 3*delt_t_sigm) :
                    continue
#         //make sure they are top/bottom
#                print 'Passed the timing cut' 
#                print str(cl_yi)+"   " + str(cl_yj)
                if requireTopBottomCut and cl_yi*cl_yj>0 :
                    continue

                if requireLeftRightCut and cl_xi*cl_xj>0 :
                    continue

#                print 'Found a pair!!!!' 

                clpair=[cl1,cl2]
                pairList.append(clpair)
                                
        pairsFound+=len(pairList)
#        if len(pairList) >0 : print "found this many pairs "+str(len(pairList))

        fspList=[]
        for i in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)):
            fspList.append( hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE,i))

      
        #########################        
        #   found some candidates...lets fill plots...
        #########################        
        removeL1HitEle=False
        removeL1HitPos=False
        for pair in pairList : 
            if pair[0].getPosition()[1] >0 :
                clTop=pair[0]
                clBottom=pair[1]
            else :
                clTop=pair[1]
                clBottom=pair[0]
            clTopPosition=clTop.getPosition()
            clBottomPosition=clBottom.getPosition()

            topX=clTopPosition[0]
            topY=clTopPosition[1]
            topZ=clTopPosition[2]
            botX=clBottomPosition[0]
            botY=clBottomPosition[1]
            botZ=clBottomPosition[2]
            topE=clTop.getEnergy()
            botE=clBottom.getEnergy()
            Esum=topE+botE
            Ediff=abs(topE-botE)
            cl_impact_angleTop = math.atan2(topY, topX - phot_nom_x)*radian
            cl_impact_angleBottom = math.atan2(botY,botX - phot_nom_x)*radian
            if cl_impact_angleTop < 0. :
                cl_impact_angleTop = cl_impact_angleTop + 360. 
            if cl_impact_angleBottom < 0. :
                cl_impact_angleBottom = cl_impact_angleBottom + 360.
            coplanarity=  cl_impact_angleBottom -  cl_impact_angleTop  
            myhist.h_coplan_Esum1.Fill(Esum,coplanarity)

                
#            cl_d_top= math.sqrt( (topX - phot_nom_x)*(topX - phot_nom_x) + topY*topY )- (60. + 100*(topE - 0.85)*(topE - 0.85) )       
#            cl_d_bottom= math.sqrt( (botX - phot_nom_x)*(botX - phot_nom_x) + botY*botY )- (60. + 100*(botE - 0.85)*(botE - 0.85) )       
            
            #do track matching
            trTop=ecalMatchTrack(fspList,clTop)
            trBottom=ecalMatchTrack(fspList,clBottom)
            #initial PDG assignments
            trEle=trTop
            trPos=trBottom
            clEle=clTop
            clPos=clBottom

            if topX > 0 : #assign the ele & pos with respect to the side of ECAL the cluster is on  
                trEle=trBottom
                clEle=clBottom
                trPos=trTop
                clPos=clTop
            
            if trEle is not None and trEle.getPDG() == -11 :# whoops, it's a positron
                trEle=trBottom
                trPos=trTop
                clEle=clBottom
                clPos=clTop
#            if trPos is not None and trPos.getPDG() == 11 : # whoops, it's an electron
#                trEle=trBottom
#                trPos=trTop
#                clEle=clBottom
#                clPos=clTop
                #for ++ or -- events, this will get flipped twice...live with it...
                

            if topY*botY >0 : 
                print "both clusters in same half?? How could this happen?"+str(topY)+" vs "+str(botY)

            if trackKiller and isMC: 
                if killInMomentum : 
                    p=clEle.getEnergy()
                    bin=effData.FindBin(p)                    
                    tkEff=effData.GetBinContent(bin)
                    print str(p)+ ' '+str(bin)+' '+str(tkEff)
                    if random.random()>tkEff  :  #high ratio of efficiencies, this hardly  kills...low, kills a lot
                        print "REJECTING THIS ELECTRON TRACK!!! "+str(p)
                        trEle=None 
                #### same thing for positron side
                    p=clPos.getEnergy()
                    bin=effData.FindBin(p)                    
                    tkEff=effData.GetBinContent(bin)
                    print str(p)+' '+str(bin)+' '+str(tkEff)
                    if random.random()>tkEff  :  #high ratio of efficiencies, this hardly  kills...low, kills a lot
                        print "REJECTING THIS ELECTRON TRACK!!! "+str(p)
                        trPos=None
                if killInClusterPosition:  
                    clX=clEle.getPosition()[0]
                    clY=clEle.getPosition()[1]
                    bin=effData.FindBin(clX,clY)
                    tkEff=effData.GetBinContent(bin)
                    if random.random()>tkEff  and tkEff!=0.0:  
                        print str(clX)+ ' '+str(clY)+' '+str(bin)+' '+str(tkEff)
                        print "REJECTING THIS ELECTRON TRACK!!! "+str(clX)
                        trEle=None
                    clX=clPos.getPosition()[0]
                    clY=clPos.getPosition()[1]
                    bin=effData.FindBin(-clX+80,clY) # flip sign +80mm for positron side (this isn't strictly correct)!!!
                    tkEff=effData.GetBinContent(bin)                    
                    if random.random()>tkEff and tkEff!=0.0  :  
                        print str(clX)+ ' '+str(clY)+' '+str(bin)+' '+str(tkEff)
                        print "REJECTING THIS POSITRON TRACK!!! "+str(clX)
                        trPos=None

                if killInTrackSlope: 
                    if trEle is not None and len(trEle.getTracks())>0: 
#                        print("found an electron...kill it!!!")
                        trk=trEle.getTracks()[0]
                        nHits=len(trk.getSvtHits())
                        slp=trk.getTanLambda()
                        rndm=random.random()            
                        ibin=effSlopeData.FindBin(slp)
                        eff=1-effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency                        
#                        print(str(rndm)+"    "+str(eff))
                        if rndm>eff: 
                            if nHits==5: 
                                print('Removing this electron  due to L1 inefficiency')
                                trEle=None
                            else :                            
                                print(' Removing this electron L1 hit due to inefficiency')
                                removeL1HitEle=True
                    if trPos is not None and  len(trPos.getTracks())>0: 
#                        print("found an positron...kill it!!!")
                        trk=trPos.getTracks()[0]
                        nHits=len(trk.getSvtHits())
                        slp=trk.getTanLambda()
                        rndm=random.random()            
                        ibin=effSlopeData.FindBin(slp)
                        eff=1-effSlopeData.GetBinContent(ibin) #the slope "efficiency" is actually an inefficiency                        
#                        print(str(rndm)+"    "+str(eff))
                        if rndm>eff: 
                            if nHits==5: 
                                print('Removing this positron due to L1 inefficiency')
                                trPos=None
                            else :                            
                                print('Removing this positron L1 hit due to inefficiency')
                                removeL1HitPos=True


#require layer 1
            if L1Ele and (not myhist.hasL1Hit(trEle) or removeL1HitEle):
                trEle=None
            if L1Pos and (not myhist.hasL1Hit(trPos) or removeL1HitPos):
                trPos=None
#require layer 6
            if L6Ele and not myhist.hasLXHit(trEle,6):
                trEle=None
            if L6Pos and not myhist.hasLXHit(trPos,6):
                trPos=None

            myhist.fillBand("_copAll_",trEle,clEle,trPos,clPos)
            
            if abs(coplanarity-180)<10 :                
                #  some debugging here...
                #  for events where there is a positron track and no electron track
                #  check to see if there maybe is a track that's could be associated with this clus
                if trEle is None and trPos is not None and trPos.getCharge()>0 : 
                    nMatchEle=0;
                    print 'found positron but not electron!  ele energy = '+str(clEle.getEnergy())+'; ele clX = '+str(clEle.getPosition()[0])+'; ele clY = '+str(clEle.getPosition()[1])
                    #loop through the electrons in event and check to see if on is in the same half
                    for fsp_n in xrange(0, hps_event.getNumberOfParticles(HpsParticle.FINAL_STATE_PARTICLE)) :            
                        fsp = hps_event.getParticle(HpsParticle.FINAL_STATE_PARTICLE,fsp_n)
                        if fsp.getType() !=0 : 
                            if  fsp.getType() > 32  : continue
                            track=fsp.getTracks()[0]
                            slope=track.getTanLambda()
                            if fsp.getCharge()<0 and slope*clEle.getPosition()[1]>0 and pMag(fsp.getMomentum())<0.8 : 
                                nMatchEle=nMatchEle+1
                                print 'found and electron in right half!!'
                                print 'track p = '+str(pMag(fsp.getMomentum())) 
                                trkAtEcal=track.getPositionAtEcal()
                                delX=trkAtEcal[0]-clEle.getPosition()[0]
                                delY=trkAtEcal[1]-clEle.getPosition()[1]
                                print 'trk-clEle delX = '+str(delX)+'; delY = '+str(delY)
                                myhist.h_misEle_delXvsdelY.Fill(delX,delY)
                                myhist.h_misEle_trkPvsclE.Fill(pMag(fsp.getMomentum()),clEle.getEnergy())
                                if len(fsp.getClusters())>0 : 
                                    clThisE=fsp.getClusters()[0]
                                    print '...this track matched to cluster with ele energy = '+str(clThisE.getEnergy())+'; ele clX = '+str(clThisE.getPosition()[0])+'; ele clY = '+str(clThisE.getPosition()[1])
########################                    
                    myhist.h_misEle_eleTrks.Fill(nMatchEle)
                myhist.fillBand("_cop180_",trEle,clEle,trPos,clPos)
                if Esum>myhist.midESumLow and Esum<myhist.midESumHigh :
                    myhist.fillBand("_cop180_midESum_",trEle,clEle,trPos,clPos)
                    if myhist.inSuperFiducialRegion(topX,topY) and myhist.inSuperFiducialRegion(botX,botY):
                        myhist.fillBand("_cop180_midESum_SuperFid",trEle,clEle,trPos,clPos)  
                    if not myhist.inSuperFiducialRegion(topX,topY) and not myhist.inSuperFiducialRegion(botX,botY):
                        myhist.fillBand("_cop180_midESum_AntiSuperFid",trEle,clEle,trPos,clPos)
                if myhist.inSuperFiducialRegion(topX,topY) and myhist.inSuperFiducialRegion(botX,botY):
                    myhist.fillBand("_cop180_SuperFid",trEle,clEle,trPos,clPos)  
                    if not myhist.inPhotonHole(topX,topY) and not myhist.inPhotonHole(botX,botY) : 
                        myhist.fillBand("_cop180_SuperFid_CutPhotons",trEle,clEle,trPos,clPos)  
                if not myhist.inSuperFiducialRegion(topX,topY) and not myhist.inSuperFiducialRegion(botX,botY):
                    myhist.fillBand("_cop180_AntiSuperFid",trEle,clEle,trPos,clPos)                      
                if Ediff<0.2 and len(pairList)==1: 
                    myhist.fillBand("_cop180_Holly_",trEle,clEle,trPos,clPos)
                if not myhist.inPhotonHole(topX,topY) and not myhist.inPhotonHole(botX,botY) : 
                    myhist.fillBand("_cop180_CutPhotons",trEle,clEle,trPos,clPos)  
            elif abs(coplanarity-160)<10 :                 
                myhist.fillBand("_cop160_",trEle,clEle,trPos,clPos)
                if Esum>myhist.midESumLow and Esum<myhist.midESumHigh :
                    myhist.fillBand("_cop160_midESum_",trEle,clEle,trPos,clPos)
                if myhist.inSuperFiducialRegion(topX,topY) and myhist.inSuperFiducialRegion(botX,botY):
                    myhist.fillBand("_cop160_SuperFid",trEle,clEle,trPos,clPos)  
#                    if  myhist.momFromPositionEclUpperCut(topE,myhist.momFromECalPosition(topX,topZ,beamAngle,myhist.BEff)) and myhist.momFromPositionEclUpperCut(botE,myhist.momFromECalPosition(botX,botZ,beamAngle,myhist.BEff)): 
                    if not myhist.inPhotonHole(topX,topY) and not myhist.inPhotonHole(botX,botY) : 
                        myhist.fillBand("_cop160_SuperFid_CutPhotons",trEle,clEle,trPos,clPos)  
#                if  myhist.momFromPositionEclUpperCut(topE,myhist.momFromECalPosition(topX,topZ,beamAngle,myhist.BEff)) and myhist.momFromPositionEclUpperCut(botE,myhist.momFromECalPosition(botX,botZ,beamAngle,myhist.BEff)): 
                if not myhist.inPhotonHole(topX,topY) and not myhist.inPhotonHole(botX,botY) : 
                    myhist.fillBand("_cop160_CutPhotons",trEle,clEle,trPos,clPos)  
            


#            particle = hps_event.getParticle(HpsParticle.TC_V0_CANDIDATE, candidateList[index])
#            myhist.fillCandidateHistograms(particle)
          
            

#    if(nPassTrkCuts>0): 
    print "******************************************************************************************"
    myhist.saveHistograms(output_file)   
#    sys.exit(0)
    print "***   Returning ****"
    return
#    print "Number of Events:\t\t",nEvents,"\t\t\t",float(nEvents)/nEvents,"\t\t\t",float(nEvents)/nEvents
#    print "N(particle) Cuts:\t\t",nPassBasicCuts,"\t\t\t",float(nPassBasicCuts)/nEvents,"\t\t\t",float(nPassBasicCuts)/nEvents
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
    print "***   Back in main ****"    
    os._exit(-1)
    print "os exit done"
    sys.exit(0)    
    print "system exit done"



