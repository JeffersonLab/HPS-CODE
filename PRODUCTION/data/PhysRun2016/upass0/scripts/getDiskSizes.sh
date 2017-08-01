#!/bin/sh

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

dir=/work/hallb/hps/data/engrun2015/$pass

for xx in $dir/skim/dst/*
do
    ls -l $xx > $xx.list
done

for xx in $dir/skim/*
do
    ls -l $xx > $xx.list
done

