#!/usr/bin/env python

from __future__ import division

import argparse
import math
import time
import ROOT as r

from rootpy.io import root_open

def mass_function(x, p):

    if x[0] > p[1]:

        y = x[0]/0.03

        fit_value = (p[0]*( ( pow((x[0] - p[1]), p[2]) )*math.exp(-p[3]*x[0]) ) /
                ( ( pow((0.03 - p[1]), p[2]) )*math.exp(-p[3]*0.03) ) * 
                ( 1 + p[4]*y + p[5]*pow(y,2) + p[6]*pow(y,3) + p[7]*pow(y,4) 
                    + p[8]*pow(y,5) + p[9]*pow(y,6) + p[10]*pow(y,7) ) 
                / (1 + p[4] + p[5] + p[6] + p[7] + p[8] + p[9] + p[10]))
        
        return fit_value

    else: return 0

def main() :

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-i", "--file", 
                        help='File containing invariant mass histogram to process.')
    args = parser.parse_args()

    if not args.file:
        parser.error('Please specify a file to process.')

    r.gStyle.SetOptStat(1111111)
    r.gStyle.SetOptFit(1)
    rfile = root_open(args.file)
    mass_hist = rfile.invariant_mass

    fit_function = r.TF1("function", mass_function , 0.01, 0.09, 11)
    fit_function.SetParameters(2000,0.015,0,0,0,0,0,0,0,0,0);

    mass_hist.Fit("function", "R")
    mass_hist.Fit("function", "R")
    mass_hist.Fit("function", "R")

    canvas = r.TCanvas("canvas", "canvas", 800, 800)
    canvas.SetLogy()
    mass_hist.Draw()
    
    canvas.SaveAs("mass_fit.pdf")

    # Initialize the random number generator
    r.gRandom.SetSeed(int(time.time()))
    rmass_hist = r.TH1F("invariant_mass", "invariant_mass", 3000, 0., 0.15)
    for value in xrange(0, int(r.gRandom.Poisson(mass_hist.Integral()))):
        rmass_hist.Fill(fit_function.GetRandom(0.01, 0.1))
    
    rmass_hist.SetLineColor(r.kRed)
    rmass_hist.Draw("")

    canvas.SaveAs("mass_overlay.pdf")

if __name__ == "__main__":
    main()
