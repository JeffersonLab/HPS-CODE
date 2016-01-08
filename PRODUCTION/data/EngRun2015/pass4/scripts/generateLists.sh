#!/bin/sh

# generate lists in ./lists of existing reconstructed files on tape and disk
# outputs used by mkjsub.py to determine what needs to be submitted

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

dir=/u/group/hps/production/data/EngRun2015/$pass/lists
mkdir -p $dir

rm -f $dir/disk_$pass.txt $dir/tape_$pass.txt
touch $dir/disk_$pass.txt $dir/tape_$pass.txt

find /mss/hallb/hps/engrun2015/$pass > $dir/tape_$pass.txt
find /work/hallb/hps/data/engrun2015/$pass > $dir/disk_$pass.txt

