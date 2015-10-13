import sys
import shutil
import re
import string
import os
import glob
import array
from subprocess import Popen, PIPE


inputDir="/nfs/slac/g/hps3/data/engrun2015/pass2/mc/recon"
outputDir="/nfs/slac/g/hps3/data/engrun2015/pass2/mc/dst"
MCtype="tritrig"

allIn=inputDir+"/"+MCtype
allOut=outputDir+"/"+MCtype
print allIn
print allOut

fileList=os.listdir(allIn)

for ifile in fileList:
    print ifile
    outName=ifile.replace("slcio","root")
    inFile=allIn+"/"+ifile
    outFile=allOut+"/"+outName
    cmd="hps-dst/build/bin/dst_maker -o "+outFile+" "+inFile
    p=Popen(cmd,shell=True)
