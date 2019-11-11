import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

radCut="" #don't cut in radiative region
#radCut="-r True"
energy="-e 2.3"
weigh=""  #don't do track efficiency weighting
#weigh="-w True"

#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut_KillInMomentum'
#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut_WeighInEclVsY_ElePosSame'

analysis_postfix='pass4_NoESumCut_OmarsBase_ClusterDeltaT_ClusterKilling_WeightedRatios_L6_0pt1mm'
#analysis_postfix='pass4_RadCut_OmarsBase_ClusterKilling_WeightedRatios_L6_0pt1mm'

#analysis_postfix='pass6_WABs_PureAndConverted_WeighInEclVsY_ElePosSeparate'
#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut_SameValDtCut'
#analysis_postfix='pass6_WABs_PureAndConverted'
#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut'
#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut_LooseDtCut'


runList=['8099']
data_dir='/nfs/slac/g/hps3/data/hpsrun2016/Pass4/dst'
pulser_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/skim/pulser'
data_prefix='hps_00'
data_postfix='.root'
doMC = True
doData = False
doPulser = False
analysis='wabAnalysisOmarsCuts.py'
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
        cmd='bsub -R "rhel60" -W 5000 -o '+logfile+' python '+analysis+' '+radCut+' '+energy+' -o '+outfile+' '+dstfile
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
        
#mcTypeList=['tritrig-WB','wabtrig-BT','RAD-WBT','WBT']
mcTypeList=['tritrig-WB','wabtrig-BT']
#mcTypeList=['tritrig-WB']
mc_dir='/nfs/slac/g/hps/HPS-CODE/ANALYSIS/users/mgraham/SVTHitEfficiency/SVTEfficiencyData/'
#mc_dir='/nfs/slac/g/hps/mgraham/hpsrun2016/mc/pass4_4.3.1/'
mc_prefix='HPS-PhysicsRun2016-Pass2' 
if doMC is True : 
    for mcType in mcTypeList:
        logfile='logs/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/MC/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
        dstfile=mc_dir+'/'+mcType+'/dst/'+'*'+mc_prefix #TChain will glob onto this
        print dstfile
        cmd='bsub -W 5000 -R "rhel60" -o '+logfile+' python '+analysis+' '+radCut+' '+energy+' -m True -o '+outfile+' '+dstfile
        print cmd
        os.system(cmd)
