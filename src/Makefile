ROOTLIBS = `$(ROOTSYS)/bin/root-config --glibs`

BIN := ../bin/
SRC_DIR := ../src/
LOADLIBS=-L$(CERNLIB) -L$(X11LIB) -L/usr/local/lib/stdhep -L/afs/slac/package/cernlib/@sys/cern/2002/lib
LDLIBS=-lstdhepC $(ROOTLIBS) -lFmcfio 
INCFILES=-I/home/meeg/stdhep-5-06-01/src/inc/ -I$(ROOTSYS)/include/ -I/afs/slac/package/cernlib/@sys/cern/2002/include/stdhep -I$(SRC_DIR)
CPP=g++
CPPFLAGS=$(LOADLIBS) $(LDLIBS) $(INCFILES) -g
TARGETS := $(patsubst $(SRC_DIR)/%.cc,$(BIN)/%,$(wildcard $(SRC_DIR)/*.cc))

all: $(TARGETS)
$(BIN)/%: $(SRC_DIR)/%.cc
	$(CPP) $< $(CPPFLAGS) -o $@
clean:
	@rm -f $(TARGETS)

