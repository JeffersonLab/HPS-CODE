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
    parser.add_argument('-i', "--file", 
                        help='File containing invariant mass histogram to process.')
    parser.add_argument('-t', "--toys", 
                        help='Number of toys to generate.')
    parser.add_argument('-s', '--start', 
                        help='Number to start toy naming.')
    parser.add_argument('-e', '--events', 
                        help='Number of events to generate')
    args = parser.parse_args()

    if not args.file:
        parser.error('Please specify a file to process.')

    r.gStyle.SetOptStat(0)
    r.gStyle.SetOptFit(1)
    r.gStyle.SetStatX(1)
    r.gStyle.SetStatY(1)
   
    fte_blue = r.TColor(0, 143, 213)
    fte_orange = r.TColor(252, 79, 48)

    rfile = root_open(args.file)
    mass_hist = rfile.invariant_mass

    fit_function = r.TF1("function", mass_function , 0.01, 0.09, 11)
    fit_function.SetParameters(2000,0.015,0,0,0,0,0,0,0,0,0);
    
    # Fit parameters for full dataset
    #fit_function = r.TF1("function", mass_function , 0.013, 0.099, 11)
    #fit_function.SetParameters(10000,0.01,0,0,0,0,0,0,0,0,0);

    mass_hist.Fit("function", "R")
    mass_hist.Fit("function", "R")
    mass_hist.Fit("function", "R")

    canvas = r.TCanvas("canvas", "canvas", 800, 800)
    canvas.SetLogy()
   
    fit_function.SetLineColor(fte_orange.GetNumber())
    fit_function.SetLineWidth(3)
    fit_function.SetRange(0.014, 0.115)
    
    mass_hist.SetLineColor(fte_blue.GetNumber())
    mass_hist.SetMarkerColor(fte_blue.GetNumber())
    mass_hist.SetTitle("")
    mass_hist.GetXaxis().SetTitle("#font[12]{m(e^{+}e^{-})} GeV")
    mass_hist.GetXaxis().CenterTitle()
    mass_hist.Draw()

    # Get the number of events in the range of interest
    bmin = mass_hist.GetXaxis().FindBin(0.014)
    bmax = mass_hist.GetXaxis().FindBin(0.115)
    bmin_center = mass_hist.GetXaxis().GetBinCenter(bmin)
    bmax_center = mass_hist.GetXaxis().GetBinCenter(bmax)
    

    integral = mass_hist.Integral(bmin, bmax)
    if args.events:
        integral = int(args.events) 
    print 'Total number of events to sample: %s' % integral

    canvas.SaveAs("mass_global_fit.pdf")
    rfile.Close()    

    seed = int(time.time())
    r.gRandom.SetSeed() 

    start = 0 if not args.start else int(args.start)
    
    # Initialize the random number generator
    rfile = r.TFile("toy_distributions_seed%s_start%s.root" % (seed, start) , "recreate")
    
    for itoy in xrange(0, int(args.toys)):
        print 'Generating toy histogram %s' % itoy
        rmass_hist = r.TH1F('invariant_mass_%s' % (itoy + start), 'invariant_mass_%s' % (itoy + start), 3000, 0., 0.15)
        for value in xrange(0, int(r.gRandom.Poisson(integral))):
            rmass_hist.Fill(fit_function.GetRandom(bmin_center, bmax_center))
    
        rmass_hist.SetTitle("")
        rmass_hist.GetXaxis().SetTitle("#font[12]{m(e^{+}e^{-})} GeV")
        rmass_hist.GetXaxis().CenterTitle()
    
        rmass_hist.Write()

    rfile.Close()

if __name__ == "__main__":
    main()
