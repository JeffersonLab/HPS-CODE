#!/bin/sh

function jsub1
{
    if [ -e jsubs/$1.xml ]
    then
        jsub -xml jsubs/$1.xml
        mv -f jsubs/$1.xml jsubs-subbed
    fi
}

if [ -z "$1" ] || [ -z "$2" ]; then
    echo 'Usage: jsub.sh r1/start r2/end [r3 [r4 [...]]]'
    exit
fi

if [ -z "$3" ]
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

