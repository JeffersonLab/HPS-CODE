# HPS_Calibration
Author: Holly Szumila-Vance
Email: hszumila@jlab.org

This contains the scripts for running the cosmic calibration for the HPS
Ecal. 

In order to run the cosmic calibration, one must first have the evio files
converted to ROOT files containing the raw adc spectra for each crystal. This
still needs to be added here.

The raw data needs to be analyzed using a strict geometric cut, loose
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

To use the geometric cut, one can run cosmicAnalysis in root by typing:
.L cosmicAnalysis.C++
geoCut(0) //Option 0 is strict, option 1 is loose
getGain()

To use the counting cut, one can run cosmicAnalysis in root by typing:
.L cosmicAnalysis.C++
countingCut(2) // 2 is a good default, 3 is tighter
getGain()

The output file (gains4db.txt) with the crystals and gains is in the format to upload to the database.

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