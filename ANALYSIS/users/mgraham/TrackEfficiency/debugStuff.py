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
#        print  str(cl_impact_angleTop)+'   '+str(cl_impact_angleBottom)
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
        

    
    seedCnt=0
    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 
                 
        # Print the event number every 500 events
        if (entry+1)%10000 == 0 : print "Event " + str(entry+1)
        tree.GetEntry(entry)
        if not hps_event.isPair1Trigger() and not isMC and not isPulser: continue
        nEvents+=1
       
      
        nPassBasicCuts+=1
#        print "passed basic cuts"
        pairList=[]
        bestCandidate=-99
        pairsFound=0
        print 'looking at mcparticles' 
        for i in range(0,hps_event.n_mc_particles) : 
            mcp=hps_event.getMCParticle(i)
            print type(mcp)
            if mcp is None : break            
            if mcp.getEnergy() is None: 
                print 'no PDGID'
                continue
            else : 
                print mcp.getEnergy()

        print '....done' 

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
#         //      if(!energySlopeCut(cl_xj,cl_d,cl_Ej))
#         //        continue
                if  requireECalFiducial and not myhist.inFiducialRegion(cl_xj,cl_yj): 
                    continue
                if  requireECalSuperFiducial and not myhist.inSuperFiducialRegion(cl_xj,cl_yj): 
                    continue
                if not (cl_tj > clTimeMin and cl_tj < clTimeMax ):
                    continue
#                print 'Found second good cluster'
#                //if(!fid_ECal(cl_x[j],cl_y[j]))
#         //  continue
#         //      if(!(energySlopeCut(cl_xi,cl_di,cl_Ei) || energySlopeCut(cl_xj,cl_dj,cl_Ej)))
#         //   continue
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
            
#            if trEle is not None and trEle.getPDG() == -11 :# whoops, it's a positron
#                trEle=trBottom
#                trPos=trTop
#                clEle=clBottom
#                clPos=clTop
#            if trPos is not None and trPos.getPDG() == 11 : # whoops, it's an electron
#                trEle=trBottom
#                trPos=trTop
#                clEle=clBottom
#                clPos=clTop
                #for ++ or -- events, this will get flipped twice...live with it...
                

            if topY*botY >0 : 
                print "both clusters in same half?? How could this happen?"+str(topY)+" vs "+str(botY)

#            print coplanarity
            myhist.fillBand("_copAll_",trEle,clEle,trPos,clPos)
            
            if abs(coplanarity-180)<10 :                 
                myhist.fillBand("_cop180_",trEle,clEle,trPos,clPos)
                if Esum>myhist.midESumLow and Esum<myhist.midESumHigh :
                    myhist.fillBand("_cop180_midESum_",trEle,clEle,trPos,clPos)
                if myhist.inSuperFiducialRegion(topX,topY) and myhist.inSuperFiducialRegion(botX,botY):
                    myhist.fillBand("_cop180_SuperFid",trEle,clEle,trPos,clPos)  
#                    if  myhist.momFromPositionEclUpperCut(topE,myhist.momFromECalPosition(topX,topZ,beamAngle,myhist.BEff)) and myhist.momFromPositionEclUpperCut(botE,myhist.momFromECalPosition(botX,botZ,beamAngle,myhist.BEff)): 
                    if not myhist.inPhotonHole(topX,topY) and not myhist.inPhotonHole(botX,botY) : 
                        myhist.fillBand("_cop180_SuperFid_CutPhotons",trEle,clEle,trPos,clPos)  
                if Ediff<0.2 and len(pairList)==1: 
                    myhist.fillBand("_cop180_Holly_",trEle,clEle,trPos,clPos)
#                if  myhist.momFromPositionEclUpperCut(topE,myhist.momFromECalPosition(topX,topZ,beamAngle,myhist.BEff)) and myhist.momFromPositionEclUpperCut(botE,myhist.momFromECalPosition(botX,botZ,beamAngle,myhist.BEff)): 
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
    myhist.saveHistograms(output_file)   

#    print "******************************************************************************************"
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



