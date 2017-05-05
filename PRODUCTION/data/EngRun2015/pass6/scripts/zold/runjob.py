#!/usr/bin/env python
import sys,shutil,re,string,os
from subprocess import Popen, PIPE
from getfilenumbers import getfilenumbers

def runjob(xmltemplate,runtype,runnumber,detector=None):

    PARS={
      'PASS':'pass1',
      'DETECTOR':'FOOBAR',
      'RELEASE':'R331',
      'JAR':'/u/group/hps/hps_soft/hps-java/hps-distribution-3.3.1-bin.jar'
    }
    PARS['RUNNO'] = str(runnumber)
    PARS['FILENOS'] = getfilenumbers(PARS['PASS'],str(PARS['RUNNO']))
    if detector!=None:  PARS['DETECTOR']=detector

    sys.stdout.flush()
    if PARS['FILENOS']=='foobar':
        print 'Nothing to run'
        sys.stdout.flush()
        sys.exit()

    tmpfile = 'temp.xml'
    shutil.copy(xmltemplate, tmpfile)

    with open(tmpfile,'r') as tmp:
        lines = tmp.readlines()

    with open(tmpfile,'w') as tmp:
        for line in lines:
            for key in PARS.keys():
                if line.find(key)<0: continue
                line=line.replace('XXX'+key+'XXX',PARS[key])
            tmp.write(line)

    #os.system("jsub -xml temp.xml")
    os.system('mv temp.xml jsubs/%s.xml'%(PARS['RUNNO']))


if __name__ == '__main__':
    if len(sys.argv) < 4:  #remember, the script name counts as an argument!
        print 'runjob.py <xml template> <runtype> <run number> [<detector>]'
        print '<runtype> can be eviotolcio, recon, dqm, dst'
        sys.exit()
    runjob(*sys.argv[1:])



