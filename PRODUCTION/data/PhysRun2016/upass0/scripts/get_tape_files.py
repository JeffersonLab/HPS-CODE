#!/usr/bin/env python
import os,re,sys,glob

run_min = 7219
run_max = 8101

evio_pattern = '*.evio.*'

f_tape_list = open("lists/tepe_files.dat", 'w')

file_list_dict = dict()

for run in range(run_min, run_max):
    file_list_dict[run] = glob.glob('/mss/hallb/hps/data/*'+str(run)+evio_pattern)
#    print '/mss/hallb/hps/*'+str(run)+evio_pattern
    print "cur run is ", run
    for cur_file in file_list_dict[run]:
        print >>f_tape_list, cur_file
