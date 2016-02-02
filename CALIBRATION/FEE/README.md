# HPS_Calibration
Author: Holly Szumila-Vance
Date: 2 Feb 2016
Email: hvanc001@odu.edu

This contains the scripts for running the FEE (elastically-scattered e-)
calibration for the HPS Ecal. 

In order to run the FEE calibration, one must first run reconstruction on data
using the FEEFilterDriver and the FEECLusterPlotter after
reconstruction. These will produce an output root file with the FEE peak in
each crystal. The offline code here will use that root file for input.

Input files:
-cosmic gains (coeff/cosmic.txt) 
-previous c factor (c=c1xc2xc3...), (coeff/cX.txt)
-root histograms (input_iterX/FEE_cX.root) where X is iteration
-crystal index converter (util/indexConverter.txt)
-elastic SF from MC (coeff/MC_constant.txt)

Output files:
-new c factor (output_iterX/cX.txt)
-current global gain (c x cosmic) for DB (coeff/cGlobal_X.txt)
-plots to check iteration (output_iterX/cX.txt)

The c factor is used in hps-java to iterate on the hit energies after cosmic
gains are already applied. Therefore, when ready to upload to db, the global
gain must be used. The iterations should be repeated until all crystals (in
acceptance region) are within 1% according to the Elasticmean plot. 

The code can be run in root:
.L analyzeFeePeak.C
fitPeaks(ITER)

ITER is an integer referring to the iteration (user must count). The first
time the code is used, the iteration is 1. The input root file should be
labeled as 1 and c output file is 1. The previous c input file is always c
ITER-1. 
