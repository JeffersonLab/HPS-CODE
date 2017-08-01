import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

####
#if len(sys.argv) != 2:  #remember, the script name counts as an argument!
#    print 'parseDQMLog.py <run number>'
#    sys.exit()
####

firstRun = 3183
finalRun = 3461

runNumber=firstRun
outFile=open("dqmout.log","w")
while runNumber<finalRun : 
    dir="/home/hps/hps-work/data/logs/pass0/dqm/"
    pre="hps_00" 
    mid="_dqm_"
    label="20141225"
    runtype='dqm' 
#    run=sys.argv[1]
    run=str(runNumber)
    runNumber+=1 
    #get the jobs
    cmd ='./getfilenumbers.sh ' +runtype +' '+str(run)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    nums=p.stdout.readline()
    if nums == "foobar" : 
        print "Nothing to run for run #"+run
        sys.stdout.flush()        
        continue
        ####
    numsArray=nums.split()
    i = 0 
    while (i<len(numsArray)): 
        ext=numsArray[i]
        i+=1
        fileName=dir+pre+str(run)+"."+ext+mid+label+".out"
        print fileName
        with open(fileName,"r") as tmp:
            lines = tmp.readlines()
            pattern="^(\w+)\s(\w+)\s=\s(\d+.\d+)"
            for line in lines:        
                matchMe=re.search(pattern,line)
                if matchMe!=None :
                    print line.rstrip()
                    outFile.write(run+"  "+ext+"  "+matchMe.group(1)+"  "+matchMe.group(2)+"  "+matchMe.group(3)+"\n")    
                    
outFile.close()


