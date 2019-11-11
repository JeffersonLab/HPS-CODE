import sys
import shutil
import re
import string
import os
import glob
from subprocess import Popen, PIPE

nFilesToConcat=5
reconDir='/nfs/slac/g/hps3/data/mc_production/wab-beam-tri/1pt05/recon/'
outDir='/nfs/slac/g/hps3/data/engrun2015/tweakpass7/mc/dst/wab-beam-tri-slac'

recoFiles=glob.glob(reconDir+'*.slcio')

dstMaker='/nfs/slac/g/hps3/software/hps-dst/bin/dst_maker'
print 'number of recon files = '+str(len(recoFiles))

dstNum=0
#for n in range(0,len(recoFiles)): 
n=0
while n < len(recoFiles): 
    inString=''
    for k in range(0,nFilesToConcat):
        inString=inString+' '+recoFiles[n]
        n+=1
    print n
    print inString
    outFile=outDir+'/wab-beam-tri_SLAC_HPS-EngRun2015-Nominal-v5-0_'+str(dstNum)+'.root'
    cmd=dstMaker+' -o '+str(outFile)+' '+inString
    print cmd
    os.system(cmd)    
    dstNum=dstNum+1
