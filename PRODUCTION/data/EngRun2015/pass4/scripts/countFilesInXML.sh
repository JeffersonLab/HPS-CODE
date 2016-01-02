#!/bin/sh

# parse the xml submission scripts, and print:
# runno filno1 filno2 filno3 ....

jsubdir=$1

for xx in $jsubdir/*
do 
    run=${xx%.*}
    run=${run#*/} 
    echo -n "$run "
    grep 'List name="fnum"' $xx | sed 's/.*">//' | sed 's/<.*//'
done

