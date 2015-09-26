#!/bin/sh

#dir=/mss/hallb/hps/engrun2015/pass2
dir=/work/hallb/hps/data/engrun2015/pass2
dir2=/work/hallb/hps/data/engrun2015/pass2fail

for xx in `grep \ 24981$ tape_dst.list | awk '{print$1"-"$2"-"$3}'`
do

    dst=`   echo $xx | awk -F- '{print $1}'`
    runfil=`echo $xx | awk -F- '{print $2"."$3}'`

    out=$dir/logs/hps_00$runfil\_R340.out
    err=$dir/logs/hps_00$runfil\_R340.err
    out2=$dir2/logs/hps_00$runfil\_R340.out
    err2=$dir2/logs/hps_00$runfil\_R340.err
    dst=$dir/recon/hps_00$runfil\_dst_R340.root
    recon=$dir/recon/hps_00$runfil\_recon_R340.slcio
    moller=$dir/skim/moller/hps_00$runfil\_moller_R340.slcio
    pulser=$dir/skim/pulser/hps_00$runfil\_pulser_R340.slcio

#    echo $recon

#    grep $recon tape_recon.list

#    echo $dst $recon

#    more $dst

#    echo jremove $dst >> rm_dst.txt

#    ls $pulser
#    ls $moller
#    ls $dst

    f=$out
    
    echo $f
    if [ -e "$f" ]
    then
        ls -l $f
        #more $f
        #rm -f $f
    fi

    if [ -e "$err" ]
    then
        mv -f $err $err2
    fi

done

