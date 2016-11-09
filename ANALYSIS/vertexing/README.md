# Monte Carlo inputs
The Monte Carlo types listed here are what should be used --- not necessarily what was used for Sho's thesis.

All MC inputs should be overlaid with full beam background (e.g. tritrig-wab-beam-tri).
* Tritrig: use tritrig-wab-beam-tri if available.
* WAB: use wabtrig-wab-beam-tri if available; wab-beam-tri is okay too.
* RAD: use rad-wab-beam-tri if available; Sho's thesis used rad_vert.root, which is pure RAD.
* Displaced A': need both the tuples from SLIC output, and the tuples from reconstruction.
The SLIC output must be pure A', but the reconstructed A' should be ap-wab-beam-tri if available.
Sho's thesis used aptuple/apsignal_slic_displaced_*_dq_truth.root (SLIC output) and aptuple/apsignal_displaced_*_dq_tri.root (recon, no cuts), which are both pure A'.
The ctau should be large enough to populate the full range in Z; 1 mm worked for 1.056 GeV.
Masses should cover the full range, and be spaced closely enough for good fits.

## Files used for Sho's thesis
All relative paths (no initial slash) are relative to http://www.slac.stanford.edu/~meeg/tuples/ (on AFS, /afs/slac.stanford.edu/u/xo/meeg/public_html/tuples).

### data
pass6 recon

raw tuples: goldentuple/hps_\*_dq_tri.root

after vertexing cuts: golden_vert.root

after `applyCuts.py`: vertexing/golden_vertcuts.root

### tritrig
pure tritrig

LCIO at JLab: /mss/hallb/hps/production/postTriSummitFixes/recon/tritrig/1pt05/tritrigv1_10to1_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_pairs1_\*.slcio

LCIO at SLAC: /nfs/slac/g/hps3/data/engrun2015/postTriSummitFixes/mc/recon/tritrig

raw tuples: tritrigtuple/tritrig_skim_\*_postfix_dq_tri.root

after vertexing cuts: tritrig_postfix_vert.root

after `applyCuts.py`: vertexing/tritrig_postfix_vertcuts.root

### WAB
pure WAB

LCIO at JLab: /mss/hallb/hps/production/postTriSummitFixes/recon/wab/1pt05/wabv2_10to1_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_pairs1_\*.slcio

LCIO at SLAC: /nfs/slac/g/hps3/data/engrun2015/postTriSummitFixes/mc/recon/wab

raw tuples: wabtuple/wabv2postfix_*_dq_tri.root

after vertexing cuts: wabv2postfix_vert.root

after `applyCuts.py`: vertexing/wabv2postfix_vertcuts.root

### rad
pure RAD

LCIO at JLab: /mss/hallb/hps/production/postTriSummitFixes/recon/RAD/1pt05/RADv2_10to1_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_pairs1_\*.slcio

LCIO at SLAC: /nfs/slac/g/hps3/data/engrun2015/postTriSummitFixes/mc/recon/RAD

raw tuples: radtuple/rad_dq_tri.root

after vertexing cuts: rad_vert.root

after `applyCuts.py`: vertexing/rad_vertcuts.root

### ap (recon)
pure displaced A'

LCIO at JLab: /mss/hallb/hps/production/postTriSummitFixes/recon/ap/1pt05/\*/apsignalv2_displaced_1mm_epsilon-4_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_pairs1_\*.slcio

LCIO at SLAC: /nfs/slac/g/hps3/data/engrun2015/postTriSummitFixes/mc/recon/ap

raw tuples: aptuple/apsignal_displaced_\*_dq_tri.root

after vertexing cuts: vertexing/acceptance/ap_\*_vert.root

after `applyCuts.py`: vertexing/acceptance/ap_\*_vertcuts.root

### ap (SLIC output)
pure displaced A'

LCIO at JLab: /mss/hallb/hps/production/postTriSummitFixes/slic/ap/1pt05/\*/apsignalv2_displaced_1mm_epsilon-4_HPS-EngRun2015-Nominal-v5-0-fieldmap_\*.slcio

LCIO at SLAC: /nfs/slac/g/hps3/data/engrun2015/postTriSummitFixes/mc/slic/ap

raw tuples: aptuple/apsignal_slic_displaced_\*_dq_truth.root

# Compiling optimum interval code
This requires the `f2py` command. By default, `make` will build the Fortran examples as well, but `make upperlimit.so` will just build the Python module.
```
cd upperlimit
make
```

# Running the analysis
All steps of the analysis have shell scripts that can be used to run things quickly.
Most assume access to the SLAC batch farm, and all have hard-coded file names/paths.

If you can't use the scripts and have to run things "by hand," the commands are also written out.

## Making tuples and applying cuts

For data:

1. Run the tuple maker in hps-java using `MakeTuples.lcsim`, which will make a text tuple `file_dq_tri.txt`
2. Convert each text file to ROOT tuple using `makeTree.py file_dq_tri.root file_dq_tri.txt`
3. Merge and apply vertexing cuts with `mergeTrees.py -v file_vert.root file1_dq_tri.root file2_dq_tri.root`
4. Cut down to a single trident candidate per event using `applyCut.py -t vertexing -bv file_vertcuts.root file_vert.root`

For MC recon:

1. Run the tuple maker in hps-java using `MakeTuplesMC.lcsim`, which will make a text tuple `file_dq_tri.txt`
2. Convert each text file to ROOT tuple using `makeTree.py file_dq_tri.root file_dq_tri.txt`
3. Merge with `mergeTrees.py -v file_vert.root file1_dq_tri.root file2_dq_tri.root`
4. Cut down to a single trident candidate per event using `applyCut.py -t vertexing -mbv file_vertcuts.root file_vert.root`

For SLIC output, only do steps 1 and 2 of the above.

## Radiative fraction
The integrated luminosities of the MC samples are hard-coded in `radfrac.py`.

With scripts:
```
./run_radfrac.sh
```

By hand:
```
./radfrac.py frac rad_vertcuts.root tritrig_vertcuts.root wab_vertcuts.root
```

## Mass resolution and acceptance
This finds the mass resolution and the acceptance dependence on Z.

With scripts (`run.sh` actually runs `mergeTrees.py` and `applyCuts.py` as well):
```
cd acceptance
./run.sh
./run_apeff.sh
```

By hand, for each mass:
```
./acceptance/ap_plots.py acceptance_22 ap_22_vertcuts.root apsignal_slic_displaced_22_dq_truth.root -c
```
then:
```
./acceptance/apeff.py acceptance_data acceptance_22.root acceptance_24.root acceptance_26.root acceptance_28.root acceptance_30.root acceptance_35.root acceptance_40.root acceptance_50.root acceptance_60.root
```

## Vertex tails fit
This fits the vertex distribution as a function of mass.
Requires the mass resolution data as input.

With scripts:
```
./run_fittails.sh
```

By hand:
```
./fittails_mc.py tails tritrig_vertcuts.root acceptance/acceptance_data.root -mc
```

## Running the analysis
With scripts:
```
cd upperlimit
./run.sh
```

By hand:
```
./fitvtx.py golden ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails.root ../frac.root -m
```
