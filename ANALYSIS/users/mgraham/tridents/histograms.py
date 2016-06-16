import ROOT 
import math
from ROOT import TLorentzVector
import numpy as np 
me=0.000000511 #kev
class myHistograms:  
    histogramList=[]

    nbinsSmall=50
    nbinsBig=500

    nTrk = ROOT.TH1F("nTrk","Number of Tracks/Event",11,0,11)
    nEle = ROOT.TH1F("nEle","Number of Electrons/Event",11,0,11)
    nPos = ROOT.TH1F("nPos","Number of Positrons/Event",5,0,5)
    nClust = ROOT.TH1F("nClust","Number of Clusters/Event",11,0,11)
    nTrkCand = ROOT.TH1F("nTrkCand","Number of Tracks/Event",11,0,11)
    nEleCand = ROOT.TH1F("nEleCand","Number of Electrons/Event",11,0,11)
    nPosCand = ROOT.TH1F("nPosCand","Number of Positrons/Event",5,0,5)
    nClustCand = ROOT.TH1F("nClustCand","Number of Clusters/Event",11,0,11)
    nCand = ROOT.TH1F("nCand","Number of Candidates/Event",5,0,5)
    histogramList.append(nTrk)
    histogramList.append(nEle)
    histogramList.append(nPos)
    histogramList.append(nClust)
    histogramList.append(nTrkCand)
    histogramList.append(nEleCand)
    histogramList.append(nPosCand)
    histogramList.append(nClustCand)
    histogramList.append(nCand)

    tridentMass = ROOT.TH1F("TridentMass","Trident Mass (GeV)", nbinsBig, 0, 0.100)
    histogramList.append(tridentMass)
    tridentMassVtxCut = ROOT.TH1F( "TridentMassBeforeVertex", "Trident Mass (GeV): Before  VtxCut", nbinsBig, 0, 0.100)
    histogramList.append(tridentMassVtxCut)    

    eSum =  ROOT.TH1F("eSum", "Energy Sum", nbinsSmall, 0.3, 1.2)
    histogramList.append(eSum)
    eDiff =  ROOT.TH1F("eDiffoverESum", "Energy Difference", nbinsSmall, -0.8, 0.8)    
    histogramList.append(eDiff)
    ePosvseEle=ROOT.TH2F("ePosvseEle","Positron vs Electron Energy",nbinsSmall,0.1,0.9,50,0.1,0.9)
    histogramList.append(ePosvseEle)
    openAngle =  ROOT.TH1F("openAngle", "openAngle", nbinsSmall, 0.015, 0.16)
    histogramList.append(openAngle)
    minAngle = ROOT.TH1F("minAngle","Minimum Track Angle",nbinsSmall,0.01,0.03)
    histogramList.append(minAngle)
    coplan=ROOT.TH1F("coplanarity","Coplanarity",nbinsSmall,-0.004,0.004)
    histogramList.append(coplan)
    copVseSum=ROOT.TH2F("coplanarity vs eSum", "coplanarity vs eSum", 100,0.5,1.2,100,-0.004,0.004)
    histogramList.append(copVseSum)
    openVseSum=ROOT.TH2F("openAngle vs eSum", "opening angle vs eSum", 100,0.5,1.2,100,0.015,0.16)
    histogramList.append(openVseSum)
    eleMom = ROOT.TH1F("eleMom","Electron Momentum (GeV)", nbinsSmall, 0, 1.)
    posMom = ROOT.TH1F("posMom","Positron Momentum (GeV)", nbinsSmall, 0, 1.)
    recMom = ROOT.TH1F("recMom","Recoil Momentum (GeV)", nbinsSmall, 0, 1.)
    histogramList.append(eleMom)
    histogramList.append(posMom)
    histogramList.append(recMom)
    eleChi2 = ROOT.TH1F("eleChi2","Electron Track Chi2",nbinsSmall,0,10)
    posChi2 = ROOT.TH1F("posChi2","Positron Track Chi2",nbinsSmall,0,10)
    histogramList.append(eleChi2)
    histogramList.append(posChi2)
    eleChi2vsMom = ROOT.TH2F("eleChi2vsMom","Electron Track Chi2 vs Momentum",nbinsSmall,0,10,nbinsSmall,0,1.0)
    posChi2vsMom = ROOT.TH2F("posChi2vsMom","Positron Track Chi2 vs Momentum",nbinsSmall,0,10,nbinsSmall,0,1.0)
    histogramList.append(eleChi2vsMom)
    histogramList.append(posChi2vsMom)

    raweleMom = ROOT.TH1F("raweleMom","Electron Momentum (GeV)", nbinsSmall, 0, 1.)
    rawposMom = ROOT.TH1F("rawposMom","Positron Momentum (GeV)", nbinsSmall, 0, 1.)
    histogramList.append(raweleMom)
    histogramList.append(rawposMom)
    
    eled0 = ROOT.TH1F("eled0","Electron d0 (mm)", nbinsSmall, -3, 3)
    posd0 = ROOT.TH1F("posd0","Positron d0 (mm)", nbinsSmall, -3, 3)

    histogramList.append(eled0)
    histogramList.append(posd0)

    elez0 = ROOT.TH1F("elez0","Electron z0 (mm)", nbinsSmall, -1.5, 1.5)
    posz0 = ROOT.TH1F("posz0","Positron z0 (mm)", nbinsSmall, -1.5, 1.5)

    histogramList.append(elez0)
    histogramList.append(posz0)

    elephi0 = ROOT.TH1F("elephi0","Electron phi0", nbinsSmall, -0.1, 0.1)
    posphi0 = ROOT.TH1F("posphi0","Positron phi0", nbinsSmall, -0.1, 0.1)
    histogramList.append(elephi0)
    histogramList.append(posphi0)

    eleslope = ROOT.TH1F("eleslope","Electron slope", nbinsSmall, -0.08, 0.08)
    posslope = ROOT.TH1F("posslope","Positron slope", nbinsSmall, -0.08, 0.08)
    histogramList.append(eleslope)
    histogramList.append(posslope)

    # 2d track kinematics distributions for electrons & positrons
    eVsSlopeEle=ROOT.TH2F("eVsSlopeEle","Electron Energy vs Slope",100,0.1,0.8,100,-0.08,0.08)
    histogramList.append(eVsSlopeEle)
    eVsSlopePos=ROOT.TH2F("eVsSlopePos","Positron Energy vs Slope",100,0.1,0.8,100,-0.08,0.08)
    histogramList.append(eVsSlopePos)

    eVsPhiEle=ROOT.TH2F("eVsPhiEle","Electron Energy vs Phi",100,0.1,0.8,100,-0.04,0.14)
    histogramList.append(eVsPhiEle)
    eVsPhiPos=ROOT.TH2F("eVsPhiPos","Positron Energy vs Phi",100,0.1,0.8,100,-0.04,0.14)
    histogramList.append(eVsPhiPos)

    eVsPhiEleBottom=ROOT.TH2F("eVsPhiEleBottom","Electron (Bottom) Energy vs Phi",100,0.1,0.8,100,-0.04,0.14)
    histogramList.append(eVsPhiEleBottom)
    eVsPhiPosTop=ROOT.TH2F("eVsPhiPosTop","Positron (Top) Energy vs Phi",100,0.1,0.8,100,-0.04,0.14)
    histogramList.append(eVsPhiPosTop)

    eVsPhiEleTop=ROOT.TH2F("eVsPhiEleTop","Electron (Top) Energy vs Phi",100,0.1,0.8,100,-0.04,0.14)
    histogramList.append(eVsPhiEleTop)
    eVsPhiPosBottom=ROOT.TH2F("eVsPhiPosBottom","Positron (Bottom) Energy vs Phi",100,0.1,0.8,100,-0.04,0.14)
    histogramList.append(eVsPhiPosBottom)

    slopeVsPhiEle=ROOT.TH2F("slopeVsPhiEle","Electron Slope vs Phi",100,-0.08,0.08,100,-0.04,0.14)
    histogramList.append(slopeVsPhiEle)
    slopeVsPhiPos=ROOT.TH2F("slopeVsPhiPos","Positron Slope vs Phi",100,-0.08,0.08,100,-0.04,0.14)
    histogramList.append(slopeVsPhiPos)

####################
    #2d cluster/track distributions 
    EclXEclYEle = ROOT.TH2D("EclXEclYEle","Electron Cluster X vs Y",100,-400,400,100,-100,100)
    histogramList.append(EclXEclYEle)
    EclXEclYPos = ROOT.TH2D("EclXEclYPos","Positron Cluster X vs Y",100,-400,400,100,-100,100)
    histogramList.append(EclXEclYPos)
    
    EclEPtrkPos = ROOT.TH2D("EclEPtrkPos","Positron Cluster Energy vs Track Momentum",100, 0.1 ,0.8,100 ,0.1, 0.8)
    histogramList.append(EclEPtrkPos)    
    EclEPtrkEle = ROOT.TH2D("EclEPtrkEle","Electron Cluster Energy vs Track Momentum",100, 0.1 ,0.8,100 ,0.1, 0.8)
    histogramList.append(EclEPtrkEle)

    EclXPtrkPos = ROOT.TH2D("EclXPtrkPos","Positron Cluster X vs Track Momentum",100, 0.1 ,0.8,100 ,-100,400)
    histogramList.append(EclXPtrkPos)    
    EclXPtrkEle = ROOT.TH2D("EclXPtrkEle","Electron Cluster X vs Track Momentum",100, 0.1 ,0.8,100 ,-400,100)
    histogramList.append(EclXPtrkEle)    

    EclTimePtrkEle =  ROOT.TH2D("EclTimePtrkEle","Electron Cluster Time vs Momentum",100,0.1,0.8,100,-4, 4)
    EclTimePtrkPos = ROOT.TH2D("EclTimePtrkPos","Positron Cluster Time vs Momentum",100,0.1,0.8,100,-4, 4)
    histogramList.append(EclTimePtrkEle)
    histogramList.append(EclTimePtrkPos)

    TrkTimePtrkEle =   ROOT.TH2D("TrkTimePtrkEle","Electron Track Time vs Momentum",100,0.1,0.8,100,-10, 10)
    TrkTimePtrkPos =  ROOT.TH2D("TrkTimePtrkPos","Positron Track Time vs Momentum",100,0.1,0.8,100,-10, 10)
    histogramList.append(TrkTimePtrkEle)
    histogramList.append(TrkTimePtrkPos)

    TrkTimeEclTimeEle = ROOT.TH2D("TrkTimeEclTimeEle","Electron Track Time vs Cluster Time",100,-4,4,100,-10, 10)
    TrkTimeEclTimePos = ROOT.TH2D("TrkTimeEclTimePos","Positron Track Time vs Cluster Time",100,-4,4,100,-10, 10)
    histogramList.append(TrkTimeEclTimeEle)
    histogramList.append(TrkTimeEclTimePos)

###################
### WAB histograms
    wabESum = ROOT.TH1D("wabESum","Electron + Photon Energy",nbinsSmall,0.2,1.2)
    wabCoplanarity = ROOT.TH1D("wabCoplanarity","Electron/Photon Coplanarity",nbinsSmall,120,240)
    wabCoplanarityVsESum = ROOT.TH2D("wabCoplanarityVsESum","Electron/Photon Coplanarity Versus ESum",100, 0.2, 1.2, 100,120,240)
    wabPredictedVsMeasuredE=ROOT.TH2D("wabPredictedVsMeasuredE","wabPredictedVsMeasuredE",100,0.0,1.2,100,0,1.2) 
    wabPredictedVsMeasuredX=ROOT.TH2D("wabPredictedVsMeasuredX","wabPredictedVsMeasuredX",100,-200,200,100,-200,200)
    wabPredictedVsMeasuredY=ROOT.TH2D("wabPredictedVsMeasuredY","wabPredictedVsMeasuredY",100,-100,100,100,-100,100)
    wabDeltaX=ROOT.TH1D("wabDeltaX","wabDeltaX",100,-100,100)
    wabDeltaY=ROOT.TH1D("wabDeltaY","wabDeltaY",100,-100,100)
    histogramList.append(wabESum)
    histogramList.append(wabCoplanarity)
    histogramList.append(wabCoplanarityVsESum)
    histogramList.append(wabPredictedVsMeasuredE)
    histogramList.append(wabPredictedVsMeasuredX)
    histogramList.append(wabPredictedVsMeasuredY)
    histogramList.append(wabDeltaX)
    histogramList.append(wabDeltaY)
##################    
    
    deltaPhi=ROOT.TH1F("deltaPhi","DeltaPhi",nbinsSmall,-2,2)
    deltaTheta=ROOT.TH1F("deltaTheta","DeltaTheta",nbinsSmall,-0.1,0.1)
    histogramList.append(deltaPhi)
    histogramList.append(deltaTheta)
    
    elephibeam = ROOT.TH1F("elephibeam","Electron phibeam", nbinsSmall, -3.15, 3.15)
    posphibeam = ROOT.TH1F("posphibeam","Positron phibeam", nbinsSmall, -3.15, 3.15)
    histogramList.append(elephibeam)
    histogramList.append(posphibeam)
    
    elepolarangle = ROOT.TH1F("elepolarangle","Electron Polar Angle", nbinsSmall, 0.0, 0.1)
    pospolarangle = ROOT.TH1F("pospolarangle","Positron Polar Angle", nbinsSmall, 0.0, 0.1)
    histogramList.append(elepolarangle)
    histogramList.append(pospolarangle)

#non-truth plots
    tridentVx = ROOT.TH1F("Vx", "Trident Vx (mm)", nbinsSmall, -4, 4)
    tridentVy = ROOT.TH1F("Vy","Trident Vy (mm)", nbinsSmall, -2, 2)
    tridentVz =  ROOT.TH1F("Vz", "Trident Vz (mm)", nbinsBig, -50, 50)
    histogramList.append(tridentVx)
    histogramList.append(tridentVy)
    histogramList.append(tridentVz)    
    vertChi2 =  ROOT.TH1F("vertChi2", "V0 Chi2", nbinsSmall, 0, 50)    
    histogramList.append(vertChi2)

    tridentVxUC = ROOT.TH1F("VxUC", "Trident Uconstrained Vx (mm)", nbinsSmall, -4, 4)
    tridentVyUC = ROOT.TH1F("VyUC","Trident Uconstrained Vy (mm)", nbinsSmall, -2, 2)
    tridentVzUC =  ROOT.TH1F("VzUC", "Trident Uconstrained Vz (mm)", nbinsBig, -50, 50)
    histogramList.append(tridentVxUC)
    histogramList.append(tridentVyUC)
    histogramList.append(tridentVzUC)    
    vertChi2UC =  ROOT.TH1F("vertChi2UC", "V0 Uconstrained Chi2", nbinsSmall, 0, 50)    
    histogramList.append(vertChi2UC)

    trkTimeDiff = ROOT.TH1F("trkTimeDiff","Ele-Pos Time Difference (ns)", nbinsSmall, -6, 6)
    cluTimeDiff = ROOT.TH1F("cluTimeDiff","Cluster Time Difference (ns)", nbinsSmall, -2, 2)
    histogramList.append(trkTimeDiff)
    histogramList.append(cluTimeDiff)

    trkCluTimeDiffEle = ROOT.TH1F("trkCluTimeDiffEle","Electron Track-Cluster Time (ns)", nbinsSmall, -10, 10)
    trkCluTimeDiffPos = ROOT.TH1F("trkCluTimeDiffPos","Positron Track-Cluster Time (ns)", nbinsSmall, -10, 10)
    histogramList.append(trkCluTimeDiffEle)
    histogramList.append(trkCluTimeDiffPos)
    
    nHitsEle=ROOT.TH1F("nHitsEle","Number of Hits: Electrons",2,5,7)
    histogramList.append(nHitsEle)
    nHitsPos=ROOT.TH1F("nHitsPos","Number of Hits: Positrons",2,5,7)
    histogramList.append(nHitsPos)
    
    nlayers = 12 
    eleLambdaKink=[]
    posLambdaKink=[]
    elePhiKink=[]
    posPhiKink=[]
    eleIso=[]
    posIso=[]
    
    for  i in range(0, nlayers) :
        name="eleLambdaKinkL"+str(i)
        eleLambdaKink.append(ROOT.TH1F(name,name,nbinsSmall,-0.02,0.02))
        histogramList.append(eleLambdaKink[i])
        name="elePhiKinkL"+str(i)
        elePhiKink.append(ROOT.TH1F(name,name,nbinsSmall,-0.02,0.02))
        histogramList.append(elePhiKink[i])
        name="eleIsoL"+str(i)
        eleIso.append(ROOT.TH1F(name,name,nbinsSmall,-7.5,7.5))
        histogramList.append(eleIso[i])
        name="posLambdaKinkL"+str(i)
        posLambdaKink.append(ROOT.TH1F(name,name,nbinsSmall,-0.02,0.02))
        histogramList.append(posLambdaKink[i])
        name="posPhiKinkL"+str(i)
        posPhiKink.append(ROOT.TH1F(name,name,nbinsSmall,-0.02,0.02))
        histogramList.append(posPhiKink[i])
        name="posIsoL"+str(i)
        posIso.append(ROOT.TH1F(name,name,nbinsSmall,-7.5,7.5))
        histogramList.append(posIso[i])

        
 #plots in slices of Mass    
    eleMomMass=[]
    posMomMass=[]
    eleThetaMass=[]
    posThetaMass=[]
    elePhi0Mass=[]
    posPhi0Mass=[]
    coplanMass=[]
    eDiffMass=[]
    polarAngleMass=[]#polar angle of the V0
    phiV0Mass=[]  #phi of the V0
    esumMass=[]
    vertZMass=[]
    vertXMass=[]
    vertYMass=[]

#  Mass slices upper limits    
    nSlicesMass=10 
    massMin=0.010
    massMax=0.060
    sliceSizeMass= (massMax-massMin)/nSlicesMass # (0.06-0.01)/10 = 5 MeV bins
##############    

    post="_Mass_Slice_"
    for i in range(1, nSlicesMass+1) :
        name="eleMom"+post+str(i)
        eleMomMass.append(ROOT.TH1F(name,name,nbinsSmall,0,1.0))
        histogramList.append(eleMomMass[i-1])
        name="posMom"+post+str(i)
        posMomMass.append(ROOT.TH1F(name,name,nbinsSmall,0,1.0))
        histogramList.append(posMomMass[i-1])
        name="eleTheta"+post+str(i)
        eleThetaMass.append(ROOT.TH1F(name,name,nbinsSmall,-0.08,0.08))
        histogramList.append(eleThetaMass[i-1])
        name="posTheta"+post+str(i)
        posThetaMass.append(ROOT.TH1F(name,name,nbinsSmall,-0.08,0.08))
        histogramList.append(posThetaMass[i-1])
        name="elePhi0"+post+str(i)
        elePhi0Mass.append(ROOT.TH1F(name,name,nbinsSmall,-0.1,0.1))
        histogramList.append(elePhi0Mass[i-1])
        name="posPhi0"+post+str(i)
        posPhi0Mass.append(ROOT.TH1F(name,name,nbinsSmall,-0.1,0.1))
        histogramList.append(posPhi0Mass[i-1])
        name="Coplanarity"+post+str(i)
        coplanMass.append(ROOT.TH1F(name,name,nbinsSmall,-0.004,0.004))
        histogramList.append(coplanMass[i-1])
        name="Ediff"+post+str(i)
        eDiffMass.append(ROOT.TH1F(name,name,nbinsSmall,-0.8,0.8)) 
        histogramList.append(eDiffMass[i-1])
        name="V0PolarAngle"+post+str(i)
        polarAngleMass.append(ROOT.TH1F(name,name,nbinsSmall,0,0.05))
        histogramList.append(polarAngleMass[i-1]) 
        name="V0Phi"+post+str(i)
        phiV0Mass.append(ROOT.TH1F(name,name,nbinsSmall,0,3.15))
        histogramList.append(phiV0Mass[i-1])
        name="ESum"+post+str(i)
        esumMass.append(ROOT.TH1F(name,name,nbinsSmall,0.3,1.2))
        histogramList.append(esumMass[i-1])
        name="vertX"+post+str(i)
        vertXMass.append(ROOT.TH1F(name,name,nbinsSmall,-4,4))
        histogramList.append(vertXMass[i-1])
        name="vertY"+post+str(i)
        vertYMass.append(ROOT.TH1F(name,name,nbinsSmall,-2,2))
        histogramList.append(vertYMass[i-1])
        name="vertZ"+post+str(i)
        vertZMass.append(ROOT.TH1F(name,name,nbinsBig, -50,50))
        histogramList.append(vertZMass[i-1])

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
    massESum=[]
##############
#  ESum slices upper limits    
    nSlicesESum=5 
    esumMin=0.55
    esumMax=1.2
    sliceSizeESum=0.1 #100MeV starting at esumMin
##############

    post=" ESum Slice "
    for i in range(1, nSlicesESum+1) :
        name="eleMom "+post+str(i)
        eleMomESum.append(ROOT.TH1F(name,name,nbinsSmall,0,1.0))
        histogramList.append(eleMomESum[i-1])
        name="posMom "+post+str(i)
        posMomESum.append(ROOT.TH1F(name,name,nbinsSmall,0,1.0))
        histogramList.append(posMomESum[i-1])
        name="eleTheta "+post+str(i)
        eleThetaESum.append(ROOT.TH1F(name,name,nbinsSmall,-0.08,0.08))
        histogramList.append(eleThetaESum[i-1])
        name="posTheta "+post+str(i)
        posThetaESum.append(ROOT.TH1F(name,name,nbinsSmall,-0.08,0.08))
        histogramList.append(posThetaESum[i-1])
        name="elePhi0 "+post+str(i)
        elePhi0ESum.append(ROOT.TH1F(name,name,nbinsSmall,-0.1,0.1))
        histogramList.append(elePhi0ESum[i-1])
        name="posPhi0 "+post+str(i)
        posPhi0ESum.append(ROOT.TH1F(name,name,nbinsSmall,-0.1,0.1))
        histogramList.append(posPhi0ESum[i-1])
        name="Coplanarity "+post+str(i)
        coplanESum.append(ROOT.TH1F(name,name,nbinsSmall,-0.004,0.004))
        histogramList.append(coplanESum[i-1])
        name="Ediff "+post+str(i)
        eDiffESum.append(ROOT.TH1F(name,name,nbinsSmall,-0.8,0.8)) 
        histogramList.append(eDiffESum[i-1])
        name="V0PolarAngle "+post+str(i)
        polarAngleESum.append(ROOT.TH1F(name,name,nbinsSmall,0,0.05))
        histogramList.append(polarAngleESum[i-1]) 
        name="V0Phi "+post+str(i)
        phiV0ESum.append(ROOT.TH1F(name,name,nbinsSmall,0,3.15))
        histogramList.append(phiV0ESum[i-1])
        name="Mass "+post+str(i)        
        massESum.append(ROOT.TH1F(name,name, nbinsBig, 0, 0.100))
        histogramList.append(massESum[i-1])
        

    beam=[np.sin(0.0305),0,np.cos(0.0305)]
    beamRotAxis=[0,1,0]
    rotAngle=-0.0305
    #takes in an HpsParticle candidate and makes plots
    #use this for reconstructed events
    def fillCandidateHistograms(self,particle, ucparticle = None) :
        toBeamFrame=self.rotation_matrix(self.beamRotAxis,self.rotAngle)
  #fill the vertex position plots        
        vposition=particle.getVertexPosition()
        self.tridentVx.Fill(vposition[0])
        self.tridentVy.Fill(vposition[1])
        self.tridentVz.Fill(vposition[2])
        self.vertChi2.Fill(particle.getVertexFitChi2())

        if ucparticle != None : 
            ucvposition=ucparticle.getVertexPosition()
            self.tridentVxUC.Fill(ucvposition[0])
            self.tridentVyUC.Fill(ucvposition[1])
            self.tridentVzUC.Fill(ucvposition[2])
            self.vertChi2UC.Fill(ucparticle.getVertexFitChi2())
            

        daughter_particles = particle.getParticles()
        electron =  daughter_particles.At(0)
        positron =  daughter_particles.At(1)
        
        if daughter_particles.At(0).getCharge()>0:
            electron =  daughter_particles.At(1)
            positron =  daughter_particles.At(0)
        pEle=electron.getMomentum()
        pPos=positron.getMomentum()
        
        eleBeam =self.rotateFourMomentum(self.getLorentzVector(pEle),toBeamFrame)
        posBeam =self.rotateFourMomentum(self.getLorentzVector(pPos),toBeamFrame)
        self.fillHistograms(eleBeam,posBeam)
        #get tracks
        eleTrk=electron.getTracks().At(0)
        posTrk=positron.getTracks().At(0)

        self.eled0.Fill(eleTrk.getD0())
        self.elez0.Fill(eleTrk.getZ0())
        self.posd0.Fill(posTrk.getD0())
        self.posz0.Fill(posTrk.getZ0())

        self.eleChi2.Fill(eleTrk.getChi2());
        self.posChi2.Fill(posTrk.getChi2());
        self.eleChi2vsMom.Fill(eleTrk.getChi2(),eleBeam.E());
        self.posChi2vsMom.Fill(posTrk.getChi2(),posBeam.E());

        self.trkTimeDiff.Fill(eleTrk.getTrackTime()-posTrk.getTrackTime())
        self.TrkTimePtrkEle.Fill(eleBeam.E(),eleTrk.getTrackTime())
        self.TrkTimePtrkPos.Fill(posBeam.E(),posTrk.getTrackTime())
        self.nHitsEle.Fill(eleTrk.getSvtHits().GetSize())
        self.nHitsPos.Fill(posTrk.getSvtHits().GetSize())

        mass=math.sqrt(eleBeam.Mag2()+posBeam.Mag2()+2*(eleBeam*posBeam))
        massBin=int((mass-self.massMin)/self.sliceSizeMass)            
        if(massBin>=self.nSlicesMass) :
            massBin = self.nSlicesMass-1
        self.vertXMass[massBin].Fill(vposition[0]) 
        self.vertYMass[massBin].Fill(vposition[1]) 
        self.vertZMass[massBin].Fill(vposition[2]) 
        

        for i in range(0,self.nlayers) :
            self.eleIso[i].Fill(eleTrk.getIsolation(i))
            self.posIso[i].Fill(posTrk.getIsolation(i))
            if type(eleTrk).__name__ == 'GblTrack':
                self.elePhiKink[i].Fill(eleTrk.getPhiKink(i))
                self.posPhiKink[i].Fill(posTrk.getPhiKink(i))
                self.eleLambdaKink[i].Fill(eleTrk.getLambdaKink(i))
                self.posLambdaKink[i].Fill(posTrk.getLambdaKink(i))
        # matched clusters
        if positron.getClusters().GetEntries() != 0 :
            posCluster=positron.getClusters().First()
            self.EclXEclYPos.Fill(posCluster.getPosition()[0],posCluster.getPosition()[1])
            self.EclEPtrkPos.Fill(posBeam.E(),posCluster.getEnergy())
            self.EclXPtrkPos.Fill(posBeam.E(),posCluster.getPosition()[0])
            posDt=posTrk.getTrackTime()-positron.getClusters().First().getClusterTime()+43.5
            self.trkCluTimeDiffPos.Fill(posDt)
            self.EclTimePtrkPos.Fill(posBeam.E(),posCluster.getClusterTime()-43.5)
            self.TrkTimeEclTimePos.Fill(posCluster.getClusterTime()-43.5,posTrk.getTrackTime())
            print str(posCluster.getClusterTime()) + " " +str(posTrk.getTrackTime())
        if electron.getClusters().GetEntries() != 0 :
            eleCluster=electron.getClusters().First()
            self.EclXEclYEle.Fill(eleCluster.getPosition()[0],eleCluster.getPosition()[1])
            self.EclEPtrkEle.Fill(eleBeam.E(),eleCluster.getEnergy())
            self.EclXPtrkEle.Fill(eleBeam.E(),eleCluster.getPosition()[0])
            eleDt=eleTrk.getTrackTime()-electron.getClusters().First().getClusterTime()+43.5
            self.trkCluTimeDiffEle.Fill(eleDt)
            self.EclTimePtrkEle.Fill(eleBeam.E(),eleCluster.getClusterTime()-43.5)
            self.TrkTimeEclTimeEle.Fill(eleCluster.getClusterTime()-43.5,eleTrk.getTrackTime())

        if  positron.getClusters().GetEntries() != 0 and  electron.getClusters().GetEntries() != 0 :
            self.cluTimeDiff.Fill(electron.getClusters().First().getClusterTime()-positron.getClusters().First().getClusterTime())

                                          
    # note that pE, pP, and pR are in the BEAM frame!
    # ...for truth MC, use this directly
    def fillHistograms(self,pE,pP,pR = None) :
        toDetFrame=self.rotation_matrix(self.beamRotAxis,-self.rotAngle)
        pEDet=self.rotateFourMomentum(pE,toDetFrame)
        pPDet=self.rotateFourMomentum(pP,toDetFrame)
        if pR != None: 
            pRDet=self.rotateFourMomentum(pR,toDetFrame)
#        print pE
#        print pEDet
        mass=math.sqrt(pE.Mag2()+pP.Mag2()+2*(pE*pP))
        self.tridentMass.Fill(mass)
        pV0=pE+pP
        ediff=(pE.E()-pP.E())/pV0.E()
        self.eSum.Fill(pV0.E())  
        self.eDiff.Fill(ediff)
        self.ePosvseEle.Fill(pE.E(),pP.E())
        self.eleMom.Fill(pE.E())
        self.posMom.Fill(pP.E())
        if pR != None :
            self.recMom.Fill(pR.E())
        self.elephi0.Fill(self.getPhi0(pEDet))
        self.posphi0.Fill(self.getPhi0(pPDet))
        self.eleslope.Fill(self.getSlope(pEDet))
        self.posslope.Fill(self.getSlope(pPDet))
        self.eVsSlopeEle.Fill(pE.E(),self.getSlope(pEDet))
        self.eVsSlopePos.Fill(pP.E(),self.getSlope(pPDet))
        self.eVsPhiEle.Fill(pE.E(),self.getPhi0(pEDet))
        self.eVsPhiPos.Fill(pP.E(),self.getPhi0(pPDet))
        if self.getSlope(pEDet) > 0 :
            self.eVsPhiEleTop.Fill(pE.E(),self.getPhi0(pEDet))
            self.eVsPhiPosBottom.Fill(pP.E(),self.getPhi0(pPDet))
        else : 
            self.eVsPhiEleBottom.Fill(pE.E(),self.getPhi0(pEDet))
            self.eVsPhiPosTop.Fill(pP.E(),self.getPhi0(pPDet))

        self.slopeVsPhiEle.Fill(self.getSlope(pEDet),self.getPhi0(pEDet))
        self.slopeVsPhiPos.Fill(self.getSlope(pPDet),self.getPhi0(pPDet))
        self.coplan.Fill(self.getCoplanarity(pEDet,pPDet))
        self.copVseSum.Fill(pV0.E(),self.getCoplanarity(pEDet,pPDet))
        self.elephibeam.Fill(pE.Phi())
        self.posphibeam.Fill(pP.Phi())
        self.elepolarangle.Fill(pE.Theta())
        self.pospolarangle.Fill(pP.Theta())

        dTheta=pE.Theta()-pP.Theta()
        dPhi=pE.Phi()+pP.Phi()
        self.deltaTheta.Fill(dTheta)
        self.deltaPhi.Fill(dPhi)

        a = pE.Angle(pP.Vect())
        self.openAngle.Fill(a)
        self.openVseSum.Fill(pV0.E(),a)
        
        esumBin=int((pV0.E()-self.esumMin)/self.sliceSizeESum)            
        if(esumBin>=self.nSlicesESum) :
            esumBin = self.nSlicesESum-1
        self.eleMomESum[esumBin].Fill(pE.E())
        self.posMomESum[esumBin].Fill(pP.E())
        self.eleThetaESum[esumBin].Fill(self.getSlope(pEDet))
        self.posThetaESum[esumBin].Fill(self.getSlope(pPDet))
        self.elePhi0ESum[esumBin].Fill(self.getPhi0(pEDet))
        self.posPhi0ESum[esumBin].Fill(self.getPhi0(pPDet))
        self.coplanESum[esumBin].Fill(self.getCoplanarity(pEDet,pPDet))
        self.eDiffESum[esumBin].Fill(ediff)
        self.polarAngleESum[esumBin].Fill(pV0.Theta())
        self.phiV0ESum[esumBin].Fill(abs(pV0.Phi())) 
        self.massESum[esumBin].Fill(mass)

        massBin=int((mass-self.massMin)/self.sliceSizeMass)            
        if(massBin>=self.nSlicesMass) :
            massBin = self.nSlicesMass-1
        self.eleMomMass[massBin].Fill(pE.E())
        self.posMomMass[massBin].Fill(pP.E())
        self.eleThetaMass[massBin].Fill(self.getSlope(pEDet))
        self.posThetaMass[massBin].Fill(self.getSlope(pPDet))
        self.elePhi0Mass[massBin].Fill(self.getPhi0(pEDet))
        self.posPhi0Mass[massBin].Fill(self.getPhi0(pPDet))
        self.coplanMass[massBin].Fill(self.getCoplanarity(pEDet,pPDet))
        self.eDiffMass[massBin].Fill(ediff)
        self.polarAngleMass[massBin].Fill(pV0.Theta())
        self.phiV0Mass[massBin].Fill(abs(pV0.Phi())) 
        

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


    def momFromRadius(self,rad,BEff) :
        return abs(rad*BEff*2.99792458e-4)

    def momFromECalPosition(self, x, z, b, BEff) :
        return momFromRadius(radiusFromECal(x,z,b),BEff)

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
