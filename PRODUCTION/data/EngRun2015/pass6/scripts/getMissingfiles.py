#!/usr/bin/env python
import os,re,sys,glob
sys.path.insert(0, 'scripts')
import general_functions

f_runs = open("lists/Nathans_List.dat", 'r')

#for cur_run in f_runs.readlines():
#    cur_run = cur_run.replace('\n', '')
#getListofMissingFiles(passn, category, cur_run)

base_recon_dir = "/mss/hallb/hps/engrun2015";
passn = "tweakpass6";
stub = "ntuple/moller";
dir_recon_files = base_recon_dir+'/'+passn+"/recon";
dir_recon = base_recon_dir+'/'+passn+'/'+stub;
category = 'nt_moller'

stage_base_dir = "/lustre/expphy/stage/hps/mss/hallb/hps/engrun2015"
stage_dir = stage_base_dir+'/'+passn+'/'+stub

print dir_recon_files;
print dir_recon;

files_recon = glob.glob(dir_recon_files+'/'+'*.slcio')
files_category = glob.glob(dir_recon+'/'+'*.root')

files_recon = [w.replace(dir_recon_files, dir_recon) for w in files_recon]
files_recon = [w.replace('slcio', 'root') for w in files_recon]
files_recon = [w.replace('recon', category) for w in files_recon]

f_outfile = open('lists/broken_stage_'+category+'.dat', 'w')

for cur_file in files_recon:
    #print cur_file
    if cur_file in files_category: continue
    else:
        cur_file = cur_file.replace(dir_recon, stage_dir)
        print >>f_outfile, cur_file

