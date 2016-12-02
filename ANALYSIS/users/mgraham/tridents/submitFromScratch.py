import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

#analysis_postfix='pass6_useGBL_ECalMatch'
analysis_postfix='pass6_useGBL_ECalMatch_ECalCoincidence_TrackKiller_Position'
#analysis_postfix='foobar' 
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
doData = False
doPulser = False
analysis='fromscratchAnalysis.py'
analysisPulser='pulserAnalysis.py'
anapre='fromscratch_'
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
        
#mcTypeList=['RAD','BH','tritrig-beam-tri','beam-tri']
#mcTypeList=['wab-beam-tri','wab','tritrig']
#mcTypeList=['wab-beam-tri-zipFix','wab-beam-tri-zipFix-T0Offset','tritrig-NOSUMCUT']
mcTypeList=['wab','wab-beam-tri-zipFix','wab-beam-tri-zipFix-T0Offset','tritrig-NOSUMCUT']
#mcTypeList=['wab-beam-tri']
#mcTypeList=['wab']
#mcTypeList=['tritrig-beam-tri','tritrig-wab-beam-tri']
mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/mc/dst'
mc_prefix='HPS-EngRun2015-Nominal-v5-0'
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
