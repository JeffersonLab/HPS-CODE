import sys
import os
import string
import glob
import re
import subprocess
run=8099
doMC = True
doData = False

label="svt-efficiency-allow-missed-sensor"
outDataDir="SVTEfficiencyData/"
jarfile="./hps-distribution-4.4-svt-hit-killer-weighted-ratios-L6-0pt05mm.jar"
outLogDir = "SVTEfficiencyLogs/"
steering="/nfs/slac/g/hps/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTHitPlots.lcsim"
if doData:
    data_prefix='hps_00'
    indir="pass4-v0-skims"
    instart=indir+"/"+str(run)+"/"+data_prefix+"*"
    foobar=glob.glob(instart)
    for infile in foobar: 
        print(infile)
        part=re.search('\.(\d*)\_',infile).group(1)
        outfile=outDataDir+data_prefix+str(run)+"."+str(part)+"-"+label
        print(outfile)
        logfile=outLogDir+data_prefix+str(run)+"."+str(part)+"-"+label+".log"
        print(logfile)
        os.system("rm "+logfile)
        cmd='bsub -R "rhel60" -W 5000 -o '+logfile+' java -jar  '+str(jarfile)+' '+str(steering)+' -i '+str(infile)+'  -n 10000000 '+'  -DoutputFile='+str(outfile)
        print (cmd)
        os.system(cmd)


if doMC:
    
    label="cluster-killing-weighted-ratios-L6-0pt1mm"
    jarfile="./hps-distribution-4.4-svt-hit-killer-weighted-ratios-L6-0pt1mm.jar"
    steering="/nfs/slac/g/hps/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/PhysicsRun2016FullReconMC.lcsim"

    mcTypeList=['tritrig-WB','wabtrig-BT','WBT']
#    mcTypeList=['tritrig-WB']
    mc_dir='/nfs/slac/g/hps/mgraham/hpsrun2016/mc/pass4_4.3.1'
    mc_prefix='HPS-PhysicsRun2016-Pass2'

    for mcType in mcTypeList:
        instart=mc_dir+"/"+mcType+"/recon/*"+mc_prefix+"*.slcio"
        foobar=glob.glob(instart)        
        maxfiles=50
        incnt=0    
        jobcnt=0
        while incnt<len(foobar): 
            infile=""
            fcnt=0
            while fcnt<maxfiles and incnt<len(foobar): 
                infile=infile +" -i "+str(foobar[incnt])
                fcnt+=1
                incnt+=1
            jobcnt+=1
            logfile=outLogDir+mcType+'_'+mc_prefix+"-"+label+"-"+str(jobcnt)+".log"
            os.system("rm "+logfile)
            outfile=outDataDir+"/"+mcType+"/recon/"+mcType+"-"+mc_prefix+"-"+label+str(jobcnt)
#        print(outfile)
            cmd='bsub -R "rhel60" -W 5000 -o '+logfile+' java -DdisableSvtAlignmentConstants -jar  '+str(jarfile)+' '+str(steering)+str(infile)+'  -n 10000000 '+'  -DoutputFile='+str(outfile)
#            cmd='bsub -R "rhel60" -W 5000 -o '+logfile+' java -jar  '+str(jarfile)+' '+str(steering)+str(infile)+'  -n 10000000 '+'  -DoutputFile='+str(outfile)
            print (cmd)
#            subprocess.call(cmd)
            os.system(cmd)
