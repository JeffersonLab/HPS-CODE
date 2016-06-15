import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

#analysis_postfix='pass3_matchECal' 
#analysis_postfix='pass4_useGBL' 
#analysis_postfix='pass4_noIsoCut_v0chi2_10_useGBL' 
analysis_postfix='pass4_IsoCut_1pt0_v0chi2_10_useGBL_ECalMatch'
#mc_dir='mc/tritrig/dst/'
runList=['5772']
data_dir='/nfs/slac/g/hps3/data/engrun2015/pass4/dst/'
data_prefix='hps_00'
data_postfix='.root'

analysis='vertexAnalysis_pass4.py'
anapre='vertexing_'

for run in runList:
    logfile='logs/'+anapre+data_prefix+run+'_'+analysis_postfix+'.log'
    os.system('rm '+logfile)
    outfile='VertexHistograms/Data/'+data_prefix+run+'_'+analysis_postfix+'.root'
    dstfile=data_dir+'/'+data_prefix+run #TChain will glob onto this
    print dstfile
    cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -o '+outfile+' '+dstfile
    print cmd
    os.system(cmd)


