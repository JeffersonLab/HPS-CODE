#!/bin/sh

# creates all the subdirectories for pass outputs in .
# used by xml template so don't have to do it manually

pass=$1

dirs=(\
logs \
recon \
dst \
data_quality/dqm \
data_quality/recon \
skim/pulser \
skim/fee \
skim/moller \
skim/v0 \
skim/p0 \
skim/s0 \
skim/dst/pulser \
skim/dst/fee \
skim/dst/moller \
skim/dst/v0 \
skim/dst/p0 \
skim/dst/s0 \
)

for dd in ${dirs[@]};
do
  mkdir -p $pass/$dd
  mkdir -p $pass'fail'/$dd
done

