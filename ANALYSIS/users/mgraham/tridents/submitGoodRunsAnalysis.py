import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE


analysis_postfix='09252015' 
goodRuns='goodRuns.txt'
data_dir='pass2-dst/'
data_prefix='hps_00'
data_postfix='_dst_R340.root'



with open(goodRuns,"r") as tmp:
    lines = tmp.readlines()

run=[]
charge=[]

for line in lines:
    line=line.strip()
    columns=line.split()
    run.append(columns[0])
    charge.append(columns[1])

    logfile='logs/pass2/'+data_prefix+columns[0]+'_'+analysis_postfix+'.log'
    outfile='OutputHistograms/Data/pass2/'+data_prefix+columns[0]+'_'+analysis_postfix+'.root'
    dstfile=data_dir+data_prefix+columns[0] #TChain will glob onto this
    cmd='bsub -q long -o '+logfile+' python tridentAnalysis_pass2.py -o '+outfile+' '+dstfile
    os.system(cmd)


