#!/bin/bash

export ROOTSYS=/u/apps/root/6.08.00/root
#export ROOTSYS=/u/apps/root/5.34.36/root

#export LCIO=/net/home/byale/hps/dst/lcio/trunk
#export GBL_DIR=/net/home/byale/hps/dst/gbl-V01-16-02/cpp/build
source $ROOTSYS/bin/thisroot.sh

#PATH=$PATH:/u/group/hps/hps_soft/hps-dst/centos7-64/lib
#PATH=$PATH:/u/apps/root/5.34.36/root/lib
PATH=$PATH:/u/apps/root/6.08.00/root/lib

#ldconfig /u/group/hps/hps_soft/hps-dst/build/lib
#ldconfig /u/apps/root/5.34.13/root/lib

#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u/group/hps/hps_soft/hps-dst-0.8/build/lib
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u/group/hps/hps_soft/hps-dst-withiso/build/lib
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u/group/hps/hps_soft/hps-dst/build/lib
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u/apps/root/5.34.36/root/lib
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u/apps/root/6.08.00/root/lib

#source /u/group/hps/hps_soft/setup_dst.csh

#export CC=/apps/gcc/4.9.2/bin/gcc
#export CXX=/apps/gcc/4.9.2/bin/g++
export CC=/apps/gcc/5.2.0/install/bin/gcc
export GCC=/apps/gcc/5.2.0/install/bin/gcc
export CXX=/apps/gcc/5.2.0/install/bin/g++
#module load gcc_5.2.0

#export ROOTSYS=/apps/root/5.34.36/root
#export ROOTSYS=/u/apps/root/6.08.00/root
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/apps/gcc/5.2.0/install/lib64
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/apps/gcc/5.2.0/gcc-5.2.0/libgcc
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/apps/root/5.34.36/root/lib

PATH=${PATH}:${ROOTSYS}/bin
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${ROOTSYS}/lib
export LCIO=/u/group/hps/hps_soft/lcio/centos7-64
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LCIO}/lib
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/u/group/hps/hps_soft/lcio/centos7-64/trunk/trunk/lib
#LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/apps/gcc/5.2.0/lib64
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/u/group/hps/hps_soft/hps-dst/centos7-64/lib
PATH=${PATH}:/u/group/hps/hps_soft/hps-dst/centos7-64/bin
PATH=${PATH}:/u/group/hps/hps_soft/hps-dst/centos7-64/lib

#g++ ap_2pt2.cc -o ap_2pt2.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ ap_2pt2.cc -o ap_2pt2.exe -Wl,--no-as-needed -L /u/group/hps/hps_soft/lcio/trunk/lib -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/src/cpp/include -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ moller_2pt2.cc -o moller_2pt2.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ moller_uncut.cc -o moller_uncut.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ moller_tilt.cc -o moller_tilt.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ ap.cc -o ap.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ moller_v4.cc -o moller_v4.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -L${LCIO}/lib -L$ROOTSYS/lib -lHpsEvent -I${LCIO}/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ moller_without_ECal.cc -o moller_without_ECal.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

g++ CompareHistograms_2pt3_Mollers.cc -o CompareHistograms_2pt3_Mollers.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/centos7-64/lib -L${LCIO}/lib -L$ROOTSYS/lib -lHpsEvent -I${LCIO}/include -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ CompareHistograms_6pt6_TM.cc -o CompareHistograms_6pt6_TM.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/centos7-64/lib -lHpsEvent -L${LCIO}/lib -L$ROOTSYS/lib -I${LCIO}/include -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ CompareHistograms_1pt05_Tridents.cc -o CompareHistograms_1pt05_Tridents.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/hps-dst/build/lib -L${LCIO}/lib -L$ROOTSYS/lib -lHpsEvent -I${LCIO}/include -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ CompareHistograms_1pt05_Mollers_pairs1.cc -o CompareHistograms_1pt05_Mollers_pairs1.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst_old/build/lib -L${LCIO}/lib -L$ROOTSYS/lib -lHpsEvent -I${LCIO}/include -I/u/group/hps/hps_soft/hps-dst_old/include/hps_event -I/u/group/hps/hps_soft/hps-dst_old/include/dst -I/u/group/hps/hps_soft/hps-dst_old/include/utils `root-config --cflags` `root-config --libs`

#g++ tridentAnalysis.cc -o tridentAnalysis.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -L${LCIO}/lib -L$ROOTSYS/lib -lHpsEvent -I${LCIO}/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ simpleROOTex.cc -o simpleROOTex.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/lcio/trunk/include -I/u/group/hps/hps_soft/hps-dst/include/hps_event -I/u/group/hps/hps_soft/hps-dst/include/dst -I/u/group/hps/hps_soft/hps-dst/include/utils `root-config --cflags` `root-config --libs`

#g++ moller_uncut.cc -o moller_uncut.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst-withiso/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/hps-dst-withiso/include/hps_event -I/u/group/hps/hps_soft/hps-dst-withiso/include/dst -I/u/group/hps/hps_soft/hps-dst-withiso/include/utils `root-config --cflags` `root-config --libs`

#g++ particles.cc -o particles.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst-0.8/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/hps-dst-0.8/include/hps_event -I/u/group/hps/hps_soft/hps-dst-0.8/include/dst -I/u/group/hps/hps_soft/hps-dst-0.8/include/utils `root-config --cflags` `root-config --libs`

#g++ coplanarity.cc -o coplanarity.exe -Wl,--no-as-needed -L/u/group/hps/hps_soft/hps-dst-withiso/build/lib -lHpsEvent -L$ROOTSYS/lib -I/u/group/hps/hps_soft/hps-dst-withiso/include/hps_event -I/u/group/hps/hps_soft/hps-dst-withiso/include/dst -I/u/group/hps/hps_soft/hps-dst-withiso/include/utils `root-config --cflags` `root-config --libs`
