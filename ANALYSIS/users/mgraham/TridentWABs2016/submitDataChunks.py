import sys
import shutil
import re
import string
import os
import glob
from subprocess import Popen, PIPE

radCut="" #don't cut in radiative region
#radCut="-r True"
energy="-e 2.3"
weigh=""  #don't do track efficiency weighting
#weigh="-w True"

#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut_KillInMomentum'
#analysis_postfix='pass6_WABs_PureAndConverted_NoESumCut_WeighInEclVsY_ElePosSame'

analysis_postfix='pass4_NoESumCut_OmarsBase_ClusterDeltaT'

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
doMC = False
doData = True
doPulser = False
analysis='wabAnalysisOmarsCuts.py'
analysisPulser='pulserAnalysis.py'
anapre='fromscratch_'
#perRun=10 #multiple...e.g.10, 100, 1000, etc. 
#perRun=5 #multiple...e.g.10, 100, 1000, etc. or 1, 2, 5 
perRun=1 #multiple...e.g.10, 100, 1000, etc. or 1, 2, 5
if doData : 
    nst=0
    pref=""
    post=""
    jobcnt=1
    for run in runList:
        nfiles=len(glob.glob(data_dir+"/"+data_prefix+run+"*"))
        print nfiles
        while nst<nfiles:
            if nst>9 : 
                pref=str(int(nst/10))
            mod=nst%10
            post="["+str(mod)+"-"+str(mod+perRun-1)+"]"
#            dstfile=data_dir+"/"+data_prefix+run+"."+pref+"[0-9]_"
            dstfile=data_dir+"/"+data_prefix+run+"."+pref+post+"_"
            print(dstfile)
            logfile='logs/'+anapre+data_prefix+run+"."+str(jobcnt)+'_'+analysis_postfix+'.log'
            os.system('rm '+logfile)
            outfile='OutputHistograms/Data/'+anapre+data_prefix+run+"."+str(jobcnt)+'_'+analysis_postfix+'.root'
            cmd='bsub -R "rhel60" -W 5000 -o '+logfile+' python '+analysis+' '+radCut+' '+energy+' -o '+outfile+' '+dstfile
            print cmd
            os.system(cmd)
            jobcnt+=1
            nst=nst+perRun
