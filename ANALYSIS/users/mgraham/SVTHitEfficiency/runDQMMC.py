import sys
import os
import string
import glob
import re
import subprocess


nfilesPerJob=100
remakeProd=True
justDoOne=False
tempxml="dqmMC_template.xml"

prodxmlPre="MCXMLDIR/DQMV0_prod"

patINPUT="^(.*)REPLACEINPUT(.*)FOOBAR(.*)"
patMCTYPE="^(.*)REPLACEMCTYPE(.*)"
patPOST="^(.*)REPLACEPOSTFIX(.*)"
patCOMM="^(.*)REPLACECOMMAND(.*)"


outMCDir="SVTEfficiencyData/"
jarfile="/w/hallb-scifs17exp/general/hps/mgraham/hps-java/distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar"
outLogDir = "."
#steering="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTHitPlots.lcsim"
#steering="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTHitPlotsWithSVTClusterKilling.lcsim"
steering="/w/hallb-scifs17exp/general/hps/mgraham/hps-java/steering-files/src/main/resources/org/hps/steering/production/DataQualityRecon.lcsim"

#mctypeList=["RAD","RAD-beam_2500kBunches","tritrig-beam_2500kBunches"]
mctypeList=["tritrig-beam_2500kBunches"]
#mctypeList=["RAD","RAD-beam_2500kBunches","wab-beam_2500kBunches","tritrig-beam_2500kBunches"]
#mctypeList=["RAD-beam_2500kBunches","wab-beam_2500kBunches"]
##############  unskimmed nominal recon data
mcdir="/mss/hallb/hps/production/PhysicsRun2016/pass4/npt224npt08n4pt3_npt33/recon"
mcmidfix="2pt3/PhysRun2016-Pass2/v4_5_0"
mcinpostfix=""
mcpostfix='pass4_v4_5_0'

#############  skimmed/killed data
#mcdir="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/MCV0Skims"
#mcmidfix=""
#mcinpostfix='pass4_v4_5_0_svt_efficiency_allow_missed_sensor_5sigma_weighted_ratios'
#mcpostfix='pass4_v4_5_0_svt_efficiency_allow_missed_sensor_5sigma_weighted_ratios_dqm'

cmdpre='java -DdisableSvtAlignmentConstants -jar  '+str(jarfile)+' '+str(steering)
cmdpost='  -n 10000000 '+'  -DoutputFile='


for mctype in mctypeList :
    instring=mcdir+"/"+mctype+"/"+mcmidfix+"/"+mcinpostfix+"*.slcio"
#    instring=mcdir+"/"+mctype+"*"+mcinpostfix+"_[0-9]*.slcio"
    #    print(mcdir+"/"+mctype+"/"+mcmidfix+"/"+mcinpostfix+"*.slcio")
    print(instring)
    fcnt=0
    #    fileListTot=glob.glob(mcdir+"/"+mctype+"/"+mcmidfix+"/"+mcinpostfix+"*.slcio")
    fileListTot=glob.glob(instring)
    print("Total Files in List = "+str(len(fileListTot)))
    doAnotherJob=True
    while doAnotherJob: 
        prodxml=prodxmlPre+"_"+mctype+"_"+mcpostfix+"_"+str(fcnt)+".xml"
#        lastFileNum=(fcnt+1)*nfilesPerJob-1
        lastFileNum=(fcnt+1)*nfilesPerJob
        print("Last Index is :  "+str(lastFileNum))
        if lastFileNum>len(fileListTot)-1: 
            lastFileNum=len(fileListTot)
            doAnotherJob=False
        fileList=fileListTot[fcnt*nfilesPerJob:lastFileNum]
        print("Running over index "+str(fcnt*nfilesPerJob)+" to "+str(lastFileNum))
        print(len(fileList))
        nfiles=len(fileList)
        inputString=""
        for n in range(0,nfiles):
            print(" -i out_"+str(n)+".slcio")
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
#                            outFile.write(matchINPUT.group(1)+"mss:"+infile+matchINPUT.group(2)+"out_"+str(cnt)+".slcio"+matchINPUT.group(3)+"\n");
                            print(matchINPUT.group(1)+"file:"+infile+matchINPUT.group(2)+"out_"+str(cnt)+".slcio"+matchINPUT.group(3)+"\n")
                            outFile.write(matchINPUT.group(1)+"file:"+infile+matchINPUT.group(2)+"out_"+str(cnt)+".slcio"+matchINPUT.group(3)+"\n");
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

