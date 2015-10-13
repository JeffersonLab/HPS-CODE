import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

analysis_postfix='10022015_BeamEle0pt8_ECal_GBL_v0Mom_slopeGT0pt2' 
#mc_dir='mc/tritrig/dst/'
mcTypeList=['Rad','BH','tritrig-beam-tri','tritrig']
#mcTypeList=['Rad']
mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass2/mc/dst'
#mc_prefix='tritrigv1_FIXEDFILTERING_10to1_HPS-EngRun2015-Nominal-v1_3.4.0-20150805_pairs1_'
mc_prefix='HPS-EngRun2015-Nominal-v3'
mc_postfix='.root'

for mcType in mcTypeList:
    logfile='logs/'+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
    os.system('rm '+logfile)
    outfile='OutputHistograms/MC/'+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
    dstfile=mc_dir+'/'+mcType+'/'+'*'+mc_prefix #TChain will glob onto this
    print dstfile
    cmd='bsub -q short -o '+logfile+' python tridentAnalysis_pass2.py -m True -o '+outfile+' '+dstfile
    print cmd
    os.system(cmd)
