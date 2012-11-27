ROOTLIBS = `$(ROOTSYS)/bin/root-config --glibs`

BIN := ../bin/
SRC_DIR := ../src/
LOADLIBS=-L$(CERNLIB) -L$(X11LIB) -L/usr/local/lib/stdhep -L/afs/slac.stanford.edu/package/cernlib/@sys/cern/2002/lib
LDLIBS=-lstdhepC $(ROOTLIBS) -lFmcfio -lgsl -lgslcblas
INCFILES=-I/home/meeg/stdhep-5-06-01/src/inc/ -I$(ROOTSYS)/include/ -I$(ROOTSYS)/include/root/ -I/afs/slac.stanford.edu/package/cernlib/@sys/cern/2002/include/stdhep -I$(SRC_DIR)
CPP=g++
CPPFLAGS=$(LOADLIBS) $(LDLIBS) $(INCFILES) -g
TARGETS := $(patsubst $(SRC_DIR)/%.cc,$(BIN)/%,$(wildcard $(SRC_DIR)/*.cc))
UTIL_SRC := $(wildcard $(SRC_DIR)/*.cpp)
UTIL_OBJ := $(UTIL_SRC:.cpp=.o)

all: $(TARGETS) $(UTIL_OBJ)
$(BIN)/%: $(SRC_DIR)/%.cc $(UTIL_OBJ)
	$(CPP) $< $(CPPFLAGS) $(UTIL_OBJ) -o $@
$(SRC_DIR)/%.o: $(SRC_DIR)/%.cpp $(SRC_DIR)/%.hh
	$(CPP) $< -c $(INCFILES) -g -o $@
clean:
	@rm -f $(TARGETS) $(UTIL_OBJ)

