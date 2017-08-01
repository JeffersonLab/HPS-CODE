#!/usr/bin/env python
import os,re,sys,glob
sys.path.insert(0, 'scripts')
import compare_mss_sizes
import mkjsubs

def getFileNumbersOfRun(RunNo):
    # This will look into the /mss/hallb/hps/data directory, and for 
    # run "RunNo" make a list that contains all file numbers for that run
    fileNumberList = []
    file_pattern = "/mss/hallb/hps/data/*"+str(RunNo)+"*"

    files = glob.glob(file_pattern)
    print "Determining file numbers " + file_pattern
    for cur_file in files:
        file_number = cur_file.split('evio.')
        #print file_number[1]
        fileNumberList.append(file_number[1]);

    return fileNumberList

BASEDIR = '/mss/hallb/hps/engrun2015/'
PASS = "pass6"
CATEGORY = 'dst'
PRE = 'hps_00'
RELEASE = 'R3.8'
SUFFIX = '.root'

mkjsubs.updateLists()

raw_number_dict = dict()

### The list of runs ###
f_runs = open("lists/Nathans_List.dat", 'r')
f_Blinded_files = open('lists/BLinded_List_of_'+CATEGORY+'.dat', 'w')

raw_number_dict = dict();

for cur_run in f_runs.readlines():
    cur_run = cur_run.replace('\n', '')

    if int(cur_run) in mkjsubs.IGNORERUNS: continue
    print "cur run is " + cur_run
    
    raw_number_dict[cur_run] = getFileNumbersOfRun(cur_run)
    n_files = len(raw_number_dict[cur_run])
    
    for ii in range(0, n_files - 1):
        if ii%10 == 0:
            filename = BASEDIR+PASS+'/'+CATEGORY+'/'+PRE+cur_run+'.'+str(ii)+'_'+CATEGORY+'_'+RELEASE+SUFFIX
            if os.path.isfile(filename):
                print >>f_Blinded_files, filename
