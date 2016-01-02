#!/usr/bin/env python
import re

rawDataFile=sys.argv[1]
recDataFile=sys.argv[2]

#'jsubs-subbed_files.txt'
#'disk/pulser.list'

#'jsubs-subbed-0pt5.list'
#'tape_recon.txt'

rawdata=open(rawDataFile,'r').readlines()
recdata=open(recDataFile,'r').readlines()

rawfiles={}
recfiles={}

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
        filename=cols.pop()
        mm=re.search('_00(\d\d\d\d).(\d+)',filename)
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

