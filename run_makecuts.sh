#!/bin/bash
#~/bin/tuple/mergeTrees.py -v tritrig_pass6_vert.root /nfs/slac/g/hps3/users/meeg/tritrigtuple/tritrig_pass6_skim_*_dq_tri.root
#~/bin/tuple/mergeTrees.py -a tritrig_pass6_allvert.root /nfs/slac/g/hps3/users/meeg/tritrigtuple/tritrig_pass6_skim_*_dq_tri.root
#~/bin/tuple/applyCut.py golden_vertcuts.root /nfs/slac/g/hps3/users/meeg/goldentuple/golden_loosetri.root -t vertexing -bv
~/bin/tuple/applyCut.py tritrig_postfix_vertcuts.root /nfs/slac/g/hps3/users/meeg/tritrigtuple/tritrig_postfix_vert.root -t vertexing -bv

