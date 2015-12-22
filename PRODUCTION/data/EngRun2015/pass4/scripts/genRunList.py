#!/usr/bin/env python
import sys,re

runmin=int(sys.argv[2])
runmax=int(sys.argv[3])

runs={}
for filename in open(sys.argv[1]).readlines():
    filename=filename.strip()
    match=re.search('hps_00(\d\d\d\d)\.evio\.(\d+)',filename)
    if match==None: continue
    runno,filno=int(match.group(1)),int(match.group(2))
    if not runs.has_key(runno): runs[runno]=[filno]
    else:                       runs[runno].append(filno)
    #print filename,runno,filno

for run in sorted(runs.keys()):
    if run<runmin: continue
    if run>runmax: continue
    if len(runs[run])<=1: continue
    print run,len(runs[run])

