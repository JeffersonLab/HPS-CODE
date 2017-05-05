#!/usr/bin/env python
import os,re,sys,glob
sys.path.insert(0, 'scripts')
import general_functions

MSS_TOP = '/mss/hallb/hps'
DISK_TOP = '/work/hallb/hps/data'
RUNPERIOD = 'physrun2016'
PASS = 'pass0'
PRE = 'hps_00'

# For each recon file on tapes, write file name and the size
# in the file
#===== Recon =====
'''
f_recon_file_sizes = open('lists/reon_file_sizes.dat', 'w')
print MSS_TOP+'/'+RUNPERIOD+'/'+PASS+'/'+'recon'+'/'+'*recon*.slcio'

files = sorted(glob.glob(MSS_TOP+'/'+RUNPERIOD+'/'+PASS+'/'+'recon'+'/'+'*recon*.slcio'))

for cur_file in files:
    recon_size = general_functions.getTapeFileSize(cur_file)

    splited_fname = cur_file.split(PRE)
    splited_fname = splited_fname[1].split('.')
    
    runnumber = splited_fname[0]
    
    splited_fname = splited_fname[1].split('_')
    filenumber = splited_fname[0]

    print runnumber, filenumber, cur_file
    
    print >>f_recon_file_sizes, runnumber, filenumber, recon_size
   ''' 

#===== DST =====
# I want to compare tape and disk file sizes, to see if they match for all files or not
CATEGORY = 'dst'
FILEPATTERN = DISK_TOP+'/'+RUNPERIOD+'/'+PASS+'/'+CATEGORY+'/'+'*'+CATEGORY+'*'

disk_files = sorted(glob.glob(FILEPATTERN))

f_mismatch_DST = open('lists/TAPE_DISK_difference_DST.dat', 'w')

for cur_disk_file in disk_files:
    cur_tape_file = cur_disk_file.replace(DISK_TOP, MSS_TOP )
    disk_size = os.path.getsize(cur_disk_file)
    tape_size = general_functions.getTapeFileSize(cur_tape_file)
   # print cur_disk_file, cur_tape_file, disk_size, tape_size
    size_diff = int(disk_size) - int(tape_size)
    
    if size_diff != 0:
        #print >>f_mismatch_DST, size_diff, disk_size, tape_size, cur_disk_file
        print >>f_mismatch_DST, cur_tape_file
