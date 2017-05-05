#!/usr/bin/env python
import os,re,sys,glob
sys.path.insert(0, 'scripts')
import compare_mss_sizes
import mkjsubs

global blinded

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
        if blinded and int(file_number[1])%10 > 0: continue
        fileNumberList.append(file_number[1]);
    return fileNumberList


def getReconFileNumbersOfRun(passn , RunNo):
    # This will look into the "/mss/hallb/hps/engrun2015/passn/recon directory, and for
    # run "RunNo" make a list that contains all recon file numbers for that run
    fileNumberList = []
    file_pattern = "/mss/hallb/hps/physrun2016/"+str(passn)+"/recon/hps_00"+str(RunNo)+"*"

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
        if blinded and int(file_number[0])%10 > 0: continue
        fileNumberList.append(file_number[0]);

    return fileNumberList


def getCategorizedFileNumbersOfRun(passn, category, RunNo):
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


    fileNumberList = []
    file_pattern = "/mss/hallb/hps/physrun2016/"+str(passn)+stub+"/hps_00"+str(RunNo)+"*"

    files = glob.glob(file_pattern)
    print "Determining Recon file numbers " + file_pattern

   # print files

    for cur_file in files:
        file_number = cur_file.split(str(RunNo)+'.')
        file_number = file_number[1].split('_'+run_type)
        if blinded and int(file_number[0])%10 > 0: continue
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


PASS = "upass0"
#blinded = True
blinded_pass = False
blinded = False

unblinded_list = [7804, 7808, 7809, 8054]

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
pulser_skim_missing_dict = dict()

s0_number_dict = dict()
s0_missing_number_dict = dict()
s0_dst_number_dict = dict()
s0_dst_missing_number_dict = dict()
s0_skim_missing_dict = dict()

p0_number_dict = dict()
p0_missing_number_dict = dict()
p0_dst_number_dict = dict()
p0_dst_missing_number_dict = dict()
p0_skim_missing_dict = dict()

fee_number_dict = dict()
fee_missing_number_dict = dict()
fee_dst_number_dict = dict()
fee_dst_missing_number_dict = dict()
fee_skim_missing_dict = dict()

moller_number_dict = dict()
moller_missing_number_dict = dict()
moller_dst_number_dict = dict()
moller_dst_missing_number_dict = dict()
v0_number_dict = dict()
v0_missing_number_dict = dict()
v0_dst_number_dict = dict()
v0_dst_missing_number_dict = dict()
phys_skim_missing_dict = dict()

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


#f_runs = open("lists/test_list.dat", 'r')
#f_runs = open("lists/runs_2015_0p5mm.dat", 'r')
#f_runs = open("lists/goldenRunListSorted.txt", 'r')
f_runs = open("lists/Prod_list.dat", 'r')
#f_runs = open("lists/testlist.dat", 'r')
#f_runs = open("lists/StrightTracks.dat", 'r')

f_miss_stats = open('lists/failure_stats', 'w')

for cur_run in f_runs.readlines():
    cur_run = cur_run.replace('\n', '')
    print "cur run is " + cur_run

    if int(cur_run) in unblinded_list: blinded = False
    else: blinded = blinded_pass

    raw_number_dict[cur_run] = getFileNumbersOfRun(cur_run)
    
#    recon_miss_filenos = ''
#    for cur_fileno in recon_missing_number_dict[cur_run]:
#        recon_miss_filenos = recon_miss_filenos + ' ' + cur_fileno


    # ================= Pulser Skim their DSTs ================
    pulser_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "pulser", cur_run)
    pulser_missing_number_dict[cur_run] = getMissing( pulser_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_pulser = Nmis_pulser + len( pulser_missing_number_dict[cur_run])
    pulser_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "pulser_dst", cur_run)
    pulser_dst_missing_number_dict[cur_run] = getMissing( pulser_dst_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_dst_pulser = Nmis_dst_pulser + len( pulser_dst_missing_number_dict[cur_run])

#    s0_missing_number_dict[cur_run] = RemoveMissRecons(s0_missing_number_dict[cur_run], recon_missing_number_dict[cur_run])
#    s0_miss_filenos = getListAsOneString(s0_missing_number_dict[cur_run])

    pulser_skim_missing_dict[cur_run] = getCombined(pulser_missing_number_dict[cur_run], pulser_dst_missing_number_dict[cur_run])
    pulser_skim_filenos = getListAsOneString(pulser_skim_missing_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, pulser_skim_filenos, "pulser")
    print pulser_skim_filenos

    # ================= Single0 Skim with their DSTs ================
    s0_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "s0", cur_run)
    s0_missing_number_dict[cur_run] = getMissing( s0_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_s0 = Nmis_s0 + len( s0_missing_number_dict[cur_run])
    s0_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "s0_dst", cur_run)
    s0_dst_missing_number_dict[cur_run] = getMissing( s0_dst_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_dst_s0 = Nmis_dst_s0 + len( s0_dst_missing_number_dict[cur_run])

    s0_skim_missing_dict[cur_run] = getCombined(s0_missing_number_dict[cur_run], s0_dst_missing_number_dict[cur_run])
    s0_skim_filenos = getListAsOneString(s0_skim_missing_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, s0_skim_filenos, "s0")

    # ================= Single1 Skim with their DSTs ================
    fee_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "fee", cur_run)
    fee_missing_number_dict[cur_run] = getMissing( fee_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_fee = Nmis_fee + len( fee_missing_number_dict[cur_run])
    fee_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "fee_dst", cur_run)
    fee_dst_missing_number_dict[cur_run] = getMissing( fee_dst_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_dst_fee = Nmis_dst_fee + len( fee_dst_missing_number_dict[cur_run])

    fee_skim_missing_dict[cur_run] = getCombined(fee_missing_number_dict[cur_run], fee_dst_missing_number_dict[cur_run])
    fee_skim_filenos = getListAsOneString(fee_skim_missing_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, fee_skim_filenos, "fee")
    
    # ================= Pair0 Skim with their DSTs ================
    p0_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "p0", cur_run)
    p0_missing_number_dict[cur_run] = getMissing( p0_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_p0 = Nmis_p0 + len( p0_missing_number_dict[cur_run])
    p0_dst_number_dict[cur_run] = getCategorizedFileNumbersOfRun(PASS, "p0_dst", cur_run)
    p0_dst_missing_number_dict[cur_run] = getMissing( p0_dst_number_dict[cur_run], raw_number_dict[cur_run])
    Nmis_dst_p0 = Nmis_dst_p0 + len( p0_dst_missing_number_dict[cur_run])

    p0_skim_missing_dict[cur_run] = getCombined(p0_missing_number_dict[cur_run], p0_dst_missing_number_dict[cur_run])
    p0_skim_filenos = getListAsOneString(p0_skim_missing_dict[cur_run])
    mkjsubs.Remkjsub(cur_run, p0_skim_filenos, "p0")

    if int(cur_run) in mkjsubs.IGNORERUNS: continue
    else:
        print >>f_miss_stats, cur_run, len(raw_number_dict[cur_run]), len( pulser_missing_number_dict[cur_run]), len( pulser_dst_missing_number_dict[cur_run]), \
            len( s0_missing_number_dict[cur_run]), len( s0_dst_missing_number_dict[cur_run]), \
            len( fee_missing_number_dict[cur_run]), len( fee_dst_missing_number_dict[cur_run]), \
            len( p0_missing_number_dict[cur_run]), len( p0_dst_missing_number_dict[cur_run]), \

f_summary = open('lists/summary_stats.dat', 'w')
print >>f_summary, "====================== Summary of Missing files ======================"

print >>f_summary, "Number of Missing pulsers            ", Nmis_pulser
print >>f_summary, "Number of Missing pulser DSts        ", Nmis_dst_pulser
print >>f_summary, "Number of Missing s0s                ", Nmis_s0
print >>f_summary, "Number of Missing s0 DSTs            ", Nmis_dst_s0
print >>f_summary, "Number of Missing p0s                ", Nmis_p0
print >>f_summary, "Number of Missing p0 DSTs            ", Nmis_dst_p0
print >>f_summary, "Number of Missing fees               " ,Nmis_fee
print >>f_summary, "Number of Missing fee DSTs           ", Nmis_dst_fee
