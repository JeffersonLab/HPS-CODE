#!/bin/sh
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

dir=/u/group/hps/production/data/EngRun2015/$pass/lists
rm -f $dir/disk_$pass.txt $dir/tape_$pass.txt
touch $dir/disk_$pass.txt $dir/tape_$pass.txt
find /mss/hallb/hps/physrun2016/$pass > $dir/tape_$pass.txt
find /work/hallb/hps/data/physrun2016/$pass > $dir/disk_$pass.txt

