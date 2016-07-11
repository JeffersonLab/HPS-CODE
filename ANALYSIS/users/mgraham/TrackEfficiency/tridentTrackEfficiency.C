#define tridentTrackEfficiency_cxx
#include "tridentTrackEfficiency.h"
#include <TH2.h>
#include <TF1.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <TGaxis.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TCanvas.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <utility>  
#include <list>
void tridentTrackEfficiency::Loop(TString outpre)
{
//   In a ROOT session, you can do:
//      Root > .L tridentTrackEfficiency.C
//      Root > tridentTrackEfficiency t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;
   
   std::list<TH1*> histogramList;
   const double radian = TMath::RadToDeg();
   const double phot_nom_x = 42.52;
   double wabCut=0.95-0.2;//subtract 0.2 since not corrected for sampling fraction
   double b=TMath::Sin(0.0305);//beam angle
   const double BEff=0.24;  //effective B-field...reduced to account for no-field region between magnet and ECAL
 
   //Plots!!!!!!!!!!!!!!!!!!!!!!

   TH2D *h_coplan_Esum1 = new TH2D("h_coplan_Esum1", "", 200, 0.2, 1.14, 200, 120., 240.);
   
   TH2D *h_E1vsE2_cop180 = new TH2D("h_E1vsE2_cop180", "", 200, 0.1, 1.14, 200,  0.1, 1.14);
   TH1D *h_ESum_cop180 = new TH1D("h_ESum_cop180","",100,0.2,1.14);
   TH1D *h_ESum_cop180_bothtracks = new TH1D("h_ESum_cop180_bothtracks","",100,0.2,1.14);
   TH1D *h_ESum_cop180_eletrack = new TH1D("h_ESum_cop180_eletrack","",100,0.2,1.14);
   TH1D *h_ESum_cop180_postrack = new TH1D("h_ESum_cop180_postrack","",100,0.2,1.14);
   TH1D *h_ESum_cop180_notracks = new TH1D("h_ESum_cop180_notracks","",100,0.2,1.14);
   

   TH2D *h_Ecl_Ptrk_from_position_WAB_ele=new  TH2D("h_Ecl_Ptrk_from_position_WAB_ele","",100,0.1,0.6,100,0.2,1.5);
   TH2D *h_Ecl_Ptrk_from_position_WAB_pho=new  TH2D("h_Ecl_Ptrk_from_position_WAB_pho","",100,0.1,0.6,100,0.2,1.5);
   TH2D *h_Ecl_Ptrk_from_position_Tri_ele=new  TH2D("h_Ecl_Ptrk_from_position_Tri_ele","",100,0.1,0.6,100,0.2,1.5);
   TH2D *h_Ecl_Ptrk_from_position_Tri_pos=new  TH2D("h_Ecl_Ptrk_from_position_Tri_pos","",100,0.1,0.6,100,0.2,1.5);

   TH2D *h_Ecl_Ptrk_from_position_Tri_misele=new  TH2D("h_Ecl_Ptrk_from_position_Tri_misele","",100,0.1,0.6,100,0.2,1.5);
   TH2D *h_Ecl_Ptrk_from_position_Tri_mispos=new  TH2D("h_Ecl_Ptrk_from_position_Tri_mispos","",100,0.1,0.6,100,0.2,1.5);

   TH2D *h_Ptrk_Ptrk_from_position_Tri_ele=new  TH2D("h_Ptrk_Ptrk_from_position_Tri_ele","",100,0.1,0.6,100,0.2,1.5);
   TH2D *h_Ptrk_Ptrk_from_position_Tri_pos=new  TH2D("h_Ptrk_Ptrk_from_position_Tri_pos","",100,0.1,0.6,100,0.2,1.5);


   
   TH2D *h_E1vsE2_cop160 = new TH2D("h_E1vsE2_cop160", "", 200, 0.1, 1.14, 200,  0.1, 1.14);
   TH1D *h_ESum_cop160 = new TH1D("h_ESum_cop160","",100,0.2,1.14);
   TH1D *h_ESum_cop160_bothtracks = new TH1D("h_ESum_cop160_bothtracks","",100,0.2,1.14);
   TH1D *h_ESum_cop160_eletrack = new TH1D("h_ESum_cop160_eletrack","",100,0.2,1.14);
   TH1D *h_ESum_cop160_postrack = new TH1D("h_ESum_cop160_postrack","",100,0.2,1.14);
   TH1D *h_ESum_cop160_notracks = new TH1D("h_ESum_cop160_notracks","",100,0.2,1.14);

   /////////////////////////////////////////////////////////
   /*  WAB plots  */
   TH1D *h_Ecl_cop160_wab_photon = new TH1D("h_Ecl_cop160_wab_photon","",100,0.1,0.6);
   TH1D *h_Ecl_cop160_wab_electron = new TH1D("h_Ecl_cop160_wab_electron","",100,0.1,0.6);
   TH1D *h_Ecl_cop160_wab_missed = new TH1D("h_Ecl_cop160_wab_missed","",100,0.1,0.6);
   
   TH1D *h_EclX_cop160_wab_photon = new TH1D("h_EclX_cop160_wab_photon","",100,-300,300);
   TH1D *h_EclX_cop160_wab_electron = new TH1D("h_EclX_cop160_wab_electron","",100,-300,300 );
   TH1D *h_EclX_cop160_wab_missed = new TH1D("h_EclX_cop160_wab_missed","",100,-300,300);

   TH1D *h_EclY_cop160_wab_photon = new TH1D("h_EclY_cop160_wab_photon","",100,-100,100);
   TH1D *h_EclY_cop160_wab_electron = new TH1D("h_EclY_cop160_wab_electron","",100,-100,100 );
   TH1D *h_EclY_cop160_wab_missed = new TH1D("h_EclY_cop160_wab_missed","",100,-100,100);

   TH1D *h_ClD_cop160_wab_photon = new TH1D("h_ClD_cop160_wab_photon","",100,0,200);
   TH1D *h_ClD_cop160_wab_electron = new TH1D("h_ClD_cop160_wab_electron","",100,0,200 );
   TH1D *h_ClD_cop160_wab_missed = new TH1D("h_ClD_cop160_wab_missed","",100,0,200);

   TH1D *h_ntrk_cop160_wab_missed = new TH1D("h_ntrk_cop160_wab_missed","",5,0,5);
   TH1D *h_ntrk_cop160_wab_found = new TH1D("h_ntrk_cop160_wab_found","",5,0,5);

   TH1D *h_Ecl_cop180_wab_photon = new TH1D("h_Ecl_cop180_wab_photon","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_wab_electron = new TH1D("h_Ecl_cop180_wab_electron","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_wab_missed = new TH1D("h_Ecl_cop180_wab_missed","",100,0.1,0.6);
   
   TH1D *h_EclX_cop180_wab_photon = new TH1D("h_EclX_cop180_wab_photon","",100,-300,300);
   TH1D *h_EclX_cop180_wab_electron = new TH1D("h_EclX_cop180_wab_electron","",100,-300,300 );
   TH1D *h_EclX_cop180_wab_missed = new TH1D("h_EclX_cop180_wab_missed","",100,-300,300);

   TH1D *h_EclY_cop180_wab_photon = new TH1D("h_EclY_cop180_wab_photon","",100,-100,100);
   TH1D *h_EclY_cop180_wab_electron = new TH1D("h_EclY_cop180_wab_electron","",100,-100,100 );
   TH1D *h_EclY_cop180_wab_missed = new TH1D("h_EclY_cop180_wab_missed","",100,-100,100);

   TH1D *h_ClD_cop180_wab_photon = new TH1D("h_ClD_cop180_wab_photon","",100,0,200);
   TH1D *h_ClD_cop180_wab_electron = new TH1D("h_ClD_cop180_wab_electron","",100,0,200 );
   TH1D *h_ClD_cop180_wab_missed = new TH1D("h_ClD_cop180_wab_missed","",100,0,200);

   /////////////////////////////////////////////////////////

  /////////////////////////////////////////////////////////
   /*  mid-ESum plots  */ 

   TH1D *h_Ecl_midESum_coplanarity = new TH1D("h_Ecl_midESum_coplanarity","",100,120,240);

   TH1D *h_Ecl_cop180_midESum_positron = new TH1D("h_Ecl_cop180_midESum_positron","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_electron = new TH1D("h_Ecl_cop180_midESum_electron","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_mis_ele = new TH1D("h_Ecl_cop180_midESum_mis_ele","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_mis_pos = new TH1D("h_Ecl_cop180_midESum_mis_pos","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_mis_both_ele_side = new TH1D("h_Ecl_cop180_midESum_mis_both_ele_side","",100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_mis_both_pos_side = new TH1D("h_Ecl_cop180_midESum_mis_both_pos_side","",100,0.1,0.6);
   
   TH1D *h_EclX_cop180_midESum_positron = new TH1D("h_EclX_cop180_midESum_positron","",100,-400,400);
   TH1D *h_EclX_cop180_midESum_electron = new TH1D("h_EclX_cop180_midESum_electron","",100,-400,400 );
   TH1D *h_EclX_cop180_midESum_mis_ele = new TH1D("h_EclX_cop180_midESum_mis_ele","",100,-400,400);
   TH1D *h_EclX_cop180_midESum_mis_pos = new TH1D("h_EclX_cop180_midESum_mis_pos","",100,-400,400);
   TH1D *h_EclX_cop180_midESum_mis_both_ele_side = new TH1D("h_EclX_cop180_midESum_mis_both_ele_side","",100,-400,400);
   TH1D *h_EclX_cop180_midESum_mis_both_pos_side = new TH1D("h_EclX_cop180_midESum_mis_both_pos_side","",100,-400,400);

   TH1D *h_EclY_cop180_midESum_positron = new TH1D("h_EclY_cop180_midESum_positron","",100,-100,100);
   TH1D *h_EclY_cop180_midESum_electron = new TH1D("h_EclY_cop180_midESum_electron","",100,-100,100 );
   TH1D *h_EclY_cop180_midESum_mis_ele = new TH1D("h_EclY_cop180_midESum_mis_ele","",100,-100,100);
   TH1D *h_EclY_cop180_midESum_mis_pos = new TH1D("h_EclY_cop180_midESum_mis_pos","",100,-100,100);
   TH1D *h_EclY_cop180_midESum_mis_both_ele_side = new TH1D("h_EclY_cop180_midESum_mis_both_ele_side","",100,-100,100);
   TH1D *h_EclY_cop180_midESum_mis_both_pos_side = new TH1D("h_EclY_cop180_midESum_mis_both_pos_side","",100,-100,100);

   TH1D *h_ClD_cop180_midESum_positron = new TH1D("h_ClD_cop180_midESum_positron","",100,0,200);
   TH1D *h_ClD_cop180_midESum_electron = new TH1D("h_ClD_cop180_midESum_electron","",100,0,200 );
   TH1D *h_ClD_cop180_midESum_mis_ele = new TH1D("h_ClD_cop180_midESum_mis_ele","",100,0,200);
   TH1D *h_ClD_cop180_midESum_mis_pos = new TH1D("h_ClD_cop180_midESum_mis_pos","",100,0,200);
   TH1D *h_ClD_cop180_midESum_mis_both_ele_side = new TH1D("h_ClD_cop180_midESum_mis_both_ele_side","",100,0,200);
   TH1D *h_ClD_cop180_midESum_mis_both_pos_side = new TH1D("h_ClD_cop180_midESum_mis_both_pos_side","",100,0,200);

   TH1D *h_Ecl_cop180_midESum_pos_side_found_ele = new TH1D("h_Ecl_cop180_midESum_pos_side_found_ele","", 100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_pos_side_found_ele_found_pos = new TH1D("h_Ecl_cop180_midESum_pos_side_found_ele_found_pos","", 100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_ele_side_found_pos = new TH1D("h_Ecl_cop180_midESum_ele_side_found_pos","", 100,0.1,0.6);
   TH1D *h_Ecl_cop180_midESum_ele_side_found_pos_found_ele = new TH1D("h_Ecl_cop180_midESum_ele_side_found_pos_found_ele","", 100,0.1,0.6);
   /////////////////////////////////////////////////////////


   TH2D *h_EclX_EclY_ElectronPositron = new TH2D("h_EclX_EclY_ElectronPositron","",100,-400,400,100,-100,100);
   histogramList.push_back(h_EclX_EclY_ElectronPositron);
   ////////////////////////
   // same sign found tracks. 
   TH1D *h_Ecl_TwoElectrons_coplanarity = new TH1D("h_Ecl_TwoElectrons_coplanarity ","",100,0,240);
   TH1D *h_Ecl_TwoPositrons_coplanarity = new TH1D("h_Ecl_TwoPositrons_coplanarity","",100,0,240);
   TH1D *h_Ecl_TwoElectrons_mass=new TH1D("h_Ecl_TwoElectrons_mass","",100,0,0.1);
   TH1D *h_Ecl_TwoPositrons_mass=new TH1D("h_Ecl_TwoPositrons_mass","",100,0,0.1);
   TH2D *h_EclX_EclY_TwoElectrons = new TH2D("h_EclX_EclY_TwoElectrons","",100,-400,400,100,-100,100);
   TH2D *h_EclX_EclY_TwoPositrons = new TH2D("h_EclX_EclY_TwoPositrons","",100,-400,400,100,-100,100);
   TH2D *h_Ecl_Ptrk_from_position_TwoElectrons_ele=new  TH2D("h_Ecl_Ptrk_from_position_TwoElectrons_ele","",100,0.1,0.6,100,0.2,1.5);
   TH2D *h_Ecl_Ptrk_from_position_TwoPositrons_ele=new  TH2D("h_Ecl_Ptrk_from_position_TwoPositrons_pho","",100,0.1,0.6,100,0.2,1.5);
   TH1D *h_Ecl_TwoElectrons_esum=new TH1D("h_Ecl_TwoElectrons_esum","",100,0.2,1.14);
   TH1D *h_Ecl_TwoPositrons_esum=new TH1D("h_Ecl_TwoPositrons_esum","",100,0.2,1.14);

   histogramList.push_back(h_Ecl_TwoElectrons_coplanarity);
   histogramList.push_back(h_Ecl_TwoPositrons_coplanarity);
   histogramList.push_back(h_EclX_EclY_TwoElectrons);
   histogramList.push_back(h_EclX_EclY_TwoPositrons);
   histogramList.push_back(h_Ecl_Ptrk_from_position_TwoElectrons_ele);
   histogramList.push_back(h_Ecl_Ptrk_from_position_TwoPositrons_ele);
   histogramList.push_back(h_Ecl_TwoElectrons_mass);
   histogramList.push_back(h_Ecl_TwoPositrons_mass);

   /////////////////////

   /////////////////////
   //  no matched tracks
   TH1D *h_Ecl_TwoPhotons_coplanarity = new TH1D("h_Ecl_TwoPhotons_coplanarity ","",100,0,240);
   TH2D *h_EclX_EclY_TwoPhotons = new TH2D("h_EclX_EclY_TwoPhotons","",100,-400,400,100,-100,100);
   TH2D *h_Ecl_Ptrk_from_position_TwoPhotons_ele=new  TH2D("h_Ecl_Ptrk_from_position_TwoPhotons_ele","",100,0.1,0.6,100,0.2,1.5);
   TH1D *h_Ecl_TwoPhotons_mass=new TH1D("h_Ecl_TwoPhotons_mass","",100,0,0.1);
   TH1D *h_Ecl_TwoPhotons_esum=new TH1D("h_Ecl_TwoPhotons_esum","",100,0.2,1.14);
   
   histogramList.push_back(h_Ecl_TwoPhotons_coplanarity);
   histogramList.push_back(h_EclX_EclY_TwoPhotons);
   histogramList.push_back(h_Ecl_Ptrk_from_position_TwoPhotons_ele);
   histogramList.push_back(h_Ecl_TwoPhotons_mass);
   histogramList.push_back(h_Ecl_TwoPhotons_esum);
   histogramList.push_back(h_Ecl_TwoElectrons_esum);
   histogramList.push_back(h_Ecl_TwoPositrons_esum);



   TH1D *h_diffTkCl_E = new TH1D("h_diffTkCl_E","",100,-0.5,0.5);
   TH1D *h_diffTkCl_x = new TH1D("h_diffTkCl_x","",100,-100,100);
   TH1D *h_diffTkCl_y = new TH1D("h_diffTkCl_y","",100,-100,100);
 
   TH1D *h_trkmatch_cop160 = new TH1D("h_trkmatch_cop160","",9,-1,8);
   TH1D *h_trkmatch_cop180 = new TH1D("h_trkmatch_cop180","",9,-1,8);

   double midESumLow=0.25; 
   double midESumHigh=0.70; 

   double esumSliceSize=0.1;
   double esumSliceStart=0.25;
   int nEsumBins=7;
   TH1D* h_copl_esum_slice[nEsumBins];

   TH1D* h_Ecl_esum_slice_ele_side_found_pos_found_ele[nEsumBins];
   TH1D* h_Ecl_esum_slice_ele_side_found_pos[nEsumBins];
   TH1D* h_Ecl_esum_slice_pos_side_found_ele_found_pos[nEsumBins];
   TH1D* h_Ecl_esum_slice_pos_side_found_ele[nEsumBins];
   TH1D* h_Ecl_esum_slice_positron[nEsumBins];
   TH1D* h_Ecl_esum_slice_electron[nEsumBins];
   TH1D* h_Ecl_esum_slice_mis_ele[nEsumBins];
   TH1D* h_Ecl_esum_slice_mis_pos[nEsumBins];

   TString baseName="h_Ecl_esum_slice_";
   TString name;
   for (int i=0;i<nEsumBins;i++){
     name="h_copl_esum_slice";name+=i;
     h_copl_esum_slice[i] = new TH1D(name,"",100,120,240);     
     name=baseName;name+="ele_side_found_pos_found_ele_";name+=i;
     h_Ecl_esum_slice_ele_side_found_pos_found_ele[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="ele_side_found_pos_";name+=i;
     h_Ecl_esum_slice_ele_side_found_pos[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="pos_side_found_ele_found_pos_";name+=i;
     h_Ecl_esum_slice_pos_side_found_ele_found_pos[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="pos_side_found_ele_";name+=i;
     h_Ecl_esum_slice_pos_side_found_ele[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="positron_";name+=i;
     h_Ecl_esum_slice_positron[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="electron_";name+=i;
     h_Ecl_esum_slice_electron[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="mis_ele_";name+=i;
     h_Ecl_esum_slice_mis_ele[i]=new TH1D(name,"",100,0.1,0.6);
     name=baseName;name+="mis_pos_";name+=i;
     h_Ecl_esum_slice_mis_pos[i]=new TH1D(name,"",100,0.1,0.6);

   }
   

   //================ Time coincidence ======================================
   double coincide_pars_mean[6] = {0.289337,   -2.81998,   9.03475, -12.93,   8.71476,   -2.26969};
   double coincide_pars_sigm[6] = {4.3987,   -24.2371,   68.9567, -98.2586,   67.562,   -17.8987};
   
   std::string formula_pol5 = "[0] + x*( [1] + x*( [2] + x*( [3] + x*( [4] + x*( [5] ) ) ) ) ) ";
   TF1 *f_coincide_clust_mean = new TF1("f_coincide_clust_mean", formula_pol5.c_str(), 0., 1.4);
   TF1 *f_coincide_clust_sigm = new TF1("f_coincide_clust_sigm", formula_pol5.c_str(), 0., 1.4);
   f_coincide_clust_mean->SetParameters(coincide_pars_mean);
   f_coincide_clust_sigm->SetParameters(coincide_pars_sigm);
   //The cut is            === mean - 3sigma < dt < mean + 3sigma ===

   ofstream missPositron;
   ofstream missElectron;
   missPositron.open("missedPositron_run5772.dat");
   missElectron.open("missedElectron_run5772.dat");
   Long64_t nentries = fChain->GetEntriesFast();
   std::vector<std::pair<int,int> > clPairs;
   Long64_t nbytes = 0, nb = 0;
   int pairsFound=0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {                  
     nb = fChain->GetEntry(jentry);   nbytes += nb;
     // if (Cut(ientry) < 0) continue;
     clPairs.clear();
     Long64_t ientry = LoadTree(jentry);
     if (ientry < 0) break;   
     std::pair <int,int> clpair;      
     for (int i=0;i<n_cl;i++){       
       double cl_di = sqrt( (cl_x[i] - phot_nom_x)*(cl_x[i] - phot_nom_x) + cl_y[i]*cl_y[i] );       
       //if(!fid_ECal(cl_x[i],cl_y[i]))
       //	 continue;
       if(!superFid_ECal(cl_x[i],cl_y[i]))
       	 continue;
       if( !(cl_t[i] > 30 && cl_t[i] < 50 ))
	 continue;
       if(!momFromPositionEclUpperCut(cl_E[i],momFromECalPosition(cl_x[i],cl_z[i],b,BEff)))
       	 continue;
       for (int j=i+1;j<n_cl;j++){
	 double cl_dj =sqrt( (cl_x[j] - phot_nom_x)*(cl_x[j] - phot_nom_x) + cl_y[j]*cl_y[j] );
	 double Esum = cl_E[i] + cl_E[j];
	 //	 if(!energySlopeCut(cl_x[j],cl_d,cl_E[j]))
	 //	   continue;
	 if( !(cl_t[j] > 30 && cl_t[j] < 50 ))
	   continue;
	 if(!superFid_ECal(cl_x[j],cl_y[j]))
	   continue;
	 //if(!fid_ECal(cl_x[j],cl_y[j]))
	 //  continue;
	 //	 if(!(energySlopeCut(cl_x[i],cl_di,cl_E[i]) || energySlopeCut(cl_x[j],cl_dj,cl_E[j])))
	 //   continue;
	 if(!momFromPositionEclUpperCut(cl_E[j],momFromECalPosition(cl_x[j],cl_z[j],b,BEff)))
	   continue;
	 double dt = cl_t[i] - cl_t[j];
	 double delt_t_mean = f_coincide_clust_mean->Eval(Esum);
	 double delt_t_sigm = f_coincide_clust_sigm->Eval(Esum);	 
	 if( ! (dt < delt_t_mean + 3*delt_t_sigm && dt > delt_t_mean - 3*delt_t_sigm))
	   continue;
	 //make sure they are top/bottom
	 if(cl_y[i]*cl_y[j]>0)
	   continue;
	 clpair=std::make_pair(i,j);
	 clPairs.push_back(clpair);	  
       }
     }
     pairsFound+=clPairs.size();

     //loop over the good pairs
     for(std::vector<std::pair<int,int> >::iterator it = clPairs.begin(); it != clPairs.end(); ++it) {
       int clTop=it->first;
       int clBottom=it->second;
       double Esum = cl_E[clTop] + cl_E[clBottom];
       if(cl_y[clTop]<0){
	 double tmp=clBottom;
	 clBottom=clTop;
	 clTop=tmp;
       }
       double cl_impact_angleTop = atan2(cl_y[clTop], cl_x[clTop] - phot_nom_x)*radian;
       double cl_impact_angleBottom = atan2(cl_y[clBottom], cl_x[clBottom] - phot_nom_x)*radian;
       double cl_d_top= sqrt( (cl_x[clTop] - phot_nom_x)*(cl_x[clTop] - phot_nom_x) + cl_y[clTop]*cl_y[clTop] )- (60. + 100*(cl_E[clTop] - 0.85)*(cl_E[clTop] - 0.85) );       
       double cl_d_bottom= sqrt( (cl_x[clBottom] - phot_nom_x)*(cl_x[clBottom] - phot_nom_x) + cl_y[clBottom]*cl_y[clBottom] )- (60. + 100*(cl_E[clBottom] - 0.85)*(cl_E[clBottom] - 0.85) );       

       if( cl_impact_angleTop < 0. ) 
	 cl_impact_angleTop = cl_impact_angleTop + 360.;
       if( cl_impact_angleBottom < 0. ) 
	 cl_impact_angleBottom = cl_impact_angleBottom + 360.;       
       double coplanarity=  cl_impact_angleBottom -  cl_impact_angleTop  ;
       //cout<<coplanarity<<endl;
       h_coplan_Esum1->Fill(Esum,coplanarity);

       //see if we can match tracks
       int trTop=matchTrack(clTop);
       int trBottom=matchTrack(clBottom);
       int trPos=trTop;
       int trEle=trBottom;
       double cl_d_pos=cl_d_top;
       double cl_d_ele=cl_d_bottom;
       if(tr_omega[trTop]>0&&tr_omega[trBottom]<0){//positive is electron
	 trPos=trBottom;
	 trEle=trTop;
	 cl_d_pos=cl_d_bottom;
	 cl_d_ele=cl_d_top;
       }


       ////////////////////       

       int matchID=0;
       if(trEle!=-99 && trPos!=-99)
	 matchID=2;
       else if(trEle!=-99)
	 matchID=-1;
       else if(trPos!=-99)
	 matchID=1;

       int matchIDTB=5;
       if(trTop!=-99 && trBottom!=-99)
	 matchIDTB=7;
       else if(trBottom!=-99)
	 matchIDTB=4;
       else if(trTop!=-99)
	 matchIDTB=6;
       
       

       if(trTop!=-99){
	 h_diffTkCl_x->Fill(tr_x[trTop]-cl_x[clTop]);
	 h_diffTkCl_y->Fill(tr_y[trTop]-cl_y[clTop]);
	 h_diffTkCl_E->Fill(tr_p[trTop]-cl_E[clTop]);
       }
       if(trBottom!=-99){
	 h_diffTkCl_x->Fill(tr_x[trBottom]-cl_x[clBottom]);
	 h_diffTkCl_y->Fill(tr_y[trBottom]-cl_y[clBottom]);
	 h_diffTkCl_E->Fill(tr_p[trBottom]-cl_E[clBottom]);
       }
       if(Esum>midESumLow&&Esum<midESumHigh){	 
	 h_Ecl_midESum_coplanarity->Fill(coplanarity);
       }
       int bin=(int)((Esum-esumSliceStart)/esumSliceSize);
       //       cout<<"Filling into "<<bin<<endl;
       if(bin<nEsumBins&&bin>-1)
	 h_copl_esum_slice[bin]->Fill(coplanarity);
       
       
       //coplan ~180 degrees band:
       if( fabs(coplanarity-180)<10 ){	 
	 h_ESum_cop180->Fill(Esum);
	 h_E1vsE2_cop180->Fill(cl_E[clTop],cl_E[clBottom]);
	 h_trkmatch_cop180->Fill(matchID);	 
	 h_trkmatch_cop180->Fill(matchIDTB);	 
	 if(trTop!=-99 && trBottom!=-99 && tr_omega[trTop]*tr_omega[trBottom]< 0 ) { // require +/- tracks
	 //found both tracks
	   int clEle=clTop;
	   int clPos=clBottom;
	   if(tr_omega[trBottom] >0 ){
	     clEle=clBottom;
	     clPos=clTop;	     
	   }
	   h_EclX_EclY_ElectronPositron->Fill(cl_x[clTop],cl_y[clTop]);
	   h_EclX_EclY_ElectronPositron->Fill(cl_x[clBottom],cl_y[clBottom]);
	   double eleRadius=radiusFromECAL(cl_x[clEle],cl_z[clEle],b);
	   double eleMomFromPosition=momFromRadius(eleRadius,BEff);
	   h_Ecl_Ptrk_from_position_Tri_ele->Fill(cl_E[clEle],eleMomFromPosition);
	   
	   double posRadius=radiusFromECAL(cl_x[clPos],cl_z[clPos],b);
	   double posMomFromPosition=momFromRadius(posRadius,BEff);
	   h_Ecl_Ptrk_from_position_Tri_pos->Fill(cl_E[clPos],posMomFromPosition);

   	   h_Ptrk_Ptrk_from_position_Tri_ele->Fill(tr_p[trEle],eleMomFromPosition);
	   h_Ptrk_Ptrk_from_position_Tri_pos->Fill(tr_p[trPos],posMomFromPosition);
	   
	   if(Esum>midESumLow&&Esum<midESumHigh){
	     h_Ecl_cop180_midESum_positron->Fill(cl_E[clPos]);
	     h_EclX_cop180_midESum_positron->Fill(cl_x[clPos]);
	     h_EclY_cop180_midESum_positron->Fill(cl_y[clPos]);
	     h_ClD_cop180_midESum_positron->Fill(cl_d_pos);
	     h_Ecl_cop180_midESum_electron->Fill(cl_E[clEle]);
	     h_EclX_cop180_midESum_electron->Fill(cl_x[clEle]);
	     h_EclY_cop180_midESum_electron->Fill(cl_y[clEle]);
	     h_ClD_cop180_midESum_electron->Fill(cl_d_ele);
	     h_Ecl_cop180_midESum_pos_side_found_ele->Fill(cl_E[clPos]);
	     h_Ecl_cop180_midESum_pos_side_found_ele_found_pos->Fill(cl_E[clPos]);
	     h_Ecl_cop180_midESum_ele_side_found_pos->Fill(cl_E[clEle]);
	     h_Ecl_cop180_midESum_ele_side_found_pos_found_ele->Fill(cl_E[clEle]);
	   		     
	   }
	   
	   //esum slices	     
	   if(bin<nEsumBins&&bin>-1){
	     h_Ecl_esum_slice_electron[bin]->Fill(cl_E[clEle]);
	     h_Ecl_esum_slice_positron[bin]->Fill(cl_E[clPos]);
	     h_Ecl_esum_slice_pos_side_found_ele[bin]->Fill(cl_E[clPos]);
	     h_Ecl_esum_slice_ele_side_found_pos[bin]->Fill(cl_E[clEle]);
	     h_Ecl_esum_slice_pos_side_found_ele_found_pos[bin]->Fill(cl_E[clPos]);
	     h_Ecl_esum_slice_ele_side_found_pos_found_ele[bin]->Fill(cl_E[clEle]);
	   }
	   h_ESum_cop180_bothtracks->Fill(Esum);
	     
	 }else if ( (trTop !=-99 && tr_omega[trTop] >0 ) ||  (trBottom !=-99 && tr_omega[trBottom] >0 )){
	   //found just electron
	   h_ESum_cop180_eletrack->Fill(Esum);	       
	   // fill some WAB stuff. 
	   int clPhoton=clTop;
	   int clTrack=clBottom;
	   if  (trTop !=-99 && tr_omega[trTop] >0 ) {
	     clPhoton=clBottom;
	     clTrack=clTop;
	   }	     


	   
	   double posRadius=radiusFromECAL(cl_x[clPhoton],cl_z[clPhoton],b);
	   double posMomFromPosition=momFromRadius(posRadius,BEff);
	   h_Ecl_Ptrk_from_position_Tri_mispos->Fill(cl_E[clPhoton],posMomFromPosition);


	   if(Esum > wabCut){
	     h_Ecl_cop180_wab_photon->Fill(cl_E[clPhoton]);
	     h_Ecl_cop180_wab_electron->Fill(cl_E[clTrack]);

	     h_EclX_cop180_wab_photon->Fill(cl_x[clPhoton]);
	     h_EclX_cop180_wab_electron->Fill(cl_x[clTrack]);

	     h_EclY_cop180_wab_photon->Fill(cl_y[clPhoton]);
	     h_EclY_cop180_wab_electron->Fill(cl_y[clTrack]);

	     h_ClD_cop180_wab_photon->Fill(cl_d_pos);
	     h_ClD_cop180_wab_electron->Fill(cl_d_ele);
	   }
	   if(Esum>midESumLow&&Esum<midESumHigh){
	     h_Ecl_cop180_midESum_electron->Fill(cl_E[clTrack]);
	     h_EclX_cop180_midESum_electron->Fill(cl_x[clTrack]);
	     h_EclY_cop180_midESum_electron->Fill(cl_y[clTrack]);
	     h_ClD_cop180_midESum_electron->Fill(cl_d_ele);
	     h_Ecl_cop180_midESum_mis_pos->Fill(cl_E[clPhoton]);
	     h_EclX_cop180_midESum_mis_pos->Fill(cl_x[clPhoton]);
	     h_EclY_cop180_midESum_mis_pos->Fill(cl_y[clPhoton]);
	     h_ClD_cop180_midESum_mis_pos->Fill(cl_d_pos);
	     h_Ecl_cop180_midESum_pos_side_found_ele->Fill(cl_E[clPhoton]);
	     missPositron<<  hps_ev_number<<endl;
	   }	   	   
	   //esum slices
	   if(bin<nEsumBins&&bin>-1){	     
	     h_Ecl_esum_slice_electron[bin]->Fill(cl_E[clTrack]);
	     h_Ecl_esum_slice_mis_pos[bin]->Fill(cl_E[clPhoton]);
	     h_Ecl_esum_slice_pos_side_found_ele[bin]->Fill(cl_E[clPhoton]);
	   }
	 } else if( (trTop !=-99 && tr_omega[trTop] <0 ) ||  (trBottom !=-99 && tr_omega[trBottom] <0 )){
	   //found just positron
	   h_ESum_cop180_postrack->Fill(Esum);
	   int clPhoton=clTop;
	   int clTrack=clBottom;
	   if  (trTop !=-99 ) {
	     clPhoton=clBottom;
	     clTrack=clTop;
	   }	     

	   double eleRadius=radiusFromECAL(cl_x[clPhoton],cl_z[clPhoton],b);
	   double eleMomFromPosition=momFromRadius(eleRadius,BEff);
	   h_Ecl_Ptrk_from_position_Tri_misele->Fill(cl_E[clPhoton],eleMomFromPosition);

	   if(Esum>midESumLow&&Esum<midESumHigh){
	     h_Ecl_cop180_midESum_positron->Fill(cl_E[clTrack]);
	     h_EclX_cop180_midESum_positron->Fill(cl_x[clTrack]);
	     h_EclY_cop180_midESum_positron->Fill(cl_y[clTrack]);
	     h_ClD_cop180_midESum_positron->Fill(cl_d_pos);
	     h_Ecl_cop180_midESum_mis_ele->Fill(cl_E[clPhoton]);
	     h_EclX_cop180_midESum_mis_ele->Fill(cl_x[clPhoton]);
	     h_EclY_cop180_midESum_mis_ele->Fill(cl_y[clPhoton]);
	     h_ClD_cop180_midESum_mis_ele->Fill(cl_d_ele);
	     h_Ecl_cop180_midESum_ele_side_found_pos->Fill(cl_E[clPhoton]);
	     missElectron<<  hps_ev_number<<endl;
	   }	  
	   //esum slices
	   if(bin<nEsumBins&&bin>-1){	     
	     h_Ecl_esum_slice_positron[bin]->Fill(cl_E[clTrack]);
	     h_Ecl_esum_slice_mis_ele[bin]->Fill(cl_E[clPhoton]);
	     h_Ecl_esum_slice_ele_side_found_pos[bin]->Fill(cl_E[clPhoton]);
	   }
	 } else if(trTop==-99 && trBottom == -99){
	   //found nothing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	   h_ESum_cop180_notracks->Fill(Esum);	       
	   // fill some WAB stuff
	   if(Esum > wabCut){ 
	     int clESide=clTop;
	     if(cl_x[clBottom]<0)
	       clESide=clBottom;
	     h_Ecl_cop180_wab_missed->Fill(cl_E[clESide]);
	     h_EclX_cop180_wab_missed->Fill(cl_x[clESide]);
	     h_EclY_cop180_wab_missed->Fill(cl_y[clESide]);
	     h_ClD_cop180_wab_missed->Fill(cl_d_ele);
	   }	 	  
	   int clPos=clTop;
	   int clEle=clBottom;
	   if(cl_x[clTop]<0){
	     clPos=clBottom;
	     clEle=clTop;
	   }
	   if(Esum>midESumLow&&Esum<midESumHigh){
	     h_Ecl_cop180_midESum_mis_both_ele_side->Fill(cl_E[clEle]);
	     h_EclX_cop180_midESum_mis_both_ele_side->Fill(cl_x[clEle]);
	     h_EclY_cop180_midESum_mis_both_ele_side->Fill(cl_y[clEle]);
	     h_ClD_cop180_midESum_mis_both_ele_side->Fill(cl_d_ele);
	     h_Ecl_cop180_midESum_mis_both_pos_side->Fill(cl_E[clPos]);
	     h_EclX_cop180_midESum_mis_both_pos_side->Fill(cl_x[clPos]);
	     h_EclY_cop180_midESum_mis_both_pos_side->Fill(cl_y[clPos]);	     	     
	     h_ClD_cop180_midESum_mis_both_pos_side->Fill(cl_d_pos);	     	     
	   }
	 }
       }
       //coplan ~160 degrees band:
       if( fabs(coplanarity-160)<10 ){	 
	 h_ESum_cop160->Fill(Esum);
	 h_E1vsE2_cop160->Fill(cl_E[clTop],cl_E[clBottom]);
	 //found both tracks
	 h_trkmatch_cop160->Fill(matchID);	 
	 h_trkmatch_cop160->Fill(matchIDTB);	 
	 if(trEle!=-99 && trPos!=-99 && tr_omega[trTop]*tr_omega[trBottom]< 0) {
	   h_ESum_cop160_bothtracks->Fill(Esum);
	 }else if ( (trTop !=-99 && tr_omega[trTop] >0 ) ||  (trBottom !=-99 && tr_omega[trBottom] >0 )){
	   h_ESum_cop160_eletrack->Fill(Esum);	
	   int clPhoton=clTop;
	   int clTrack=clBottom;
	   if  (trTop !=-99 && tr_omega[trTop] >0 ) {
	     clPhoton=clBottom;
	     clTrack=clTop;
	   }	     
	   if(Esum > wabCut){
	     h_ntrk_cop160_wab_found->Fill(n_tr);

	     h_Ecl_cop160_wab_photon->Fill(cl_E[clPhoton]);
	     h_Ecl_cop160_wab_electron->Fill(cl_E[clTrack]);

	     h_EclX_cop160_wab_photon->Fill(cl_x[clPhoton]);
	     h_EclX_cop160_wab_electron->Fill(cl_x[clTrack]);

	     h_EclY_cop160_wab_photon->Fill(cl_y[clPhoton]);
	     h_EclY_cop160_wab_electron->Fill(cl_y[clTrack]);

	     h_ClD_cop160_wab_photon->Fill(cl_d_pos);
	     h_ClD_cop160_wab_electron->Fill(cl_d_ele);

	     double eleRadius=radiusFromECAL(cl_x[clTrack],cl_z[clTrack],b);
	     double eleMomFromPosition=momFromRadius(eleRadius,BEff);
	     h_Ecl_Ptrk_from_position_WAB_ele->Fill(cl_E[clTrack],eleMomFromPosition);
	     
	     double phoRadius=radiusFromECAL(cl_x[clPhoton],cl_z[clPhoton],b);
	     double phoMomFromPosition=momFromRadius(phoRadius,BEff);
	     h_Ecl_Ptrk_from_position_WAB_pho->Fill(cl_E[clPhoton],phoMomFromPosition);
	
	   }
	 } else if( (trTop !=-99 && tr_omega[trTop] <0 ) ||  (trBottom !=-99 && tr_omega[trBottom] <0 )){
	   h_ESum_cop160_postrack->Fill(Esum);	       	 
	 }else if(trTop==-99 && trBottom == -99){
	   h_ESum_cop160_notracks->Fill(Esum);	       	 
	   //fill just the electron side...
	   if(Esum > wabCut){ 
	     h_ntrk_cop160_wab_missed->Fill(n_tr);
	     int clESide=clTop;
	     if(cl_x[clBottom]<0)
	       clESide=clBottom;
	     h_Ecl_cop160_wab_missed->Fill(cl_E[clESide]);
	     h_EclX_cop160_wab_missed->Fill(cl_x[clESide]);
	     h_EclY_cop160_wab_missed->Fill(cl_y[clESide]);
	     h_ClD_cop160_wab_missed->Fill(cl_d_ele);
	   }
	 }
       }

       //       if(trTop==-99 && trBottom == -99&&coplanarity<120){
       if(trTop==-99 && trBottom == -99){
	 //no matches
	 double normTop=sqrt(cl_x[clTop]*cl_x[clTop]+cl_y[clTop]*cl_y[clTop]+cl_z[clTop]*cl_z[clTop]);
	 double normBottom=sqrt(cl_x[clBottom]*cl_x[clBottom]+cl_y[clBottom]*cl_y[clBottom]+cl_z[clBottom]*cl_z[clBottom]);
	 TLorentzVector* pTop=new TLorentzVector(cl_E[clTop]*cl_x[clTop]/normTop,
					       cl_E[clTop]*cl_y[clTop]/normTop,
					       cl_E[clTop]*cl_z[clTop]/normTop,
					       cl_E[clTop]);

	 TLorentzVector* pBottom=new TLorentzVector(cl_E[clBottom]*cl_x[clBottom]/normTop,
					       cl_E[clBottom]*cl_y[clBottom]/normTop,
					       cl_E[clBottom]*cl_z[clBottom]/normTop,
					       cl_E[clBottom]);

	 double mass=sqrt(pTop->Dot(*pBottom));
	 //	 Cout<<"mass = "<<mass<<"; topEnergy = "<<cl_E[clTop]<<"; bottomEnergy = "<<cl_E[clBottom]<<endl;
	 h_Ecl_TwoPhotons_mass->Fill(mass);
	 h_Ecl_TwoPhotons_esum->Fill(cl_E[clTop]+cl_E[clBottom]);
	 h_Ecl_TwoPhotons_coplanarity-> Fill(coplanarity);	  
	 h_EclX_EclY_TwoPhotons->Fill(cl_x[clTop],cl_y[clTop]);
	 h_EclX_EclY_TwoPhotons->Fill(cl_x[clBottom],cl_y[clBottom]);
	 h_Ecl_Ptrk_from_position_TwoPhotons_ele->Fill(cl_E[clTop], momFromRadius(radiusFromECAL(cl_x[clTop],cl_z[clTop],b),BEff));
	 h_Ecl_Ptrk_from_position_TwoPhotons_ele->Fill(cl_E[clBottom], momFromRadius(radiusFromECAL(cl_x[clBottom],cl_z[clBottom],b),BEff));
       }

       if(trTop!=-99&&trBottom!=-99&&tr_omega[trTop]*tr_omega[trBottom]>0){
       	 //cout<<"  this pair is the same sign!!!   Moller?  "<<coplanarity<<endl;

	 TLorentzVector* pTop=new TLorentzVector(tr_px[trTop],
						 tr_py[trTop],
						 tr_pz[trTop],
						 tr_p[trTop]);
	 TLorentzVector* pBottom=new TLorentzVector(tr_px[trBottom],
						 tr_py[trBottom],
						 tr_pz[trBottom],
						 tr_p[trBottom]);
	 double mass=sqrt(pTop->Dot(*pBottom));
	 if(tr_omega[trTop]<0){
	   //	   cout<<"Both positrons  "<<tr_omega[trTop]<<endl;
	   h_Ecl_TwoPositrons_coplanarity -> Fill(coplanarity);	   
	   h_EclX_EclY_TwoPositrons->Fill(cl_x[clTop],cl_y[clTop]);
	   h_EclX_EclY_TwoPositrons->Fill(cl_x[clBottom],cl_y[clBottom]);
	   h_Ecl_Ptrk_from_position_TwoPositrons_ele->Fill(cl_E[clTop], momFromRadius(radiusFromECAL(cl_x[clTop],cl_z[clTop],b),BEff));
	   h_Ecl_Ptrk_from_position_TwoPositrons_ele->Fill(cl_E[clBottom], momFromRadius(radiusFromECAL(cl_x[clBottom],cl_z[clBottom],b),BEff));
	   h_Ecl_TwoPositrons_mass->Fill(mass);
	   h_Ecl_TwoPositrons_esum->Fill(cl_E[clTop]+cl_E[clBottom]);

	 } else {
	   
	   h_Ecl_TwoElectrons_coplanarity -> Fill(coplanarity);
	   h_EclX_EclY_TwoElectrons->Fill(cl_x[clTop],cl_y[clTop]);
	   h_EclX_EclY_TwoElectrons->Fill(cl_x[clBottom],cl_y[clBottom]);
	   h_Ecl_Ptrk_from_position_TwoElectrons_ele->Fill(cl_E[clTop], momFromRadius(radiusFromECAL(cl_x[clTop],cl_z[clTop],b),BEff));
	   h_Ecl_Ptrk_from_position_TwoElectrons_ele->Fill(cl_E[clBottom], momFromRadius(radiusFromECAL(cl_x[clBottom],cl_z[clBottom],b),BEff));
	   //	   if(cl_E[clTop]+cl_E[clBottom]>0.75 && cl_E[clTop]+cl_E[clBottom]<0.9)
	     h_Ecl_TwoElectrons_mass->Fill(mass);
	     h_Ecl_TwoElectrons_esum->Fill(cl_E[clTop]+cl_E[clBottom]);
	     //	     h_Ecl_TwoElectrons_esum->Fill(tr_p[trTop]+tr_p[trBottom]);
	 }
       }
     }

   }

   missPositron.close();
   missElectron.close();


   TFile* out=new TFile(outpre+"out.root","RECREATE");
   cout<<"Total of pairs found = "<<pairsFound<<" out of "<<nentries<<endl;
   
   gStyle->SetOptStat(0);

   TCanvas* c1=new TCanvas();
   h_coplan_Esum1->Draw("colz");
   c1->SaveAs(outpre+"CoplanarityVsESum.pdf");

   h_E1vsE2_cop180->Draw("colz");
   c1->SaveAs(outpre+"ETopVsEBottom-Coplan-180.pdf");
   
   h_E1vsE2_cop160->Draw("colz");
   c1->SaveAs(outpre+"ETopVsEBottom-Coplan-160.pdf");


   TLegend leg(0.2,0.7,0.4,0.9);
   leg.AddEntry(h_ESum_cop160,"Coplanarity ~ 160","l");
   leg.AddEntry(h_ESum_cop160_notracks,"No Tracks","l");
   leg.AddEntry(h_ESum_cop160_eletrack,"Electron Track","l");
   leg.AddEntry(h_ESum_cop160_postrack,"Positron Track","l");
   leg.AddEntry(h_ESum_cop160_bothtracks,"Both Tracks","l");
   
   h_ESum_cop160->SetLineColor(1);
   h_ESum_cop160->SetXTitle("ECal Energy Sum (GeV)");
   h_ESum_cop160_notracks->SetLineStyle(2);
   h_ESum_cop160_notracks->SetLineColor(1);
   h_ESum_cop160_bothtracks->SetLineColor(2);
   h_ESum_cop160_eletrack->SetLineColor(3);
   h_ESum_cop160_postrack->SetLineColor(4);
   h_ESum_cop160->Draw();
   h_ESum_cop160_bothtracks->Draw("same");
   h_ESum_cop160_notracks->Draw("same");
   h_ESum_cop160_eletrack->Draw("same");
   h_ESum_cop160_postrack->Draw("same");
   leg.Draw();
   c1->SaveAs(outpre+"ESum-Coplan-160.pdf");
   
   TLegend leg2(0.2,0.7,0.4,0.9);
   leg2.AddEntry(h_ESum_cop180,"Coplanarity ~ 180","l");
   leg2.AddEntry(h_ESum_cop180_notracks,"No Tracks","l");
   leg2.AddEntry(h_ESum_cop180_eletrack,"Electron Track","l");
   leg2.AddEntry(h_ESum_cop180_postrack,"Positron Track","l");
   leg2.AddEntry(h_ESum_cop180_bothtracks,"Both Tracks","l");
   
   h_ESum_cop180->SetXTitle("ECal Energy Sum (GeV)");
   h_ESum_cop180->SetLineColor(1);
   h_ESum_cop180_notracks->SetLineStyle(2);
   h_ESum_cop180_notracks->SetLineColor(1);
   h_ESum_cop180_bothtracks->SetLineColor(2);
   h_ESum_cop180_eletrack->SetLineColor(3);
   h_ESum_cop180_postrack->SetLineColor(4);
   h_ESum_cop180->Draw();
   h_ESum_cop180_bothtracks->Draw("same");
   h_ESum_cop180_notracks->Draw("same");
   h_ESum_cop180_eletrack->Draw("same");
   h_ESum_cop180_postrack->Draw("same");
   leg2.Draw();
   c1->SaveAs(outpre+"ESum-Coplan-180.pdf");

   h_diffTkCl_x->Draw();
   c1->SaveAs(outpre+"delta-X.pdf");
   h_diffTkCl_y->Draw();
   c1->SaveAs(outpre+"delta-Y.pdf");
   h_diffTkCl_E->Draw();
   c1->SaveAs(outpre+"delta-E.pdf");
   
   h_trkmatch_cop160->SetLineColor(2);
   h_trkmatch_cop180->Draw();
   h_trkmatch_cop160->Draw("same");
   c1->SaveAs(outpre+"trackMatch.pdf");

 
   /*   Plot the WAB stuff   */  

   TLegend legWAB0(0.6,0.8,0.9,0.9);
   legWAB0.AddEntry(h_ntrk_cop160_wab_found,"Found WAB Electron","l");
   legWAB0.AddEntry(h_ntrk_cop160_wab_missed,"Missed WAB Electron","l");

   h_ntrk_cop160_wab_found->SetXTitle("# Tracks In Event");
   h_ntrk_cop160_wab_found->Draw();
   h_ntrk_cop160_wab_found->SetLineColor(2);
   h_ntrk_cop160_wab_missed->SetLineColor(4);
   h_ntrk_cop160_wab_found->SetLineWidth(3);
   h_ntrk_cop160_wab_missed->SetLineWidth(3);
   h_ntrk_cop160_wab_missed->Draw("same");
   legWAB0.Draw();
   c1->SaveAs(outpre+"WAB-ntrks.pdf");

   ////////  energy   //////////////
   TLegend legWAB1(0.1,0.8,0.3,0.9);
   legWAB1.AddEntry(h_Ecl_cop160_wab_photon,"WAB Photon","l");
   legWAB1.AddEntry(h_Ecl_cop160_wab_electron,"WAB Electron","l");
   legWAB1.AddEntry(h_Ecl_cop160_wab_missed,"WAB Missed Track","l");
   
   h_Ecl_cop160_wab_photon->SetXTitle("Cluster Energy (GeV)");
   h_Ecl_cop160_wab_photon->SetLineColor(1);
   h_Ecl_cop160_wab_electron->SetLineColor(2);
   h_Ecl_cop160_wab_missed->SetLineColor(4);

   TCanvas *ct = new TCanvas("ct","transparent pad",200,10,700,500);
   TPad *pad1 = new TPad("pad1","",0,0,1,1);
   TPad *pad2 = new TPad("pad2","",0,0,1,1);
   pad2->SetFillStyle(4000); //will be transparent
   pad2->SetFillStyle(4000); //will be transparent
   pad1->Draw();
   pad1->cd();
   h_Ecl_cop160_wab_photon->Draw();
   h_Ecl_cop160_wab_electron->Draw("same");
   h_Ecl_cop160_wab_missed->Draw("same");
   
   TH1D* denom=(TH1D*)h_Ecl_cop160_wab_electron->Clone();
   denom->Sumw2();
   denom->Add(h_Ecl_cop160_wab_missed);   
   denom->Rebin(4);
   TH1D* eff=(TH1D*)h_Ecl_cop160_wab_electron->Clone();
   eff->Sumw2();
   eff->Rebin(4);
   eff->Divide(denom);
   eff->SetLineWidth(3);
   ct->cd();
   Double_t ymin = 0.0;
   Double_t ymax = 1.0;
   Double_t dy = (ymax-ymin)/0.8; //10 per cent margins top and bottom
   Double_t xmin = 0.1;
   Double_t xmax = 0.6;
   Double_t dx = (xmax-xmin)/0.8; //10 per cent margins left and right
   pad2->Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy);
   pad2->Draw();
   pad2->cd();
   eff->SetLineColor(kBlack);
   TH1* effWABElectron=(TH1*)eff->Clone();
   eff->Draw("][samese");
   pad2->Update();

   TGaxis *axis = new TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L");
   axis->SetLabelColor(kRed);
   axis->Draw();

   legWAB1.Draw();  
   ct->SaveAs(outpre+"WAB-cluster-energy.pdf");


   //////////////   X position (of cluster)   //////////////////
   c1->cd();

   TLegend legWAB2(0.2,0.7,0.5,0.9);
   legWAB2.AddEntry(h_EclX_cop160_wab_photon,"WAB Photon","l");
   legWAB2.AddEntry(h_EclX_cop160_wab_electron,"WAB Electron","l");
   legWAB2.AddEntry(h_EclX_cop160_wab_missed,"WAB Missed Track","l");
 
   h_EclX_cop160_wab_photon->SetXTitle("Cluster X (mm)");
   h_EclX_cop160_wab_photon->SetLineColor(1);
   h_EclX_cop160_wab_electron->SetLineColor(2);
   h_EclX_cop160_wab_missed->SetLineColor(4);

   h_EclX_cop160_wab_photon->Draw();
   h_EclX_cop160_wab_electron->Draw("same");
   h_EclX_cop160_wab_missed->Draw("same");
   legWAB2.Draw();
   c1->SaveAs(outpre+"WAB-cluster-x.pdf");

 
   TLegend legWAB3(0.2,0.7,0.5,0.9);
   legWAB3.AddEntry(h_EclY_cop160_wab_photon,"WAB Photon","l");
   legWAB3.AddEntry(h_EclY_cop160_wab_electron,"WAB Electron","l");
   legWAB3.AddEntry(h_EclY_cop160_wab_missed,"WAB Missed Track","l");
 

   h_EclY_cop160_wab_photon->SetXTitle("Cluster Y (mm)");
   h_EclY_cop160_wab_photon->SetLineColor(1);
   h_EclY_cop160_wab_electron->SetLineColor(2);
   h_EclY_cop160_wab_missed->SetLineColor(4);
   
   h_EclY_cop160_wab_photon->SetMaximum( h_EclY_cop160_wab_photon->GetMaximum()*1.5);
   h_EclY_cop160_wab_photon->Draw();
   h_EclY_cop160_wab_electron->Draw("same");
   h_EclY_cop160_wab_missed->Draw("same");
   legWAB3.Draw();
   c1->SaveAs(outpre+"WAB-cluster-y.pdf");


   TLegend legWABD3(0.2,0.7,0.5,0.9);
   legWABD3.AddEntry(h_ClD_cop160_wab_photon,"WAB Photon","l");
   legWABD3.AddEntry(h_ClD_cop160_wab_electron,"WAB Electron","l");
   legWABD3.AddEntry(h_ClD_cop160_wab_missed,"WAB Missed Track","l");
 

   h_ClD_cop160_wab_photon->SetXTitle("Distance From Photon (mm)");
   h_ClD_cop160_wab_photon->SetLineColor(1);
   h_ClD_cop160_wab_electron->SetLineColor(2);
   h_ClD_cop160_wab_missed->SetLineColor(4);
   
   h_ClD_cop160_wab_photon->SetMaximum( h_ClD_cop160_wab_photon->GetMaximum()*1.5);
   h_ClD_cop160_wab_photon->Draw();
   h_ClD_cop160_wab_electron->Draw("same");
   h_ClD_cop160_wab_missed->Draw("same");
   legWABD3.Draw();
   c1->SaveAs(outpre+"WAB-cluster-distance-from-photon.pdf");



   /*  the WAB tail that's at 180 degrees  */
   TLegend legWAB4(0.6,0.7,0.9,0.9);
   legWAB4.AddEntry(h_Ecl_cop180_wab_photon,"WAB Photon","l");
   legWAB4.AddEntry(h_Ecl_cop180_wab_electron,"WAB Electron","l");
   legWAB4.AddEntry(h_Ecl_cop180_wab_missed,"WAB Missed Track","l");

   
   h_Ecl_cop180_wab_photon->SetXTitle("Cluster Energy (GeV)");
   h_Ecl_cop180_wab_photon->SetLineColor(1);
   h_Ecl_cop180_wab_electron->SetLineColor(2);
   h_Ecl_cop180_wab_missed->SetLineColor(4);

   h_Ecl_cop180_wab_photon->Draw();
   h_Ecl_cop180_wab_electron->Draw("same");
   h_Ecl_cop180_wab_missed->Draw("same");
   legWAB4.Draw();
   c1->SaveAs(outpre+"WAB-cluster-energy-180degrees.pdf");

   TLegend legWAB5(0.2,0.7,0.5,0.9);
   legWAB5.AddEntry(h_EclX_cop180_wab_photon,"WAB Photon","l");
   legWAB5.AddEntry(h_EclX_cop180_wab_electron,"WAB Electron","l");
   legWAB5.AddEntry(h_EclX_cop180_wab_missed,"WAB Missed Track","l");
 
   h_EclX_cop180_wab_photon->SetXTitle("Cluster X (mm)");
   h_EclX_cop180_wab_photon->SetLineColor(1);
   h_EclX_cop180_wab_electron->SetLineColor(2);
   h_EclX_cop180_wab_missed->SetLineColor(4);

   h_EclX_cop180_wab_photon->Draw();
   h_EclX_cop180_wab_electron->Draw("same");
   h_EclX_cop180_wab_missed->Draw("same");
   legWAB5.Draw();
   c1->SaveAs(outpre+"WAB-cluster-x-180degrees.pdf");

 
   TLegend legWAB6(0.2,0.7,0.5,0.9);
   legWAB6.AddEntry(h_EclY_cop180_wab_photon,"WAB Photon","l");
   legWAB6.AddEntry(h_EclY_cop180_wab_electron,"WAB Electron","l");
   legWAB6.AddEntry(h_EclY_cop180_wab_missed,"WAB Missed Track","l");
 

   h_EclY_cop180_wab_photon->SetXTitle("Cluster Y (mm)");
   h_EclY_cop180_wab_photon->SetLineColor(1);
   h_EclY_cop180_wab_electron->SetLineColor(2);
   h_EclY_cop180_wab_missed->SetLineColor(4);
   
   h_EclY_cop180_wab_photon->SetMaximum( h_EclY_cop180_wab_photon->GetMaximum()*1.5);
   h_EclY_cop180_wab_photon->Draw();
   h_EclY_cop180_wab_electron->Draw("same");
   h_EclY_cop180_wab_missed->Draw("same");
   legWAB6.Draw();
   c1->SaveAs(outpre+"WAB-cluster-y-180degrees.pdf");

   TLegend legWABD6(0.2,0.7,0.5,0.9);
   legWABD6.AddEntry(h_ClD_cop180_wab_photon,"WAB Photon","l");
   legWABD6.AddEntry(h_ClD_cop180_wab_electron,"WAB Electron","l");
   legWABD6.AddEntry(h_ClD_cop180_wab_missed,"WAB Missed Track","l");
 

   h_ClD_cop180_wab_photon->SetXTitle("Distance From Photon(mm)");
   h_ClD_cop180_wab_photon->SetLineColor(1);
   h_ClD_cop180_wab_electron->SetLineColor(2);
   h_ClD_cop180_wab_missed->SetLineColor(4);
   
   h_ClD_cop180_wab_photon->SetMaximum( h_ClD_cop180_wab_photon->GetMaximum()*1.5);
   h_ClD_cop180_wab_photon->Draw();
   h_ClD_cop180_wab_electron->Draw("same");
   h_ClD_cop180_wab_missed->Draw("same");
   legWABD6.Draw();
   c1->SaveAs(outpre+"WAB-cluster-distance-from-photon-180degrees.pdf");

   /////////////////////////////////////////////////////////////////////////////

   /* plot he middle ESum slice  */
   TLegend legMIDESUM4(0.6,0.7,0.9,0.9);
   legMIDESUM4.AddEntry(h_Ecl_cop180_midESum_positron,"Positron","l");
   legMIDESUM4.AddEntry(h_Ecl_cop180_midESum_electron,"Electron","l");
   legMIDESUM4.AddEntry(h_Ecl_cop180_midESum_mis_ele,"Missed Electron","l");
   legMIDESUM4.AddEntry(h_Ecl_cop180_midESum_mis_pos,"Missed Positron","l");
   legMIDESUM4.AddEntry(h_Ecl_cop180_midESum_mis_both_ele_side,"Missed Both:  Electron","l");
   legMIDESUM4.AddEntry(h_Ecl_cop180_midESum_mis_both_pos_side,"Missed Both:  Positron","l");

   
   h_Ecl_cop180_midESum_positron->SetXTitle("Cluster Energy (GeV)");
   h_Ecl_cop180_midESum_positron->SetLineColor(1);
   h_Ecl_cop180_midESum_electron->SetLineColor(2);
   h_Ecl_cop180_midESum_mis_ele->SetLineColor(4);
   h_Ecl_cop180_midESum_mis_pos->SetLineColor(3);
   h_Ecl_cop180_midESum_mis_both_pos_side->SetLineColor(1);
   h_Ecl_cop180_midESum_mis_both_ele_side->SetLineColor(2);
   h_Ecl_cop180_midESum_mis_both_pos_side->SetLineStyle(2);
   h_Ecl_cop180_midESum_mis_both_ele_side->SetLineStyle(2);

   h_Ecl_cop180_midESum_positron->SetMaximum( h_Ecl_cop180_midESum_electron->GetMaximum()*1.5);

   h_Ecl_cop180_midESum_positron->Draw();
   h_Ecl_cop180_midESum_electron->Draw("same");
   h_Ecl_cop180_midESum_mis_ele->Draw("same");
   h_Ecl_cop180_midESum_mis_pos->Draw("same");
   h_Ecl_cop180_midESum_mis_both_ele_side->Draw("same");
   h_Ecl_cop180_midESum_mis_both_pos_side->Draw("same");

   legMIDESUM4.Draw();
   c1->SaveAs(outpre+"MIDESUM-cluster-energy-180degrees.pdf");



   TLegend legMIDESUM5(0.6,0.7,0.9,0.9);
   legMIDESUM5.AddEntry(h_EclX_cop180_midESum_positron,"Positron","l");
   legMIDESUM5.AddEntry(h_EclX_cop180_midESum_electron,"Electron","l");
   legMIDESUM5.AddEntry(h_EclX_cop180_midESum_mis_ele,"Missed Electron","l");
   legMIDESUM5.AddEntry(h_EclX_cop180_midESum_mis_pos,"Missed Positron","l");
   legMIDESUM5.AddEntry(h_EclX_cop180_midESum_mis_both_ele_side,"Missed Both:  Electron","l");
   legMIDESUM5.AddEntry(h_EclX_cop180_midESum_mis_both_pos_side,"Missed Both:  Positron","l");

   
   h_EclX_cop180_midESum_positron->SetXTitle("Cluster X (mm)");
   h_EclX_cop180_midESum_positron->SetLineColor(1);
   h_EclX_cop180_midESum_electron->SetLineColor(2);
   h_EclX_cop180_midESum_mis_ele->SetLineColor(4);
   h_EclX_cop180_midESum_mis_pos->SetLineColor(3);
   h_EclX_cop180_midESum_mis_both_pos_side->SetLineColor(1);
   h_EclX_cop180_midESum_mis_both_ele_side->SetLineColor(2);
   h_EclX_cop180_midESum_mis_both_pos_side->SetLineStyle(2);
   h_EclX_cop180_midESum_mis_both_ele_side->SetLineStyle(2);

   h_EclX_cop180_midESum_positron->SetMaximum( h_EclX_cop180_midESum_positron->GetMaximum()*1.5);
   h_EclX_cop180_midESum_positron->Draw();
   h_EclX_cop180_midESum_electron->Draw("same");
   h_EclX_cop180_midESum_mis_ele->Draw("same");
   h_EclX_cop180_midESum_mis_pos->Draw("same");
   h_EclX_cop180_midESum_mis_both_ele_side->Draw("same");
   h_EclX_cop180_midESum_mis_both_pos_side->Draw("same");

   legMIDESUM5.Draw();
   c1->SaveAs(outpre+"MIDESUM-cluster-x-180degrees.pdf");


   TLegend legMIDESUM6(0.6,0.7,0.9,0.9);
   legMIDESUM6.AddEntry(h_EclY_cop180_midESum_positron,"Positron","l");
   legMIDESUM6.AddEntry(h_EclY_cop180_midESum_electron,"Electron","l");
   legMIDESUM6.AddEntry(h_EclY_cop180_midESum_mis_ele,"Missed Electron","l");
   legMIDESUM6.AddEntry(h_EclY_cop180_midESum_mis_pos,"Missed Positron","l");
   legMIDESUM6.AddEntry(h_EclY_cop180_midESum_mis_both_ele_side,"Missed Both:  Electron","l");
   legMIDESUM6.AddEntry(h_EclY_cop180_midESum_mis_both_pos_side,"Missed Both:  Positron","l");

   
   h_EclY_cop180_midESum_positron->SetXTitle("Cluster Y (mm)");
   h_EclY_cop180_midESum_positron->SetLineColor(1);
   h_EclY_cop180_midESum_electron->SetLineColor(2);
   h_EclY_cop180_midESum_mis_ele->SetLineColor(4);
   h_EclY_cop180_midESum_mis_pos->SetLineColor(3);
   h_EclY_cop180_midESum_mis_both_pos_side->SetLineColor(1);
   h_EclY_cop180_midESum_mis_both_ele_side->SetLineColor(2);
   h_EclY_cop180_midESum_mis_both_pos_side->SetLineStyle(2);
   h_EclY_cop180_midESum_mis_both_ele_side->SetLineStyle(2);
   h_EclY_cop180_midESum_positron->SetMaximum( h_EclY_cop180_midESum_positron->GetMaximum()*1.5);
   h_EclY_cop180_midESum_positron->Draw();
   h_EclY_cop180_midESum_electron->Draw("same");
   h_EclY_cop180_midESum_mis_ele->Draw("same");
   h_EclY_cop180_midESum_mis_pos->Draw("same");
   h_EclY_cop180_midESum_mis_both_ele_side->Draw("same");
   h_EclY_cop180_midESum_mis_both_pos_side->Draw("same");

   legMIDESUM6.Draw();
   c1->SaveAs(outpre+"MIDESUM-cluster-y-180degrees.pdf");


   TLegend legMIDESUMD6(0.6,0.7,0.9,0.9);
   legMIDESUMD6.AddEntry(h_ClD_cop180_midESum_positron,"Positron","l");
   legMIDESUMD6.AddEntry(h_ClD_cop180_midESum_electron,"Electron","l");
   legMIDESUMD6.AddEntry(h_ClD_cop180_midESum_mis_ele,"Missed Electron","l");
   legMIDESUMD6.AddEntry(h_ClD_cop180_midESum_mis_pos,"Missed Positron","l");
   legMIDESUMD6.AddEntry(h_ClD_cop180_midESum_mis_both_ele_side,"Missed Both:  Electron","l");
   legMIDESUMD6.AddEntry(h_ClD_cop180_midESum_mis_both_pos_side,"Missed Both:  Positron","l");

   
   h_ClD_cop180_midESum_positron->SetXTitle("Distance From Photon (mm)");
   h_ClD_cop180_midESum_positron->SetLineColor(1);
   h_ClD_cop180_midESum_electron->SetLineColor(2);
   h_ClD_cop180_midESum_mis_ele->SetLineColor(4);
   h_ClD_cop180_midESum_mis_pos->SetLineColor(3);
   h_ClD_cop180_midESum_mis_both_pos_side->SetLineColor(1);
   h_ClD_cop180_midESum_mis_both_ele_side->SetLineColor(2);
   h_ClD_cop180_midESum_mis_both_pos_side->SetLineStyle(2);
   h_ClD_cop180_midESum_mis_both_ele_side->SetLineStyle(2);
   h_ClD_cop180_midESum_positron->SetMaximum( h_ClD_cop180_midESum_electron->GetMaximum()*1.5);
   h_ClD_cop180_midESum_positron->Draw();
   h_ClD_cop180_midESum_electron->Draw("same");
   h_ClD_cop180_midESum_mis_ele->Draw("same");
   h_ClD_cop180_midESum_mis_pos->Draw("same");
   h_ClD_cop180_midESum_mis_both_ele_side->Draw("same");
   h_ClD_cop180_midESum_mis_both_pos_side->Draw("same");

   legMIDESUMD6.Draw();
   c1->SaveAs(outpre+"MIDESUM-cluster-distance-from-photon-180degrees.pdf");


   ///*** get some efficiency plots for the MIDESUM set of plots   ***///

   denom = (TH1D*)h_Ecl_cop180_midESum_pos_side_found_ele->Clone();
   denom->Rebin(4);
   denom->Sumw2();
   eff= (TH1D*)h_Ecl_cop180_midESum_pos_side_found_ele_found_pos->Clone();
   eff->Rebin(4);
   eff->Sumw2();
   eff->Divide(denom);
   eff->SetLineWidth(3);
   TLegend legMIDESUM7(0.1,0.8,0.4,0.9);
   legMIDESUM7.AddEntry(h_Ecl_cop180_midESum_pos_side_found_ele,"Positron-Side Clusters","l"); 
   legMIDESUM7.AddEntry(h_Ecl_cop180_midESum_mis_pos,"No Positron Track","l");

  
   ct = new TCanvas("ct","transparent pad",200,10,700,500);
   pad1 = new TPad("pad1","",0,0,1,1);
   pad2 = new TPad("pad2","",0,0,1,1);
   pad2->SetFillStyle(4000); //will be transparent
   pad2->SetFillStyle(4000); //will be transparent
   pad1->Draw();
   pad1->cd();

   h_Ecl_cop180_midESum_pos_side_found_ele->SetXTitle("Cluster Energy (GeV)");
   h_Ecl_cop180_midESum_pos_side_found_ele->SetLineColor(1);
   h_Ecl_cop180_midESum_pos_side_found_ele->SetLineColor(2);
   h_Ecl_cop180_midESum_mis_pos->SetLineColor(3);

   h_Ecl_cop180_midESum_pos_side_found_ele->Draw();  
   h_Ecl_cop180_midESum_mis_pos->Draw("same");

   ct->cd();
   ymin = 0.0;
   ymax = 1.0;
   dy = (ymax-ymin)/0.8; //10 per cent margins top and bottom
   xmin = 0.1;
   xmax = 0.6;
   dx = (xmax-xmin)/0.8; //10 per cent margins left and right
   pad2->Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy);
   pad2->Draw();
   pad2->cd();
   eff->SetLineColor(kBlack);
   eff->Draw("][samese");
   pad2->Update();

   axis = new TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L");
   axis->SetLabelColor(kRed);
   axis->Draw();
   legMIDESUM7.Draw();
   ct->SaveAs(outpre+"MIDESUM-cluster-energy-positron-efficiency.pdf");


   denom = (TH1D*)h_Ecl_cop180_midESum_ele_side_found_pos->Clone();
   denom->Rebin(4);
   denom->Sumw2();
   eff= (TH1D*)h_Ecl_cop180_midESum_ele_side_found_pos_found_ele->Clone();
   eff->Rebin(4);
   eff->Sumw2();
   eff->Divide(denom);
   eff->SetLineWidth(3);

   TLegend legMIDESUM8(0.6,0.2,0.9,0.3);
   legMIDESUM8.AddEntry(h_Ecl_cop180_midESum_pos_side_found_ele,"Electron-Side Clusters","l"); 
   legMIDESUM8.AddEntry(h_Ecl_cop180_midESum_mis_pos,"No Electron Track","l");



   ct = new TCanvas("ct","transparent pad",200,10,700,500);
   pad1 = new TPad("pad1","",0,0,1,1);
   pad2 = new TPad("pad2","",0,0,1,1);
   pad2->SetFillStyle(4000); //will be transparent
   pad2->SetFillStyle(4000); //will be transparent
   pad1->Draw();
   pad1->cd();

   h_Ecl_cop180_midESum_ele_side_found_pos->SetXTitle("Cluster Energy (GeV)");
   h_Ecl_cop180_midESum_ele_side_found_pos->SetLineColor(1);
   h_Ecl_cop180_midESum_ele_side_found_pos->SetLineColor(2);
   h_Ecl_cop180_midESum_mis_ele->SetLineColor(3);

   h_Ecl_cop180_midESum_ele_side_found_pos->Draw();  
   h_Ecl_cop180_midESum_mis_ele->Draw("same");

   ct->cd();
   ymin = 0.0;
   ymax = 1.0;
   dy = (ymax-ymin)/0.8; //10 per cent margins top and bottom
   xmin = 0.1;
   xmax = 0.6;
   dx = (xmax-xmin)/0.8; //10 per cent margins left and right
   pad2->Range(xmin-0.1*dx,ymin-0.1*dy,xmax+0.1*dx,ymax+0.1*dy);
   pad2->Draw();
   pad2->cd();
   eff->SetLineColor(kBlack);
   eff->Draw("][samese");
   //   effWABElectron->SetLineColor(kBlue);
   //effWABElectron->Draw("][samese");
   pad2->Update();

   axis = new TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,50510,"+L");
   axis->SetLabelColor(kRed);
   axis->Draw();
   legMIDESUM8.Draw();
   ct->SaveAs(outpre+"MIDESUM-cluster-energy-electron-efficiency.pdf");


   for(std::list<TH1*>::const_iterator iterator =  histogramList.begin();iterator!= histogramList.end();++iterator){
     (*iterator)->Write();
   }
   
   h_Ecl_midESum_coplanarity->Write();
   h_Ecl_Ptrk_from_position_Tri_ele->Write();
   h_Ecl_Ptrk_from_position_Tri_pos->Write();
   h_Ecl_Ptrk_from_position_Tri_misele->Write();
   h_Ecl_Ptrk_from_position_Tri_mispos->Write();
   h_Ptrk_Ptrk_from_position_Tri_ele->Write();
   h_Ptrk_Ptrk_from_position_Tri_pos->Write();
   h_Ecl_Ptrk_from_position_WAB_ele->Write();
   h_Ecl_Ptrk_from_position_WAB_pho->Write();
   //////
   /*
   h_Ecl_TwoElectrons_coplanarity ->Write();
   h_Ecl_TwoPositrons_coplanarity ->Write();
   h_EclX_EclY_TwoElectrons->Write();
   h_EclX_EclY_TwoPositrons->Write();
   */

   for(int i=0;i<nEsumBins;i++){
     h_copl_esum_slice[i]->Write();
     h_Ecl_esum_slice_ele_side_found_pos_found_ele[i]->Write();
     h_Ecl_esum_slice_ele_side_found_pos[i]->Write();
     h_Ecl_esum_slice_pos_side_found_ele_found_pos[i]->Write();
     h_Ecl_esum_slice_pos_side_found_ele[i]->Write();
     h_Ecl_esum_slice_positron[i]->Write();
     h_Ecl_esum_slice_electron[i]->Write();
     h_Ecl_esum_slice_mis_pos[i]->Write();
     h_Ecl_esum_slice_mis_ele[i]->Write();
     
     denom = (TH1D*)h_Ecl_esum_slice_ele_side_found_pos[i]->Clone();
     denom->Rebin(4);
     denom->Sumw2();
     eff= (TH1D*)h_Ecl_esum_slice_ele_side_found_pos_found_ele[i]->Clone();
     eff->Rebin(4);
     eff->Sumw2();
     eff->Divide(denom);
     eff->SetLineWidth(3);
     name="electron_efficiency_slice";name+=i;
     eff->SetName(name);
     eff->Write();

     denom = (TH1D*)h_Ecl_esum_slice_pos_side_found_ele[i]->Clone();
     denom->Rebin(4);
     denom->Sumw2();
     eff= (TH1D*)h_Ecl_esum_slice_pos_side_found_ele_found_pos[i]->Clone();
     eff->Rebin(4);
     eff->Sumw2();
     eff->Divide(denom);
     eff->SetLineWidth(3);
     name="positron_efficiency_slice";name+=i;
     eff->SetName(name);
     eff->Write();

   }
   out->Close();

}
     


  
