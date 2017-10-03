#!/usr/bin/env python

from __future__ import division

import argparse
import collections
import sys
import math
import numpy as np
import Plotter
import root_numpy as rnp
import ROOT as r

def main() :

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", "--file_list", help="List of ROOT ntuples to process.")
    parser.add_argument("-i", "--file",      help="ROOT ntuple to process.")
    parser.add_argument("-r", "--run",       help="Run number of the file that is being processed.")
    parser.add_argument("-l", "--lumi_file", help="Path to file containing Luminosities.")
    args = parser.parse_args()

    # If a file hasn't been specified, warn the user and exit.
    if ((not args.file_list) and (not args.file)):
        parser.error('Please specify a file to process.')

    # Open the file containing the list of files to process
    root_files = []
    if args.file_list: 
        root_file_list = None
        try:
            root_file_list = open(args.file_list, 'r')
        except IOError: 
            print "Unable to open file %s" % args.file_list
            sys.exit(2)
    
        for line in root_file_list: 
            root_files.append(line.strip())
    else: 
        root_files.append(args.file.strip())

    rec = rnp.root2array(root_files, 'results')
    
    lumis = np.genfromtxt(args.lumi_file.strip(), 
                          dtype=[('run', 'f8'), ('lumi', 'f8')], 
                          delimiter=',')
    run_index = np.where(lumis['run'] == float(args.run))[0]
    lumi = lumis['lumi'][run_index]

    output_prefix = '%s_trident_selection' % args.run

    apply_tri_selection(rec, lumi, output_prefix)

def save_to_root(plt, name, hists, x_label, bins, min_x, max_x, labels, **params): 
    for index in xrange(0, len(hists)):
            if 'lumi' in params: 
                plt.create_root_hist('%s - %s' % (name, labels[index]), 
                    hists[index], bins, min_x, max_x, x_label, 
                    lumi=params['lumi'])
            else:
                plt.create_root_hist('%s - %s' % (name, labels[index]), 
                    hists[index], bins, min_x, max_x, x_label) 

def apply_tri_selection(rec, lumi, output_prefix):

    electron_p      = rec['electron_p']
    electron_px     = rec['electron_px']
    electron_py     = rec['electron_py']
    electron_chi2   = rec['electron_chi2']
    electron_pt = np.sqrt(np.power(electron_px, 2) + np.power(electron_py, 2))
    
    positron_p      = rec['positron_p']
    positron_px     = rec['positron_px']
    positron_py     = rec['positron_py']
    positron_chi2   = rec['positron_chi2']
    positron_d0     = rec['positron_d0']
    positron_has_l1 = rec['positron_has_l1']
    positron_has_l2 = rec['positron_has_l2']

    positron_pt = np.sqrt(np.power(positron_px, 2) + np.power(positron_py, 2))

    top_cluster_time  = rec['top_cluster_time']
    bot_cluster_time  = rec['bot_cluster_time']
    cluster_time_diff = top_cluster_time - bot_cluster_time
    
    top_time = rec['top_time']
    
    bot_time = rec['bot_time']

    mass = rec['invariant_mass']

    v0_p = rec["v0_p"]
    v_chi2 = rec['v_chi2']

    top_track_cluster_dt = top_cluster_time - top_time
    abs_top_track_cluster_dt = np.absolute(top_track_cluster_dt - 43)
    bot_track_cluster_dt = bot_cluster_time - bot_time
    abs_bot_track_cluster_dt = np.absolute(bot_track_cluster_dt - 43)
    track_cluster_dt_cut = ((abs_top_track_cluster_dt < 5.8) 
                            & (abs_bot_track_cluster_dt < 5.8))

    asym = (electron_pt - positron_pt)/(electron_pt + positron_pt)
    #
    # Define cuts
    #
    cuts = collections.OrderedDict()

    # Base cuts used to reduce accidentals
    cuts['FEE cut'] = electron_p < 0.75*1.056 # GeV
    cuts['Radiative cut'] = v0_p > 0.8*1.056 # GeV
    cuts['abs(Ecal clust time - trk time) - 43 ns < 5.8'] = track_cluster_dt_cut
    cuts['$p(V_0) < 1.2 E_{beam}$'] = v0_p < 1.18*1.056 # GeV
    cuts['trk $\chi^2$ < 40'] = (electron_chi2 < 40) & (positron_chi2 < 40)
    cuts['vtx $\chi^2$ < 75'] = v_chi2 < 75 
    cuts['Ecal clust pair dt < 2 ns'] = np.absolute(cluster_time_diff) < 2
    cuts['l1 & l2 hit'] = (positron_has_l1 == 1) & (positron_has_l2 == 1)
    cuts['$d_{0}(e^+) < 1.1$'] = positron_d0 < 1.1
    cuts['$p_t(e^-) - p_t(e^+)/p_t(e^-) + p_t(e^+)$'] = asym < .47
    
    labels = ['Opp. Ecal clusters, trk-cluster match $\chi^2 < 10$, $p(e^-)<0.75E_{beam}$']
   
    cut_flow = {}
    for name in rec.dtype.names: 
        cut_flow[name] = [rec[name]]

    cut_flow['cluster_time_diff'] = [cluster_time_diff]
    cut_flow['asym'] = [asym]
    cut_flow['abs_top_cluster_dt'] = [abs_top_track_cluster_dt]

    cut = np.ones(len(v0_p), dtype=bool)
    for key, value in cuts.iteritems():
        cut = cut & value
        
        for name in rec.dtype.names: 
            cut_flow[name].append(rec[name][cut])

        cut_flow['cluster_time_diff'].append(cluster_time_diff[cut])
        cut_flow['asym'].append(asym[cut])
        cut_flow['abs_top_cluster_dt'].append(abs_top_track_cluster_dt[cut])

        labels.append(key)

    plt = Plotter.Plotter(output_prefix)
    
    plt.plot_hists(cut_flow['cluster_time_diff'], 
                   np.linspace(-10, 10, 201),
                   labels=labels,
                   label_loc=10, 
                   x_label='Top cluster time - Bottom cluster time (ns)',
                   norm=True,
                   ylog=True)

    save_to_root(plt, 'cluster_time_diff', cut_flow['cluster_time_diff'],
            'Top cluster time - Bottom cluster time (ns)',
            200, -10, 10, labels, lumi=lumi)

    plt.plot_hists(cut_flow['abs_top_cluster_dt'],
                   np.linspace(0, 60, 121),
                   labels=labels,
                   x_label='abs(ECal cluster time - track time - 43) ns',
                   label_loc=10,
                   ylog=True)

    save_to_root(plt, 'cluster_track_time_diff', cut_flow['abs_top_cluster_dt'],
            'abs(ECal cluster time - track time - 43) ns',
            120, 0, 60, labels, lumi=lumi)

    plt.plot_hists(cut_flow['invariant_mass'], 
                   np.linspace(0, 0.15, 501),
                       labels=labels,
                       label_loc=10,
                       ylog=True,
                       x_label='$m(e^-e^-)$ GeV')

    save_to_root(plt, 'mass', cut_flow['invariant_mass'], 'm(e^{-}e^{-}) GeV', 
            500, 0, .15, labels, lumi=lumi)

    #
    # V0 particle plots
    #

    plt.plot_hists(cut_flow['v0_p'], 
                   np.linspace(0, 1.5, 151),
                   labels=labels,
                   label_loc=10,
                   ylog=True,
                   x_label='$V_{0}(p)$ (GeV)')

    save_to_root(plt, 'v0_p', cut_flow['v0_p'], 'V_{0}(p) (GeV)',
            150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['v0_px'], 
                   np.linspace(-0.1, 0.1, 101),
                       labels=labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p_{x}(V_{0})$ (GeV)')

    save_to_root(plt, 'v0_px', cut_flow['v0_px'], 'p_{x}(V_{0}) (GeV)',
            100, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['v0_py'], 
                       np.linspace(-0.1, 0.1, 101),
                       labels=labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p_{y}(V_{0})$ (GeV)')

    save_to_root(plt, 'v0_py', cut_flow['v0_py'], 'p_{y}(V_{0}) (GeV)',
            100, -0.1, 0.1, labels, lumi=lumi)
    
    plt.plot_hists(cut_flow['v0_pz'], 
                       np.linspace(0, 2.0, 201),
                       labels=labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$p_{z}(V_{0})$ (GeV)')

    save_to_root(plt, 'v0_pz', cut_flow['v0_pz'], 'p_{z}(V_{0}) (GeV)',
            200, 0, 2.0, labels, lumi=lumi)
    #
    # Vertex plots
    #

    plt.plot_hists(cut_flow['v_chi2'], 
                   np.linspace(0, 100, 101),
                   labels=labels,
                   ylog=True,
                   label_loc=10,
                   x_label='$V_{0}$ Vertex Fit $\chi^{2}$')

    save_to_root(plt, 'v_chi2', cut_flow['v_chi2'], 'V_{0} Vertex Fit #chi^{2}',
            200, 0, 200, labels, lumi=lumi)

    plt.plot_hists(cut_flow['vx'], 
                       np.linspace(-1, 1, 101),
                       labels=labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ Vertex x (mm)')

    save_to_root(plt, 'vx', cut_flow['vx'], 'V_{0} Vertex x (mm)',
            100, -1, 1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['vy'], 
                       np.linspace(-1, 1, 101),
                       labels=labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ y (mm)')

    save_to_root(plt, 'vy', cut_flow['vy'], 'V_{0} Vertex y (mm)',
            100, -1, 1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['vz'], 
                       np.linspace(-1, 1, 101),
                       labels=labels,
                       ylog=True,
                       label_loc=10,
                       x_label='$v_{0}$ z (mm)')

    save_to_root(plt, 'vz', cut_flow['vz'], 'V_{0} Vertex z (mm)',
            100, -1, 1, labels, lumi=lumi)
    #
    # Electron
    #

    plt.plot_hists(cut_flow['electron_chi2'], 
                   np.linspace(0, 100, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Track $\chi^2$') 

    save_to_root(plt, 'electron_chi2', cut_flow['electron_chi2'],
                 'Track #chi^2', 200, 0, 100, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_d0'], 
                   np.linspace(-10, 10, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron d0 (mm)') 

    save_to_root(plt, 'electron_d0', cut_flow['electron_d0'],
                 'Electron d0 (mm)', 200, -10, 10, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_phi0'], 
                   np.linspace(-0.1, 0.3, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron $\phi_{0}$ (rad)') 

    save_to_root(plt, 'electron_phi0', cut_flow['electron_phi0'],
                 'Electron #phi_{0} (mm)', 200, -0.1, 0.3, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_omega'], 
                   np.linspace(0, 0.0007, 141),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron $\Omega$') 

    save_to_root(plt, 'electron_omega', cut_flow['electron_omega'],
                 'Electron #Omega', 140, 0, 0.00007, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_tan_lambda'], 
                   np.linspace(-0.1, 0.1, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron tan($\lambda$)') 

    save_to_root(plt, 'electron_tan_lambda', 
                 cut_flow['electron_tan_lambda'],
                 'Electron tan(#lambda)', 200, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_z0'], 
                   np.linspace(-5, 5, 101),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron Z$_{0}$ (mm)') 

    save_to_root(plt, 'electron_z0', 
                 cut_flow['electron_z0'],
                 'Electron Z_{0}', 100, -5, 5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_p'], 
                   np.linspace(0, 1.5, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p(e^-)$ (GeV)')

    save_to_root(plt, 'electron_p', cut_flow['electron_p'],
                 'p(e^-) (GeV)', 150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_px'], 
                   np.linspace(-0.1, 0.1, 101), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p_{x}(e^-)$ (GeV)')

    save_to_root(plt, 'electron_px', cut_flow['electron_px'],
                 'p_x(e^-) (GeV)', 100, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_py'], 
                   np.linspace(-0.1, 0.1, 101), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p_{y}(e^-)$ (GeV)')

    save_to_root(plt, 'electron_py', cut_flow['electron_py'],
                 'p_y(e^-) (GeV)', 100, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_pz'], 
                   np.linspace(0, 1.5, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p_{z}(e^-)$ (GeV)')

    save_to_root(plt, 'electron_pz', cut_flow['electron_pz'],
                 'p_z(e^-) (GeV)', 150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_time'], 
                   np.linspace(-15, 15, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron time (ns)')

    save_to_root(plt, 'electron_time', cut_flow['electron_time'],
                 'Electron time (ns)', 150, -15, 15, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_cluster_energy'], 
                   np.linspace(0, 1.5, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron cluster energy (GeV)')

    save_to_root(plt, 'electron_cluster_energy', 
                 cut_flow['electron_cluster_energy'],
                 'Electron cluster energy (GeV)',
                 150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_cluster_time'], 
                   np.linspace(0, 100, 101), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron cluster time (ns)')

    save_to_root(plt, 'electron_cluster_time', 
                 cut_flow['electron_cluster_time'],
                 'Electron cluster time (ns)',
                 100, 0, 100, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_cluster_x'], 
                   np.linspace(-300, 100, 401), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron cluster x (mm)')

    save_to_root(plt, 'electron_cluster_x', 
                 cut_flow['electron_cluster_x'],
                 'Electron cluster x (mm)',
                 400, -300, 100, labels, lumi=lumi)

    plt.plot_hists(cut_flow['electron_cluster_y'], 
                   np.linspace(-100, 100, 201), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Electron cluster y (mm)')

    save_to_root(plt, 'electron_cluster_y', 
                 cut_flow['electron_cluster_y'],
                 'Electron cluster y (mm)',
                 200, -100, 100, labels, lumi=lumi)


    #
    # Positron
    #

    plt.plot_hists(cut_flow['positron_chi2'], 
                   np.linspace(0, 100, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$e^{+}$ Track $\chi^2$') 

    save_to_root(plt, 'positron_chi2', cut_flow['positron_chi2'],
                 'e^{+} Track #chi^2', 200, 0, 100, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_d0'], 
                   np.linspace(-10, 10, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron d0 (mm)') 

    save_to_root(plt, 'positron_d0', cut_flow['positron_d0'],
                 'Positron d0 (mm)', 200, -10, 10, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_phi0'], 
                   np.linspace(-0.2, 0.2, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron $\phi_{0}$ (rad)') 

    save_to_root(plt, 'positron_phi0', cut_flow['positron_phi0'],
                 'Positron #phi_{0} (mm)', 200, -0.2, 0.2, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_omega'], 
                   np.linspace(-0.0007, 0, 141),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron $\Omega$') 

    save_to_root(plt, 'positron_omega', cut_flow['positron_omega'],
                 'Positron #Omega', 140, -0.00007, 0, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_tan_lambda'], 
                   np.linspace(-0.1, 0.1, 201),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron tan($\lambda$)') 

    save_to_root(plt, 'positron_tan_lambda', 
                 cut_flow['positron_tan_lambda'],
                 'Positron tan(#lambda)', 200, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_z0'], 
                   np.linspace(-5, 5, 101),
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron Z$_{0}$ (mm)') 

    save_to_root(plt, 'positron_z0', 
                 cut_flow['positron_z0'],
                 'Positron Z_{0}', 100, -5, 5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_p'], 
                   np.linspace(0, 1.5, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p(e^{+})$ (GeV)')

    save_to_root(plt, 'positron_p', cut_flow['positron_p'],
                 'p(e^{+}) (GeV)', 150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_px'], 
                   np.linspace(-0.1, 0.1, 101), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p_{x}(e^{+})$ (GeV)')

    save_to_root(plt, 'positron_px', cut_flow['positron_px'],
                 'p_x(e^{+}) (GeV)', 100, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_py'], 
                   np.linspace(-0.1, 0.1, 101), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p_{y}(e^{+})$ (GeV)')

    save_to_root(plt, 'positron_py', cut_flow['positron_py'],
                 'p_y(e^{+}) (GeV)', 100, -0.1, 0.1, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_pz'], 
                   np.linspace(0, 1.5, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='$p_{z}(e^{+})$ (GeV)')

    save_to_root(plt, 'positron_pz', cut_flow['positron_pz'],
                 'p_z(e^{+}) (GeV)', 150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_time'], 
                   np.linspace(-15, 15, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron time (ns)')

    save_to_root(plt, 'positron_time', cut_flow['positron_time'],
                 'Positron time (ns)', 150, -15, 15, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_cluster_energy'], 
                   np.linspace(0, 1.5, 151), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron cluster energy (GeV)')

    save_to_root(plt, 'positron_cluster_energy', 
                 cut_flow['positron_cluster_energy'],
                 'Positron cluster energy (GeV)',
                 150, 0, 1.5, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_cluster_time'], 
                   np.linspace(0, 100, 101), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron cluster time (ns)')

    save_to_root(plt, 'positron_cluster_time', 
                 cut_flow['positron_cluster_time'],
                 'Positron cluster time (ns)',
                 100, 0, 100, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_cluster_x'], 
                   np.linspace(-100, 500, 601), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron cluster x (mm)')

    save_to_root(plt, 'positron_cluster_x', 
                 cut_flow['positron_cluster_x'],
                 'Positron cluster x (mm)',
                 500, -100, 400, labels, lumi=lumi)

    plt.plot_hists(cut_flow['positron_cluster_y'], 
                   np.linspace(-100, 100, 201), 
                   labels=labels, 
                   label_loc=10, 
                   ylog=True,
                   x_label='Positron cluster y (mm)')

    save_to_root(plt, 'positron_cluster_y', 
                 cut_flow['positron_cluster_y'],
                 'Positron cluster y (mm)',
                 200, -100, 100, labels, lumi=lumi)

    #
    # Other plots
    #

    plt.plot_hists(cut_flow['asym'], 
                   np.linspace(-1, 1, 201),
                   labels=labels, 
                   x_label='$p_t(e^-) - p_t(e^+)/p_t(e^-) + p_t(e^+)$',
                   label_loc=10, 
                   ylog=True)

    plt.close()
    

    file = r.TFile("%s_invariant_mass.root" % output_prefix, "recreate")

    mass_histo = r.TH1F("invariant_mass", "invariant_mass", 3000, 0., 0.15)
    #mass_histo = r.TH1F("invariant_mass", "invariant_mass", 50, 0., 0.1)
    mass_histo.GetXaxis().SetTitle("m(e^+e^-) (GeV)")
    bin_width = mass_histo.GetXaxis().GetBinWidth(1)
        
    #rnp.fill_hist(mass_histo, mass[cut], weights=weights)    
    rnp.fill_hist(mass_histo, mass[cut])    
    mass_histo.Write()
    file.Close()


if __name__ == "__main__" : 
    main()
