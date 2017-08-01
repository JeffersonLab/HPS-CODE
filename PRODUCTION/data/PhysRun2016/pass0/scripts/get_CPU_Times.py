import os,re,sys,glob

#timeouts_fname = sys.argv[1];
#### The 1st argument is the directory where log files are
#### The 2nd argument is the category of Jobs, e.g. recon, DST, TriggerSkim etc
logdir = sys.argv[1];
category = sys.argv[2];
#logdir = '/lustre/expphy/work/hallb/hps/data/engrun2015/pass6/1stSubmission_Farmouts/'

f1 = open ('job_time_statistscs_'+str(category)+'.dat', 'w+')

log_out_files = glob.glob(logdir+'/'+'*'+category+'*.out')

print log_out_files

for cur_file in log_out_files:

    for line in open(cur_file, 'r').readlines():
        if 'cput' in line:
#            print line
            time = line.split(":")
            cphour = time[0]
            cphour = cphour.replace('cput=', '')
#            print "hour = ", hour
            cpminute = time[1]
            duration = float(cphour) +float(int(cpminute))/float(60)
#            print "CPUT = ", duration, " h"
            midpart = time[2]
            walltime_hour = midpart.split('walltime=')
            whour = float(walltime_hour[1])
            wminute = float(time[3])
            wallduration = whour + wminute/60. 
        elif '/bin/ln -s ' in line and 'evio' in line:
            line = line.replace('\n', '')
#            print line
            file_num = line.split('.evio.')
            part1 = file_num[0].split('hps_00')
            runNo = part1[1];
            part2 = file_num[1].split(' ')
            fileNo = part2[0]
#                print "filenuber is " + file_num[1]
        elif  '/bin/ln -s ' in line and 'slcio' in line:
            line = line.replace('\n', '')
 #           print line
            file_num = line.split('.')
            part1 = file_num[0].split('hps_00')
            runNo = part1[1];
            part2 = file_num[1].split('_')
            fileNo = part2[0]
   
    print >>f1, runNo, fileNo, wallduration, duration
