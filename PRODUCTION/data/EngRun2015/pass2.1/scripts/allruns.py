#!/usr/bin/env python
import sys,shutil,re,string,os,time,subprocess

# these can be overridden by command line:
PARS={
    'PASS':'pass2',
    'DETECTOR':'HPS-EngRun2015-Nominal-v3-fieldmap',
    'FIELDMAP':'125acm2_3kg_corrected_unfolded_scaled_0.7992.dat',
    'TAPETOPDIR':'/mss/hallb/hps/engrun2015',
    'DISKTOPDIR':'/work/hallb/hps/data/engrun2015',
    'RELEASE':'R340',
    'JAR':'/u/group/hps/hps_soft/hps-java/hps-distribution-3.4.0-bin.jar',
    'XMLTEMPLATE':'templates/all.xml',
    'RUNTYPE':'recon',
    'PREFIX':'hps',
    'DEBUG': 0,
    'STEERING':'/org/hps/steering/recon/EngineeringRun2015FullRecon_Pass2.lcsim'
}

# the default run range (can be overriden by command line):
RUNRANGE=[5254,5800]

# these will go to disk (in addition to tape):
CANONRUNS=[5772,5739,5698]

# these will be processed in full, and go to disk (in addition to tape):
CALIBRUNS=[5222,5228,5229,5393,5546,5747,5749,5754,5755,
           5756,5757,5774,5777,5778,5779,5781,5784,5785,5786]

# these will not be processed at all:
IGNORERUNS=[4924,5216,5240,5249,5352,5388,5413,5464,5488,5528,
            5580,5612,5628,5658,5798,5814]

# not currently used:
#ECALONLYRUNS=[5770,5771,5772,5773]

ROOTDIR='/u/group/hps/production/data/EngRun2015'
LISTEXE=ROOTDIR+'/scripts/generateLists.sh'

TAPERAWLIST=[]
TAPECOOKEDLIST=[]
DISKCOOKEDLIST=[]

def allruns(runs):
    updateLists()
    print 'Finding Runs ...'
    if len(runs)==0: runs=RUNRANGE
    if len(runs)==2: runs=range(int(runs[0]),int(runs[1]))
    for xx in runs: runjob(int(xx))
    print "Done with allruns.py"

def runjob(runno):
    if runno in IGNORERUNS: return
    PARS['RUNNO'] = str(runno)
    PARS['FILENOS'],PARS['PREFIX'] = getFileNumbers(str(runno))
    if PARS['FILENOS']=='': return
    if PARS['DEBUG']>0:
        print 'DBG: ',runno,PARS['FILENOS']
        return
    with open(PARS['XMLTEMPLATE'],'r') as tmp: lines=tmp.readlines()
    if not os.path.exists('jsubs'): os.mkdir('jsubs')
    with open('jsubs/%s.xml'%(PARS['RUNNO']),'w') as tmp:
        for line in lines:
            for key in PARS.keys():
                if key == 'DEBUG': continue
                line=line.replace('XXX'+key+'XXX',PARS[key])
            if line.find('CANON')==0:
                if runno in CANONRUNS or runno in CALIBRUNS:
                    line=line.replace('CANON','     ')
                else:
                    continue
            if line.find('PROD')==0:
                if runno in CALIBRUNS:
                    continue
                else:
                    line=line.replace('PROD','     ')
            tmp.write(line)

def getPathStub(runtype):
    if   runtype == 'recon':      stub = 'recon'
    elif runtype == 'dst':        stub = 'dst'
    elif runtype == 'dqm':        stub = 'data_quality/dqm'
    elif runtype == 'dq':         stub = 'data_quality/recon'
    elif runtype == 'trigdiag':   stub = 'trigdiag/aida'
    else:                         sys.exit('Invalid Runtype')
    if runtype == 'recon': return PARS['TAPETOPDIR']+'/'+PARS['PASS']+'/'+stub
    else:                  return PARS['DISKTOPDIR']+'/'+PARS['PASS']+'/'+stub

def updateLists():
    global TAPERAWLIST,TAPECOOKEDLIST,DISKCOOKEDLIST
    listdir = ROOTDIR + '/' + PARS['PASS'] + '/lists'
    if PARS['DEBUG']==0:
        print 'Generating lists ....'
        subprocess.call(LISTEXE+' '+PARS['PASS']+' >& /dev/null',shell=True)
    with open(listdir+'/tape.txt','r') as tmp:
        TAPERAWLIST=tmp.readlines()
    with open(listdir+'/tape_'+PARS['PASS']+'.txt','r') as tmp:
        TAPECOOKEDLIST=tmp.readlines()
    with open(listdir+'/disk_'+PARS['PASS']+'.txt','r') as tmp:
        DISKCOOKEDLIST=tmp.readlines()

def getFileNumbers(runno):
    prefix=''
    space=''
    filenos=''
    blinded = not int(runno) in CALIBRUNS # and not int(runno) in ECALONLYRUNS
    for file1 in TAPERAWLIST:
        (runno1,filno1) = getRawRunfilno(file1)
        if runno1==None or filno1==None: continue
        if int(runno1) != int(runno): continue
        if blinded and int(filno1)%10!=0: continue
        prefix = re.split('/',file1).pop()
        prefix = re.split('_',prefix).pop(0)
        stub = getPathStub(PARS['RUNTYPE'])+'/'+prefix
        if isMissing(file1,stub,DISKCOOKEDLIST):
        #if isMissing(file1,stub,TAPECOOKEDLIST):
            filenos += space+filno1
            space=' '
    return (filenos,prefix)

def getRawRunfilno(filename):
    mm = re.search('_(\d\d\d\d\d\d)\.evio\.(\d+)',filename)
    if mm==None: return (None,None)
    else:        return (mm.group(1),mm.group(2))

def getCookedRunfilno(filename,stub):
    mm = re.search(stub+'_(\d\d\d\d\d\d)\.(\d+)',filename)
    if mm==None: return (None,None)
    else:        return (mm.group(1),mm.group(2))

def isMissing(rawfile,cookedStub,cookedFileList):
    missing = 1
    (rawRunno,rawFilno) = getRawRunfilno(rawfile)
    if not rawRunno or not rawFilno: return False
    for cookedFile in cookedFileList:
        (cookedRunno,cookedFilno) = getCookedRunfilno(cookedFile,cookedStub)
        if not cookedRunno or not cookedFilno: continue
        if rawRunno==cookedRunno and rawFilno==cookedFilno:
            return False
    return True

if __name__ == '__main__':

    sys.argv.pop(0) # remove python script name

    for arg in sys.argv:
        if arg=='-h': sys.exit(PARS)

    for arg in sys.argv[:]:
        if arg.find('=')<0: continue
        (key,val) = arg.split('=',1)
        if not PARS.has_key(key): sys.exit('Missing Key:  '+key)
        PARS[key]=val
        sys.argv.remove(arg)

    if len(sys.argv)==1: runjob(sys.argv[0])
    else:                allruns(sys.argv)


