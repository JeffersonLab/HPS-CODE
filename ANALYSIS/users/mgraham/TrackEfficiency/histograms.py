import ROOT 
import math
from ROOT import TLorentzVector
import numpy as np 
me=0.000000511 #kev
class myHistograms:  
    
    beam=[np.sin(0.0305),0,np.cos(0.0305)]
    beamRotAxis=[0,1,0]
    rotAngle=-0.0305
#    BEff=0.24
    BEff=0.5
    beamAngle = 0.0305
    midESumLow=0.25*2.3/1.05
    midESumHigh=0.70*2.3/1.05


    histogramList=[]
    
    nbinsSmall=50
    nbinsBig=500

    def __init__(self,beamEnergy) : 
    
        #1.05 GeV by default
        minClE=0.2
        maxClE=0.8
        minTrkP=0.2
        maxTrkP=1.5
        minESum=0.2
        maxESum=1.14
        self.midESumLow=0.45
        self.midESumHigh=0.65
        if beamEnergy == 2.3 : 
            minClE=0.4
            maxClE=1.5
            minTrkP=0.2
            maxTrkP=2.5
            minESum=0.4
            minESum=2.5
            self.BEff=0.5
#            self.midESumLow=self.midESumLow*2.3/1.05
            self.midESumHigh=self.midESumHigh*0.9*2.3/1.05
            self.midESumLow=1.1
            self.midESumHigh=1.9

        self.h_coplan_Esum1 = ROOT.TH2D("h_coplan_Esum1", "", 200, minESum, maxESum, 200, 120., 240.)  
        self.h_clTime1vsclTime2 = ROOT.TH2D("h_clTime1vsclTime2", "", 100, 40,70, 100, 40,70)
        self.h_clTime1vsclE = ROOT.TH2D("h_clTime1vsclE", "", 100, minClE,maxClE, 100, 20,80)
        self.h_E1vsE2_cop180 = ROOT.TH2D("h_E1vsE2_cop180", "", 200, minClE, maxClE, 200,  minClE, maxClE)
        self.h_ESum_cop180 = ROOT.TH1D("h_ESum_cop180","",100,minESum,maxESum)
        self.h_ESum_cop180_bothtracks = ROOT.TH1D("h_ESum_cop180_bothtracks","",100,minESum,maxESum)
        self.h_ESum_cop180_eletrack = ROOT.TH1D("h_ESum_cop180_eletrack","",100,minESum,maxESum)
        self.h_ESum_cop180_postrack = ROOT.TH1D("h_ESum_cop180_postrack","",100,minESum,maxESum)
        self.h_ESum_cop180_notracks = ROOT.TH1D("h_ESum_cop180_notracks","",100,minESum,maxESum)

        self.histogramList.append(self.h_coplan_Esum1)
        self.histogramList.append( self.h_clTime1vsclTime2)
        self.histogramList.append( self.h_clTime1vsclE)
        self.histogramList.append( self.h_E1vsE2_cop180)
        self.histogramList.append(self.h_ESum_cop180)
        self.histogramList.append( self.h_ESum_cop180_bothtracks)
        self.histogramList.append( self.h_ESum_cop180_eletrack)
        self.histogramList.append( self.h_ESum_cop180_postrack)
        self.histogramList.append( self.h_ESum_cop180_notracks)
   
        self.h_Ecl_Ptrk_from_position_WAB_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_WAB_ele","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        self.h_Ecl_Ptrk_from_position_WAB_pho=ROOT.TH2D("h_Ecl_Ptrk_from_position_WAB_pho","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_WAB_ele)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_WAB_pho)

        self.h_Ecl_Ptrk_from_position_Tri_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_ele","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        self.h_Ecl_Ptrk_from_position_Tri_pos=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_pos","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        self.h_Ecl_Ptrk_from_position_Tri_misele=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_misele","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        self.h_Ecl_Ptrk_from_position_Tri_mispos=ROOT.TH2D("h_Ecl_Ptrk_from_position_Tri_mispos","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        self.h_Ptrk_Ptrk_from_position_Tri_ele=ROOT.TH2D("h_Ptrk_Ptrk_from_position_Tri_ele","",100,minClE,maxClE,100,minTrkP,maxTrkP)
        self.h_Ptrk_Ptrk_from_position_Tri_pos=ROOT.TH2D("h_Ptrk_Ptrk_from_position_Tri_pos","",100,minClE,maxClE,100,minTrkP,maxTrkP)

        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_ele)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_pos)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_misele)
        self.histogramList.append(self.h_Ecl_Ptrk_from_position_Tri_mispos)
        self.histogramList.append(self.h_Ptrk_Ptrk_from_position_Tri_ele)
        self.histogramList.append(self.h_Ptrk_Ptrk_from_position_Tri_pos)
        
        self.h_E1vsE2_cop160 = ROOT.TH2D("h_E1vsE2_cop160", "", 200, minClE, maxClE, 200,  minClE, maxClE)
        self.h_ESum_cop160 = ROOT.TH1D("h_ESum_cop160","",100,minESum,maxESum)
        self.h_ESum_cop160_bothtracks = ROOT.TH1D("h_ESum_cop160_bothtracks","",100,minESum,maxESum)
        self.h_ESum_cop160_eletracks = ROOT.TH1D("h_ESum_cop160_eletrack","",100,minESum,maxESum)
        self.h_ESum_cop160_postracks = ROOT.TH1D("h_ESum_cop160_postrack","",100,minESum,maxESum)
        self.h_ESum_cop160_notracks = ROOT.TH1D("h_ESum_cop160_notracks","",100,minESum,maxESum)
        #    self.histogramList.append(self.h_E1vsE2_cop160)
        #    self.histogramList.append( self.h_ESum_cop160_bothtracks)
        #    self.histogramList.append( self.h_ESum_cop160_eletracks)
        #    self.histogramList.append( self.h_ESum_cop160_postracks)
        #    self.histogramList.append( self.h_ESum_cop160_notracks)
        
  
        #     /////////////////////////////////////////////////////////
        #   /*  mid-ESum plots  */ 
        
        self.h_Ecl_midESum_coplanarity = ROOT.TH1D("h_Ecl_midESum_coplanarity","",100,120,240)
        self.histogramList.append( self.h_Ecl_midESum_coplanarity)
        self.h_Ecl_cop180_midESum_positron = ROOT.TH1D("h_Ecl_cop180_midESum_positron","",100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_electron = ROOT.TH1D("h_Ecl_cop180_midESum_electron","",100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_mis_ele = ROOT.TH1D("h_Ecl_cop180_midESum_mis_ele","",100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_mis_pos = ROOT.TH1D("h_Ecl_cop180_midESum_mis_pos","",100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_mis_both_ele_side = ROOT.TH1D("h_Ecl_cop180_midESum_mis_both_ele_side","",100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_mis_both_pos_side = ROOT.TH1D("h_Ecl_cop180_midESum_mis_both_pos_side","",100,minClE,maxClE)
        self.histogramList.append( self.h_Ecl_cop180_midESum_positron)
        self.histogramList.append( self.h_Ecl_cop180_midESum_electron)
        self.histogramList.append( self.h_Ecl_cop180_midESum_mis_ele)
        self.histogramList.append( self.h_Ecl_cop180_midESum_mis_pos)
        self.histogramList.append( self.h_Ecl_cop180_midESum_mis_both_ele_side)
        self.histogramList.append( self.h_Ecl_cop180_midESum_mis_both_pos_side)
        self.h_EclX_cop180_midESum_positron = ROOT.TH1D("h_EclX_cop180_midESum_positron","",100,-400,400)
        self.h_EclX_cop180_midESum_electron = ROOT.TH1D("h_EclX_cop180_midESum_electron","",100,-400,400 )
        self.h_EclX_cop180_midESum_mis_ele = ROOT.TH1D("h_EclX_cop180_midESum_mis_ele","",100,-400,400)
        self.h_EclX_cop180_midESum_mis_pos = ROOT.TH1D("h_EclX_cop180_midESum_mis_pos","",100,-400,400)
        self.h_EclX_cop180_midESum_mis_both_ele_side = ROOT.TH1D("h_EclX_cop180_midESum_mis_both_ele_side","",100,-400,400)
        self.h_EclX_cop180_midESum_mis_both_pos_side = ROOT.TH1D("h_EclX_cop180_midESum_mis_both_pos_side","",100,-400,400)
        self.histogramList.append( self.h_EclX_cop180_midESum_positron)
        self.histogramList.append( self.h_EclX_cop180_midESum_electron)
        self.histogramList.append( self.h_EclX_cop180_midESum_mis_ele)
        self.histogramList.append( self.h_EclX_cop180_midESum_mis_pos)
        self.histogramList.append( self.h_EclX_cop180_midESum_mis_both_ele_side)
        self.histogramList.append( self.h_EclX_cop180_midESum_mis_both_pos_side)
        self.h_EclY_cop180_midESum_positron = ROOT.TH1D("h_EclY_cop180_midESum_positron","",100,-100,100)
        self.h_EclY_cop180_midESum_electron = ROOT.TH1D("h_EclY_cop180_midESum_electron","",100,-100,100 )
        self.h_EclY_cop180_midESum_mis_ele = ROOT.TH1D("h_EclY_cop180_midESum_mis_ele","",100,-100,100)
        self.h_EclY_cop180_midESum_mis_pos = ROOT.TH1D("h_EclY_cop180_midESum_mis_pos","",100,-100,100)
        self.h_EclY_cop180_midESum_mis_both_ele_side = ROOT.TH1D("h_EclY_cop180_midESum_mis_both_ele_side","",100,-100,100)
        self.h_EclY_cop180_midESum_mis_both_pos_side = ROOT.TH1D("h_EclY_cop180_midESum_mis_both_pos_side","",100,-100,100)
        self.histogramList.append( self.h_EclY_cop180_midESum_positron)
        self.histogramList.append( self.h_EclY_cop180_midESum_electron)
        self.histogramList.append( self.h_EclY_cop180_midESum_mis_ele)
        self.histogramList.append( self.h_EclY_cop180_midESum_mis_pos)
        self.histogramList.append( self.h_EclY_cop180_midESum_mis_both_ele_side)
        self.histogramList.append( self.h_EclY_cop180_midESum_mis_both_pos_side)
        self.h_ClD_cop180_midESum_positron = ROOT.TH1D("h_ClD_cop180_midESum_positron","",100,0,200)
        self.h_ClD_cop180_midESum_electron = ROOT.TH1D("h_ClD_cop180_midESum_electron","",100,0,200 )
        self.h_ClD_cop180_midESum_mis_ele = ROOT.TH1D("h_ClD_cop180_midESum_mis_ele","",100,0,200)
        self.h_ClD_cop180_midESum_mis_pos = ROOT.TH1D("h_ClD_cop180_midESum_mis_pos","",100,0,200)
        self.h_ClD_cop180_midESum_mis_both_ele_side = ROOT.TH1D("h_ClD_cop180_midESum_mis_both_ele_side","",100,0,200)
        self.h_ClD_cop180_midESum_mis_both_pos_side = ROOT.TH1D("h_ClD_cop180_midESum_mis_both_pos_side","",100,0,200)
        self.histogramList.append( self.h_ClD_cop180_midESum_positron)
        #    self.histogramList.append( self.h_ClD_cop180_midESum_electron)
        #    self.histogramList.append( self.h_ClD_cop180_midESum_mis_ele)
        #    self.histogramList.append( self.h_ClD_cop180_midESum_mis_pos)
        #    self.histogramList.append( self.h_ClD_cop180_midESum_mis_both_ele_side)
        #    self.histogramList.append( self.h_ClD_cop180_midESum_mis_both_pos_side)
        self.h_Ecl_cop180_midESum_pos_side_found_ele = ROOT.TH1D("h_Ecl_cop180_midESum_pos_side_found_ele","", 100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_pos_side_found_ele_found_pos = ROOT.TH1D("h_Ecl_cop180_midESum_pos_side_found_ele_found_pos","", 100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_ele_side_found_pos = ROOT.TH1D("h_Ecl_cop180_midESum_ele_side_found_pos","", 100,minClE,maxClE)
        self.h_Ecl_cop180_midESum_ele_side_found_pos_found_ele = ROOT.TH1D("h_Ecl_cop180_midESum_ele_side_found_pos_found_ele","", 100,minClE,maxClE)
        self.histogramList.append(  self.h_Ecl_cop180_midESum_pos_side_found_ele )
        self.histogramList.append(  self.h_Ecl_cop180_midESum_pos_side_found_ele_found_pos )
        self.histogramList.append(  self.h_Ecl_cop180_midESum_ele_side_found_pos )
        self.histogramList.append(  self.h_Ecl_cop180_midESum_ele_side_found_pos_found_ele )
        
    #   /////////////////////////////////////////////////////////
        self.h_EclX_EclY_ElectronPositron = ROOT.TH2D("h_EclX_EclY_ElectronPositron","",100,-400,400,100,-100,100)
        self.histogramList.append(self.h_EclX_EclY_ElectronPositron);
        #     ////////////////////////
        #   // same sign found tracks. 
        #    self.h_Ecl_TwoElectrons_coplanarity = ROOT.TH1D("h_Ecl_TwoElectrons_coplanarity ","",100,0,240);
        #    self.h_Ecl_TwoPositrons_coplanarity = ROOT.TH1D("h_Ecl_TwoPositrons_coplanarity","",100,0,240);
        #    self.h_Ecl_TwoElectrons_mass=ROOT.TH1D("h_Ecl_TwoElectrons_mass","",100,0,0.1);
        #    self.h_Ecl_TwoPositrons_mass=ROOT.TH1D("h_Ecl_TwoPositrons_mass","",100,0,0.1);
        #    self.h_EclX_EclY_TwoElectrons = ROOT.TH2D("h_EclX_EclY_TwoElectrons","",100,-400,400,100,-100,100);
        #    self.h_EclX_EclY_TwoPositrons = ROOT.TH2D("h_EclX_EclY_TwoPositrons","",100,-400,400,100,-100,100);
        #    self.h_Ecl_Ptrk_from_position_TwoElectrons_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_TwoElectrons_ele","",100,minClE,maxClE,100,minTrkP,maxTrkP);
        #    self.h_Ecl_Ptrk_from_position_TwoPositrons_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_TwoPositrons_pho","",100,minClE,maxClE,100,minTrkP,maxTrkP);
        #    self.h_Ecl_TwoElectrons_esum=ROOT.TH1D("h_Ecl_TwoElectrons_esum","",100,minESum,maxESum);
        #    self.h_Ecl_TwoPositrons_esum=ROOT.TH1D("h_Ecl_TwoPositrons_esum","",100,minESum,maxESum);
        
        #    self.histogramList.append(self.h_Ecl_TwoElectrons_coplanarity);
        #    self.histogramList.append(self.h_Ecl_TwoPositrons_coplanarity);
        #    self.histogramList.append(self.h_EclX_EclY_TwoElectrons);
        #    self.histogramList.append(self.h_EclX_EclY_TwoPositrons);
        #    self.histogramList.append(self.h_Ecl_Ptrk_from_position_TwoElectrons_ele);
        #    self.histogramList.append(self.h_Ecl_Ptrk_from_position_TwoPositrons_ele);
        #    self.histogramList.append(self.h_Ecl_TwoElectrons_mass);
        #    self.histogramList.append(self.h_Ecl_TwoPositrons_mass);
        
#   /////////////////////
        
# /////////////////////
#   //  no matched tracks
        self.h_Ecl_TwoPhotons_coplanarity = ROOT.TH1D("h_Ecl_TwoPhotons_coplanarity ","",100,0,240);
        self.h_EclX_EclY_TwoPhotons = ROOT.TH2D("h_EclX_EclY_TwoPhotons","",100,-400,400,100,-100,100);
        self.h_Ecl_Ptrk_from_position_TwoPhotons_ele=ROOT.TH2D("h_Ecl_Ptrk_from_position_TwoPhotons_ele","",100,minClE,maxClE,100,minTrkP,maxTrkP);
        self.h_Ecl_TwoPhotons_mass=ROOT.TH1D("h_Ecl_TwoPhotons_mass","",100,0,0.1);
        self.h_Ecl_TwoPhotons_esum=ROOT.TH1D("h_Ecl_TwoPhotons_esum","",100,minESum,maxESum);
        
        #    self.histogramList.append(self.h_Ecl_TwoPhotons_coplanarity)
        #    self.histogramList.append(self.h_EclX_EclY_TwoPhotons)
        #    self.histogramList.append(self.h_Ecl_Ptrk_from_position_TwoPhotons_ele)
        #    self.histogramList.append(self.h_Ecl_TwoPhotons_mass)
        #    self.histogramList.append(self.h_Ecl_TwoPhotons_esum)
        #    self.histogramList.append(self.h_Ecl_TwoElectrons_esum)
        #    self.histogramList.append(self.h_Ecl_TwoPositrons_esum)
        
        
    def setEnergyScales(self, ebeam)  :
        # modify scales if we need to
        return



    #takes in an HpsParticle candidate and makes plots
    #use this for reconstructed events
    def fillCandidateHistograms(self,particle, ucparticle = None) :
        #fill histograms
        return
        
      
    def fillTridentBand(self,trEle,clEle,trPos,clPos) : 
        cl_x_ele=clEle.getPosition()[0]
        cl_y_ele=clEle.getPosition()[1]
        cl_z_ele=clEle.getPosition()[2]
        cl_E_ele=clEle.getEnergy()

        cl_x_pos=clPos.getPosition()[0]
        cl_y_pos=clPos.getPosition()[1]
        cl_z_pos=clPos.getPosition()[2]
        cl_E_pos=clPos.getEnergy()
        Esum=cl_E_ele+cl_E_pos
        self.h_ESum_cop180.Fill(Esum)
        self.h_E1vsE2_cop180.Fill(clEle.getEnergy(),clPos.getEnergy())
        eleMomFromPosition=self.momFromECalPosition(cl_x_ele,cl_z_ele,self.beamAngle,self.BEff)
        posMomFromPosition=self.momFromECalPosition(cl_x_pos,cl_z_pos,self.beamAngle,self.BEff)

        if trEle is not None and trPos is not None :
            if trEle.getPDG() == trPos.getPDG() : 
                print "Same sign! PDG ID = "+str( trEle.getPDG())+"...Bailing..."
                return

            tr_p_ele=self.pMag(trEle.getMomentum())
            tr_p_pos=self.pMag(trPos.getMomentum())
            self.h_EclX_EclY_ElectronPositron.Fill(cl_x_ele,cl_y_ele)
            self.h_EclX_EclY_ElectronPositron.Fill(cl_x_pos,cl_y_pos)
           
            self.h_Ecl_Ptrk_from_position_Tri_ele.Fill(cl_E_ele,eleMomFromPosition)                      
            self.h_Ecl_Ptrk_from_position_Tri_pos.Fill(cl_E_pos,posMomFromPosition)            
            self.h_Ptrk_Ptrk_from_position_Tri_ele.Fill(tr_p_ele,eleMomFromPosition)
            self.h_Ptrk_Ptrk_from_position_Tri_pos.Fill(tr_p_pos,posMomFromPosition)
            self.h_ESum_cop180_bothtracks.Fill(Esum)
            if Esum>self.midESumLow and Esum<self.midESumHigh : 
                self.h_Ecl_cop180_midESum_positron.Fill(cl_E_pos)
                self.h_EclX_cop180_midESum_positron.Fill(cl_x_pos)
                self.h_EclY_cop180_midESum_positron.Fill(cl_y_pos)
#                self.h_ClD_cop180_midESum_positron.Fill(cl_d_pos)
                self.h_Ecl_cop180_midESum_electron.Fill(cl_E_ele)
                self.h_EclX_cop180_midESum_electron.Fill(cl_x_ele)
                self.h_EclY_cop180_midESum_electron.Fill(cl_y_ele)
#                self.h_ClD_cop180_midESum_electron.Fill(cl_d_ele)
                self.h_Ecl_cop180_midESum_pos_side_found_ele.Fill(cl_E_pos)
                self.h_Ecl_cop180_midESum_pos_side_found_ele_found_pos.Fill(cl_E_pos)
                self.h_Ecl_cop180_midESum_ele_side_found_pos.Fill(cl_E_ele)
                self.h_Ecl_cop180_midESum_ele_side_found_pos_found_ele.Fill(cl_E_ele)
                

        elif trEle is not None : #but trPos is...just found electron 
            self.h_ESum_cop180_eletrack.Fill(Esum) 
            self.h_Ecl_Ptrk_from_position_Tri_mispos.Fill(cl_E_pos,posMomFromPosition)
            if Esum>self.midESumLow and Esum<self.midESumHigh  : 
                self.h_Ecl_cop180_midESum_electron.Fill(cl_E_ele)
                self.h_EclX_cop180_midESum_electron.Fill(cl_x_ele)
                self.h_EclY_cop180_midESum_electron.Fill(cl_y_ele)
#                self.h_ClD_cop180_midESum_electron.Fill(cl_d_ele)
                self.h_Ecl_cop180_midESum_mis_pos.Fill(cl_E_pos)
                self.h_EclX_cop180_midESum_mis_pos.Fill(cl_x_pos)
                self.h_EclY_cop180_midESum_mis_pos.Fill(cl_y_pos)
#                self.h_ClD_cop180_midESum_mis_pos.Fill(cl_d_pos)
                self.h_Ecl_cop180_midESum_pos_side_found_ele.Fill(cl_E_pos)
           
        elif trPos is not None : #but trEle is...just found positron
            self.h_ESum_cop180_postrack.Fill(Esum)
            self.h_Ecl_Ptrk_from_position_Tri_misele.Fill(cl_E_ele,eleMomFromPosition)
            if Esum>self.midESumLow and Esum<self.midESumHigh: 
                self.h_Ecl_cop180_midESum_positron.Fill(cl_E_pos)
                self.h_EclX_cop180_midESum_positron.Fill(cl_x_pos)
                self.h_EclY_cop180_midESum_positron.Fill(cl_y_pos)
#                self.h_ClD_cop180_midESum_positron.Fill(cl_d_pos)
                self.h_Ecl_cop180_midESum_mis_ele.Fill(cl_E_ele)
                self.h_EclX_cop180_midESum_mis_ele.Fill(cl_x_ele)
                self.h_EclY_cop180_midESum_mis_ele.Fill(cl_y_ele)
#                self.h_ClD_cop180_midESum_mis_ele.Fill(cl_d_ele)
                self.h_Ecl_cop180_midESum_ele_side_found_pos.Fill(cl_E_ele)


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
        cl_impact_angle = math.atan2(Y, X - phot_nom_x)*radian
        if cl_impact_angle < 0. :
            cl_impact_angle = cl_impact_angle + 360. 

#########   check if track has a hit in layer 1
    @staticmethod
    def hasL1Hit(trk): 
        if trk == None : 
            return False
        for hit in trk.getSvtHits() : 
            if hit.getLayer() == 1 : 
                return True
        return False
#########   check if track has a hit in layer X
    @staticmethod
    def hasLXHit(trk,layer): 
        if trk == None : 
            return False
        for hit in trk.getSvtHits() : 
            if hit.getLayer() == layer : 
                return True
        return False
