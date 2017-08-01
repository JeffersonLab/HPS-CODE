# HPS_Calibration
Author: Holly Szumila-Vance
Date: 18 July 2017
Email: hszumila@jlab.org

This contains the scripts for running the FEE (elastically-scattered e-)
calibration for the HPS Ecal. 

Using a recon slcio file, the following can be run in hps-java to output a root file with a histogram of each crystal by database id.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
java -jar hps-distribution-SNAPSHOT-bin.jar -r /org/hps/steering/calibration/EcalFEECalibration.lcsim -d HPS-EngRun2015-Nominal-v5-0-fieldmap -R runNumber -i input.slcio -DoutputFile=output 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the above command, the relevant detector, run number and input file slcio file should be used. This steering files reads in the hits from recon, applies a gain correction factor to their energy, re-runs clustering, and then outputs a root file called "outputFEEPlots.root". The default iteration coefficient of gains is 1 and can be obtained from the file ecalGains.txt 
When running the java part, always check the steering file collections are correct, and in the FEEClusterPlotter.java that the timing and energy variables are as desired. 

This can be run on the batch farm using the scripts found at:
/u/group/hps/production/data/feeCalib

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The calibration procedure:
1. Obtain the MC peak position / incident beam energy. Write this to coeff/MC_constant.txt
   -run hps-java as above, use default coefficients (1).
   -put the root file in input_MC/FEE_MC.root
   -open root, .L analyzeMCPeak.C, fitMCPeaks()
   -this outputs the file coeff/MC_constant.txt for use in the iterations. check fits. 
2. Put the cosmic gains in coeff/cosmic.txt
3. Run the above hps-java on the recon data file, using iteration coefficient of 1. This fills the histogram.
4. In analyzeFeePeak.C, enter the incident beam energy at EBEAM
   1st iteration: 
   -make directory output_iter1 (for first iteration)
   -put the root file from java in input_iter1/FEE_c1.root
   -open root, type .L analyzeFeePeak.C, fitPeaks(1)
   -review the fits. Use the output coeff/c1.txt file for the next iteration in hps-java 
5. Repeat step 4 but change all iteration values to 2. 
Continue until within 1% of the MC peak/ beam energy ratio. 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This folder requires the information for fitting the histograms, 
Input files:
-cosmic gains (coeff/cosmic.txt) 
-previous c factor (c=c1xc2xc3...), (coeff/cX.txt)
-root histograms (input_iterX/FEE_cX.root) where X is iteration
-elastic ratio of MC peak/ beam energy at (coeff/MC_constant.txt)

Output files:
-new c factor (output_iterX/cX.txt)
-current global gain (c x cosmic) for DB (coeff/cGlobal_X.txt)
-plots to check iteration (output_iterX/cX.txt)

The c factor is used in hps-java to iterate on the hit energies after cosmic
gains are already applied. Therefore, when ready to upload to db, the global
gain must be used. The iterations should be repeated until all crystals (in
acceptance region) are within 1% according to the Elasticmean plot. 