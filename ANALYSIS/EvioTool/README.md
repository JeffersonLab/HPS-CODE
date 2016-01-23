EvioTool
========
Author: Maurik Holtrop @ UNH  5/7/14

A tool for ROOT users to read EVIO raw data from a file or from the ET ring.

This is a work in progress. It started as a test for making sure I could read data from the ET ring at 
high speeds (>50 kHz) in a single thread. I hope to turn it into a more generally useful tool.


N. Baltzell:  In 2014, modified to read Mode-7, create a ROOT
TTree to kickstart cosmic analysis (AnaEcal.cc, still used),
read SSP+TI and put in tree, etc.  Compiling is some combination
of scons, configure, in different directories ...


