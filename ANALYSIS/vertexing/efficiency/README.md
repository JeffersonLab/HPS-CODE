# Running `GenerateEfficiencyTable.py`

## Command

```
python GenerateEfficiencyTable.py <output basename> <input text file> <options>
```

## Options

-e: beam energy in GeV (default 1.056 GeV) `
-t: target position in mm (default -5 mm) `
-n: number of bins in histograms (default 50) `
-z: total range in z covered in mm (default is 100 mm) `
-T: plot Test plots `

## Output Files

Output files include <output basename>.eff and <output basename>.pdf (if -T option is used)

### .eff File

This is the output text file of efficiency values. The output file reads like this:

```
line 1 {mass array mass[0...n]} `
line 2 {z array z[0...m]} `
line 3 {efficiency values at z[i] for mass[0]} `
line 4 {efficiency values at z[i] for mass[1]} `
`
`
`
line n + 2 {efficiency values at z[i for mass[n-1]}
```

where `n` is the number of mass values and `m` is the number of z bins

### pdf File

If -T option is selected, a pdf file of test plots will be output. These plots compare the interpolation values of a known A' mass with an interpolation using the mass value above and below the test mass value.

## Input Text File

Input text files corresponds to files paths to tuple files. `
Each line corresponds to a file in the following format: `

```
line 1 {path to cut tuple file for mass[0]} `
line 2 {path to cut tuple file for mass[1]} `
`
`
`
line n {path to cut tuple file for mass[n-1]} `
line n+1 {path to truth tuple file for mass[0]} `
line n+2 {path to truth tuple file for mass[1]} `
`
`
`
line 2n {path to truth tuple file for mass[n-1]} `
```

where `n` is the number of mass values

## Reading Values from Efficiency Table

Use the following functions to read the .eff text file

### Getting Mass Array `mass_arr`
```
mass_arr = getMassArray(<.eff file>)
```

### Getting Z Array `z_arr`
```
z_arr = getZArray(<.eff file>)
```

### Getting 2D Efficiency Table `eff_arr`
```
eff_arr = getEfficiency(<.eff file>)
```

### Get Interpolatation Values `intrplt` for a given `mass` and `z`

* Directly from .eff file
```
intrplt = InterpolateFromFile(mass,z,<.eff file>)
```

* Using mass, z, and efficiency arrays grabbed from functions above
```
intrplt = Interpolate(mass,z,mass_arr,z_arr,eff_arr)
```