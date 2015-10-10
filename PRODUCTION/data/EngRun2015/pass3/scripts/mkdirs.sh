#!/bin/sh
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
skim/dst/pulser \
skim/dst/fee \
skim/dst/moller \
skim/dst/v0 \
)

for dd in ${dirs[@]};
do
  mkdir -p $1/$dd
  mkdir -p $1'fail'/$dd
done

