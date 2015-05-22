#!/bin/sh

rootcint -f hps_ecal_scalers_Dict.cxx -c -p hps_ecal_scalers.h hps_ecal_scalers_LinkDef.h

g++ -W -Wall -Wshadow -Wstrict-aliasing -pthread -m64 -I$ROOTSYS/include \
    -c hps_ecal_scalers.cxx

g++ -W -Wall -Wshadow -Wstrict-aliasing -pthread -m64 -I$ROOTSYS/include \
    -c hps_ecal_scalers_Dict.cxx

g++ -W -Wall -Wshadow -Wstrict-aliasing -pthread -m64 -I$ROOTSYS/include \
    -L$ROOTSYS/lib -lCore -lCint -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad \
    -lTree -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread \
    -pthread -lm -ldl -rdynamic -L$ROOTSYS/lib -lGui \
    -o hps_ecal_scalers hps_ecal_scalers.o  hps_ecal_scalers_Dict.o


