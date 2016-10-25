# Monte Carlo inputs
The Monte Carlo types listed here are what should be used --- not necessarily what was used for Sho's thesis.

All MC inputs should be overlaid with full beam background (e.g. tritrig-wab-beam-tri).
* Tritrig: use tritrig-wab-beam-tri if available. Sho's thesis used tritrig_postfix_vert.root.
* WAB: use wabtrig-wab-beam-tri if available; wab-beam-tri is okay too. Sho's thesis used wabv2postfix_vert.root.
* RAD: use rad-wab-beam-tri if available; Sho's thesis used rad_vert.root.
* Displaced A': use ap-wab-beam-tri if available.
Need both the tuples from SLIC output, and the tuples from reconstruction.
The ctau should be large enough to populate the full range in Z; 1 mm worked for 1.056 GeV.
Masses should cover the full range, and be spaced closely enough for good fits.

# Compiling optimum interval code
```
cd upperlimit
make
```

# Running the analysis
All steps of the analysis have shell scripts that can be used to run things quickly.
Most assume access to the SLAC batch farm, and all have hard-coded file names/paths.

## Radiative fraction
With scripts:
```
./radfrac.py frac rad.root tritrig.root wab.root
```

## Mass resolution

## Vertex tails fit

## Running the analysis
