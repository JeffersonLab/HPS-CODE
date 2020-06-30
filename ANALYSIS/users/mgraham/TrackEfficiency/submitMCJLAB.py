import sys
import shutil
import re
import string
import os
import glob
from subprocess import Popen, PIPE
import csv


remakeProd=True
justDoOne=False;
tempxml="MCDST_template.xml"

prodxmlPre="MCXMLDIR/MCDST_prod"

patINPUT="^(.*)REPLACEINPUT(.*)FOOBAR(.*)"
patPOST="^(.*)REPLACEPOSTFIX(.*)"
patMCTYPE="^(.*)REPLACEMCTYPE(.*)"

#mctypeList=["RAD","RAD-beam_2500kBunches","tritrig-beam_2500kBunches"]
mctypeList=["tritrig-beam_2500kBunches"]
#mctypeList=["RAD","RAD-beam_2500kBunches","wab-beam_2500kBunches","tritrig-beam_2500kBunches"]
#mctypeList=["RAD-beam_2500kBunches","wab-beam_2500kBunches"]
mcdir="/mss/hallb/hps/production/PhysicsRun2016/pass4/npt224npt08n4pt3_npt33/dst"
mcmidfix="2pt3/PhysRun2016-Pass2/v4_5_0"
mcpostfix='pass4_killInSlope_reqL6'

nfilesPerJob=100

for mctype in mctypeList :
    print(mcdir+"/"+mctype+"/"+mcmidfix+"/*.root")
    fcnt=0
    fileListTot=glob.glob(mcdir+"/"+mctype+"/"+mcmidfix+"/*.root")
    doAnotherJob=True
    while doAnotherJob: 
        prodxml=prodxmlPre+"_"+mctype+"_"+mcpostfix+"_"+str(fcnt)+".xml"
        lastFileNum=(fcnt+1)*nfilesPerJob-1
        if lastFileNum>=len(fileListTot)-1: 
            lastFileNum=len(fileListTot)-1
            doAnotherJob=False
        fileList=fileListTot[fcnt*nfilesPerJob:lastFileNum]
        print(len(fileList))
        postfix=mcpostfix+"-"+str(fcnt)
        if remakeProd: 
            outFile=open(prodxml,"w")
            cnt=0
            with open(tempxml,"r") as tmp:
                lines = tmp.readlines()
                for line in lines:        
                    matchINPUT=re.search(patINPUT,line)
                    matchPOST=re.search(patPOST,line)
                    matchMCTYPE=re.search(patMCTYPE,line)
                    if matchMCTYPE!=None :
                        print line.rstrip()
                        outFile.write(matchMCTYPE.group(1)+mctype+matchMCTYPE.group(2)+"\n");
                    elif matchINPUT!=None: 
                        print line.rstrip()
                        for infile in fileList: 
                            outFile.write(matchINPUT.group(1)+"mss:"+infile+matchINPUT.group(2)+"${mctype}_"+str(cnt)+".root"+matchINPUT.group(3)+"\n");
                            cnt+=1
                    elif matchPOST!=None: 
                        print line.rstrip()
                        outFile.write(matchPOST.group(1)+postfix+matchPOST.group(2)+"\n");
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

