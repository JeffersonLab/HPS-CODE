#!/usr/bin/env python
import subprocess
import tempfile
import re
import os,sys
import getopt

def print_usage():
    print "\nUsage: {} <settings name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-s: use the settings file at this full path (omit settings name)'
    print '\t-j: use the jar file at this full path'
    print '\t-p: use this SVT position (default \"Nominal\")'
    print '\t-d: use this detector name (default {}{}{})'.format(detectorprefix,position,detectorsuffix)
    print '\t-t: use this steering file'
    print '\t-H: use this host'
    print '\t-h: this help message'
    print


javapath="/home/hpsrun/hps_software/jdk1.8.0_40/bin/java"
settingsdir="/home/hpsrun/hps_software/reconMonitoringSettings"
jarpath="/home/hpsrun/hps_software/jars/hps-java.jar"
#settings='TrackAndReconMonitoring-template'

detectorprefix='HPS-EngRun2015-'
detectorsuffix='-v1'
position='Nominal'

steeringprefix='/org/hps/steering/monitoring/'
steeringname=None

detectorname=None
settingspath=None

settingsdict = {}

#print sys.argv[0]

options, remainder = getopt.gnu_getopt(sys.argv[1:], 's:j:p:d:t:H:h')

# Parse the command line arguments
for opt, arg in options:
    if opt=='-s':
        settingspath = arg
    if opt=='-j':
        jarpath = arg
    if opt=='-p':
        position = arg
    if opt=='-d':
        detectorname = arg
    if opt=='-t':
        steeringname = arg
        settingsdict['SteeringResource'] = steeringprefix + steeringname
    if opt=='-H':
        settingsdict['Host'] = arg
    elif opt=='-h':
        print_usage()
        sys.exit(0)


if (settingspath==None):
    if (len(remainder) != 1):
        print "need settings"
        print_usage()
        sys.exit(-1)
    settings=remainder[0]
    settingspath='{}/{}.settings'.format(settingsdir,settings)
else:
    if (len(remainder) != 0):
        print "don't need settings if -s option used"
        sys.exit(-1)

if (detectorname==None):
    detectorname= detectorprefix + position + detectorsuffix

settingsdict['DetectorName']= detectorname;

f = open(settingspath)
tempsettings = tempfile.NamedTemporaryFile(delete=False)
print tempsettings.name
for i in f:
    varname = i.split('=')[0].strip()
    if settingsdict.has_key(varname):
        #print i
        i=varname+'='+settingsdict[varname]+'\n'
        print i
    tempsettings.write(i)
f.close()
tempsettings.close()

java_args = [javapath,'-Xmx2g','-cp',jarpath,'-DdisableSvtAlignmentConstants']
app_args = ['org.hps.monitoring.application.Main','-c',tempsettings.name]
print java_args
print app_args
subprocess.call(java_args+app_args, shell=False)
os.remove(tempsettings.name)

