#!/usr/bin/env python
import sys
import shutil
import re
import string
import os
import time
import subprocess

from subprocess import Popen, PIPE

def getfilenumbers(xmlfile,runtype, run):    

    with open(xmlfile,"r") as tmp:
        lines = tmp.readlines()
        
    reltag="foobar"
    indir="foodir"
    for line in lines:      
        #get the release tag
        if re.search("Variable name=\"reltag\"", line) != None:
 #           print line.rstrip()
            matchMe=re.search("value=\"(\S*)\"",line)        
            if matchMe!=None and not isComment(line):
 #               print matchMe.group(1)
                reltag=matchMe.group(1)
        #get the input directory
        if re.search("Input src=", line) != None:
#            print line.rstrip()
            matchMe=re.search("src=\"(\S*)\"",line)
            if matchMe!=None and not isComment(line):
#                print matchMe.group(1)
                indirtmp=matchMe.group(1)
        #get the ouput directory
        if re.search("Variable name=\"out_dir\"", line) != None:
#            print line.rstrip()            
            matchMe=re.search("value=\"(\S*)\"",line)        
            if matchMe!=None and not isComment(line):
#                print matchMe.group(1)
                outdirtmp=matchMe.group(1)

    prefix=getPrefix(indirtmp)
    indir=fixDir(indirtmp)
    outdir=removeType(outdirtmp)
    print "release tag = "+reltag
    print "file prefix = "+prefix
    print "input directory = "+indir  
    print "output directory = "+outdir

# JUST FOR RUNNING OVER THE release=20150517.064728-130 THAT I SCREWED UP
#    reltag="20150517.064728-130"

    if runtype == "eviotolcio":
        midout=""                
    if runtype == "recon":
        midin=""
        postfixin="evio"
        midout="_recon_"+reltag
        postfixout="slcio"
    if runtype == "dst":
        midin="_recon_"+reltag
        postfixin="slcio"
        midout="_dst_"+reltag
        postfixout="root"
    if runtype == "dqm":
        postfixout="root"
        postfixin = "slcio"
        midin="_recon_"+reltag
        midout="_dqm_"+reltag
    n=0
    cnt=0
    maxCnt=1000
    outstring = "" 
    while n < maxCnt :
        if n%10 == 0 : 
            infileName=indir+prefix+run+"."+str(n)+midin+"."+postfixin
            if postfixin == "evio":    # the evio has funny label format...file extension not at end	
                infileName=indir+prefix+run+"."+postfixin+"."+str(n)
            outfileName=outdir+"/"+prefix+run+"."+str(n)+midout+"."+postfixout
#            print "input file is "+infileName
#            print "looking for "+outfileName
            if  (not os.path.isfile(outfileName)  and os.path.isfile(infileName)) :            
                outstring=outstring+ " " +str(n)
                cnt=cnt+1
        n=n+1

    if cnt == 0:
        outstring="foobar"
    print "Run over "+str(cnt)+" files for Run#"+run
    return outstring
#############################################
    
def removeType(inDir) : 
     #first, strip leading mss: or file:
    matchMe=re.search("mss:(\S*)",inDir) 
    if matchMe!=None :
        inDir=matchMe.group(1)
    matchMe=re.search("file:(\S*)",inDir) 
    if matchMe!=None :
        inDir=matchMe.group(1)
    return inDir

#############################################
def fixDir(inDir) :
    inDir=removeType(inDir)
    #now match to the last backslash
    matchMe=re.search("(\S+\/)\S+",inDir) 
    if matchMe!=None :
        inDir=matchMe.group(1)
    
#    print "returning "+inDir
    return inDir

##########################################
def getPrefix(inDir) :
    #match to the last backslash, save the next bit until the first $
    matchMe=re.search("\S+\/(\w+)\$",inDir) 
    if matchMe!=None :
        prefix=matchMe.group(1)
    
 #   print "returning "+prefix
    return prefix
############################################
def isComment(line) :
    return  re.search("<!--", line) != None

if __name__ == '__main__':
####
    if len(sys.argv) < 4:  #remember, the script name counts as an argument!
        print 'getFileNumbersBlind.py  <xml template> <runtype> <run number> '
        print '<runtype> can be eviotolcio, recon, dqm, dst'
        sys.exit()
    ####
    xmlfileI=sys.argv[1]
    runtypeI=sys.argv[2]
    runI=sys.argv[3]
    mystring=getfilenumbers(xmlfileI,runtypeI,runI)
    print mystring
