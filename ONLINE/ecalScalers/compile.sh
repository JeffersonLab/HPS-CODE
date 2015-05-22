#!/bin/sh

rootcint -f hps_ecal_scalers_Dict.cxx -c -p hps_ecal_scalers.h hps_ecal_scalers_LinkDef.h
g++ -W -Wall -Wshadow -Wstrict-aliasing -pthread -m64 -I/home/hpsrun/apps/root_v5.34.21.Linux-slc6-amd64-gcc4.4/include -I/home/hpsrun/.root -c hps_ecal_scalers.cxx
g++ -W -Wall -Wshadow -Wstrict-aliasing -pthread -m64 -I/home/hpsrun/apps/root_v5.34.21.Linux-slc6-amd64-gcc4.4/include -I/home/hpsrun/.root -c hps_ecal_scalers_Dict.cxx
g++ -W -Wall -Wshadow -Wstrict-aliasing -pthread -m64 -I/home/hpsrun/apps/root_v5.34.21.Linux-slc6-amd64-gcc4.4/include -L/home/hpsrun/apps/root_v5.34.21.Linux-slc6-amd64-gcc4.4/lib -lCore -lCint -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lTree -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -pthread -lm -ldl -rdynamic -L/home/hpsrun/apps/root_v5.34.21.Linux-slc6-amd64-gcc4.4/lib -lGui -I/home/hpsrun/.root -o hps_ecal_scalers hps_ecal_scalers.o  hps_ecal_scalers_Dict.o


