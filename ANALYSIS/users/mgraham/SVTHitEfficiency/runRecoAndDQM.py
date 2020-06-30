import sys
import os
import string
import glob

#jarfile="iss-421-dqm/distribution/target/hps-distribution-4.3-SNAPSHOT-bin.jar"

#detector='HPS-PhysicsRun2016-Pass2'
#outDataDir="Iss410Data/"
#outfile = "ap-80-ctau10mm-"+label
#log = "Iss410Logs/"+outfile+".log"
#instart="Data/PhysRun2016/recon/ap/80/*.slcio"
#steering="iss-410/steering-files/src/main/resources/org/hps/steering/recon/PhysicsRun2016FullReconMC.lcsim"


run=10548
subrun='00666'
#dir="iss-617"
#dir="iss-583"
dir="iss-549"
#dir="Run2019Master"
label=dir+"-dqm"
jarfile=dir+"/distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar"
detector='HPS-PhysicsRun2019-v1-4pt5'
outDataDir="DQM2019/"
outfile = "hps_0"+str(run)+"."+str(subrun)+"-"+label
instart="Data/PhysicsRun2019/evio/hps_010030.evio."+str(subrun)+"*"
log = "DQM2019/"+outfile+".log"
#steering=dir+"/steering-files/src/main/resources/org/hps/steering/production/Run2019ReconPlusDataQuality.lcsim"
steering=dir+"/steering-files/src/main/resources/org/hps/steering/recon/PhysicsRun2019FullRecon.lcsim"

#label="Run2016Master-dqm"
#subrun='122'
#run=7799
#detector='HPS-PhysicsRun2016-Pass2'
#outDataDir="DQM2016/"
#outfile = "hps_007799."+str(subrun)+"-"+label
#instart="Data/PhysRun2016/evio/hps_007799.evio."+str(subrun)+"*"
#log = "DQM2016/"+outfile+".log"
#steering="hps-java-ALWAYS-HEAD/steering-files/src/main/resources/org/hps/steering/production/Run2016ReconPlusDataQuality.lcsim"
#jarfile="hps-java-ALWAYS-HEAD/distribution/target/hps-distribution-4.4-SNAPSHOT-bin.jar"

foobar=glob.glob(instart)
infile=""
for inf in foobar: 
    infile=infile +" -i "+str(inf)

print(infile)

#this one's for lcio files
#cmd='java -cp '+str(jarfile)+'  org.hps.job.JobManager  '+str(steering)+'  -n 1000000 '+str(infile)+'  -DoutputFile='+str(outDataDir+outfile)+' >& '+str(log)
#this one's for evio 
cmd='java   -cp '+str(jarfile)+ ' org.hps.evio.EvioToLcio   -x '+  str(steering)  +'  -d '+str(detector)+' -n 10000 '+ str(instart)+' -DoutputFile='+str(outDataDir+outfile)+ ' -R '+str(run) +' >& '+ str(log)

#Print (steering)

print (cmd)
os.system(cmd)




