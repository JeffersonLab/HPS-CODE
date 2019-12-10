import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

analysis_postfix='pass4_useGBL_ECalMatch_cluster_killing_weighted_ratios_L6_0pt1mm_L6Ele'
#analysis_postfix='pass6_useGBL_ECalMatch_SuperFiducialCut'
#analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_2Tracks'
#analysis_postfix='pass4_useGBL_ECalMatch_SuperFiducialCut_MoreThan2Tracks_HighESum'
#mc_dir='mc/tritrig/dst/'
runList=['8099']
data_dir='/nfs/sla/g/hps3/data/hpsrun2016/Pass4/dst'
pulser_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/skim/pulser'
data_prefix='hps_00'
data_postfix='.root'
doMC = True
doData = False
doPulser = False
analysis='tridentEfficiencyAnalysis.py'
anapre='trackefficiency_'
if doData : 
    for run in runList:
        logfile='logs/'+anapre+data_prefix+run+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/Data/'+data_prefix+run+'_'+analysis_postfix+'.root'
        dstfile=data_dir+'/'+data_prefix+run #TChain will glob onto this
    #    dstfile=data_dir+'/'+data_prefix+run+'.4' #TChain will glob onto this
        print dstfile
        cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' -o '+outfile+' -e 2.3 '+dstfile
        print cmd
        os.system(cmd)
    #run over pulser data too...ltr
   

if doPulser :
    logfilePulser='logs/'+anapre+data_prefix+'_pulser_'+analysis_postfix+'.log'
    os.system('rm '+logfilePulser)
    outfilePulser='OutputHistograms/Data/'+data_prefix+'_pulser_'+analysis_postfix+'.root'
    dstfilePulser=pulser_dir+'/'+data_prefix #TChain will glob onto this
        #    dstfilePulser=data_dir+'/'+data_prefix+'5772.4' #TChain will glob onto this
    print dstfilePulser
    cmd='bsub -q long -W 5000 -o '+logfilePulser+' python '+analysis+' -p True -e 2.3 -o '+outfilePulser+' '+dstfilePulser
    os.system(cmd)
        
#mcTypeList=['RAD','BH','tritrig-beam-tri','beam-tri']
#mcTypeList=['tritrig-WB','wabtrig-BT','WBT']
mcTypeList=['tritrig-WB','wabtrig-BT']
#mc_dir='/nfs/slac/g/hps/mgraham/hpsrun2016/mc/pass4_4.3.1'
mc_dir='/nfs/slac/g/hps/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTEfficiencyData/'
mc_prefix='HPS-PhysicsRun2016-Pass2-cluster-killing'
mc_postfix='.root'
if doMC is True : 
    for mcType in mcTypeList:
        logfile='logs/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/MC/'+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
        dstfile=mc_dir+'/'+mcType+'/dst/'+'*'+mc_prefix #TChain will glob onto this
        print dstfile
        cmd='bsub -R "rhel60" -W 5000 -o '+logfile+' python '+analysis+' -m True -e 2.3  -o '+outfile+' '+dstfile
        print cmd
        os.system(cmd)
