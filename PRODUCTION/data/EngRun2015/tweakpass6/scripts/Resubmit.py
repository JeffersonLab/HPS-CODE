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


def getReconFileNumbersOfRun(passn , RunNo):
    # This will look into the "/mss/hallb/hps/engrun2015/passn/recon directory, and for 
    # run "RunNo" make a list that contains all recon file numbers for that run
    fileNumberList = []
    file_pattern = "/mss/hallb/hps/engrun2015/"+str(passn)+"/recon/hps_00"+str(RunNo)+"*"

    files = glob.glob(file_pattern)
    print "Determining Recon file numbers " + file_pattern

   # print files

    for cur_file in files:
        file_number = cur_file.split(str(RunNo)+'.')
        file_number = file_number[1].split('_recon')
        #print file_number[0]
 #       file_size = compare_mss_sizes.getReconFileSize(str(passn), RunNo, file_number[0])
      #  print "file_size = ", file_size
  #      if file_size > 100000000:                # if file size is larger than 100 Mb
        fileNumberList.append(file_number[0]);

    return fileNumberList


def getCategorizedFileNumbersOfRun(passn, category, RunNo, from_tape=True):
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
    if category == 'v0pulser':        stub = '/skim/v0pulser'        ; run_type = 'v0pulser'
    if category == 'v0pulser_dst':    stub = '/skim/dst/v0pulser'    ; run_type = 'v0pulser'
    if category == 'nt_tri':          stub = '/ntuple2/tri'           ; run_type = 'tri'
    if category == 'nt_fee':          stub = '/ntuple2/fee'           ; run_type = 'fee'
    if category == 'nt_moller':       stub = '/ntuple2/moller'        ; run_type = 'moller'

    tape_top_dir = "/mss/hallb/hps/engrun2015/"
    disk_top_dir = "/work/hallb/hps/data/engrun2015/"
    file_top_dir = ""

    if from_tape == True:
        file_top_dir = tape_top_dir
    else:
        file_top_dir = disk_top_dir
    
    fileNumberList = []
    file_pattern = file_top_dir + str(passn)+stub+"/hps_00"+str(RunNo)+"*"

    files = glob.glob(file_pattern)
    print "Determining Recon file numbers " + file_pattern

   # print files

    for cur_file in files:
        file_number = cur_file.split(str(RunNo)+'.')
        file_number = file_number[1].split('_'+run_type)
        fileNumberList.append(file_number[0]);

    return fileNumberList



def getMissing(listA, list_Raw):
     missingNumberList = []
     
     for raw_n in list_Raw:
         if raw_n in listA: continue
         else: missingNumberList.append(raw_n);

     return missingNumberList

def getCombined(listA, listB):
    combinedlist = list(listA)
    
    for n1 in listB:
        if n1 in combinedlist: continue
        else: combinedlist.append(n1)
    return combinedlist


def RemoveMissRecons(listMissA, list_MissRecon):
    # This function will remov from the listA elements that are contained in in the Missing Recon list
    Reduced_List = list(listMissA)
    for cur_n in listMissA:
        if cur_n in list_MissRecon:
           Reduced_List.remove(cur_n)
        
    return Reduced_List
    

def getListAsOneString(aList):
    astr = ''
    for cur in aList:
        astr = astr + ' ' + cur
    
    return astr


#getReconFileNumbersOfRun("pass6", 5772)


PASS = "tweakpass6"


mkjsubs.updateLists()

raw_number_dict = dict()
recon_number_dict = dict()
recon_missing_number_dict = dict()
dst_number_dict = dict()
dst_missing_number_dict = dict()
dqm_number_dict = dict()
dqm_missing_number_dict = dict()

pulser_number_dict = dict()
pulser_missing_number_dict = dict()
pulser_dst_number_dict = dict()
pulser_dst_missing_number_dict = dict()
s0_number_dict = dict()
s0_missing_number_dict = dict()
s0_dst_number_dict = dict()
s0_dst_missing_number_dict = dict()
p0_number_dict = dict()
p0_missing_number_dict = dict()
p0_dst_number_dict = dict()
p0_dst_missing_number_dict = dict()
trigger_skim_missing_dict = dict()

fee_number_dict = dict()
fee_missing_number_dict = dict()
fee_dst_number_dict = dict()
fee_dst_missing_number_dict = dict()
moller_number_dict = dict()
moller_missing_number_dict = dict()
moller_dst_number_dict = dict()
moller_dst_missing_number_dict = dict()
v0_number_dict = dict()
v0_missing_number_dict = dict()
v0_dst_number_dict = dict()
v0_dst_missing_number_dict = dict()
phys_skim_missing_dict = dict()

v0pulser_number_dict = dict()
v0pulser_missing_number_dict = dict()
v0pulser_dst_number_dict = dict()
v0pulser_dst_missing_number_dict = dict()

nt_tri_number_dict = dict()
nt_tri_missing_number_dict = dict()
nt_fee_number_dict = dict()
nt_fee_missing_number_dict = dict()
nt_moller_number_dict = dict()
nt_moller_missing_number_dict = dict()
nt_all_missing_number_dict = dict()



Nmis_recon = 0
Nmis_dst = 0
Nmis_dqm = 0
Nmis_pulser = 0
Nmis_dst_pulser = 0
Nmis_s0 = 0
Nmis_dst_s0 = 0
Nmis_p0 = 0
Nmis_dst_p0 = 0
Nmis_fee = 0
Nmis_dst_fee = 0
Nmis_Moller = 0
Nmis_dst_Moller = 0
Nmis_v0 = 0
Nmis_dst_v0 = 0
Nmis_v0pulser = 0
Nmis_dst_v0pulser = 0
Nmis_nt_tri = 0
Nmis_nt_fee = 0
Nmis_nt_moller = 0

#f_runs = open("lists/test_list.dat", 'r')
#f_runs = open("lists/runs_2015_0p5mm.dat", 'r')
#f_runs = open("lists/goldenRunListSorted.txt", 'r')
#f_runs = open("lists/Nathans_List.dat", 'r')
#f_runs = open("lists/0p5mm_Holly", 'r');
f_runs = open("lists/1p5mm_Holly.dat", 'r');
#f_runs = open("lists/tmp.dat", 'r')

f_miss_stats = open('lists/failure_stats', 'w')

for cur_run in f_runs.readlines():
    cur_run = cur_run.replace('\n', '')

    if int(cur_run) in mkjsubs.IGNORERUNS: continue
    
    print "cur run is " + cur_run

    raw_number_dict[cur_run] = getFileNumbersOfRun(cur_run)

# =============== RECON ==================
    recon_number_dict[cur_run] = getReconFileNumbersOfRun(PASS, cur_run)
    recon_missing_number_dict[cur_run] = getMissing(recon_number_dict[cur_run], raw_number_dict[cur_run])
    
    recon_miss_filenos = getListAsOneString(recon_missing_number_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, recon_miss_filenos, "Recon")
    print recon_missing_number_dict[cur_run]
    
    Nmis_recon = Nmis_recon + len( recon_missing_number_dict[cur_run])
#    recon_miss_filenos = ''
#    for cur_fileno in recon_missing_number_dict[cur_run]:
#        recon_miss_filenos = recon_miss_filenos + ' ' + cur_fileno

    # ================= DST ================
    dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "dst", cur_run)
    dst_missing_number_dict[cur_run] = getMissing( dst_number_dict[cur_run], raw_number_dict[cur_run])
    dst_missing_number_dict[cur_run] = RemoveMissRecons(dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    dst_miss_filenos = getListAsOneString(dst_missing_number_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, dst_miss_filenos, "DST")
    print dst_missing_number_dict[cur_run]
    Nmis_dst = Nmis_dst + len( dst_missing_number_dict[cur_run])

    # ================= DQM ================
    dqm_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "dqm", cur_run)
    dqm_missing_number_dict[cur_run] = getMissing( dqm_number_dict[cur_run], raw_number_dict[cur_run])
    dqm_missing_number_dict[cur_run] = RemoveMissRecons(dqm_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    dqm_miss_filenos = getListAsOneString(dqm_missing_number_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, dqm_miss_filenos, "DQM")
    print dqm_missing_number_dict[cur_run]
    Nmis_dqm = Nmis_dqm + len( dqm_missing_number_dict[cur_run])

    # ================= Trig skims, this include pulser, s0 and p0 with their DSTs ================
    pulser_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "pulser", cur_run)
    pulser_missing_number_dict[cur_run] = getMissing( pulser_number_dict[cur_run], raw_number_dict[cur_run])
    pulser_missing_number_dict[cur_run] = RemoveMissRecons(pulser_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_pulser = Nmis_pulser + len( pulser_missing_number_dict[cur_run])
    pulser_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "pulser_dst", cur_run)
    pulser_dst_missing_number_dict[cur_run] = getMissing( pulser_dst_number_dict[cur_run], raw_number_dict[cur_run])
    pulser_dst_missing_number_dict[cur_run] = RemoveMissRecons(pulser_dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_dst_pulser = Nmis_dst_pulser + len( pulser_dst_missing_number_dict[cur_run])

    s0_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "s0", cur_run)
    s0_missing_number_dict[cur_run] = getMissing( s0_number_dict[cur_run], raw_number_dict[cur_run])
    s0_missing_number_dict[cur_run] = RemoveMissRecons(s0_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_s0 = Nmis_s0 + len( s0_missing_number_dict[cur_run])
    s0_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "s0_dst", cur_run)
    s0_dst_missing_number_dict[cur_run] = getMissing( s0_dst_number_dict[cur_run], raw_number_dict[cur_run])
    s0_dst_missing_number_dict[cur_run] = RemoveMissRecons(s0_dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_dst_s0 = Nmis_dst_s0 + len( s0_dst_missing_number_dict[cur_run])

    p0_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "p0", cur_run)
    p0_missing_number_dict[cur_run] = getMissing( p0_number_dict[cur_run], raw_number_dict[cur_run])
    p0_missing_number_dict[cur_run] = RemoveMissRecons(p0_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_p0 = Nmis_p0 + len( p0_missing_number_dict[cur_run])
    p0_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "p0_dst", cur_run)
    p0_dst_missing_number_dict[cur_run] = getMissing( p0_dst_number_dict[cur_run], raw_number_dict[cur_run])
    p0_dst_missing_number_dict[cur_run] = RemoveMissRecons(p0_dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_dst_p0 = Nmis_dst_p0 + len( p0_dst_missing_number_dict[cur_run])

#    s0_missing_number_dict[cur_run] = RemoveMissRecons(s0_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
#    s0_miss_filenos = getListAsOneString(s0_missing_number_dict[cur_run])

    trigger_skim_missing_dict[cur_run] = getCombined(pulser_missing_number_dict[cur_run], pulser_dst_missing_number_dict[cur_run])
    trigger_skim_missing_dict[cur_run] = getCombined(trigger_skim_missing_dict[cur_run], s0_missing_number_dict[cur_run])
    trigger_skim_missing_dict[cur_run] = getCombined(trigger_skim_missing_dict[cur_run], s0_dst_missing_number_dict[cur_run])
    trigger_skim_missing_dict[cur_run] = getCombined(trigger_skim_missing_dict[cur_run], p0_missing_number_dict[cur_run])
    trigger_skim_missing_dict[cur_run] = getCombined(trigger_skim_missing_dict[cur_run], p0_dst_missing_number_dict[cur_run])

    trigger_skim_missing_dict[cur_run] = RemoveMissRecons(trigger_skim_missing_dict[cur_run], recon_missing_number_dict[cur_run])
    trigger_skim_filenos = getListAsOneString(trigger_skim_missing_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, trigger_skim_filenos, "TriggerSkim")
    print trigger_skim_filenos


    # ================= Physics skims, this include fee, Moller and v0 with thir DSTs ================
    fee_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "fee", cur_run)
    fee_missing_number_dict[cur_run] = getMissing( fee_number_dict[cur_run], raw_number_dict[cur_run])
    fee_missing_number_dict[cur_run] = RemoveMissRecons(fee_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_fee = Nmis_fee + len( fee_missing_number_dict[cur_run])
    fee_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "fee_dst", cur_run)
    fee_dst_missing_number_dict[cur_run] = getMissing(fee_dst_number_dict[cur_run], raw_number_dict[cur_run])
    fee_dst_missing_number_dict[cur_run] = RemoveMissRecons(fee_dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_dst_fee = Nmis_dst_fee + len( fee_dst_missing_number_dict[cur_run])

    moller_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "moller", cur_run)
    moller_missing_number_dict[cur_run] = getMissing( moller_number_dict[cur_run], raw_number_dict[cur_run])
    moller_missing_number_dict[cur_run] = RemoveMissRecons(moller_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_Moller = Nmis_Moller + len( moller_missing_number_dict[cur_run])
    moller_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "moller_dst", cur_run)
    moller_dst_missing_number_dict[cur_run] = getMissing( moller_dst_number_dict[cur_run], raw_number_dict[cur_run])
    moller_dst_missing_number_dict[cur_run] = RemoveMissRecons(moller_dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    Nmis_dst_Moller = Nmis_dst_Moller + len( moller_dst_missing_number_dict[cur_run])

    # ==== in a tweakpass6 we will not use v0 skim ===
#    v0_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "v0", cur_run)
#    v0_missing_number_dict[cur_run] = getMissing( v0_number_dict[cur_run], raw_number_dict[cur_run])
#    v0_missing_number_dict[cur_run] = RemoveMissRecons(v0_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
#    Nmis_v0 = Nmis_v0 + len( v0_missing_number_dict[cur_run])
#    v0_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "v0_dst", cur_run)
#    v0_dst_missing_number_dict[cur_run] = getMissing( v0_dst_number_dict[cur_run], raw_number_dict[cur_run])
#    v0_dst_missing_number_dict[cur_run] = RemoveMissRecons(v0_dst_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
#    Nmis_dst_v0 = Nmis_dst_v0 + len( v0_dst_missing_number_dict[cur_run])
#
    
    phys_skim_missing_dict[cur_run] = getCombined(fee_missing_number_dict[cur_run], fee_dst_missing_number_dict[cur_run])
    phys_skim_missing_dict[cur_run] = getCombined(phys_skim_missing_dict[cur_run], moller_missing_number_dict[cur_run])
    phys_skim_missing_dict[cur_run] = getCombined(phys_skim_missing_dict[cur_run], moller_dst_missing_number_dict[cur_run])
#    phys_skim_missing_dict[cur_run] = getCombined(phys_skim_missing_dict[cur_run], v0_missing_number_dict[cur_run])
#    phys_skim_missing_dict[cur_run] = getCombined(phys_skim_missing_dict[cur_run], v0_dst_missing_number_dict[cur_run])
    
    phys_skim_missing_dict[cur_run] = RemoveMissRecons(phys_skim_missing_dict[cur_run], recon_missing_number_dict[cur_run])
    phys_skim_filenos = getListAsOneString(phys_skim_missing_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, phys_skim_filenos, "PhysicsSkim")
    print phys_skim_filenos
    
   
    # ================= v0pulser ================
#    v0pulser_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "v0pulser", cur_run, False) # "False" means the file number list will be taken from disk, instead of th tape
#    v0pulser_missing_number_dict[cur_run] = getMissing( v0pulser_number_dict[cur_run], raw_number_dict[cur_run])
#    v0pulser_missing_number_dict[cur_run] = RemoveMissRecons(v0pulser_missing_number_dict[cur_run], pulser_missing_number_dict[cur_run]) # Note: here it removes files, that have missing pulser, instead of usuall missing recon files
#
#    Nmis_v0pulser = Nmis_v0pulser + len(v0pulser_missing_number_dict[cur_run])
#    v0pulser_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "v0pulser_dst", cur_run, False) # "False" means the file number list will be taken from disk, instead of th tape
#    v0pulser_dst_missing_number_dict[cur_run] = getMissing( v0pulser_dst_number_dict[cur_run], raw_number_dict[cur_run])
#    v0pulser_dst_missing_number_dict[cur_run] = RemoveMissRecons(v0pulser_dst_missing_number_dict[cur_run], pulser_missing_number_dict[cur_run])
#    Nmis_dst_v0pulser = Nmis_dst_v0pulser + len(v0pulser_dst_missing_number_dict[cur_run])
#    v0pulser_missing_number_dict[cur_run] = getCombined(v0pulser_missing_number_dict[cur_run], v0pulser_dst_missing_number_dict[cur_run])
#    #=============== At the end we remove files from the list, that have missing recons and missing in normal v0 skim, since we know already these files have problems
#    v0pulser_missing_number_dict[cur_run] = RemoveMissRecons(v0pulser_missing_number_dict[cur_run], v0_missing_number_dict[cur_run])
#    v0pulser_missing_number_dict[cur_run] = RemoveMissRecons(v0pulser_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
#
#    v0pulser_miss_filenos = getListAsOneString(v0pulser_missing_number_dict[cur_run])
#    mkjsubs.Remkjsub(cur_run, v0pulser_miss_filenos, "v0pulser")
#    print v0pulser_missing_number_dict[cur_run]
#
 
    nt_tri_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "nt_tri", cur_run)
    nt_tri_missing_number_dict[cur_run] = getMissing( nt_tri_number_dict[cur_run], raw_number_dict[cur_run])
    nt_tri_missing_number_dict[cur_run] = RemoveMissRecons(nt_tri_missing_number_dict[cur_run], recon_missing_number_dict[cur_run] )
    Nmis_nt_tri = Nmis_nt_tri + len(nt_tri_missing_number_dict[cur_run])

    nt_fee_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "nt_fee", cur_run)
    nt_fee_missing_number_dict[cur_run] = getMissing( nt_fee_number_dict[cur_run], raw_number_dict[cur_run])
    nt_fee_missing_number_dict[cur_run] = RemoveMissRecons(nt_fee_missing_number_dict[cur_run], recon_missing_number_dict[cur_run] )
    Nmis_nt_fee = Nmis_nt_fee + len(nt_fee_missing_number_dict[cur_run])

    nt_moller_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "nt_moller", cur_run)
    nt_moller_missing_number_dict[cur_run] = getMissing( nt_moller_number_dict[cur_run], raw_number_dict[cur_run])
    nt_moller_missing_number_dict[cur_run] = RemoveMissRecons(nt_moller_missing_number_dict[cur_run], recon_missing_number_dict[cur_run] )
    Nmis_nt_moller = Nmis_nt_moller + len(nt_moller_missing_number_dict[cur_run])

    nt_all_missing_number_dict[cur_run] = getCombined(nt_tri_missing_number_dict[cur_run], nt_fee_missing_number_dict[cur_run])
    nt_all_missing_number_dict[cur_run] = getCombined(nt_all_missing_number_dict[cur_run], nt_moller_missing_number_dict[cur_run])
    nt_all_missing_number_dict[cur_run] = RemoveMissRecons(nt_all_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
    nt_skim_file_nos = getListAsOneString(nt_all_missing_number_dict[cur_run])

    mkjsubs.Remkjsub(cur_run, nt_skim_file_nos, "ntuple2")

    print >>f_miss_stats, cur_run, len(raw_number_dict[cur_run]), len( recon_missing_number_dict[cur_run]), len( dst_missing_number_dict[cur_run]), len( dqm_missing_number_dict[cur_run]), \
            len( pulser_missing_number_dict[cur_run]), len( pulser_dst_missing_number_dict[cur_run]), len( s0_missing_number_dict[cur_run]), len( s0_dst_missing_number_dict[cur_run]), \
            len( p0_missing_number_dict[cur_run]), len( p0_dst_missing_number_dict[cur_run]), len( fee_missing_number_dict[cur_run]), len( fee_dst_missing_number_dict[cur_run]), \
            len( moller_missing_number_dict[cur_run]), len( moller_dst_missing_number_dict[cur_run]), len(nt_tri_missing_number_dict[cur_run]), len(nt_fee_missing_number_dict[cur_run]), \
            len(nt_moller_missing_number_dict[cur_run])
#, len( v0_missing_number_dict[cur_run]), len( v0_dst_missing_number_dict[cur_run])


f_summary = open('lists/summary_stats.dat', 'w')
print >>f_summary, "====================== Summary of Missing files ======================"
    
print >>f_summary, "Number of Missing Recons             ", Nmis_recon
print >>f_summary, "Number of Missing DSts               ", Nmis_dst
print >>f_summary, "Number of Missing DQMs               ", Nmis_dqm
print >>f_summary, "Number of Missing pulsers            ", Nmis_pulser
print >>f_summary, "Number of Missing pulser DSts        ", Nmis_dst_pulser
print >>f_summary, "Number of Missing s0s                ", Nmis_s0
print >>f_summary, "Number of Missing s0 DSTs            ", Nmis_dst_s0
print >>f_summary, "Number of Missing p0s                ", Nmis_p0
print >>f_summary, "Number of Missing p0 DSTs            ", Nmis_dst_p0
print >>f_summary, "Number of Missing fees               " ,Nmis_fee
print >>f_summary, "Number of Missing fee DSTs           ", Nmis_dst_fee
print >>f_summary, "Number of Missing Mollers            ", Nmis_Moller
print >>f_summary, "Number of Missing Moller DSTs        ", Nmis_dst_Moller
print >>f_summary, "Number of Missing V0s                ", Nmis_v0
#print >>f_summary, "Number of Missing V0 DSTs            ", Nmis_dst_v0
print >>f_summary, "Number of Missing V0pulser           ", Nmis_v0pulser
print >>f_summary, "Number of Missing V0pulser_dst       ", Nmis_dst_v0pulser
