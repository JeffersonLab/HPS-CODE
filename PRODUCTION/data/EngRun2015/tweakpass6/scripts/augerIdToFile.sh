#!/bin/sh

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

for xx in /work/hallb/hps/data/engrun2015/$pass$1/logs/*.out.gz
do
#    echo $xx
    runfil=`echo $xx | awk -F_ '{print$2}'`
    run=${runfil%.*}
    run=${run#0}
    run=${run#0}
    fil=${runfil#*.}
    aug=`gunzip -c $xx | grep -m 1 Auger | awk '{print$2}'`
    #aug=`grep -m 1 Auger $xx | awk '{print$2}'`
    printf "%4d %3d %10d\n" $run $fil $aug
done
