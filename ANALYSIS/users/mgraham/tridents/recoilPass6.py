import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

analysis_postfix='pass6_useGBL_ECalMatch_noV0Cuts'
#analysis_postfix='pass6_useGBL_ECalMatch_SuperFiducialCut'
#analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_2Tracks'
#analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_MoreThan2Tracks_HighESum'
#mc_dir='mc/tritrig/dst/'
runList=['5772']
data_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/dst/'
pulser_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/skim/pulser'
data_prefix='hps_00'
data_postfix='.root'
doMC = True
doData = True
doPulser = False
analysis='recoilAnalysis.py'
analysisPulser='pulserAnalysis_pass4.py'
anapre='recoil_'
if doData : 
    for run in runList:
        logfile='logs/'+anapre+data_prefix+run+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/Data/'+anapre+data_prefix+run+'_'+analysis_postfix+'.root'
        dstfile=data_dir+'/'+data_prefix+run #TChain will glob onto this
    #    dstfile=data_dir+'/'+data_prefix+run+'.4' #TChain will glob onto this
        print dstfile
        cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -o '+outfile+' '+dstfile
        print cmd
        os.system(cmd)
    #run over pulser data too...
   

if doPulser :
    logfilePulser='logs/'+anapre+data_prefix+'_pulser_'+analysis_postfix+'.log'
    os.system('rm '+logfilePulser)
    outfilePulser='OutputHistograms/Data/'+data_prefix+'_pulser_'+analysis_postfix+'.root'
    dstfilePulser=pulser_dir+'/'+data_prefix #TChain will glob onto this
        #    dstfilePulser=data_dir+'/'+data_prefix+'5772.4' #TChain will glob onto this
    print dstfilePulser
    cmd='bsub -q long -W 5000 -o '+logfilePulser+' python '+analysis+' -p True -o '+outfilePulser+' '+dstfilePulser
    os.system(cmd)
        
#mcTypeList=['beam-tri']
#mcTypeList=['wab-beam-tri','beam-tri','tritrig','pulser-beam-tri','pulser-wab-beam-tri','tritrig-beam-tri','tritrig-wab-beam-tri' ]
#mcTypeList=['wab-beam-tri']
mcTypeList=['tritrig-beam-tri','tritrig-wab-beam-tri','wab-beam-tri','beam-tri','wab']
#mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass4/mc/dst'
mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/mc/dst'
mc_prefix='HPS-EngRun2015-Nominal-v4-4'
mc_postfix='.root'
if doMC is True : 
    for mcType in mcTypeList:
        logfile='logs/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/MC/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
        dstfile=mc_dir+'/'+mcType+'/'+'*'+mc_prefix #TChain will glob onto this
        print dstfile
        cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -m True -o '+outfile+' '+dstfile
        print cmd
        os.system(cmd)
