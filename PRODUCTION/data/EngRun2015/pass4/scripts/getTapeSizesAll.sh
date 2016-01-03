#!/bin/sh

# wrapper to getTapeSizes.sh for all output subdirs

for xx in \
    recon \
    dst \
    skim/fee \
    skim/moller \
    skim/p0 \
    skim/pulser \
    skim/s0 \
    skim/v0 \
    skim/dst/fee \
    skim/dst/moller \
    skim/dst/p0 \
    skim/dst/pulser \
    skim/dst/s0 \
    skim/dst/v0
do
    ofile=tape_${xx//\//-}.list
    ./scripts/getTapeSizes.sh $xx > $ofile
done

