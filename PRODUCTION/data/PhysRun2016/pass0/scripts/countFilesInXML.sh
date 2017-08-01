#!/bin/sh

jsubdir=$1

for xx in $jsubdir/*
do 
    run=${xx%.*}
    run=${run#*/} 
    echo -n "$run "
    grep 'List name="fnum"' $xx | sed 's/.*">//' | sed 's/<.*//'
done

