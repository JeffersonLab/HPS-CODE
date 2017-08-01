#!/usr/bin/env python
import sys,re,os,subprocess

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


