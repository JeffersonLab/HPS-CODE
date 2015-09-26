#!/bin/sh
if [ -z "$1" ] || [ -z "$2" ]; then
    echo Usage: jsub.sh r1 r2
    exit
fi
for rr in `seq $1 $2`;
do
    if ! [ -e jsubs/$rr.xml ]; then
        continue
    fi
    jsub -xml jsubs/$rr.xml
    mv jsubs/$rr.xml jsubs-subbed
done

