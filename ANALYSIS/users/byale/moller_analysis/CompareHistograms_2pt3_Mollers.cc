#include <TH1D.h>
#include <TH2D.h>
#include <TF1.h>
#include <THStack.h>
#include <TMath.h>
#include <TFile.h>
#include <TTree.h>
#include <iostream>
#include <TStyle.h>
#include <TChain.h>
#include <TSystem.h>
#include <TCanvas.h>
#include <TLorentzVector.h>

#include <HpsEvent.h>
#include <GblTrack.h>
#include <SvtTrack.h>
#include <MCParticle.h>
//#include <TrackUtils.h>
//#include <TriggerData.h>

using namespace std;

//*****************************************
// Moller Analysis
// ****************************************

int main()
{
  
  const double radian = TMath::RadToDeg();
  const int pair = 2;
// Target Parameters
  const double rho=19.6; // g/cm3
  const double A=183.84; // g/mole
  const double t=100*4.375e-6; // cm (thickness)
  const double qe=1.6e-19;// e- charge
  const double Na=6.022e23;  // atoms/mole
  

//  const double num_files = 98*10; // # of generated Moller MC files used

const double num_files = 100*10; // wab-beam-tri files (singles0)
//const double num_files = 992*10; // wab-beam-tri files (singles1)
//const double num_files = 870*10; // wab-beam-tri files (pairs1)

//  const double MC_time = num_files*(2e6)*(2e-9);

// MC Luminosity
//  double MC_Ne = num_files*2000000*2500;
//  double MC_Lumin = (MC_Ne)*rho*t*Na/A;
//double MC_Lumin = 74*(2e6)*(625)*(4.062e-4)*(6.306e-2)*num_files; // Total luminosity for pure Mollers (2M bunches) (1/barns)
double MC_Lumin = 74*(2e6)*(2500)*(4.062e-4)*(6.306e-2)*num_files; // "" for wab-beam-tri (500k bunches)

//double MC_Lumin = 1;



  
const HpsParticle::ParticleType fs_part_type = HpsParticle::FINAL_STATE_PARTICLE;  // Collection name for FINAL_STATE_PARTICLES
// const HpsParticle::ParticleType fs_part_type = HpsParticle::FINAL_STATE_PARTICLE;  // Collection name for FINAL_STATE_PARTICLES
//  const HpsEvent::collection_t uc_part_type = HpsEvent::UC_VTX_PARTICLES;  // Collection name for unconstrained particles
//  const HpsEvent::collection_t uc_moller_type = HpsEvent::UC_MOLLER_CANDIDATES;  // Collection name for FINAL_STATE_PARTICLES
//***
const HpsParticle::ParticleType uc_moller = HpsParticle::BSC_MOLLER_CANDIDATE;  // Collection name for UC_Mollers
//const HpsParticle::ParticleType uc_moller = HpsParticle::UC_V0_CANDIDATE;  // Collection name for UC_V0
//***
//const HpsParticle::ParticleType uc_moller = HpsParticle::FINAL_STATE_PARTICLE;

  TChain *tr1 = new TChain("HPS_Event", "HPS_Event");

  //tr1->Add("/path/to/file");    // Add files to the chain
//tr1->Add("/cache/mss/hallb/hps/production/dst/wab-beam-tri/1pt05/wabv1-egsv3-triv2-g4v1_s2d6_HPS-EngRun2015-Nominal-v1_3.4.0-20150710_singles1_*.root"); // WAB-BEAM-TRI

//tr1->Add("/cache/mss/hallb/hps/production/pass2/dst/beam-tri/1pt05/egsv3-triv2-g4v1_HPS-EngRun2015-Nominal-v3_3.4.0_singles1_*.root"); //PASS2 BEAM-TRI

//tr1->Add("/work/hallb/hps/byale/mc/moller/1pt05/molv1_s2d6_HPS-EngRun2015-Nominal-v1_3.4.0-20150710_singles1_18.root"); // PURE MOLLERS
//tr1->Add("/cache/mss/hallb/hps/production/pass2/dst/moller/1pt05/molv1_s2d6_HPS-EngRun2015-Nominal-v3_3.4.0_singles1_*"); // PURE MOLLERS
//tr1->Add("/work/hallb/hps/data/engrun2015/pass1/dst/hps_005772.1*_dst_R3321.root"); // DATA
//tr1->Add("/cache/mss/hallb/hps/engrun2015/pass3/skim/moller/*"); // Pass2 Moller Skim

//tr1->Add("/scratch/byale/MollerSkim_withiso.root");
//tr1->Add("/scratch/byale/MollerSkim_v0pt8.root");


/////////// MC Files ////////////////////
//
//tr1->Add("/cache/mss/hallb/hps/production/pass3/dst/moller/1pt05/molv1_HPS-EngRun2015-Nominal-v3-1-fieldmap_3.4.1_singles1_*.root");
// Post-trident summit fixes
//tr1->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/wab-beam-tri/1pt05/wabv2-egsv5-triv2-g4v1_500kBunches_10to1_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_pairs1_*.root");
//tr1->Add("/u/group/hps/production/mc/EngRun2015Scripts/tritrig_4hitStandardRecon.root");

// PURE MOLLERS
//tr1->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/moller/1pt05/molv3_5mrad_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_singles1_*.root");

// WAB-BEAM-TRI

// Singles1
//tr1->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/wab-beam-tri/1pt05/wabv2-egsv5-triv2-g4v1_zipFix_10to1_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_singles1_*.root");

// Singles0
//tr1->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/wab-beam-tri/1pt05/wabv2-egsv5-triv2-g4v1_10to1_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.11-20161202_singles0_*.root");

// Pairs1
tr1->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/moller/2pt3/3.11-20170331/molv3_5mrad_10to1_HPS-PhysicsRun2016-Nominal-v5-0-fieldmap_3.11-20170331_run7984_singles0_*.root");
//tr1->Add("/cache/hallb/hps/physrun2016/pass0/skim/dst/moller/hps_007984.*_moller_R3.9.root");
//tr1->Add("");

  HpsEvent *ev1 = new HpsEvent(); // Tree 1
  HpsParticle *fs_part, *uc_part, *fs_part_upper, *dau_particles, *dau_part1, *dau_part2, *Moller,*moller1, *moller2;
  EcalCluster *ec_clust, *ec_clust_upper, *dau_clust1, *dau_clust2, *moller_clust1, *moller_clust2;
  EcalHit *ec_hit, *ec_hit1, *ec_hit2,*CUT_ec_hit1, *CUT_ec_hit2;
  SvtHit *svt_hit1, *svt_hit2, *DATA_svt_hit1, *DATA_svt_hit2;
  SvtTrack *moller_track1, *moller_track2, *eventTracks;
//  TriggerData *DATA_trigger;

//  GblTrack *moller_track1, *moller_track2;
  //IMPL::TrackImpl *moller_track1, *moller_track2;
  int charge1, charge2;
  bool Fiducial1 = false, Fiducial2 = false, Edge1 = false, Edge2 = false;

  tr1->SetBranchAddress("Event", &ev1);

  //TLorentzVector L_em, L_ep;      // Lorentz vectors, that to be assigned to e- and e+
  
  TFile *file_out = new TFile("moller.root", "Recreate"); // Histograms, and other necessary objects will be saved in this file

  // Moller Tests (EE, TT, TE)
  TH2D *moller_thetaE = new TH2D("Pass3 MollerCandidates","Moller Theta vs. Cluster E;Energy (GeV);Theta (rad)",200,0.0,2.5,200,0.0,0.06);
  TH1D *moller_E = new TH1D("moller Cluster E", ";Energy (GeV)", 200, 0., 2.5);
  TH2D *moller_thetaTrackE = new TH2D("Pass3 MollerCandidates","Moller Theta vs. Track E;Energy (GeV);Theta (rad)",200,0.0,2.5,200,0.0,0.06);
  TH1D *moller_TrackE = new TH1D("moller TrackE", ";Energy (GeV)", 200, 0., 2.5);

  TH1D *moller_Theta = new TH1D("moller_Theta", ";Theta (rad)", 200, 0.0, 0.06);
 
  TH1D *moller_ESum = new TH1D("moller_E1+E2","Energy Sum;Energy (GeV)", 200, 0., 2.5);
  TH2D *unrot_moller_thetaE = new TH2D("Pass3 MollerCandidates","'Unrotated' Moller Theta vs. E;Energy (GeV);Theta (rad)",200,0.0,2.5,200,0.0,0.06);
  TH1D *ETTest = new TH1D("E - Ebeam/(1+(2Ebeam/m)sin^2(theta/2)","E-Theta Test;Energy (GeV)",200,-0.4,0.4);

  TH1D *highET = new TH1D("highET","E-Theta Test;Energy (GeV)",200,-0.4,0.4);
  TH1D *DATA_highET = new TH1D("DATA_highET","E-Theta Test;Energy (GeV)",200,-0.4,0.4);
  TH1D *PURE_highET = new TH1D("PURE_highET","E-Theta Test;Energy (GeV)",200,-0.4,0.4);
  TH1D *lowET = new TH1D("lowET","E-Theta Test;Energy (GeV)",200,-0.4,0.4);
  TH1D *DATA_lowET = new TH1D("DATA_lowET","E-Theta Test;Energy (GeV)",200,-0.4,0.4);
  TH1D *PURE_lowET = new TH1D("PURE_lowET","E-Theta Test;Energy (GeV)",200,-0.4,0.4);

  TH2D *MollerEE = new TH2D("Pass3 MollerCandidates","E1 vs. E2;Energy (GeV);Energy (GeV)",200,0.0,2.5,200,0.0,2.3);
  TH2D *MollerTT = new TH2D("Pass3 MollerCandidates","Theta1 vs. Theta2;Theta (rad);Theta (rad)",200,0.0,0.06,200,0.0,0.06);
  TH1D *SinSinTest = new TH1D("Prox. to Model (m/2Ebeam)","Theta-Theta Test ;Sin(T1/2)Sin(T2/2)", 200, 0,0.0008);
  TH2D *moller_EP = new TH2D("moller_EP","Moller Track E vs. Cluster E;Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.3);

// CUT Moller Tests ("V0" = "Mollers", haven't renamed everything...)
  TH2D *CUT_moller_thetaE = new TH2D("CUT_moller_thetaE","Moller Theta vs. Track E;Energy (GeV);Theta (rad)",200,0.0,2,200,0.0,0.06);
  TH1D *TRACK_V0_E = new TH1D("Moller_Track_E","Track E;Energy (GeV)",200,0,2.3);
  TH1D *EDGE_TRACK_V0_E = new TH1D("EDGE_TRACK_Moller_E","Track E (Edge);Energy (GeV)", 200, 0., 2.3);
  TH1D *FIDUCIAL_TRACK_V0_E = new TH1D("FIDUCIAL_TRACK_Moller_E","Track E (Fiducial);Energy (GeV)", 200, 0., 2.3);
  TH1D *TRACK_V0_E1 = new TH1D("TRACK_Moller_E1","Top Track E1;Energy (GeV)", 200, 0., 2.3);
  TH1D *TRACK_V0_E2 = new TH1D("TRACK_Moller_E2","Bottom Track E2;Energy (GeV)", 200, 0., 2.3);

// ALL EVENT TRACKS
  TH1D *eventsTrackE = new TH1D("eventsTrackE","Track E;Energy (GeV)", 180, 0, 2.5);
  TH1D *DATA_eventsTrackE = new TH1D("DATA_eventsTrackE","Track E;Energy (GeV)", 180, 0, 2.5);
  TH1D *PURE_eventsTrackE = new TH1D("PURE_eventsTrackE","Track E;Energy (GeV)", 180, 0, 2.5);

  TH1D *CLUSTER_V0_E = new TH1D("CLUSTER_Moller_E","Cluster E;Energy (GeV)", 200, 0., 2.3);
  TH1D *CLUSTER_V0_E1 = new TH1D("CLUSTER_Moller_E1","Top Cluster E;Energy (GeV)", 200, 0., 2.3);
  TH1D *CLUSTER_V0_E2 = new TH1D("CLUSTER_Moller_E2","Bottom Cluster E;Energy (GeV)", 200, 0., 2.3);

  TH1D *FIDUCIAL_V0_E = new TH1D("FIDUCIAL_Moller_E","Cluster E (Fiducial);Energy (GeV)", 200, 0., 2.3);
  TH1D *EDGE_V0_E = new TH1D("EDGE_Moller_E","Cluster E (Edge);Energy (GeV)", 200, 0., 2.3);


  TH1D *CUT_V0_Theta = new TH1D("CUT_Moller_Theta", ";Unrot Theta (rad)", 200, 0.0, 0.08);

  TH1D *TRACK_V0_ESum = new TH1D("Track_Moller_ESum","Track Energy Sum;Energy (GeV)", 200, 0, 3);
  TH1D *CLUSTER_V0_ESum = new TH1D("CLUSTER_Moller_ESum","Cluster Energy Sum;Energy (GeV)", 200, 0., 3);
  TH1D *TRACK_V0_EDiff = new TH1D("TRACK_Moller_EDiff","Track Energy Difference;Energy (GeV)", 200, 0., 3);
  TH1D *CLUSTER_V0_EDiff = new TH1D("CLUSTER_Moller_EDiff","Cluster Energy Difference;Energy (GeV)", 200, 0., 3);


  TH1D *FIDUCIAL_V0_ESum = new TH1D("FIDUCIAL_Moller_ESum","Cluster Energy Sum (Fiducial);Energy (GeV)", 200, 0., 3);
  TH1D *EDGE_V0_ESum = new TH1D("EDGE_Moller_ESum","Cluster Energy Sum (Edge);Energy (GeV)", 200, 0., 3);

//  TH2D *CUT_unrot_V0_thetaE = new TH2D("CUT_unrot_Moller_thetaE","'Unrotated' Theta vs. E;Energy (GeV);Theta (rad)",200,0.0,2.3,200,0.0,0.06);
  TH2D *CUT_unrot_V0_thetaE = new TH2D("CUT_unrot_Moller_thetaE","'Unrotated' Theta vs. E (ClustE>0.6);Energy (GeV);Theta (rad)",200,0.0,2.3,200,0.0,0.06);

  TH2D *CUT_ESumE = new TH2D("CUT_ESumE","Track ESum vs. Energy;GeV;GeV",200,0.0,3,200,0.0,3);
  TH2D *DATA_ESumE = new TH2D("DATA_ESumE","Track ESum vs. Energy;GeV;GeV",200,0.0,3,200,0.0,3);
  TH2D *PURE_ESumE = new TH2D("PURE_ESumE","Track ESum vs. Energy;GeV;GeV",200,0.0,3,200,0.0,3);

  TH2D *CUT_ESumE1 = new TH2D("CUT_ESumE1","Track ESum vs. Energy;GeV;GeV",200,0.0,3,200,0.0,3);
  TH2D *CUT_ESumE2 = new TH2D("CUT_ESumE2","Track ESum vs. Energy;GeV;GeV",200,0.0,3,200,0.0,3);
  
  TH2D *VtxTrackChi2_1 = new TH2D("VtxTrackChi2_1","Vtx Chi2 vs. Track Chi2",200,0.0,20,200,0.0,20);
  TH2D *VtxTrackChi2_2 = new TH2D("VtxTrackChi2_2","Vtx Chi2 vs. Track Chi2",200,0.0,20,200,0.0,20);



  TH1D *CUT_ETTest = new TH1D("CUT_ETTest","E - Ebeam/(1+(2Ebeam/m)sin^2(theta/2);Energy (GeV)",200,-0.3,0.4);


  TH2D *TRACK_V0EE = new TH2D("TRACK_V0EE","Track E1 vs. E2;E1 (GeV);E2 (GeV)",200,0.0,2.5,200,0.0,2);
  TH2D *TRACK_V0EE_FIDUCIAL = new TH2D("TRACK_V0EE_FIDUCIAL","Track E1 vs. E2 (both fiducial);E1 (GeV);E2 (GeV)",200,0.0,2,200,0.0,2);
  TH2D *TRACK_V0EE_EDGE = new TH2D("TRACK_V0EE_EDGE","Track E1 vs. E2 (both edge);E1 (GeV);E2 (GeV)",200,0.0,2,200,0.0,2);
  TH2D *CLUSTER_V0EE = new TH2D("CLUSTER_V0EE","Cluster Electron E vs. Positron E;Positron E (GeV);Electron E (GeV)",200,0.0,2,200,0.0,2);

  TH2D *CUT_V0TT = new TH2D("CUT_MollerTT","Theta1 vs. Theta2;Theta (rad);Theta (rad)",200,0.0,0.06,200,0.0,0.06);
  TH1D *CUT_SinSinTest = new TH1D("CUT_SinSinTest","Prox. to Model (m/2Ebeam);Sin(T1/2)Sin(T2/2)", 200, 0,0.0008);
  TH2D *CUT_V0_EP = new TH2D("CUT_moller_EP","Momentum vs. Cluster Energy;Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);


// Coincidence
  TH1D *moller_coincidence = new TH1D("time1 - time2", ";time (ns)", 200, -3,3);
  TH1D *CUT_V0_coincidence = new TH1D("CUT_V0_coincidence", ";timeDiff (ns)", 200, -3,3);
  TH1D *hitTime = new TH1D("hitTime", ";time (ns)", 200,0,5);
  TH1D *DATA_CUT_V0_coincidence = new TH1D("DATA_CUT_V0_coincidence","Cluster Hit Time Difference;timeDiff (ns)", 200, -3,3);
  TH1D *PURE_CUT_V0_coincidence = new TH1D("PURE_CUT_V0_coincidence","Cluster Hit Time Difference;timeDiff (ns)", 200, -3,3);
  TH1D *DATA_hitTime = new TH1D("DATA_hitTime", ";time (ns)", 200,0,5);
  TH1D *PURE_hitTime = new TH1D("PURE_hitTime", ";time (ns)", 200,0,5);


  TH2D *energy_slope = new TH2D("energy_slope","Low E Cluster Distance from Photon Beam vs. Energy;Energy (GeV);Distance (mm)",200,0.0,1.0, 200,0.0,100);
  TH1D *seed_E = new TH1D("seed_E","Seed Energy;Energy (GeV)", 200, 0., 2.5);

  // SVT related
  TH2D *L1 = new TH2D("L1","SVT_Hits_L1;mm;mm",200,-100,30, 200,-100,100);
TH2D *L2 = new TH2D("L2","SVT_Hits_L2;mm;mm",200,-100,30, 200,-100,100);
TH2D *L3 = new TH2D("L3","SVT_Hits_L3;mm;mm",200,-100,30, 200,-100,100);
TH2D *L4 = new TH2D("L4","SVT_Hits_L4;mm;mm",200,-100,30, 200,-100,100);
TH2D *L5 = new TH2D("L5","SVT_Hits_L5;mm;mm",200,-100,30, 200,-100,100);
TH2D *L6 = new TH2D("L6","SVT_Hits_L6;mm;mm",200,-100,30, 200,-100,100);


  // ECAL-Related
  TH2D *CUT_FIDUCIAL_V0_EP = new TH2D("CUT_FIDUCIAL_V0_EP","V0 Momentum vs. E (Fiducial);Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);
  TH2D *CUT_EDGE_V0_EP = new TH2D("CUT_EDGE_V0_EP","V0 Momentum vs. E (Inner Edge);Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);

  TH2D *FIDUCIAL_allEP = new TH2D("Pass3 fs_part","Fiducial Momentum vs. E;Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);
  TH2D *FIDUCIAL_allECal_hits=new TH2D("Fiducial All ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);

  TH2D *ECal_hits=new TH2D("ECal_hits","ECal Seed Hits",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *CUT_ECal_hits=new TH2D("CUT V0 ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *CUT_ECal_seedHits=new TH2D("CUT_ECal_seedHits","",49,-24.5,24.5, 13,-6.5,6.5);

  TH2D *neg_hits=new TH2D("neg_hits","ECalHits from Clusters < 0.5 GeV",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *pos_hits=new TH2D("pos_hits","ECalHits from Clusters > 0.5 GeV",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *DATA_neg_hits=new TH2D("DATA_neg_hits","ECalHits from Clusters < 0.5 GeV",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *DATA_pos_hits=new TH2D("DATA_pos_hits","ECalHits from Clusters > 0.5 GeV",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *PURE_neg_hits=new TH2D("PURE_neg_hits","ECalHits from Clusters < 0.5 GeV",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *PURE_pos_hits=new TH2D("PURE_pos_hits","ECalHits from Clusters > 0.5 GeV",49,-24.5,24.5, 13,-6.5,6.5);

  TH2D *CUT_FIDUCIAL_ECal_hits=new TH2D("V0 ECal_hits (Fiducial)","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *CUT_EDGE_ECal_hits=new TH2D("V0 ECal_hits (Edge)","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *CUT_ECalMollers4Calib=new TH2D("","Moller Pairs w/ 1 Fiducial, 1Edge Seed",49,-24.5,24.5, 13,-6.5,6.5);

// Track parameter-related
  TH1D *phi0 = new TH1D("phi0","phi0;degrees", 200, 0,180);
  TH1D *tanLambda = new TH1D("tanLambda","Track Slope", 200, -0.5,0.5);
  TH1D *phiDiff = new TH1D("phiDiff","phiDiff;degrees", 200,-90,90);
  TH1D *DATA_phiDiff = new TH1D("DATA_phiDiff","phiDiff;degrees", 200,-90,90); 
  TH1D *PURE_phiDiff = new TH1D("PURE_phiDiff","phiDiff;degrees", 200,-90,90);

  TH2D *phi1phi2=new TH2D("phi1phi2","",200,0,250,200,0,250);

  TH1D *hitxDiff = new TH1D("hitxDiff","hitxDiff;mm", 200, -25, 25);
  TH1D *hityDiff = new TH1D("hityDiff","hityDiff;mm", 200, -25, 25);
  TH1D *DATA_hitxDiff = new TH1D("DATA_hitxDiff","DATA_hitxDiff;mm", 200, -25, 25);
  TH1D *DATA_hityDiff = new TH1D("DATA_hityDiff","DATA_hityDiff;mm", 200, -25, 25);
  TH1D *PURE_hitxDiff = new TH1D("PURE_hitxDiff","PURE_hitxDiff;mm", 200, -25, 25);
  TH1D *PURE_hityDiff = new TH1D("PURE_hityDiff","PURE_hityDiff;mm", 200, -25, 25);

  TH2D *tracksAtEcal=new TH2D("tracksAtEcal","",200,-200,100,200,-100,100);
  TH2D *DATA_tracksAtEcal=new TH2D("DATA_tracksAtEcal","",200,-200,100,200,-100,100);
  TH2D *PURE_tracksAtEcal=new TH2D("PURE_tracksAtEcal","",200,-200,100,200,-100,100);

  TH2D *pT1pT2=new TH2D("pT1pT2","",200,0,2.5,200,0,2.5);
  TH1D *pTDiff=new TH1D("pTDiff","",200,-1,1);

  TH1D *px = new TH1D("px","px;(GeV/c)", 200, -0.01,0.04); 
  TH1D *py = new TH1D("py","py;(GeV/c)", 200, -0.04, 0.04);
  TH1D *pz = new TH1D("pz","pz;(GeV/c)", 200,0, 2.3);
  TH1D *DATA_px = new TH1D("DATA_px","px;(GeV/c)", 200, -0.01,0.04);
  TH1D *DATA_py = new TH1D("DATA_py","py;(GeV/c)", 200, -0.04, 0.04);
  TH1D *DATA_pz = new TH1D("DATA_pz","pz;(GeV/c)", 200,0, 2.3);
  TH1D *PURE_px = new TH1D("PURE_px","px;(GeV/c)", 200, -0.01,0.04);
  TH1D *PURE_py = new TH1D("PURE_py","py;(GeV/c)", 200, -0.04, 0.04);
  TH1D *PURE_pz = new TH1D("PURE_pz","pz;(GeV/c)", 200,0, 2.3);


  // EP Ratio
  TH1D *CUT_EPRatio = new TH1D("CUT_EPRatio","E/P Ratio;ClusterE/TrackP", 200, 0,2);
  TH1D *CUT_FIDUCIAL_V0_EPRatio = new TH1D("CUT_FIDUCIAL_V0_EPRatio","E/P Ratio (Fiducial);ClusterE/TrackP", 200, 0,2);
  TH1D *CUT_EDGE_V0_EPRatio = new TH1D("CUT_EDGE_V0_EPRatio","E/P Ratio (Edge);ClusterE/TrackP", 200, 0,2);

  TH1D *fs_EPRatio = new TH1D("Pass3 fs_part","E/P Ratio;TrackE/TrackP", 200, 0,2);
  TH1D *FEE_EPRatio = new TH1D("Pass3 FEE (E,P>0.8)","E/P Ratio;ClusterE/TrackP", 200, 0,2);
  TH2D *FEE_EP = new TH2D("Pass3 FEE (E,P>0.8)","Momentum vs. E;Energy (GeV);Momentum (GeV/c)",200,0.0,1.056,200,0.0,1.056);

  // MASS
  TH1D *V0_Mass = new TH1D("Moller_Mass","Uncut Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *CUT_V0_Mass = new TH1D("CUT_Moller_Mass","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *massSingles1 = new TH1D("massSingles1","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *massGBL = new TH1D("massGBL","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *mass1 = new TH1D("mass1","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *mass2 = new TH1D("mass2","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *mass3 = new TH1D("mass3","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *mass4 = new TH1D("mass4","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *massMatch = new TH1D("massMatch","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *DATA_massSingles1 = new TH1D("DATA_massSingles1","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.02,0.08);
  TH1D *DATA_massGBL = new TH1D("DATA_massGBL","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *DATA_mass1 = new TH1D("DATA_mass1","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *DATA_mass2 = new TH1D("DATA_mass2","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *DATA_mass3 = new TH1D("DATA_mass3","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *DATA_mass4 = new TH1D("DATA_mass4","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *DATA_massMatch = new TH1D("DATA_massMatch","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_massSingles1 = new TH1D("PURE_massSingles1","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_massGBL = new TH1D("PURE_massGBL","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_mass1 = new TH1D("PURE_mass1","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_mass2 = new TH1D("PURE_mass2","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_mass3 = new TH1D("PURE_mass3","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_mass4 = new TH1D("PURE_mass4","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *PURE_massMatch = new TH1D("PURE_massMatch","Moller_Candidate Invariant Mass;Mass(GeV)", 200, 0.00,0.08);

  TH2D *ESumMass = new TH2D("ESumMass","ClustESum vs. Mass;GeV;ns",200,0.02,0.08,200,0,2.5);
  TH2D *DATA_ESumMass = new TH2D("DATA_ESumMass","ClustESum vs. Mass (data);GeV;ns",200,0.02,0.08,200,0,2.5);
  TH2D *PURE_ESumMass = new TH2D("PURE_ESumMass","ClustESum vs. Mass (pure);GeV;ns",200,0.02,0.08,200,0,2.5);

  // VERTEX
  TH2D *eVTX = new TH2D("Pass3 Electrons","Vtx_y vs. Vtx_x;Vtx_x (mm);Vtx_y (mm)",500,-0.00005,0.00005,500,-0.00005,0.00005);
  TH1D *MollerXVTX = new TH1D("MollerXVTX","XVtx;XVtx (mm)",200,-3,3);
  TH1D *MollerYVTX = new TH1D("MollerYVTX","YVtx;YVtx (mm)",200,-2,2);
  TH1D *MollerZVTX = new TH1D("MollerZVTX","ZVtx;ZVtx (mm)",200,-0.001,0.001);
  TH1D *CUT_V0_XVTX = new TH1D("CUT_Moller_XVTX","XVtx;XVtx (mm)",200,-0.5,0.5);
  TH1D *CUT_V0_YVTX = new TH1D("CUT_Moller_YVTX","YVtx;YVtx (mm)",200,-0.5,0.5);
  TH1D *CUT_V0_ZVTX = new TH1D("CUT_Moller_ZVTX","ZVtx;ZVtx (mm)",200,-0.01,0.01);
  
  TH1D *vtxChi2 = new TH1D("","V0 Candidate Vtx Chi2", 200, 0.,20);
  //TH1D *trackChi2 = new TH1D("","V0 Candidate Track Chi2", 200, 0.,20);
  TH1D *CUT_vtxChi2 = new TH1D("CUT_vtxChi2","TC_Mollers Vtx Chi2", 200, 0.,30);
  TH1D *CUT_trackChi2 = new TH1D("","CUT_trackChi2", 200, 0.,30);

  TH2D *electron_thetaE = new TH2D("electron_thetaE","Electron Theta vs. E (singles1 recon)",200,0.0,2,200,0.0,0.13);
  TH2D *electron_EP = new TH2D("Pass3 Data","Electron Momentum vs. E;Energy (GeV);Momentum (GeV/c)",200,0.0,2,200,0.0,2.5);
  TH1D *fs_electron_E = new TH1D("fs_electron_E", "", 200, 0., 2);
  TH1D *fs_electron_Theta = new TH1D("fs_electron_Theta", "", 200, 0.0, 0.2);

  TH1D *coplanarity = new TH1D("coplanarity","Coplanarity Angle;deg", 200, 0.0, 180);
  TH1D *trackChi2 = new TH1D("trackChi2 (top:green, bottom:blue)","TrackChi2", 200, 0.,30);


// All Particles
  TH2D *allECal_hits=new TH2D("ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *CUT_allECal_hits=new TH2D("Cut ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *WTF_gap=new TH2D("WTF_gap","",49,-24.5,24.5, 13,-6.5,6.5);
  TH1D *GapTrackE = new TH1D("GapTrackE","Track E;GeV", 200, 0., 3);



TH1D *fs_ESum = new TH1D("fs_ESum","fs Energy Sum;Energy (GeV)", 200, 0.0, 1.2);
TH1D *DATA_fs_ESum = new TH1D("DATA_fs_ESum","fs Energy Sum;Energy (GeV)", 200, 0.0, 1.2);


//////// HISTOGRAM STACKS //////////////////////////////////
THStack *Mass = new THStack("mass","Mass (Cluster-Track x:[-15,15],y:[-20,20] mm), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *MassSingles1 = new THStack("massSingles1","Mass (Singles1), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *MassGBL = new THStack("massGBL","Mass (GBL), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *Mass1 = new THStack("mass1","Mass (coincidence), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *Mass2 = new THStack("mass2","Mass (TrackE<0.85), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *Mass3 = new THStack("mass3","Mass (ESum<1.2), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *Mass4 = new THStack("mass4","Mass (thetaSum [50,80]), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");

THStack *Energy = new THStack("energy","Track Energy, Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
//THStack *Energy = new THStack("energy","Track Energy, Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV);mb/GeV");

THStack *ClustEnergy = new THStack("ClustEnergy","Cluster Energy, Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
//THStack *ClustEnergy = new THStack("ClustEnergy","Cluster Energy, Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV);mb/GeV");

THStack *ClustEnergy_TOP = new THStack("ClustEnergy_TOP","Cluster Energy (Top), Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
THStack *ClustEnergy_BOTTOM = new THStack("ClustEnergy_BOTTOM","Cluster Energy (Bottom), Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");

THStack *EDGE_ClustEnergy = new THStack("EDGE_ClustEnergy","Cluster Energy (Edge), Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
THStack *FIDUCIAL_ClustEnergy = new THStack("FIDUCIAL_ClustEnergy","Cluster Energy (Fiducial), Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
THStack *EDGE_TrackEnergy = new THStack("EDGE_TrackEnergy","Track Energy (Edge), Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
THStack *FIDUCIAL_TrackEnergy = new THStack("FIDUCIAL_TrackEnergy","Track Energy (Fiducial), Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");

//THStack *EDGE_ClustEnergy = new THStack("EDGE_ClustEnergy","Cluster Energy (Edge),  Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV);mb/GeV");
//THStack *FIDUCIAL_ClustEnergy = new THStack("FIDUCIAL_ClustEnergy","Cluster Energy (Fiducial),  Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV);mb/GeV");
//THStack *EDGE_TrackEnergy = new THStack("EDGE_TrackEnergy","Track Energy (Edge),  Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV);mb/GeV");
//THStack *FIDUCIAL_TrackEnergy = new THStack("FIDUCIAL_TrackEnergy","Track Energy (Fiducial),  Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV);mb/GeV");

THStack *Theta =new THStack("theta","Theta (-29.5 mrad), Pure (Green) WBT (blue) vs. Data (Red);(rad)");
THStack *XVtx =new THStack("XVtx","Xvtx, Pure (Green) WBT (blue) vs. Data (Red);(mm)");
THStack *YVtx =new THStack("YVtx","Yvtx, Pure (Green) WBT (blue) vs. Data (Red);(mm)");
THStack *ZVtx =new THStack("ZVtx","ZVtx, Pure (Green) WBT (blue) vs. Data (Red);(mm)");
THStack *ClusterCoincidence = new THStack("ClusterCoincidence","Cluster Coincidence, 4Hit (blue), Standard (Red);(ns)");
//THStack *ClusterCoincidence = new THStack("ClusterCoincidence","Cluster Coincidence, Pure (Green) WBT (blue) vs. Data (Red);(ns)");
THStack *ClusterCoplanarity = new THStack("ClusterCoplanarity","ClusterCoplanarity, Pure (Green) WBT (blue) vs. Data (Red);(deg)");
THStack *EE = new THStack("ESum","ESum, Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
THStack *ClustESum = new THStack("ClustESum","ClustESum, Pure (Green) WBT (blue) vs. Data (Red);(GeV);mb/GeV");
THStack *TT = new THStack("SinSin","SinSin-test, Pure (Green) WBT (blue) vs. Data (Red);(rad)");

THStack *ET = new THStack("ET","TrackE-ModelE, Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
//THStack *ET = new THStack("ET","TrackE-ModelE, Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(GeV)");

THStack *HighET = new THStack("HighET","TrackE-ModelE (Cluster > 0.5 GeV), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *LowET = new THStack("LowET","TrackE-ModelE (Cluster < 0.5 GeV), Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *TrackEGap = new THStack("TrackEGap","UC Mollers (blue) vs. All Event Tracks (red) (Data,pair1,EsumCut);(GeV)");
THStack *eventTrackE = new THStack("eventTrackE","Event TrackE, Pure (Green) WBT (blue) vs. Data (Red);(GeV)");
THStack *fsESum = new THStack("fsESum","3-track Events +/-/- ESum Tritrig MC Standard (red) vs. 4-Hit (blue);(GeV)");
THStack *TrackChi2 =new THStack("TrackChi2","Track Chi2, Pure (Green) WBT (blue) vs. Data (Red)");
THStack *VtxChi2 =new THStack("VtxChi2","VtxChi2, Pure (Green) WBT (blue) vs. Data (Red);(mm)");

THStack *HitXDiff =new THStack("HitXDiff","HitX-TrackX, Pure (Green) WBT (blue) vs. Data (Red);(mm)");
THStack *HitYDiff =new THStack("HitYDiff","HitY-TrackY, Pure (Green) WBT (blue) vs. Data (Red)");
//THStack *HitXDiff =new THStack("HitXDiff","HitX-TrackX, Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(mm)");
//THStack *HitYDiff =new THStack("HitYDiff","HitY-TrackY, Pure Mollers (Green: All, Blue: ClustE>0.6 GeV);(mm)");

THStack *PhiDiff =new THStack("PhiDiff","|phi1-phi2|, Pure (Green) WBT (blue) vs. Data (Red);(deg)");

THStack *Px = new THStack("Px","Px, Pure (Green) WBT (blue) vs. Data (Red);(GeV/c)");
THStack *Py = new THStack("Py","Py, Pure (Green) WBT (blue) vs. Data (Red);(GeV/c)");
THStack *Pz = new THStack("Pz","Pz, Pure (Green) WBT (blue) vs. Data (Red);(GeV/c)");

THStack *TanLambda = new THStack("TanLambda","Track Slope, Pure (Green) WBT (blue) vs. Data (Red)");


///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////// TREE 1: WBT MC ////////////////////////////////////////////////////////////////////////////////
  int nev1 = tr1->GetEntries();
  cout<<"Entries in Tree 1: "<<nev1<<endl;
  char outputname[200];

  // Loop over events
  for( int i = 0; i < nev1; i++ )
    {

//cout<<i<<'\n';

     // if( i%50000 == 0 )
      if(true)
	{
	  cout.flush()<<"Processed "<<i<<" events: about "<<(100.*double(i)/double(nev1))<<" % \r\n";
	}

      // Read the current (i-th) entry from the tree
      tr1->GetEntry(i);   

     int n_uc_mollers = ev1->getNumberOfParticles(uc_moller);   // Number of tracks in the collection "UC_VTX_PARTICLES"
     // These are particles which actually contain 2 sub particles, i.e. two tracks were fitted to have a same vertex
     
     // FINAL STATE PARTICLES
     int n_pos = 0;
     int n_fs_part = ev1->getNumberOfParticles(fs_part_type);
     for( int f = 0; f < n_fs_part; f++)
       {
          if(ev1->getParticle(fs_part_type, f)->getCharge()>0)
          {
             n_pos+=1;
          }
          //  fs_part = ev1->getParticle(fs_part_type, f);
          //  TRefArray *svt_tracks = fs_part->getTracks();
          //  int n_fs_tracks = svt_tracks->GetEntries();
          //  if(n_fs_tracks>0)
          //  {

            //  if(n_fs_tracks==2 && ev1->getTrack(0)->getCharge()*ev1->getTrack(1)->getCharge() < 0)
            //  {
            //     vector<double> fsMom1 = ev1->getTrack(0)->getMomentum(); double fspx1 = fsMom1[0]; double fspy1 = fsMom1[1]; double fspz1 = fsMom1[2];
            //    double fsP1 = sqrt( fspx1*fspx1 + fspy1*fspy1 + fspz1*fspz1 );

            //    vector<double> fsMom2 = ev1->getTrack(1)->getMomentum(); double fspx2 = fsMom2[0]; double fspy2 = fsMom2[1]; double fspz2 = fsMom2[2];
            //    double fsP2 = sqrt( fspx2*fspx2 + fspy2*fspy2 + fspz2*fspz2 );


          //       fs_ESum->Fill(fsP1+fsP2);

            //  }


             // for( int t = 0; t < n_fs_Tracks; t++ )
             //    {
                                  
 

             //    }             


          //  }




        //    TRefArray *ec_clusters = fs_part->getClusters();
        //    int n_clust = ec_clusters->GetEntries();
           
        //    if( n_clust > 0 )
        //    {
        //      ec_clust = (EcalCluster*)ec_clusters->At(0);
        //      double E = ec_clust->getEnergy();
        //      MC_pulser_clusterE->Fill(E);

        //    }

       }


// LOOP OVER CLUSTERS AND ASSOCIATED TRACKS

//CLusters
int n_eventClusters = ev1->getNumberOfEcalClusters();

   for( int c = 0; c < n_eventClusters; c++ )
      {

         double eventE = ev1->getEcalCluster(c)->getEnergy();

         //Cluster Cuts
         if(eventE<0.85)
         {
 

 	    //EVENT TRACKS
     	int n_eventTracks = ev1->getNumberOfTracks();
     	for( int t = 0; t < n_eventTracks; t++ )
       	 {
            
           //Track Cuts
           if(n_eventTracks>2 && ev1->getTrack(0)->getCharge()*ev1->getTrack(1)->getCharge()*ev1->getTrack(2)->getCharge()>0 && ev1->getTrack(0)->getTanLambda()*ev1->getTrack(1)->getTanLambda()*ev1->getTrack(2)->getTanLambda()<0)
           {
               vector<double> fsMom1 = ev1->getTrack(0)->getMomentum(); double fspx1 = fsMom1[0]; double fspy1 = fsMom1[1]; double fspz1 = fsMom1[2];
               double fsP1 = sqrt( fspx1*fspx1 + fspy1*fspy1 + fspz1*fspz1 );

            //   vector<double> fsMom2 = ev1->getTrack(1)->getMomentum(); double fspx2 = fsMom2[0]; double fspy2 = fsMom2[1]; double fspz2 = fsMom2[2];
            //   double fsP2 = sqrt( fspx2*fspx2 + fspy2*fspy2 + fspz2*fspz2 );

            //   vector<double> fsMom3 = ev1->getTrack(2)->getMomentum(); double fspx3 = fsMom3[0]; double fspy3 = fsMom3[1]; double fspz3 = fsMom3[2];
            //   double fsP3 = sqrt( fspx3*fspx3 + fspy3*fspy3 + fspz3*fspz3 );

             //  vector<double> fsMom2 = ev1->getTrack(1)->getMomentum(); double fspx2 = fsMom2[0]; double fspy2 = fsMom2[1]; double fspz2 = fsMom2[2];
             //  double fsP2 = sqrt( fspx2*fspx2 + fspy2*fspy2 + fspz2*fspz2 );

               //fs_ESum->Fill(fsP1+fsP2+fsP3);

           vector<double> eventMom = ev1->getTrack(t)->getMomentum(); double evpx = eventMom[0]; double evpy = eventMom[1]; double evpz = eventMom[2];

           //double eventP = sqrt( evpx*evpx + evpy*evpy + evpz*evpz );
          // if(eventP<0.85)
           if(true)
           {
           //eventsTrackE->SetLineColor(kRed);
           // eventsTrackE->Fill(eventP);
           }//Track Cuts
          }//Tracks>0        


         }//Event Tracks

        }//Cluster Cuts
      }//Event Clusters

       //int n_mc_particles = ev1->n_mc_particles;
       //TRefArray *mc_particles = ev1->get();



      for( int jj = 0; jj < n_uc_mollers; jj++ )
	{

	  Moller = ev1->getParticle(uc_moller, jj); // get the jj-th particle from the UC_VTX_PARTICLES collection

          // Vertex
          vector<double> vtx_moller = Moller->getVertexPosition();
	  double mollerMass = Moller->getMass();   // This is the parent of two particles, invariant mass from its child particles.
	  
                  
          // Get the daughter particles from the uc_part
         // TRefArray *dau_particles = uc->getParticles();
         TRefArray *mollers = Moller->getParticles();
      //   int n_mollers = mollers->GetEntries();
         moller1 = (HpsParticle*)mollers->At(0);
         moller2 = (HpsParticle*)mollers->At(1);

          TRefArray *moller_clusters1 = moller1->getClusters();   // Get ECcal clusters assoicated with that particle
          TRefArray *moller_clusters2 = moller2->getClusters();
         int n_moller_clust1 = moller_clusters1->GetEntries();           // Number of clusters (Should always be 0 or 1)
         int n_moller_clust2 = moller_clusters2->GetEntries();

          TRefArray *moller_tracks1 = moller1->getTracks();      // Get SVT tracks associated with this particle
          TRefArray *moller_tracks2 = moller2->getTracks();
         int n_moller_tracks1 = moller_tracks1->GetEntries();           // Should always be (0 or 1)
         int n_moller_tracks2 = moller_tracks2->GetEntries();


//cout<<"Tracks1: "<<n_moller_tracks1<<endl;
//cout<<"Clusters1: "<<n_moller_clust1<<endl;
//cout<<"Tracks2: "<<n_moller_tracks2<<endl;
//cout<<"Clusters2: "<<n_moller_clust2<<endl;


         if( n_moller_clust1>0 && n_moller_tracks1>0 && n_moller_clust2>0 && n_moller_tracks2>0) // Both Mollers must have at least 1 cluster and 1 track (prevents null array crash)
//           if(true)
            {
                   
// FIRST MOLLER
          moller_clust1 = (EcalCluster*)moller_clusters1->At(0);
          moller_track1 = (SvtTrack*)moller_tracks1->At(0);
          int tracktype1 = moller_track1->getType();


          // TRACK PARAMETERS
        //  double phi01 = moller_track1->getPhi0();
          double tanLambda1 = moller_track1->getTanLambda();
          double d01 = moller_track1->getD0();          

          vector<double>  mom1 = moller1->getMomentum(); double px1 = mom1[0]; double py1 = mom1[1]; double pz1 = mom1[2];
          double P1 = sqrt( px1*px1 + py1*py1 + pz1*pz1 );
          double E1 = moller_clust1->getEnergy();
          double TrackE1 = sqrt(P1*P1 + 0.0005109989*0.0005109989);
          double theta1 = atan2(sqrt(px1*px1 + py1*py1),pz1);
          //double theta1 = atan2(1,tanLambda1);
          double time1 = moller_clust1->getSeed()->getTime();

          // 'Unrotate' momentum1
          double offset = -0.0305;

          double unrot_px1 = px1*cos(offset) + pz1*sin(offset);
          double unrot_pz1 = pz1*cos(offset) - px1*sin(offset);
          double unrot_theta1 = atan2(sqrt(unrot_px1*unrot_px1 + py1*py1),unrot_pz1);
          // Find Model energy
          double denom1 = 1+2*sin(unrot_theta1/2)*sin(unrot_theta1/2)*(2300/0.5109989);
          double model1 = 2.3/denom1;

          double phi01 = 90 + atan(py1/unrot_px1)*180.0 / TMath::Pi();
          double pT1 = (3e-4)*TMath::Abs(0.5/(moller_track1->getOmega()));
          
// SECOND MOLLER
          moller_clust2 = (EcalCluster*)moller_clusters2->At(0);
          moller_track2 = (SvtTrack*)moller_tracks2->At(0);
          int tracktype2 = moller_track2->getType();

          // TRACK PARAMETERS
          // double phi02 = moller_track2->getPhi0();
          double tanLambda2 = moller_track2->getTanLambda();
          double d02 = moller_track2->getD0();

          vector<double>  mom2 = moller2->getMomentum(); double px2 = mom2[0]; double py2 = mom2[1]; double pz2 = mom2[2];
          double P2 = sqrt( px2*px2 + py2*py2 + pz2*pz2 );
          double E2 = moller_clust2->getEnergy();
          double TrackE2 = sqrt(P2*P2 + 0.0005109989*0.0005109989);
          double theta2 = atan2(sqrt(px2*px2 + py2*py2),pz2);
          double time2 = moller_clust2->getSeed()->getTime();
          // 'Unrotate' momentum2
          double unrot_px2 = px2*cos(offset) + pz2*sin(offset);
          double unrot_pz2 = pz2*cos(offset) - px2*sin(offset);
          double unrot_theta2 = atan2(sqrt(unrot_px2*unrot_px2 + py2*py2),unrot_pz2);
          // Find Model energy2
          double denom2 = 1+2*sin(unrot_theta2/2)*sin(unrot_theta2/2)*(2300/0.5109989);
          double model2 = 2.3/denom2;
   
          double phi02 = 90 + atan(py2/unrot_px2)*180.0 / TMath::Pi();
          double pT2 = (3e-4)*TMath::Abs(0.5/(moller_track2->getOmega()));

          vector<double> position1 = moller_clust1->getPosition();
          vector<double> position2 = moller_clust2->getPosition();
          vector<double> trackAtEcal1 = moller_track1->getPositionAtEcal();
               vector<double> trackAtEcal2 = moller_track2->getPositionAtEcal();
         
          TRefArray *SVT_hits1 = moller_track1->getSvtHits();
          TRefArray *SVT_hits2 = moller_track2->getSvtHits();
      //    TRefArray *CUT_ec_hits1 = moller_clust1->getEcalHits();
      //   TRefArray *CUT_ec_hits2 = moller_clust2->getEcalHits(); 

    //      TRefArray *SVT_Hits1 = moller_track1->getSvtHits();
    //      TRefArray *SVT_Hits2 = moller_track2->getSvtHits();        

           // vector<double> positionL1 = moller_track1->getSvtHits()->getPosition();



               double clusterAngle1 = atan(position1[0]/position1[1]) * 180.0 / TMath::Pi();
               double clusterAngle2 = atan(position2[0]/position2[1]) * 180.0 / TMath::Pi();


         massSingles1->Fill(mollerMass);


          //double vtxChi2 = Moller->getVertexFitChi2();

        // vtxChi2->Fill(Moller->getVertexFitChi2());
        // trackChi2->Fill(moller_track1->getChi2());
        // trackChi2->Fill(moller_track2->getChi2());

	// Only GBL Tracks w/ VtxChi2 <=10
	// if(tracktype1 > 32 && tracktype2 > 32 && Moller->getVertexFitChi2()<=10 && moller_track1->getChi2()<=15 && moller_track2->getChi2()<=15)
  //if(moller_track1->getChi2()<=10 && moller_track2->getChi2()<=10) 
   if(tracktype1 > 32 && tracktype2 > 32)
//     if(true)
      {    

//    if(!ev1->isPair0Trigger() && ev1->isPair1Trigger() && !ev1->isPulserTrigger() && !ev1->isSingle1Trigger() && !ev1->isSingle0Trigger()) // Only select events with singles1 trigger
   if(true)
//   if(ev1->isPulserTrigger())
	{

         massGBL->Fill(mollerMass);

         vtxChi2->Fill(Moller->getVertexFitChi2());
         trackChi2->Fill(moller_track1->getChi2());
         trackChi2->Fill(moller_track2->getChi2());

           // Uncut Histograms
         //  moller_thetaE->Fill(E1,theta1); moller_thetaE->Fill(E2,theta2);
           moller_thetaE->Fill(TrackE1,theta1); moller_thetaE->Fill(TrackE2,theta2);
           unrot_moller_thetaE->Fill(E1,unrot_theta1); unrot_moller_thetaE->Fill(E2,unrot_theta2);
//           moller_E->Fill(TrackE1); moller_E->Fill(TrackE2);
          // MollerEE->Fill(TrackE1,TrackE2);
           moller_Theta->Fill(unrot_theta1); moller_Theta->Fill(unrot_theta2);
           MollerTT->Fill(unrot_theta1,unrot_theta2);
           moller_ESum->Fill(TrackE1+TrackE2);
          // moller_coincidence->Fill(time1-time2);
           ETTest->Fill(model1-TrackE1); ETTest->Fill(model2-TrackE2);   
           SinSinTest->Fill(sin(unrot_theta1/2)*sin(unrot_theta2/2));
       //    moller_EP->Fill(E1,TrackE1); moller_EP->Fill(E2,TrackE2);

           V0_Mass->Fill(mollerMass);

           MollerXVTX->Fill(vtx_moller[0]); 
           MollerYVTX->Fill(vtx_moller[1]); 
           MollerZVTX->Fill(vtx_moller[2]); 

           // ECal Plot
   //        TRefArray *ec_hits1 = moller_clust1->getEcalHits(); 

 
  //         for(int hit_n=0; hit_n<ec_hits1->GetEntries(); ++hit_n)
    //              {
   //                  ec_hit1 = (EcalHit*) ec_hits1->At(hit_n);
   //                  index_x1 = ec_hit1->getXCrystalIndex();
   //                  index_y1 = ec_hit1->getYCrystalIndex();                                                       
   //                  ECal_hits->Fill(index_x1,index_y1,1);

                     // Look at individual crystal
                    // if(index_x1==-10 && index_y1==3)
    //                if((index_x1<=-5 && index_x1>=-10) && index_y1==2)
    //                 {
                      //  MolCan_EPRatio->Fill(E1/P1);
    //                 }                 
    //              }

     //       TRefArray *ec_hits2 = moller_clust2->getEcalHits();
     //         int index_x2=0, index_y2=0;

     //      for(int hit_n=0; hit_n<ec_hits2->GetEntries(); ++hit_n)
      //            {
     //                ec_hit2 = (EcalHit*) ec_hits2->At(hit_n);
     //                index_x2 = ec_hit2->getXCrystalIndex();
     //                index_y2 = ec_hit2->getYCrystalIndex();
     //                ECal_hits->Fill(index_x2,index_y2,1);

                     // Individual Crystal
                    // if(index_x2==-10 && index_y2==3)
     //                if((index_x2<=-5 && index_x2>=-10) && index_y2==2)
     //                {
                      //  MolCan_EPRatio->Fill(E2/P2);
     //                }
     //             }            

 
 /////////////// Apply Cuts to MC //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 
           // Theta1-Theta2 (Elastic Model + "Triangle Cut")
  //         if((sin(unrot_theta1/2)*sin(unrot_theta2/2)>=0.00016 && sin(unrot_theta1/2)*sin(unrot_theta2/2)<=0.00045 && unrot_theta1+unrot_theta2<=0.09) )
        //  if(sin(unrot_theta1/2)*sin(unrot_theta2/2)>=0.00016)
        if(abs(time1-time2)<=1.7)
     //   if(abs(time1-time2)< 2 && unrot_theta1+unrot_theta2<=0.050)
      //   if(true)
            // if((sin(unrot_theta1/2)*sin(unrot_theta2/2)<=0.00040))
  //          if(abs(phi01 - phi02) <= 20)

  //          if((phi01 <= 60 || phi01 >=120) && (phi02 <= 60 || phi02 >=120) && abs(phi01 - phi02) <= 20)
             {  
               mass1->Fill(mollerMass);
               CUT_ESumE->Fill(E1,E1+E2);
           // Energy1-Energy2
         //  if( TrackE1+TrackE2<=2.47332 && TrackE1+TrackE2>=2.09268) // 3 Sigma ESum cut
        //   if(true)
          // if( TrackE1+TrackE2>=0.8 && TrackE1+TrackE2<=1.3 && TrackE1<=0.9 && TrackE2<=0.9 && E1<=0.9 && E2<=0.9 && abs(clusterAngle1-clusterAngle2)>=80 && abs(clusterAngle1-clusterAngle2)<=150)
            // if((phi01 - phi02) > -70 && (phi01 - phi02) < 70 && TrackE1+TrackE2>=0.9 && TrackE1+TrackE2<=1.2 && E1+E2>=0.9 && E1+E2<=1.2 && TrackE1<=0.85 && TrackE2<=0.85 && E1<=0.85 && E2<=0.85)
         //   if(E1>=0.6 && E2>=0.6)
           if(true)
             { 
               mass2->Fill(mollerMass); 
           // Energy-Theta
         //  if((abs(TrackE1-model1)<=0.2 && abs(TrackE2-model2)<= 0.2))
     //      if (mollerMass<=0.055)
     //      if(unrot_theta1+unrot_theta2>=0.05)
           // if(TrackE1+TrackE2<=1.2 && TrackE1+TrackE2>=0.9 && E1+E2<=1.2 && E1+E2>=0.9)
           if(TrackE1+TrackE2<=2.6 && TrackE1+TrackE2>=2)
          //  if(true)
             {
                mass3->Fill(mollerMass);
               // Secondary Cuts
         //  if(abs(time1-time2)<=1.7)
      // if(unrot_theta1+unrot_theta2>=0.050 && unrot_theta1+unrot_theta2<=0.080)
 //        if(true)
       //  if(svt_hit1->getLayer()==6 && -6<=svt_hit1->getPosition()[0]<=-15)
       //  if((time1-time2)>=-1.25 && (time1-time2)<=1.5)
    //   if((time1-time2)>=-1.25 && (time1-time2)<=1.5 && TrackE1<=1.85 && TrackE2<=1.85) // ~3 Sigma Coincidence Cut
         
       //  if(TrackE1<=1.8 && TrackE2<=1.8 && (time1-time2)<=1.2 && (time1-time2)>=-1.2 && E1>0.65 && E2>0.65)
      //  if(TrackE1<=1.8 && TrackE2<=1.8 && trackAtEcal1[2] > 1200 && trackAtEcal2[2] > 1200)

       //    if((E1+E2)<=0.85 && (E1+E2)>=0.7) // Cluster E Cut
         // if(abs(position1[1] - trackAtEcal1[1])<=10 && abs(position2[1] - trackAtEcal2[1])<=10) // Track-Cluster Match
        // if(((TrackE1>=1.15 && TrackE2<=1.15)||(TrackE1<=1.15 && TrackE2>=1.15)) && (TrackE1<=1.2 && TrackE2<=1.2 && TrackE1>=1.1 && TrackE2>=1.1))
        //  if(((TrackE1>=1.15 && TrackE2<=1.15)||(TrackE1<=1.15 && TrackE2>=1.15)) && (TrackE1<=1.2 && TrackE2<=1.2 && TrackE1>=1.05 && TrackE2>=1.05)) // Opposite Energies cut

          //  if(abs(clusterAngle1-clusterAngle2)>=110 && unrot_theta1>=0.015 && unrot_theta1<=0.055 && unrot_theta2>=0.015 && unrot_theta2<=0.055 && (unrot_theta1 + unrot_theta2) <= 0.085 && TrackE1<=1.8 && TrackE2<=1.8)
          //if(abs(clusterAngle1-clusterAngle2)<=50 )

           // if(true)
           if(TrackE1<1.6 && TrackE2<1.6)
//Momar Cuts //if(TrackE1>=0.05 && TrackE2>=0.05 && TrackE1<=0.85 && TrackE2<=0.85 && abs(time1-time2)<=1.6 && tanLambda1*tanLambda2 < 0)
         //  if(E1<0.5 && E2<0.5)
             {

          // if((position1[0] - trackAtEcal1[0]) <= 15 && (position1[0] - trackAtEcal1[0]) >= -15 && (position1[1] - trackAtEcal1[1])<= 20 && (position1[1] - trackAtEcal1[1])>= -20 && (position2[0] - trackAtEcal2[0]) <= 15 && (position2[0] - trackAtEcal2[0]) >= -15 && (position2[1] - trackAtEcal2[1])<= 20 && (position2[1] - trackAtEcal2[1])>= -20)
          //   if((position1[1] - trackAtEcal1[1])<= 10 && (position1[1] - trackAtEcal1[1])>= -10 && (position2[1] - trackAtEcal2[1])<= 10 && (position2[1] - trackAtEcal2[1])>= -10)
            if(true)
               {

               CUT_moller_thetaE->Fill(TrackE1,theta1); CUT_moller_thetaE->Fill(TrackE2,theta2);
           //    CUT_unrot_V0_thetaE->Fill(TrackE1,unrot_theta1); CUT_unrot_V0_thetaE->Fill(TrackE2,unrot_theta2);             
            


               px->Fill(px1); px->Fill(px2);
               py->Fill(py1); py->Fill(py2);
               pz->Fill(pz1); pz->Fill(pz2);
 
               tanLambda->Fill(tanLambda1); tanLambda->Fill(tanLambda2);

  
            //   TRACK_V0_E->Fill(TrackE1); TRACK_V0_E->Fill(TrackE2);
          //     if(E1>0.6){
               TRACK_V0_E->Fill(TrackE1);
               TRACK_V0_E1->Fill(TrackE1); 
               CLUSTER_V0_E->Fill(E1);
               CLUSTER_V0_E1->Fill(E1);
               CUT_ETTest->Fill(model1-TrackE1);
         //     }
         //     if(E2>0.6){
               TRACK_V0_E->Fill(TrackE2);
               TRACK_V0_E2->Fill(TrackE2);
               CLUSTER_V0_E->Fill(E2);
               CLUSTER_V0_E2->Fill(E2);
               CUT_ETTest->Fill(model2-TrackE2);
         //     }

//               CLUSTER_V0_E->Fill(E1); CLUSTER_V0_E->Fill(E2);


             //  CLUSTER_V0_E1->Fill(E1); 
             //  CLUSTER_V0_E2->Fill(E2);


                 TRACK_V0EE->Fill(TrackE1,TrackE2);
                 CLUSTER_V0EE->Fill(E1,E2);

               //  CUT_ESumE1->Fill(TMath::Max(TrackE1,TrackE2),TrackE1+TrackE2);
               //  CUT_ESumE2->Fill(TMath::Min(TrackE1,TrackE2),TrackE1+TrackE2);

                 CUT_ESumE1->Fill(E1,E1+E2);
                 CUT_ESumE2->Fill(E2,E1+E2);
                 
             //    if(E1<0.6){
                
                 CUT_ECal_seedHits->Fill(moller_clust1->getSeed()->getXCrystalIndex(),moller_clust1->getSeed()->getYCrystalIndex());
              //   }
              //   if(E2<0.6){
                
                 CUT_ECal_seedHits->Fill(moller_clust2->getSeed()->getXCrystalIndex(),moller_clust2->getSeed()->getYCrystalIndex());
              //   }

                 VtxTrackChi2_1->Fill(moller_track1->getChi2(),Moller->getVertexFitChi2());
                 VtxTrackChi2_2->Fill(moller_track2->getChi2(),Moller->getVertexFitChi2());

         //      if(moller1->getCharge() > 0 && moller2->getCharge() < 0)
         //      {
         //        TRACK_V0EE->Fill(TrackE1,TrackE2);
         //        CLUSTER_V0EE->Fill(E1,E2);
         //       } else if (moller1->getCharge() < 0 && moller2->getCharge() > 0)
         //       {
         //         TRACK_V0EE->Fill(TrackE2,TrackE1);
         //         CLUSTER_V0EE->Fill(E2,E1);
         //       }


               CUT_V0_Theta->Fill(unrot_theta1); CUT_V0_Theta->Fill(unrot_theta2);
               CUT_V0TT->Fill(unrot_theta1,unrot_theta2);

               TRACK_V0_ESum->Fill(TrackE1+TrackE2);
               CLUSTER_V0_ESum->Fill(E1+E2);
               TRACK_V0_EDiff->Fill(abs(TrackE1-TrackE2));
               CLUSTER_V0_EDiff->Fill(abs(E1-E2));

         //      CUT_ETTest->Fill(model1-TrackE1); CUT_ETTest->Fill(model2-TrackE2); 
               CUT_SinSinTest->Fill(sin(unrot_theta1/2)*sin(unrot_theta2/2));

               CUT_V0_coincidence->Fill(time1-time2);
               hitTime->Fill(time1); hitTime->Fill(time2);
               CUT_V0_EP->Fill(E1,TrackE1); CUT_V0_EP->Fill(E2,TrackE2);

               CUT_V0_XVTX->Fill(vtx_moller[0]);
               CUT_V0_YVTX->Fill(vtx_moller[1]);
               CUT_V0_ZVTX->Fill(vtx_moller[2]);

               CUT_V0_Mass->Fill(mollerMass);

               CUT_vtxChi2->Fill(Moller->getVertexFitChi2());

               CUT_trackChi2->SetLineColor(kGreen);
               CUT_trackChi2->Fill(moller_track1->getChi2());
               CUT_trackChi2->SetLineColor(kBlue);
               CUT_trackChi2->Fill(moller_track2->getChi2());

               // Coplanarity      
               coplanarity->Fill(abs(clusterAngle1-clusterAngle2));

               ESumMass->Fill(mollerMass,E1+E2);

               // Track Parameter Plots
               phi0->Fill(phi01);  phi0->Fill(phi02);
               phiDiff->Fill(phi01 - phi02);
               phi1phi2->Fill(phi01,phi02);

              // if(E1>0.6){
              
               hitxDiff->Fill(position1[0] - trackAtEcal1[0]); 
               hityDiff->Fill(position1[1] - trackAtEcal1[1]);
              // tracksAtEcal->Fill(trackAtEcal1[0],trackAtEcal1[1]);
              // CUT_unrot_V0_thetaE->Fill(TrackE1,unrot_theta1);
              // }
            //   if(true){
              
               hitxDiff->Fill(position2[0] - trackAtEcal2[0]);
               hityDiff->Fill(position2[1] - trackAtEcal2[1]);     
              // tracksAtEcal->Fill(trackAtEcal2[0],trackAtEcal2[1]);
              // CUT_unrot_V0_thetaE->Fill(TrackE2,unrot_theta2);    
            //   }
            
             //  if(E1<0.6){
               tracksAtEcal->Fill(trackAtEcal1[0],trackAtEcal1[1]);
               CUT_unrot_V0_thetaE->Fill(TrackE1,unrot_theta1);
           //    }
           
            //   if(E2<0.6){  
               tracksAtEcal->Fill(trackAtEcal2[0],trackAtEcal2[1]);
               CUT_unrot_V0_thetaE->Fill(TrackE2,unrot_theta2);
           //    }


               //hityDiff->Fill(position1[1] - trackAtEcal1[1]); hityDiff->Fill(position2[1] - trackAtEcal2[1]);

              // tracksAtEcal->Fill(trackAtEcal1[0],trackAtEcal1[1]);
              // tracksAtEcal->Fill(trackAtEcal2[0],trackAtEcal2[1]);

               pT1pT2->Fill(pT1,pT2);
               pTDiff->Fill(abs(pT1-pT2));





          // SVT
         // TRefArray *SVT_hits1 = moller_track1->getSvtHits();
         // TRefArray *SVT_hits2 = moller_track2->getSvtHits();

            for(int hit_n=0; hit_n<SVT_hits1->GetEntries(); ++hit_n)
              {
                svt_hit1 = (SvtHit*) SVT_hits1->At(hit_n);
                vector<double> svt_hit_position1 = svt_hit1->getPosition();
                int layer = svt_hit1->getLayer();

                switch(layer){
                case 1:
                   L1->Fill(svt_hit_position1[0],svt_hit_position1[1]);
                   break;
                case 2:
                   L2->Fill(svt_hit_position1[0],svt_hit_position1[1]);
                   break;
                case 3:
                   L3->Fill(svt_hit_position1[0],svt_hit_position1[1]);
                   break;
                case 4:
                   L4->Fill(svt_hit_position1[0],svt_hit_position1[1]);
                   break;
                case 5:
                   L5->Fill(svt_hit_position1[0],svt_hit_position1[1]);
               
               if(svt_hit1->getPosition()[0]>=-13 && svt_hit1->getPosition()[0]<=-9)
               {
              // index_x1=0, index_y1=0;
               // Mystery of the gap in layer 5
            //   WTF_gap->Fill(position1[0],position1[1]);
             //  for(int hit_n=0; hit_n<CUT_ec_hits1->GetEntries(); ++hit_n)
             //     {
                    // ec_hit1 = (EcalHit*) CUT_ec_hits1->At(hit_n);
               //      index_x1 = moller_clust1->getSeed()->getXCrystalIndex();
               //      index_y1 = moller_clust1->getSeed()->getYCrystalIndex();
               //      WTF_gap->Fill(index_x1,index_y1);
               //      GapTrackE->Fill(TrackE1);
              //    }
                }
                   break;
                case 6:
                   L6->Fill(svt_hit_position1[0],svt_hit_position1[1]);
                   break;
                   
                }

              }

              for(int hit_n=0; hit_n<SVT_hits2->GetEntries(); ++hit_n)
              {
                svt_hit2 = (SvtHit*) SVT_hits2->At(hit_n);
                vector<double> svt_hit_position2 = svt_hit2->getPosition();
                int layer = svt_hit2->getLayer();

                switch(layer){
                case 1:
                   L1->Fill(svt_hit_position2[0],svt_hit_position2[1]);
                   break;
                case 2:
                   L2->Fill(svt_hit_position2[0],svt_hit_position2[1]);
                   break;
                case 3:
                   L3->Fill(svt_hit_position2[0],svt_hit_position2[1]);
                   break;
                case 4:
                   L4->Fill(svt_hit_position2[0],svt_hit_position2[1]);
                   break;
                case 5:
                   L5->Fill(svt_hit_position2[0],svt_hit_position2[1]);
 
                // if(svt_hit2->getPosition()[0]>=-13 && svt_hit2->getPosition()[0]<=-9)
                 if(true)
                 { 
                  //WTF_gap->Fill(position2[0],position2[1]); 
                //   index_x2=0, index_y2=0;
                 //  for(int hit_n=0; hit_n<CUT_ec_hits2->GetEntries(); ++hit_n)
                //  {
                    // ec_hit2 = (EcalHit*) CUT_ec_hits2->At(0);
                //     index_x2 = moller_clust2->getSeed()->getXCrystalIndex();
                //     index_y2 = moller_clust2->getSeed()->getYCrystalIndex();
                //     WTF_gap->Fill(index_x2,index_y2);
                //     GapTrackE->Fill(TrackE2);
                //  }
                 }
                   break;
                case 6:
                   L6->Fill(svt_hit_position2[0],svt_hit_position2[1]);
                   break;
                }

              }
 

      // ECAL
               TRefArray *CUT_ec_hits1 = moller_clust1->getEcalHits();
               int index_x1=0, index_y1=0;
               Fiducial1 = false, Fiducial2 = false, Edge1 = false, Edge2 = false;

           for(int hit_n=0; hit_n<CUT_ec_hits1->GetEntries(); ++hit_n)
                  {
                     ec_hit1 = (EcalHit*) CUT_ec_hits1->At(hit_n);
                     index_x1 = ec_hit1->getXCrystalIndex();
                     index_y1 = ec_hit1->getYCrystalIndex();

                     CUT_EPRatio->Fill(E1/P1);

                     // Select electron or positron tracks
                     if(E1<0.6)
                       {
                         neg_hits->Fill(index_x1,index_y1,1);
                         lowET->Fill(model1-TrackE1);
                       }
                       if(E1>0.6)
                       {
                         pos_hits->Fill(index_x1,index_y1,1);
                         highET->Fill(model1-TrackE1);
                       }

                    // Edge Elastic Cut, Moller1
                    if(((index_x1<=-2 && index_x1>=-10)&&(index_y1==2||index_y1==-2)) || (index_y1==1||index_y1==-1))
                //    if((index_x1<=-8 && index_x1>=-10)&&(index_y1==2||index_y1==-2) || ((index_x1<=-10 && index_x1>=-12)&&(index_y1==1||index_y1==-1)))
                     {
                       CUT_ECal_hits->Fill(index_x1,index_y1,1);                   
                       CUT_EDGE_ECal_hits->Fill(index_x1,index_y1,1);
                       CUT_EDGE_V0_EPRatio->Fill(E1/P1);
                       CUT_EDGE_V0_EP->Fill(E1,P1);
                       
                    //   if(E1>0.6){
                       EDGE_TRACK_V0_E->Fill(TrackE1);
                       EDGE_V0_E->Fill(E1);
                   //    }
                       if(moller_clust1->getSeed()->getXCrystalIndex()==index_x1 && moller_clust1->getSeed()->getYCrystalIndex()==index_y1)
                       {
                         Edge1 = true;
                       }

                     }

                    // Fiducial Elastic Cut, Moller1
                     if(index_y1!=1 && index_y1!=-1)
                    {
                    if( !((index_y1==2||index_y1==-2)&&(index_x1>=-10 && index_x1<=-2)))
                    {
                     CUT_ECal_hits->Fill(index_x1,index_y1,1);
                     CUT_FIDUCIAL_ECal_hits->Fill(index_x1,index_y1,1);
                     CUT_FIDUCIAL_V0_EPRatio->Fill(E1/P1);
                     CUT_FIDUCIAL_V0_EP->Fill(E1,P1);

                //     if(E1>0.6){
                     FIDUCIAL_V0_E->Fill(E1);
                     FIDUCIAL_TRACK_V0_E->Fill(TrackE1);
                //   }

                     if(moller_clust1->getSeed()->getXCrystalIndex()==index_x1 && moller_clust1->getSeed()->getYCrystalIndex()==index_y1)
                       {
                         Fiducial1 = true;
                       }

                    }
                    }
                  }

            TRefArray *CUT_ec_hits2 = moller_clust2->getEcalHits();
             int index_x2=0, index_y2=0;

           for(int hit_n=0; hit_n<CUT_ec_hits2->GetEntries(); ++hit_n)
                  {
                     ec_hit2 = (EcalHit*) CUT_ec_hits2->At(hit_n);
                     index_x2 = ec_hit2->getXCrystalIndex();
                     index_y2 = ec_hit2->getYCrystalIndex();

                     CUT_EPRatio->Fill(E2/P2);

                     // Select pos or neg tracks/hits
                     if(E2<0.5)
                       {
                         neg_hits->Fill(index_x2,index_y2,1);
                         lowET->Fill(model2-TrackE2);
                       }
                       if(E2>0.5)
                       {
                         pos_hits->Fill(index_x2,index_y2,1);
                         highET->Fill(model2-TrackE2);
                       }


                     // Edge Elastic Cut, Moller2
                     if((index_x2<=-2 && index_x2>=-10)&&((index_y2==2||index_y2==-2) || (index_y2==1||index_y2==-1)))
        //             if((index_x2<=-8 && index_x2>=-10)&&(index_y2==2||index_y2==-2) || ((index_x2<=-10 && index_x2>=-12)&&(index_y2==1||index_y2==-1)))
                     {
                       
                       CUT_ECal_hits->Fill(index_x2,index_y2,1);
                       CUT_EDGE_ECal_hits->Fill(index_x2,index_y2,1);
                       CUT_EDGE_V0_EPRatio->Fill(E2/P2);
                       CUT_EDGE_V0_EP->Fill(E2,P2);
                       

                   //    if(E2>0.6){
                       EDGE_TRACK_V0_E->Fill(TrackE2);
                       EDGE_V0_E->Fill(E2);
                  //     }

                       if(moller_clust2->getSeed()->getXCrystalIndex()==index_x2 && moller_clust2->getSeed()->getYCrystalIndex()==index_y2)
                       {
                         Edge2 = true;
                       }
                       
                     }
                     // Fiducial Elastic Cut, Moller2
                     if(index_y2!=1 && index_y2!=-1)
                     {
                     if( !((index_y2==2||index_y2==-2)&&(index_x2>=-10 && index_x2<=-2)))
                     {
                     CUT_ECal_hits->Fill(index_x2,index_y2,1);
                     CUT_FIDUCIAL_ECal_hits->Fill(index_x2,index_y2,1);
                     CUT_FIDUCIAL_V0_EPRatio->Fill(E2/P2);
                     CUT_FIDUCIAL_V0_EP->Fill(E2,P2);

                  //   if(E2>0.6){
                     FIDUCIAL_V0_E->Fill(E2);
                     FIDUCIAL_TRACK_V0_E->Fill(TrackE2);
                 //   }

                     if(moller_clust2->getSeed()->getXCrystalIndex()==index_x2 && moller_clust2->getSeed()->getYCrystalIndex()==index_y2)
                       {
                         Fiducial2 = true;
                       }
                     }
                     }
                  }


                  // Analyze Calibration Prospects
                  if((Fiducial1 && Edge2)||(Fiducial2 && Edge1))
                   {
                     CUT_ECalMollers4Calib->Fill(moller_clust1->getSeed()->getXCrystalIndex(),moller_clust1->getSeed()->getYCrystalIndex(),1);
                     CUT_ECalMollers4Calib->Fill(moller_clust2->getSeed()->getXCrystalIndex(),moller_clust2->getSeed()->getYCrystalIndex(),1);
                     
                   }

                  if((Fiducial1)&&(Fiducial2))
                   {
                     FIDUCIAL_V0_ESum->Fill(E1+E2);
                     TRACK_V0EE_FIDUCIAL->Fill(TrackE1,TrackE2);
                   }

                   if((Edge1)&&(Edge2))
                   {
                     EDGE_V0_ESum->Fill(E1+E2);
                     TRACK_V0EE_EDGE->Fill(TrackE1,TrackE2);
                   }
           
               
               if(E1 < E2)
               {
               double lowEClusterDistance = TMath::Hypot(moller_clust1->getSeed()->getXCrystalIndex() - 1393.0 * TMath::Tan(0.03052), moller_clust1->getSeed()->getYCrystalIndex());
               energy_slope->Fill(E1,lowEClusterDistance);
               }

               if(E1 > E2)
               {
               double lowEClusterDistance = TMath::Hypot(moller_clust2->getSeed()->getXCrystalIndex() - 1393.0 * TMath::Tan(0.03052), moller_clust2->getSeed()->getYCrystalIndex());
               energy_slope->Fill(E2,lowEClusterDistance);
               }

        //   if(E1>0.6){
               seed_E->Fill(moller_clust1->getSeed()->getEnergy());
        //       }
        //      if(E2>0.6){
               seed_E->Fill(moller_clust2->getSeed()->getEnergy());
        //      }



             } // Track-Cluster matching
             } // Momentum Cut
             }  // Energy-Theta
             } // Energy1-Energy2
             } // Theta1-Theta2
/////////////////////////////////////////////////////////////////////// END MOLLER CUTS ///////////////////////////////////

           } // Trigger
	 } // GBL Tracks
      } // n_moller_clust == 1 && n_moller_tracks == 1

     } // loop over Mollers
    } // loop over events

///////////////////////////////////////////////////////////////////////// END TREE 1: WBT MC ////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

         // Draw the Moller cross section from literature

         double E0=1.056;
         double hc2=0.389379e-27; // [0]
         double alpha=0.00729735; // [1]

         double X0 = 6.76641; // g*cm^-2
         double areal_d = 0.00782; // g*cm^-2
         double r0 = 1.2e-13; // cm
         double cm2_to_mb = 1e27;


         double g=E0/0.000510998;
         double beta=1-1/pow(g,2); // [5]

         double V1=pow(((g-1)/g),2); // [2]
         double V2=(2*g-1)/pow(g,2); // [3]
         double T0=E0-0.000510998;  // [4]

         
         // Two symmetric plots
      //   TF1 *XS = new TF1("XS","([0]*[1]/([5]*[4]*[4]))*([2]+([4]/x)*([4]/x -[3]) + (1/(1-[4]/x))*((1/(1-[4]/x)) -[3]))",0.010,0.528);
      //   TF1 *XS2 = new TF1("XS2","([0]*[1]/([5]*[4]*[4]))*([2]+([4]/(1.056-x))*([4]/(1.056-x) -[3]) + (1/(1-[4]/(1.056-x)))*((1/(1-[4]/(1.056-x))) -[3]))",0.528,1.056);

      //   XS->SetParameters(1,cm2_to_mb*X0*2*M_PI*r0*r0*0.000510998/2/200,V1,V2,T0,beta); // mb/GeV
      //   XS2->SetParameters(1,cm2_to_mb*X0*2*M_PI*r0*r0*0.000510998/2/200,V1,V2,T0,beta);// mb/GeV


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////// TREE 2: DATA ///////////////////////////////////////////////////////////////////////////////////
////////////// Second verse, same as the first~! ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



//  const double FCup=611.208e-9; // Gated Faraday Cup Charge for file 350, run 5772
//const double FCup=557.167e-9; // Gated Faraday Cup Charge for file 350, run 5772
// const double FCup=524.139e-9; // Gated Faraday Cup Charge for file 90, run 5772
//  const double FCup=2*28528.086e-9; // Gated Faraday Cup Charge for ALL 5772 files
// const double FCup=6754.459e-9; // Gated Faraday Cup Charge for 3* 5772 files

const double FCup=759002.391747972e-9; // Gated Faraday Cup Charge for 2016 run 7985

//  const double DATA_time=570.56172; // time for ALL 5772 files
//  const double DATA_time=10.48278; // time for 90 5772 files

  double DATA_Ne = FCup/qe;
  double DATA_Lumin = 74*2*(DATA_Ne)*(4.062e-4)*(6.306e-2);

//  double DATA_Lumin = 42.36560598*1e9; // TOTAL 5772 luminosity, corrected for SVT Bias, deadtime, etc. (1/barns)
//double DATA_Lumin = 4.403638304*1e9; // "Blinded" (10%) 5772 luminosity (1/barns) (Spreadsheet calls this "unblinded"...)

 // double DATA_Lumin = 1;

double DATA_Prescale = 4097; //eng2015 singles0, 1+2^(13-1)
//  double DATA_Prescale = 2048; // eng2015 singles1, 2^11
//  double DATA_Prescale = 1; // eng2015 pairs1, 2^0

TChain *tr2 = new TChain("HPS_Event", "HPS_Event");

// FOR NORMAL USE /////////
//  tr2->Add("/cache/mss/hallb/hps/engrun2015/pass3/dst/hps_005772.*_dst_20151010092742126.root");

//tr2->Add("/work/hallb/hps/data/physrun2016/triggerStudy/dst/7488_200nA_v6_isha70_vfs0_1.root");
//tr2->Add("/cache/mss/hallb/hps/physrun2016/noPass/dst/hps_007780_v7_200nA_3.6_*.root");

// This takes forever (>24hrs.) to process...
//tr2->Add("");
//tr2->Add("/cache/hallb/hps/physrun2016/pass0/skim/dst/moller/hps_007984.*_moller_R3.9.root");
tr2->Add("/cache/mss/hallb/hps/physrun2016/pass0/dst/hps_007984.*.root");

  HpsEvent *ev2 = new HpsEvent(); 
  tr2->SetBranchAddress("Event", &ev2);

  HpsParticle *DATA_fs_part, *DATA_uc_part, *DATA_fs_part_upper, *DATA_dau_particles, *DATA_dau_part1, *DATA_dau_part2, *DATA_Moller,*DATA_moller1, *DATA_moller2;
  EcalCluster *DATA_ec_clust, *DATA_ec_clust_upper, *DATA_dau_clust1, *DATA_dau_clust2, *DATA_moller_clust1, *DATA_moller_clust2;
  EcalHit *DATA_ec_hit, *DATA_ec_hit1, *DATA_ec_hit2,*DATA_CUT_ec_hit1, *DATA_CUT_ec_hit2;
  SvtTrack *DATA_moller_track1, *DATA_moller_track2;

  TH2D *DATA_CUT_moller_thetaE = new TH2D("DATA_CUT_moller_thetaE","Moller Theta vs. E;Energy (GeV);Theta (rad)",200,0.0,2,200,0.0,0.06);
  TH1D *DATA_CUT_moller_E = new TH1D("DATA_CUT_moller_E", ";Energy (GeV)", 200, 0.,2);
  TH1D *DATA_ClusterE = new TH1D("DATA_ClusterE","Cluster Energy;Energy (GeV)", 200, 0., 1);
  TH1D *DATA_ClusterE1 = new TH1D("DATA_ClusterE1","Cluster Energy;Energy (GeV)", 200, 0., 1);
  TH1D *DATA_ClusterE2 = new TH1D("DATA_ClusterE2","Cluster Energy;Energy (GeV)", 200, 0., 1);

  TH1D *DATA_TrackE = new TH1D("DATA_TrackE","Track Energy;Energy (GeV)", 200, 0.,2.5);
//  TH2D *DATA_ClusterEE = new TH2D("DATA_ClusterEE","Cluster E1 vs. E2;Electron E (GeV);Positron E (GeV)",200,0.0,2.5,200,0.0,2.5);
  TH2D *DATA_ClusterEE = new TH2D("DATA_ClusterEE","Cluster E1 vs. E2;E1 (GeV);E2 (GeV)",200,0.0,2,200,0.0,2.5);
  TH1D *DATA_CUT_moller_Theta = new TH1D("DATA_CUT_moller_Theta", ";Theta (rad)", 200, 0.0, 0.08);
  TH1D *DATA_TRACK_ESum = new TH1D("DATA_TRACK_ESum","Track Energy Sum;Energy (GeV)", 200, 0,3);
  TH1D *DATA_CLUSTER_ESum = new TH1D("DATA_CLUSTER_ESum","V0 Cluster Energy Sum;Energy (GeV)", 200, 0.,3);
  TH2D *DATA_CUT_unrot_moller_thetaE = new TH2D("DATA_CUT_unrot_moller_thetaE","'Unrotated' Moller Theta vs. E;Energy (GeV);Theta (rad)",200,0.0,2,200,0.0,0.06);
  TH1D *DATA_CUT_ETTest = new TH1D("DATA_CUT_ETTest","E - Ebeam/(1+(2Ebeam/m)sin^2(theta/2);Energy (GeV)",200,-0.4,0.4);
//  TH2D *DATA_TrackEE = new TH2D("DATA_TrackEE","Track E1 vs. E2;Electron E (GeV);Positron E (GeV)",200,0.0,1.056,200,0.0,1.056);
  TH2D *DATA_TrackEE = new TH2D("DATA_TrackEE","Track E1 vs. E2;E1 (GeV);E2 (GeV)",200,0.0,2.5,200,0.0,2);
  TH2D *DATA_CUT_MollerTT = new TH2D("DATA_CUT_MollerTT","Theta1 vs. Theta2;Theta (rad);Theta (rad)",200,0.0,0.06,200,0.0,0.06);
  TH1D *DATA_CUT_SinSinTest = new TH1D("DATA_CUT_SinSinTest","Prox. to Model (m/2Ebeam);Sin(T1/2)Sin(T2/2)", 200, 0,0.0008);
  TH2D *DATA_EP = new TH2D("DATA_EP","Moller Track E vs. Cluster E;Energy (GeV);Momentum (GeV/c)",200,0.0,1.056,200,0.0,1.056);
  TH1D *DATA_Mass = new TH1D("DATA_Mass","V0 Candidate Mass;Mass(GeV)", 200, 0.00,0.08);
  TH1D *DATA_CUT_MollerXVTX = new TH1D("DATA_CUT_MollerXVTX","XVtx;XVtx (mm)",200,-0.5,0.5);
  TH1D *DATA_CUT_MollerYVTX = new TH1D("DATA_CUT_MollerYVTX","YVtx;YVtx (mm)",200,-0.5,0.5);
  TH1D *DATA_CUT_MollerZVTX = new TH1D("DATA_CUT_MollerZVTX","ZVtx;ZVtx (mm)",200,-0.001,0.001);

  TH1D *DATA_moller_ESum = new TH1D("DATA_moller_ESum","Track Energy Sum;Energy (GeV)", 200, 0.0,3);
  TH1D *DATA_coplanarity = new TH1D("DATA_coplanarity","Coplanarity Angle;deg", 200, 0.0, 180);
  TH2D *DATA_energy_slope = new TH2D("energy_slope","Low E Cluster Distance from Photon Beam vs. Energy;Energy (GeV);Distance (mm)",200,0.0,1.0, 200,0.0,100);
  TH1D *DATA_seed_E = new TH1D("seed_E","Seed Energy;Energy (GeV)", 200, 0., 1);
  TH1D *DATA_TrackChi2 = new TH1D("DATA_TrackChi2 (top:yellow, bottom:red)","TrackChi2", 200, 0.,30);
  TH1D *DATA_vtxChi2 = new TH1D("DATA_vtxChi2","TC_Mollers Vtx Chi2", 200, 0.,30);

// SVT
  TH2D *DATA_L1 = new TH2D("DATA_L1","SVT_Hits_L1;mm;mm",200,-100,30, 200,-100,100);
  TH2D *DATA_L2 = new TH2D("DATA_L2","SVT_Hits_L2;mm;mm",200,-100,30, 200,-100,100);
  TH2D *DATA_L3 = new TH2D("DATA_L3","SVT_Hits_L3;mm;mm",200,-100,30, 200,-100,100);
  TH2D *DATA_L4 = new TH2D("DATA_L4","SVT_Hits_L4;mm;mm",200,-100,30, 200,-100,100);
  TH2D *DATA_L5 = new TH2D("DATA_L5","SVT_Hits_L5;mm;mm",200,-100,30, 200,-100,100);
  TH2D *DATA_L6 = new TH2D("DATA_L6","SVT_Hits_L6;mm;mm",200,-100,30, 200,-100,100);

// ECAL
  TH1D *DATA_FIDUCIAL_Moller_E = new TH1D("DATA_FIDUCIAL_Moller_E","Cluster E (Fiducial);Energy (GeV)", 200, 0., 1);
  TH1D *DATA_EDGE_Moller_E = new TH1D("DATA_EDGE_Moller_E","Cluster E (Edge);Energy (GeV)", 200, 0., 1);
  TH1D *DATA_EDGE_TRACK_E = new TH1D("DATA_EDGE_Moller_E","Cluster E (Edge);Energy (GeV)", 200, 0., 1);

  DATA_EDGE_TRACK_E->SetLineColor(kRed);

  TH2D *DATA_FIDUCIAL_Moller_EP = new TH2D("DATA_FIDUCIAL_Moller_EP","Momentum vs. E (Fiducial);Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);
  TH2D *DATA_EDGE_Moller_EP = new TH2D("DATA_EDGE_Moller_EP","Momentum vs. E (Inner Edge);Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);

  TH2D *DATA_FIDUCIAL_allEP = new TH2D("DATA_FIDUCIAL_allEP","Fiducial Momentum vs. E;Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);
  TH2D *DATA_FIDUCIAL_allECal_hits = new TH2D("DATA_FIDUCIAL_allECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);

  TH2D *DATA_ECal_hits=new TH2D("DATA_ECal_hits","ECal Seed Hits",49,-24.5,24.5, 13,-6.5,6.5);
//  TH2D *DATA_ECal_hits=new TH2D("DATA_CUT_ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *DATA_ECal_seedHits=new TH2D("DATA_CUT_ECal_seedHits","",49,-24.5,24.5, 13,-6.5,6.5);

  TH1D *DATA_CUT_EPRatio = new TH1D("DATA_CUT_EPRatio","E/P Ratio;ClusterE/TrackP", 200, 0,2);
  TH1D *DATA_FIDUCIAL_Moller_EPRatio = new TH1D("DATA_CUT_FIDUCIAL_Moller_EPRatio","E/P Ratio (Fiducial);ClusterE/TrackP", 200, 0,2);
  TH1D *DATA_EDGE_Moller_EPRatio = new TH1D("DATA_CUT_EDGE_Moller_EPRatio","E/P Ratio (Edge);ClusterE/TrackP", 200, 0,2);
 
  TH2D *DATA_FIDUCIAL_ECal_hits =new TH2D("DATA_CUT_FIDUCIAL_ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *DATA_EDGE_ECal_hits =new TH2D("DATA_CUT_EDGE_ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *DATA_ECalMollers4Calib=new TH2D("DATA_CUT_ECalMollers4Calib","Moller Pairs w/ 1 Fiducial, 1Edge Seed",49,-24.5,24.5, 13,-6.5,6.5);

  TH1D *DATA_EDGE_TRACK_Moller_E = new TH1D("EDGE_TRACK_Moller_E","Track E (Edge);Energy (GeV)", 200, 0., 1);
  TH1D *DATA_FIDUCIAL_TRACK_Moller_E = new TH1D("FIDUCIAL_TRACK_Moller_E","Track E (Fiducial);Energy (GeV)", 200, 0., 1);
  TH1D *DATA_tanLambda = new TH1D("DATA_tanLambda","Track Slope", 200, -0.5,0.5);


  int nev2 = tr2->GetEntries();
  cout<<"Entries in Tree 2: "<<nev2<<endl;
  //char outputname[200];

 long t0=0;
 long tf=0;
// int n=0;

 for(int foo = 0; foo < nev2; foo++)
    {
      // timestamps
      if(foo==0)
        {
          t0 = ev2->getEventTime();
          cout<<""<<'\n';
        }

      if(foo==nev2-50)
        {
          tf = ev2->getEventTime();
          cout<<foo<<'\n';
        }

//   cout<<nev2<<'\n';
//   cout<<foo<<'\n';

      if( foo%50000 == 0 )
  //    if(true)
        {
          cout<<"Processed "<<foo<<" events: about "<<(100.*double(foo)/double(nev2))<<" % \r\n";
        }

      // Read the current (foo-th) entry from the tree
      tr2->GetEntry(foo);
      int DATA_n_uc_mollers = ev2->getNumberOfParticles(uc_moller);
 
      int DATA_n_pos = 0;
      int DATA_n_fs_part = ev2->getNumberOfParticles(fs_part_type);
     for( int f = 0; f < DATA_n_fs_part; f++)
       {
          bool pos_exists = false;
          if(ev2->getParticle(fs_part_type, f)->getCharge()>0)
          {
             DATA_n_pos+=1;
             pos_exists = true;
          }

            fs_part = ev2->getParticle(fs_part_type, f);
            TRefArray *svt_tracks = fs_part->getTracks();
            int n_fs_tracks = svt_tracks->GetEntries();
            if(n_fs_tracks>0)
            {
              if(n_fs_tracks==2 )
             // if(true)
              {
               // vector<double> fsMom1 = ev2->getTrack(0)->getMomentum(); double fspx1 = fsMom1[0]; double fspy1 = fsMom1[1]; double fspz1 = fsMom1[2];
               // double fsP1 = sqrt( fspx1*fspx1 + fspy1*fspy1 + fspz1*fspz1 );

               // vector<double> fsMom2 = ev2->getTrack(1)->getMomentum(); double fspx2 = fsMom2[0]; double fspy2 = fsMom2[1]; double fspz2 = fsMom2[2];
               // double fsP2 = sqrt( fspx2*fspx2 + fspy2*fspy2 + fspz2*fspz2 );

              //   DATA_fs_ESum->Fill(fsP1+fsP2);
               // fs_elE->Fill(ev1->getTrack(0)->getMomentum());
               // fs_posE->Fill(ev1->getTrack(1)->getMomentum());
              }


             // for( int t = 0; t < n_fs_Tracks; t++ )
             //    {



             //    }


            }
       
       }


      int n_eventTracks = ev2->getNumberOfTracks(); 
     for( int t = 0; t < n_eventTracks; t++ )
        {
          if(n_eventTracks>2 && ev2->getTrack(0)->getCharge()*ev2->getTrack(1)->getCharge()*ev2->getTrack(2)->getCharge()>0 && ev2->getTrack(0)->getTanLambda()*ev2->getTrack(1)->getTanLambda()*ev2->getTrack(2)->getTanLambda()<0)
          //if(n_eventTracks==2)
          {
             vector<double> evMom1 = ev2->getTrack(0)->getMomentum(); double evpx1 = evMom1[0]; double evpy1 = evMom1[1]; double evpz1 = evMom1[2];
             double evP1 = sqrt( evpx1*evpx1 + evpy1*evpy1 + evpz1*evpz1 );

              vector<double> evMom2 = ev2->getTrack(1)->getMomentum(); double evpx2 = evMom2[0]; double evpy2 = evMom2[1]; double evpz2 = evMom2[2];
              double evP2 = sqrt( evpx2*evpx2 + evpy2*evpy2 + evpz2*evpz2 );
             
              vector<double> evMom3 = ev2->getTrack(2)->getMomentum(); double evpx3 = evMom3[0]; double evpy3 = evMom3[1]; double evpz3 = evMom3[2];
              double evP3 = sqrt( evpx3*evpx3 + evpy3*evpy3 + evpz3*evpz3 );


              DATA_fs_ESum->SetLineColor(kRed);
              DATA_fs_ESum->Fill(evP1+evP2+evP3);
          }

           vector<double> eventMom = ev2->getTrack(t)->getMomentum(); double evpx = eventMom[0]; double evpy = eventMom[1]; double evpz = eventMom[2];
           double eventP = sqrt( evpx*evpx + evpy*evpy + evpz*evpz );
             if(true)
             {
              DATA_eventsTrackE->SetLineColor(kRed);
              DATA_eventsTrackE->Fill(eventP);
             }
        }



 
      for( int jj = 0; jj < DATA_n_uc_mollers; jj++ )
        {
          DATA_Moller = ev2->getParticle(uc_moller, jj); // get the jj-th particle from the UC_VTX_PARTICLES collection
          // Vertex
          vector<double> DATA_vtx_moller = DATA_Moller->getVertexPosition();
          double DATA_mollerMass = DATA_Moller->getMass();
          TRefArray *DATA_mollers = DATA_Moller->getParticles();
          int DATA_n_mollers = DATA_mollers->GetEntries();
          DATA_moller1 = (HpsParticle*)DATA_mollers->At(0);
          DATA_moller2 = (HpsParticle*)DATA_mollers->At(1);

          TRefArray *DATA_moller_clusters1 = DATA_moller1->getClusters();   // Get ECcal clusters assoicated with that particle
          TRefArray *DATA_moller_clusters2 = DATA_moller2->getClusters();
          int DATA_n_moller_clust1 = DATA_moller_clusters1->GetEntries();           // NUmber of clusters (Should always be 0 or 1)
          int DATA_n_moller_clust2 = DATA_moller_clusters2->GetEntries();

          TRefArray *DATA_moller_tracks1 = DATA_moller1->getTracks();      // Get SVT tracks associated with this particle
          TRefArray *DATA_moller_tracks2 = DATA_moller2->getTracks();
          int DATA_n_moller_tracks1 = DATA_moller_tracks1->GetEntries();           // Should always be (0 or 1)
          int DATA_n_moller_tracks2 = DATA_moller_tracks2->GetEntries();


//          TRefArray *DATA_SVT_hits1 = DATA_moller_track1->getSvtHits();
//          TRefArray *DATA_SVT_hits2 = DATA_moller_track2->getSvtHits();

 
     // Only select data events with a certain trigger (MC doesn't have this variable, one trigger is simulated in readout)
    //   if(!ev2->isPair0Trigger() && ev2->isPair1Trigger() && !ev2->isPulserTrigger() && !ev2->isSingle1Trigger() && !ev2->isSingle0Trigger())
     if(ev2->isSingle0Trigger())
    //   if(ev2->isPair0Trigger())
//     if(true)
        {
	if( DATA_n_moller_clust1>0 && DATA_n_moller_tracks1>0 && DATA_n_moller_clust2>0 && DATA_n_moller_tracks2>0) // Both Mollers have at least 1 cluster and 1 track
            {

	// FIRST MOLLER
	  DATA_moller_clust1 = (EcalCluster*)DATA_moller_clusters1->At(0);
          DATA_moller_track1 = (SvtTrack*)DATA_moller_tracks1->At(0);
          int DATA_tracktype1 = DATA_moller_track1->getType();

          double DATA_tanLambda1 = DATA_moller_track1->getTanLambda();

          vector<double> DATA_mom1 = DATA_moller1->getMomentum(); double DATA_px1 = DATA_mom1[0]; double DATA_py1 = DATA_mom1[1]; double DATA_pz1 = DATA_mom1[2];
          double DATA_P1 = sqrt( DATA_px1*DATA_px1 + DATA_py1*DATA_py1 + DATA_pz1*DATA_pz1 );
          double DATA_E1 = DATA_moller_clust1->getEnergy();
          double DATA_TrackE1 = sqrt(DATA_P1*DATA_P1 + 0.0005109989*0.0005109989);
          double DATA_theta1 = atan2(sqrt(DATA_px1*DATA_px1 + DATA_py1*DATA_py1),DATA_pz1);
          double DATA_time1 = DATA_moller_clust1->getSeed()->getTime();
          // 'Unrotate' momentum1
          double DATA_unrot_px1 = DATA_px1*cos(-0.0305) + DATA_pz1*sin(-0.0305);
          double DATA_unrot_pz1 = DATA_pz1*cos(-0.0305) - DATA_px1*sin(-0.0305);
          double DATA_unrot_theta1 = atan2(sqrt(DATA_unrot_px1*DATA_unrot_px1 + DATA_py1*DATA_py1),DATA_unrot_pz1);
          // Find Model energy
          double DATA_denom1 = 1+2*sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta1/2)*(2300/0.5109989);
          double DATA_model1 = 2.3/DATA_denom1;

          double DATA_phi01 = 90 + atan(DATA_py1/DATA_unrot_px1)*180.0 / TMath::Pi();
           double DATA_d01 = moller_track1->getD0();

        // SECOND MOLLER
          DATA_moller_clust2 = (EcalCluster*)DATA_moller_clusters2->At(0);
          DATA_moller_track2 = (SvtTrack*)DATA_moller_tracks2->At(0);
          int DATA_tracktype2 = DATA_moller_track2->getType();

           double DATA_tanLambda2 = DATA_moller_track2->getTanLambda();

          vector<double>  DATA_mom2 = DATA_moller2->getMomentum(); double DATA_px2 = DATA_mom2[0]; double DATA_py2 = DATA_mom2[1]; double DATA_pz2 = DATA_mom2[2];
           double DATA_P2 = sqrt( DATA_px2*DATA_px2 + DATA_py2*DATA_py2 + DATA_pz2*DATA_pz2 );
           double DATA_E2 = DATA_moller_clust2->getEnergy();
           double DATA_TrackE2 = sqrt(DATA_P2*DATA_P2 + 0.0005109989*0.0005109989);
           double DATA_theta2 = atan2(sqrt(DATA_px2*DATA_px2 + DATA_py2*DATA_py2),DATA_pz2);
           double DATA_time2 = DATA_moller_clust2->getSeed()->getTime();
           // 'Unrotate' momentum2
           double DATA_unrot_px2 = DATA_px2*cos(-0.0305) + DATA_pz2*sin(-0.0305);
           double DATA_unrot_pz2 = DATA_pz2*cos(-0.0305) - DATA_px2*sin(-0.0305);
           double DATA_unrot_theta2 = atan2(sqrt(DATA_unrot_px2*DATA_unrot_px2 + DATA_py2*DATA_py2),DATA_unrot_pz2);
           // Find Model energy2
           double DATA_denom2 = 1+2*sin(DATA_unrot_theta2/2)*sin(DATA_unrot_theta2/2)*(2300/0.5109989);
           double DATA_model2 = 2.3/DATA_denom2;

            double DATA_phi02 = 90 + atan(DATA_py2/DATA_unrot_px2)*180.0 / TMath::Pi();
             double DATA_d02 = moller_track2->getD0();

            DATA_moller_ESum->Fill(DATA_TrackE1+DATA_TrackE2);

            vector<double> DATA_position1 = DATA_moller_clust1->getPosition();
            vector<double> DATA_position2 = DATA_moller_clust2->getPosition();
            vector<double> DATA_trackAtEcal1 = DATA_moller_track1->getPositionAtEcal();
               vector<double> DATA_trackAtEcal2 = DATA_moller_track2->getPositionAtEcal();   


               double DATA_clusterAngle1 = atan(DATA_position1[0]/DATA_position1[1]) * 180.0 / TMath::Pi();
               double DATA_clusterAngle2 = atan(DATA_position2[0]/DATA_position2[1]) * 180.0 / TMath::Pi();

          DATA_massSingles1->SetLineColor(kRed);
          DATA_massSingles1->Fill(DATA_mollerMass);

// ChiSq Cuts
       //  if(DATA_tracktype1 > 32 && DATA_tracktype2 > 32 && DATA_Moller->getVertexFitChi2()<=10 && DATA_moller_track1->getChi2()<=15 && DATA_moller_track2->getChi2()<=15)
        if(DATA_tracktype1 > 32 && DATA_tracktype2 > 32) // GBL only
    //   if(true)
        {
         DATA_massGBL->SetLineColor(kRed);
         DATA_massGBL->Fill(DATA_mollerMass);
	  // Theta1-Theta2 (Elastic Model + "Triangle Cut")
	 // if((sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)<=0.00040 && sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)>=0.00016 && DATA_unrot_theta1+DATA_unrot_theta2<=0.0725 && DATA_unrot_theta1+DATA_unrot_theta2>=0.055) )
	//  if(sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)>=0.00016 && sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)<=0.00045 && DATA_unrot_theta1+DATA_unrot_theta2<=0.09)
//          if(abs(DATA_time1-DATA_time2)<=1.7 && DATA_unrot_theta1+DATA_unrot_theta2<=0.050)
        if(abs(DATA_time1-DATA_time2)< 1.7)
      //   if(true)
          {
            DATA_mass1->SetLineColor(kRed);
            DATA_mass1->Fill(DATA_mollerMass);
         //   DATA_ESumE->Fill(DATA_E1,DATA_E1+DATA_E2);

	  // Energy1-Energy2
         //  if( DATA_TrackE1+DATA_TrackE2>=0.8 && DATA_TrackE1+DATA_TrackE2<=1.3 && DATA_TrackE1<=0.9 && DATA_TrackE2<=0.9 && DATA_E1<=0.9 && DATA_E2<=0.9 && abs(DATA_clusterAngle1-DATA_clusterAngle2)>=80 && abs(DATA_clusterAngle1-DATA_clusterAngle2)<=150)
          // if((DATA_phi01 - DATA_phi02) > -70 && (DATA_phi01 - DATA_phi02) < 70 && DATA_TrackE1+DATA_TrackE2>=0.9 && DATA_TrackE1+DATA_TrackE2<=1.2 && DATA_E1+DATA_E2>=0.9 && DATA_E1+DATA_E2<=1.2 && DATA_TrackE1<=0.85 && DATA_TrackE2<=0.85 && DATA_E1<=0.85 && DATA_E2<=0.85)
	//  if(DATA_TrackE1<=1.8 && DATA_TrackE2<=1.8)
          if(DATA_TrackE1<1.6 && DATA_TrackE2<1.6)
       //   if(true)
            {
             DATA_mass2->SetLineColor(kRed);
            DATA_mass2->Fill(DATA_mollerMass);
	  // Energy-Theta
	//  if((abs(DATA_TrackE1-DATA_model1)<=0.2 && abs(DATA_TrackE2-DATA_model2)<= 0.2))
	  if(DATA_TrackE1+DATA_TrackE2<=2.6 && DATA_TrackE1+DATA_TrackE2>=2)
       // if(true)
//	  if(DATA_TrackE1+DATA_TrackE2<=2.6 && DATA_TrackE1+DATA_TrackE2>=1.75 && DATA_trackAtEcal1[2] > 1200 && DATA_trackAtEcal2[2] > 1200)
            {
              DATA_mass3->SetLineColor(kRed);
            DATA_mass3->Fill(DATA_mollerMass);
	  // Secondary Cuts
	 // if((abs(DATA_time1-DATA_time2)<=1.5 && DATA_TrackE1>=0.3 && DATA_TrackE1<=0.75 && DATA_TrackE2>=0.3 && DATA_TrackE2<=0.75 && DATA_unrot_theta1>=0.02 && DATA_unrot_theta1<=0.045 && DATA_unrot_theta2>=0.02 && DATA_unrot_theta2<=0.045) )
	 //  if((abs(DATA_time1-DATA_time2)<=3) && DATA_E1>=0.5 && DATA_E1<=2 && DATA_E2>=0.5 && DATA_E2<=2 )
          //   if(DATA_unrot_theta1<=0.06 && DATA_unrot_theta2<=0.06)
         //  if(DATA_TrackE1<=1.7 && DATA_TrackE2<=1.7)
         //  if(abs(DATA_time1-DATA_time2)<=1.7)
	 //if(abs(DATA_time1-DATA_time2)<=1.7 && DATA_unrot_theta1>=0.015 && DATA_unrot_theta2>=0.015 && DATA_unrot_theta1+DATA_unrot_theta2 >=0.045 && DATA_unrot_theta1+DATA_unrot_theta2 <=0.085)
        //  if(DATA_unrot_theta1+DATA_unrot_theta2>=0.050 && DATA_unrot_theta1+DATA_unrot_theta2<=0.080)
         if(true)
         // if(true)
// Momar Cuts //  if(DATA_TrackE1>=0.05 && DATA_TrackE2>=0.05 && DATA_TrackE1<=0.85 && DATA_TrackE2<=0.85 && abs(DATA_time1-DATA_time2)<=1.6 && DATA_tanLambda1*DATA_tanLambda2 < 0)
            {
	    //CUT_moller_thetaE->Fill(TrackE1,theta1); CUT_moller_thetaE->Fill(TrackE2,theta2);
          
          //  if((DATA_position1[0] - DATA_trackAtEcal1[0]) <= 15 && (DATA_position1[0] - DATA_trackAtEcal1[0]) >= -15 && (DATA_position1[1] - DATA_trackAtEcal1[1])<= 20 && (DATA_position1[1] - DATA_trackAtEcal1[1])>= -20 && (DATA_position2[0] - DATA_trackAtEcal2[0]) <= 15 && (DATA_position2[0] - DATA_trackAtEcal2[0]) >= -15 && (DATA_position2[1] - DATA_trackAtEcal2[1])<= 20 && (DATA_position2[1] - DATA_trackAtEcal2[1])>= -20)
     //   if((DATA_position1[1] - DATA_trackAtEcal1[1])<= 10 && (DATA_position1[1] - DATA_trackAtEcal1[1])>= -10 && (DATA_position2[1] - DATA_trackAtEcal2[1])<= 10 && (DATA_position2[1] - DATA_trackAtEcal2[1])>= -10)
           if(true)
               {

            DATA_CUT_MollerTT->Fill(DATA_unrot_theta1,DATA_unrot_theta2);
	    DATA_CUT_unrot_moller_thetaE->Fill(DATA_TrackE1,DATA_unrot_theta1); DATA_CUT_unrot_moller_thetaE->Fill(DATA_TrackE2,DATA_unrot_theta2);
	    DATA_CUT_moller_E->SetLineColor(kRed);
            //DATA_CUT_moller_E->Scale(norm);
     
            DATA_TrackE->SetLineColor(kRed);
            DATA_TrackE->Fill(DATA_TrackE1); DATA_TrackE->Fill(DATA_TrackE2);
            DATA_ClusterE->SetLineColor(kRed);
            DATA_ClusterE->Fill(DATA_E1); DATA_ClusterE->Fill(DATA_E2);

            DATA_ClusterE1->SetLineColor(kRed); DATA_ClusterE2->SetLineColor(kRed);
            DATA_ClusterE1->Fill(DATA_E1);
            DATA_ClusterE2->Fill(DATA_E2);

            DATA_ClusterEE->Fill(DATA_E1,DATA_E2);
            DATA_TrackEE->Fill(DATA_TrackE1,DATA_TrackE2);

            DATA_ECal_seedHits->Fill(DATA_moller_clust1->getSeed()->getXCrystalIndex(),DATA_moller_clust1->getSeed()->getYCrystalIndex());
            DATA_ECal_seedHits->Fill(DATA_moller_clust2->getSeed()->getXCrystalIndex(),DATA_moller_clust2->getSeed()->getYCrystalIndex());

//            if(DATA_moller1->getCharge() > 0 && DATA_moller2->getCharge() < 0)
//               {
//                 DATA_TrackEE->Fill(DATA_TrackE1,DATA_TrackE2);
//                 DATA_ClusterEE->Fill(DATA_E1,DATA_E2);
//                } else if (DATA_moller1->getCharge() < 0 && DATA_moller2->getCharge() > 0)
//                {
//                  DATA_TrackEE->Fill(DATA_TrackE2,DATA_TrackE1);
//                  DATA_ClusterEE->Fill(DATA_E2,DATA_E1);
//                }


               if(DATA_E1 < DATA_E2)
               {
               double DATA_lowEClusterDistance = TMath::Hypot(DATA_moller_clust1->getSeed()->getXCrystalIndex() - 1393.0 * TMath::Tan(0.03052), DATA_moller_clust1->getSeed()->getYCrystalIndex());
               DATA_energy_slope->Fill(DATA_E1,DATA_lowEClusterDistance);
               }

               if(DATA_E1 > DATA_E2)
               {
               double DATA_lowEClusterDistance = TMath::Hypot(DATA_moller_clust2->getSeed()->getXCrystalIndex() - 1393.0 * TMath::Tan(0.03052), DATA_moller_clust2->getSeed()->getYCrystalIndex());
               DATA_energy_slope->Fill(DATA_E2,DATA_lowEClusterDistance);
               }

               DATA_seed_E->Fill(DATA_moller_clust1->getSeed()->getEnergy());
               DATA_seed_E->Fill(DATA_moller_clust2->getSeed()->getEnergy());


             DATA_ESumMass->Fill(DATA_mollerMass,DATA_E1+DATA_E2);


            DATA_px->SetLineColor(kRed);
            DATA_py->SetLineColor(kRed);
            DATA_pz->SetLineColor(kRed);
            DATA_px->Fill(DATA_px1); DATA_px->Fill(DATA_px2);
            DATA_py->Fill(DATA_py1); DATA_py->Fill(DATA_py2);
            DATA_pz->Fill(DATA_pz1); DATA_pz->Fill(DATA_pz2);

            DATA_tanLambda->SetLineColor(kRed);
            DATA_tanLambda->Fill(DATA_tanLambda1); DATA_tanLambda->Fill(DATA_tanLambda2);

	    DATA_CUT_moller_Theta->SetLineColor(kRed);
	    DATA_CUT_moller_Theta->Fill(DATA_unrot_theta1); DATA_CUT_moller_Theta->Fill(DATA_unrot_theta2);
	    DATA_TRACK_ESum->SetLineColor(kRed);
	    DATA_TRACK_ESum->Fill(DATA_TrackE1+DATA_TrackE2);
            DATA_CLUSTER_ESum->SetLineColor(kRed);
            DATA_CLUSTER_ESum->Fill(DATA_E1+DATA_E2);
            DATA_CUT_ETTest->SetLineColor(kRed);
	    DATA_CUT_ETTest->Fill(DATA_model1-DATA_TrackE1); DATA_CUT_ETTest->Fill(DATA_model2-DATA_TrackE2);
            DATA_CUT_SinSinTest->SetLineColor(kRed);
	    DATA_CUT_SinSinTest->Fill(sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2));
            DATA_CUT_V0_coincidence->SetLineColor(kRed);
            DATA_CUT_V0_coincidence->Fill(DATA_time1-DATA_time2);
            DATA_hitTime->Fill(DATA_time1); DATA_hitTime->Fill(DATA_time2);
	    //CUT_moller_EP->Fill(E1,TrackE1); CUT_moller_EP->Fill(E2,TrackE2);
	   DATA_CUT_MollerXVTX->SetLineColor(kRed);
	   DATA_CUT_MollerXVTX->Fill(DATA_vtx_moller[0]);
           DATA_CUT_MollerYVTX->SetLineColor(kRed);
	   DATA_CUT_MollerYVTX->Fill(DATA_vtx_moller[1]);
           DATA_CUT_MollerZVTX->SetLineColor(kRed);
	   DATA_CUT_MollerZVTX->Fill(DATA_vtx_moller[2]);


           DATA_hitxDiff->SetLineColor(kRed); DATA_hityDiff->SetLineColor(kRed);
           DATA_hitxDiff->Fill(DATA_position1[0] - DATA_trackAtEcal1[0]); DATA_hitxDiff->Fill(DATA_position2[0] - DATA_trackAtEcal2[0]);
           DATA_hityDiff->Fill(DATA_position1[1] - DATA_trackAtEcal1[1]); DATA_hityDiff->Fill(DATA_position2[1] - DATA_trackAtEcal2[1]);

          // DATA_tracksAtEcal->SetLineColor(kRed);
           DATA_tracksAtEcal->Fill(DATA_trackAtEcal1[0],DATA_trackAtEcal1[1]);
           DATA_tracksAtEcal->Fill(DATA_trackAtEcal2[0],DATA_trackAtEcal2[1]);

           DATA_EP->Fill(DATA_E1,DATA_TrackE1); DATA_EP->Fill(DATA_E2,DATA_TrackE2);
           DATA_ESumE->Fill(DATA_E1,DATA_E1+DATA_E2);


          //  DATA_CUT_MollerMass->Scale(100);
	    DATA_Mass->SetLineColor(kRed);
	    DATA_Mass->Fill(DATA_mollerMass);
	  
          // CUT_vtxChi2->Fill(Moller->getVertexFitChi2());
          // CUT_trackChi2->Fill(moller_track1->getChi2()); 
          // CUT_trackChi2->Fill(moller_track2->getChi2());

              DATA_coplanarity->SetLineColor(kRed);
              DATA_coplanarity->Fill(abs(DATA_clusterAngle1-DATA_clusterAngle2));

              DATA_phiDiff->SetLineColor(kRed);
              DATA_phiDiff->Fill(DATA_phi01 - DATA_phi02);

               DATA_TrackChi2->SetLineColor(kYellow);
               DATA_TrackChi2->Fill(DATA_moller_track1->getChi2());
               DATA_TrackChi2->SetLineColor(kRed);
               DATA_TrackChi2->Fill(DATA_moller_track2->getChi2());

               DATA_vtxChi2->SetLineColor(kRed);
               DATA_vtxChi2->Fill(DATA_Moller->getVertexFitChi2());


 // SVT WORLD
//          for(int hit_n=0; hit_n<DATA_SVT_hits1->GetEntries(); ++hit_n)
//              {
//                DATA_svt_hit1 = (SvtHit*) DATA_SVT_hits1->At(hit_n);
//                vector<double> DATA_svt_hit_position1 = DATA_svt_hit1->getPosition();
//                int DATA_layer = DATA_svt_hit1->getLayer();

//                switch(DATA_layer){
//                case 1:
//                   DATA_L1->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 2:
//                   DATA_L2->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 3:
//                   DATA_L3->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 4:
//                   DATA_L4->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 5:
//                   DATA_L5->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);

//                   break;
//                case 6:
//                    DATA_L6->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                    break;  
//                 }
//               }// SVT WORLD1

//           for(int hit_n=0; hit_n<DATA_SVT_hits2->GetEntries(); ++hit_n)
//              {
//                DATA_svt_hit2 = (SvtHit*) DATA_SVT_hits2->At(hit_n);
//                vector<double> DATA_svt_hit_position2 = DATA_svt_hit2->getPosition();
//                   int DATA_layer = DATA_svt_hit2->getLayer();

//                switch(DATA_layer){
//                case 1:
//                   DATA_L1->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 2:
//                   DATA_L2->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 3:
//                   DATA_L3->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 4:
//                   DATA_L4->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 5:
//                   DATA_L5->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);

//                   break;
//                case 6:
//                    DATA_L6->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                    break;
//                 }
//               }// SVT WORLD2

// ECAL WORLD

           TRefArray *DATA_CUT_ec_hits1 = DATA_moller_clust1->getEcalHits();
           int index_x1=0, index_y1=0;
           Fiducial1 = false, Fiducial2 = false, Edge1 = false, Edge2 = false;

           for(int hit_n=0; hit_n<DATA_CUT_ec_hits1->GetEntries(); ++hit_n)
                  {
                     ec_hit1 = (EcalHit*) DATA_CUT_ec_hits1->At(hit_n);
                     index_x1 = ec_hit1->getXCrystalIndex();
                     index_y1 = ec_hit1->getYCrystalIndex();

                  //   DATA_EPRatio->Fill(DATA_E1/DATA_P1);

                     // Explore the 0.5 GeV discontinuity
                     	if(DATA_E1>0.5)
                     	{
                     	DATA_pos_hits->Fill(index_x1,index_y1,1);
                        DATA_highET->SetLineColor(kRed);
                        DATA_highET->Fill(DATA_model1-DATA_TrackE1);
                     	}
                     	if(DATA_E1<0.5)
                     	{
                     	DATA_neg_hits->Fill(index_x1,index_y1,1);
                        DATA_lowET->SetLineColor(kRed);
                        DATA_lowET->Fill(DATA_model1-DATA_TrackE1);
                     	}

                     // Edge 1
                     if(((index_x1<=-2 && index_x1>=-10)&&(index_y1==2||index_y1==-2)) || (index_y1==1||index_y1==-1))
                     //if((index_x1<=-8 && index_x1>=-10)&&(index_y1==2||index_y1==-2) || ((index_x1<=-10 && index_x1>=-12)&&(index_y1==1||index_y1==-1)))
                     {
                     	DATA_ECal_hits->Fill(index_x1,index_y1,1);
                     	DATA_EDGE_ECal_hits->Fill(index_x1,index_y1,1);
                     	DATA_EDGE_Moller_EPRatio->Fill(DATA_E1/DATA_P1);
                     	DATA_EDGE_Moller_EP->Fill(DATA_E1,DATA_P1);

                        DATA_EDGE_Moller_E->SetLineColor(kRed);
                     	DATA_EDGE_Moller_E->Fill(DATA_E1);
                        DATA_EDGE_TRACK_Moller_E->SetLineColor(kRed);
                     	DATA_EDGE_TRACK_E->Fill(DATA_TrackE1);

                     	if(DATA_moller_clust1->getSeed()->getXCrystalIndex()==index_x1 && DATA_moller_clust1->getSeed()->getYCrystalIndex()==index_y1)
                     	{                     
                       	Edge1 = true;
                     	}
                    
                     } // EDGE1

                     // Fiducial Elastic Cut, Moller1
                     if(index_y1!=1 && index_y1!=-1)
                     {
                     if( !((index_y1==2||index_y1==-2)&&(index_x1>=-10 && index_x1<=-2)))
                     {
                        DATA_ECal_hits->Fill(index_x1,index_y1,1);
                        DATA_FIDUCIAL_ECal_hits->Fill(index_x1,index_y1,1);                     
                        DATA_FIDUCIAL_Moller_EPRatio->Fill(DATA_E1/DATA_P1);
                        DATA_FIDUCIAL_Moller_EP->Fill(DATA_E1,DATA_P1);

                        DATA_FIDUCIAL_Moller_E->SetLineColor(kRed);
                        DATA_FIDUCIAL_Moller_E->Fill(DATA_E1);
                        DATA_FIDUCIAL_TRACK_Moller_E->SetLineColor(kRed);
                        DATA_FIDUCIAL_TRACK_Moller_E->Fill(DATA_TrackE1);

                        if(DATA_moller_clust1->getSeed()->getXCrystalIndex()==index_x1 && DATA_moller_clust1->getSeed()->getYCrystalIndex()==index_y1)
                         {                                                                                                                                                                                                                                          Fiducial1 = true;
                         }
                       }
                     }//FIDUCIAL 1
                    }// CLUSTER1


                  // CLUSTER 2

                  TRefArray *DATA_CUT_ec_hits2 = DATA_moller_clust2->getEcalHits();
                  int index_x2=0, index_y2=0;
                  Fiducial1 = false, Fiducial2 = false, Edge1 = false, Edge2 = false;

                  for(int hit_n=0; hit_n<DATA_CUT_ec_hits2->GetEntries(); ++hit_n)
                  {
                     ec_hit2 = (EcalHit*) DATA_CUT_ec_hits2->At(hit_n);
                     index_x2 = ec_hit2->getXCrystalIndex();
                     index_y2 = ec_hit2->getYCrystalIndex();

                    // DATA_CUT_EPRatio->Fill(DATA_E2/DATA_P2);

                     if(DATA_E2<0.5)
                        {
                        DATA_neg_hits->Fill(index_x2,index_y2,1);
                        DATA_lowET->SetLineColor(kRed);
                        DATA_lowET->Fill(DATA_model2-DATA_TrackE2);
                        }
                        if(DATA_E2>0.5)
                        {
                        DATA_pos_hits->Fill(index_x2,index_y2,1);
                        DATA_highET->SetLineColor(kRed);
                        DATA_highET->Fill(DATA_model2-DATA_TrackE2);
                        }


                   // EDGE 2
                     if(((index_x2<=-2 && index_x2>=-10)&&(index_y2==2||index_y2==-2)) || (index_y2==1||index_y2==-1))
                   //if((index_x2<=-8 && index_x2>=-10)&&(index_y2==2||index_y2==-2) || ((index_x1<=-10 && index_x1>=-12)&&(index_y2==1||index_y2==-1)))
                     {
                     DATA_ECal_hits->Fill(index_x2,index_y2,1);
                     DATA_EDGE_ECal_hits->Fill(index_x2,index_y2,1);
                     DATA_EDGE_Moller_EPRatio->Fill(DATA_E2/DATA_P2);
                     DATA_EDGE_Moller_EP->Fill(DATA_E2,DATA_P2);

                     DATA_EDGE_Moller_E->SetLineColor(kRed);
                     DATA_EDGE_Moller_E->Fill(DATA_E2);
                     DATA_EDGE_TRACK_E->SetLineColor(kRed);
                     DATA_EDGE_TRACK_Moller_E->Fill(DATA_TrackE2);

                     if(DATA_moller_clust2->getSeed()->getXCrystalIndex()==index_x2 && DATA_moller_clust2->getSeed()->getYCrystalIndex()==index_y2)
                     {
                       Edge2 = true;
                     }
                    } // EDGE 2

                   // FIDUCIAL 2
                   if(index_y2!=1 && index_y2!=-1)
                     {
                     if( !((index_y2==2||index_y2==-2)&&(index_x2>=-10 && index_x2<=-2)))
                     {
                        DATA_ECal_hits->Fill(index_x2,index_y2,1);
                        DATA_FIDUCIAL_ECal_hits->Fill(index_x2,index_y2,1);
                        DATA_FIDUCIAL_Moller_EPRatio->Fill(DATA_E2/DATA_P2);
                        DATA_FIDUCIAL_Moller_EP->Fill(DATA_E2,DATA_P2);

                        DATA_FIDUCIAL_Moller_E->SetLineColor(kRed);
                        DATA_FIDUCIAL_Moller_E->Fill(DATA_E2);
                        DATA_FIDUCIAL_TRACK_Moller_E->SetLineColor(kRed);
                        DATA_FIDUCIAL_TRACK_Moller_E->Fill(DATA_TrackE2);

                        if(DATA_moller_clust2->getSeed()->getXCrystalIndex()==index_x2 && DATA_moller_clust2->getSeed()->getYCrystalIndex()==index_y2)
                         {                                                                                                                                                                                                                                          Fiducial2 = true;
                         }
                       }
                    } // FIDUCIAL 2

                  } // CLUSTER 2



             }// Matching
             }//
             }//
             }//
             }//
 
            } // GBL Tracks

         } // n_moller_clust == 1 && n_moller_tracks == 1

       } // trigger select

     } // loop over Mollers

   } // loop over events

/////////////////////////////////////////////////////////////////////////////////////// END TREE 2: DATA ////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////// TREE 3: PURE MC ///////////////////////////////////////////////////////////////////////////////////
////////////// Third time's the charm~! ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




// Normalize PURE events
//const double num_PURE_files = 98*10; // # of generated Pure Moller MC files used (singles1)
const double num_PURE_files = 100*10; // # of generated Pure Moller MC files used (singles0)
double PURE_Lumin = 74*(2e6)*(2500)*(4.062e-4)*(6.306e-2)*num_PURE_files; // Total luminosity for pure Mollers (2M bunches) (1/barns)




TChain *tr3 = new TChain("HPS_Event", "HPS_Event");

//tr3->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/moller/1pt05/molv3_5mrad_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.10-20160813_singles1_*.root");
//tr3->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/moller/1pt05/molv3_5mrad_HPS-EngRun2015-Nominal-v5-0-fieldmap_3.11-20161202_singles0_*.root");
//tr3->Add("/cache/mss/hallb/hps/production/postTriSummitFixes/dst/moller/2pt3/3.11-20170331/molv3_5mrad_10to1_HPS-PhysicsRun2016-Nominal-v5-0-fieldmap_3.11-20170331_run7984_singles0_*.root");
tr3->Add("");

  HpsEvent *ev3 = new HpsEvent(); 
  tr3->SetBranchAddress("Event", &ev3);

  HpsParticle *PURE_fs_part, *PURE_uc_part, *PURE_fs_part_upper, *PURE_dau_particles, *PURE_dau_part1, *PURE_dau_part2, *PURE_Moller,*PURE_moller1, *PURE_moller2;
  EcalCluster *PURE_ec_clust, *PURE_ec_clust_upper, *PURE_dau_clust1, *PURE_dau_clust2, *PURE_moller_clust1, *PURE_moller_clust2;
  EcalHit *PURE_ec_hit, *PURE_ec_hit1, *PURE_ec_hit2,*PURE_CUT_ec_hit1, *PURE_CUT_ec_hit2;
  SvtTrack *PURE_moller_track1, *PURE_moller_track2;

  TH2D *PURE_CUT_moller_thetaE = new TH2D("PURE_CUT_moller_thetaE","Moller Theta vs. E;Energy (GeV);Theta (rad)",200,0.0,2,200,0.0,0.06);
  TH1D *PURE_CUT_moller_E = new TH1D("PURE_CUT_moller_E", ";Energy (GeV)", 200, 0.,2.3);
  TH1D *PURE_ClusterE = new TH1D("PURE_ClusterE","Cluster Energy;Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_ClusterE1 = new TH1D("PURE_ClusterE1","Cluster Energy;Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_ClusterE2 = new TH1D("PURE_ClusterE2","Cluster Energy;Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_TrackE = new TH1D("PURE_TrackE","Track Energy;Energy (GeV)", 200, 0.,2.3);
//  TH2D *DATA_ClusterEE = new TH2D("DATA_ClusterEE","Cluster E1 vs. E2;Electron E (GeV);Positron E (GeV)",200,0.0,2.5,200,0.0,2.5);
  TH2D *PURE_ClusterEE = new TH2D("PURE_ClusterEE","Cluster E1 vs. E2;E1 (GeV);E2 (GeV)",200,0.0,2.3,200,0.0,2.3);
  TH1D *PURE_CUT_moller_Theta = new TH1D("PURE_CUT_moller_Theta", ";Theta (rad)", 200, 0.0, 0.06);
  TH1D *PURE_TRACK_ESum = new TH1D("PURE_TRACK_ESum","V0 Track Energy Sum;Energy (GeV)", 200, 0,3);
  TH1D *PURE_CLUSTER_ESum = new TH1D("PURE_CLUSTER_ESum","V0 Cluster Energy Sum;Energy (GeV)", 200, 0.,3);
  TH2D *PURE_CUT_unrot_moller_thetaE = new TH2D("PURE_CUT_unrot_moller_thetaE","'Unrotated' Moller Theta vs. E;Energy (GeV);Theta (rad)",200,0.0,2.3,200,0.0,0.06);
  TH1D *PURE_CUT_ETTest = new TH1D("PURE_CUT_ETTest","E - Ebeam/(1+(2Ebeam/m)sin^2(theta/2);Energy (GeV)",200,-0.4,0.4);
//  TH2D *DATA_TrackEE = new TH2D("DATA_TrackEE","Track E1 vs. E2;Electron E (GeV);Positron E (GeV)",200,0.0,1.056,200,0.0,1.056);
  TH2D *PURE_TrackEE = new TH2D("PURE_TrackEE","Track E1 vs. E2;E1 (GeV);E2 (GeV)",200,0.0,3,200,0.0,3);
  TH2D *PURE_CUT_MollerTT = new TH2D("PURE_CUT_MollerTT","Theta1 vs. Theta2;Theta (rad);Theta (rad)",200,0.0,0.06,200,0.0,0.06);
  TH1D *PURE_CUT_SinSinTest = new TH1D("PURE_CUT_SinSinTest","Prox. to Model (m/2Ebeam);Sin(T1/2)Sin(T2/2)", 200, 0,0.0008);
  TH2D *PURE_CUT_moller_EP = new TH2D("PURE_CUT_moller_EP","Moller Track E vs. Cluster E;Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.3);
  TH1D *PURE_Mass = new TH1D("PURE_Mass","V0 Candidate Mass;Mass(GeV)", 200, 0.04,0.06);
  TH1D *PURE_CUT_MollerXVTX = new TH1D("PURE_CUT_MollerXVTX","XVtx;XVtx (mm)",200,-0.5,0.5);
  TH1D *PURE_CUT_MollerYVTX = new TH1D("PURE_CUT_MollerYVTX","YVtx;YVtx (mm)",200,-0.5,0.5);
  TH1D *PURE_CUT_MollerZVTX = new TH1D("PURE_CUT_MollerZVTX","ZVtx;ZVtx (mm)",200,-0.001,0.001);

  TH1D *PURE_moller_ESum = new TH1D("PURE_moller_ESum","Track Energy Sum;Energy (GeV)", 200, 0.0, 3);
  TH1D *PURE_coplanarity = new TH1D("PURE_coplanarity","Coplanarity Angle;deg", 200, 0.0, 180);
  TH2D *PURE_energy_slope = new TH2D("energy_slope","Low E Cluster Distance from Photon Beam vs. Energy;Energy (GeV);Distance (mm)",200,0.0,1.0, 200,0.0,100);
  TH1D *PURE_seed_E = new TH1D("seed_E","Seed Energy;Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_TrackChi2 = new TH1D("PURE_TrackChi2 (top:yellow, bottom:red)","TrackChi2", 200, 0.,30);
  TH1D *PURE_vtxChi2 = new TH1D("PURE_vtxChi2","TC_Mollers Vtx Chi2", 200, 0.,30);

// SVT
//  TH2D *DATA_L1 = new TH2D("DATA_L1","SVT_Hits_L1;mm;mm",200,-100,30, 200,-100,100);
//  TH2D *DATA_L2 = new TH2D("DATA_L2","SVT_Hits_L2;mm;mm",200,-100,30, 200,-100,100);
//  TH2D *DATA_L3 = new TH2D("DATA_L3","SVT_Hits_L3;mm;mm",200,-100,30, 200,-100,100);
//  TH2D *DATA_L4 = new TH2D("DATA_L4","SVT_Hits_L4;mm;mm",200,-100,30, 200,-100,100);
//  TH2D *DATA_L5 = new TH2D("DATA_L5","SVT_Hits_L5;mm;mm",200,-100,30, 200,-100,100);
//  TH2D *DATA_L6 = new TH2D("DATA_L6","SVT_Hits_L6;mm;mm",200,-100,30, 200,-100,100);

// ECAL
  TH1D *PURE_FIDUCIAL_Moller_E = new TH1D("PURE_FIDUCIAL_Moller_E","Cluster E (Fiducial);Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_EDGE_Moller_E = new TH1D("PURE_EDGE_Moller_E","Cluster E (Edge);Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_EDGE_TRACK_E = new TH1D("PURE_EDGE_Moller_E","Cluster E (Edge);Energy (GeV)", 200, 0., 2.3);

  PURE_EDGE_TRACK_E->SetLineColor(kGreen);

  TH2D *PURE_EP = new TH2D("PURE_EP","Moller Track E vs. Cluster E;Energy (GeV);Momentum (GeV/c)",200,0.0,2.3,200,0.0,2.3);

  TH2D *PURE_FIDUCIAL_Moller_EP = new TH2D("PURE_FIDUCIAL_Moller_EP","Momentum vs. E (Fiducial);Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);
  TH2D *PURE_EDGE_Moller_EP = new TH2D("PURE_EDGE_Moller_EP","Momentum vs. E (Inner Edge);Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);

  TH2D *PURE_FIDUCIAL_allEP = new TH2D("PURE_FIDUCIAL_allEP","Fiducial Momentum vs. E;Energy (GeV);Momentum (GeV/c)",200,0.0,2.5,200,0.0,2.5);
  TH2D *PURE_FIDUCIAL_allECal_hits = new TH2D("PURE_FIDUCIAL_allECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);

  TH2D *PURE_ECal_hits=new TH2D("PURE_ECal_hits","ECal Seed Hits",49,-24.5,24.5, 13,-6.5,6.5);
//  TH2D *DATA_ECal_hits=new TH2D("DATA_CUT_ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *PURE_ECal_seedHits=new TH2D("PURE_CUT_ECal_seedHits","",49,-24.5,24.5, 13,-6.5,6.5);

  TH1D *PURE_CUT_EPRatio = new TH1D("PURE_CUT_EPRatio","E/P Ratio;ClusterE/TrackP", 200, 0,3);
  TH1D *PURE_FIDUCIAL_Moller_EPRatio = new TH1D("PURE_CUT_FIDUCIAL_Moller_EPRatio","E/P Ratio (Fiducial);ClusterE/TrackP", 200, 0,3);
  TH1D *PURE_EDGE_Moller_EPRatio = new TH1D("PURE_CUT_EDGE_Moller_EPRatio","E/P Ratio (Edge);ClusterE/TrackP", 200, 0,3);

  TH2D *PURE_FIDUCIAL_ECal_hits =new TH2D("PURE_CUT_FIDUCIAL_ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *PURE_EDGE_ECal_hits =new TH2D("PURE_CUT_EDGE_ECal_hits","",49,-24.5,24.5, 13,-6.5,6.5);
  TH2D *PURE_ECalMollers4Calib=new TH2D("PURE_CUT_ECalMollers4Calib","Moller Pairs w/ 1 Fiducial, 1Edge Seed",49,-24.5,24.5, 13,-6.5,6.5);

  TH1D *PURE_EDGE_TRACK_Moller_E = new TH1D("PURE_EDGE_TRACK_Moller_E","Track E (Edge);Energy (GeV)", 200, 0.,2.3);
  TH1D *PURE_FIDUCIAL_TRACK_Moller_E = new TH1D("PURE_FIDUCIAL_TRACK_Moller_E","Track E (Fiducial);Energy (GeV)", 200, 0., 2.3);
  TH1D *PURE_tanLambda = new TH1D("PURE_tanLambda","Track Slope", 200, -0.5,0.5);

  int nev3 = tr3->GetEntries();
  cout<<"Entries in Tree 3: "<<nev3<<endl;
  //char outputname[200];
  
  

 for(int foo = 0; foo < nev3; foo++)
    {

      if( foo%50000 == 0 )
  //    if(true)
        {
          cout<<"Processed "<<foo<<" events: about "<<(100.*double(foo)/double(nev3))<<" % \r\n";
        }

      // Read the current (foo-th) entry from the tree
      tr3->GetEntry(foo);
      int PURE_n_uc_mollers = ev3->getNumberOfParticles(uc_moller);
 
      int PURE_n_pos = 0;
      int PURE_n_fs_part = ev3->getNumberOfParticles(fs_part_type);
     for( int f = 0; f < PURE_n_fs_part; f++)
       {
          bool pos_exists = false;
          if(ev3->getParticle(fs_part_type, f)->getCharge()>0)
          {
             PURE_n_pos+=1;
             pos_exists = true;
          }

            fs_part = ev3->getParticle(fs_part_type, f);
            TRefArray *svt_tracks = fs_part->getTracks();
            int n_fs_tracks = svt_tracks->GetEntries();
            if(n_fs_tracks>0)
            {
              if(n_fs_tracks==2 )
             // if(true)
              {
               // vector<double> fsMom1 = ev2->getTrack(0)->getMomentum(); double fspx1 = fsMom1[0]; double fspy1 = fsMom1[1]; double fspz1 = fsMom1[2];
               // double fsP1 = sqrt( fspx1*fspx1 + fspy1*fspy1 + fspz1*fspz1 );

               // vector<double> fsMom2 = ev2->getTrack(1)->getMomentum(); double fspx2 = fsMom2[0]; double fspy2 = fsMom2[1]; double fspz2 = fsMom2[2];
               // double fsP2 = sqrt( fspx2*fspx2 + fspy2*fspy2 + fspz2*fspz2 );

              //   DATA_fs_ESum->Fill(fsP1+fsP2);
               // fs_elE->Fill(ev1->getTrack(0)->getMomentum());
               // fs_posE->Fill(ev1->getTrack(1)->getMomentum());
              }


             // for( int t = 0; t < n_fs_Tracks; t++ )
             //    {



             //    }


            }
       
       }


      int n_eventTracks = ev3->getNumberOfTracks(); 
     for( int t = 0; t < n_eventTracks; t++ )
        {
          if(n_eventTracks>2 && ev3->getTrack(0)->getCharge()*ev3->getTrack(1)->getCharge()*ev3->getTrack(2)->getCharge()>0 && ev3->getTrack(0)->getTanLambda()*ev3->getTrack(1)->getTanLambda()*ev3->getTrack(2)->getTanLambda()<0)
          //if(n_eventTracks==2)
          {
             vector<double> evMom1 = ev3->getTrack(0)->getMomentum(); double evpx1 = evMom1[0]; double evpy1 = evMom1[1]; double evpz1 = evMom1[2];
             double evP1 = sqrt( evpx1*evpx1 + evpy1*evpy1 + evpz1*evpz1 );

              vector<double> evMom2 = ev3->getTrack(1)->getMomentum(); double evpx2 = evMom2[0]; double evpy2 = evMom2[1]; double evpz2 = evMom2[2];
              double evP2 = sqrt( evpx2*evpx2 + evpy2*evpy2 + evpz2*evpz2 );
             
              vector<double> evMom3 = ev3->getTrack(2)->getMomentum(); double evpx3 = evMom3[0]; double evpy3 = evMom3[1]; double evpz3 = evMom3[2];
              double evP3 = sqrt( evpx3*evpx3 + evpy3*evpy3 + evpz3*evpz3 );


             // PURE_fs_ESum->SetLineColor(kRed);
             // PURE_fs_ESum->Fill(evP1+evP2+evP3);
          }

           vector<double> eventMom = ev3->getTrack(t)->getMomentum(); double evpx = eventMom[0]; double evpy = eventMom[1]; double evpz = eventMom[2];
           double eventP = sqrt( evpx*evpx + evpy*evpy + evpz*evpz );
             if(true)
             {
                PURE_eventsTrackE->SetLineColor(kRed);
                PURE_eventsTrackE->Fill(eventP);
             }
        }



 
      for( int jj = 0; jj < PURE_n_uc_mollers; jj++ )
        {
          PURE_Moller = ev3->getParticle(uc_moller, jj); // get the jj-th particle from the UC_VTX_PARTICLES collection
          // Vertex
          vector<double> PURE_vtx_moller = PURE_Moller->getVertexPosition();
          double PURE_mollerMass = PURE_Moller->getMass();
          TRefArray *PURE_mollers = PURE_Moller->getParticles();
          int PURE_n_mollers = PURE_mollers->GetEntries();
          PURE_moller1 = (HpsParticle*)PURE_mollers->At(0);
          PURE_moller2 = (HpsParticle*)PURE_mollers->At(1);

          TRefArray *PURE_moller_clusters1 = PURE_moller1->getClusters();   // Get ECcal clusters assoicated with that particle
          TRefArray *PURE_moller_clusters2 = PURE_moller2->getClusters();
          int PURE_n_moller_clust1 = PURE_moller_clusters1->GetEntries();           // NUmber of clusters (Should always be 0 or 1)
          int PURE_n_moller_clust2 = PURE_moller_clusters2->GetEntries();

          TRefArray *PURE_moller_tracks1 = PURE_moller1->getTracks();      // Get SVT tracks associated with this particle
          TRefArray *PURE_moller_tracks2 = PURE_moller2->getTracks();
          int PURE_n_moller_tracks1 = PURE_moller_tracks1->GetEntries();           // Should always be (0 or 1)
          int PURE_n_moller_tracks2 = PURE_moller_tracks2->GetEntries();


//          TRefArray *DATA_SVT_hits1 = DATA_moller_track1->getSvtHits();
//          TRefArray *DATA_SVT_hits2 = DATA_moller_track2->getSvtHits();

 
     // Only select data events with a certain trigger (MC doesn't have this variable, one trigger is simulated in readout)
     if(true)
        {
	if( PURE_n_moller_clust1>0 && PURE_n_moller_tracks1>0 && PURE_n_moller_clust2>0 && PURE_n_moller_tracks2>0) // Both Mollers have at least 1 cluster and 1 track
            {

	// FIRST MOLLER
	  PURE_moller_clust1 = (EcalCluster*)PURE_moller_clusters1->At(0);
          PURE_moller_track1 = (SvtTrack*)PURE_moller_tracks1->At(0);
          int PURE_tracktype1 = PURE_moller_track1->getType();

          double PURE_tanLambda1 = PURE_moller_track1->getTanLambda();

          vector<double> PURE_mom1 = PURE_moller1->getMomentum(); double PURE_px1 = PURE_mom1[0]; double PURE_py1 = PURE_mom1[1]; double PURE_pz1 = PURE_mom1[2];
          double PURE_P1 = sqrt( PURE_px1*PURE_px1 + PURE_py1*PURE_py1 + PURE_pz1*PURE_pz1 );
          double PURE_E1 = PURE_moller_clust1->getEnergy();
          double PURE_TrackE1 = sqrt(PURE_P1*PURE_P1 + 0.0005109989*0.0005109989);
          double PURE_theta1 = atan2(sqrt(PURE_px1*PURE_px1 + PURE_py1*PURE_py1),PURE_pz1);
          double PURE_time1 = PURE_moller_clust1->getSeed()->getTime();
          // 'Unrotate' momentum1
          double PURE_unrot_px1 = PURE_px1*cos(-0.0305) + PURE_pz1*sin(-0.0305);
          double PURE_unrot_pz1 = PURE_pz1*cos(-0.0305) - PURE_px1*sin(-0.0305);
          double PURE_unrot_theta1 = atan2(sqrt(PURE_unrot_px1*PURE_unrot_px1 + PURE_py1*PURE_py1),PURE_unrot_pz1);
          // Find Model energy
          double PURE_denom1 = 1+2*sin(PURE_unrot_theta1/2)*sin(PURE_unrot_theta1/2)*(2300/0.5109989);
          double PURE_model1 = 2.3/PURE_denom1;

          double PURE_phi01 = 90 + atan(PURE_py1/PURE_unrot_px1)*180.0 / TMath::Pi();

        // SECOND MOLLER
          PURE_moller_clust2 = (EcalCluster*)PURE_moller_clusters2->At(0);
          PURE_moller_track2 = (SvtTrack*)PURE_moller_tracks2->At(0);
          int PURE_tracktype2 = PURE_moller_track2->getType();

           double PURE_tanLambda2 = PURE_moller_track2->getTanLambda();

          vector<double>  PURE_mom2 = PURE_moller2->getMomentum(); double PURE_px2 = PURE_mom2[0]; double PURE_py2 = PURE_mom2[1]; double PURE_pz2 = PURE_mom2[2];
           double PURE_P2 = sqrt( PURE_px2*PURE_px2 + PURE_py2*PURE_py2 + PURE_pz2*PURE_pz2 );
           double PURE_E2 = PURE_moller_clust2->getEnergy();
           double PURE_TrackE2 = sqrt(PURE_P2*PURE_P2 + 0.0005109989*0.0005109989);
           double PURE_theta2 = atan2(sqrt(PURE_px2*PURE_px2 + PURE_py2*PURE_py2),PURE_pz2);
           double PURE_time2 = PURE_moller_clust2->getSeed()->getTime();
           // 'Unrotate' momentum2
           double PURE_unrot_px2 = PURE_px2*cos(-0.0305) + PURE_pz2*sin(-0.0305);
           double PURE_unrot_pz2 = PURE_pz2*cos(-0.0305) - PURE_px2*sin(-0.0305);
           double PURE_unrot_theta2 = atan2(sqrt(PURE_unrot_px2*PURE_unrot_px2 + PURE_py2*PURE_py2),PURE_unrot_pz2);
           // Find Model energy2
           double PURE_denom2 = 1+2*sin(PURE_unrot_theta2/2)*sin(PURE_unrot_theta2/2)*(2300/0.5109989);
           double PURE_model2 = 2.3/PURE_denom2;

            double PURE_phi02 = 90 + atan(PURE_py2/PURE_unrot_px2)*180.0 / TMath::Pi();

            PURE_moller_ESum->Fill(PURE_TrackE1+PURE_TrackE2);

            vector<double> PURE_position1 = PURE_moller_clust1->getPosition();
            vector<double> PURE_position2 = PURE_moller_clust2->getPosition();
            vector<double> PURE_trackAtEcal1 = PURE_moller_track1->getPositionAtEcal();
            vector<double> PURE_trackAtEcal2 = PURE_moller_track2->getPositionAtEcal();

               double PURE_clusterAngle1 = atan(PURE_position1[0]/PURE_position1[1]) * 180.0 / TMath::Pi();
               double PURE_clusterAngle2 = atan(PURE_position2[0]/PURE_position2[1]) * 180.0 / TMath::Pi();

            PURE_massSingles1->SetLineColor(kGreen);
            PURE_massSingles1->Fill(PURE_mollerMass);

// ChiSq Cuts
       //  if(DATA_tracktype1 > 32 && DATA_tracktype2 > 32 && DATA_Moller->getVertexFitChi2()<=10 && DATA_moller_track1->getChi2()<=15 && DATA_moller_track2->getChi2()<=15)
        if(PURE_tracktype1 > 32 && PURE_tracktype2 > 32) // GBL only
    //   if(true)
        {
           PURE_massGBL->SetLineColor(kGreen);
           PURE_massGBL->Fill(PURE_mollerMass);

	  // Theta1-Theta2 (Elastic Model + "Triangle Cut")
	 // if((sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)<=0.00040 && sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)>=0.00016 && DATA_unrot_theta1+DATA_unrot_theta2<=0.0725 && DATA_unrot_theta1+DATA_unrot_theta2>=0.055) )
	//  if(sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)>=0.00016 && sin(DATA_unrot_theta1/2)*sin(DATA_unrot_theta2/2)<=0.00045 && DATA_unrot_theta1+DATA_unrot_theta2<=0.09)
         // if(abs(PURE_time1-PURE_time2)<=1.7)
          if(true)
          {
             PURE_mass1->SetLineColor(kGreen);
            PURE_mass1->Fill(PURE_mollerMass);

            PURE_ESumE->Fill(PURE_E1,PURE_E1+PURE_E2);

	  // Energy1-Energy2
         //  if( DATA_TrackE1+DATA_TrackE2>=0.8 && DATA_TrackE1+DATA_TrackE2<=1.3 && DATA_TrackE1<=0.9 && DATA_TrackE2<=0.9 && DATA_E1<=0.9 && DATA_E2<=0.9 && abs(DATA_clusterAngle1-DATA_clusterAngle2)>=80 && abs(DATA_clusterAngle1-DATA_clusterAngle2)<=150)
          // if((PURE_phi01 - PURE_phi02) > -70 && (PURE_phi01 - PURE_phi02) < 70 && PURE_TrackE1+PURE_TrackE2>=0.9 && PURE_TrackE1+PURE_TrackE2<=1.2 && PURE_E1+PURE_E2>=0.9 && PURE_E1+PURE_E2<=1.2 && PURE_TrackE1<=0.85 && PURE_TrackE2<=0.85 && PURE_E1<=0.85 && PURE_E2<=0.85)
	 // if(true)
        //  if(PURE_TrackE1<=0.85 && PURE_TrackE2<=0.85)
           if(true)
            {
               PURE_mass2->SetLineColor(kGreen);
            PURE_mass2->Fill(PURE_mollerMass);

	  // Energy-Theta
	//  if((abs(DATA_TrackE1-DATA_model1)<=0.2 && abs(DATA_TrackE2-DATA_model2)<= 0.2))
       //  if(PURE_TrackE1+PURE_TrackE2<=1.2 && PURE_TrackE1+PURE_TrackE2>=0.9)
	//  if(PURE_TrackE1+PURE_TrackE2<=1.2 && PURE_TrackE1+PURE_TrackE2>=0.9 && PURE_E1+PURE_E2<=1.2 && PURE_E1+PURE_E2>=0.9)
          if(true)
            {
              PURE_mass3->SetLineColor(kGreen);
            PURE_mass3->Fill(PURE_mollerMass);
	  // Secondary Cuts
	 // if((abs(DATA_time1-DATA_time2)<=1.5 && DATA_TrackE1>=0.3 && DATA_TrackE1<=0.75 && DATA_TrackE2>=0.3 && DATA_TrackE2<=0.75 && DATA_unrot_theta1>=0.02 && DATA_unrot_theta1<=0.045 && DATA_unrot_theta2>=0.02 && DATA_unrot_theta2<=0.045) )
	 //  if((abs(DATA_time1-DATA_time2)<=3) && DATA_E1>=0.5 && DATA_E1<=2 && DATA_E2>=0.5 && DATA_E2<=2 )
          //   if(DATA_unrot_theta1<=0.06 && DATA_unrot_theta2<=0.06)
         //  if(DATA_TrackE1<=1.7 && DATA_TrackE2<=1.7)
         //  if(abs(PURE_time1-PURE_time2)<=1.7)
//	  if(abs(PURE_time1-PURE_time2)<=1.7 && PURE_unrot_theta1>=0.015 && PURE_unrot_theta2>=0.015 && PURE_unrot_theta1+PURE_unrot_theta2 >=0.045 && PURE_unrot_theta1+PURE_unrot_theta2 <=0.085)
//          if(PURE_unrot_theta1+PURE_unrot_theta2>=0.050 && PURE_unrot_theta1+PURE_unrot_theta2<=0.080)
          if(true)
// Momar Cuts //  if(DATA_TrackE1>=0.05 && DATA_TrackE2>=0.05 && DATA_TrackE1<=0.85 && DATA_TrackE2<=0.85 && abs(DATA_time1-DATA_time2)<=1.6 && DATA_tanLambda1*DATA_tanLambda2 < 0)
            {
	    //CUT_moller_thetaE->Fill(TrackE1,theta1); CUT_moller_thetaE->Fill(TrackE2,theta2);
          
         //  if((PURE_position1[0] - PURE_trackAtEcal1[0]) <= 15 && (PURE_position1[0] - PURE_trackAtEcal1[0]) >= -15 && (PURE_position1[1] - PURE_trackAtEcal1[1])<= 20 && (PURE_position1[1] - PURE_trackAtEcal1[1])>= -20 && (PURE_position2[0] - PURE_trackAtEcal2[0]) <= 15 && (PURE_position2[0] - PURE_trackAtEcal2[0]) >= -15 && (PURE_position2[1] - PURE_trackAtEcal2[1])<= 20 && (PURE_position2[1] - PURE_trackAtEcal2[1])>= -20)
            if((PURE_position1[1] - PURE_trackAtEcal1[1])<= 10 && (PURE_position1[1] - PURE_trackAtEcal1[1])>= -10 && (PURE_position2[1] - PURE_trackAtEcal2[1])<= 10 && (PURE_position2[1] - PURE_trackAtEcal2[1])>= -10)
          //  if(true)
               {

            PURE_CUT_MollerTT->Fill(PURE_unrot_theta1,PURE_unrot_theta2);
	    PURE_CUT_unrot_moller_thetaE->Fill(PURE_E1,PURE_unrot_theta1); PURE_CUT_unrot_moller_thetaE->Fill(PURE_E2,PURE_unrot_theta2);
	    PURE_CUT_moller_E->SetLineColor(kGreen);
            //DATA_CUT_moller_E->Scale(norm);


            PURE_px->SetLineColor(kGreen);
            PURE_py->SetLineColor(kGreen);
            PURE_pz->SetLineColor(kGreen);
            PURE_px->Fill(PURE_px1); PURE_px->Fill(PURE_px2);
            PURE_py->Fill(PURE_py1); PURE_py->Fill(PURE_py2);
            PURE_pz->Fill(PURE_pz1); PURE_pz->Fill(PURE_pz2);     


            PURE_TrackE->SetLineColor(kGreen);
            PURE_TrackE->Fill(PURE_TrackE1); PURE_TrackE->Fill(PURE_TrackE2);
            PURE_ClusterE->SetLineColor(kGreen);
            PURE_ClusterE->Fill(PURE_E1); PURE_ClusterE->Fill(PURE_E2);

            PURE_ClusterE1->SetLineColor(kGreen); PURE_ClusterE2->SetLineColor(kGreen);
            PURE_ClusterE1->Fill(PURE_E1);
            PURE_ClusterE2->Fill(PURE_E2);


            PURE_ClusterEE->Fill(PURE_E1,PURE_E2);
            PURE_TrackEE->Fill(PURE_TrackE1,PURE_TrackE2);


//            if(DATA_moller1->getCharge() > 0 && DATA_moller2->getCharge() < 0)
//               {
//                 DATA_TrackEE->Fill(DATA_TrackE1,DATA_TrackE2);
//                 DATA_ClusterEE->Fill(DATA_E1,DATA_E2);
//                } else if (DATA_moller1->getCharge() < 0 && DATA_moller2->getCharge() > 0)
//                {
//                  DATA_TrackEE->Fill(DATA_TrackE2,DATA_TrackE1);
//                  DATA_ClusterEE->Fill(DATA_E2,DATA_E1);
//                }


               if(PURE_E1 < PURE_E2)
               {
               double PURE_lowEClusterDistance = TMath::Hypot(PURE_moller_clust1->getSeed()->getXCrystalIndex() - 1393.0 * TMath::Tan(0.03052), PURE_moller_clust1->getSeed()->getYCrystalIndex());
               PURE_energy_slope->Fill(PURE_E1,PURE_lowEClusterDistance);
               }

               if(PURE_E1 > PURE_E2)
               {
               double PURE_lowEClusterDistance = TMath::Hypot(PURE_moller_clust2->getSeed()->getXCrystalIndex() - 1393.0 * TMath::Tan(0.03052), PURE_moller_clust2->getSeed()->getYCrystalIndex());
               PURE_energy_slope->Fill(PURE_E2,PURE_lowEClusterDistance);
               }

               PURE_seed_E->Fill(PURE_moller_clust1->getSeed()->getEnergy());
               PURE_seed_E->Fill(PURE_moller_clust2->getSeed()->getEnergy());





	    PURE_CUT_moller_Theta->SetLineColor(kGreen);
	    PURE_CUT_moller_Theta->Fill(PURE_unrot_theta1); PURE_CUT_moller_Theta->Fill(PURE_unrot_theta2);
	    PURE_TRACK_ESum->SetLineColor(kGreen);
	    PURE_TRACK_ESum->Fill(PURE_TrackE1+PURE_TrackE2);
            PURE_CLUSTER_ESum->SetLineColor(kGreen);
            PURE_CLUSTER_ESum->Fill(PURE_E1+PURE_E2);
            PURE_CUT_ETTest->SetLineColor(kGreen);
	    PURE_CUT_ETTest->Fill(PURE_model1-PURE_TrackE1); PURE_CUT_ETTest->Fill(PURE_model2-PURE_TrackE2);
            PURE_CUT_SinSinTest->SetLineColor(kGreen);
	    PURE_CUT_SinSinTest->Fill(sin(PURE_unrot_theta1/2)*sin(PURE_unrot_theta2/2));
            PURE_CUT_V0_coincidence->SetLineColor(kGreen);
            PURE_CUT_V0_coincidence->Fill(PURE_time1-PURE_time2);
            PURE_hitTime->Fill(PURE_time1); PURE_hitTime->Fill(PURE_time2);
	    //CUT_moller_EP->Fill(E1,TrackE1); CUT_moller_EP->Fill(E2,TrackE2);
	   PURE_CUT_MollerXVTX->SetLineColor(kGreen);
	   PURE_CUT_MollerXVTX->Fill(PURE_vtx_moller[0]);
           PURE_CUT_MollerYVTX->SetLineColor(kGreen);
	   PURE_CUT_MollerYVTX->Fill(PURE_vtx_moller[1]);
           PURE_CUT_MollerZVTX->SetLineColor(kGreen);
	   PURE_CUT_MollerZVTX->Fill(PURE_vtx_moller[2]);

           PURE_hitxDiff->SetLineColor(kGreen); PURE_hityDiff->SetLineColor(kGreen);
           PURE_hitxDiff->Fill(PURE_position1[0] - PURE_trackAtEcal1[0]); PURE_hitxDiff->Fill(PURE_position2[0] - PURE_trackAtEcal2[0]);
           PURE_hityDiff->Fill(PURE_position1[1] - PURE_trackAtEcal1[1]); PURE_hityDiff->Fill(PURE_position2[1] - PURE_trackAtEcal2[1]);
 
           //PURE_tracksAtEcal->SetLineColor(kGreen);
           PURE_tracksAtEcal->Fill(PURE_trackAtEcal1[0],PURE_trackAtEcal1[1]);
           PURE_tracksAtEcal->Fill(PURE_trackAtEcal2[0],PURE_trackAtEcal2[1]);

           PURE_EP->Fill(PURE_E1,PURE_TrackE1); PURE_EP->Fill(PURE_E2,PURE_TrackE2);

	    PURE_Mass->SetLineColor(kGreen);
	    PURE_Mass->Fill(PURE_mollerMass);
	     
            PURE_ESumMass->Fill(PURE_mollerMass,PURE_E1+PURE_E2);

          // CUT_vtxChi2->Fill(Moller->getVertexFitChi2());
          // CUT_trackChi2->Fill(moller_track1->getChi2()); 
          // CUT_trackChi2->Fill(moller_track2->getChi2());

              PURE_coplanarity->SetLineColor(kGreen);
              PURE_coplanarity->Fill(abs(PURE_clusterAngle1-PURE_clusterAngle2));

               PURE_phiDiff->SetLineColor(kGreen);
              PURE_phiDiff->Fill(PURE_phi01 - PURE_phi02);


               PURE_TrackChi2->SetLineColor(kGreen);
               PURE_TrackChi2->Fill(PURE_moller_track1->getChi2());
               PURE_TrackChi2->SetLineColor(kGreen);
               PURE_TrackChi2->Fill(PURE_moller_track2->getChi2());

               PURE_vtxChi2->SetLineColor(kGreen);
               PURE_vtxChi2->Fill(PURE_Moller->getVertexFitChi2());
 
               PURE_ESumE->Fill(PURE_E1,PURE_E1+PURE_E2);


 // SVT WORLD
//          for(int hit_n=0; hit_n<DATA_SVT_hits1->GetEntries(); ++hit_n)
//              {
//                DATA_svt_hit1 = (SvtHit*) DATA_SVT_hits1->At(hit_n);
//                vector<double> DATA_svt_hit_position1 = DATA_svt_hit1->getPosition();
//                int DATA_layer = DATA_svt_hit1->getLayer();

//                switch(DATA_layer){
//                case 1:
//                   DATA_L1->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 2:
//                   DATA_L2->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 3:
//                   DATA_L3->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 4:
//                   DATA_L4->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                   break;
//                case 5:
//                   DATA_L5->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);

//                   break;
//                case 6:
//                    DATA_L6->Fill(DATA_svt_hit_position1[0],DATA_svt_hit_position1[1]);
//                    break;  
//                 }
//               }// SVT WORLD1

//           for(int hit_n=0; hit_n<DATA_SVT_hits2->GetEntries(); ++hit_n)
//              {
//                DATA_svt_hit2 = (SvtHit*) DATA_SVT_hits2->At(hit_n);
//                vector<double> DATA_svt_hit_position2 = DATA_svt_hit2->getPosition();
//                   int DATA_layer = DATA_svt_hit2->getLayer();

//                switch(DATA_layer){
//                case 1:
//                   DATA_L1->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 2:
//                   DATA_L2->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 3:
//                   DATA_L3->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 4:
//                   DATA_L4->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                   break;
//                case 5:
//                   DATA_L5->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);

//                   break;
//                case 6:
//                    DATA_L6->Fill(DATA_svt_hit_position2[0],DATA_svt_hit_position2[1]);
//                    break;
//                 }
//               }// SVT WORLD2

// ECAL WORLD

           TRefArray *PURE_CUT_ec_hits1 = PURE_moller_clust1->getEcalHits();
           int index_x1=0, index_y1=0;
           Fiducial1 = false, Fiducial2 = false, Edge1 = false, Edge2 = false;

           for(int hit_n=0; hit_n<PURE_CUT_ec_hits1->GetEntries(); ++hit_n)
                  {
                     ec_hit1 = (EcalHit*) PURE_CUT_ec_hits1->At(hit_n);
                     index_x1 = ec_hit1->getXCrystalIndex();
                     index_y1 = ec_hit1->getYCrystalIndex();

                     //PURE_EPRatio->Fill(PURE_E1/PURE_P1);

                     // Select electron or positron tracks
                     	if(PURE_E1<0.5)
                     	{
                     	PURE_neg_hits->Fill(index_x1,index_y1,1);
                        PURE_lowET->SetLineColor(kRed);
                        PURE_lowET->Fill(PURE_model1-PURE_TrackE1);
                     	}
                     	if(PURE_E1>0.5)
                     	{
                     	PURE_pos_hits->Fill(index_x1,index_y1,1);
                        PURE_highET->Fill(PURE_model1-PURE_TrackE1);
                     	}

                     // Edge 1
                     //if(((index_x1<=-2 && index_x1>=-10)&&(index_y1==2||index_y1==-2)) || (index_y1==1||index_y1==-1))
                     if((index_x1<=-8 && index_x1>=-10)&&(index_y1==2||index_y1==-2) || ((index_x1<=-10 && index_x1>=-12)&&(index_y1==1||index_y1==-1)))
                     {
                     	PURE_ECal_hits->Fill(index_x1,index_y1,1);
                     	PURE_EDGE_ECal_hits->Fill(index_x1,index_y1,1);
                     	PURE_EDGE_Moller_EPRatio->Fill(PURE_E1/PURE_P1);
                     	PURE_EDGE_Moller_EP->Fill(PURE_E1,PURE_P1);

                        PURE_EDGE_Moller_E->SetLineColor(kGreen);
                     	PURE_EDGE_Moller_E->Fill(PURE_E1);
                        PURE_EDGE_TRACK_E->SetLineColor(kGreen);
                     	PURE_EDGE_TRACK_E->Fill(PURE_TrackE1);

                     	if(PURE_moller_clust1->getSeed()->getXCrystalIndex()==index_x1 && PURE_moller_clust1->getSeed()->getYCrystalIndex()==index_y1)
                     	{                     
                       	Edge1 = true;
                     	}
                    
                     } // EDGE1

                     // Fiducial Elastic Cut, Moller1
                     if(index_y1!=1 && index_y1!=-1)
                     {
                     if( !((index_y1==2||index_y1==-2)&&(index_x1>=-10 && index_x1<=-2)))
                     {
                        PURE_ECal_hits->Fill(index_x1,index_y1,1);
                        PURE_FIDUCIAL_ECal_hits->Fill(index_x1,index_y1,1);                     
                        PURE_FIDUCIAL_Moller_EPRatio->Fill(PURE_E1/PURE_P1);
                        PURE_FIDUCIAL_Moller_EP->Fill(PURE_E1,PURE_P1);

                        PURE_FIDUCIAL_Moller_E->SetLineColor(kGreen);
                        PURE_FIDUCIAL_Moller_E->Fill(PURE_E1);
                        PURE_FIDUCIAL_TRACK_Moller_E->SetLineColor(kGreen);
                        PURE_FIDUCIAL_TRACK_Moller_E->Fill(PURE_TrackE1);

                        if(PURE_moller_clust1->getSeed()->getXCrystalIndex()==index_x1 && PURE_moller_clust1->getSeed()->getYCrystalIndex()==index_y1)
                         {                                                                                                                                                                                                                                          Fiducial1 = true;
                         }
                       }
                     }//FIDUCIAL 1
                    }// CLUSTER1


                  // CLUSTER 2

                  TRefArray *PURE_CUT_ec_hits2 = PURE_moller_clust2->getEcalHits();
                  int index_x2=0, index_y2=0;
                  Fiducial1 = false, Fiducial2 = false, Edge1 = false, Edge2 = false;

                  for(int hit_n=0; hit_n<PURE_CUT_ec_hits2->GetEntries(); ++hit_n)
                  {
                     ec_hit2 = (EcalHit*) PURE_CUT_ec_hits2->At(hit_n);
                     index_x2 = ec_hit2->getXCrystalIndex();
                     index_y2 = ec_hit2->getYCrystalIndex();

                     PURE_CUT_EPRatio->Fill(PURE_E2/PURE_P2);

                     if(PURE_E2<0.5)
                        {
                        PURE_neg_hits->Fill(index_x2,index_y2,1);
                        PURE_lowET->SetLineColor(kRed);
                        PURE_lowET->Fill(PURE_model2-PURE_TrackE2);
                        }
                        if(PURE_E2>0.5)
                        {
                        PURE_pos_hits->Fill(index_x2,index_y2,1);
                        PURE_highET->SetLineColor(kRed);
                        PURE_highET->Fill(PURE_model2-PURE_TrackE2);
                        }


                   // EDGE 2
                   if((index_x2<=-8 && index_x2>=-10)&&(index_y2==2||index_y2==-2) || ((index_x1<=-10 && index_x1>=-12)&&(index_y2==1||index_y2==-1)))
                     {
                     PURE_ECal_hits->Fill(index_x2,index_y2,1);
                     PURE_EDGE_ECal_hits->Fill(index_x2,index_y2,1);
                     PURE_EDGE_Moller_EPRatio->Fill(PURE_E2/PURE_P2);
                     PURE_EDGE_Moller_EP->Fill(PURE_E2,PURE_P2);
                    
                     PURE_EDGE_Moller_E->SetLineColor(kGreen);
                     PURE_EDGE_Moller_E->Fill(PURE_E2);
                     PURE_EDGE_TRACK_Moller_E->SetLineColor(kGreen);
                     PURE_EDGE_TRACK_Moller_E->Fill(PURE_TrackE2);

                     if(PURE_moller_clust2->getSeed()->getXCrystalIndex()==index_x2 && PURE_moller_clust2->getSeed()->getYCrystalIndex()==index_y2)
                     {
                       Edge2 = true;
                     }
                    } // EDGE 2

                   // FIDUCIAL 2
                   if(index_y2!=1 && index_y2!=-1)
                     {
                     if( !((index_y2==2||index_y2==-2)&&(index_x2>=-10 && index_x2<=-2)))
                     {
                        PURE_ECal_hits->Fill(index_x2,index_y2,1);
                        PURE_FIDUCIAL_ECal_hits->Fill(index_x2,index_y2,1);
                        PURE_FIDUCIAL_Moller_EPRatio->Fill(PURE_E2/PURE_P2);
                        PURE_FIDUCIAL_Moller_EP->Fill(PURE_E2,PURE_P2);

                        PURE_FIDUCIAL_Moller_E->SetLineColor(kGreen);
                        PURE_FIDUCIAL_Moller_E->Fill(PURE_E2);
                        PURE_FIDUCIAL_TRACK_Moller_E->SetLineColor(kGreen);
                        PURE_FIDUCIAL_TRACK_Moller_E->Fill(PURE_TrackE2);

                        if(PURE_moller_clust2->getSeed()->getXCrystalIndex()==index_x2 && PURE_moller_clust2->getSeed()->getYCrystalIndex()==index_y2)
                         {                                                                                                                                                                                                                                          Fiducial2 = true;
                         }
                       }
                    } // FIDUCIAL 2

                  } // CLUSTER 2


             }// Matching
             }//
             }//
             }//
             }//
 
            } // GBL Tracks

         } // n_moller_clust == 1 && n_moller_tracks == 1

       } // trigger select

     } // loop over Mollers

   } // loop over events

/////////////////////////////////////////////////////////////////////////////////////// END TREE 3: PURE MC ////////////////////////////////////////////////////////////////////////////////////






///// Overlay Plots with Moller Models (VERY stupid way of doing this. Set it up before learning about TF1's, and just never got around to changing it...) ///////////////////////////////////////////////////////////////////

      double modelT,modelDenom, modelAngleCorr,ModelE, var, MT;
      for(int k=1;k<=200000;k++)
        {

          // Theta-Energy Model
          modelT = k*0.06/200000;
          modelDenom = 1+2*sin(modelT/2)*sin(modelT/2)*(2300/0.5109989);
          moller_thetaE->Fill(2.3/modelDenom,modelT);
          unrot_moller_thetaE->Fill(2.3/modelDenom,modelT);
          CUT_moller_thetaE->Fill(2.3/modelDenom,modelT);
          CUT_unrot_V0_thetaE->Fill(2.3/modelDenom,modelT);
          DATA_CUT_unrot_moller_thetaE->Fill(2.3/modelDenom,modelT);
          PURE_CUT_unrot_moller_thetaE->Fill(2.3/modelDenom,modelT);

          electron_thetaE->Fill(2.3/modelDenom,modelT);

          // Theta-Theta Model
          modelAngleCorr = 2*asin(0.5109989/2/2300/sin(modelT/2));
          MollerTT->Fill(modelT,modelAngleCorr);
          CUT_V0TT->Fill(modelT,modelAngleCorr);
          DATA_CUT_MollerTT->Fill(modelT,modelAngleCorr);
          PURE_CUT_MollerTT->Fill(modelT,modelAngleCorr);

          // Energy-Energy Model
          ModelE = k*2.3/200000;
          MollerEE->Fill(ModelE,2.3-ModelE);
          TRACK_V0EE->Fill(ModelE,2.3-ModelE);
          CLUSTER_V0EE->Fill(ModelE,2.3-ModelE);
          DATA_ClusterEE->Fill(ModelE,2.3-ModelE);
          DATA_TrackEE->Fill(ModelE,2.3-ModelE);
          PURE_ClusterEE->Fill(ModelE,2.3-ModelE);
          PURE_TrackEE->Fill(ModelE,2.3-ModelE);

          var = k*2.3/200000;
          // Energy-Momentum
          CUT_FIDUCIAL_V0_EP->Fill(var,var);
          CUT_EDGE_V0_EP->Fill(var,var);
          CUT_V0_EP->Fill(var,var);
          DATA_EP->Fill(var,var);
          PURE_EP->Fill(var,var);
          moller_EP->Fill(var,var);
          FIDUCIAL_allEP->Fill(var,var);
          FEE_EP->Fill(var,var);
        }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


///// OUTPUT HISTOGRAMS //////////////////////////////////////////////////////
      TCanvas *c1 = new TCanvas("c1", "c1",10,10,1000,750);
      c1->SetLogz();   
//      gStyle->SetOptFit(1);

//// OUTPUT STACKS //////////////////////////////////////////////////////////////////

CUT_V0_Mass->Scale(1000/MC_Lumin/2); // Scale by XS (mb)
DATA_Mass->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_Mass->Scale(1000/PURE_Lumin/2);
CUT_V0_Mass->Write();
DATA_Mass->Write();
PURE_Mass->Write();
Mass->Add(CUT_V0_Mass);
Mass->Add(DATA_Mass);
Mass->Add(PURE_Mass);
Mass->Write();
Mass->Draw("nostack");
strcpy(outputname,"ALL_mass4");
c1->SaveAs(strcat(outputname,".png"));

massSingles1->Scale(1000/MC_Lumin/2); // Scale by XS (mb)
DATA_massSingles1->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_massSingles1->Scale(1000/PURE_Lumin/2);
massSingles1->Write();
DATA_massSingles1->Write();
PURE_massSingles1->Write();
MassSingles1->Add(massSingles1);
MassSingles1->Add(DATA_massSingles1);
MassSingles1->Add(PURE_massSingles1);
MassSingles1->Write();
MassSingles1->Draw("nostack");
strcpy(outputname,"ALL_massSingles1");
c1->SaveAs(strcat(outputname,".png"));

massGBL->Scale(1000/MC_Lumin/2); // Scale by XS (mb)
DATA_massGBL->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_massGBL->Scale(1000/PURE_Lumin/2);
massGBL->Write();
DATA_massGBL->Write();
PURE_massGBL->Write();
MassGBL->Add(massGBL);
MassGBL->Add(DATA_massGBL);
MassGBL->Add(PURE_massGBL);
MassGBL->Write();
MassGBL->Draw("nostack");
strcpy(outputname,"ALL_massGBL");
c1->SaveAs(strcat(outputname,".png"));

mass1->Scale(1000/MC_Lumin/2); // Scale by XS (mb)
DATA_mass1->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_mass1->Scale(1000/PURE_Lumin/2);
mass1->Write();
DATA_mass1->Write();
PURE_mass1->Write();
Mass1->Add(mass1);
Mass1->Add(DATA_mass1);
Mass1->Add(PURE_mass1);
Mass1->Write();
Mass1->Draw("nostack");
strcpy(outputname,"ALL_mass1");
c1->SaveAs(strcat(outputname,".png"));

mass2->Scale(1000/MC_Lumin/2); // Scale by XS (mb)
DATA_mass2->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_mass2->Scale(1000/PURE_Lumin/2);
mass2->Write();
DATA_mass2->Write();
PURE_mass2->Write();
Mass2->Add(mass2);
Mass2->Add(DATA_mass2);
Mass2->Add(PURE_mass2);
Mass2->Write();
Mass2->Draw("nostack");
strcpy(outputname,"ALL_mass2");
c1->SaveAs(strcat(outputname,".png"));

mass3->Scale(1000/MC_Lumin/2); // Scale by XS (mb)
DATA_mass3->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_mass3->Scale(1000/PURE_Lumin/2);
mass3->Write();
DATA_mass3->Write();
PURE_mass3->Write();
Mass3->Add(mass3);
Mass3->Add(DATA_mass3);
Mass3->Add(PURE_mass3);
Mass3->Write();
Mass3->Draw("nostack");
strcpy(outputname,"ALL_mass3");
c1->SaveAs(strcat(outputname,".png"));


//TRACK_V0_E->Scale(1/MC_Lumin);
//CLUSTER_V0_E->Scale(1/MC_Lumin);
TRACK_V0_E->Scale(1000/MC_Lumin/2);
DATA_TrackE->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_TrackE->Scale(1000/PURE_Lumin/2);
TRACK_V0_E->Write();
DATA_TrackE->Write();
Energy->Add(TRACK_V0_E);
Energy->Add(DATA_TrackE);
Energy->Add(PURE_TrackE);
Energy->Write();
Energy->Draw("nostack");
strcpy(outputname,"ALL_Energy");
c1->SaveAs(strcat(outputname,".png"));

CLUSTER_V0_E->Scale(1000/MC_Lumin/2);
DATA_ClusterE->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_ClusterE->Scale(1000/PURE_Lumin/2);
CLUSTER_V0_E->Write();
DATA_ClusterE->Write();
ClustEnergy->Add(CLUSTER_V0_E);
ClustEnergy->Add(DATA_ClusterE);
ClustEnergy->Add(PURE_ClusterE);
ClustEnergy->Write();
ClustEnergy->Draw("nostack");
strcpy(outputname,"ALL_EnergyClust");
c1->SaveAs(strcat(outputname,".png"));

CLUSTER_V0_E1->Scale(1000/MC_Lumin/2);
DATA_ClusterE1->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_ClusterE1->Scale(1000/PURE_Lumin/2);
CLUSTER_V0_E1->Write();
DATA_ClusterE1->Write();
ClustEnergy_TOP->Add(CLUSTER_V0_E1);
ClustEnergy_TOP->Add(DATA_ClusterE1);
ClustEnergy_TOP->Add(PURE_ClusterE1);
ClustEnergy_TOP->Write();
ClustEnergy_TOP->Draw("nostack");
strcpy(outputname,"ALL_EnergyClust_TOP");
c1->SaveAs(strcat(outputname,".png"));

CLUSTER_V0_E2->Scale(1000/MC_Lumin/2);
DATA_ClusterE2->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_ClusterE2->Scale(1000/PURE_Lumin/2);
CLUSTER_V0_E2->Write();
DATA_ClusterE2->Write();
ClustEnergy_BOTTOM->Add(CLUSTER_V0_E2);
ClustEnergy_BOTTOM->Add(DATA_ClusterE2);
ClustEnergy_BOTTOM->Add(PURE_ClusterE2);
ClustEnergy_BOTTOM->Write();
ClustEnergy_BOTTOM->Draw("nostack");
strcpy(outputname,"ALL_EnergyClust_BOTTOM");
c1->SaveAs(strcat(outputname,".png"));

EDGE_TRACK_V0_E->Scale(1000/MC_Lumin/2);
DATA_EDGE_TRACK_Moller_E->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_EDGE_TRACK_Moller_E->Scale(1000/PURE_Lumin/2);
EDGE_TRACK_V0_E->Write();
DATA_EDGE_TRACK_Moller_E->Write();
EDGE_TrackEnergy->Add(EDGE_TRACK_V0_E);
EDGE_TrackEnergy->Add(DATA_EDGE_TRACK_Moller_E);
EDGE_TrackEnergy->Add(PURE_EDGE_TRACK_Moller_E);
EDGE_TrackEnergy->Write();
EDGE_TrackEnergy->Draw("nostack");
strcpy(outputname,"ALL_EDGE_TrackE");
c1->SaveAs(strcat(outputname,".png"));

FIDUCIAL_TRACK_V0_E->Scale(1000/MC_Lumin/2);
DATA_FIDUCIAL_TRACK_Moller_E->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_FIDUCIAL_TRACK_Moller_E->Scale(1000/PURE_Lumin/2);
FIDUCIAL_TRACK_V0_E->Write();
DATA_FIDUCIAL_TRACK_Moller_E->Write();
FIDUCIAL_TrackEnergy->Add(FIDUCIAL_TRACK_V0_E);
FIDUCIAL_TrackEnergy->Add(DATA_FIDUCIAL_TRACK_Moller_E);
FIDUCIAL_TrackEnergy->Add(PURE_FIDUCIAL_TRACK_Moller_E);
FIDUCIAL_TrackEnergy->Write();
FIDUCIAL_TrackEnergy->Draw("nostack");
strcpy(outputname,"ALL_FIDUCIAL_TrackE");
c1->SaveAs(strcat(outputname,".png"));

EDGE_V0_E->Scale(1000/MC_Lumin/2);
DATA_EDGE_Moller_E->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_EDGE_Moller_E->Scale(1000/PURE_Lumin/2);
EDGE_V0_E->Write();
DATA_EDGE_Moller_E->Write();
EDGE_ClustEnergy->Add(EDGE_V0_E);
EDGE_ClustEnergy->Add(DATA_EDGE_Moller_E);
EDGE_ClustEnergy->Add(PURE_EDGE_Moller_E);
EDGE_ClustEnergy->Write();
EDGE_ClustEnergy->Draw("nostack");
strcpy(outputname,"ALL_EDGE_ClustE");
c1->SaveAs(strcat(outputname,".png"));

FIDUCIAL_V0_E->Scale(1000/MC_Lumin/2);
DATA_FIDUCIAL_Moller_E->Scale(DATA_Prescale*1000/DATA_Lumin); // one of 471 files used
PURE_FIDUCIAL_Moller_E->Scale(1000/PURE_Lumin/2);
FIDUCIAL_V0_E->Write();
DATA_FIDUCIAL_Moller_E->Write();
FIDUCIAL_ClustEnergy->Add(FIDUCIAL_V0_E);
FIDUCIAL_ClustEnergy->Add(DATA_FIDUCIAL_Moller_E);
FIDUCIAL_ClustEnergy->Add(PURE_FIDUCIAL_Moller_E);
FIDUCIAL_ClustEnergy->Write();
FIDUCIAL_ClustEnergy->Draw("nostack");
strcpy(outputname,"ALL_FIDUCIAL_ClustE");
c1->SaveAs(strcat(outputname,".png"));


CUT_V0_Theta->Scale(1000/MC_Lumin/2);
DATA_CUT_moller_Theta->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_moller_Theta->Scale(1000/PURE_Lumin/2);
CUT_V0_Theta->Write();
//DATA_CUT_moller_Theta->Write();
Theta->Add(CUT_V0_Theta);
Theta->Add(DATA_CUT_moller_Theta);
Theta->Add(PURE_CUT_moller_Theta);
Theta->Write();
Theta->Draw("nostack");
strcpy(outputname,"ALL_Theta");
c1->SaveAs(strcat(outputname,".png"));

//TRACK_V0_ESum->Scale(1/MC_Lumin);
//CLUSTER_V0_ESum->Scale(1/MC_Lumin);
//FIDUCIAL_V0_ESum->Scale(1/MC_Lumin);
//EDGE_V0_ESum->Scale(1/MC_Lumin);

TRACK_V0_ESum->Scale(1000/MC_Lumin/2);
DATA_TRACK_ESum->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_TRACK_ESum->Scale(1000/PURE_Lumin/2);
TRACK_V0_ESum->Write();
DATA_TRACK_ESum->Write();
//DATA_ESum->Write();
EE->Add(TRACK_V0_ESum);
EE->Add(DATA_TRACK_ESum);
EE->Add(PURE_TRACK_ESum);
EE->Write();
EE->Draw("nostack");
strcpy(outputname,"ALL_ESum");
c1->SaveAs(strcat(outputname,".png"));

CLUSTER_V0_ESum->Scale(1000/MC_Lumin/2);
DATA_CLUSTER_ESum->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CLUSTER_ESum->Scale(1000/PURE_Lumin/2);
CLUSTER_V0_ESum->Write();
DATA_CLUSTER_ESum->Write();
ClustESum->Add(CLUSTER_V0_ESum);
ClustESum->Add(DATA_CLUSTER_ESum);
ClustESum->Add(PURE_CLUSTER_ESum);
ClustESum->Write();
ClustESum->Draw("nostack");
strcpy(outputname,"ALL_ClustESum");
c1->SaveAs(strcat(outputname,".png"));

CUT_SinSinTest->Scale(1000/MC_Lumin/2);
DATA_CUT_SinSinTest->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_SinSinTest->Scale(1000/PURE_Lumin/2);
CUT_SinSinTest->Write();
DATA_CUT_SinSinTest->Write();
TT->Add(CUT_SinSinTest);
TT->Add(DATA_CUT_SinSinTest);
TT->Add(PURE_CUT_SinSinTest);
TT->Write();
TT->Draw("nostack");
strcpy(outputname,"ALL_TT");
c1->SaveAs(strcat(outputname,".png"));

CUT_ETTest->Scale(1000/MC_Lumin/2);
DATA_CUT_ETTest->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_ETTest->Scale(1000/PURE_Lumin/2);
CUT_ETTest->Write();
DATA_CUT_ETTest->Write();
ET->Add(CUT_ETTest);
ET->Add(DATA_CUT_ETTest);
ET->Add(PURE_CUT_ETTest);
ET->Write();
ET->Draw("nostack");
strcpy(outputname,"ALL_ET");
c1->SaveAs(strcat(outputname,".png"));

highET->Scale(1000/MC_Lumin/2);
DATA_highET->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_highET->Scale(1000/PURE_Lumin/2);
//CUT_ETTest->Write();
//DATA_CUT_ETTest->Write();
HighET->Add(highET);
HighET->Add(DATA_highET);
HighET->Add(PURE_highET);
HighET->Write();
HighET->Draw("nostack");
strcpy(outputname,"ALL_HighET");
c1->SaveAs(strcat(outputname,".png"));

lowET->Scale(1000/MC_Lumin/2);
DATA_lowET->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_lowET->Scale(1000/PURE_Lumin/2);
//CUT_ETTest->Write();
////DATA_CUT_ETTest->Write();
LowET->Add(highET);
LowET->Add(DATA_highET);
LowET->Add(PURE_highET);
LowET->Write();
LowET->Draw("nostack");
strcpy(outputname,"ALL_LowET");
c1->SaveAs(strcat(outputname,".png"));

CUT_V0_XVTX->Scale(1000/MC_Lumin/2);
DATA_CUT_MollerXVTX->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_MollerXVTX->Scale(1000/PURE_Lumin/2);
CUT_V0_XVTX->Write();
DATA_CUT_MollerXVTX->Write();
XVtx->Add(CUT_V0_XVTX);
XVtx->Add(DATA_CUT_MollerXVTX);
XVtx->Add(PURE_CUT_MollerXVTX);
XVtx->Write();
XVtx->Draw("nostack");
strcpy(outputname,"ALL_XVtx");
c1->SaveAs(strcat(outputname,".png"));

CUT_V0_YVTX->Scale(1000/MC_Lumin/2);
DATA_CUT_MollerYVTX->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_MollerYVTX->Scale(1000/PURE_Lumin/2);
CUT_V0_YVTX->Write();
DATA_CUT_MollerYVTX->Write();
YVtx->Add(CUT_V0_YVTX);
YVtx->Add(DATA_CUT_MollerYVTX);
YVtx->Add(PURE_CUT_MollerYVTX);
YVtx->Write();
YVtx->Draw("nostack");
strcpy(outputname,"ALL_YVtx");
c1->SaveAs(strcat(outputname,".png"));

CUT_V0_ZVTX->Scale(1000/MC_Lumin/2);
DATA_CUT_MollerZVTX->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_MollerZVTX->Scale(1000/PURE_Lumin/2);
CUT_V0_ZVTX->Write();
DATA_CUT_MollerZVTX->Write();
ZVtx->Add(CUT_V0_ZVTX);
ZVtx->Add(DATA_CUT_MollerZVTX);
ZVtx->Add(PURE_CUT_MollerZVTX);
ZVtx->Write();
ZVtx->Draw("nostack");
strcpy(outputname,"ALL_ZVtx");
c1->SaveAs(strcat(outputname,".png"));

CUT_V0_coincidence->Scale(1000/MC_Lumin/2);
DATA_CUT_V0_coincidence->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_CUT_V0_coincidence->Scale(1000/PURE_Lumin/2);
CUT_V0_coincidence->Write();
DATA_CUT_V0_coincidence->Write();
ClusterCoincidence->Add(CUT_V0_coincidence);
ClusterCoincidence->Add(DATA_CUT_V0_coincidence);
ClusterCoincidence->Add(PURE_CUT_V0_coincidence);
ClusterCoincidence->Write();
ClusterCoincidence->Draw("nostack");
strcpy(outputname,"ALL_Coincidence");
c1->SaveAs(strcat(outputname,".png"));

coplanarity->Scale(1000/MC_Lumin/2);
DATA_coplanarity->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_coplanarity->Scale(1000/PURE_Lumin/2);
//CUT_V0_coincidence->Write();
//DATA_Coplanarity->Write();
ClusterCoplanarity->Add(coplanarity);
ClusterCoplanarity->Add(DATA_coplanarity);
ClusterCoplanarity->Add(PURE_coplanarity);
ClusterCoplanarity->Write();
ClusterCoplanarity->Draw("nostack");
strcpy(outputname,"ALL_Coplanarity");
c1->SaveAs(strcat(outputname,".png"));

phiDiff->Scale(1000/MC_Lumin/2);
DATA_phiDiff->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_phiDiff->Scale(1000/PURE_Lumin/2);
phiDiff->Write();
DATA_phiDiff->Write();
PhiDiff->Add(phiDiff);
PhiDiff->Add(DATA_phiDiff);
PhiDiff->Add(PURE_phiDiff);
PhiDiff->Write();
PhiDiff->Draw("nostack");
strcpy(outputname,"ALL_PhiDiff");
c1->SaveAs(strcat(outputname,".png"));

hitxDiff->Scale(1000/MC_Lumin/2);
DATA_hitxDiff->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_hitxDiff->Scale(1000/PURE_Lumin/2);
HitXDiff->Add(hitxDiff);
HitXDiff->Add(DATA_hitxDiff);
HitXDiff->Add(PURE_hitxDiff);
HitXDiff->Write();
HitXDiff->Draw("nostack");
strcpy(outputname,"ALL_HitXDiff");
c1->SaveAs(strcat(outputname,".png"));

hityDiff->Scale(1000/MC_Lumin/2);
DATA_hityDiff->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_hityDiff->Scale(1000/PURE_Lumin/2);
HitYDiff->Add(hityDiff);
HitYDiff->Add(DATA_hityDiff);
HitYDiff->Add(PURE_hityDiff);
HitYDiff->Write();
HitYDiff->Draw("nostack");
strcpy(outputname,"ALL_HitYDiff");
c1->SaveAs(strcat(outputname,".png"));


CUT_trackChi2->Scale(1000/MC_Lumin/2);
DATA_TrackChi2->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_TrackChi2->Scale(1000/PURE_Lumin/2);
//CUT_V0_coincidence->Write();
//DATA_TrackChi2->Write();
TrackChi2->Add(CUT_trackChi2);
TrackChi2->Add(DATA_TrackChi2);
TrackChi2->Add(PURE_TrackChi2);
TrackChi2->Write();
TrackChi2->Draw("nostack");
strcpy(outputname,"ALL_TrackChi2");
c1->SaveAs(strcat(outputname,".png"));

CUT_vtxChi2->Scale(1000/MC_Lumin/2);
DATA_vtxChi2->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_vtxChi2->Scale(1000/PURE_Lumin/2);
CUT_vtxChi2->Write();
DATA_vtxChi2->Write();
VtxChi2->Add(CUT_vtxChi2);
VtxChi2->Add(DATA_vtxChi2);
VtxChi2->Add(PURE_vtxChi2);
VtxChi2->Write();
VtxChi2->Draw("nostack");
strcpy(outputname,"ALL_VtxChi2");
c1->SaveAs(strcat(outputname,".png"));

px->Scale(1000/MC_Lumin/2);
DATA_px->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_px->Scale(1000/PURE_Lumin/2);
px->Write();
DATA_px->Write();
Px->Add(px);
Px->Add(DATA_px);
Px->Add(PURE_px);
Px->Write();
Px->Draw("nostack");
strcpy(outputname,"ALL_Px");
c1->SaveAs(strcat(outputname,".png"));

py->Scale(1000/MC_Lumin/2);
DATA_py->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_py->Scale(1000/PURE_Lumin/2);
py->Write();
DATA_py->Write();
Py->Add(py);
Py->Add(DATA_py);
Py->Add(PURE_py);
Py->Write();
Py->Draw("nostack");
strcpy(outputname,"ALL_Py");
c1->SaveAs(strcat(outputname,".png"));

pz->Scale(1000/MC_Lumin/2);
DATA_pz->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_pz->Scale(1000/PURE_Lumin/2);
pz->Write();
DATA_pz->Write();
Pz->Add(pz);
Pz->Add(DATA_pz);
Pz->Add(PURE_pz);
Pz->Write();
Pz->Draw("nostack");
strcpy(outputname,"ALL_Pz");
c1->SaveAs(strcat(outputname,".png"));

tanLambda->Scale(1000/MC_Lumin/2);
DATA_tanLambda->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_tanLambda->Scale(1000/PURE_Lumin/2);
TanLambda->Write();
DATA_tanLambda->Write();
TanLambda->Add(tanLambda);
TanLambda->Add(DATA_tanLambda);
TanLambda->Add(PURE_tanLambda);
TanLambda->Write();
TanLambda->Draw("nostack");
strcpy(outputname,"ALL_tanLambda");
c1->SaveAs(strcat(outputname,".png"));

//TrackEGap->Add(eventsTrackE);
//TrackEGap->Add(TRACK_V0_E);
//TrackEGap->Draw("nostack");
//strcpy(outputname,"TrackEGap");
//c1->SaveAs(strcat(outputname,".png"));

eventsTrackE->Scale(1000/MC_Lumin/2);
DATA_eventsTrackE->Scale(DATA_Prescale*1000/DATA_Lumin);
PURE_eventsTrackE->Scale(1000/PURE_Lumin/2);
eventTrackE->Add(eventsTrackE);
eventTrackE->Add(DATA_eventsTrackE);
eventTrackE->Add(PURE_eventsTrackE);
eventTrackE->Draw("nostack");
strcpy(outputname,"ALL_eventTrackE");
c1->SaveAs(strcat(outputname,".png"));





//fsESum->Add(fs_ESum);
//fsESum->Add(DATA_fs_ESum);
//fsESum->Draw("nostack");
//strcpy(outputname,"fsESum");
//c1->SaveAs(strcat(outputname,".png"));


////////////////////////////////////////////////////////////////////////////

//      moller_thetaE->Draw("COLZ");
//      strcpy(outputname,"RAW_moller_ThetaE");
//      c1->SaveAs(strcat(outputname,".png"));

    //  unrot_moller_thetaE->Draw("COLZ");
    //  strcpy(outputname,"RAW_Unrotmoller_ThetaE");
    //  c1->SaveAs(strcat(outputname,".png"));

    //  moller_E->Draw("COLZ");
    //  strcpy(outputname,"RAW_moller_E");
    //  c1->SaveAs(strcat(outputname,".png"));

      FIDUCIAL_V0_E->Write();
      FIDUCIAL_V0_E->Draw("COLZ");
      strcpy(outputname,"FIDUCIAL_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      EDGE_V0_E->Write();
      EDGE_V0_E->Draw("COLZ");
      strcpy(outputname,"EDGE_Energy");
      c1->SaveAs(strcat(outputname,".png"));


      moller_Theta->Draw("COLZ");
      strcpy(outputname,"RAW_moller_Theta");
      c1->SaveAs(strcat(outputname,".png"));

      moller_ESum->Draw("COLZ");
      strcpy(outputname,"RAW_moller_ESum");
      c1->SaveAs(strcat(outputname,".png"));
  
      ESumMass->Draw("COLZ");
      strcpy(outputname,"ESumMass");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_ESumMass->Draw("COLZ");
      strcpy(outputname,"DATA_ESumMass");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_ESumMass->Draw("COLZ");
      strcpy(outputname,"PURE_ESumMass");
      c1->SaveAs(strcat(outputname,".png"));
   
     // ETTest->Fit("gaus");
   //   ETTest->Draw("COLZ");
   //   strcpy(outputname,"RAW_ETTest");
   //   c1->SaveAs(strcat(outputname,".png"));

    //  MollerEE->Draw("COLZ");
    //  strcpy(outputname,"RAW_mollerEE");
    //  c1->SaveAs(strcat(outputname,".png"));

    //  MollerTT->Draw("COLZ");
    //  strcpy(outputname,"RAW_mollerTT");
    //  c1->SaveAs(strcat(outputname,".png"));

    //  moller_coincidence->Draw("COLZ");
    //  strcpy(outputname,"RAW_mollerCoincidence");
    //  c1->SaveAs(strcat(outputname,".png"));

   //   DATA_CUT_V0_coincidence->Write();
      DATA_CUT_V0_coincidence->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_V0Coincidence");
      c1->SaveAs(strcat(outputname,".png"));

      hitTime->Draw("COLZ");
      strcpy(outputname,"hitTime");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_hitTime->Draw("COLZ");
      strcpy(outputname,"DATA_hitTime");
      c1->SaveAs(strcat(outputname,".png"));

    //  SinSinTest->Draw("COLZ");
    //  strcpy(outputname,"RAW_SinSinTest");
    //  c1->SaveAs(strcat(outputname,".png"));

    //  moller_EP->Draw("COLZ");
    //  strcpy(outputname,"RAW_mollerEP");
    //  c1->SaveAs(strcat(outputname,".png"));

// Moller E,T,TE ///////////
    //  CUT_moller_thetaE->Draw("COLZ");
    //  strcpy(outputname,"CUT_moller_ThetaE");
     /// c1->SaveAs(strcat(outputname,".png"));

      CUT_unrot_V0_thetaE->Scale(1000/MC_Lumin/2);
      CUT_unrot_V0_thetaE->Draw("COLZ");
      strcpy(outputname,"CUT_Unrotmoller_ThetaE");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0_E->Write();
      TRACK_V0_E->Draw("COLZ");
    //  XS->Draw("SAME");
    //  XS2->Draw("SAME");
      strcpy(outputname,"TRACK_Energy");
      c1->SaveAs(strcat(outputname,".C"));

      EDGE_TRACK_V0_E->Write();
      EDGE_TRACK_V0_E->Draw("COLZ");
      strcpy(outputname,"EDGE_TRACK_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      FIDUCIAL_TRACK_V0_E->Write();
      FIDUCIAL_TRACK_V0_E->Draw("COLZ");
      strcpy(outputname,"FIDUCIAL_TRACK_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      //E->Write();
      eventsTrackE->Write();
      eventsTrackE->Draw("COLZ");
      strcpy(outputname,"eventsTrackE");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0_E1->Write();
      TRACK_V0_E1->Draw("COLZ");
      strcpy(outputname,"TOP_TRACK_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0_E2->Write();
      TRACK_V0_E2->Draw("COLZ");
      strcpy(outputname,"BOTTOM_TRACK_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      CLUSTER_V0_E->Write();
      CLUSTER_V0_E->Draw("COLZ");
      strcpy(outputname,"CLUSTER_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      CLUSTER_V0_E1->Write();
      CLUSTER_V0_E1->Draw("COLZ");
      strcpy(outputname,"TOP_CLUSTER_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      CLUSTER_V0_E2->Write();
      CLUSTER_V0_E2->Draw("COLZ");
      strcpy(outputname,"BOTTOM_CLUSTER_Energy");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_V0_Theta->Draw("COLZ");
      strcpy(outputname,"CUT_Theta");
      c1->SaveAs(strcat(outputname,".png"));

      //DATA_CUT_moller_thetaE->Draw("COLZ");
      //strcpy(outputname,"DATA_CUT_moller_ThetaE");
      //c1->SaveAs(strcat(outputname,".png"));

      DATA_CUT_unrot_moller_thetaE->Scale(DATA_Prescale*1000/DATA_Lumin/74/2);
      DATA_CUT_unrot_moller_thetaE->Write();
      DATA_CUT_unrot_moller_thetaE->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_Unrotmoller_ThetaE");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_CUT_unrot_moller_thetaE->Scale(1000/PURE_Lumin/2); 
      PURE_CUT_unrot_moller_thetaE->Write();
      PURE_CUT_unrot_moller_thetaE->Draw("COLZ");
      strcpy(outputname,"PURE_CUT_Unrotmoller_ThetaE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_TrackE->Draw("COLZ");
      strcpy(outputname,"DATA_TrackE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_ClusterE->Draw("COLZ");
      strcpy(outputname,"DATA_ClusterE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_CUT_moller_Theta->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_moller_Theta");
     c1->SaveAs(strcat(outputname,".png"));

/// Moller Tests /////////////
      TRACK_V0_ESum->Write();
      TRACK_V0_ESum->Draw("COLZ");
      strcpy(outputname,"TRACK_ESum");
      c1->SaveAs(strcat(outputname,".png"));

      CLUSTER_V0_ESum->Write();
      CLUSTER_V0_ESum->Draw("COLZ");
      strcpy(outputname,"CLUSTER_ESum");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0_EDiff->Draw("COLZ");
      strcpy(outputname,"TRACK_EDiff");
      c1->SaveAs(strcat(outputname,".png"));

      CLUSTER_V0_EDiff->Draw("COLZ");
      strcpy(outputname,"CLUSTER_EDiff");
      c1->SaveAs(strcat(outputname,".png"));

      FIDUCIAL_V0_ESum->Write();
      FIDUCIAL_V0_ESum->Draw("COLZ");
      strcpy(outputname,"FIDUCIAL_ESum");
      c1->SaveAs(strcat(outputname,".png"));

      EDGE_V0_ESum->Write();
      EDGE_V0_ESum->Draw("COLZ");
      strcpy(outputname,"EDGE_ESum");
      c1->SaveAs(strcat(outputname,".png"));

   //   CUT_ETTest->Fit("gaus");
   //   CUT_ETTest->Draw("COLZ");
   //   strcpy(outputname,"CUT_TestTE");
   //   c1->SaveAs(strcat(outputname,".png"));

      CUT_ESumE->Write();
      CUT_ESumE->Draw("COLZ");
      strcpy(outputname,"TRACK_EsumE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_ESumE->Write();
      DATA_ESumE->Draw("COLZ");
      strcpy(outputname,"DATA_EsumE");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_ESumE->Write();
      PURE_ESumE->Draw("COLZ");
      strcpy(outputname,"PURE_EsumE");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_ESumE1->Write();
      CUT_ESumE1->Draw("COLZ");
      strcpy(outputname,"TRACK_EsumE1");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_ESumE2->Write();
      CUT_ESumE2->Draw("COLZ");
      strcpy(outputname,"TRACK_EsumE2");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0EE->Draw("COLZ");
      strcpy(outputname,"TRACK_PlotEE");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0EE_FIDUCIAL->Draw("COLZ");
      strcpy(outputname,"TRACK_PlotEE_FIDUCIAL");
      c1->SaveAs(strcat(outputname,".png"));

      TRACK_V0EE_EDGE->Draw("COLZ");
      strcpy(outputname,"TRACK_PlotEE_EDGE");
      c1->SaveAs(strcat(outputname,".png"));

      CLUSTER_V0EE->Draw("COLZ");
      strcpy(outputname,"CLUSTER_PlotEE");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_V0TT->Draw("COLZ");
      strcpy(outputname,"CUT_PlotTT");
      c1->SaveAs(strcat(outputname,".png"));

     // DATA_CUT_MollerEE->Draw("COLZ");
     // strcpy(outputname,"DATA_CUT_PlotEE");
     // c1->SaveAs(strcat(outputname,".png"));

      DATA_CUT_MollerTT->Scale(DATA_Prescale*1000/DATA_Lumin/74/2);
      DATA_CUT_MollerTT->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_PlotTT");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_CUT_MollerTT->Scale(1000/PURE_Lumin/2);
      PURE_CUT_MollerTT->Draw("COLZ");
      strcpy(outputname,"PURE_CUT_PlotTT");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_V0_coincidence->Write();
      CUT_V0_coincidence->Draw("COLZ");
      strcpy(outputname,"CUT_Coincidence");
      c1->SaveAs(strcat(outputname,".png"));
    
  //    CUT_SinSinTest->Fit("gaus");
   //   CUT_SinSinTest->Draw("COLZ");
   //   strcpy(outputname,"CUT_TestTT");
   //   c1->SaveAs(strcat(outputname,".png"));

      DATA_TrackEE->Draw("COLZ");
      strcpy(outputname,"DATA_TrackEE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_ClusterEE->Draw("COLZ");
      strcpy(outputname,"DATA_ClusterEE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_moller_ESum->Draw("COLZ");
      strcpy(outputname,"DATA_TestEE");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_ETTest->Fit("gaus");
      DATA_CUT_ETTest->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_TestTE");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_TRACK_ESum->Draw("COLZ");
      strcpy(outputname,"DATA_TrackESum");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_CLUSTER_ESum->Draw("COLZ");
      strcpy(outputname,"DATA_ClusterESum");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_CUT_MollerTT->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_PlotTT");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_CUT_V0_coincidence->Write();
      DATA_CUT_V0_coincidence->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_V0Coincidence");
      c1->SaveAs(strcat(outputname,".png"));

      seed_E->Draw("COLZ");
      strcpy(outputname,"DATA_SeedE");
      c1->SaveAs(strcat(outputname,".png"));

      energy_slope->Draw("COLZ");
      strcpy(outputname,"DATA_EnergySlope");
      c1->SaveAs(strcat(outputname,".png"));


      CUT_SinSinTest->Fit("gaus");
      DATA_CUT_SinSinTest->Draw("COLZ");
      strcpy(outputname,"DATA_CUT_TestTT");
     c1->SaveAs(strcat(outputname,".png"));


      // Energy Momentum
      CUT_V0_EP->Scale(1000/MC_Lumin/2);
      CUT_V0_EP->Draw("COLZ");
      strcpy(outputname,"CUT_EP");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_EP->Scale(DATA_Prescale*1000/DATA_Lumin/74/2);
      DATA_EP->Draw("COLZ");
      strcpy(outputname,"DATA_EP");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_EP->Scale(1000/PURE_Lumin/2);
      PURE_EP->Draw("COLZ");
      strcpy(outputname,"PURE_EP");
      c1->SaveAs(strcat(outputname,".png"));

      ECal_hits->Draw("COLZ");
      strcpy(outputname,"ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));

      neg_hits->Draw("COLZ");
      strcpy(outputname,"HitsFromLowEClust");
      c1->SaveAs(strcat(outputname,".png"));

      pos_hits->Draw("COLZ");
      strcpy(outputname,"HitsFromHighEClust");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_neg_hits->Draw("COLZ");
      strcpy(outputname,"HitsFromLowEClust_DATA");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_pos_hits->Draw("COLZ");
      strcpy(outputname,"HitsFromHighEClust_DATA");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_neg_hits->Draw("COLZ");
      strcpy(outputname,"HitsFromLowEClust_PURE");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_pos_hits->Draw("COLZ");
      strcpy(outputname,"HitsFromHighEClust_PURE");
      c1->SaveAs(strcat(outputname,".png"));

  //    WTF_gap->Draw("COLZ");
  //    strcpy(outputname,"WTF_gap");
  //    c1->SaveAs(strcat(outputname,".png"));

  //    GapTrackE->Draw("COLZ");
  //    strcpy(outputname,"GapTrackE");
  //    c1->SaveAs(strcat(outputname,".png"));

      CUT_FIDUCIAL_ECal_hits->Draw("COLZ");
      strcpy(outputname,"FIDUCIAL_ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_ECal_seedHits->Draw("COLZ");
      strcpy(outputname,"SeedHits");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_EDGE_ECal_hits->Draw("COLZ");
      strcpy(outputname,"EDGE_ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_ECal_hits->Draw("COLZ");
      strcpy(outputname,"ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_FIDUCIAL_ECal_hits->Draw("COLZ");
      strcpy(outputname,"DATA_FIDUCIAL_ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_ECal_seedHits->Draw("COLZ");
      strcpy(outputname,"DATA_SeedHits");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_EDGE_ECal_hits->Draw("COLZ");
      strcpy(outputname,"DATA_EDGE_ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_ECal_hits->Draw("COLZ");
      strcpy(outputname,"DATA_ECal_hits");
      c1->SaveAs(strcat(outputname,".png"));



  //      CUT_ECalMollers4Calib->Draw("COLZ");
  //      strcpy(outputname,"CUT_ECalMollers4Calib");
  //      c1->SaveAs(strcat(outputname,".png"));


      CUT_V0_XVTX->Draw("COLZ");
      strcpy(outputname,"CUTmollerXVTX");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_V0_YVTX->Draw("COLZ");
      strcpy(outputname,"CUTmollerYVTX");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_V0_ZVTX->Draw("COLZ");
      strcpy(outputname,"CUTmollerZVTX");
      c1->SaveAs(strcat(outputname,".png"));

  //      V0_Mass->Draw("COLZ");
  //      strcpy(outputname,"RAW_InvarMass");
  //      c1->SaveAs(strcat(outputname,".png"));

        CUT_V0_Mass->Draw("COLZ");
        strcpy(outputname,"CUT_InvarMass");
        c1->SaveAs(strcat(outputname,".png"));

        DATA_Mass->Draw("COLZ");
        strcpy(outputname,"DATA_CUT_InvarMass");
        c1->SaveAs(strcat(outputname,".png"));

     //   trackChi2->Draw("COLZ");
     //   strcpy(outputname,"trackChi2");
     //   c1->SaveAs(strcat(outputname,".png"));
 
  //      vtxChi2->Draw("COLZ");
   //     strcpy(outputname,"vtxChi2");
   //     c1->SaveAs(strcat(outputname,".png"));

     //   CUT_trackChi2->Draw("COLZ");
     //   strcpy(outputname,"CUT_trackChi2");
     //   c1->SaveAs(strcat(outputname,".png"));

     //   CUT_vtxChi2->Draw("COLZ");
     //   strcpy(outputname,"CUT_vtxChi2");
      //  c1->SaveAs(strcat(outputname,".png"));

        coplanarity->Write();
        coplanarity->Draw("COLZ");
        strcpy(outputname,"coplanarity");
        c1->SaveAs(strcat(outputname,".png"));

        DATA_coplanarity->Draw("COLZ");
        strcpy(outputname,"DATA_coplanarity");
        c1->SaveAs(strcat(outputname,".png"));

      //  VtxTrackChi2_1->Write();
        VtxTrackChi2_1->Draw("COLZ");
        strcpy(outputname,"VtxTrackChi2_1");
        c1->SaveAs(strcat(outputname,".png"));

        VtxTrackChi2_2->Draw("COLZ");
        strcpy(outputname,"VtxTrackChi2_2");
        c1->SaveAs(strcat(outputname,".png"));


//// ECal Stuff ////////////////////////////////////

      CUT_EPRatio->Write();
      CUT_EPRatio->Draw("COLZ");
      strcpy(outputname,"EP_Ratio");
      c1->SaveAs(strcat(outputname,".png"));

    //  DATA_CUT_EPRatio->Write();
    //  DATA_CUT_EPRatio->Draw("COLZ");
    //  strcpy(outputname,"DATA_EP_Ratio");
    //  c1->SaveAs(strcat(outputname,".png"));

    //  PURE_CUT_EPRatio->Write();
    //  PURECUT_EPRatio->Draw("COLZ");
    //  strcpy(outputname,"EP_Ratio");
    //  c1->SaveAs(strcat(outputname,".png"));

//      CUT_EDGE_MolCan_EPRatio->Fit("gaus");
      CUT_EDGE_V0_EPRatio->Write();
      CUT_EDGE_V0_EPRatio->Draw("COLZ");
      strcpy(outputname,"EDGE_EP");
      c1->SaveAs(strcat(outputname,".png"));

  //    CUT_FIDUCIAL_MolCan_EPRatio->Fit("gaus");
      CUT_FIDUCIAL_V0_EPRatio->Draw("COLZ");
      strcpy(outputname,"FIDUCIAL_EPRatio");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_FIDUCIAL_V0_EP->Draw("COLZ");
      strcpy(outputname,"FIDUCIAL_EP");
      c1->SaveAs(strcat(outputname,".png"));

 //     CUT_EDGE_MolCan_EPRatio->Fit("gaus");
      CUT_EDGE_V0_EPRatio->Draw("COLZ");
      strcpy(outputname,"EDGE_EPRatio");
      c1->SaveAs(strcat(outputname,".png"));

      CUT_EDGE_V0_EP->Draw("COLZ");
      strcpy(outputname,"EDGE_EP");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_EDGE_Moller_EP->Draw("COLZ");
      strcpy(outputname,"DATA_EDGE_EP");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_FIDUCIAL_Moller_EP->Draw("COLZ");
      strcpy(outputname,"DATA_FIDUCIAL_EP");
      c1->SaveAs(strcat(outputname,".png"));

      phi0->Draw("COLZ");
      strcpy(outputname,"phi0");
      c1->SaveAs(strcat(outputname,".png"));

      phiDiff->Draw("COLZ");
      strcpy(outputname,"phiDiff");
      c1->SaveAs(strcat(outputname,".png"));

      phi1phi2->Draw("COLZ");
      strcpy(outputname,"phi1phi2");
      c1->SaveAs(strcat(outputname,".png"));

//      hitxDiff->Draw("COLZ");
//      strcpy(outputname,"hitxDiff");
//      c1->SaveAs(strcat(outputname,".png"));

//      hityDiff->Draw("COLZ");
//      strcpy(outputname,"hityDiff");
//      c1->SaveAs(strcat(outputname,".png"));

      tracksAtEcal->Scale(1000/MC_Lumin/2);
      tracksAtEcal->Draw("COLZ");
      strcpy(outputname,"tracksAtEcal");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_tracksAtEcal->Scale(DATA_Prescale*1000/DATA_Lumin/74/2);
      DATA_tracksAtEcal->Draw("COLZ");
      strcpy(outputname,"tracksAtEcal_DATA");
      c1->SaveAs(strcat(outputname,".png"));

      PURE_tracksAtEcal->Draw("COLZ");
      strcpy(outputname,"tracksAtEcal_PURE");
      c1->SaveAs(strcat(outputname,".png"));

      pT1pT2->Draw("COLZ");
      strcpy(outputname,"pT1pT2");
      c1->SaveAs(strcat(outputname,".png"));

      pTDiff->Draw("COLZ");
      strcpy(outputname,"pTDiff");
      c1->SaveAs(strcat(outputname,".png"));

      L1->Draw("COLZ");
      strcpy(outputname,"L1");
      c1->SaveAs(strcat(outputname,".png"));

      L2->Draw("COLZ");
      strcpy(outputname,"L2");
      c1->SaveAs(strcat(outputname,".png"));

      L3->Draw("COLZ");
      strcpy(outputname,"L3");
      c1->SaveAs(strcat(outputname,".png"));

      L4->Draw("COLZ");
      strcpy(outputname,"L4");
      c1->SaveAs(strcat(outputname,".png"));

      L5->Draw("COLZ");
      strcpy(outputname,"L5");
      c1->SaveAs(strcat(outputname,".png"));

      L6->Draw("COLZ");
      strcpy(outputname,"L6");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_L1->Draw("COLZ");
      strcpy(outputname,"DATA_L1");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_L2->Draw("COLZ");
      strcpy(outputname,"DATA_L2");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_L3->Draw("COLZ");
      strcpy(outputname,"DATA_L3");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_L4->Draw("COLZ");
      strcpy(outputname,"DATA_L4");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_L5->Draw("COLZ");
      strcpy(outputname,"DATA_L5");
      c1->SaveAs(strcat(outputname,".png"));

      DATA_L6->Draw("COLZ");
      strcpy(outputname,"DATA_L6");
      c1->SaveAs(strcat(outputname,".png"));

}
