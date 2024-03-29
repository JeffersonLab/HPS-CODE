import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE


analysis_postfix='useGBL_ECalMatch' 
goodRuns='golden-runs-Feb10-2016.txt'
data_dir='pass4-dst/'
data_prefix='hps_00'
data_postfix='_dst_0151218.205540.root'



with open(goodRuns,"r") as tmp:
    lines = tmp.readlines()

run=[]
charge=[]

for line in lines:
    line=line.strip()
    columns=line.split()
    run.append(columns[0])
    charge.append(columns[1])

    logfile='logs/pass4/'+data_prefix+columns[0]+'_'+analysis_postfix+'.log'
    outfile='OutputHistograms/Data/pass4/'+data_prefix+columns[0]+'_'+analysis_postfix+'.root'
    dstfile=data_dir+data_prefix+columns[0] #TChain will glob onto this
    cmd='bsub -q long -W 5000 -o'+logfile+' python tridentAnalysis_pass4.py -o '+outfile+' '+dstfile
    os.system(cmd)


