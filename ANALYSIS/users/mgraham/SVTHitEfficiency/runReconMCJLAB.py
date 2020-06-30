import sys
import os
import string
import glob
import re
import subprocess


nfilesPerJob=100
#justDoOne=False
justDoOne=True
remakeProd=True

tempxml="recoMC_template.xml"

prodxmlPre="MCRecoXMLDIR/MCV0_reco"

patINPUT="^(.*)REPLACEINPUT(.*)FOOBAR(.*)"
patMCTYPE="^(.*)REPLACEMCTYPE(.*)"
patPOST="^(.*)REPLACEPOSTFIX(.*)"
patCOMM="^(.*)REPLACECOMMAND(.*)"



jarfile="/w/hallb-scifs17exp/general/hps/mgraham/hps-java/distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar"
outLogDir = "."
#steering="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTHitPlots.lcsim"
#steering="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/PhysicsRun2016FullReconMCSVTHitKillerV0Skim.lcsim"
steering="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/PhysicsRun2016FullReconMCSVTHitKiller.lcsim"

#mctypeList=["RAD","RAD-beam_2500kBunches","tritrig-beam_2500kBunches"]
mctypeList=["tritrig-beam_2500kBunches"]
#mctypeList=["RAD-beam_2500kBunches","wab-beam_2500kBunches"]
#mctypeList=["RAD-beam_2500kBunches","wab-beam_2500kBunches"]
mcdir="/mss/hallb/hps/production/PhysicsRun2016/pass4/npt224npt08n4pt3_npt33/recon"
mcmidfix="2pt3/PhysRun2016-Pass2/v4_5_0"
mcpostfix='pass4_v4_5_0_svt_efficiency_allow_missed_sensor_5sigma_weighted_ratios_scalekilling_First3pt0_Second2pt0_NoV0Skim'

cmdpre='/usr/bin/java -XX:+UseSerialGC -Xmx4G -DdisableSvtAlignmentConstants -jar  '+str(jarfile)+' '+str(steering)
cmdpost='  -n 10000000 '+'  -DoutputFile='

for mctype in mctypeList :
    print(mcdir+"/"+mctype+"/"+mcmidfix+"/*.slcio")
    fcnt=0
    fileListTot=glob.glob(mcdir+"/"+mctype+"/"+mcmidfix+"/"+"*.slcio")
    doAnotherJob=True
    while doAnotherJob: 
        prodxml=prodxmlPre+"_"+mctype+"_"+mcpostfix+"_"+str(fcnt)+".xml"
        lastFileNum=(fcnt+1)*nfilesPerJob-1
        if lastFileNum>=len(fileListTot)-1: 
            lastFileNum=len(fileListTot)-1
            doAnotherJob=False
        fileList=fileListTot[fcnt*nfilesPerJob:lastFileNum]
        print(len(fileList))
        nfiles=len(fileList)
        inputString=""
        for n in range(0,nfiles):
            inputString+=" -i out_"+str(n)+".slcio"
        postfix=mcpostfix+"_"+str(fcnt)
#        javacmd=cmdpre+inputString+cmdpost+outDataDir+datamidfix+postfix+".root"
        javacmd=cmdpre+inputString+cmdpost+"out"
        if remakeProd: 
            outFile=open(prodxml,"w")
            cnt=0
            with open(tempxml,"r") as tmp:
                lines = tmp.readlines()
                for line in lines:        
                    matchINPUT=re.search(patINPUT,line)
                    matchPOST=re.search(patPOST,line)
                    matchMCTYPE=re.search(patMCTYPE,line)
                    matchCOMM=re.search(patCOMM,line)
                    if matchMCTYPE!=None :
                        print line.rstrip()
                        outFile.write(matchMCTYPE.group(1)+mctype+matchMCTYPE.group(2)+"\n");
                    elif matchPOST!=None: 
                        print line.rstrip()
                        outFile.write(matchPOST.group(1)+postfix+matchPOST.group(2)+"\n");
                    elif matchINPUT!=None: 
                        print line.rstrip()
                        for infile in fileList: 
                            outFile.write(matchINPUT.group(1)+"mss:"+infile+matchINPUT.group(2)+"out_"+str(cnt)+".slcio"+matchINPUT.group(3)+"\n");
                            cnt+=1
                    elif matchCOMM!=None: 
                        print line.rstrip()
                        outFile.write(javacmd)
                    else : 
                        outFile.write(line)
        if remakeProd:
            outFile.close()
        cmd='jsub -xml '+prodxml
        print cmd
        os.system(cmd )
        fcnt+=1
        if justDoOne: 
            break
