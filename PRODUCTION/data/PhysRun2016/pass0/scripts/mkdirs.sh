#!/bin/sh

pass=$1

dirs=(\
logs \
recon \
dst \
ntuple \
ntuple/fee \
ntuple/moller \
ntuple/tri \
data_quality/dqm \
data_quality/recon \
skim/pulser \
skim/fee \
skim/moller \
skim/v0 \
skim/s0 \
skim/dst/pulser \
skim/dst/fee \
skim/dst/moller \
skim/dst/v0 \
skim/dst/s0 \
)

for dd in ${dirs[@]};
do
  mkdir -p $pass/$dd
  mkdir -p $pass'fail'/$dd
done

