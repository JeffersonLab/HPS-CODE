#!/bin/sh

pass=$1

dirs=(\
logs \
skim/pulser \
skim/fee \
skim/p0 \
skim/s0 \
skim/dst/pulser \
skim/dst/fee \
skim/dst/p0 \
skim/dst/s0 \
)

for dd in ${dirs[@]};
do
  mkdir -p $pass/$dd
  mkdir -p $pass'fail'/$dd
done

