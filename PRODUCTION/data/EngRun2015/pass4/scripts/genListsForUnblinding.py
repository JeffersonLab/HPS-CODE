#!/usr/bin/env python
import os

# this was used once to generate lists for scicomp to set blinding tape permissions.

with open('blinded-lessthan3mm.txt','r') as tmp: 
    blinded=tmp.readlines()

blinded=map(str.rstrip, blinded)

for (dpath, dnames, fnames) in os.walk('/mss/hallb/hps/data'):
    ll=[dpath+'/'+xx.rstrip() for xx in fnames]
    for xx in ll:
        if not xx in blinded: print xx

