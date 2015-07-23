#!/bin/sh
if [ -z "$1" ]; then
    echo Usage:  listfiles passN
    exit
fi
dir=/u/group/hps/production/data/EngRun2015/lists
rm -f $dir/disk_$1.txt $dir/tape_$1.txt
find /mss/hallb/hps/engrun2015/$1 > $dir/tape_$1.txt
find /work/hallb/hps/data/engrun2015/$1 > $dir/disk_$1.txt

