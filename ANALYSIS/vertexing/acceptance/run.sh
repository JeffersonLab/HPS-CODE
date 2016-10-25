#!/bin/bash
for i in 15 16 17 18 19 20 22 24 26 28 30 35 40 50 60 70 80 90
do 
    filename="acceptance_${i}"
    tempname="ap_${i}_vert"
    bsub -W 60 -oo $filename.out -eo $filename.err "../tuple/mergeTrees.py -v ${tempname}.root apsignal_displaced_${i}_dq_tri.root;../tuple/applyCut.py -t vertexing ${tempname}cuts.root ${tempname}.root -mbv;./ap_plots.py $filename ${tempname}cuts.root apsignal_slic_displaced_${i}_dq_truth.root -c"
    filename="acceptance_alllayers_${i}"
    tempname="ap_${i}_allvert"
    bsub -W 60 -oo $filename.out -eo $filename.err "../tuple/mergeTrees.py -a ${tempname}.root apsignal_displaced_${i}_dq_tri.root;../tuple/applyCut.py -t vertexing ${tempname}cuts.root ${tempname}.root -mbv;./ap_plots.py $filename ${tempname}cuts.root apsignal_slic_displaced_${i}_dq_truth.root -c"
done
