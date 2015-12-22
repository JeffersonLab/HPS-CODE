#!/bin/sh

function jsub1
{
    if [ -e jsubs/$1.xml ]
    then
        jsub -xml jsubs/$1.xml
        mv -f jsubs/$1.xml jsubs-subbed
    fi
}

if [ -z "$1" ]; then
    echo 'Usage1: jsub.sh rstart rend'
    echo 'Usage2: jsub.sh r1 r2 r3 [r4 [...]]'
    echo 'Usage3: jsub.sh r'
    exit
fi

if [ -z "$2" ]
then
    jsub1 $1
    
elif [ -z "$3" ]
then
    for rr in `seq $1 $2`
    do
        jsub1 $rr
    done
else
    for rr in $@
    do
        jsub1 $rr
    done
fi

