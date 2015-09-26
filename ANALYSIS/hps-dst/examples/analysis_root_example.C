/**
 * 	@section purpose:
 *		A simple ROOT analysis demonstrating the use of a DST to make simple
 *		plots of Ecal, SVT and Particle physics objects
 *
 *  @author: 	Omar Moreno <omoreno1@ucsc.edu>
 *              Santa Cruz Institute for Particle Physics
 *              University of California, Santa Cruz
 *  @date: March 19, 2013
 */	

#include <iostream>

#include <TCanvas.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <TRefArray.h>


#include <HpsEvent.h>
#include <SvtTrack.h>
#include <EcalCluster.h>
#include <EcalHit.h>

//
//--- Functions ---//
//-----------------//

// Note: These functions will be placed in utility classes included with the
//	     DST at some point.

void setupCanvas(TCanvas* canvas){

	canvas->SetFillColor(0);
 	canvas->SetBorderMode(0);
 	canvas->SetBorderSize(0);
 	canvas->SetFrameFillColor(0);
 	canvas->SetFrameBorderMode(0);

}

void setup1DHistogram(TH1 *histo, string x_axis_title){

	histo->SetStats(0);
	histo->GetXaxis()->SetTitle(x_axis_title.c_str());
	histo->GetXaxis()->SetTitleSize(0.03);
	histo->GetXaxis()->SetLabelSize(0.03);
	histo->GetYaxis()->SetTitleSize(0.03);
	histo->GetYaxis()->SetLabelSize(0.03);

}

void setup2DHistogram(TH1* histo, string x_axis_title, string y_axis_title){

	histo->GetYaxis()->SetTitle(y_axis_title.c_str());
	setup1DHistogram(histo, x_axis_title);
}
 
double magnitude(vector<double> vector)
{
    return sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2]); 
}

//---------------------//
void runAnalysis(std::string root_file_name, std::string pdf_file_name){
	
    const double param = 2.99792458e-04;

 	//-- Setup ROOT histograms ---//
 	//----------------------------//

	// Create a canvas and set its characteristics
 	TCanvas *canvas = new TCanvas("canvas", "Data Summary Tape Plots", 700, 700);
 	setupCanvas(canvas);

    //
 	// Ecal
    //
 	TH2F *h_hit_pos = new TH2F("h_hit_pos", "Ecal Hit Positions", 47, -23, 24, 12, -6, 6);
 	setup2DHistogram(h_hit_pos, "Ecal Hit Index - x", "Ecal Hit Index - y");
 	TH1F *h_cluster_energy = new TH1F("h_cluster_energy", "Ecal Cluster Energy", 100, 0, 5.5);
 	setup1DHistogram(h_cluster_energy, "Ecal Cluster Energy [GeV]");

    //
 	// Tracking
    //
 	TH1F *h_d0   = new TH1F("h_d0",  "Track D0", 64, -8, 8);
 	setup1DHistogram(h_d0, "D0 [mm]");
 	TH1F *h_tlambda   = new TH1F("h_tlambda",  "Track Tan(#lambda)", 64, -0.08, 0.08);
 	setup1DHistogram(h_tlambda, "Tan #lambda");
    TH1F *h_chi2 = new TH1F("h_chi2", "Track #chi^{2}", 25, 0, 25);
    setup1DHistogram(h_chi2, "#chi^{2}");

    //
    // Particles
    //
    TH1F *h_p = new TH1F("h_p", "Particle Momentum", 64, 0, 2.2);
    setup1DHistogram(h_p, "Momentum [GeV]");  
	TH1F *h_vertex_z = new TH1F("h_vertex_z", "Vertex - Z", 150, -150, 150); 
	setup1DHistogram(h_vertex_z, "Vertex z [mm]"); 

 	//-----------------------------//


    // Open the ROOT file
 	TFile *file = new TFile(root_file_name.c_str());

    // Get the TTree "HPS_EVENT" containing the HpsEvent branch and all
    // other collections
    TTree *tree = (TTree*) file->Get("HPS_Event");

    // Create a pointer to an HpsEvent object in order to read the TClonesArrays
    // collections
    HpsEvent *hps_event = new HpsEvent();

    // Get the HpsEvent branch from the TTree and set the branch address to
    // the pointer created above
    TBranch *b_hps_event = tree->GetBranch("Event");
    b_hps_event->SetAddress(&hps_event);

    int index_x, index_y;
	
    double d0, tan_lambda, chi2;  
    double cluster_energy;
	double vertex_z; 
	vector<double> p;
    
    SvtTrack *track = 0;
    EcalCluster* ecal_cluster = 0;
    EcalHit* ecal_hit = 0;
    HpsParticle* particle = 0; 

	//--- Analysis ---//
	//----------------//

	// Loop over all events
    for(int entry = 0; entry < tree->GetEntries(); ++entry){

    	// Print the event number every 500 events
    	if((entry+1)%500 == 0){
    		std::cout << "Event: " << entry+1 << endl;
    	}

        // Read the ith entry from the tree.  This "fills" HpsEvent and allows
        // access to all collections
        tree->GetEntry(entry);

        // Loop over all of the Ecal clusters in the event
        for(int cluster_n = 0; cluster_n < hps_event->getNumberOfEcalClusters(); ++cluster_n){

        	// Get an Ecal cluster from the event
        	ecal_cluster = hps_event->getEcalCluster(cluster_n);

        	// Get the Ecal cluster energy
        	cluster_energy = ecal_cluster->getEnergy();

        	// Fill the cluster energy plot
        	h_cluster_energy->Fill(cluster_energy);

        	// Get the Ecal hits used to create the cluster
        	TRefArray* ecal_hits = ecal_cluster->getEcalHits();

        	// Loop through all of the Ecal hits and plot their positions
        	for(int hit_n = 0; hit_n < ecal_hits->GetEntries(); ++hit_n){

        		// Get an Ecal hit from the cluster
        		ecal_hit = (EcalHit*) ecal_hits->At(hit_n);

        		// Get the crystal index of the ecal hit
        		index_x = ecal_hit->getXCrystalIndex();
        		index_y = ecal_hit->getYCrystalIndex();

        		// Fill the Ecal hit position plot
        		h_hit_pos->Fill(index_x, index_y, 1);

        	}
        }

		// Loop over all tracks in the event
        for(int track_n = 0; track_n < hps_event->getNumberOfTracks(); ++track_n){

        	// Get a track from the event
        	track = hps_event->getTrack(track_n);

            d0 = track->getD0();
            tan_lambda = track->getTanLambda(); 
            chi2 = track->getChi2();  

            // Fill the plots
			h_d0->Fill(d0);
            h_tlambda->Fill(tan_lambda); 
            h_chi2->Fill(chi2); 
        }

        // Loop over all final state particles in the event
        for(int particle_n = 0; particle_n < hps_event->getNumberOfParticles(HpsParticle::FINAL_STATE_PARTICLE); ++particle_n){
            
            // Get a final state particle from the event
            particle = hps_event->getParticle(HpsParticle::FINAL_STATE_PARTICLE, particle_n); 

            //
            if(particle->getPDG() == 22) continue; 

            p = particle->getMomentum();
            h_p->Fill(magnitude(p));             

        }

		// Loop over all unconstrained vertexed particles in the event
		for(int particle_n = 0; particle_n < hps_event->getNumberOfParticles(HpsParticle::UC_V0_CANDIDATE); ++particle_n){
			
			// Get a vertexed particle from the event
			particle = hps_event->getParticle(HpsParticle::UC_V0_CANDIDATE, particle_n); 
			
			vertex_z = particle->getVertexPosition()[2];
			h_vertex_z->Fill(vertex_z);
		}
    }

	// Save all plots to a single pdf file
	h_hit_pos->Draw("colz");
	canvas->Print( (pdf_file_name + "(").c_str());
	h_cluster_energy->Draw("");
	canvas->Print( (pdf_file_name + "(").c_str());
	h_d0->Draw("");
	canvas->Print( (pdf_file_name + "(").c_str());
	h_tlambda->Draw(""); 
	canvas->Print( (pdf_file_name + "(").c_str());
    h_chi2->Draw("");
	canvas->Print( (pdf_file_name + "(").c_str());
    h_p->Draw(""); 
	canvas->Print( (pdf_file_name + "(").c_str());
	h_vertex_z->Draw("");
    canvas->Print( (pdf_file_name + ")").c_str());

}
