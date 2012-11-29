ROOTLIBS = `$(ROOTSYS)/bin/root-config --glibs`

BIN := ../bin
SRC_DIR := ../src
#STDHEP_DIR := ../src/stdhep-5-06-01
#STDHEP_C := $(STDHEP_DIR)/lib/libstdhepC.a
#MCFIO := $(STDHEP_DIR)/lib/libFmcfio.a
#STDHEP_LIBS = $(STDHEP_C) $(MCFIO)
LOADLIBS=-L/usr/local/lib/stdhep -L/afs/slac.stanford.edu/package/cernlib/@sys/cern/2002/lib
LDLIBS=-lstdhepC -lFmcfio $(ROOTLIBS) -lgsl -lgslcblas
INCFILES=-I$(ROOTSYS)/include/ -I$(ROOTSYS)/include/root/ -I$(SRC_DIR) -I/home/meeg/stdhep-5-06-01/src/inc/ -I/afs/slac.stanford.edu/package/cernlib/@sys/cern/2002/include/stdhep
CPP=g++
CPPFLAGS=$(LOADLIBS) $(LDLIBS) $(INCFILES) -g
TARGETS := $(patsubst $(SRC_DIR)/%.cc,$(BIN)/%,$(wildcard $(SRC_DIR)/*.cc))
UTIL_SRC := $(wildcard $(SRC_DIR)/*.cpp)
UTIL_OBJ := $(UTIL_SRC:.cpp=.o)

all: $(TARGETS) $(UTIL_OBJ)
$(BIN)/%: $(SRC_DIR)/%.cc $(UTIL_OBJ)
	$(CPP) $< $(UTIL_OBJ) $(CPPFLAGS) -o $@
$(SRC_DIR)/%.o: $(SRC_DIR)/%.cpp $(SRC_DIR)/%.hh
	$(CPP) $< -c $(INCFILES) -g -o $@
clean:
	@rm -f $(TARGETS) $(UTIL_OBJ)

