#!/usr/bin/env python
import sys
import getopt
from ROOT import gROOT, TFile, TTree
print sys.argv[1]
treeFile = TFile(sys.argv[1],"RECREATE")
tree = TTree("ntuple","data from text tuple "+sys.argv[2])
print sys.argv[2:]

if len(sys.argv)>3:
    inputfile = tempfile.NamedTemporaryFile(delete=False)
    print inputfile.name
    firstfile = True
    for filename in sys.argv[2:]:
        f = open(filename)
        firstline = True
        for i in f:
            if firstline:
                if firstfile:
                    branchdescriptor = i
                    inputfile.write(i)
                else:
                    if branchdescriptor != i:
                        print "branch descriptor doesn't match"
                        sys.exit(-1)
            else:
                inputfile.write(i)
            firstline = False
        f.close()
        firstfile = False
    inputfile.close()
    print tree.ReadFile(inputfile.name)
    os.remove(inputfile.name)
else:
    print tree.ReadFile(sys.argv[2])



tree.Write()
