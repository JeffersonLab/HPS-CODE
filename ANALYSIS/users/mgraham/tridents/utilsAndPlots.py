import ROOT 
import math
from ROOT import TLorentzVector
import numpy as np 
me=0.000000511 #kev
class utilsAndPlots:  
    histogramList=[]
    # dictionary structure 
    #  {'FinalState':{'DetHalves':{'HistName':histogram}}}
    #'FinalState'='EpEm'||'EmEm'||'EpEp'||...
    #'DetHalves'='TT','TB','BB' ...
    #'HistName' = 'Esum','d0Ele'...
    histDict={}
    nbinsSmall=50
    nbinsBig=500
    p_mean = [0.289337,   -2.81998,   9.03475, -12.93,   8.71476,   -2.26969]
    p_sig = [4.3987,   -24.2371,   68.9567, -98.2586,   67.562,   -17.8987]

    beam=[np.sin(0.0305),0,np.cos(0.0305)]
    beamRotAxis=[0,1,0]
    rotAngle=-0.0305
    beamAngle = 0.0305
#histogram parameters that don't depend on energy
    mind0=-3
    maxd0=3
#
    minz0=-1.5
    maxz0=1.5
#
    minphi0=-0.1
    maxphi0=0.1
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
    minclx=-200
    maxclx=200
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

    def __init__(self,beamEnergy) : 
    
        #1.05 GeV by default
        self.BEff=0.24
        self.minClE=0.1
        self.maxClE=0.8
        self.minTrkP=0.1
        self.maxTrkP=0.8
        self.minESum=0.2
        self.maxESum=1.14
        self.midESumLow=0.45
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
            self.midESumHigh=self.midESumHigh*0.9*2.3/1.05
            self.midESumLow=1.1
            self.BEff=0.5
            self.clTimeMinCut = 40
            self.clTimeMaxCut = 65


    #  fill two-body plots..
    #  p1 and p2 are final state particles (in detector frame)
    #  ---  if e+ e- final state, p1=positron, p2=electron
    #  ---  if e+/- gamm final state, p1=electron/positron, p2=gamma
    #  ---  otherwise, for identical particles it's in random order
    #  finalState='EpEm','EmEm','EpEp', 'EmGam', 'EpGam', 'GamGam' 
    #  detHalves='TT','TB','BB'
    def fillTwoBody(self,p1,p2,finalState,detHalves) : 
        #calculate stuff
        toBeamFrame=self.rotation_matrix(self.beamRotAxis,self.rotAngle)
        mom1=p1.getMomentum()
        mom2=p2.getMomentum()
        if p1.getType()!=0 : 
            p1Trk=p1.getTracks()[0]
        if p2.getType()!=0 : 
            p2Trk=p2.getTracks()[0]
        if p1.getClusters().GetEntries == 0 : 
            print 'What??? p1 has no cluster?...'
            return
        if p2.getClusters().GetEntries == 0 : 
            print 'What??? p2 has no cluster?...'
            return
        p1Cl=p1.getClusters().First()
        p2Cl=p2.getClusters().First()
        p1ClTime=p1Cl.getClusterTime()
        p2ClTime=p2Cl.getClusterTime()
        if p1.getType()==0: # it's a photon
            mom1=self.makePhotonMometum(p1Cl)            
        if p2.getType==0: # it's a photon
            mom2=self.makePhotonMometum(p2Cl)

        p4p1Beam=self.rotateFourMomentum(self.getLorentzVector(mom1),toBeamFrame)
        p4p2Beam=self.rotateFourMomentum(self.getLorentzVector(mom2),toBeamFrame)
        pV0=p4p1Beam+p4p2Beam
        mass=math.sqrt(pV0.M2())
        ediff=(p4p1Beam.E()-p4p2Beam.E())/pV0.E()

        p1MomFromPosition=self.momFromECalPosition(p1Cl.getPosition()[0],p1Cl.getPosition()[2],self.beamAngle,self.BEff)
        p2MomFromPosition=self.momFromECalPosition(p2Cl.getPosition()[0],p2Cl.getPosition()[2],self.beamAngle,self.BEff)

        self.fill1DHistogram(finalState,detHalves,'eSum',self.nbinsSmall,self.minESum,self.maxESum,pV0.E())
#            
        hname="pairMass"
        val=mass
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minmass,self.maxmass,val)
#
        hname="eDiff"
        val=ediff
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minediff,self.maxediff,val)
#
        hname="clTimeDiff"
        val=p1ClTime-p2ClTime
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mincltimediff,self.maxcltimediff,val)
#
        hname="p1Mom"
        val=p4p1Beam.E()
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkP,self.maxTrkP,val)
#
        hname="p2Mom"
        val=p4p2Beam.E()
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkP,self.maxTrkP,val)
#
        hname="p1Vsp2Mom"
        valx=p4p1Beam.E()
        valy=p4p2Beam.E()
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkP,self.maxTrkP,
                                 self.nbinsSmall,self.minTrkP,self.maxTrkP,valx,valy)       
#
        hname="p1Vsp2XMom"
        valx=p4p1Beam.Px()
        valy=p4p2Beam.Px()
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkPx,self.maxTrkPx,
                                 self.nbinsSmall,self.minTrkPx,self.maxTrkPx,valx,valy)
#
        hname="p1Vsp2YMom"
        valx=p4p1Beam.Py()
        valy=p4p2Beam.Py()
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkPy,self.maxTrkPy,
                                 self.nbinsSmall,self.minTrkPy,self.maxTrkPy,valx,valy)       
#
        hname="p1Vsp2ClE"
        valx=p1Cl.getEnergy()
        valy=p2Cl.getEnergy()
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minClE,self.maxClE,
                                 self.nbinsSmall,self.minClE,self.maxClE,valx,valy)       
#
        hname="p1MomFromClPosVsClE"
        valx=p1Cl.getEnergy()
        valy=p1MomFromPosition
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minClE,self.maxClE,
                                 self.nbinsSmall,self.minTrkP,self.maxTrkP,valx,valy)       
#
        hname="p2MomFromClPosVsClE"
        valx=p2Cl.getEnergy()
        valy=p2MomFromPosition
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minClE,self.maxClE,
                                 self.nbinsSmall,self.minTrkP,self.maxTrkP,valx,valy)       

        hname="coplanVsESum"
        valx=pV0.E()
        valy=self.getECalCoplanarity(p1Cl,p2Cl)
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minESum,self.maxESum,
                                 self.nbinsSmall,self.mincopl,self.maxcopl,valx,valy)       

        hname="V0PyTimesP2Py"
        val=pV0.Py()*np.sign(p4p2Beam.Py())
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minpt,self.maxpt,val)
#
        if p1.getType()!=0 :#only if p1 is a track
            hname="p1d0"
            val=p1Trk.getD0()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mind0,self.maxd0,val)
#
            hname="p1z0"
            val=p1Trk.getZ0()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minz0,self.maxz0,val)
#
            hname="p1phi0"
            val=p1Trk.getPhi0()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minphi0,self.maxphi0,val)
#
            hname="p1slope"
            val=p1Trk.getTanLambda()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minslope,self.maxslope,val)
#
            hname="p1TrkTime"
            val=p1Trk.getTrackTime()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mintrktime,self.maxtrktime,val) 
#
            hname="p1TrkTimeVsClTime"
            valx=p1Trk.getTrackTime()
            valy=p1ClTime
            self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mintrktime,self.maxtrktime,
                                 self.nbinsSmall,self.mincltime,self.maxcltime,valx,valy)       
#
            hname="p1TrkPVsClE"
            valx=p4p1Beam.E()
            valy=p1Cl.getEnergy()
            self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkP,self.maxTrkP,
                                self.nbinsSmall,self.minClE,self.maxClE,valx,valy)
#
        if p2.getType()!=0 :#only if p2 is a track
            hname="p2d0"
            val=p2Trk.getD0()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mind0,self.maxd0,val)
#
            hname="p2z0"
            val=p2Trk.getZ0()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minz0,self.maxz0,val)
#
            hname="p2phi0"
            val=p2Trk.getPhi0()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minphi0,self.maxphi0,val)
#
            hname="p2slope"
            val=p2Trk.getTanLambda()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minslope,self.maxslope,val)
#
            hname="p2TrkTime"
            val=p2Trk.getTrackTime()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mintrktime,self.maxtrktime,val)
#
            hname="p2TrkTimeVsClTime"
            valx=p2Trk.getTrackTime()
            valy=p2ClTime
            self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mintrktime,self.maxtrktime,
                                self.nbinsSmall,self.mincltime,self.maxcltime,valx,valy)
#
            hname="p2TrkPVsClE"
            valx=p4p2Beam.E()
            valy=p2Cl.getEnergy()
            self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minTrkP,self.maxTrkP,
                                self.nbinsSmall,self.minClE,self.maxClE,valx,valy)
#
#
#
        if p2.getType()!=0 and p1.getType() !=0 :#only if p1 _and_ p2 are tracks
            hname="p1Vsp2TrkTime"
            valx=p1Trk.getTrackTime()
            valy=p2Trk.getTrackTime()
            self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mintrktime,self.maxtrktime,
                                self.nbinsSmall,self.mintrktime,self.maxtrktime,valx,valy)
#
            hname="p1p2TrkTimeDiff"
            val=p1Trk.getTrackTime()-p2Trk.getTrackTime()
            self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.mintrktimediff,self.maxtrktimediff,val)

            hname="p1p2SharedHits"
            val=self.getSharedHits(p1Trk,p2Trk)
            self.fill1DHistogram(finalState,detHalves,hname,7,0,7,val)


    def fillThreeBody(self,p1,p2,p3,finalState,detHalves) : 
        #calculate stuff
        toBeamFrame=self.rotation_matrix(self.beamRotAxis,self.rotAngle)
        mom1=p1.getMomentum()
        mom2=p2.getMomentum()
        mom3=p3.getMomentum()
        if p1.getType()!=0 : 
            p1Trk=p1.getTracks()[0]
        if p2.getType()!=0 : 
            p2Trk=p2.getTracks()[0]
        if p3.getType()!=0 : 
            p3Trk=p3.getTracks()[0]
        if p1.getClusters().GetEntries == 0 : 
            print 'What??? p1 has no cluster?...'
            return
        if p2.getClusters().GetEntries == 0 : 
            print 'What??? p2 has no cluster?...'
            return
        if p3.getClusters().GetEntries == 0 : 
            print 'What??? p3 has no cluster?...'
            return
        p1Cl=p1.getClusters().First()
        p2Cl=p2.getClusters().First()
        p3Cl=p3.getClusters().First()
        p1ClTime=p1Cl.getClusterTime()
        p2ClTime=p2Cl.getClusterTime()
        p3ClTime=p3Cl.getClusterTime()
        if p1.getType()==0: # it's a photon
            mom1=self.makePhotonMometum(p1Cl)            
        if p2.getType==0: # it's a photon
            mom2=self.makePhotonMometum(p2Cl)
        if p3.getType==0: # it's a photon
            mom3=self.makePhotonMometum(p3Cl)

        p4p1Beam=self.rotateFourMomentum(self.getLorentzVector(mom1),toBeamFrame)
        p4p2Beam=self.rotateFourMomentum(self.getLorentzVector(mom2),toBeamFrame)
        p4p3Beam=self.rotateFourMomentum(self.getLorentzVector(mom3),toBeamFrame)
        pV0=p4p1Beam+p4p2Beam+p4p3Beam
        p12=p4p1Beam+p4p2Beam
        p13=p4p1Beam+p4p3Beam
        mass=math.sqrt(pV0.M2())
               
        hname="threeBodyMass"
        val=mass
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minmass,self.maxmass,val)
#
        hname="threeBodyeSum"
        val=pV0.E()
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minESum,self.maxESum,val)
# 
        hname="threeBodypT"
        val=pV0.Pt()
        self.fill1DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minpt,self.maxpt,val)
#
        hname="p1p2Vsp1p3ESum"
        valx=p12.E()
        valy=p13.E()
        self.fill2DHistogram(finalState,detHalves,hname,self.nbinsSmall,self.minESum,self.maxESum,
                             self.nbinsSmall,self.minESum,self.maxESum,valx,valy)

        self.fillTwoBody(p1,p2,finalState+"-p1p2",detHalves)
        self.fillTwoBody(p1,p3,finalState+"-p1p3",detHalves)
        self.fillTwoBody(p2,p3,finalState+"-p2p3",detHalves)


    def book1DHistogram(self,fs,dh,hname,nbins,minX,maxX) : 
        name=fs+dh+"-"+hname
        title=hname+fs+dh
        self.histogramList.append(ROOT.TH1D(name,title,nbins,minX,maxX))
        try : 
            foodict=self.histDict[fs] 
        except KeyError, e:
            self.histDict[fs]={}
        try : 
            foodict=self.histDict[fs][dh]
        except KeyError, e:
            self.histDict[fs][dh]={}
            
        self.histDict[fs][dh][hname]=self.histogramList[-1]
                    
    def fill1DHistogram(self,fs,dh,hname,nbins,minX,maxX,val) : 
        try :
            hist=self.histDict[fs][dh][hname]; 
        except KeyError, e:
            self.book1DHistogram(fs,dh,hname,nbins,minX,maxX)
            
        self.histDict[fs][dh][hname].Fill(val)

    def book2DHistogram(self,fs,dh,hname,nbinsx,minX,maxX,nbinsy,minY,maxY) : 
        name=fs+dh+"-"+hname
        title=hname+fs+dh
        self.histogramList.append(ROOT.TH2D(name,title,nbinsx,minX,maxX,nbinsy,minY,maxY))
        try : 
            foodict=self.histDict[fs] 
        except KeyError, e:
            self.histDict[fs]={}
        try : 
            foodict=self.histDict[fs][dh]
        except KeyError, e:
            self.histDict[fs][dh]={}
            
        self.histDict[fs][dh][hname]=self.histogramList[-1]
                    
    def fill2DHistogram(self,fs,dh,hname,nbinsx,minX,maxX,nbinsy,minY,maxY,valx,valy) : 
        try :
            hist=self.histDict[fs][dh][hname]; 
        except KeyError, e:
            self.book2DHistogram(fs,dh,hname,nbinsx,minX,maxX,nbinsy,minY,maxY)
            
        self.histDict[fs][dh][hname].Fill(valx,valy)


#below are some useful utilities
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
        p.SetE(float(math.sqrt(self.pMag(mom)*self.pMag(mom)+me*me)))
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
        return self.momFromRadius(self.radiusFromECal(x,z,b),BEff)

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


    def getSharedHits(self,trk1,trk2) : 
        hitsTrk1=trk1.getSvtHits()  
        hitsTrk2=trk2.getSvtHits()
        overlap=0
        for hit1 in hitsTrk1 : 
            for hit2 in hitsTrk2 : 
                if hit1 == hit2 : 
#                    print "found overlapping hit"
                    overlap+=1
        return overlap


    def checkIfShared(self, fspList,fspCand) : 
#        print 'checkIfShared::fspList is '+str(len(fspList))+' tracks long'
        for ind in range(0,len(fspList)) : 
            fsp=fspList[ind]
            trk=fsp.getTracks()[0]
            trkCand=fspCand.getTracks()[0]
            if self.getSharedHits(trk,trkCand) > 2 :
#                print 'found shared track  ' + str(self.getSharedHits(trk,trkCand) )
                if len(trkCand.getSvtHits()) > len(trk.getSvtHits()): 
                    #replace element in fspList
#                    print 'replacing track in list because trkCand has '+str(  len(trkCand.getSvtHits()) ) +' while trk only has '+str(len(trk.getSvtHits()))
                    fspList[ind]=fspCand  ###  does this work?  
#                    print '...now trk has '+str(len(fspList[ind].getTracks()[0].getSvtHits()))
                return True
        return False

    #cluster time cut...
    def clusterTimingCut(self,cl_ti) : 
        if not (cl_ti > self.clTimeMinCut and cl_ti < self.clTimeMaxCut ):
            return False
        return True
###########
    def clusterCoincidence(self,p1,p2) :
        if p1.getClusters().GetEntries == 0 : 
            return false
        if p2.getClusters().GetEntries == 0 : 
            return false

        p1Cl=p1.getClusters().First()
        p2Cl=p2.getClusters().First()
#        if p1Cl==p2Cl : # pointing to the same cluster!!!
#            return false 

        p1ClTime=p1Cl.getClusterTime()
        p2ClTime=p2Cl.getClusterTime()
        p1Cle=p1Cl.getEnergy()
        p2Cle=p2Cl.getEnergy()
        return self.clusterPairTimingCoincidenceCut(p1ClTime-p2ClTime,p1Cle+p2Cle)
#        return True

#############
    #cluster pair cut...3*sigma, Esum dependent
    def clusterPairTimingCoincidenceCut(self,dt, Esum) : 
#   //================ Time coincidence ======================================
#   // these numbers are from Rafo circa ~ spring 2016....based on 2015 data, 
#        coincide_pars_mean = [0.289337,   -2.81998,   9.03475, -12.93,   8.71476,   -2.26969]
#        coincide_pars_sigm = [4.3987,   -24.2371,   68.9567, -98.2586,   67.562,   -17.8987]
   
#        formula_pol5 = "[0] + x*( [1] + x*( [2] + x*( [3] + x*( [4] + x*( [5] ) ) ) ) ) "
#       f_coincide_clust_mean = ROOT.TF1("f_coincide_clust_mean", formula_pol5, 0., 1.4)
#        f_coincide_clust_sigm = ROOT.TF1("f_coincide_clust_sigm", formula_pol5, 0., 1.4)
#        f_coincide_clust_mean.SetParameters(np.array(coincide_pars_mean))
#        f_coincide_clust_sigm.SetParameters(np.array(coincide_pars_sigm))        

#   //The cut is            === mean - 3sigma < dt < mean + 3sigma ===
#      divide by energy ratio since these parameters were extracted from 1.05GeV Data (this is kludgy!)    
#        delt_t_mean = f_coincide_clust_mean.Eval(Esum/self.energyRatio)
#        delt_t_sigm = f_coincide_clust_sigm.Eval(Esum/self.energyRatio)  

        esumScaled=Esum/self.energyRatio


        delt_t_mean=self.p_mean[0]+esumScaled*(
            self.p_mean[1]+esumScaled*(
                self.p_mean[2]+esumScaled*(
                    self.p_mean[3]+esumScaled*(
                        self.p_mean[4]+esumScaled*(
                            self.p_mean[5])))))

        delt_t_sigm=self.p_sig[0]+esumScaled*(
            self.p_sig[1]+esumScaled*(
                self.p_sig[2]+esumScaled*(
                    self.p_sig[3]+esumScaled*(
                        self.p_sig[4]+esumScaled*(
                            self.p_sig[5])))))

        if not  (dt < delt_t_mean + 3*delt_t_sigm and dt > delt_t_mean - 3*delt_t_sigm) :
            return False

        return True

    @staticmethod
    def makePhotonMomentum(cl) : 
        dS=math.sqrt(cl.getPosition()[0]*cl.getPosition()[0]+cl.getPosition()[1]*cl.getPosition()[1]+cl.getPosition()[2]*cl.getPosition()[2])
        return [cl.getEnergy()*cl.getPosition()[0]/dS, cl.getEnergy()*cl.getPosition()[1]/dS,cl.getEnergy()*cl.getPosition()[2]/dS]

    @staticmethod
    def getECalCoplanarity(cl1,cl2): 
        radian = ROOT.TMath.RadToDeg();
        phot_nom_x = 42.52  #nominal photon position (px=0)
        if cl1.getPosition()[1] >0 : 
            topX=cl1.getPosition()[0]
            topY=cl1.getPosition()[1]
            botX=cl2.getPosition()[0]
            botY=cl2.getPosition()[1]
        else : 
            botX=cl1.getPosition()[0]
            botY=cl1.getPosition()[1]
            topX=cl2.getPosition()[0]
            topY=cl2.getPosition()[1]
        cl_impact_angleTop = math.atan2(topY, topX - phot_nom_x)*radian
        cl_impact_angleBottom = math.atan2(botY,botX - phot_nom_x)*radian
        if cl_impact_angleTop < 0. :
            cl_impact_angleTop = cl_impact_angleTop + 360. 
        if cl_impact_angleBottom < 0. :
            cl_impact_angleBottom = cl_impact_angleBottom + 360.
        #        print  str(cl_impact_angleTop)+'   '+str(cl_impact_angleBottom)
        return (cl_impact_angleBottom -  cl_impact_angleTop )
