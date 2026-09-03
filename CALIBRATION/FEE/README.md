# HPS_Calibration

Original author: Holly Szumila-Vance (hszumila@jlab.org), 18 July 2017.
Adapted for the 2019 ECAL gain calibration reproduction (Andrea Celentano's
cosmic + FEE calibration) by Erbaz Khan.

This contains the scripts for running the FEE calibration for the HPS Ecal.

Using a recon slcio file, the following can be run in hps-java to output a root file with a histogram of each crystal by database id.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
java -jar hps-distribution-SNAPSHOT-bin.jar -r /org/hps/steering/calibration/EcalFEECalibration2019.lcsim -d <detector> -R runNumber -i input.slcio -DoutputFile=output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the above command, use the relevant detector, run number, and input slcio file. This steering file reads in the hits from recon, applies a gain correction factor to their energy, re-runs clustering, and then outputs a root file called "outputFEEPlots.root". The default iteration coefficient of gains is 1 and can be obtained from the file ecalGains.txt
When running the java part, always check the steering file collections are correct, and in the FEEClusterPlotter.java that the timing and energy variables are as desired.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The calibration procedure:
1. Obtain the MC peak position / incident beam energy. Write this to coeff/MC_constant.txt
   -run hps-java as above, use default coefficients (1).
   -put the root file in input_MC/FEE_MC.root
   -open root, .L analyzeMCPeak.C, fitMCPeaks()
   -this outputs the file output_MC/MC_constant.txt for use in the iterations. check fits. Copy them to coeff/MC_constant.txt.
2. Put the cosmic gains in coeff/cosmic.txt
3. Run the above hps-java on the recon data file, using iteration coefficient of 1 for first iteration or ecalGains_<n>.txt from nth iteration. This fills the histogram.
4. In analyzeFeePeak.C, enter the incident beam energy at EBEAM
   1st iteration:
   -make directory output_iter1_p<P>, where P is the period number
   -put the root file from java in input_iter1/FEE_c1_p<P>.root
   -open root, type .L analyzeFeePeak.C, fitPeaks(1,P)
   -review the fits. Use the output output_iter1_p<P>/c1.txt file for the next iteration in hps-java
5. Repeat step 4 but change all iteration values to 2.
Continue until within 1% of the MC peak/ beam energy ratio.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2019 data has 6 temperature-stable periods, calibrated independently, so
every step above is done once per period P and the outputs live under
output_iter<N>_p<P>/ instead of a single output_iterN/.

This folder requires the information for fitting the histograms,
Input files:
-cosmic gains (coeff/cosmic.txt)
-previous c factor (c=c1xc2xc3...), (output_iter<N-1>_p<P>/c<N-1>.txt)
-root histograms (input_iterN/FEE_cN_pP.root) where N is iteration, P is period
-elastic ratio of MC peak/ beam energy at (coeff/MC_constant.txt)

Output files:
-new c factor (output_iterN_pP/cN.txt)
-current global gain (c x cosmic) for DB (output_iterN_pP/cGlobal_N.txt)
-per-crystal gains, all crystals (output_iterN_pP/ecalGains_N.txt)
-per-crystal gains, edge rows (iy = -5,-1,1,5) forced to 1.0 (output_iterN_pP/ecalGains_rowexcl_N.txt)
-plots to check iteration (output_iterN_pP/*.png)

The c factor is used in hps-java to iterate on the hit energies after cosmic
gains are already applied. Therefore, when ready to upload to db, the global
gain must be used. The iterations should be repeated until all crystals (in
acceptance region) are within 1% according to the Elasticmean plot.

For atleast 2019 data, a handful of crystals (153, 198, 267, 275, 334; also 361 before run 10370) are defective and are excluded from the fit/ratio computation rather than used at face value — see analyzeFeePeak.C.

Once the FEE iterations are over, we need to correct the uncorrected crystals to bring them corrected and uncorrected crystals on the same scale. Mean of the ratio corrected_gains/baseline_gains for all the corrected crystals can be used as the correction factor for the uncorrected crystals. This step is not done this macro. We also need to test whether to exclude the edge rows based on how stable their FEE fit is.