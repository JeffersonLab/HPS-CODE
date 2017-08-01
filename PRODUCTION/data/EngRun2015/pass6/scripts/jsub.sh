#!/bin/sh

function jsub1
{
    if [ -e jsubs/$1 ]
    then
        echo Submitting jsubs/$1
        jsub -xml jsubs/$1
        mv -f jsubs/$1 jsubs-subbed
    fi
}

mkdir -p jsubs-subbed

# 0 arguments (all jsubs):
if [ -z "$1" ]
then
    for xml in jsubs/*.xml
    do
        jsub1 ${xml#*/}
    done

# 1 argument (single run, or file containing list of runs):
elif [ -z "$2" ]
then
    if [ -e "$1" ]
    then
        for rr in `cat "$1"`
        do
            jsub1 $rr.xml
        done
    else
        jsub1 $1.xml
    fi
   
# 2 arguments (run range):
elif [ -z "$3" ]
then
    for rr in `seq $1 $2`
    do
        jsub1 $rr.xml
    done

# 3 or more args (run list):
else
    for rr in $@
    do
        jsub1 $rr.xml
    done
fi

