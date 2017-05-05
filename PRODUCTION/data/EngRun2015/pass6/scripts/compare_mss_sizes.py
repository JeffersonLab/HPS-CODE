#!/usr/bin/env python
import os,re,sys,glob

def getReconSizeList(path, run):
    file_pattern = path+"/*"+"00"+str(run)+"*"
    files = glob.glob(file_pattern)
    
    fout = open('recon_mss_size'+str(run)+'.dat', 'w');

    for cur_file in files:
        ffile = open(cur_file, 'r');
        file_number = cur_file.split(str(run)+'.')
        file_number = file_number[1].split('_recon')
        
        for cur_line in ffile.readlines():
            if cur_line.find("ize=")>0:
                cur_line = cur_line.replace('size=', '')
                cur_line = cur_line.replace('\n', '')
                print >> fout, file_number[0], cur_line

def getReconFileSize(passn, run, filenum):
    file_pattern  = "/mss/hallb/hps/engrun2015/"+passn+"/recon/hps_00"+str(run)+"."+str(filenum)+"_recon*.slcio"
    file_path = glob.glob(file_pattern)
    #print file_path[0]
    if not os.path.exists(file_path[0]): sys.exit('Kuku2 File '+file_path)+'doesnt exist'
    
    ffile = open(file_path[0], 'r');
    for cur_line in ffile.readlines():
        if cur_line.find("ize=")>0:
            cur_line = cur_line.replace('size=', '')
            cur_line = cur_line.replace('\n', '')
            #print "File size is "+cur_line
            return int(cur_line)



def getRawSizeList(run):
    file_pattern = "/mss/hallb/hps/data/*"+str(run)+"*"

    files = glob.glob(file_pattern)
    
    fout = open('Raw_mss_size'+str(run)+'.dat', 'w');

    for cur_file in files:
        ffile = open(cur_file, 'r');
        file_number = cur_file.split('evio.')
        
        for cur_line in ffile.readlines():
            if cur_line.find("ize=")>0:
                cur_line = cur_line.replace('size=', '')
                cur_line = cur_line.replace('\n', '')
                print >> fout, file_number[1], cur_line

run = 5797
mss_recon_parh = "/mss/hallb/hps/engrun2015/pass6/recon/"

getReconSizeList(mss_recon_parh, run)
getRawSizeList(run)


getReconFileSize("pass6", 5772, 15)
