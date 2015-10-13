import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE


analysis_postfix='10022015_BeamEle0pt8_ECal_GBL_v0Mom_slopeGT0pt2' 
#mc_dir='mc/tritrig/dst/'
runList=['5772']
data_dir='/nfs/slac/g/hps3/data/engrun2015/pass2/dst/v0.8.1_v3-1.3/'
data_prefix='hps_00'
data_postfix='.root'



for run in runList:
    logfile='logs/'+data_prefix+run+'_'+analysis_postfix+'.log'
    os.system('rm '+logfile)
    outfile='OutputHistograms/Data/'+data_prefix+run+'_'+analysis_postfix+'.root'
    dstfile=data_dir+'/'+data_prefix+run #TChain will glob onto this
    print dstfile
    cmd='bsub -q long -W 5000 -o '+logfile+' python tridentAnalysis_pass2.py  -o '+outfile+' '+dstfile
    print cmd
    os.system(cmd)


