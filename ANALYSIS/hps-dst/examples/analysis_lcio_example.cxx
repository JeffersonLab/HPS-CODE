/**
 * @file analysis_lcio_example.cxx
 * @section purpose
 *      A simple analysis demonstrating the use of a recon LCIO
 *      file to make simple plots of Ecal and SVT physics objects.
 *
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *           Santa Cruz Institute for Particle Physics
 *           University of California, Santa Cruz
 * @date March 14, 2013
 */             

//-----------//
//--- C++ ---//
//-----------//
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <unistd.h>

//-------------//
//--- ROOT ---//
//-------------//
#include <TCanvas.h>
#include <TH1F.h>
#include <TH2F.h>

//-------------//
//--- LCIO ---//
//-------------//
#include <IO/LCReader.h>
#include <IOIMPL/LCFactory.h>
#include <EVENT/LCEvent.h>
#include <IMPL/LCCollectionVec.h>
#include <IMPL/TrackImpl.h>
#include <IMPL/ClusterImpl.h>
#include <IMPL/CalorimeterHitImpl.h>
#include <IMPL/ReconstructedParticleImpl.h>
#include <UTIL/BitField64.h>
#include <Exceptions.h>

using namespace std; 

typedef long long long64;

void printUsage();
void setup1DHistogram(TH1*,  string);
void setup2DHistogram(TH1*, string, string);
UTIL::BitFieldValue getIdentifierFieldValue(string, EVENT::CalorimeterHit*);

int main( int argc, char **argv) {


    // Name of the recon LCIO file that is going to be processed
    string lcio_file_name = "";
    // Name of the pdf file that all root plots will be saved to
    string pdf_file_name = "";

    // The number of events to process
    int n_events = 0;
    int option_char;

    // Parse any command line arguments. If there are no valid command line
    // arguments given, print the usage.
    while ((option_char = getopt(argc, argv, "i:o:n:")) != -1) {
        switch(option_char) {
            case 'i':
                lcio_file_name = optarg;
                break;
            case 'o':
                pdf_file_name = optarg;
                break;
            case 'n':
                n_events = atoi(optarg);
                break;
            default:
                printUsage(); 
                return EXIT_FAILURE;
        }
    }

    // If an lcio input file name was not specified, exit gracefully
    if (lcio_file_name.length() == 0) {
        cerr << "\nPlease specify an LCIO file to process."
             << "\n Use the -h flag for usage\n" << endl;
        return EXIT_FAILURE;
    }

    // If an output file name was not specified, set a default name and warn
    // the user
    if (pdf_file_name.length() == 0) {
        pdf_file_name = "analysis_output.pdf";
        cout << "An output file name was not specified. Setting the name to "
             << pdf_file_name << endl;
    }

    // Parameters used to calculate the momentum of a track.
    // TODO: Obtain the B field from the event
    const double param = 2.99792458e-04;
    const float b_field = -0.491;

    // The name of the LCIO collections.  The names of the collections
    // can be obtained using JAS or by running the dump_hps_event
    // executable.
    const string tracks_collection_name = "MatchedTracks";
    const string fs_recon_particles_collection_name = "FinalStateParticles";
    const string ecal_clusters_collection_name = "EcalClusters";

    //-- Setup ROOT histograms ---//
    //----------------------------//

    // Create a canvas and set its characteristics
    TCanvas *canvas = new TCanvas("canvas", "Track Momentum", 700, 700);
    canvas->SetFillColor(0);
    canvas->SetBorderMode(0);
    canvas->SetBorderSize(0);
    canvas->SetFrameFillColor(0);
    canvas->SetFrameBorderMode(0);

    // Ecal
    TH2F* h_hit_pos = new TH2F("h_hit_pos", "Ecal Hit Positions", 47, -23, 24, 12, -6, 6);
    setup2DHistogram(h_hit_pos, "Ecal Hit Index - x", "Ecal Hit Index - y");
    TH1F* h_cluster_energy = new TH1F("h_cluster_energy", "Ecal Cluster Energy", 100, 0, 5.5);
    setup1DHistogram(h_cluster_energy, "Ecal Cluster Energy [GeV]");

    // Tracking
    TH1F *h_pt  = new TH1F("h_pt", "Transverse Momentum - All Tracks", 100, 0, 5.5);
    setup1DHistogram(h_pt, "Transverse Momentum [GeV]");
    TH1F *h_p   = new TH1F("h_p",  "Momentum - All Tracks", 100, 0, 5.5);
    setup1DHistogram(h_p, "Momentum [GeV]");
    TH1F *h_px  = new TH1F("h_px", "p_{x} - All Tracks", 100, 0, 5.5);
    setup1DHistogram(h_px, "p_{x} [GeV]");
    TH1F *h_py  = new TH1F("h_py", "p_{y} - All Tracks", 40, -.2, .2);
    setup1DHistogram(h_py, "p_{y} Momentum [GeV]");
    TH1F *h_pz  = new TH1F("h_pz", "p_{z} - All Tracks", 40, -.2, .2);
    setup1DHistogram(h_pz, "p_{z} Momentum [GeV]");

    //-----------------------------//

    // Create the LCIO reader and open the LCIO file. If the file doesn't exist
    // or can't be opened, notify the user and exit
    IO::LCReader *lc_reader = IOIMPL::LCFactory::getInstance()->createLCReader();
    try {
        lc_reader->open(lcio_file_name.c_str());
    } catch(IO::IOException &e) {
        cout << "File " << lcio_file_name << " cannot be opened!" << endl;
        return EXIT_FAILURE;
    }

    EVENT::LCEvent *event  = 0;
    IMPL::TrackImpl* track = 0;
    IMPL::LCCollectionVec* tracks = 0;
    IMPL::LCCollectionVec* clusters = 0;
    IMPL::ClusterImpl* cluster = 0;
    IMPL::CalorimeterHitImpl* calorimeter_hit;
    IMPL::LCCollectionVec* recon_particles = 0;
    double pt, px, py, pz, p;
    double cluster_energy;
    int index_x, index_y;
    int event_number = 0;

    //--- Analysis ---//
    //----------------//

    // Loop over all events in the file
    while ( (event = lc_reader->readNextEvent()) ) {
        ++event_number;

        // If the desired number of events have been processed, skip the rest
        if (n_events == event_number) break;

        // Print the event number every 500 events
        if (event_number%500 == 0) {
            cout << "Event: " << event_number << endl;
        }

        // Get the collection of Ecal clusters from the event. If the event doesn't
        // have the specified collection, skip the rest of the event.
        try {
            clusters = (IMPL::LCCollectionVec*) event->getCollection(ecal_clusters_collection_name);
        } catch(EVENT::DataNotAvailableException &e) {
            cout << "Collection " << ecal_clusters_collection_name << " was not found. "
                 << "Skipping event ..." << endl;
            continue;
        }

        // Loop over all of the Ecal clusters in the event
        for (int cluster_n = 0; cluster_n < clusters->getNumberOfElements(); ++cluster_n) {

            // Get a cluster from the LCIO collection
            cluster = (IMPL::ClusterImpl*) clusters->getElementAt(cluster_n);

            // Get the Ecal cluster energy
            cluster_energy = cluster->getEnergy();

            // Fill the cluster energy plot
            h_cluster_energy->Fill(cluster_energy);

            // Get the Ecal hits used to create the cluster
            EVENT::CalorimeterHitVec calorimeter_hits = cluster->getCalorimeterHits();

            // Loop through all of the Ecal hits and plot their positions
            for (int hit_n = 0; hit_n < (int) calorimeter_hits.size(); ++hit_n) {

                // Get an Ecal hit from the cluster
                calorimeter_hit = (IMPL::CalorimeterHitImpl*) calorimeter_hits[hit_n];

                // Get the crystal index of the ecal hit
                index_x = getIdentifierFieldValue("ix", calorimeter_hit);
                index_y = getIdentifierFieldValue("iy", calorimeter_hit);

                // Fill the Ecal hit position plot
                h_hit_pos->Fill(index_x, index_y, 1);

            }

        }

        // Get the collection of tracks from the event. If the event doesn't
        // have the specified collection, skip the rest of the event.
        try {
            tracks = (IMPL::LCCollectionVec*) event->getCollection(tracks_collection_name);
        } catch(EVENT::DataNotAvailableException &e) {
            cout << "Collection " << tracks_collection_name << " was not found. "
                 << "Skipping event ..." << endl;
            continue;
        }

        // Loop over all tracks in the event
        for (int track_n = 0; track_n < tracks->getNumberOfElements(); ++track_n) { 
                
            // Get a track from the LCIO collection
            track = (IMPL::TrackImpl*) tracks->getElementAt(track_n);
        
            // Calculate the transverse momentum of the track
            pt = abs((1/track->getOmega())*b_field*param);

            // Calculate the momentum components
            px = pt*cos(track->getPhi());
            py = pt*sin(track->getPhi());
            pz = pt*track->getTanLambda();

            // Calculate the momentum of the track
            p = sqrt(px*px + py*py + pz*pz);

            // Fil the plots
            h_pt->Fill(pt);
            h_p->Fill(p);
            h_px->Fill(px);
            h_py->Fill(py);
            h_pz->Fill(pz);
                
        }

        // Get the collection of final state recon particles from the event. If
        // the event doesn't have the specified collection, skip the rest of
        // the event
        try {
            recon_particles = (IMPL::LCCollectionVec*) event->getCollection(fs_recon_particles_collection_name);
        } catch(EVENT::DataNotAvailableException &e) {
            //cout << "Collection " << fs_recon_particles_collection_name << " was not found. "
            //   << "Skipping event ..." << endl;
            continue;
        }

        // Loop over all final state recon particles in the event
        for (int particle_n = 0; particle_n < recon_particles->getNumberOfElements(); ++particle_n) {

            //IMPL::ReconstructedParticleImpl* recon_particle 
            //    = (IMPL::ReconstructedParticleImpl*) recon_particles->getElementAt(particle_n);
            // Get the recon particle from the LCIO collection
        }
    }

    //------------------------//

    // Save all plots to a single pdf file
    h_hit_pos->Draw("colz");
    canvas->Print( (pdf_file_name + "(").c_str());
    h_cluster_energy->Draw("");
    canvas->Print( (pdf_file_name + "(").c_str());
    h_pt->Draw("");
    canvas->Print( (pdf_file_name + "(").c_str());
    h_p->Draw("");
    canvas->Print( (pdf_file_name + "(").c_str());
    h_px->Draw("");
    canvas->Print( (pdf_file_name + "(").c_str());
    h_py->Draw("");
    canvas->Print( (pdf_file_name + "(").c_str());
    h_pz->Draw("");
    canvas->Print( (pdf_file_name + ")").c_str());

    return 0;
}

//--- Functions ---//
//-----------------//

// Note: Most of these functions are in utility classes included with the DST.  However,
//       they will be placed here for now until the structure of an analysis package
//       is decided upon.

void printUsage() {
    cout << "Usage: TwoTrackAnalysis_example [OPTIONS]\nOPTIONS:\n"
         << "\t-i Input LCIO file name \n"
         << "\t-p Output pdf file name \n"
         << "\t-n The number of events to process \n"
         << "\t-h Display this help and exit \n"
         << endl;
}

// These two functions should be templates instead.
void setup1DHistogram(TH1* histo, string x_axis_title) {

    histo->SetStats(0);
    histo->GetXaxis()->SetTitle(x_axis_title.c_str());
    histo->GetXaxis()->SetTitleSize(0.03);
    histo->GetXaxis()->SetLabelSize(0.03);
    histo->GetYaxis()->SetTitleSize(0.03);
    histo->GetYaxis()->SetLabelSize(0.03);

}

void setup2DHistogram(TH1* histo, string x_axis_title, string y_axis_title) {

    histo->GetYaxis()->SetTitle(y_axis_title.c_str());
    setup1DHistogram(histo, x_axis_title);
}

UTIL::BitFieldValue getIdentifierFieldValue(std::string field, EVENT::CalorimeterHit* hit) {

    std::string encoder_string = "system:6,layer:2,ix:-8,iy:-6";

    UTIL::BitField64 decoder(encoder_string);
    long64 value = long64( hit->getCellID0() & 0xffffffff ) | ( long64( hit->getCellID1() ) << 32 ) ;
    decoder.setValue(value);

    return decoder[field];
}

//---------------------//

