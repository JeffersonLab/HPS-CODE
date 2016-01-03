#!/usr/bin/env python
import sys,re,os,subprocess

# used to kill all upass4's 1.5 mm jobs since deemed unecessary and hindering pass4

first5mm=5623

for job in open('jobstat.txt','r').readlines():
    cols=job.strip().split()
    jobid=cols[0]
    jobstatus=cols[2]
    jobname=cols[5]
    if jobstatus=='R': continue
    match=re.search('(\d\d\d\d)upass4',jobname)
    if match==None: continue
    runno=int(match.group(1))
    if runno>=first5mm: continue
    #print jobname+' '+jobstatus+'  jkill '+str(jobid)
    subprocess.call(['jkill',str(jobid)])


