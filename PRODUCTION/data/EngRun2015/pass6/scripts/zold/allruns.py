#!/usr/bin/env python
import sys,shutil,re,string,os,time,subprocess
from runjob import runjob

if len(sys.argv)<3:
    sys.exit('Usage:  alruns.py firstRun lastRun')

firstRun = int(sys.argv[1])
finalRun = int(sys.argv[2])

detector='HPS-EngRun2015-Nominal-v1'

#uncomment these for reconstruction
xmlfile="templates/recon/reconDstAndDqm.xml"
runtype="recon"

#uncomment these for dqm
#xmlfile="templates/dqm/dqmFull.xml"
#runtype="dqm"

#uncomment these for dsts
#xmlfile="templates/dst/dstFull.xml"
#runtype="dst"

subprocess.call('/u/group/hps/production/data/EngRun2015/scripts/generateLists.sh pass1 >& /dev/null',shell=True)

runNumber=firstRun

while runNumber<=finalRun :
    
    #detector = getDetector(runNumber)
    #if detector != "FOOBAR":
        #runjob(xmlfile,runtype,runNumber,detector)
        #cmd ='python ./scripts/runjob.py ' +xmlfile +' '+runtype+' '+str(runNumber)+' '+detector
        #subprocess.call(cmd,shell=True)
        #sys.stdout.flush()
    #else:
    #    print 'detector not defined for run number '+str(runNumber)

    runjob(xmlfile,runtype,runNumber,detector)
    runNumber=runNumber+1
    time.sleep(0.1)

print "Done with allruns.py"



