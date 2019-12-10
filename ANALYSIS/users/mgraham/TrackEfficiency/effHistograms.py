import ROOT 
import math
from ROOT import TLorentzVector
import numpy as np 
import random
me=0.000000511 #kev
class myHistograms:  
    phot_nom_x = 42.52  #nominal photon position (px=0)
    radian = ROOT.TMath.RadToDeg();
    beam=[np.sin(0.0305),0,np.cos(0.0305)]
    beamRotAxis=[0,1,0]
    rotAngle=-0.0305
#    BEff=0.24
    BEff=0.5
    beamAngle = 0.0305


    histogramList=[]
    histDict={}
    
    nbinsSmall=50
    nbinsBig=500

#histogram parameters that don't depend on energy
    mind0=-3
    maxd0=3
#
    minz0=-1.5
    maxz0=1.5
#
    minphi0=-0.25
    maxphi0=0.25
#
    minslope=-0.08
    maxslope=0.08
#
    mincltime=10
    maxcltime=90
#
    mincltimediff=-10
    maxcltimediff=10
#
    minmass=0
    maxmass=0.1
#
    mintrktime=-10
    maxtrktime=10
#
    mintrktimediff=-3
    maxtrktimediff=3
#cluster coplanarity
    mincopl=120
    maxcopl=240
#cluster positions
    minclx=-300
    maxclx=400
    mincly=-100
    maxcly=100
#
    minediff = -1
    maxediff = 1
#
    minpt=-0.02
    maxpt=0.02
#
    minTrkPx=-0.05
    maxTrkPx=0.05
#
    minTrkPy=-0.05
    maxTrkPy=0.05

    smearEnergy=False
    smearRes=0.1  #10%

    def __init__(self,beamEnergy) : 
    

 
        #1.05 GeV by default
        self.BEff=0.24
        self.minClE=0.1
        self.maxClE=0.8
        self.minTrkP=0.1
        self.maxTrkP=0.8
        self.minESum=0.2
        self.maxESum=1.14
        self.midESumLow=0.35
        self.midESumHigh=0.65
        self.clTimeMinCut = 30
        self.clTimeMaxCut = 50
        self.energyRatio=beamEnergy/1.05
        if beamEnergy == 2.3 : 
            self.minClE=0.2
            self.maxClE=1.6
            self.minTrkP=0.2
            self.maxTrkP=1.6
            self.minESum=0.4
            self.maxESum=2.5
            self.BEff=0.5
#            self.midESumLow=self.midESumLow*2.3/1.05
            self.midESumLow=0.9
            self.midESumHigh=1.6
            self.BEff=0.5
            self.clTimeMinCut = 40
            self.clTimeMaxCut = 65
        

        self.h_coplan_Esum1 = ROOT.TH2D("h_coplan_Esum1", "", 200, self.minESum, self.maxESum, 200, 120., 240.)  
        self.h_clTime1vsclTime2 = ROOT.TH2D("h_clTime1vsclTime2", "", 100,self.clTimeMinCut,self.clTimeMaxCut, 100, self.clTimeMinCut,self.clTimeMaxCut)
        self.h_clTime1vsclE = ROOT.TH2D("h_clTime1vsclE", "", 100, self.minClE,self.maxClE, 100, self.clTimeMinCut,self.clTimeMaxCut)
        self.h_E1vsE2_cop180 = ROOT.TH2D("h_E1vsE2_cop180", "", 200, self.minClE, self.maxClE, 200,  self.minClE, self.maxClE)
#        self.h_Ecl_midESum_coplanarity=ROOT.TH1D("h_Ecl_midESum_coplanarity","h_Ecl_midESum_coplanarity",100,120,240)

        self.histogramList.append(self.h_coplan_Esum1)
        self.histogramList.append( self.h_clTime1vsclTime2)
        self.histogramList.append( self.h_clTime1vsclE)
        self.histogramList.append( self.h_E1vsE2_cop180)
        
        self.h_Ecl_Ptrk_from_position_WAB_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_WAB_ele","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        self.h_Ecl_Ptrk_from_position_WAB_pho=ROOT.TH2D("h_Ecl_Ptrk_from_position_WAB_pho","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_WAB_ele)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_WAB_pho)

        self.h_Ecl_Ptrk_from_position_Tri_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_ele","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        self.h_Ecl_Ptrk_from_position_Tri_pos=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_pos","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        self.h_Ecl_Ptrk_from_position_Tri_misele=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_misele","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        self.h_Ecl_Ptrk_from_position_Tri_mispos=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_mispos","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        self.h_Ptrk_Ptrk_from_position_Tri_ele=ROOT.TH2D("h_Ptrk_Ptrk_from_position_Tri_ele","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)
        self.h_Ptrk_Ptrk_from_position_Tri_pos=ROOT.TH2D("h_Ptrk_Ptrk_from_position_Tri_pos","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP)

        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_ele)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_pos)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_misele)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_mispos)
        self.histogramList.append(self.h_Ptrk_Ptrk_from_position_Tri_ele)
        self.histogramList.append(self.h_Ptrk_Ptrk_from_position_Tri_pos)
        
        self.h_E1vsE2_cop160 = ROOT.TH2D("h_E1vsE2_cop160", "", 200,self.minClE,self.maxClE, 200,  self.minClE, self.maxClE)

        self.h_misEle_eleTrks=ROOT.TH1D("h_misEle_eleTrks","h_misEle_eleTrks",5,0,5)
        self.h_misEle_delXvsdelY = ROOT.TH2D("h_misEle_delXvsdelY", "h_misEle_delXvsdelY", 50,-150,150, 50,-150,150)
        self.h_misEle_trkPvsclE = ROOT.TH2D("h_misEle_trkPvsclE","h_misEle_trkPvsclE",50,0,1,50,0,1)
        self.histogramList.append(self.h_misEle_eleTrks)
        self.histogramList.append(self.h_misEle_delXvsdelY)
        self.histogramList.append(self.h_misEle_trkPvsclE)
     
        
    #   /////////////////////////////////////////////////////////
        self.h_EclX_EclY_ElectronPositron = ROOT.TH2D("h_EclX_EclY_ElectronPositron","",100,-400,400,100,-100,100)
      #  self.histogramList.append(self.h_EclX_EclY_ElectronPositron);
              

        self.h_EclX_EclY_TwoPhotons = ROOT.TH2D("h_EclX_EclY_TwoPhotons","",100,-400,400,100,-100,100);
        self.h_Ecl_Ptrk_from_position_TwoPhotons_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_TwoPhotons_ele","",100,self.minClE,self.maxClE,100,self.minTrkP,self.maxTrkP);        
     
        #    self.histogramList.append(self.h_EclX_EclY_TwoPhotons)
        #    self.histogramList.append(self.h_Ecl_Ptrk_from_position_TwoPhotons_ele)
    
        
    def setEnergyScales(self, ebeam)  :
        # modify scales if we need to
        return



    #takes in an HpsParticle candidate and makes plots
    #use this for reconstructed events
    def fillCandidateHistograms(self,particle, ucparticle = None) :
        #fill histograms
        return
        
      
    def fillBand(self,bandName,trEle,clEle,trPos,clPos) : 
        cl_x_ele=clEle.getPosition()[0]
        cl_y_ele=clEle.getPosition()[1]
        cl_z_ele=clEle.getPosition()[2]
        cl_E_ele=clEle.getEnergy()

        cl_x_pos=clPos.getPosition()[0]
        cl_y_pos=clPos.getPosition()[1]
        cl_z_pos=clPos.getPosition()[2]
        cl_E_pos=clPos.getEnergy()

        if self.smearEnergy : 
            cl_E_ele=self.smearSomething(cl_E_ele,self.smearRes)

        if self.smearEnergy : 
            cl_E_pos=self.smearSomething(cl_E_pos,self.smearRes)

        Esum=cl_E_ele+cl_E_pos

            

        hname="h_ESum"+bandName
        what="AllPairs"
        val=Esum
        self.fill1DHistogram(hname,what,self.nbinsSmall,self.minESum,self.maxESum,val)

        hname="h_coplanarity"+bandName
        what=""
        val=self.getECalCoplanarity(clEle,clPos)
        self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincopl,self.maxcopl,val)

        hname="h_XvsY"+bandName
        what="AllPairs"
        valx=cl_x_ele
        valy=cl_y_ele
        self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

        hname="h_XvsY"+bandName
        what="AllPairs"
        valx=cl_x_pos
        valy=cl_y_pos
        self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

        hname="h_E1vsE2"+bandName
        what="AllPairs"
        valx=cl_E_ele
        valy=cl_E_pos
        self.fill2DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,self.nbinsSmall,self.minClE,self.maxClE,valx,valy)

        eleMomFromPosition=self.momFromECalPosition(cl_x_ele,cl_z_ele,self.beamAngle,self.BEff)
        posMomFromPosition=self.momFromECalPosition(cl_x_pos,cl_z_pos,self.beamAngle,self.BEff)
        if trEle is not None and trPos is not None :
            if trEle.getPDG() == trPos.getPDG() : 
                print "Same sign! PDG ID = "+str( trEle.getPDG())+"...Bailing..."
                return
            tr_p_ele=self.pMag(trEle.getMomentum())
            tr_p_pos=self.pMag(trPos.getMomentum())
            
            trEleTrk=trEle.getTracks()[0]
            trPosTrk=trPos.getTracks()[0]


            self.h_EclX_EclY_ElectronPositron.Fill(cl_x_ele,cl_y_ele)
            self.h_EclX_EclY_ElectronPositron.Fill(cl_x_pos,cl_y_pos)
           
            self.h_Ecl_Ptrk_from_position_Tri_ele.Fill(cl_E_ele,eleMomFromPosition)                      
            self.h_Ecl_Ptrk_from_position_Tri_pos.Fill(cl_E_pos,posMomFromPosition)            
            self.h_Ptrk_Ptrk_from_position_Tri_ele.Fill(tr_p_ele,eleMomFromPosition)
            self.h_Ptrk_Ptrk_from_position_Tri_pos.Fill(tr_p_pos,posMomFromPosition)

            hname="h_E1vsE2"+bandName
            what="bothtracks"
            valx=cl_E_ele
            valy=cl_E_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,self.nbinsSmall,self.minClE,self.maxClE,valx,valy)
            
            hname="h_XvsY"+bandName
            what="bothtracks"
            valx=cl_x_ele
            valy=cl_y_ele
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
            what="ele_side_found_pos"
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
            what="ele_side_found_pos_found_ele"
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

            hname="h_eleSlope"+bandName
            what="bothtracks"
            val=trEleTrk.getTanLambda()
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minslope,self.maxslope,val)

            hname="h_posSlope"+bandName
            what="bothtracks"
            val=trPosTrk.getTanLambda()
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minslope,self.maxslope,val)

            hname="h_elePhi0"+bandName
            what="bothtracks"
            val=math.sin(trEleTrk.getPhi0())
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minphi0,self.maxphi0,val)

            hname="h_posPhi0"+bandName
            what="bothtracks"
            val=math.sin(trPosTrk.getPhi0())
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minphi0,self.maxphi0,val)



            hname="h_XvsY"+bandName
            what="bothtracks"
            valx=cl_x_pos
            valy=cl_y_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
            what="pos_side_found_ele"
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
            what="pos_side_found_ele_found_pos"
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

            hname="h_E1vsE2"+bandName
            what="bothtracks"
            valx=cl_E_ele
            valy=cl_E_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,self.nbinsSmall,self.minClE,self.maxClE,valx,valy)

            hname="h_ESum"+bandName
            what="bothtracks"
            val=Esum
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minESum,self.maxESum,val)

            hname="h_Ecl"+bandName
            val=cl_E_pos
            what="positron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            what="pos_side_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            what="pos_side_found_ele_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
#
            val=cl_E_ele
            what="electron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            what="ele_side_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            what="ele_side_found_pos_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
#
            hname="h_EclX"+bandName
            val=cl_x_pos
            what="positron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,val)
            what="pos_side_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,val)
            what="pos_side_found_ele_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,val)
#
            val=cl_x_ele
            what="electron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minclx,0,val)
            what="ele_side_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minclx,0,val)
            what="ele_side_found_pos_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minclx,0,val)
#
            hname="h_EclY"+bandName
            val=cl_y_pos
            what="positron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            what="pos_side_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            what="pos_side_found_ele_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
#
            val=cl_y_ele
            what="electron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            what="ele_side_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            what="ele_side_found_pos_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)

        elif trEle is not None : #but trPos is...just found electron 
            if trEle.getCharge()>0 : 
#                print "found an positron on electron side" 
                return

            trEleTrk=trEle.getTracks()[0]

            hname="h_eleSlope"+bandName
            what="eletrack_only"
            val=trEleTrk.getTanLambda()
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minslope,self.maxslope,val)

            hname="h_elePhi0"+bandName
            what="eletrack_only"
            val=math.sin(trEleTrk.getPhi0())
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minphi0,self.maxphi0,val)

            hname="h_E1vsE2"+bandName
            what="eletrack_only"
            valx=cl_E_ele
            valy=cl_E_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,self.nbinsSmall,self.minClE,self.maxClE,valx,valy)
            hname="h_XvsY"+bandName
            what="eletrack_only"
            valx=cl_x_ele
            valy=cl_y_ele
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)


            hname="h_XvsY"+bandName
            what="eletrack_only"
            valx=cl_x_pos
            valy=cl_y_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
            what="pos_side_found_ele"
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

            hname="h_ESum"+bandName
            what="eletrack_only"
            val=Esum
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minESum,self.maxESum,val)
            self.h_Ecl_Ptrk_from_position_Tri_mispos.Fill(cl_E_pos,posMomFromPosition)
            hname="h_Ecl"+bandName
            val=cl_E_ele
            what="electron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            
            hname="h_Ecl"+bandName
            val=cl_E_pos
            what="mis_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            what="pos_side_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)

            hname="h_EclX"+bandName
            val=cl_x_ele
            what="electron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minclx,0,val)
            val=cl_x_pos
            what="mis_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,val)
            what="pos_side_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,val)

            hname="h_EclY"+bandName
            val=cl_y_ele
            what="electron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            val=cl_y_pos
            what="mis_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            what="pos_side_found_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            
        elif trPos is not None : #but trEle is...just found positron
            if trPos.getCharge()<0 : 
#                print "found an electron on positron side" 
                return

            trPosTrk=trPos.getTracks()[0]

            hname="h_posSlope"+bandName
            what="postrack_only"
            val=trPosTrk.getTanLambda()
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minslope,self.maxslope,val)

            hname="h_posPhi0"+bandName
            what="postrack_only"
            val=math.sin(trPosTrk.getPhi0())
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minphi0,self.maxphi0,val)

            hname="h_E1vsE2"+bandName
            what="postrack_only"
            valx=cl_E_ele
            valy=cl_E_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,self.nbinsSmall,self.minClE,self.maxClE,valx,valy)

            hname="h_XvsY"+bandName
            what="postrack_only"
            valx=cl_x_ele
            valy=cl_y_ele
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
            what="ele_side_found_pos"
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

            hname="h_E2XvsY"+bandName
            what="postrack_only"
            valx=cl_x_pos
            valy=cl_y_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

            hname="h_ESum"+bandName+""
            what="postrack_only"
            val=Esum
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minESum,self.maxESum,val)
            self.h_Ecl_Ptrk_from_position_Tri_misele.Fill(cl_E_ele,eleMomFromPosition)

            hname="h_Ecl"+bandName
            val=cl_E_pos
            what="positron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            
            hname="h_Ecl"+bandName
            val=cl_E_ele
            what="mis_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)
            what="ele_side_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,val)

            hname="h_EclX"+bandName
            val=cl_x_pos
            what="positron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,val)
            val=cl_x_ele
            what="mis_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minclx,0,val)
            what="ele_side_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minclx,0,val)

            hname="h_EclY"+bandName
            val=cl_y_pos
            what="positron"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            val=cl_y_ele
            what="mis_ele"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)
            what="ele_side_found_pos"
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.mincly,self.maxcly,val)

        else : # no tracks!!!
            hname="h_E1vsE2"+bandName
            what="notracks"
            valx=cl_E_ele
            valy=cl_E_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minClE,self.maxClE,self.nbinsSmall,self.minClE,self.maxClE,valx,valy)

            hname="h_ESum"+bandName
            what="notracks"
            val=Esum
            self.fill1DHistogram(hname,what,self.nbinsSmall,self.minESum,self.maxESum,val)

            hname="h_XvsY"+bandName
            what="notracks_eleside"
            valx=cl_x_ele
            valy=cl_y_ele
            self.fill2DHistogram(hname,what,self.nbinsSmall,self.minclx,0,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)

            hname="h_XvsY"+bandName
            what="notracks_posside"
            valx=cl_x_pos
            valy=cl_y_pos
            self.fill2DHistogram(hname,what,self.nbinsSmall,0,self.maxclx,self.nbinsSmall,self.mincly,self.maxcly,valx,valy)
#            print 'No Tracks!  pos clY = '+str(cl_y_pos)+'; ele clY = '+str(cl_y_ele)


    #take a rootfile with already filled histograms 
    #and add them to the current set
    def addHistograms(self, rootfile) : 
        for hist in self.histogramList :
            hname=hist.GetName()
#            print hname
            temphist=rootfile.Get(hname)
#            print type(temphist)
            if temphist is not None : 
                hist.Add(temphist)

    def truthAcceptanceCuts(self, pE,pP) :
        slopeCutLow=0.017
        slopeCutHigh=0.065
        ECutLow=0.2
        ECutHigh=0.8
        ESumLow=0.55
        if abs(self.getSlope(pE))<slopeCutLow or abs(self.getSlope(pE)) > slopeCutHigh:
            return False
        if abs(self.getSlope(pP))<slopeCutLow or abs(self.getSlope(pP)) > slopeCutHigh:
            return False
        if pE.E() > ECutHigh or pE.E() < ECutLow : 
            return False
        if pP.E() > ECutHigh or pP.E() < ECutLow : 
            return False
        if pP.E()+pE.E() < ESumLow : 
            return False        
        return True

    def saveHistograms(self,fileName) :
         out=ROOT.TFile(fileName,"RECREATE")
         for hist in self.histogramList : 
             hist.Write()
         out.Close()

    def getPhi0(self,p) :
        return math.atan(p.X()/p.Z())

    def getSlope(self,p) : 
        return math.atan(p.Y()/p.Z())

    def getPolarAngle(p): 
        pt = math.sqrt(p[0]*p[0]+p[1]*p[1])
        pmag=pMag(p)
        return math.asin(pt/pmag)

    def rotateFourMomentum(self,pFour,rotMatrix): 
        pArray=[pFour.X(),pFour.Y(),pFour.Z()]
        pRot= np.dot(rotMatrix,np.asarray(pArray))                 
        p=TLorentzVector(0,0,0,me)
        p.SetPx(float(pRot[0]))
        p.SetPy(float(pRot[1]))
        p.SetPz(float(pRot[2]))
        p.SetE(float(pFour.E()))
        return p

    def getLorentzVector(self, mom):
        p=TLorentzVector(0,0,0,me)
        p.SetPx(float(mom[0]))
        p.SetPy(float(mom[1]))
        p.SetPz(float(mom[2]))
        p.SetE(float(self.pMag(mom)))
    #    p.Print()
        return p 

    def pMag(self,p1) :
        return  math.sqrt(p1[0]*p1[0] + p1[1]*p1[1] + p1[2]*p1[2])


    def rotation_matrix(self,axis, theta):
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


 # calculate the coplanarity of the e+, e-, and the beam
    def getCoplanarity(self, pEle,pPos) :                                          
        normEle=np.linalg.norm(pEle.Vect())
        normPos=np.linalg.norm(pPos.Vect())
        peleArray=np.asarray(pEle.Vect())
        pposArray=np.asarray(pPos.Vect())            
        coplanarity=np.dot(self.beam,(np.cross(peleArray,pposArray)))/normEle/normPos
        return coplanarity

#   ECal fiducial region from Rafo
    def inFiducialRegion(self, x, y) :
        in_fid=False
        x_edge_low = -262.74
        x_edge_high = 347.7
        y_edge_low = 33.54
        y_edge_high = 75.18
        
        x_gap_low = -106.66
        x_gap_high = 42.17
        y_gap_high = 47.18

        y=abs(y)

        if x>x_edge_low and x < x_edge_high and y > y_edge_low and y < y_edge_high :
            if not (x > x_gap_low and x < x_gap_high and y > y_edge_low and y < y_gap_high) : 
                in_fid = True
    
        return in_fid

    def inElectronHoleRegion(self, x, y) :
        in_hole=False
        x_edge_low = -262.74
        x_edge_high = 347.7
        y_edge_low = 33.54
        y_edge_high = 75.18
        
        x_gap_low = -106.66
        x_gap_high = 42.17
        y_gap_high = 47.18

        y=abs(y)

        if x>x_edge_low and x < x_edge_high and y > y_edge_low and y < y_edge_high :
            if x > x_gap_low and x < x_gap_high and y > y_edge_low and y < y_gap_high : 
                in_hole=True

        return


    def radiusFromECal(self,  x, z,  b) : 
        return math.sqrt(1+b*b)*(x*x+z*z)/(2*(x-b*z))

    def momFromECalPosition(self, x, z, b, BEff) :
        return self.momFromRadius(self.radiusFromECal(x,z,b),BEff)
    
    def momFromRadius(self,rad,BEff) :
        return abs(rad*BEff*2.99792458e-4)


    @staticmethod
    def inPhotonHole(x,y) : 
        #ranges below for for being _in_ the photon hole
        x_low=20.0   #NOT absolute value ... only one side
        x_high=115.0
        y_low=25.0  #YES absolute value ... top or bottom
        y_high=40.0 

        if x>x_low and x<x_high : 
            return True
        if abs(y)>y_low and abs(y)<y_high : 
            return True
        return False


    @staticmethod
    def inSuperFiducialRegion(x, y) :
        in_fid=False
        x_edge_low = -262.74
        x_edge_high = 347.7
        y_edge_low = 33.54
        y_edge_high = 75.18
        
        x_gap_low = -106.66
        x_gap_high = 42.17
        y_gap_high = 47.18
        
        #set y_edge_low to the y of the electron gap!
        y_edge_low=y_gap_high

        y=abs(y)

        if x>x_edge_low and x < x_edge_high and y > y_edge_low and y < y_edge_high :
            if not (x > x_gap_low and x < x_gap_high and y > y_edge_low and y < y_gap_high) : 
                in_fid = True
    
        return in_fid

    
    def momFromPositionEclUpperCut(self,Ecl,  mFromPosition) : 
#        slp=1.176
        slp=1.176*2 #x2 since these numbers were calculated for 1.05 GeV
        b=0.182
        cutVal=Ecl*slp+b 
        if mFromPosition>cutVal :
            return False
        return True
    

#//================== Energy slope cut =============================
    def energySlopeCut(cl_x, cl_d,  cl_E) :
        return cl_x > 0 and cl_d > (60. + 100*(cl_E - 0.85)*(cl_E - 0.85)) and cl_E < 0.82
#  // cl_x > 0 : this selects non-negatives (photon ot e+)
#  // cl_E < 0.82 : We don't have (almost don't have) positrons with energies higher that this energy
#  // cl_d > 60. + 100*(cl_E - 0.85)^2: the energy slope cut
#//================= End of Energy slope cut =======================      


#    def matchTrack(self,hpsevent, ecalCluster) : 
  
#        delECut=0.5
#        delXCut=30
#        delYCut=30
#        tr=-99
  
#        for i in range(0,hpsevent.getNumberOfGblTracks()) : 
#            cl_E=ecalCluster.getEnergy()
#            cl_x=ecalCluster.getPosition()[0]
#            cl_y=ecalCluster.getPosition()[1]
#            track=hpsevent.getGblTrack(i)
#            tr_p=self.pMag(track.getMomentum())
#            tr_x=track.getPositionAtEcal()[0]# I don't the these positions have been exposed!!!  
#            tr_y=track.getPositionAtEcal()[1]# no getter
#            if abs(tr_p[i]-cl_E[cl])>delECut : 
#                continue
#            if abs(tr_x[i]-cl_x[cl])>delXCut :
#                continue
#            if abs(tr_y[i]-cl_y[cl])>delYCut :
#                continue
#            tr=i    
#            
#        return tr
    
    
    
    def pMag(self,p1) :
        return  math.sqrt(p1[0]*p1[0] + p1[1]*p1[1] + p1[2]*p1[2])

    
    def getImpactAngle(self,x,y) :
        global  phot_nom_x 
        cl_impact_angle = math.atan2(Y, X - phot_nom_x)*self.radian
        if cl_impact_angle < 0. :
            cl_impact_angle = cl_impact_angle + 360. 


    def book1DHistogram(self,hname,what,nbins,minX,maxX) : 
        name=hname+what
        title=hname+what
        self.histogramList.append(ROOT.TH1D(name,title,nbins,minX,maxX))
        try : 
            foodict=self.histDict[hname] 
        except KeyError, e:
            self.histDict[hname]={}
            
        self.histDict[hname][what]=self.histogramList[-1]
                    
    def fill1DHistogram(self,hname,what,nbins,minX,maxX,val) : 
        try :
            hist=self.histDict[hname][what]; 
        except KeyError, e:
            self.book1DHistogram(hname,what,nbins,minX,maxX)
            
        self.histDict[hname][what].Fill(val)

    def book2DHistogram(self,hname,what,nbinsx,minX,maxX,nbinsy,minY,maxY) : 
        name=hname+what
        title=hname+what
        self.histogramList.append(ROOT.TH2D(name,title,nbinsx,minX,maxX,nbinsy,minY,maxY))
        try : 
            foodict=self.histDict[hname] 
        except KeyError, e:
            self.histDict[hname]={}
        self.histDict[hname][what]=self.histogramList[-1]
                    
    def fill2DHistogram(self,hname,what,nbinsx,minX,maxX,nbinsy,minY,maxY,valx,valy) : 
        try :
            hist=self.histDict[hname][what]
        except KeyError, e:
            self.book2DHistogram(hname,what,nbinsx,minX,maxX,nbinsy,minY,maxY)
            
        self.histDict[hname][what].Fill(valx,valy)


    def getECalCoplanarity(self,cl1,cl2) : 
        if cl1.getPosition()[1] >0 :
            clTop=cl1
            clBottom=cl2
        else :
            clTop=cl2
            clBottom=cl1
        clTopPosition=clTop.getPosition()
        clBottomPosition=clBottom.getPosition()

        topX=clTopPosition[0]
        topY=clTopPosition[1]
        botX=clBottomPosition[0]
        botY=clBottomPosition[1]
        topE=clTop.getEnergy()
        botE=clBottom.getEnergy()
        Esum=topE+botE
        cl_impact_angleTop = math.atan2(topY, topX - self.phot_nom_x)*self.radian
        cl_impact_angleBottom = math.atan2(botY,botX - self.phot_nom_x)*self.radian
        if cl_impact_angleTop < 0. :
            cl_impact_angleTop = cl_impact_angleTop + 360. 
        if cl_impact_angleBottom < 0. :
            cl_impact_angleBottom = cl_impact_angleBottom + 360.
        return cl_impact_angleBottom -  cl_impact_angleTop  

    def smearSomething(self,inVal,sigma) : 
        return random.gauss(inVal,inVal*sigma)

    def setSmearEnergy(self,doit,res) : 
        self.smearEnergy=doit
        self.smearRes=res


    def getEffTH1(self,hfile, hname) : 
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
#########   check if track has a hit in layer 1
    @staticmethod
    def hasL1Hit(trk):         
        if trk == None : 
            return False
        for hit in trk.getTracks().At(0).getSvtHits() : 
            if hit.getLayer() == 1 : 
                return True
        return False
#########   check if track has a hit in layer X
    @staticmethod
    def hasLXHit(trk,layer): 
        if trk == None : 
            return False
        for hit in trk.getTracks().At(0).getSvtHits() : 
            if hit.getLayer() == layer : 
                return True
        return False
