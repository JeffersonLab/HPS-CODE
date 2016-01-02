#!/bin/sh

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

tapeDir=/mss/hallb/hps/engrun2015/$pass

for xx in `find $tapeDir/$1`
do
    run=`echo $xx | sed 's/.*hps[ecal]*_00\([0-9]*\)\..*/\1/'`
    fil=`echo $xx | sed 's/.*hps[ecal]*_00[0-9]*\.\([0-9]*\).*/\1/'`
    siz=`grep 'size=' $xx | sed 's/size=//'`
    echo $xx $run $fil $siz
done

