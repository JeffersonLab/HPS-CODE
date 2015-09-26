#!/usr/bin/python

#
# @file analysis_pyroot_example.py
# @section purpose:
#       A simple PyRoot analysis demonstrating the use of a DST to make simple
#       plots of Ecal, SVT and Particle objects
#
# @author Omar Moreno <omoreno1@ucsc.edu>
#         Santa Cruz Institute for Particle Physics
#         University of California, Santa Cruz
# @date March 29, 2013
#

#---------------#
#--- imports ---#
#---------------#
import sys
import math
import argparse
import os
#ROOT.PyConfig.IgnoreCommandLineOptions = True

#-----------------#
#--- Functions ---#
#-----------------#

def setupCanvas(canvas):
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetBorderSize(0)
    canvas.SetFrameFillColor(0)
    canvas.SetFrameBorderMode(0)

def setup1DHistogram(histo, x_axis_title):
    histo.SetStats(0)
    histo.GetXaxis().SetTitle(x_axis_title)
    histo.GetXaxis().SetTitleSize(0.03)
    histo.GetXaxis().SetLabelSize(0.03)
    histo.GetYaxis().SetTitleSize(0.03)
    histo.GetYaxis().SetLabelSize(0.03)

def setup2DHistogram(histo, x_axis_title, y_axis_title):
    histo.GetYaxis().SetTitle(y_axis_title)
    setup1DHistogram(histo, x_axis_title)

#------------------#

#------------#
#--- Main ---#
#------------#

def main():


    # Parse all command line arguments using the argparse module.
    parser = argparse.ArgumentParser(description='PyRoot analysis demostrating the use of a DST.')
    parser.add_argument("dst_file",  help="ROOT DST file to process")
    parser.add_argument("-o", "--output",  help="Name of output pdf file")
    args = parser.parse_args()

    # If an output file name was not specified, set a default name and warn
    # the user 
    if args.output:
        output_file = args.output
    else: 
        output_file = "analysis_output.pdf"
        print "[ HPS ANALYSIS ]: An output file name was not specified. Setting the name to " 
        print output_file

    # Load the HpsEvent library.  In this example, this is done by finding the
    # path to the HpsEvent shared library via the environmental variable
    # HPS_DST_PATH.  The HPS_DST_PATH environmental variable points to the
    # location of the build directory containing all binaries and libraries.
    # In general, the location of the library can be anywhere a user wants it
    # to be as long as the proper path is specified. 
    if os.getenv('HPS_DST_PATH') is None: 
        print "[ HPS ANALYSIS ]: Error! Environmental variable HPS_DST_HOME is not set."
        print "\n[ HPS ANALYSIS ]: Exiting ..."
        sys.exit(2)

    hps_dst_path = os.environ['HPS_DST_PATH']
    hps_dst_path += "/build/lib/libHpsEvent.so"
   
    # Load the library in ROOT
    import ROOT
    ROOT.gSystem.Load(hps_dst_path)

    # import the modules used by HpsEvent i.e. HpsEvent, 
    # SvtTrack, EcalCluster ...
    from ROOT import HpsEvent, SvtTrack, EcalCluster, EcalHit, HpsParticle

    #-----------------------------#
    #--- Setup ROOT histograms ---#
    #-----------------------------#

    # Create a canvas and set its characteristics
    canvas = ROOT.TCanvas("canvas", "Data Summary Tape Plots", 700, 700)
    setupCanvas(canvas)

    #
    # Ecal
    #
    h_hit_pos = ROOT.TH2F("cluster_pos", "ECal cluster position", 47, -23, 24, 12, -6, 6)
    setup2DHistogram(h_hit_pos, "Ecal Crystal Index - x", "Ecal Crystal Index - y")
    
    h_cluster_energy = ROOT.TH1F("cluster_energy", "Ecal Cluster Energy", 100, 0, 5.5)
    setup1DHistogram(h_cluster_energy, "Ecal Cluster Energy [GeV]")

    #
    # Track parameters and momentum
    #
    h_d0 = ROOT.TH1F("d0",  "Track D0", 80, -10, 10);
    setup1DHistogram(h_d0, "D0 [mm]")
    
    h_z0 = ROOT.TH1F("z0", "Track Z0", 80, -2, 2);
    setup1DHistogram(h_z0, "Z0 [mm]")
    
    h_sinphi0 = ROOT.TH1F("sin(phi0)", "Track sin(#phi_{0})", 40, -0.2, 0.2)
    setup1DHistogram(h_sinphi0, "sin(#phi_{0})")

    h_curvature = ROOT.TH1F("curvature", "Track Curvature", 50, -0.001, 0.001)
    setup1DHistogram(h_curvature, "Curvature")
    
    h_tlambda = ROOT.TH1F("tlambda",  "Track Tan(#lambda)", 64, -0.08, 0.08);
    setup1DHistogram(h_tlambda, "Tan #lambda")
    
    h_p = ROOT.TH1F("p", "Particle Momentum", 64, 0, 2.2);
    setup1DHistogram(h_p, "Momentum [GeV]")  
    
    h_chi2 = ROOT.TH1F("chi2", "Track #chi^{2}", 25, 0, 25);
    setup1DHistogram(h_chi2, "#chi^{2}")

    #
    # Particles
    #
    h_invariant_mass = ROOT.TH1F("invariant mass", "Invariant Mass", 100, 0, 0.200)
    setup1DHistogram(h_invariant_mass, "Invariant Mass [GeV]")

    h_vertex_z = ROOT.TH1F("h_vertex_z", "Particle Vertex - Z", 150, -150, 150); 
    setup1DHistogram(h_vertex_z, "Vertex z [mm]")

    h_epem = ROOT.TH2F("p[e+] v p[e-]", "p[e+] v p[e-]", 50, 0, 2.0, 50, 0, 2.0)
    setup2DHistogram(h_epem, "p[e-]", "p[e+]")

    #-----------------------------#

    # Open the ROOT file
    root_file = ROOT.TFile(str(args.dst_file))

    # Get the TTree "HPS_EVENT" containing the HpsEvent branch and all
    # other colletions
    tree = root_file.Get("HPS_Event")

    # Create an HpsEvent object in order to read the TClonesArray 
    # collections
    hps_event = HpsEvent()

    # Get the HpsEvent branch from the TTree 
    b_hps_event = tree.GetBranch("Event")
    b_hps_event.SetAddress(ROOT.AddressOf(hps_event))

    #--- Analysis ---#
    #----------------#

    # Loop over all events in the file
    for entry in xrange(0, tree.GetEntries()) : 

        # Print the event number every 500 events
        if (entry+1)%500 == 0 : print "Event " + str(entry+1)

        # Read the ith entry from the tree.  This "fills" HpsEvent and allows 
        # access to all collections
        tree.GetEntry(entry)

        # Loop over all of the Ecal clusters in the event
        for cluster_n in xrange(0, hps_event.getNumberOfEcalClusters()):

            # Get an Ecal cluster from the event
            ecal_cluster = hps_event.getEcalCluster(cluster_n)

            # Get the Ecal cluster energy
            cluster_energy = ecal_cluster.getEnergy()

            # Fill the cluster energy plot
            h_cluster_energy.Fill(cluster_energy)

            # Get the seed hit of the cluster
            ecal_cluster_seed_hit = ecal_cluster.getSeed()

            # Get the crystal index of the ecal hit
            index_x = ecal_cluster_seed_hit.getXCrystalIndex()
            index_y = ecal_cluster_seed_hit.getYCrystalIndex()

            # Fill the Ecal hit position plot
            h_hit_pos.Fill(index_x, index_y, 1)

        # Loop over all tracks in the event
        for track_n in xrange(0, hps_event.getNumberOfTracks()) : 

            # Get the track from the event
            track = hps_event.getTrack(track_n)

            # Get the track parameters 
            d0 = track.getD0()
            z0 = track.getZ0()
            sinphi0 = math.sin(track.getPhi0())
            curvature = track.getOmega()
            tan_lambda = track.getTanLambda()
            chi2 = track.getChi2()

            # Fill the plots
            h_d0.Fill(d0)
            h_z0.Fill(z0)
            h_sinphi0.Fill(sinphi0)
            h_curvature.Fill(curvature)
            h_tlambda.Fill(tan_lambda)
            h_chi2.Fill(chi2)

            # Get the track momentum and fill the plots.  The track momentum
            # is retrieved from the associated HpsParticle.
            p = track.getMomentum()
            h_p.Fill(math.sqrt(p[0]*p[0] + p[1]*p[1] + p[2]*p[2]))

        # Loop over all unconstrained vertexed particles in the event
        for particle_n in xrange(0, hps_event.getNumberOfParticles(HpsParticle.UC_V0_CANDIDATE)):

            # Get a vertexed particle from the event
            particle = hps_event.getParticle(HpsParticle.UC_V0_CANDIDATE, particle_n)
           
            # Only look at particles that have two daugther particles
            daughter_particles = particle.getParticles()
            if daughter_particles.GetSize() != 2 : continue

            # Only look at particles that are composed of e+e- pairs
            if daughter_particles.At(0).getCharge()*daughter_particles.At(1).getCharge() > 0 : continue

            # Get the vertex position of the particle and plot it
            vertex_z = particle.getVertexPosition()[2]
            h_vertex_z.Fill(vertex_z)

            # Get the invariant mass of the particle and plot it
            mass = particle.Mass()
            h_invariant_mass.Fill(mass)

            # Get the momentum of both the daughter particles and plot them
            p1 = daughter_particles.At(0).getMomentum()
            p_mag_1 = math.sqrt(p1[0]*p1[0] + p1[1]*p1[1] + p1[2]*p1[2])

            p2 = daughter_particles.At(1).getMomentum()
            p_mag_2 = math.sqrt(p2[0]*p2[0] + p2[1]*p2[1] + p2[2]*p2[2])

            if daughter_particles.At(0).getCharge() < 0 :
                h_epem.Fill(p_mag_1, p_mag_2)
            else :
                h_epem.Fill(p_mag_2, p_mag_1)

    # Save all the plots to a single pdf file
    h_hit_pos.Draw("colz")
    canvas.Print(output_file + "(")
    h_cluster_energy.Draw()
    canvas.Print(output_file + "(")
    h_d0.Draw("");
    canvas.Print(output_file + "(");
    h_z0.Draw("");
    canvas.Print(output_file + "(");
    h_sinphi0.Draw("");
    canvas.Print(output_file + "(");
    h_curvature.Draw("");
    canvas.Print(output_file + "(");
    h_tlambda.Draw(""); 
    canvas.Print(output_file + "(");
    h_chi2.Draw("");
    canvas.Print(output_file + "(");
    h_p.Draw(""); 
    canvas.Print(output_file + "(");
    h_vertex_z.Draw("");
    canvas.Print(output_file + "(");
    h_invariant_mass.Draw(""); 
    canvas.Print(output_file + "(");
    h_epem.Draw("colz"); 
    canvas.Print(output_file + ")")

if __name__ == "__main__":
    main()



