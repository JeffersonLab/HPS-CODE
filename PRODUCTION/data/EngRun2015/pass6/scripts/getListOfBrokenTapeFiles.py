#!/usr/bin/env python
import os,re,sys,glob
sys.path.insert(0, 'scripts')
import compare_mss_sizes
import mkjsubs

def getListOfBrokenTapeFiles(passn, category, RunNo):
    # This will look into the "/mss/hallb/hps/engrun2015/passn/recon directory, and for 
    # run "RunNo" make a list that contains all recon file numbers for that run

    if category == 'recon':           stub = '/recon'                ; run_type = 'recon'
    if category == 'dst':             stub = '/dst'                  ; run_type = 'dst'
    if category == 'dqm':             stub = '/data_quality/dqm'     ; run_type = 'dqm'
    if category == 'pulser':          stub = '/skim/pulser'          ; run_type = 'pulser'
    if category == 'pulser_dst':      stub = '/skim/dst/pulser'      ; run_type = 'pulser'
    if category == 's0':              stub = '/skim/s0'              ; run_type = 's0'
    if category == 's0_dst':          stub = '/skim/dst/s0'          ; run_type = 's0'
    if category == 'p0':              stub = '/skim/p0'              ; run_type = 'p0'
    if category == 'p0_dst':          stub = '/skim/dst/p0'          ; run_type = 'p0'
    if category == 'fee':             stub = '/skim/fee'             ; run_type = 'fee'
    if category == 'fee_dst':         stub = '/skim/dst/fee'         ; run_type = 'fee'
    if category == 'v0':              stub = '/skim/v0'              ; run_type = 'v0'
    if category == 'v0_dst':          stub = '/skim/dst/v0'          ; run_type = 'v0'
    if category == 'moller':          stub = '/skim/moller'          ; run_type = 'moller'
    if category == 'moller_dst':      stub = '/skim/dst/moller'      ; run_type = 'moller'
    if category == 'nt_tri':          stub = '/ntuple/tri'           ; run_type = 'nt'
    if category == 'nt_fee':          stub = '/ntuple/fee'           ; run_type = 'nt'
    if category == 'nt_moller':       stub = '/ntuple/moller'        ; run_type = 'nt'


    brokeTapeFileList = []
    file_pattern = "/mss/hallb/hps/engrun2015/"+str(passn)+stub+"/hps_00"+str(RunNo)+"*"

    files = glob.glob(file_pattern)
    
    print "Determining Broken Tape files" + file_pattern
    
    for cur_file in files:
        for cur_line in open(cur_file, 'r').readlines():
            if cur_line.find("ize=")>0:
                cur_line = cur_line.replace('size=', '')
                cur_line = cur_line.replace('\n', '')
                size = int(cur_line)
        if size < 50000:
            brokeTapeFileList.append(cur_file)
    return brokeTapeFileList


Run = 5772
category = 'fee_dst'
passn = 'tweakpass6'

#bad_dst_list = getListOfBrokenTapeFiles(passn, category, Run)

#print "List ot bad DST files = ", bad_dst_list

f_bad_Tape_files = open('lists/bad_tape_files_'+category+'.dat', 'w')

f_runs = open("lists/Nathans_List.dat", 'r')

for cur_run in f_runs.readlines():
    cur_run = cur_run.replace('\n', '')

    bad_tape_files = getListOfBrokenTapeFiles(passn, category, cur_run)
    for cur_file in bad_tape_files:
        print >>f_bad_Tape_files, cur_file
