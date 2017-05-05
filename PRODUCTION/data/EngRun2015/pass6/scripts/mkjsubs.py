#!/usr/bin/env python
import sys,re,os,subprocess

# these can be overridden by command line:
PARS={
    'PASS':'tweakpass6',
    'DETECTOR':'HPS-EngRun2015-Nominal-v5-0-fieldmap',
#    'DETECTOR':'HPS-EngRun2015-Nominal-v4-4-fieldmap',
    'FIELDMAP':'125acm2_3kg_corrected_unfolded_scaled_0.7992.dat',
    'TAPETOPDIR':'/mss/hallb/hps/engrun2015',
    'DISKTOPDIR':'/work/hallb/hps/data/engrun2015',
    'RELEASE':'Rv4657',
    'JAR':'hps-distribution-3.11_rv4657.jar',
#    'JAR':'hps-distribution-3.9-2mmskim-bin.jar',
    'XMLTEMPLATE':'templates/all.xml',
    'RUNTYPE':'recon',
    'PREFIX':'hps',
    'DEBUG': '0',
#    'STEERING':'/org/hps/steering/recon/EngineeringRun2015FullRecon.lcsim',
    'STEERING':'/org/hps/steering/recon/TweakPass.lcsim',
    'UNBLIND':1
}

# the default run range (can be overriden by command line):
RUNRANGE=[5000,5800]

# these will go to disk (in addition to tape):
CANONRUNS=[5772,5775]#,5739,5698]

# these will be processed in full, and go to disk (in addition to tape):
#CALIBRUNS=[5222,5228,5229,5393,5546,5747,5749,5754,5755,
#           5756,5757,5774,5777,5778,5779,5781,5784,5785,5786]

CALIBRUNS=[]

# these will not be processed at all:
IGNORERUNS=[4924,5216,5240,5249,5352,5388,5413,5464,5488,5528,5580,5612,5727,5628,5658,5731,5734,5735,5736,5744,5750,5751,5759,5777, 5778,5780,5798,5814]

# not currently used:
#ECALONLYRUNS=[5770,5771,5772,5773]

ROOTDIR='/u/group/hps/production/data/EngRun2015'
LISTEXE=ROOTDIR+'/scripts/generateLists.sh'

TAPERAWLIST=[]
TAPECOOKEDLIST=[]
DISKCOOKEDLIST=[]

# make the submission script for one run:
def mkjsub(runno,filnos=None):

    if runno in IGNORERUNS: return
    PARS['RUNNO'] = str(runno)
    PARS['PREFIX'] = getFilePrefix(str(runno))

    # automatic file numbers generation:
    if filnos=='' or filnos==None:
        PARS['FILENOS'] = getFileNumbers(str(runno))
        jsubfilename = 'jsubs/%s.xml'%(PARS['RUNNO'])

    # manual file numbers generation:
    else:
        PARS['FILENOS'] = filnos
        jsubfilename = 'jsubs/%s_%d.xml'%(PARS['RUNNO'],len(filnos))

    if PARS['FILENOS']=='' or PARS['FILENOS']==None: return
    if int(PARS['DEBUG'])>0:
        print 'DEBUG: ',runno,PARS['FILENOS']
        return

    nfiles=len(PARS['FILENOS'].split())
    #if nfiles<2 and not runno in CALIBRUNS: return

    # parse xml template and create jsub/*.xml:
    with open(PARS['XMLTEMPLATE'],'r') as tmp: lines=tmp.readlines()
    if not os.path.exists('jsubs'): os.mkdir('jsubs')
    with open(jsubfilename,'w') as tmp:
        for line in lines:
            for key in PARS.keys():
                if key == 'DEBUG': continue
                line=line.replace('XXX'+key+'XXX',str(PARS[key]))
            if line.find('CANON')==0:
                if not runno in CANONRUNS and not runno in CALIBRUNS: continue
                line=line.replace('CANON','     ')
            if line.find('PROD')==0:
                if runno in CALIBRUNS: continue
                else: line=line.replace('PROD','    ')
            tmp.write(line)

def getNFilesFromString(filenos):
    cols = filenos.split(" ")
    nfiles = len(cols) - 1
    return nfiles


####### Re_JSub categorized filed jobs, e.g. Recon (All), DSTs (only DSTs), DQM, etc
def Remkjsub(runno,filnos, category):

    if int(runno) in IGNORERUNS: return
    PARS['RUNNO'] = str(runno)
    PARS['PREFIX'] = getFilePrefix(str(runno))

#    # automatic file numbers generation:
#    if filnos=='' or filnos==None:
#        PARS['FILENOS'] = getFileNumbers(str(runno))
#        jsubfilename = 'Re_jsubs/%s_%s.xml'%(PARS['RUNNO'], category)

    # manual file numbers generation:
#    else:
    PARS['FILENOS'] = filnos
    
    nFiles = getNFilesFromString(filnos)
    jsubfilename = 'Re_jsubs/%s_%s_%d.xml'%(PARS['RUNNO'],category, nFiles)

    if PARS['FILENOS']=='' or PARS['FILENOS']==None: return
    if int(PARS['DEBUG'])>0:
        print 'DEBUG: ',runno,PARS['FILENOS']
        return

    #nfiles=len(PARS['FILENOS'].split())
    #if nfiles<2 and not runno in CALIBRUNS: return

    # parse xml template and create jsub/*.xml:
    with open("templates/%s.xml"%(category),'r') as tmp: lines=tmp.readlines()
    if not os.path.exists('Re_jsubs'): os.mkdir('Re_jsubs')
    with open(jsubfilename,'w') as tmp:
        for line in lines:
            for key in PARS.keys():
                if key == 'DEBUG': continue
                line=line.replace('XXX'+key+'XXX',str(PARS[key]))
            if line.find('CANON')==0:
                if not runno in CANONRUNS and not runno in CALIBRUNS: continue
                line=line.replace('CANON','     ')
            if line.find('PROD')==0:
                if runno in CALIBRUNS: continue
                else: line=line.replace('PROD','    ')
            tmp.write(line)
#######

# get path to where files should be:
def getPathStub(runtype):
    if   runtype == 'recon':      stub = 'recon'
    elif runtype == 'dst':        stub = 'dst'
    elif runtype == 'dqm':        stub = 'data_quality/dqm'
    elif runtype == 'dq':         stub = 'data_quality/recon'
    elif runtype == 'trigdiag':   stub = 'trigdiag/aida'
    else:                         sys.exit('Invalid Runtype')
    #
    if runtype == 'recon': return PARS['TAPETOPDIR']+'/'+PARS['PASS']+'/'+stub
    else:                  return PARS['DISKTOPDIR']+'/'+PARS['PASS']+'/'+stub

# update lists of files on tape and disk:
def updateLists():
    global TAPERAWLIST,TAPECOOKEDLIST,DISKCOOKEDLIST
    listdir = ROOTDIR + '/' + PARS['PASS'] + '/lists'
    if PARS['DEBUG']=='0':
        print 'Generating lists ....'
        subprocess.call(LISTEXE+' '+PARS['PASS']+' >& /dev/null',shell=True)
    with open(listdir+'/tape.txt','r') as tmp:
        TAPERAWLIST=tmp.readlines()
    with open(listdir+'/tape_'+PARS['PASS']+'.txt','r') as tmp:
        TAPECOOKEDLIST=tmp.readlines()
    with open(listdir+'/disk_'+PARS['PASS']+'.txt','r') as tmp:
        DISKCOOKEDLIST=tmp.readlines()

# get file numbers that should be processed:
def getFileNumbers(runno):
    space=''
    filenos=''
    blinded = not int(runno) in CALIBRUNS # and not int(runno) in ECALONLYRUNS
    prefix=getFilePrefix(runno)
    for file1 in TAPERAWLIST:
        (runno1,filno1) = getRawRunfilno(file1)
        if runno1==None or filno1==None: continue
        if int(runno1) != int(runno): continue
        if not PARS['UNBLIND'] and blinded and int(filno1)%10!=0: continue
        stub = getPathStub(PARS['RUNTYPE'])+'/'+prefix
        #if isMissing(file1,stub,DISKCOOKEDLIST):
        if isMissing(file1,stub,TAPECOOKEDLIST):
            filenos += space+filno1
            space=' '
    return filenos

# get file prefix (e.g. hps_, hpsecal_, hpssvt_)
def getFilePrefix(runno):
    prefix=None
    for file1 in TAPERAWLIST:
        (runno1,filno1) = getRawRunfilno(file1)
        if runno1==None or int(runno1)!=int(runno): continue
        prefix = re.split('/',file1).pop()
        prefix = re.split('_',prefix).pop(0)
        break
    return prefix

# get run/file numbers from EVIO filenames:
def getRawRunfilno(filename):
    mm = re.search('_(\d\d\d\d\d\d)\.evio\.(\d+)',filename)
    if mm==None: return (None,None)
    else:        return (mm.group(1),mm.group(2))

# get run/file numbers from any reconstructed filenames:
def getCookedRunfilno(filename,stub):
    mm = re.search(stub+'_(\d\d\d\d\d\d)\.(\d+)',filename)
    if mm==None: return (None,None)
    else:        return (mm.group(1),mm.group(2))

# see if file already exists:
def isMissing(rawfile,cookedStub,cookedFileList):
    (rawRunno,rawFilno) = getRawRunfilno(rawfile)
    if not rawRunno or not rawFilno: return False
    for cookedFile in cookedFileList:
        (cookedRunno,cookedFilno) = getCookedRunfilno(cookedFile,cookedStub)
        if not cookedRunno or not cookedFilno: continue
        if rawRunno==cookedRunno and rawFilno==cookedFilno: return False
    return True

def printPars():
    for key in PARS.keys():
        print key+'='+str(PARS[key])

if __name__ == '__main__':

    scriptName=sys.argv.pop(0)

    usage='\nUsage:\n'
    usage+='\t'+scriptName+' [options]\n'
    usage+='\t'+scriptName+' [options] runFileListFilename\n'
    usage+='\t'+scriptName+' [options] run\n'
    usage+='\t'+scriptName+' [options] runMin runMax\n'

    # find and remove PAR=VALUE configuration args:
    for arg in sys.argv[:]:
        if arg.find('=')<0: continue
        (key,val) = arg.split('=',1)
        if not PARS.has_key(key):
            print('\nInvalid Key:  '+key+'\n\nValid Keys:')
            printPars()
            sys.exit(usage)
        PARS[key]=val
        sys.argv.remove(arg)

    # don't run if -h option present:
    for arg in sys.argv:
        if arg=='-h':
            printPars()
            sys.exit(usage)

    # run/file list:
    runs={}

    # default, full run range:
    if len(sys.argv)==0:
        for run in range(RUNRANGE[0],RUNRANGE[1]+1): runs[run]=None

    elif len(sys.argv)==1:

        # read run+file list from file:
        # file format is "run [file# [file# [file#]]]"
        if os.path.exists(sys.argv[0]):
            data = open(sys.argv[0],'r').readlines()
            for line in data:
                cols=line.strip().split()
                try: run=int(cols[0])
                except ValueError: sys.exit('\nInvalid Run Number in File: '+cols[0])
                cols.pop(0)
                if len(cols)==0:
                    if runs.has_key(run): sys.exit('\nInvalid Input File: Duplicate Runs.'+usage)
                    else: runs[run]=None
                else:
                    for fil in cols:
                        if runs.has_key(run): runs[run]+=' '+fil
                        else:                 runs[run]=fil

        # single run:
        else:
            try: runs[int(sys.argv[0])]=None
            except ValueError: sys.exit('\nInvalid Run Number on Command Line: '+sys.argv[0]+usage)

    # user-defined run range:
    elif len(sys.argv)==2:
        try:
            if int(sys.argv[1])<int(sys.argv[0]):
                sys.exit('Invalid Run Range:  '+sys.argv[0]+' '+sys.argv[1]+usage)
            for run in range(int(sys.argv[0]),int(sys.argv[1])+1): runs[run]=None
        except ValueError:
            sys.exit('\nInvalid Run Number on Command Line: '+sys.argv[0]+' '+sys.argv[1]+usage)

    # invalid command line:
    else: sys.exit('\nInvalid Command Line.\n'+usage)

    updateLists()

    # make all the jsubs:
    for run in runs.keys(): mkjsub(run,runs[run])


