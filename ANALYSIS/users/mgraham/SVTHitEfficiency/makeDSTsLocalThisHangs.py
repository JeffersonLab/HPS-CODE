import sys
import os
import string
import glob
import re
import subprocess
from threading import Timer

justDoOne=False

skimdir="MCV0Skims"
dstdir="MCV0DSTs"
prefix="tritrig-beam_2500kBunches_pass4_v4_5_0_svt_efficiency_allow_missed_sensor_"
#prefix="wab-beam_2500kBunches_pass4_v4_5_0_svt_efficiency_allow_missed_sensor_"
#midfix="5sigma_weighted_ratios_scalekilling_First3pt0_Second2pt0_NoV0Skim"
midfix="5sigma_weighted_ratios_scalekilling_First3pt0_Second2pt0"

dstmaker="/group/hps/hps_soft/hps-dst/build/bin/dst_maker"

#fileListTot=glob.glob(skimdir+"/"+prefix+midfix+"*.slcio"
fileListTot=glob.glob(skimdir+"/"+prefix+midfix+"_[0-9]*.slcio")
print(fileListTot)

kill = lambda process: process.kill()
for infile in fileListTot: 
    base=os.path.basename(infile)
#    base=os.path.splitext(base)[0]+".root"
    base=os.path.splitext(base)[0]+"_Redo.root"
    outfile=dstdir+"/"+base
    print(outfile)
    if os.path.isfile(outfile):
        print(outfile+" already exists...skipping")
        continue
#    cmd=dstmaker+" -o "+outfile+" " +infile
    cmd=dstmaker
    arg1="-o "+outfile
    arg2=infile
    print(cmd+ "  " +arg1+ " "+arg2)
#    os.system(cmd)
#    process = subprocess.call([cmd,arg1,arg2],timeout=300, shell=False)
#    proc = subprocess.Popen([cmd,arg1,arg2],stderr=errFile, stdout=outFile,universal_newlines=False,shell=False)
    proc = subprocess.Popen([cmd,arg1,arg2],stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False)
    my_timer = Timer(400,kill,[proc])
    try: 
        my_timer.start()
        stdout,stderr=proc.communicate()
        print("still running")
    finally: 
        my_timer.cancel()
    if justDoOne:
        break
