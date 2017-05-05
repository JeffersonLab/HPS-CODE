#!/usr/bin/env python
import os,re,sys,glob#!/usr/bin/env python

def getListOfFiles(base_dir, pattern ):
    full_path = glob.glob(base_dir+pattern)
    fname_list = [];
    for cur_file in full_path:
        cur_file = cur_file.replace(base_dir, '')
        fname_list.append(cur_file)
    return fname_list


disk_dir = "/work/hallb/hps/data/engrun2015/pass6/recon/"
mss_dir = "/mss/hallb/hps/engrun2015/pass6/recon/"

disk_file_pattern = '*.slcio'
mss_file_pattern = '*.slcio'

fnames_disk = getListOfFiles(disk_dir, disk_file_pattern )
fnames_mss = getListOfFiles(mss_dir, mss_file_pattern )

#print fnames_disk
#print fnames_mss

fmissing = open('missing_tape_files.dat', 'w');
fnonmissing = open('non_missingmissing_tape_files.dat', 'w');

for disk_file in fnames_disk:
    if disk_file in fnames_mss: 
        print >> fnonmissing, disk_file
    else: 
        print >> fmissing, disk_file
        
