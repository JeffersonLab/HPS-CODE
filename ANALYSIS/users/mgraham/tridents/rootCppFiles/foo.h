//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Aug  4 12:50:49 2015 by ROOT version 5.34/26
// from TTree HPS_Event/HPS event tree
// found on file: ../../EngRun2015/pass1/dst/hps_005772.10_dst_R3321.root
//////////////////////////////////////////////////////////

#ifndef foo_h
#define foo_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/HpsEvent.h"
#include <TObject.h>
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/SvtTrack.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/SvtHit.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/EcalCluster.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/EcalHit.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/HpsParticle.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/HpsMCParticle.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/GblTrack.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/GblTrackData.h"
#include "/u/br/omoreno/hps3/software/hps-dst/include/hps_event/GblStripData.h"
#include <TVector3.h>

// Fixed size dimensions of array or collections stored in the TTree if any.
   const Int_t kMaxtracks = 19;
   const Int_t kMaxsvt_hits = 103;
   const Int_t kMaxecal_clusters = 11;
   const Int_t kMaxecal_hits = 44;
   const Int_t kMaxfs_particles = 21;
   const Int_t kMaxuc_vtx_particles = 88;
   const Int_t kMaxbsc_vtx_particles = 88;
   const Int_t kMaxtc_vtx_particles = 88;
   const Int_t kMaxmc_particles = 1;
   const Int_t kMaxgbl_tracks = 1;
   const Int_t kMaxgbl_tracks_data = 1;
   const Int_t kMaxgbl_strips_data = 1;

class foo {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
 //HpsEvent        *Event;
   UInt_t          fUniqueID;
   UInt_t          fBits;
   Int_t           tracks_;
   UInt_t          tracks_fUniqueID[kMaxtracks];   //[tracks_]
   UInt_t          tracks_fBits[kMaxtracks];   //[tracks_]
   TRef            tracks_fs_particle[kMaxtracks];
   Int_t           tracks_n_hits[kMaxtracks];   //[tracks_]
   Int_t           tracks_track_volume[kMaxtracks];   //[tracks_]
   Double_t        tracks_d0[kMaxtracks];   //[tracks_]
   Double_t        tracks_phi0[kMaxtracks];   //[tracks_]
   Double_t        tracks_omega[kMaxtracks];   //[tracks_]
   Double_t        tracks_tan_lambda[kMaxtracks];   //[tracks_]
   Double_t        tracks_z0[kMaxtracks];   //[tracks_]
   Double_t        tracks_chi_squared[kMaxtracks];   //[tracks_]
   Double_t        tracks_track_time[kMaxtracks];   //[tracks_]
   Double_t        tracks_l1_isolation[kMaxtracks];   //[tracks_]
   Double_t        tracks_l2_isolation[kMaxtracks];   //[tracks_]
   Int_t           svt_hits_;
   UInt_t          svt_hits_fUniqueID[kMaxsvt_hits];   //[svt_hits_]
   UInt_t          svt_hits_fBits[kMaxsvt_hits];   //[svt_hits_]
   Int_t           svt_hits_layer[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_x[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_y[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_z[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_cxx[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_cxy[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_cxz[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_cyy[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_cyz[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_czz[kMaxsvt_hits];   //[svt_hits_]
   Double_t        svt_hits_time[kMaxsvt_hits];   //[svt_hits_]
   Int_t           ecal_clusters_;
   UInt_t          ecal_clusters_fUniqueID[kMaxecal_clusters];   //[ecal_clusters_]
   UInt_t          ecal_clusters_fBits[kMaxecal_clusters];   //[ecal_clusters_]
   TRef            ecal_clusters_seed_hit[kMaxecal_clusters];
   Int_t           ecal_clusters_n_ecal_hits[kMaxecal_clusters];   //[ecal_clusters_]
   Double_t        ecal_clusters_x[kMaxecal_clusters];   //[ecal_clusters_]
   Double_t        ecal_clusters_y[kMaxecal_clusters];   //[ecal_clusters_]
   Double_t        ecal_clusters_z[kMaxecal_clusters];   //[ecal_clusters_]
   Double_t        ecal_clusters_energy[kMaxecal_clusters];   //[ecal_clusters_]
   Double_t        ecal_clusters_cluster_time[kMaxecal_clusters];   //[ecal_clusters_]
   Int_t           ecal_hits_;
   UInt_t          ecal_hits_fUniqueID[kMaxecal_hits];   //[ecal_hits_]
   UInt_t          ecal_hits_fBits[kMaxecal_hits];   //[ecal_hits_]
   Int_t           ecal_hits_index_x[kMaxecal_hits];   //[ecal_hits_]
   Int_t           ecal_hits_index_y[kMaxecal_hits];   //[ecal_hits_]
   Double_t        ecal_hits_energy[kMaxecal_hits];   //[ecal_hits_]
   Double_t        ecal_hits_hit_time[kMaxecal_hits];   //[ecal_hits_]
   Int_t           fs_particles_;
   UInt_t          fs_particles_fUniqueID[kMaxfs_particles];   //[fs_particles_]
   UInt_t          fs_particles_fBits[kMaxfs_particles];   //[fs_particles_]
   Int_t           fs_particles_n_daughters[kMaxfs_particles];   //[fs_particles_]
   Int_t           fs_particles_charge[kMaxfs_particles];   //[fs_particles_]
   Int_t           fs_particles_pdg[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_px[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_py[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_pz[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_vtx_x[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_vtx_y[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_vtx_z[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_vtx_fit_chi2[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_energy[kMaxfs_particles];   //[fs_particles_]
   Double_t        fs_particles_mass[kMaxfs_particles];   //[fs_particles_]
   Int_t           uc_vtx_particles_;
   UInt_t          uc_vtx_particles_fUniqueID[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   UInt_t          uc_vtx_particles_fBits[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Int_t           uc_vtx_particles_n_daughters[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Int_t           uc_vtx_particles_charge[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Int_t           uc_vtx_particles_pdg[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_px[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_py[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_pz[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_vtx_x[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_vtx_y[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_vtx_z[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_vtx_fit_chi2[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_energy[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Double_t        uc_vtx_particles_mass[kMaxuc_vtx_particles];   //[uc_vtx_particles_]
   Int_t           bsc_vtx_particles_;
   UInt_t          bsc_vtx_particles_fUniqueID[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   UInt_t          bsc_vtx_particles_fBits[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Int_t           bsc_vtx_particles_n_daughters[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Int_t           bsc_vtx_particles_charge[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Int_t           bsc_vtx_particles_pdg[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_px[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_py[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_pz[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_vtx_x[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_vtx_y[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_vtx_z[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_vtx_fit_chi2[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_energy[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Double_t        bsc_vtx_particles_mass[kMaxbsc_vtx_particles];   //[bsc_vtx_particles_]
   Int_t           tc_vtx_particles_;
   UInt_t          tc_vtx_particles_fUniqueID[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   UInt_t          tc_vtx_particles_fBits[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Int_t           tc_vtx_particles_n_daughters[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Int_t           tc_vtx_particles_charge[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Int_t           tc_vtx_particles_pdg[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_px[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_py[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_pz[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_vtx_x[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_vtx_y[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_vtx_z[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_vtx_fit_chi2[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_energy[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Double_t        tc_vtx_particles_mass[kMaxtc_vtx_particles];   //[tc_vtx_particles_]
   Int_t           mc_particles_;
   UInt_t          mc_particles_fUniqueID[kMaxmc_particles];   //[mc_particles_]
   UInt_t          mc_particles_fBits[kMaxmc_particles];   //[mc_particles_]
   Int_t           mc_particles_pdg[kMaxmc_particles];   //[mc_particles_]
   Int_t           mc_particles_charge[kMaxmc_particles];   //[mc_particles_]
   Int_t           mc_particles_generator_status[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_energy[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_mass[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_px[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_py[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_pz[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_endpt_x[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_endpt_y[kMaxmc_particles];   //[mc_particles_]
   Double_t        mc_particles_endpt_z[kMaxmc_particles];   //[mc_particles_]
   Int_t           gbl_tracks_;
   UInt_t          gbl_tracks_fUniqueID[kMaxgbl_tracks];   //[gbl_tracks_]
   UInt_t          gbl_tracks_fBits[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_kappa[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_theta[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_phi[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_d0[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_z0[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_seed_kappa[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_seed_theta[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_seed_phi[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_seed_d0[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_seed_z0[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_chi2[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_ndf[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_px[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_py[kMaxgbl_tracks];   //[gbl_tracks_]
   Double_t        gbl_tracks_pz[kMaxgbl_tracks];   //[gbl_tracks_]
   TMatrixT<double> gbl_tracks_cov[kMaxgbl_tracks];
   Int_t           gbl_tracks_data_;
   UInt_t          gbl_tracks_data_fUniqueID[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   UInt_t          gbl_tracks_data_fBits[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   TRef            gbl_tracks_data_svt_track[kMaxgbl_tracks_data];
   TMatrixT<double> gbl_tracks_data_m_prjPerToCl[kMaxgbl_tracks_data];
   Int_t           gbl_tracks_data_n_gbl_strip_hits[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   Double_t        gbl_tracks_data_m_kappa[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   Double_t        gbl_tracks_data_m_theta[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   Double_t        gbl_tracks_data_m_phi[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   Double_t        gbl_tracks_data_m_d0[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   Double_t        gbl_tracks_data_m_z0[kMaxgbl_tracks_data];   //[gbl_tracks_data_]
   Int_t           gbl_strips_data_;
   UInt_t          gbl_strips_data_fUniqueID[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_fBits[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Int_t           gbl_strips_data_m_id[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_path3D[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_path[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_u_fUniqueID[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_u_fBits[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_u_fX[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_u_fY[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_u_fZ[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_v_fUniqueID[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_v_fBits[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_v_fX[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_v_fY[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_v_fZ[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_w_fUniqueID[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_w_fBits[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_w_fX[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_w_fY[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_w_fZ[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_tdir_global_fUniqueID[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_tdir_global_fBits[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tdir_global_fX[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tdir_global_fY[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tdir_global_fZ[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tphi[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_tpos_fUniqueID[kMaxgbl_strips_data];   //[gbl_strips_data_]
   UInt_t          gbl_strips_data_m_tpos_fBits[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tpos_fX[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tpos_fY[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_tpos_fZ[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_phi[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_lambda[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_umeas[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_umeas_err[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Double_t        gbl_strips_data_m_ms_angle[kMaxgbl_strips_data];   //[gbl_strips_data_]
   Int_t           event_number;
   Int_t           run_number;
   Int_t           trigger_time_stamp;
   Int_t           single0_trigger;
   Int_t           single1_trigger;
   Int_t           pair0_trigger;
   Int_t           pair1_trigger;
   Int_t           pulser_trigger;
   Int_t           n_tracks;
   Int_t           n_svt_hits;
   Int_t           n_ecal_clusters;
   Int_t           n_ecal_hits;
   Int_t           n_fs_particles;
   Int_t           n_uc_vtx_particles;
   Int_t           n_bsc_vtx_particles;
   Int_t           n_tc_vtx_particles;
   Int_t           n_mc_particles;
   Int_t           n_gbl_tracks;
   Int_t           n_gbl_tracks_data;
   Int_t           n_gbl_strips_data;

   // List of branches
   TBranch        *b_Event_fUniqueID;   //!
   TBranch        *b_Event_fBits;   //!
   TBranch        *b_Event_tracks_;   //!
   TBranch        *b_tracks_fUniqueID;   //!
   TBranch        *b_tracks_fBits;   //!
   TBranch        *b_tracks_fs_particle;   //!
   TBranch        *b_tracks_n_hits;   //!
   TBranch        *b_tracks_track_volume;   //!
   TBranch        *b_tracks_d0;   //!
   TBranch        *b_tracks_phi0;   //!
   TBranch        *b_tracks_omega;   //!
   TBranch        *b_tracks_tan_lambda;   //!
   TBranch        *b_tracks_z0;   //!
   TBranch        *b_tracks_chi_squared;   //!
   TBranch        *b_tracks_track_time;   //!
   TBranch        *b_tracks_l1_isolation;   //!
   TBranch        *b_tracks_l2_isolation;   //!
   TBranch        *b_Event_svt_hits_;   //!
   TBranch        *b_svt_hits_fUniqueID;   //!
   TBranch        *b_svt_hits_fBits;   //!
   TBranch        *b_svt_hits_layer;   //!
   TBranch        *b_svt_hits_x;   //!
   TBranch        *b_svt_hits_y;   //!
   TBranch        *b_svt_hits_z;   //!
   TBranch        *b_svt_hits_cxx;   //!
   TBranch        *b_svt_hits_cxy;   //!
   TBranch        *b_svt_hits_cxz;   //!
   TBranch        *b_svt_hits_cyy;   //!
   TBranch        *b_svt_hits_cyz;   //!
   TBranch        *b_svt_hits_czz;   //!
   TBranch        *b_svt_hits_time;   //!
   TBranch        *b_Event_ecal_clusters_;   //!
   TBranch        *b_ecal_clusters_fUniqueID;   //!
   TBranch        *b_ecal_clusters_fBits;   //!
   TBranch        *b_ecal_clusters_seed_hit;   //!
   TBranch        *b_ecal_clusters_n_ecal_hits;   //!
   TBranch        *b_ecal_clusters_x;   //!
   TBranch        *b_ecal_clusters_y;   //!
   TBranch        *b_ecal_clusters_z;   //!
   TBranch        *b_ecal_clusters_energy;   //!
   TBranch        *b_ecal_clusters_cluster_time;   //!
   TBranch        *b_Event_ecal_hits_;   //!
   TBranch        *b_ecal_hits_fUniqueID;   //!
   TBranch        *b_ecal_hits_fBits;   //!
   TBranch        *b_ecal_hits_index_x;   //!
   TBranch        *b_ecal_hits_index_y;   //!
   TBranch        *b_ecal_hits_energy;   //!
   TBranch        *b_ecal_hits_hit_time;   //!
   TBranch        *b_Event_fs_particles_;   //!
   TBranch        *b_fs_particles_fUniqueID;   //!
   TBranch        *b_fs_particles_fBits;   //!
   TBranch        *b_fs_particles_n_daughters;   //!
   TBranch        *b_fs_particles_charge;   //!
   TBranch        *b_fs_particles_pdg;   //!
   TBranch        *b_fs_particles_px;   //!
   TBranch        *b_fs_particles_py;   //!
   TBranch        *b_fs_particles_pz;   //!
   TBranch        *b_fs_particles_vtx_x;   //!
   TBranch        *b_fs_particles_vtx_y;   //!
   TBranch        *b_fs_particles_vtx_z;   //!
   TBranch        *b_fs_particles_vtx_fit_chi2;   //!
   TBranch        *b_fs_particles_energy;   //!
   TBranch        *b_fs_particles_mass;   //!
   TBranch        *b_Event_uc_vtx_particles_;   //!
   TBranch        *b_uc_vtx_particles_fUniqueID;   //!
   TBranch        *b_uc_vtx_particles_fBits;   //!
   TBranch        *b_uc_vtx_particles_n_daughters;   //!
   TBranch        *b_uc_vtx_particles_charge;   //!
   TBranch        *b_uc_vtx_particles_pdg;   //!
   TBranch        *b_uc_vtx_particles_px;   //!
   TBranch        *b_uc_vtx_particles_py;   //!
   TBranch        *b_uc_vtx_particles_pz;   //!
   TBranch        *b_uc_vtx_particles_vtx_x;   //!
   TBranch        *b_uc_vtx_particles_vtx_y;   //!
   TBranch        *b_uc_vtx_particles_vtx_z;   //!
   TBranch        *b_uc_vtx_particles_vtx_fit_chi2;   //!
   TBranch        *b_uc_vtx_particles_energy;   //!
   TBranch        *b_uc_vtx_particles_mass;   //!
   TBranch        *b_Event_bsc_vtx_particles_;   //!
   TBranch        *b_bsc_vtx_particles_fUniqueID;   //!
   TBranch        *b_bsc_vtx_particles_fBits;   //!
   TBranch        *b_bsc_vtx_particles_n_daughters;   //!
   TBranch        *b_bsc_vtx_particles_charge;   //!
   TBranch        *b_bsc_vtx_particles_pdg;   //!
   TBranch        *b_bsc_vtx_particles_px;   //!
   TBranch        *b_bsc_vtx_particles_py;   //!
   TBranch        *b_bsc_vtx_particles_pz;   //!
   TBranch        *b_bsc_vtx_particles_vtx_x;   //!
   TBranch        *b_bsc_vtx_particles_vtx_y;   //!
   TBranch        *b_bsc_vtx_particles_vtx_z;   //!
   TBranch        *b_bsc_vtx_particles_vtx_fit_chi2;   //!
   TBranch        *b_bsc_vtx_particles_energy;   //!
   TBranch        *b_bsc_vtx_particles_mass;   //!
   TBranch        *b_Event_tc_vtx_particles_;   //!
   TBranch        *b_tc_vtx_particles_fUniqueID;   //!
   TBranch        *b_tc_vtx_particles_fBits;   //!
   TBranch        *b_tc_vtx_particles_n_daughters;   //!
   TBranch        *b_tc_vtx_particles_charge;   //!
   TBranch        *b_tc_vtx_particles_pdg;   //!
   TBranch        *b_tc_vtx_particles_px;   //!
   TBranch        *b_tc_vtx_particles_py;   //!
   TBranch        *b_tc_vtx_particles_pz;   //!
   TBranch        *b_tc_vtx_particles_vtx_x;   //!
   TBranch        *b_tc_vtx_particles_vtx_y;   //!
   TBranch        *b_tc_vtx_particles_vtx_z;   //!
   TBranch        *b_tc_vtx_particles_vtx_fit_chi2;   //!
   TBranch        *b_tc_vtx_particles_energy;   //!
   TBranch        *b_tc_vtx_particles_mass;   //!
   TBranch        *b_Event_mc_particles_;   //!
   TBranch        *b_mc_particles_fUniqueID;   //!
   TBranch        *b_mc_particles_fBits;   //!
   TBranch        *b_mc_particles_pdg;   //!
   TBranch        *b_mc_particles_charge;   //!
   TBranch        *b_mc_particles_generator_status;   //!
   TBranch        *b_mc_particles_energy;   //!
   TBranch        *b_mc_particles_mass;   //!
   TBranch        *b_mc_particles_px;   //!
   TBranch        *b_mc_particles_py;   //!
   TBranch        *b_mc_particles_pz;   //!
   TBranch        *b_mc_particles_endpt_x;   //!
   TBranch        *b_mc_particles_endpt_y;   //!
   TBranch        *b_mc_particles_endpt_z;   //!
   TBranch        *b_Event_gbl_tracks_;   //!
   TBranch        *b_gbl_tracks_fUniqueID;   //!
   TBranch        *b_gbl_tracks_fBits;   //!
   TBranch        *b_gbl_tracks_kappa;   //!
   TBranch        *b_gbl_tracks_theta;   //!
   TBranch        *b_gbl_tracks_phi;   //!
   TBranch        *b_gbl_tracks_d0;   //!
   TBranch        *b_gbl_tracks_z0;   //!
   TBranch        *b_gbl_tracks_seed_kappa;   //!
   TBranch        *b_gbl_tracks_seed_theta;   //!
   TBranch        *b_gbl_tracks_seed_phi;   //!
   TBranch        *b_gbl_tracks_seed_d0;   //!
   TBranch        *b_gbl_tracks_seed_z0;   //!
   TBranch        *b_gbl_tracks_chi2;   //!
   TBranch        *b_gbl_tracks_ndf;   //!
   TBranch        *b_gbl_tracks_px;   //!
   TBranch        *b_gbl_tracks_py;   //!
   TBranch        *b_gbl_tracks_pz;   //!
   TBranch        *b_gbl_tracks_cov;   //!
   TBranch        *b_Event_gbl_tracks_data_;   //!
   TBranch        *b_gbl_tracks_data_fUniqueID;   //!
   TBranch        *b_gbl_tracks_data_fBits;   //!
   TBranch        *b_gbl_tracks_data_svt_track;   //!
   TBranch        *b_gbl_tracks_data_m_prjPerToCl;   //!
   TBranch        *b_gbl_tracks_data_n_gbl_strip_hits;   //!
   TBranch        *b_gbl_tracks_data_m_kappa;   //!
   TBranch        *b_gbl_tracks_data_m_theta;   //!
   TBranch        *b_gbl_tracks_data_m_phi;   //!
   TBranch        *b_gbl_tracks_data_m_d0;   //!
   TBranch        *b_gbl_tracks_data_m_z0;   //!
   TBranch        *b_Event_gbl_strips_data_;   //!
   TBranch        *b_gbl_strips_data_fUniqueID;   //!
   TBranch        *b_gbl_strips_data_fBits;   //!
   TBranch        *b_gbl_strips_data_m_id;   //!
   TBranch        *b_gbl_strips_data_m_path3D;   //!
   TBranch        *b_gbl_strips_data_m_path;   //!
   TBranch        *b_gbl_strips_data_m_u_fUniqueID;   //!
   TBranch        *b_gbl_strips_data_m_u_fBits;   //!
   TBranch        *b_gbl_strips_data_m_u_fX;   //!
   TBranch        *b_gbl_strips_data_m_u_fY;   //!
   TBranch        *b_gbl_strips_data_m_u_fZ;   //!
   TBranch        *b_gbl_strips_data_m_v_fUniqueID;   //!
   TBranch        *b_gbl_strips_data_m_v_fBits;   //!
   TBranch        *b_gbl_strips_data_m_v_fX;   //!
   TBranch        *b_gbl_strips_data_m_v_fY;   //!
   TBranch        *b_gbl_strips_data_m_v_fZ;   //!
   TBranch        *b_gbl_strips_data_m_w_fUniqueID;   //!
   TBranch        *b_gbl_strips_data_m_w_fBits;   //!
   TBranch        *b_gbl_strips_data_m_w_fX;   //!
   TBranch        *b_gbl_strips_data_m_w_fY;   //!
   TBranch        *b_gbl_strips_data_m_w_fZ;   //!
   TBranch        *b_gbl_strips_data_m_tdir_global_fUniqueID;   //!
   TBranch        *b_gbl_strips_data_m_tdir_global_fBits;   //!
   TBranch        *b_gbl_strips_data_m_tdir_global_fX;   //!
   TBranch        *b_gbl_strips_data_m_tdir_global_fY;   //!
   TBranch        *b_gbl_strips_data_m_tdir_global_fZ;   //!
   TBranch        *b_gbl_strips_data_m_tphi;   //!
   TBranch        *b_gbl_strips_data_m_tpos_fUniqueID;   //!
   TBranch        *b_gbl_strips_data_m_tpos_fBits;   //!
   TBranch        *b_gbl_strips_data_m_tpos_fX;   //!
   TBranch        *b_gbl_strips_data_m_tpos_fY;   //!
   TBranch        *b_gbl_strips_data_m_tpos_fZ;   //!
   TBranch        *b_gbl_strips_data_m_phi;   //!
   TBranch        *b_gbl_strips_data_m_lambda;   //!
   TBranch        *b_gbl_strips_data_m_umeas;   //!
   TBranch        *b_gbl_strips_data_m_umeas_err;   //!
   TBranch        *b_gbl_strips_data_m_ms_angle;   //!
   TBranch        *b_Event_event_number;   //!
   TBranch        *b_Event_run_number;   //!
   TBranch        *b_Event_trigger_time_stamp;   //!
   TBranch        *b_Event_single0_trigger;   //!
   TBranch        *b_Event_single1_trigger;   //!
   TBranch        *b_Event_pair0_trigger;   //!
   TBranch        *b_Event_pair1_trigger;   //!
   TBranch        *b_Event_pulser_trigger;   //!
   TBranch        *b_Event_n_tracks;   //!
   TBranch        *b_Event_n_svt_hits;   //!
   TBranch        *b_Event_n_ecal_clusters;   //!
   TBranch        *b_Event_n_ecal_hits;   //!
   TBranch        *b_Event_n_fs_particles;   //!
   TBranch        *b_Event_n_uc_vtx_particles;   //!
   TBranch        *b_Event_n_bsc_vtx_particles;   //!
   TBranch        *b_Event_n_tc_vtx_particles;   //!
   TBranch        *b_Event_n_mc_particles;   //!
   TBranch        *b_Event_n_gbl_tracks;   //!
   TBranch        *b_Event_n_gbl_tracks_data;   //!
   TBranch        *b_Event_n_gbl_strips_data;   //!

   foo(TTree *tree=0);
   virtual ~foo();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef foo_cxx
foo::foo(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../../EngRun2015/pass1/dst/hps_005772.10_dst_R3321.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("../../EngRun2015/pass1/dst/hps_005772.10_dst_R3321.root");
      }
      f->GetObject("HPS_Event",tree);

   }
   Init(tree);
}

foo::~foo()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t foo::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t foo::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void foo::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("fUniqueID", &fUniqueID, &b_Event_fUniqueID);
   fChain->SetBranchAddress("fBits", &fBits, &b_Event_fBits);
   fChain->SetBranchAddress("tracks", &tracks_, &b_Event_tracks_);
   fChain->SetBranchAddress("tracks.fUniqueID", tracks_fUniqueID, &b_tracks_fUniqueID);
   fChain->SetBranchAddress("tracks.fBits", tracks_fBits, &b_tracks_fBits);
   fChain->SetBranchAddress("tracks.fs_particle", tracks_fs_particle, &b_tracks_fs_particle);
   fChain->SetBranchAddress("tracks.n_hits", tracks_n_hits, &b_tracks_n_hits);
   fChain->SetBranchAddress("tracks.track_volume", tracks_track_volume, &b_tracks_track_volume);
   fChain->SetBranchAddress("tracks.d0", tracks_d0, &b_tracks_d0);
   fChain->SetBranchAddress("tracks.phi0", tracks_phi0, &b_tracks_phi0);
   fChain->SetBranchAddress("tracks.omega", tracks_omega, &b_tracks_omega);
   fChain->SetBranchAddress("tracks.tan_lambda", tracks_tan_lambda, &b_tracks_tan_lambda);
   fChain->SetBranchAddress("tracks.z0", tracks_z0, &b_tracks_z0);
   fChain->SetBranchAddress("tracks.chi_squared", tracks_chi_squared, &b_tracks_chi_squared);
   fChain->SetBranchAddress("tracks.track_time", tracks_track_time, &b_tracks_track_time);
   fChain->SetBranchAddress("tracks.l1_isolation", tracks_l1_isolation, &b_tracks_l1_isolation);
   fChain->SetBranchAddress("tracks.l2_isolation", tracks_l2_isolation, &b_tracks_l2_isolation);
   fChain->SetBranchAddress("svt_hits", &svt_hits_, &b_Event_svt_hits_);
   fChain->SetBranchAddress("svt_hits.fUniqueID", svt_hits_fUniqueID, &b_svt_hits_fUniqueID);
   fChain->SetBranchAddress("svt_hits.fBits", svt_hits_fBits, &b_svt_hits_fBits);
   fChain->SetBranchAddress("svt_hits.layer", svt_hits_layer, &b_svt_hits_layer);
   fChain->SetBranchAddress("svt_hits.x", svt_hits_x, &b_svt_hits_x);
   fChain->SetBranchAddress("svt_hits.y", svt_hits_y, &b_svt_hits_y);
   fChain->SetBranchAddress("svt_hits.z", svt_hits_z, &b_svt_hits_z);
   fChain->SetBranchAddress("svt_hits.cxx", svt_hits_cxx, &b_svt_hits_cxx);
   fChain->SetBranchAddress("svt_hits.cxy", svt_hits_cxy, &b_svt_hits_cxy);
   fChain->SetBranchAddress("svt_hits.cxz", svt_hits_cxz, &b_svt_hits_cxz);
   fChain->SetBranchAddress("svt_hits.cyy", svt_hits_cyy, &b_svt_hits_cyy);
   fChain->SetBranchAddress("svt_hits.cyz", svt_hits_cyz, &b_svt_hits_cyz);
   fChain->SetBranchAddress("svt_hits.czz", svt_hits_czz, &b_svt_hits_czz);
   fChain->SetBranchAddress("svt_hits.time", svt_hits_time, &b_svt_hits_time);
   fChain->SetBranchAddress("ecal_clusters", &ecal_clusters_, &b_Event_ecal_clusters_);
   fChain->SetBranchAddress("ecal_clusters.fUniqueID", ecal_clusters_fUniqueID, &b_ecal_clusters_fUniqueID);
   fChain->SetBranchAddress("ecal_clusters.fBits", ecal_clusters_fBits, &b_ecal_clusters_fBits);
   fChain->SetBranchAddress("ecal_clusters.seed_hit", ecal_clusters_seed_hit, &b_ecal_clusters_seed_hit);
   fChain->SetBranchAddress("ecal_clusters.n_ecal_hits", ecal_clusters_n_ecal_hits, &b_ecal_clusters_n_ecal_hits);
   fChain->SetBranchAddress("ecal_clusters.x", ecal_clusters_x, &b_ecal_clusters_x);
   fChain->SetBranchAddress("ecal_clusters.y", ecal_clusters_y, &b_ecal_clusters_y);
   fChain->SetBranchAddress("ecal_clusters.z", ecal_clusters_z, &b_ecal_clusters_z);
   fChain->SetBranchAddress("ecal_clusters.energy", ecal_clusters_energy, &b_ecal_clusters_energy);
   fChain->SetBranchAddress("ecal_clusters.cluster_time", ecal_clusters_cluster_time, &b_ecal_clusters_cluster_time);
   fChain->SetBranchAddress("ecal_hits", &ecal_hits_, &b_Event_ecal_hits_);
   fChain->SetBranchAddress("ecal_hits.fUniqueID", ecal_hits_fUniqueID, &b_ecal_hits_fUniqueID);
   fChain->SetBranchAddress("ecal_hits.fBits", ecal_hits_fBits, &b_ecal_hits_fBits);
   fChain->SetBranchAddress("ecal_hits.index_x", ecal_hits_index_x, &b_ecal_hits_index_x);
   fChain->SetBranchAddress("ecal_hits.index_y", ecal_hits_index_y, &b_ecal_hits_index_y);
   fChain->SetBranchAddress("ecal_hits.energy", ecal_hits_energy, &b_ecal_hits_energy);
   fChain->SetBranchAddress("ecal_hits.hit_time", ecal_hits_hit_time, &b_ecal_hits_hit_time);
   fChain->SetBranchAddress("fs_particles", &fs_particles_, &b_Event_fs_particles_);
   fChain->SetBranchAddress("fs_particles.fUniqueID", fs_particles_fUniqueID, &b_fs_particles_fUniqueID);
   fChain->SetBranchAddress("fs_particles.fBits", fs_particles_fBits, &b_fs_particles_fBits);
   fChain->SetBranchAddress("fs_particles.n_daughters", fs_particles_n_daughters, &b_fs_particles_n_daughters);
   fChain->SetBranchAddress("fs_particles.charge", fs_particles_charge, &b_fs_particles_charge);
   fChain->SetBranchAddress("fs_particles.pdg", fs_particles_pdg, &b_fs_particles_pdg);
   fChain->SetBranchAddress("fs_particles.px", fs_particles_px, &b_fs_particles_px);
   fChain->SetBranchAddress("fs_particles.py", fs_particles_py, &b_fs_particles_py);
   fChain->SetBranchAddress("fs_particles.pz", fs_particles_pz, &b_fs_particles_pz);
   fChain->SetBranchAddress("fs_particles.vtx_x", fs_particles_vtx_x, &b_fs_particles_vtx_x);
   fChain->SetBranchAddress("fs_particles.vtx_y", fs_particles_vtx_y, &b_fs_particles_vtx_y);
   fChain->SetBranchAddress("fs_particles.vtx_z", fs_particles_vtx_z, &b_fs_particles_vtx_z);
   fChain->SetBranchAddress("fs_particles.vtx_fit_chi2", fs_particles_vtx_fit_chi2, &b_fs_particles_vtx_fit_chi2);
   fChain->SetBranchAddress("fs_particles.energy", fs_particles_energy, &b_fs_particles_energy);
   fChain->SetBranchAddress("fs_particles.mass", fs_particles_mass, &b_fs_particles_mass);
   fChain->SetBranchAddress("uc_vtx_particles", &uc_vtx_particles_, &b_Event_uc_vtx_particles_);
   fChain->SetBranchAddress("uc_vtx_particles.fUniqueID", uc_vtx_particles_fUniqueID, &b_uc_vtx_particles_fUniqueID);
   fChain->SetBranchAddress("uc_vtx_particles.fBits", uc_vtx_particles_fBits, &b_uc_vtx_particles_fBits);
   fChain->SetBranchAddress("uc_vtx_particles.n_daughters", uc_vtx_particles_n_daughters, &b_uc_vtx_particles_n_daughters);
   fChain->SetBranchAddress("uc_vtx_particles.charge", uc_vtx_particles_charge, &b_uc_vtx_particles_charge);
   fChain->SetBranchAddress("uc_vtx_particles.pdg", uc_vtx_particles_pdg, &b_uc_vtx_particles_pdg);
   fChain->SetBranchAddress("uc_vtx_particles.px", uc_vtx_particles_px, &b_uc_vtx_particles_px);
   fChain->SetBranchAddress("uc_vtx_particles.py", uc_vtx_particles_py, &b_uc_vtx_particles_py);
   fChain->SetBranchAddress("uc_vtx_particles.pz", uc_vtx_particles_pz, &b_uc_vtx_particles_pz);
   fChain->SetBranchAddress("uc_vtx_particles.vtx_x", uc_vtx_particles_vtx_x, &b_uc_vtx_particles_vtx_x);
   fChain->SetBranchAddress("uc_vtx_particles.vtx_y", uc_vtx_particles_vtx_y, &b_uc_vtx_particles_vtx_y);
   fChain->SetBranchAddress("uc_vtx_particles.vtx_z", uc_vtx_particles_vtx_z, &b_uc_vtx_particles_vtx_z);
   fChain->SetBranchAddress("uc_vtx_particles.vtx_fit_chi2", uc_vtx_particles_vtx_fit_chi2, &b_uc_vtx_particles_vtx_fit_chi2);
   fChain->SetBranchAddress("uc_vtx_particles.energy", uc_vtx_particles_energy, &b_uc_vtx_particles_energy);
   fChain->SetBranchAddress("uc_vtx_particles.mass", uc_vtx_particles_mass, &b_uc_vtx_particles_mass);
   fChain->SetBranchAddress("bsc_vtx_particles", &bsc_vtx_particles_, &b_Event_bsc_vtx_particles_);
   fChain->SetBranchAddress("bsc_vtx_particles.fUniqueID", bsc_vtx_particles_fUniqueID, &b_bsc_vtx_particles_fUniqueID);
   fChain->SetBranchAddress("bsc_vtx_particles.fBits", bsc_vtx_particles_fBits, &b_bsc_vtx_particles_fBits);
   fChain->SetBranchAddress("bsc_vtx_particles.n_daughters", bsc_vtx_particles_n_daughters, &b_bsc_vtx_particles_n_daughters);
   fChain->SetBranchAddress("bsc_vtx_particles.charge", bsc_vtx_particles_charge, &b_bsc_vtx_particles_charge);
   fChain->SetBranchAddress("bsc_vtx_particles.pdg", bsc_vtx_particles_pdg, &b_bsc_vtx_particles_pdg);
   fChain->SetBranchAddress("bsc_vtx_particles.px", bsc_vtx_particles_px, &b_bsc_vtx_particles_px);
   fChain->SetBranchAddress("bsc_vtx_particles.py", bsc_vtx_particles_py, &b_bsc_vtx_particles_py);
   fChain->SetBranchAddress("bsc_vtx_particles.pz", bsc_vtx_particles_pz, &b_bsc_vtx_particles_pz);
   fChain->SetBranchAddress("bsc_vtx_particles.vtx_x", bsc_vtx_particles_vtx_x, &b_bsc_vtx_particles_vtx_x);
   fChain->SetBranchAddress("bsc_vtx_particles.vtx_y", bsc_vtx_particles_vtx_y, &b_bsc_vtx_particles_vtx_y);
   fChain->SetBranchAddress("bsc_vtx_particles.vtx_z", bsc_vtx_particles_vtx_z, &b_bsc_vtx_particles_vtx_z);
   fChain->SetBranchAddress("bsc_vtx_particles.vtx_fit_chi2", bsc_vtx_particles_vtx_fit_chi2, &b_bsc_vtx_particles_vtx_fit_chi2);
   fChain->SetBranchAddress("bsc_vtx_particles.energy", bsc_vtx_particles_energy, &b_bsc_vtx_particles_energy);
   fChain->SetBranchAddress("bsc_vtx_particles.mass", bsc_vtx_particles_mass, &b_bsc_vtx_particles_mass);
   fChain->SetBranchAddress("tc_vtx_particles", &tc_vtx_particles_, &b_Event_tc_vtx_particles_);
   fChain->SetBranchAddress("tc_vtx_particles.fUniqueID", tc_vtx_particles_fUniqueID, &b_tc_vtx_particles_fUniqueID);
   fChain->SetBranchAddress("tc_vtx_particles.fBits", tc_vtx_particles_fBits, &b_tc_vtx_particles_fBits);
   fChain->SetBranchAddress("tc_vtx_particles.n_daughters", tc_vtx_particles_n_daughters, &b_tc_vtx_particles_n_daughters);
   fChain->SetBranchAddress("tc_vtx_particles.charge", tc_vtx_particles_charge, &b_tc_vtx_particles_charge);
   fChain->SetBranchAddress("tc_vtx_particles.pdg", tc_vtx_particles_pdg, &b_tc_vtx_particles_pdg);
   fChain->SetBranchAddress("tc_vtx_particles.px", tc_vtx_particles_px, &b_tc_vtx_particles_px);
   fChain->SetBranchAddress("tc_vtx_particles.py", tc_vtx_particles_py, &b_tc_vtx_particles_py);
   fChain->SetBranchAddress("tc_vtx_particles.pz", tc_vtx_particles_pz, &b_tc_vtx_particles_pz);
   fChain->SetBranchAddress("tc_vtx_particles.vtx_x", tc_vtx_particles_vtx_x, &b_tc_vtx_particles_vtx_x);
   fChain->SetBranchAddress("tc_vtx_particles.vtx_y", tc_vtx_particles_vtx_y, &b_tc_vtx_particles_vtx_y);
   fChain->SetBranchAddress("tc_vtx_particles.vtx_z", tc_vtx_particles_vtx_z, &b_tc_vtx_particles_vtx_z);
   fChain->SetBranchAddress("tc_vtx_particles.vtx_fit_chi2", tc_vtx_particles_vtx_fit_chi2, &b_tc_vtx_particles_vtx_fit_chi2);
   fChain->SetBranchAddress("tc_vtx_particles.energy", tc_vtx_particles_energy, &b_tc_vtx_particles_energy);
   fChain->SetBranchAddress("tc_vtx_particles.mass", tc_vtx_particles_mass, &b_tc_vtx_particles_mass);
   fChain->SetBranchAddress("mc_particles", &mc_particles_, &b_Event_mc_particles_);
   fChain->SetBranchAddress("mc_particles.fUniqueID", &mc_particles_fUniqueID, &b_mc_particles_fUniqueID);
   fChain->SetBranchAddress("mc_particles.fBits", &mc_particles_fBits, &b_mc_particles_fBits);
   fChain->SetBranchAddress("mc_particles.pdg", &mc_particles_pdg, &b_mc_particles_pdg);
   fChain->SetBranchAddress("mc_particles.charge", &mc_particles_charge, &b_mc_particles_charge);
   fChain->SetBranchAddress("mc_particles.generator_status", &mc_particles_generator_status, &b_mc_particles_generator_status);
   fChain->SetBranchAddress("mc_particles.energy", &mc_particles_energy, &b_mc_particles_energy);
   fChain->SetBranchAddress("mc_particles.mass", &mc_particles_mass, &b_mc_particles_mass);
   fChain->SetBranchAddress("mc_particles.px", &mc_particles_px, &b_mc_particles_px);
   fChain->SetBranchAddress("mc_particles.py", &mc_particles_py, &b_mc_particles_py);
   fChain->SetBranchAddress("mc_particles.pz", &mc_particles_pz, &b_mc_particles_pz);
   fChain->SetBranchAddress("mc_particles.endpt_x", &mc_particles_endpt_x, &b_mc_particles_endpt_x);
   fChain->SetBranchAddress("mc_particles.endpt_y", &mc_particles_endpt_y, &b_mc_particles_endpt_y);
   fChain->SetBranchAddress("mc_particles.endpt_z", &mc_particles_endpt_z, &b_mc_particles_endpt_z);
   fChain->SetBranchAddress("gbl_tracks", &gbl_tracks_, &b_Event_gbl_tracks_);
   fChain->SetBranchAddress("gbl_tracks.fUniqueID", &gbl_tracks_fUniqueID, &b_gbl_tracks_fUniqueID);
   fChain->SetBranchAddress("gbl_tracks.fBits", &gbl_tracks_fBits, &b_gbl_tracks_fBits);
   fChain->SetBranchAddress("gbl_tracks.kappa", &gbl_tracks_kappa, &b_gbl_tracks_kappa);
   fChain->SetBranchAddress("gbl_tracks.theta", &gbl_tracks_theta, &b_gbl_tracks_theta);
   fChain->SetBranchAddress("gbl_tracks.phi", &gbl_tracks_phi, &b_gbl_tracks_phi);
   fChain->SetBranchAddress("gbl_tracks.d0", &gbl_tracks_d0, &b_gbl_tracks_d0);
   fChain->SetBranchAddress("gbl_tracks.z0", &gbl_tracks_z0, &b_gbl_tracks_z0);
   fChain->SetBranchAddress("gbl_tracks.seed_kappa", &gbl_tracks_seed_kappa, &b_gbl_tracks_seed_kappa);
   fChain->SetBranchAddress("gbl_tracks.seed_theta", &gbl_tracks_seed_theta, &b_gbl_tracks_seed_theta);
   fChain->SetBranchAddress("gbl_tracks.seed_phi", &gbl_tracks_seed_phi, &b_gbl_tracks_seed_phi);
   fChain->SetBranchAddress("gbl_tracks.seed_d0", &gbl_tracks_seed_d0, &b_gbl_tracks_seed_d0);
   fChain->SetBranchAddress("gbl_tracks.seed_z0", &gbl_tracks_seed_z0, &b_gbl_tracks_seed_z0);
   fChain->SetBranchAddress("gbl_tracks.chi2", &gbl_tracks_chi2, &b_gbl_tracks_chi2);
   fChain->SetBranchAddress("gbl_tracks.ndf", &gbl_tracks_ndf, &b_gbl_tracks_ndf);
   fChain->SetBranchAddress("gbl_tracks.px", &gbl_tracks_px, &b_gbl_tracks_px);
   fChain->SetBranchAddress("gbl_tracks.py", &gbl_tracks_py, &b_gbl_tracks_py);
   fChain->SetBranchAddress("gbl_tracks.pz", &gbl_tracks_pz, &b_gbl_tracks_pz);
   fChain->SetBranchAddress("gbl_tracks.cov", &gbl_tracks_cov, &b_gbl_tracks_cov);
   fChain->SetBranchAddress("gbl_tracks_data", &gbl_tracks_data_, &b_Event_gbl_tracks_data_);
   fChain->SetBranchAddress("gbl_tracks_data.fUniqueID", &gbl_tracks_data_fUniqueID, &b_gbl_tracks_data_fUniqueID);
   fChain->SetBranchAddress("gbl_tracks_data.fBits", &gbl_tracks_data_fBits, &b_gbl_tracks_data_fBits);
   fChain->SetBranchAddress("gbl_tracks_data.svt_track", &gbl_tracks_data_svt_track, &b_gbl_tracks_data_svt_track);
   fChain->SetBranchAddress("gbl_tracks_data.m_prjPerToCl", &gbl_tracks_data_m_prjPerToCl, &b_gbl_tracks_data_m_prjPerToCl);
   fChain->SetBranchAddress("gbl_tracks_data.n_gbl_strip_hits", &gbl_tracks_data_n_gbl_strip_hits, &b_gbl_tracks_data_n_gbl_strip_hits);
   fChain->SetBranchAddress("gbl_tracks_data.m_kappa", &gbl_tracks_data_m_kappa, &b_gbl_tracks_data_m_kappa);
   fChain->SetBranchAddress("gbl_tracks_data.m_theta", &gbl_tracks_data_m_theta, &b_gbl_tracks_data_m_theta);
   fChain->SetBranchAddress("gbl_tracks_data.m_phi", &gbl_tracks_data_m_phi, &b_gbl_tracks_data_m_phi);
   fChain->SetBranchAddress("gbl_tracks_data.m_d0", &gbl_tracks_data_m_d0, &b_gbl_tracks_data_m_d0);
   fChain->SetBranchAddress("gbl_tracks_data.m_z0", &gbl_tracks_data_m_z0, &b_gbl_tracks_data_m_z0);
   fChain->SetBranchAddress("gbl_strips_data", &gbl_strips_data_, &b_Event_gbl_strips_data_);
   fChain->SetBranchAddress("gbl_strips_data.fUniqueID", &gbl_strips_data_fUniqueID, &b_gbl_strips_data_fUniqueID);
   fChain->SetBranchAddress("gbl_strips_data.fBits", &gbl_strips_data_fBits, &b_gbl_strips_data_fBits);
   fChain->SetBranchAddress("gbl_strips_data.m_id", &gbl_strips_data_m_id, &b_gbl_strips_data_m_id);
   fChain->SetBranchAddress("gbl_strips_data.m_path3D", &gbl_strips_data_m_path3D, &b_gbl_strips_data_m_path3D);
   fChain->SetBranchAddress("gbl_strips_data.m_path", &gbl_strips_data_m_path, &b_gbl_strips_data_m_path);
   fChain->SetBranchAddress("gbl_strips_data.m_u.fUniqueID", &gbl_strips_data_m_u_fUniqueID, &b_gbl_strips_data_m_u_fUniqueID);
   fChain->SetBranchAddress("gbl_strips_data.m_u.fBits", &gbl_strips_data_m_u_fBits, &b_gbl_strips_data_m_u_fBits);
   fChain->SetBranchAddress("gbl_strips_data.m_u.fX", &gbl_strips_data_m_u_fX, &b_gbl_strips_data_m_u_fX);
   fChain->SetBranchAddress("gbl_strips_data.m_u.fY", &gbl_strips_data_m_u_fY, &b_gbl_strips_data_m_u_fY);
   fChain->SetBranchAddress("gbl_strips_data.m_u.fZ", &gbl_strips_data_m_u_fZ, &b_gbl_strips_data_m_u_fZ);
   fChain->SetBranchAddress("gbl_strips_data.m_v.fUniqueID", &gbl_strips_data_m_v_fUniqueID, &b_gbl_strips_data_m_v_fUniqueID);
   fChain->SetBranchAddress("gbl_strips_data.m_v.fBits", &gbl_strips_data_m_v_fBits, &b_gbl_strips_data_m_v_fBits);
   fChain->SetBranchAddress("gbl_strips_data.m_v.fX", &gbl_strips_data_m_v_fX, &b_gbl_strips_data_m_v_fX);
   fChain->SetBranchAddress("gbl_strips_data.m_v.fY", &gbl_strips_data_m_v_fY, &b_gbl_strips_data_m_v_fY);
   fChain->SetBranchAddress("gbl_strips_data.m_v.fZ", &gbl_strips_data_m_v_fZ, &b_gbl_strips_data_m_v_fZ);
   fChain->SetBranchAddress("gbl_strips_data.m_w.fUniqueID", &gbl_strips_data_m_w_fUniqueID, &b_gbl_strips_data_m_w_fUniqueID);
   fChain->SetBranchAddress("gbl_strips_data.m_w.fBits", &gbl_strips_data_m_w_fBits, &b_gbl_strips_data_m_w_fBits);
   fChain->SetBranchAddress("gbl_strips_data.m_w.fX", &gbl_strips_data_m_w_fX, &b_gbl_strips_data_m_w_fX);
   fChain->SetBranchAddress("gbl_strips_data.m_w.fY", &gbl_strips_data_m_w_fY, &b_gbl_strips_data_m_w_fY);
   fChain->SetBranchAddress("gbl_strips_data.m_w.fZ", &gbl_strips_data_m_w_fZ, &b_gbl_strips_data_m_w_fZ);
   fChain->SetBranchAddress("gbl_strips_data.m_tdir_global.fUniqueID", &gbl_strips_data_m_tdir_global_fUniqueID, &b_gbl_strips_data_m_tdir_global_fUniqueID);
   fChain->SetBranchAddress("gbl_strips_data.m_tdir_global.fBits", &gbl_strips_data_m_tdir_global_fBits, &b_gbl_strips_data_m_tdir_global_fBits);
   fChain->SetBranchAddress("gbl_strips_data.m_tdir_global.fX", &gbl_strips_data_m_tdir_global_fX, &b_gbl_strips_data_m_tdir_global_fX);
   fChain->SetBranchAddress("gbl_strips_data.m_tdir_global.fY", &gbl_strips_data_m_tdir_global_fY, &b_gbl_strips_data_m_tdir_global_fY);
   fChain->SetBranchAddress("gbl_strips_data.m_tdir_global.fZ", &gbl_strips_data_m_tdir_global_fZ, &b_gbl_strips_data_m_tdir_global_fZ);
   fChain->SetBranchAddress("gbl_strips_data.m_tphi", &gbl_strips_data_m_tphi, &b_gbl_strips_data_m_tphi);
   fChain->SetBranchAddress("gbl_strips_data.m_tpos.fUniqueID", &gbl_strips_data_m_tpos_fUniqueID, &b_gbl_strips_data_m_tpos_fUniqueID);
   fChain->SetBranchAddress("gbl_strips_data.m_tpos.fBits", &gbl_strips_data_m_tpos_fBits, &b_gbl_strips_data_m_tpos_fBits);
   fChain->SetBranchAddress("gbl_strips_data.m_tpos.fX", &gbl_strips_data_m_tpos_fX, &b_gbl_strips_data_m_tpos_fX);
   fChain->SetBranchAddress("gbl_strips_data.m_tpos.fY", &gbl_strips_data_m_tpos_fY, &b_gbl_strips_data_m_tpos_fY);
   fChain->SetBranchAddress("gbl_strips_data.m_tpos.fZ", &gbl_strips_data_m_tpos_fZ, &b_gbl_strips_data_m_tpos_fZ);
   fChain->SetBranchAddress("gbl_strips_data.m_phi", &gbl_strips_data_m_phi, &b_gbl_strips_data_m_phi);
   fChain->SetBranchAddress("gbl_strips_data.m_lambda", &gbl_strips_data_m_lambda, &b_gbl_strips_data_m_lambda);
   fChain->SetBranchAddress("gbl_strips_data.m_umeas", &gbl_strips_data_m_umeas, &b_gbl_strips_data_m_umeas);
   fChain->SetBranchAddress("gbl_strips_data.m_umeas_err", &gbl_strips_data_m_umeas_err, &b_gbl_strips_data_m_umeas_err);
   fChain->SetBranchAddress("gbl_strips_data.m_ms_angle", &gbl_strips_data_m_ms_angle, &b_gbl_strips_data_m_ms_angle);
   fChain->SetBranchAddress("event_number", &event_number, &b_Event_event_number);
   fChain->SetBranchAddress("run_number", &run_number, &b_Event_run_number);
   fChain->SetBranchAddress("trigger_time_stamp", &trigger_time_stamp, &b_Event_trigger_time_stamp);
   fChain->SetBranchAddress("single0_trigger", &single0_trigger, &b_Event_single0_trigger);
   fChain->SetBranchAddress("single1_trigger", &single1_trigger, &b_Event_single1_trigger);
   fChain->SetBranchAddress("pair0_trigger", &pair0_trigger, &b_Event_pair0_trigger);
   fChain->SetBranchAddress("pair1_trigger", &pair1_trigger, &b_Event_pair1_trigger);
   fChain->SetBranchAddress("pulser_trigger", &pulser_trigger, &b_Event_pulser_trigger);
   fChain->SetBranchAddress("n_tracks", &n_tracks, &b_Event_n_tracks);
   fChain->SetBranchAddress("n_svt_hits", &n_svt_hits, &b_Event_n_svt_hits);
   fChain->SetBranchAddress("n_ecal_clusters", &n_ecal_clusters, &b_Event_n_ecal_clusters);
   fChain->SetBranchAddress("n_ecal_hits", &n_ecal_hits, &b_Event_n_ecal_hits);
   fChain->SetBranchAddress("n_fs_particles", &n_fs_particles, &b_Event_n_fs_particles);
   fChain->SetBranchAddress("n_uc_vtx_particles", &n_uc_vtx_particles, &b_Event_n_uc_vtx_particles);
   fChain->SetBranchAddress("n_bsc_vtx_particles", &n_bsc_vtx_particles, &b_Event_n_bsc_vtx_particles);
   fChain->SetBranchAddress("n_tc_vtx_particles", &n_tc_vtx_particles, &b_Event_n_tc_vtx_particles);
   fChain->SetBranchAddress("n_mc_particles", &n_mc_particles, &b_Event_n_mc_particles);
   fChain->SetBranchAddress("n_gbl_tracks", &n_gbl_tracks, &b_Event_n_gbl_tracks);
   fChain->SetBranchAddress("n_gbl_tracks_data", &n_gbl_tracks_data, &b_Event_n_gbl_tracks_data);
   fChain->SetBranchAddress("n_gbl_strips_data", &n_gbl_strips_data, &b_Event_n_gbl_strips_data);
   Notify();
}

Bool_t foo::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void foo::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t foo::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef foo_cxx
