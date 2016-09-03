#!/bin/bash
for i in 15 16 17 18 19 20 22 24 26 28 30 35 40 50 60 70 80 90
do 
    ../tuple/mergeTrees.py -v temp.root apsignal_displaced_${i}_dq_tri.root
    ../tuple/applyCut.py -t vertexing temp2.root temp.root -mb
    ./ap_plots.py acceptance_${i} temp2.root apsignal_slic_displaced_${i}_dq_truth.root
done
