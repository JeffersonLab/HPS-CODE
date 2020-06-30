import sys
import os
import string
import glob
import re
import subprocess


remakeProd=True
justDoOne=True
tempxml="dqmData_template.xml"

prodxmlPre="DATAXMLDIR/DQMV0_prod"

patINPUT="^(.*)REPLACEINPUT(.*)FOOBAR(.*)"
patRUN="^(.*)REPLACERUNVALUE(.*)"
patPOST="^(.*)REPLACEPOSTFIX(.*)"
patCOMM="^(.*)REPLACECOMMAND(.*)"


label="svt-efficiency-allow-missed-sensor"
jarfile="/w/hallb-scifs17exp/general/hps/mgraham/hps-java/distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar"
outLogDir = "."
#steering="/w/hallb-scifs17exp/general/hps/mgraham/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTHitPlots.lcsim"
steering="/w/hallb-scifs17exp/general/hps/mgraham/hps-java/steering-files/src/main/resources/org/hps/steering/production/DataQualityRecon.lcsim"
datadir="/w/hallb-scifs17exp/general/hps/mgraham/physicsrun2019/v0/work/hallb/hps/data/physrun2016/pass4/skim/v0"
datamidfix="hps_00"
datapostfix='pass4_v4_5_0_dqm'


cmdpre='java -jar  '+str(jarfile)+' '+str(steering)
cmdpost='  -n 10000000 '+'  -DoutputFile='
runList=['7963']

nfilesPerJob=10

for run in runList:
    fcnt=0
    fileListTot=glob.glob(datadir+"/"+datamidfix+run+"*.slcio")
    doAnotherJob=True
    while doAnotherJob: 
        prodxml=prodxmlPre+"_"+run+"_"+datapostfix+"_"+str(fcnt)+".xml"
        lastFileNum=(fcnt+1)*nfilesPerJob-1
        if lastFileNum>=len(fileListTot)-1: 
            lastFileNum=len(fileListTot)-1
            doAnotherJob=False
        fileList=fileListTot[fcnt*nfilesPerJob:lastFileNum]
        print(len(fileList))
        nfiles=len(fileList)
        inputString=""
        for n in range(0,nfiles-1):
            inputString+=" -i out_"+str(n)+".slcio"
        postfix=datapostfix+"_"+str(fcnt)
        javacmd=cmdpre+inputString+cmdpost+"out"
        if remakeProd: 
            outFile=open(prodxml,"w")
            cnt=0
            with open(tempxml,"r") as tmp:
                lines = tmp.readlines()
                for line in lines:        
                    matchINPUT=re.search(patINPUT,line)
                    matchPOST=re.search(patPOST,line)
                    matchRUN=re.search(patRUN,line)
                    matchCOMM=re.search(patCOMM,line)
                    if matchRUN!=None :
                        print line.rstrip()
                        outFile.write(matchRUN.group(1)+run+matchRUN.group(2)+"\n");
                    elif matchPOST!=None: 
                        print line.rstrip()
                        outFile.write(matchPOST.group(1)+postfix+matchPOST.group(2)+"\n");
                    elif matchINPUT!=None: 
                        print line.rstrip()
                        for infile in fileList: 
                            outFile.write(matchINPUT.group(1)+infile+matchINPUT.group(2)+"out_"+str(cnt)+".slcio"+matchINPUT.group(3)+"\n");
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

