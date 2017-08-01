import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

####
if len(sys.argv) != 2:  #remember, the script name counts as an argument!
    print 'countEvents.py <run number>'
    print '<runnumber>  can be a number or all' 
    sys.exit()
####

#inDir="data_quality/pass0/recon/"
#pattern="^Read\s(\d+)"
#postfix=".txt"
inDir="/mss/hallb/hps/engrun/pass0/recon/"
pattern="^size=(\d+)"
postfix=".slcio"

diveser=1000*1000*1000.0
type="_recon_"
label="20141225"
maxFiles=50


run=sys.argv[1]
if run == "all" : 
    startRun=3183
    endRun=3460
else:
    startRun=int(run)
    endRun=int(run)

#parse the xml template
eventCount=0
runCnt=startRun
while runCnt<= endRun:
    fileCnt=0
    while fileCnt<maxFiles:        
        filename=inDir+"hps_00"+str(runCnt)+"."+str(fileCnt)+type+label+postfix
        if os.path.isfile(filename) :
            print "Opening "+filename
            with open(filename,"r") as tmp:
                lines = tmp.readlines()
            for line in lines:
                matchMe=re.search(pattern,line)
                if matchMe!=None :
                    eventCount+=int(matchMe.group(1))                    
                    print int(matchMe.group(1))/diveser
        fileCnt+=1
    runCnt+=1

print eventCount/diveser
