import sys
import shutil
import re
import string
import os
import glob
from subprocess import Popen, PIPE
import csv


tempxml="tarredDST_template.xml"
prodxml="tarredDST_prod.xml"

patRUN="^(.*)REPLACERUNVALUE(.*)"
patFILE="^(.*)REPLACEFILENUM(.*)"
patPOST="^(.*)REPLACEPOSTFIX(.*)"

radCut="" #don't cut in radiative region
#radCut="-r True"
energy="-e 2.3"
weigh=""  #don't do track efficiency weighting
#weigh="-w True"


#runList=['8099']
runList=[]
with open('HPS_Runs_2016-golder-runs.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
#        print(row)
#        print(row[0])
#        print(row[0],row[1],row[2],)
        if row[0].isdigit() :
            runList.append(row[0])

#print(runList)
runList=['7963']
fileList=['1']
data_dir='/volatile/hallb/hps/mgraham/physicsrun2016/dst'
postfix='pass4_reqL1'
for run in runList:
    for file in fileList:
        outFile=open(prodxml,"w")
        with open(tempxml,"r") as tmp:
            lines = tmp.readlines()
            for line in lines:        
                matchRUN=re.search(patRUN,line)
                matchFILE=re.search(patFILE,line)
                matchPOST=re.search(patPOST,line)
                if matchRUN!=None :
                    print line.rstrip()
                    outFile.write(matchRUN.group(1)+run+matchRUN.group(2)+"\n");
                elif matchFILE!=None: 
                    print line.rstrip()
                    outFile.write(matchFILE.group(1)+file+matchFILE.group(2)+"\n");
                elif matchPOST!=None: 
                    print line.rstrip()
                    outFile.write(matchPOST.group(1)+postfix+matchPOST.group(2)+"\n");
                else : 
                    outFile.write(line)

        #        os.system('rm '+logfile)
        outFile.close()
        cmd='jsub -xml '+prodxml
        print cmd
        os.system(cmd)
