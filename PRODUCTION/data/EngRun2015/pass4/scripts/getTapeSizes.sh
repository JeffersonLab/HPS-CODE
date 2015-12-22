#!/bin/sh

dir=/mss/hallb/hps/engrun2015/pass4

for xx in `find $dir/$1`
do

    run=`echo $xx | sed 's/.*hps[ecal]*_00\([0-9]*\)\..*/\1/'`
    fil=`echo $xx | sed 's/.*hps[ecal]*_00[0-9]*\.\([0-9]*\).*/\1/'`
    siz=`grep 'size=' $xx | sed 's/size=//'`

    echo $xx $run $fil $siz

done

