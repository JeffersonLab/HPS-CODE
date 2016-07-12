# Tuple maker
Start with LCIO files from recon.

Run the tuple maker steering file:

```
java -jar hps-distribution-bin.jar -r /org/hps/steering/analysis/TupleMaker.lcsim -i in.slcio -DoutputFile=out
```

This will dump data to text files: `out_fee.txt`, `out_moller.txt`, `out_tri.txt`.
The file is written in the format required by `TTree::ReadFile()`.
For MC, or data without event flags, use `TupleMakerMC.lcsim`.

The trident tuple has cuts applied: $p(e^-), p(e^+)<0.9E_{beam}$, $p(e^-)+p(e^+)<1.3E_{beam}$.

Convert the text file to a ROOT tree:
```
./makeTree.py tri.root out_tri.txt
```

Merge multiple ROOT trees:
```
./mergeTrees.py merged_tri.root tri1.root tri2.root
```
You can apply cuts at this stage with command-line options: run `./mergeTrees.py -h` to list the choices.

Count and rank trident candidates (this code requires numpy and root_numpy):
```
./applyCuts.py cuts.root merged_tri.root
```
This makes a new tree in `cuts.root` that can be added as a friend to `merged_tri.root`.
Your analysis can cut on `rank==1` to select only the highest-ranked trident candidate in each event.