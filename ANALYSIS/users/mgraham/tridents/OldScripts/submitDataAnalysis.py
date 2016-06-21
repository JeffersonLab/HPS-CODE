import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_TestWABs'
#analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_2Tracks'
#analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_MoreThan2Tracks_HighESum'
#mc_dir='mc/tritrig/dst/'
runList=['5772']
data_dir='/nfs/slac/g/hps3/data/engrun2015/pass4/dst/'
pulser_dir='/nfs/slac/g/hps3/data/engrun2015/pass4/skim/dst/pulser'
data_prefix='hps_00'
data_postfix='.root'
doMC = False
analysis='tridentAnalysis_pass4.py'
analysisPulser='pulserAnalysis_pass4.py'
anapre='tridents_'

for run in runList:
    logfile='logs/'+anapre+data_prefix+run+'_'+analysis_postfix+'.log'
    os.system('rm '+logfile)
    outfile='OutputHistograms/Data/'+data_prefix+run+'_'+analysis_postfix+'.root'
    dstfile=data_dir+'/'+data_prefix+run #TChain will glob onto this
#    dstfile=data_dir+'/'+data_prefix+run+'.4' #TChain will glob onto this
    print dstfile
    cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -o '+outfile+' '+dstfile
    print cmd
#    os.system(cmd)
    #run over pulser data too...
    logfilePulser='logs/'+anapre+data_prefix+run+'_pulser_'+analysis_postfix+'.log'
    os.system('rm '+logfilePulser)
    outfilePulser='OutputHistograms/Data/'+data_prefix+run+'_pulser_'+analysis_postfix+'.root'
    dstfilePulser=pulser_dir+'/'+data_prefix+'5772' #TChain will glob onto this
#    dstfilePulser=data_dir+'/'+data_prefix+'5772.4' #TChain will glob onto this
    print dstfile
    cmd='bsub -q long -W 5000 -o '+logfilePulser+' python '+analysisPulser+' -o '+outfilePulser+' '+dstfilePulser
    os.system(cmd)


mcTypeList=['RAD','BH','tritrig-beam-tri','beam-tri']
mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass4/mc/dst'
mc_prefix='HPS-EngRun2015-Nominal-v3-4'
mc_postfix='.root'
if doMC is True : 
    for mcType in mcTypeList:
        logfile='logs/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/MC/'+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
        dstfile=mc_dir+'/'+mcType+'/'+'*'+mc_prefix #TChain will glob onto this
        print dstfile
        cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -m True -o '+outfile+' '+dstfile
        print cmd
        os.system(cmd)
