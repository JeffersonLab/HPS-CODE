#!/usr/bin/env python
import os,re,sys

def getRunfilesFromXmlFile(fileName):
    if not os.path.exists(fileName): sys.exit('Missing file:  '+fileName)
    runno,filenos,runfiles=0,[],{}
    for line in open(fileName,'r').readlines():
        if line.find('<List name="fnum">')>0:
            line=line.replace('<List name="fnum">','')
            line=line.replace('</List>','')
            filenos=[int(xx) for xx in line.strip().split()]
            if len(filenos)<=0: sys.exit('Error in '+fileName+':  '+line)
        elif line.find('<Variable name="run"')>0:
            mm=re.search('(\d\d\d\d+)',line)
            if mm==None: sys.exit('Error in '+fileName+':  '+line)
            runno=int(mm.group(1))
        if runno>0 and len(filenos)>0: break
    if runno!=0 and len(filenos)>0: runfiles[runno]=filenos
    return runfiles

def getRunfilesFromXmlDir(dirname):
    runfiles={}
    for (dpath,dnames,fnames) in os.walk(dirname):
        for fileName in [dpath+'/'+xx.rstrip() for xx in fnames]:
            runfiles.update(getRunfilesFromXmlFile(fileName))
    return runfiles

def getRunfileFromDataFile(fileName):
    mm=re.search('_00(\d\d\d\d).(\d+)',fileName)
    if mm==None: sys.exit('Error in '+fileName)
    return [int(mm.group(1)),int(mm.group(2))]

def getRunfilesFromDataDir(dirname):
    runfiles={}
    for (dpath,dnames,fnames) in os.walk(dirname):
        for fileName in [dpath+'/'+xx.rstrip() for xx in fnames]:
            [runno,filno]=getRunfileFromDataFile(fileName)
            if runfiles.has_key(runno):
                if not filno in runfiles[runno]:
                    runfiles[runno].append(filno)
            else: runfiles[runno]=[filno]
    return runfiles

def getNfiles(runfiles):
    nfiles=0
    for runno in runfiles.keys(): 
        nfiles += len(runfiles[runno])
    return nfiles

def getMissingRunfiles(submitted,resulted):
    missing={}
    for runno in submitted.keys():
        for filno in submitted[runno]:
            if filno in resulted[runno]: continue
            if missing.has_key(runno): missing[runno].append(filno)
            else:                      missing[runno]=[filno]
    return missing


dog=getRunfilesFromDataDir(sys.argv[1])
print dog
print getNfiles(dog)

cat=getRunfilesFromXmlDir(sys.argv[2])
print cat
print getNfiles(cat)

pig=getMissingRunfiles(cat,dog)
print pig
print getNfiles(pig)

sys.exit()

rawDataFile=sys.argv[1]
recDataFile=sys.argv[2]

#'jsubs-subbed_files.txt'
#'disk/pulser.list'

#'jsubs-subbed-0pt5.list'
#'tape_recon.txt'

rawdata=open(rawDataFile,'r').readlines()
recdata=open(recDataFile,'r').readlines()

rawfiles={},{}

for rawdatum in rawdata:
    cols = rawdatum.strip().split()
    runno = int(cols.pop(0))
    for filno in cols:
        if rawfiles.has_key(runno):
            rawfiles[runno].append(int(filno))
        else:
            rawfiles[runno]=[int(filno)]

for recdatum in recdata:
    cols = recdatum.strip().split()
    if len(cols)==4:
        runno = int(cols[1])
        filno = int(cols[2])
        if recfiles.has_key(runno):  recfiles[runno].append(filno)
        else:                        recfiles[runno]=[filno]
    elif len(cols)==9:
        fileName=cols.pop()
        mm=re.search('_00(\d\d\d\d).(\d+)',fileName)
        if mm==None: continue
        runno,filno=int(mm.group(1)),int(mm.group(2))
        if recfiles.has_key(runno):  recfiles[runno].append(filno)
        else:                        recfiles[runno]=[filno]


for runno in sorted(rawfiles.keys()):
    for filno in sorted(rawfiles[runno]):
        if recfiles.has_key(runno):
            if filno in recfiles[runno]:
                continue
        print runno,filno


#adict = recfiles
#for runno in sorted(adict.keys()):
#    for filno in sorted(adict[runno]):
#        print runno,filno


#        recfiles.find('00%d.%d'%(runno,filno))

