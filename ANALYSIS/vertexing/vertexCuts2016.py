#!/usr/bin/env python
import sys
tmpargv = sys.argv
sys.argv = []
import getopt
from ROOT import gROOT, TFile, TTree, TChain, gDirectory
sys.argv = tmpargv

def print_usage():
    print "\nUsage: {0} <output ROOT file name> <input ROOT file names>".format(sys.argv[0])
    print "Arguments: "

    print '\t-l: apply loose vertexing cuts'
    print '\t-f: apply loose L1L1 vertexing cuts'
    print '\t-g: apply loose L1L2 vertexing cuts'
    print '\t-i: apply loose L2L2 vertexing cuts'
    print '\t-v: apply default vertexing cuts'
    print '\t-w: apply default L1L1 vertexing cuts'
    print '\t-x: apply default L1L2 vertexing cuts'
    print '\t-y: apply default L2L2 vertexing cuts'
    print '\t-t: apply tight cut'
    print '\t-q: apply L1L1 isolation cut'
    print '\t-r: apply L1L2 isolation cut'
    print '\t-s: apply L2L2 isolation cut'
    print '\t-d: apply custom cuts'
    print '\t-j: uncVX mean (default 0)'
    print '\t-k: uncVX sigma (default 9999)'
    print '\t-m: uncVY mean (default 0)'
    print '\t-n: uncVY sigma (default 9999)'
    print '\t-o: uncTargProjX mean (default 0)'
    print '\t-p: uncTargProjX sigma (default 9999)'
    print '\t-a: uncTargProjY mean (default 0)'
    print '\t-b: uncTargProjY sigma (default 9999)'
    print '\t-e: use this beam energy (default 2.3)'
    print '\t-c: use this cluster-track deltaT (default 55.0)'
    print '\t-z: use this target Z (default -4.3)'
    print '\t-h: this help message'
    print

ebeam = 2.3
clusterT = 55.0
targetZ = -4.3
uncVX = 0.
uncVXSig = 9999.
uncVY = 0.
uncVYSig = 9999.
uncTargProjX = 0.
uncTargProjXSig = 9999.
uncTargProjY = 0.
uncTargProjYSig = 9999.

loosevertCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<1.45&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&uncChisq<10&&max(eleTrkChisq/(2*eleNTrackHits-5),posTrkChisq/(2*posNTrackHits-5))<6&&eleP>0.4&&posP>0.4&&uncP<2.4"#&&eleHasL2&&posHasL2" #&&uncP>1.85" #&&eleHasL1&&posHasL1

#loosevertCutL1L1 = "eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2.0&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&bscChisq<15&&max(eleTrkChisq/eleNTrackHits,posTrkChisq/posNTrackHits)<6&&nPos<2"

loosevertCutL1L1 = "eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2.0&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&uncChisq<10&&max(eleTrkChisq/(2*eleNTrackHits-5),posTrkChisq/(2*posNTrackHits-5))<6&&eleP<1.75"

#loosevertCutL1L2 = "((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2.0&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&bscChisq<15&&max(eleTrkChisq/eleNTrackHits,posTrkChisq/posNTrackHits)<6&&nPos<2"

loosevertCutL1L2 = "((!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1))&&eleHasL2&&posHasL2&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2.0&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&uncChisq<10&&max(eleTrkChisq/(2*eleNTrackHits-5),posTrkChisq/(2*posNTrackHits-5))<6&&eleP<1.75"

#loosevertCutL2L2 = "!eleHasL1&&!posHasL1&&eleHasL2&&posHasL2&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2.0&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&bscChisq<15&&max(eleTrkChisq/eleNTrackHits,posTrkChisq/posNTrackHits)<6&&nPos<2"

loosevertCutL2L2 = "!eleHasL1&&!posHasL1&&eleHasL2&&posHasL2&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleClT-posClT)<2.0&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&eleClY*posClY<0&&uncChisq<10&&max(eleTrkChisq/(2*eleNTrackHits-5),posTrkChisq/(2*posNTrackHits-5))<6&&eleP<1.75"

vertCut = "isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&abs(eleP-posP)/(eleP+posP)<0.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(elePhiKink2)<0.002&&abs(posPhiKink2)<0.002&&abs(elePhiKink3)<0.002&&abs(posPhiKink3)<0.002&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(eleLambdaKink2)<0.004&&abs(posLambdaKink2)<0.004&&abs(eleLambdaKink3)<0.004&&abs(posLambdaKink3)<0.004"

trkExtrpCutL1L2 = "(!eleHasL1&&posHasL1&&((eleTrkExtrpYSensorAxialTopL1<-19.2&&eleTrkExtrpYSensorAxialTopL1>-9998)||(eleTrkExtrpYSensorAxialBotL1<-19.2&&eleTrkExtrpYSensorAxialBotL1>-9998))&&(eleTrkExtrpYSensorStereoTopL1>19.2||eleTrkExtrpYSensorStereoBotL1>19.2))||(!posHasL1&&eleHasL1&&((posTrkExtrpYSensorAxialTopL1<-19.2&&posTrkExtrpYSensorAxialTopL1>-9998)||(posTrkExtrpYSensorAxialBotL1<-19.2&&posTrkExtrpYSensorAxialBotL1>-9998))&&(posTrkExtrpYSensorStereoTopL1>19.2||posTrkExtrpYSensorStereoBotL1>19.2))"

trkExtrpCutL2L2 = "(((eleTrkExtrpYSensorAxialTopL1<-19.2&&eleTrkExtrpYSensorAxialTopL1>-9998)||(eleTrkExtrpYSensorAxialBotL1<-19.2&&eleTrkExtrpYSensorAxialBotL1>-9998))&&((posTrkExtrpYSensorAxialTopL1<-19.2&&posTrkExtrpYSensorAxialTopL1>-9998)||(posTrkExtrpYSensorAxialBotL1<-19.2&&posTrkExtrpYSensorAxialBotL1>-9998))&&((eleTrkExtrpYSensorStereoTopL1>19.2||eleTrkExtrpYSensorStereoBotL1>19.2)&&(posTrkExtrpYSensorStereoTopL1>19.2||posTrkExtrpYSensorStereoBotL1>19.2)))"

vertCutL1L1 = "eleHasL1&&posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq/eleNTrackHits,posTrkChisq/posNTrackHits)<5&&abs(eleP-posP)/(eleP+posP)<0.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(elePhiKink2)<0.002&&abs(posPhiKink2)<0.002&&abs(elePhiKink3)<0.002&&abs(posPhiKink3)<0.002&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(eleLambdaKink2)<0.004&&abs(posLambdaKink2)<0.004&&abs(eleLambdaKink3)<0.004&&abs(posLambdaKink3)<0.004"

vertCutL1L2 = "isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&abs(eleP-posP)/(eleP+posP)<0.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2&&((!eleHasL1&&posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0)||(eleHasL1&&!posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0))&&((!eleHasL1&&posHasL1&&((eleTrkExtrpYSensorAxialTopL1<-19.2&&eleTrkExtrpYSensorAxialTopL1>-9998)||(eleTrkExtrpYSensorAxialBotL1<-19.2&&eleTrkExtrpYSensorAxialBotL1>-9998))&&(eleTrkExtrpYSensorStereoTopL1>19.2||eleTrkExtrpYSensorStereoBotL1>19.2))||(eleHasL1&&!posHasL1&&((posTrkExtrpYSensorAxialTopL1<-19.2&&posTrkExtrpYSensorAxialTopL1>-9998)||(posTrkExtrpYSensorAxialBotL1<-19.2&&posTrkExtrpYSensorAxialBotL1>-9998))&&(posTrkExtrpYSensorStereoTopL1>19.2||posTrkExtrpYSensorStereoBotL1>19.2)))&&((uncVX-(uncVZ-{2})*uncPX/uncPZ)**2/(0.64)+(uncVY-(uncVZ-{2})*uncPY/uncPZ)**2/(0.64))<1&&abs(bscVY-(bscVZ-{2})*bscPY/bscPZ)<0.5&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(elePhiKink2)<0.002&&abs(posPhiKink2)<0.002&&abs(elePhiKink3)<0.002&&abs(posPhiKink3)<0.002&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(eleLambdaKink2)<0.004&&abs(posLambdaKink2)<0.004&&abs(eleLambdaKink3)<0.004&&abs(posLambdaKink3)<0.004"


#vertCutL1L2 = "isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&abs(eleP-posP)/(eleP+posP)<0.5&&posTrkD0+{2}*posPX/posP<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2&&((!eleHasL1&&posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&((eleTrkExtrpYSensorAxialTopL1<-19.2&&eleTrkExtrpYSensorAxialTopL1>-9998)||(eleTrkExtrpYSensorAxialBotL1<-19.2&&eleTrkExtrpYSensorAxialBotL1>-9998))&&(eleTrkExtrpYSensorStereoTopL1>19.2||eleTrkExtrpYSensorStereoBotL1>19.2))||(eleHasL1&&!posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0)&&((posTrkExtrpYSensorAxialTopL1<-19.2&&posTrkExtrpYSensorAxialTopL1>-9998)||(posTrkExtrpYSensorAxialBotL1<-19.2&&posTrkExtrpYSensorAxialBotL1>-9998))&&(posTrkExtrpYSensorStereoTopL1>19.2||posTrkExtrpYSensorStereoBotL1>19.2))"

vertCutL2L2 = "!eleHasL1&&!posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&abs(eleP-posP)/(eleP+posP)<0.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2&&(((eleTrkExtrpYSensorAxialTopL1<-19.2&&eleTrkExtrpYSensorAxialTopL1>-9998)||(eleTrkExtrpYSensorAxialBotL1<-19.2&&eleTrkExtrpYSensorAxialBotL1>-9998))&&((posTrkExtrpYSensorAxialTopL1<-19.2&&posTrkExtrpYSensorAxialTopL1>-9998)||(posTrkExtrpYSensorAxialBotL1<-19.2&&posTrkExtrpYSensorAxialBotL1>-9998))&&((eleTrkExtrpYSensorStereoTopL1>19.2||eleTrkExtrpYSensorStereoBotL1>19.2)&&(posTrkExtrpYSensorStereoTopL1>19.2||posTrkExtrpYSensorStereoBotL1>19.2)))&&!((uncVZ>74.6&&uncVZ<111.4&&uncVY>0.4)||(uncVZ>95.6&&uncVZ<121.3&&uncVY<-0.4))&&((uncVX-(uncVZ-{2})*uncPX/uncPZ)**2/(0.64)+(uncVY-(uncVZ-{2})*uncPY/uncPZ)**2/(0.64))<1&&abs(bscVY-(bscVZ-{2})*bscPY/bscPZ)<0.5&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(elePhiKink2)<0.002&&abs(posPhiKink2)<0.002&&abs(elePhiKink3)<0.002&&abs(posPhiKink3)<0.002&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(eleLambdaKink2)<0.004&&abs(posLambdaKink2)<0.004&&abs(eleLambdaKink3)<0.004&&abs(posLambdaKink3)<0.004"

#tightCut = "uncChisq<4&&uncP>0.8*{0}&&uncP<1.15*{0}&&abs(uncVX-{3})<3*{4}&&abs(uncVY-{5})<3*{6}&&abs(uncTargProjX-{7})<3*{8}&&abs(uncTargProjY-{9})<3*{10}"

#tightCut = "eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&uncChisq<4&&uncP>1.55&&sqrt((uncVX-{3})^2/(3*{4})^2+(uncVY-{5})^2/(3*{6})^2)<1&&sqrt((uncTargProjX-{7})^2/(3*{8})^2+(uncTargProjY-{9})^2/(3*{10})^2)<1&&(eleMinPositiveIso+0.5*((eleTrkZ0+{2}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({2}*eleTrkLambdaErr)+abs(2*{2}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega))))>0&&(posMinPositiveIso+0.5*((posTrkZ0+{2}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({2}*posTrkLambdaErr)+abs(2*{2}*posTrkLambda*posTrkOmegaErr/posTrkOmega))))>0"

#tightCut = "eleHasL2&&posHasL2&&uncChisq<4&&uncP>1.55&&sqrt((uncVX-{3})^2/(3*{4})^2+(uncVY-{5})^2/(3*{6})^2)<1&&sqrt(((uncVX-(uncVZ-{2})*uncPX/uncPZ)-{7})^2/(3*{8})^2+((uncVY-(uncVZ-{2})*uncPY/uncP)-{9})^2/(3*{10})^2)<1&&(eleMinPositiveIso+0.5*((eleTrkZ0+{2}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({2}*eleTrkLambdaErr)+abs(2*{2}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega))))>0&&(posMinPositiveIso+0.5*((posTrkZ0+{2}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({2}*posTrkLambdaErr)+abs(2*{2}*posTrkLambda*posTrkOmegaErr/posTrkOmega))))>0"

#tightCut = "eleHasL2&&posHasL2&&uncChisq<4&&uncP>1.55&&(eleMinPositiveIso+0.5*((eleTrkZ0+{2}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({2}*eleTrkLambdaErr)+abs(2*{2}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega))))>0&&(posMinPositiveIso+0.5*((posTrkZ0+{2}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({2}*posTrkLambdaErr)+abs(2*{2}*posTrkLambda*posTrkOmegaErr/posTrkOmega))))>0"

isoCutL1L1 = "eleHasL1&&posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP+3*(eleTrkZ0err+abs({2}*eleTrkLambdaErr)+abs(2*{2}*eleTrkLambda*eleTrkOmega/eleTrkOmegaErr)))*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP+3*(posTrkZ0err+abs({2}*posTrkLambdaErr)+abs(2*{2}*posTrkLambda*posTrkOmega/posTrkOmegaErr)))*sign(posPY))>0"

isoCutL1L2 = "((!eleHasL1&&posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0)||(eleHasL1&&!posHasL1&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0))"

isoCutL2L2 = "min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0"


#vertCutL2L2 = "!eleHasL1&&!posHasL1&&min(eleMinPositiveIsoL2+0.33*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIsoL2+0.33*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&isPair1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&abs(eleP-posP)/(eleP+posP)<0.5&&posTrkD0+{2}*posPX/posP<1.5&&eleP<{0}*0.75&&uncP<{0}*1.15&&uncP>{0}*0.8&&eleHasL2&&posHasL2&&(((eleTrkExtrpYSensorAxialTopL1<-19.2&&eleTrkExtrpYSensorAxialTopL1>-9998)||(eleTrkExtrpYSensorAxialBotL1<-19.2&&eleTrkExtrpYSensorAxialBotL1>-9998))&&((posTrkExtrpYSensorAxialTopL1<-19.2&&posTrkExtrpYSensorAxialTopL1>-9998)||(posTrkExtrpYSensorAxialBotL1<-19.2&&posTrkExtrpYSensorAxialBotL1>-9998))&&((eleTrkExtrpYSensorStereoTopL1>19.2||eleTrkExtrpYSensorStereoBotL1>19.2)&&(posTrkExtrpYSensorStereoTopL1>19.2||posTrkExtrpYSensorStereoBotL1>19.2)))"

#customCut = "sqrt(((bscVX-(bscVZ-{0})*bscPX/bscPZ)/(0.0801*2))**2+((bscVY-(bscVZ-{0})*bscPY/bscPZ)/(0.0288*2))**2)<1&&sqrt(((uncVX-(uncVZ-{0})*uncPX/uncPZ)/(0.331*2))**2+((uncVY-(uncVZ-{0})*uncPY/uncPZ)/(0.31*2))**2)<1"

#customCut = "isPair1&&eleHasL1&&posHasL1&&max(eleMatchChisq,posMatchChisq)<10&&max(abs(eleClT-eleTrkT-{1}),abs(posClT-posTrkT-{1}))<4&&abs(eleClT-posClT)<2&&eleClY*posClY<0&&bscChisq<10&&bscChisq-uncChisq<5&&max(eleTrkChisq,posTrkChisq)<30&&min(eleMinPositiveIso+0.5*(eleTrkZ0+{2}*elePY/eleP)*sign(elePY),posMinPositiveIso+0.5*(posTrkZ0+{2}*posPY/posP)*sign(posPY))>0&&eleP<{0}*0.4&&posP<{0}*0.4&&uncP<{0}*0.65&&uncP>{0}*0.4&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(elePhiKink2)<0.002&&abs(posPhiKink2)<0.002&&abs(elePhiKink3)<0.002&&abs(posPhiKink3)<0.002&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(eleLambdaKink2)<0.004&&abs(posLambdaKink2)<0.004&&abs(eleLambdaKink3)<0.004&&abs(posLambdaKink3)<0.004&&(pow((uncVX-(uncVZ-0.5)*uncPX/uncPZ-0.1)*cos(-0.5)-(uncVY-(uncVZ-0.5)*uncPY/uncPZ)*sin(-0.5),2)/0.4356+pow((uncVX-(uncVZ-0.5)*uncPX/uncPZ)*sin(-0.5)+(uncVY-(uncVZ-0.5)*uncPY/uncPZ)*cos(-0.5),2)/0.3249)<1&&abs(bscVY-(bscVZ-{0})*bscPY/bscPZ)<0.4"

#customCut = "eleClY*posClY<0&&eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&bscChisq<10&&bscChisq-uncChisq<5&&abs(eleClT-posClT)<2&&uncP>0.8*1.056&&uncP<1.15*1.056&&eleP<0.75*1.056&&min(eleMinPositiveIso+0.5*(eleTrkZ0+0.5*uncElePY/uncEleP)*sign(uncElePY),posMinPositiveIso+0.5*(posTrkZ0+0.5*uncPosPY/uncPosP)*sign(uncPosPY))>0&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleP-posP)/uncP<0.5&&(pow((uncVX-(uncVZ)*uncPX/uncPZ-0.05)*cos(-0.5)-(uncVY-(uncVZ)*uncPY/uncPZ)*sin(-0.5),2)/0.55+pow((uncVX-(uncVZ)*uncPX/uncPZ)*sin(-0.5)+(uncVY-(uncVZ)*uncPY/uncPZ)*cos(-0.5),2)/0.25)<1&&uncM<0.1&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(elePhiKink1)<0.002&&abs(posPhiKink1)<0.002&&abs(eleLambdaKink1)<0.004&&abs(posLambdaKink1)<0.004&&abs(elePhiKink1)<0.002&&abs(posPhiKink1)<0.002&&abs(eleLambdaKink1)<0.004&&abs(posLambdaKink1)<0.004&&(eleTrkChisq/(2.0*eleNTrackHits-5.0)+posTrkChisq/(2.0*posNTrackHits-5.0))<6.0"

#customCut = "eleClY*posClY<0&&eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&bscChisq<10&&bscChisq-uncChisq<5&&abs(eleClT-posClT)<2&&uncP>0.8*2.3&&uncP<1.15*2.3&&eleP<0.75*2.3&&min(eleMinPositiveIso+0.5*(eleTrkZ0-4*uncElePY/uncEleP)*sign(uncElePY),posMinPositiveIso+0.5*(posTrkZ0-4*uncPosPY/uncPosP)*sign(uncPosPY))>0&&max(eleMatchChisq,posMatchChisq)<10&&abs(eleP-posP)/uncP<0.5&&(pow((uncVX-(uncVZ)*uncPX/uncPZ-0.05)*cos(-0.5)-(uncVY-(uncVZ)*uncPY/uncPZ)*sin(-0.5),2)/0.55+pow((uncVX-(uncVZ)*uncPX/uncPZ)*sin(-0.5)+(uncVY-(uncVZ)*uncPY/uncPZ)*cos(-0.5),2)/0.25)<1&&uncM<0.2&&abs(elePhiKink1)<0.0001&&abs(posPhiKink1)<0.0001&&abs(eleLambdaKink1)<0.002&&abs(posLambdaKink1)<0.002&&abs(elePhiKink1)<0.002&&abs(posPhiKink1)<0.002&&abs(eleLambdaKink1)<0.004&&abs(posLambdaKink1)<0.004&&abs(elePhiKink1)<0.002&&abs(posPhiKink1)<0.002&&abs(eleLambdaKink1)<0.004&&abs(posLambdaKink1)<0.004&&(eleTrkChisq/(2.0*eleNTrackHits-5.0)+posTrkChisq/(2.0*posNTrackHits-5.0))<6.0&&max(abs(eleClT-eleTrkT-55),abs(posClT-posTrkT-55))<4"

x0_cut1_pos_x0 = -0.2289
x1_cut1_pos_x0 = -1.09

x0_cut1_neg_x0 = -0.0009241
x1_cut1_neg_x0 = -1.612

x0_cut1_pos_x1 = 0.009205
x1_cut1_pos_x1 = 0.2069

x0_cut1_neg_x1 = 0.0091
x1_cut1_neg_x1 = 0.2341

dz = "(-3.517-13.41*uncM+88.16*uncM^2-173.1*uncM^3)-(-3.14-27.2*uncM+144*uncM^2-257.1*uncM^3)"
#dz = 0

x0_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x0,x1_cut1_pos_x0)
x1_cut1_pos = "({0}+{1}*uncM)".format(x0_cut1_pos_x1,x1_cut1_pos_x1)
cut1_pos = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_pos,x1_cut1_pos,dz)

x0_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x0,x1_cut1_neg_x0)
x1_cut1_neg = "({0}+{1}*uncM)".format(x0_cut1_neg_x1,x1_cut1_neg_x1)
cut1_neg = "({0}+{1}*(uncVZ+{2}))".format(x0_cut1_neg,x1_cut1_neg,dz)

z0cut = "((eleTrkZ0>{0}&&-posTrkZ0>{1})||(posTrkZ0>{0}&&-eleTrkZ0>{1}))".format(cut1_pos,cut1_neg)
#z0cut = "((eleTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*(uncVZ+{0}))&&-posTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.177913468428+-0.932330924205*uncM)+(0.00961915803124+0.228303547556*uncM)*uncVZ)&&-eleTrkZ0>((0.0115212779435+-0.651929048499*uncM)+(0.0125216209858+0.217752673675*uncM)*(uncVZ+{0}))))".format(dz) #80% L1L1
#z0cut = "((eleTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-posTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0})))||(posTrkZ0>((-0.204298550172+-0.819203072994*uncM)+(0.0215541584276+0.0769066743212*uncM)*(uncVZ+{0}))&&-eleTrkZ0>((-0.0131964462788+-0.356152922206*uncM)+(0.0199952852357+0.0682704240163*uncM)*(uncVZ+{0}))))".format(dz) #80% L1L2

#eleiso = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targetZ) #L1L1
#posiso = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targetZ) #L1L1

eleisoL1 = "eleMinPositiveIso+0.5*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targetZ) #L1L2
posisoL1 = "posMinPositiveIso+0.5*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targetZ) #L1L2

eleisoL2 = "eleMinPositiveIso+1/3.*((eleTrkZ0+{0}*elePY/eleP)*sign(elePY)-3*(eleTrkZ0Err+abs({0}*eleTrkLambdaErr)+abs(2*{0}*eleTrkLambda*eleTrkOmegaErr/eleTrkOmega)))>0".format(targetZ) #L1L2
posisoL2 = "posMinPositiveIso+1/3.*((posTrkZ0+{0}*posPY/posP)*sign(posPY)-3*(posTrkZ0Err+abs({0}*posTrkLambdaErr)+abs(2*{0}*posTrkLambda*posTrkOmegaErr/posTrkOmega)))>0".format(targetZ) #L1L2

eleiso = "((eleHasL1&&{0})||(!eleHasL1&&{1}))".format(eleisoL1,eleisoL2)
posiso = "((posHasL1&&{0})||(!posHasL1&&{1}))".format(posisoL1,posisoL2)

isocut = "({0}&&{1})".format(eleiso,posiso)

#tightCut = "eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&uncChisq<4&&uncP>2.0&&sqrt((uncVX-{3})^2/(3*{4})^2+(uncVY-{5})^2/(3*{6})^2)<1&&sqrt(((uncVX-(uncVZ-{0})*uncPX/uncPZ)-{7})^2/(2*{8})^2+((uncVY-(uncVZ-{0})*uncPY/uncPZ)-{9})^2/(2*{10})^2)<1&&"+isocut+"&&"+z0cut #L1L1

tightCut = "((eleHasL1&&!posHasL1)||(!eleHasL1&&posHasL1))&&eleHasL2&&posHasL2&&uncChisq<4&&uncP>2.0&&sqrt((uncVX-{3})^2/(3*1.25*{4})^2+(uncVY-{5})^2/(3*1.5*{6})^2)<1&&sqrt(((uncVX-(uncVZ-{0})*uncPX/uncPZ)-{7})^2/(2*1.25*{8})^2+((uncVY-(uncVZ-{0})*uncPY/uncPZ)-{9})^2/(2*1.5*{10})^2)<1&&"+isocut+"&&"+z0cut #L1L2

#customCut = "eleHasL1&&posHasL1&&eleHasL2&&posHasL2&&uncChisq<4&&uncP>1.55&&({0})&&({1})".format(z0cut,isocut)
#customCut = "uncP>0.8*2.3"
#customCut = "eleNHitsShared<1&&posNHitsShared<1&&nSVTHitsL1<100&&nSVTHitsL1b<100&&eleTrkChisq/(2*eleNTrackHits-5)+posTrkChisq/(2*posNTrackHits-5)<6"

#customCut = "eleHasL1&&posHasL1"
#customCut = "(!eleHasL1&&posHasL1)||(eleHasL1&&!posHasL1)"
#customCut = "!eleHasL1&&!posHasL1&&eleHasL2&&posHasL2"
#customCut = "sqrt((uncVX-{3})^2/(3*{4})^2+(uncVY-{5})^2/(3*{6})^2)<1&&sqrt(((uncVX-(uncVZ-{0})*uncPX/uncPZ)-{7})^2/(3*{8})^2+((uncVY-(uncVZ-{0})*uncPY/uncPZ)-{9})^2/(3*{10})^2)<1"
#customCut = "isPair1&&tarP<2.4&&tarP>1.9&&abs(eleClT-posClT)<1.43"
#customCut = "eleHasL2&&posHasL2&&uncP>1.85"
#customCut = "uncVZ>({0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(21.61,-339.8,6319,-84860,556600,-1362000)
customCut = "eleHasL1&&posHasL1&&uncVZ>({0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(19,53.04,-2566,-4258,2.345e5,-8.994e5)
#customCut = "((eleHasL1&&!posHasL1)||(!eleHasL1&&posHasL1))&&uncVZ>({0}+{1}*uncM+{2}*uncM^2+{3}*uncM^3+{4}*uncM^4+{5}*uncM^5)".format(-133,8211,-162000,1480000,-6406000,10560000)

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'lfgivwxydtqrsj:k:m:n:o:p:u:a:b:e:c:z:h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-l':
            cut=loosevertCut
        if opt=='-f':
            cut=loosevertCutL1L1  
        if opt=='-g':
            cut=loosevertCutL1L2  
        if opt=='-i':
            cut=loosevertCutL2L2          
        if opt=='-v':
            cut=vertCut
        if opt=='-w':
            cut=vertCutL1L1
        if opt=='-x':
            cut=vertCutL1L2
        if opt=='-y':
            cut=vertCutL2L2
	if opt=='-t':
            cut=tightCut
	if opt=='-q':
            cut=isoCutL1L1
	if opt=='-r':
            cut=isoCutL1L2
	if opt=='-s':
            cut=isoCutL2L2
	if opt=='-d':
            cut=customCut
	if opt=='-j':
            uncVX=float(arg)
	if opt=='-k':
            uncVXSig=float(arg)
	if opt=='-m':
            uncVY=float(arg)
	if opt=='-n':
            uncVYSig=float(arg)
	if opt=='-o':
            uncTargProjX=float(arg)
	if opt=='-p':
            uncTargProjXSig=float(arg)
	if opt=='-a':
            uncTargProjY=float(arg)
	if opt=='-b':
            uncTargProjYSig=float(arg)
        if opt=='-e':
            ebeam=float(arg)
        if opt=='-c':
            clusterT=float(arg)
        if opt=='-z':
            targetZ=float(arg)
        if opt=='-h':
            print_usage()
            sys.exit(0)

print remainder[0]
#treeFile = TFile(sys.argv[1],"RECREATE")
#tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print remainder[1:]
chain = TChain("ntuple")
for i in remainder[1:]:
	chain.Add(i,0)
print chain.GetEntries()
outFile = TFile(remainder[0],"RECREATE")
#events = chain.CopyTree(cut.format(ebeam,clusterT,targetZ))
events = chain.CopyTree(cut.format(ebeam,clusterT,targetZ,uncVX,uncVXSig,uncVY,uncVYSig,uncTargProjX,uncTargProjXSig,uncTargProjY,uncTargProjYSig))
print events.GetEntries()
#outFile = TFile(remainder[0],"RECREATE")
#events.Write()
events.Write("ntuple",TTree.kOverwrite)
gDirectory.ls()
