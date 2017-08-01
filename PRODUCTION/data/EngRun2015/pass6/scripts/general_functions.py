#!/usr/bin/env python
import os,re,sys,glob

# This function returns tape file size in bytes
# the argument is the full path mss file
def getTapeFileSize(fname):
    
    f_mss = open(fname, 'r')
    
    for cur_line in f_mss.readlines():
        if cur_line.find("ize=")>0:
            cur_line = cur_line.replace('size=', '')
            cur_line = cur_line.replace('\n', '')
            return int(cur_line)


#This function looks into directories dir1 and dir2 for
#files with pattern, thenreturn list of files that are in
# dir1, but missing in dir2 
def FindMissingFiles(dir1, dir2, pattern):
    files1 = glob.glob(dir1+'/'+pattern)
    files2 = glob.glob(dir2+'/'+pattern)
    
    for (i, cur_file) in enumerate(files1):
        files1[i] = files1[i].replace(dir1 + '/', '')

    for (i, cur_file) in enumerate(files2):
        files2[i] = files2[i].replace(dir2 + '/', '')

    missing_list = []
    for cur_file in files1:
        if cur_file in files2: continue
        else: missing_list.append(dir1+'/'+cur_file)
        
    return missing_list
