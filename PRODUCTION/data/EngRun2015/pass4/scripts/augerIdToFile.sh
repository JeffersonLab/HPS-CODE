#!/bin/sh

for xx in /work/hallb/hps/data/engrun2015/pass4/logs/*.out
do
    runfil=`echo $xx | awk -F_ '{print$2}'`
    run=${runfil%.*}
    run=${run#0}
    run=${run#0}
    fil=${runfil#*.}
    aug=`grep -m 1 Auger $xx | awk '{print$3}'`
    printf "%4d %3d %10d\n" $run $fil $aug
done
