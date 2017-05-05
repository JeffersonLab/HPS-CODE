import sys
import shutil
import re
import string
import os
from subprocess import Popen, PIPE

####
if len(sys.argv) != 5:  #remember, the script name counts as an argument!
    print 'runjob.py <xml template> <runtype> <run number> <fileNumber>'
    print '<runtype> can be eviotolcio, recon, dqm, dst'
    sys.exit()
####

xmlfile=sys.argv[1]
runtype=sys.argv[2]
run=sys.argv[3]
nums=sys.argv[4]

#get the missing jobs
#cmd ='./getfilenumbers.sh ' +runtype +' '+str(run)
#print cmd
#p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
#nums=p.stdout.readline()
#nums = "0"
print nums
sys.stdout.flush()
if nums == "foobar" : 
    print "Nothing to run"
    sys.stdout.flush()
    sys.exit()
####
#parse the xml template

tmpfile = 'temp.xml'
shutil.copy(xmlfile, tmpfile)

with open(tmpfile,"r") as tmp:
    lines = tmp.readlines()

with open(tmpfile,"w") as tmp:
    for line in lines:
        if re.search("List .*\"filenum\"", line) != None:
            line=line.replace("666",str(nums))
            print line.rstrip()
        if re.search("Variable .*\"run\"", line) != None:
            line=line.replace("666",str(run))
            print line.rstrip()
        tmp.write(line)
     
os.system("jsub -xml temp.xml")


