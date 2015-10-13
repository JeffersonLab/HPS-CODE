#!/usr/local/bin/perl

print "submitting jobs...";
`rm data.log; bsub -q long -o data.log root -l -b -q runAnalysis.cc\\\(1\\\)`;
`rm  tritrig-beam-tri.log;bsub -q long -o tritrig-beam-tri.log root -l -b -q runAnalysis.cc\\\(2\\\)`;
`rm  tritrig.log; bsub -q long -o tritrig.log root -l -b -q runAnalysis.cc\\\(3\\\)`;
`rm  beam-tri.log; bsub -q long -o beam-tri.log root -l -b -q runAnalysis.cc\\\(4\\\)`;
print "done";
