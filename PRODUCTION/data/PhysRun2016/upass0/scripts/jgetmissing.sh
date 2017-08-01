#!/bin/sh

scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pass=`echo $scriptDir | awk -F/ '{print$(NF-1)}'`

tdir=/mss/hallb/hps/engrun2015/$pass
ddir=/work/hallb/hps/data/engrun2015/$pass

nn=0
tt2dd=''

for xx in dst skim/moller skim/fee skim/v0 skim/pulser skim/dst/moller skim/dst/fee skim/dst/v0 skim/dst/pulser
do
  echo
  echo cd $ddir/$xx
  for tt in $tdir/$xx/*
  do
    dd=$ddir/$xx/`basename $tt`
    if [ ! -e $dd ]; then
      tt2dd=$tt2dd' '$tt
      let nn=nn+1
      if [ $nn -ge 50 ]
      then
        echo jget $tt2dd .
        let nn=0
        tt2dd=''
      fi   
    fi
  done
  echo jget $tt2dd .
  let nn=0
  tt2dd=''
done

