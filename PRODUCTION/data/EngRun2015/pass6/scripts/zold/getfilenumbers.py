#!/usr/bin/env python
import re

UNBLINDEDRUNS=[5222,5228,5229,5393,5546,5747,5749,5754,5755,
               5756,5757,5774,5777,5779,5781,5784,5785,5786]

def getfilenumbers(PASS,RUN):

    blind = not int(RUN) in UNBLINDEDRUNS

    listdir='/u/group/hps/production/data/EngRun2015/lists'
    
    with open(listdir+'/tape.txt','r') as tmp:
        mssraw=tmp.readlines()
    
    with open(listdir+'/tape_'+PASS+'.txt','r') as tmp:
        msspass=tmp.readlines()
    
    with open(listdir+'/disk_'+PASS+'.txt','r') as tmp:
        diskpass=tmp.readlines()
   
    space=''
    filenos=''

    for file1 in mssraw:
     
        if file1.find(RUN)<0: continue

        mm1 = re.search('_(\d\d\d\d\d\d).evio.(\d+)',file1)
        
        if mm1 == None: continue

        runno1 = mm1.group(1)
        filno1 = mm1.group(2)

        if int(runno1) != int(RUN): continue;
        
        if blind and int(filno1)%10!=0: continue

        missing=1
        for file2 in msspass:
            mm2 = re.search('_(\d\d\d\d\d\d).(\d+)',file2)
            if mm2 == None: continue
            runno2 = mm2.group(1)
            filno2 = mm2.group(2)
            if runno1==runno2 and filno1==filno2:
                missing=0
                break

        if missing:
            filenos += space+filno1
            space=' '

    return filenos
        
