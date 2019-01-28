import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

radCut="" #don't cut in radiative region
#radCut="-r True"

#analysis_postfix='tweakpass7_NoESumCut_WeighInEclVsY_KillL1Hits_ElePosSame_OmarsBase_WABCuts'
#analysis_postfix='tweakpass7_WeighInEclVsY_KillL1Hits_ElePosSame_OmarsBase'
analysis_postfix='tweakpass7_NoESumCut_WeighInEclVsY_KillL1Hits_ElePosSame_OmarsBase_WABCuts_SuperFiducial'
#analysis_postfix='tweakpass7_NoESumCut_WeighInEclVsY_ElePosSame_OmarsBase_WABCuts'


#analysis_postfix='tweakpass7_NoESumCut_WeighInEclVsY_ElePosSame_OmarsBase_WABCuts_SuperFiducial'
#analysis_postfix='tweakpass7_WeighInEclVsY_ElePosSame_OmarsBase_WABCuts_SuperFiducial'


#runList=['5772','5755','5754']
runList=['5772.1'] # this is 111/471 files
#runList=['5772.11'] # this is 11/471 files
#runList=['5772.*0_dst_'] # this is 48 files
#runList=['5772'] 
#data_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/dst/'
data_dir='/nfs/slac/g/hps3/data/engrun2015/tweakpass6/dst/'
pulser_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/skim/pulser'
data_prefix='hps_00'
data_postfix='.root'
doMC = True
doData = False
doPulser = False
doSkim=False
runOverSkim=False
analysis='wabAnalysisOmarsCuts.py'
analysisPulser='pulserAnalysis.py'
anapre='fromscratch_'
skimdir='SkimmedDSTs/'
if doData : 
    #!!!!!!!!!!!!!!!!!!!!!!!    screw with the data prefix   !!!!!!!!!!!!
    data_analysis_postfix=analysis_postfix.replace('tweakpass7','tweakpass6')
    for run in runList:
        logfile='logs/'+anapre+data_prefix+run+'_'+data_analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/Data/'+anapre+data_prefix+run+'_'+data_analysis_postfix+'.root'
        skimfile=skimdir+anapre+data_prefix+run+'_'+data_analysis_postfix+'.root'
        dstfile=data_dir+'/'+data_prefix+run #TChain will glob onto this
        print dstfile
        opts=' -o '+outfile
        if doSkim:
            opts=opts+' -n '+skimfile            
        if runOverSkim: 
            dstfile=skimfile
        cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' '+radCut+opts+' '+dstfile 
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
        

#mcTypeList=['wab-spinfix-100to1','RAD-MG5','wab-beam-tri-MG5','tritrig-MG5-ESum0pt5']
#mcTypeList=['wab-beam','tri-beam','wab-beam-tri-MG5-fixECalTiming','wab-spinfix-100to1','RAD-MG5','tritrig-MG5-ESum0pt5']
#mcTypeList=['RAD-MG5']
#mcTypeList=['tritrig-wab-beam']
#mcTypeList=['wabtrig-tri-beam','tritrig-wab-beam']
#mcTypeList=['wab','tritrig','wab-beam-tri','RAD']
mcTypeList=['wab-beam','tritrig-beam','RAD-beam','wab','tritrig','RAD']
#mc_dir='/nfs/slac/g/hps3/data/engrun2015/pass6/mc/dst'
mc_dir='/nfs/slac/g/hps3/data/engrun2015/tweakpass7/mc/dst'
#mc_prefix='HPS-EngRun2015-Nominal-v6-0'
mc_prefix='HPS-EngRun2015-Nominal-v5-0'
mc_postfix='.root'
if doMC is True : 
    for mcType in mcTypeList:
        logfile='logs/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.log'
        os.system('rm '+logfile)
        outfile='OutputHistograms/MC/'+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
        skimfile=skimdir+anapre+mcType+'_'+mc_prefix+'_'+analysis_postfix+'.root'
        dstfile=mc_dir+'/'+mcType+'/'+'*'+mc_prefix #TChain will glob onto this
        opts=' -o '+outfile
        if doSkim:
            opts=opts+' -n '+skimfile            
        if runOverSkim: 
            dstfile=skimfile   
        print dstfile
        cmd='bsub -q long -W 5000 -o '+logfile+' python '+analysis+' '+radCut+' -m True '+opts +' '+dstfile
        print cmd
        os.system(cmd)
