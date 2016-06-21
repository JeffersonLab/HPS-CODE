import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

#analysis_postfix='pass3_matchECal'
analysis_postfix='pass4_IsoCut_1pt0_v0chi2_10_useGBL_ECalMatch'
#analysis_postfix='pass4_killTracks'
#mc_dir='mc/tritrig/dst/'
#mcTypeList=['Rad','BH','tritrig-beam-tri','tritrig']
#mcTypeList=['RAD','BH','tritrig-beam-tri']
mcTypeList=['tritrig-beam-tri']
#mcTypeList=['Rad']
mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass4/mc/dst'
#mc_prefix='HPS-EngRun2015-Nominal-v3-1-fieldmap_3.4.1'
mc_prefix='HPS-EngRun2015-Nominal-v3-4'
mc_postfix='.root'

analysis='vertexAnalysis_pass4.py'
anapre='vertexing' 
for mcType in mcTypeList:
    logfile='logs/'+anapre+'_'+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
    os.system('rm '+logfile)
    outfile='VertexHistograms/MC/'+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
    dstfile=mc_dir+'/'+mcType+'/'+'*'+mc_prefix #TChain will glob onto this
    print dstfile
    cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -m True -o '+outfile+' '+dstfile
    print cmd
    os.system(cmd)
