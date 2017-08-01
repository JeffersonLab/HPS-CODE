# HPS_Calibration
Author: Holly Szumila-Vance
Email: hszumila@jlab.org

This contains the scripts for running the cosmic calibration for the HPS
Ecal. 

In order to run the cosmic calibration, one must first have the evio files
converted to ROOT files containing the raw adc spectra for each crystal. There are two options:
1. (optimal) Use hps-java 
2. Use C codes at: https://github.com/JeffersonLab/HPS-CODE/tree/master/ANALYSIS/EvioTool

If using option 1, then the scripts to run this are located at /u/group/hps/production/data/cosmic on ifarm. 
The java command:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
java -cp jarfile.jar org.hps.evio.EvioToLcio -x /org/hps/steering/analysis/CosmicCalibration.lcsim -r -d HPS-PhysicsRun2016-Nominal-v5-0-fieldmap -R run# -DoutputFile=output inputEvio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Above, the jarfile.jar should be the actual jar file, the run# should be a valid run number from the current run dates (sometimes a number for pure cosmic runs does not work), and inputEvio should point to some raw evio file from cosmic running. This will output a root file (the same as would be produced in steps 1-2 below. 

Step 1. The raw data needs to be analyzed using a strict geometric cut, loose
geometric cut, or counting cut. The first is recommended for the
calibration, but the latter two are useful when there are bad crystals. A
strict geometric cut requires that there is no hit above threshold to the left
and right crystals but there must be a hit above AND below. A loose geometric
cut requires that there can be no hit in the left and right crystals but there
must be a hit in a crystal above OR below. A counting cut requires that any
number of crystals (2 is good) in the same column (and half) have a hit above
threshold and not the ones to the left and right. 

Make directory: input
Put raw files in the folder "input".
(Or make a symbolic link as: ln -s folder/with/root/files.root input)

In the folder, "dependency", one must replace the line in chainfilelist.C to
give a scratch folder directory.

Step 2:
To use the geometric cut, one can run cosmicAnalysis in root by typing:
.L cosmicAnalysis.C++
geoCut(0) //Option 0 is strict, option 1 is loose
To use the counting cut, one can run cosmicAnalysis in root by typing:
.L cosmicAnalysis.C++
countingCut(2) // 2 is a good default, 3 is tighter


Step 3 for those who used hps-java or the EvioTool from C code:
In root, type .L cosmicAnalysis.C++
getGain()

The output file (gains4db.txt) with the crystals and gains is in the format to upload to the database. This is also in the desired format for input to the elastic calibration.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to upload to the database:
java -cp hps-distribution-SNAPSHOT-bin.jar org.hps.conditions.cli.CommandLineTool -p jlab_write.prop load -f convolFit/gains4db.txt -t ecal_gains

After this command, there will be a collection id number given. This is used as ## in the next command:

java -cp hps-distribution-SNAPSHOT-bin.jar org.hps.conditions.cli.CommandLineTool -p jlab_write.prop add -c ## -r XXXX -e 9999999 -t ecal_gains -u username -m 'gains from cosmics'

where:
XXXX is the starting run number that these gains apply to
username is the user name upload the gains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The other output file is gains4DAQconversion.txt. This file must be converted so that the gains cna be uploaded into the DAQ prior to running. This can be done using the script calibUtilHpsEcal.py:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python calibUtilHpsEcal.py -g convolFit/gains4DAQconversion.txt -G -DAQ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~