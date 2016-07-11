//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Feb 15 18:45:05 2016 by ROOT version 5.34/32
// from TTree tr1/Matched clusters and Tracks
// found on file: Analyze_tr_and_cl__5772.root
//////////////////////////////////////////////////////////

#ifndef tridentTrackEfficiency_h
#define tridentTrackEfficiency_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class tridentTrackEfficiency {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Long64_t        time_stamp;
   Int_t           hps_ev_number;
   Bool_t          single0;
   Bool_t          single1;
   Bool_t          pair0;
   Bool_t          pair1;
   Bool_t          pulser;
   Int_t           n_cl;
   Double_t        cl_E[14];   //[n_cl]
   Double_t        cl_t[14];   //[n_cl]
   Double_t        cl_x[14];   //[n_cl]
   Double_t        cl_y[14];   //[n_cl]
   Double_t        cl_z[14];   //[n_cl]
   Int_t           cl_size[14];   //[n_cl]
   Int_t           n_tr;
   Double_t        tr_px[20];   //[n_tr]
   Double_t        tr_py[20];   //[n_tr]
   Double_t        tr_pz[20];   //[n_tr]
   Double_t        tr_p[20];   //[n_tr]
   Double_t        tr_omega[20];   //[n_tr]
   Double_t        tr_tanLambda[20];   //[n_tr]
   Double_t        tr_phi[20];   //[n_tr]
   Double_t        tr_d0[20];   //[n_tr]
   Double_t        tr_z0[20];   //[n_tr]
   Double_t        tr_x[20];   //[n_tr]
   Double_t        tr_y[20];   //[n_tr]
   Double_t        tr_chi2[20];   //[n_tr]
   Int_t           tr_nhits[20];   //[n_tr]
   Int_t           tr_ndf[20];   //[n_tr]

   // List of branches
   TBranch        *b_time_stamp;   //!
   TBranch        *b_hps_ev_number;   //!
   TBranch        *b_single0;   //!
   TBranch        *b_single1;   //!
   TBranch        *b_pair0;   //!
   TBranch        *b_pair1;   //!
   TBranch        *b_pulser;   //!
   TBranch        *b_n_cl;   //!
   TBranch        *b_cl_E;   //!
   TBranch        *b_cl_t;   //!
   TBranch        *b_cl_x;   //!
   TBranch        *b_cl_y;   //!
   TBranch        *b_cl_z;   //!
   TBranch        *b_cl_size;   //!
   TBranch        *b_n_tr;   //!
   TBranch        *b_tr_px;   //!
   TBranch        *b_tr_py;   //!
   TBranch        *b_tr_pz;   //!
   TBranch        *b_tr_p;   //!
   TBranch        *b_tr_omega;   //!
   TBranch        *b_tr_tanLambda;   //!
   TBranch        *b_tr_phi;   //!
   TBranch        *b_tr_d0;   //!
   TBranch        *b_tr_z0;   //!
   TBranch        *b_tr_x;   //!
   TBranch        *b_tr_y;   //!
   TBranch        *b_tr_chi2;   //!
   TBranch        *b_tr_nhits;   //!
   TBranch        *b_tr_ndf;   //!

   tridentTrackEfficiency(TTree *tree=0);
   virtual ~tridentTrackEfficiency();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString out);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
   
   bool energySlopeCut(double, double, double);
   bool fid_ECal(double, double);
   bool superFid_ECal(double, double);
   int matchTrack(int);

   double momFromRadius(double, double);
   double radiusFromECAL(double, double, double);
   double momFromECalPosition(double ,double , double , double );
   bool momFromPositionEclUpperCut(double, double);
};

#endif

#ifdef tridentTrackEfficiency_cxx
tridentTrackEfficiency::tridentTrackEfficiency(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("Analyze_tr_and_cl__5772.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("Analyze_tr_and_cl__5772.root");
      }
      f->GetObject("tr1",tree);

   }
   Init(tree);
}

tridentTrackEfficiency::~tridentTrackEfficiency()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t tridentTrackEfficiency::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t tridentTrackEfficiency::LoadTree(Long64_t entry)
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

void tridentTrackEfficiency::Init(TTree *tree)
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

   fChain->SetBranchAddress("time_stamp", &time_stamp, &b_time_stamp);
   fChain->SetBranchAddress("hps_ev_number", &hps_ev_number, &b_hps_ev_number);
   fChain->SetBranchAddress("single0", &single0, &b_single0);
   fChain->SetBranchAddress("single1", &single1, &b_single1);
   fChain->SetBranchAddress("pair0", &pair0, &b_pair0);
   fChain->SetBranchAddress("pair1", &pair1, &b_pair1);
   fChain->SetBranchAddress("pulser", &pulser, &b_pulser);
   fChain->SetBranchAddress("n_cl", &n_cl, &b_n_cl);
   fChain->SetBranchAddress("cl_E", cl_E, &b_cl_E);
   fChain->SetBranchAddress("cl_t", cl_t, &b_cl_t);
   fChain->SetBranchAddress("cl_x", cl_x, &b_cl_x);
   fChain->SetBranchAddress("cl_y", cl_y, &b_cl_y);
   fChain->SetBranchAddress("cl_z", cl_z, &b_cl_z);
   fChain->SetBranchAddress("cl_size", cl_size, &b_cl_size);
   fChain->SetBranchAddress("n_tr", &n_tr, &b_n_tr);
   fChain->SetBranchAddress("tr_px", tr_px, &b_tr_px);
   fChain->SetBranchAddress("tr_py", tr_py, &b_tr_py);
   fChain->SetBranchAddress("tr_pz", tr_pz, &b_tr_pz);
   fChain->SetBranchAddress("tr_p", tr_p, &b_tr_p);
   fChain->SetBranchAddress("tr_omega", tr_omega, &b_tr_omega);
   fChain->SetBranchAddress("tr_tanLambda", tr_tanLambda, &b_tr_tanLambda);
   fChain->SetBranchAddress("tr_phi", tr_phi, &b_tr_phi);
   fChain->SetBranchAddress("tr_d0", tr_d0, &b_tr_d0);
   fChain->SetBranchAddress("tr_z0", tr_z0, &b_tr_z0);
   fChain->SetBranchAddress("tr_x", tr_x, &b_tr_x);
   fChain->SetBranchAddress("tr_y", tr_y, &b_tr_y);
   fChain->SetBranchAddress("tr_chi2", tr_chi2, &b_tr_chi2);
   fChain->SetBranchAddress("tr_nhits", tr_nhits, &b_tr_nhits);
   fChain->SetBranchAddress("tr_ndf", tr_ndf, &b_tr_ndf);
   Notify();
}

Bool_t tridentTrackEfficiency::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void tridentTrackEfficiency::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t tridentTrackEfficiency::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}

//================== Energy slope cut =============================
bool tridentTrackEfficiency::energySlopeCut(double cl_x,double cl_d, double cl_E){
  return cl_x > 0 && cl_d > (60. + 100*(cl_E - 0.85)*(cl_E - 0.85) )&& cl_E < 0.82;
  // cl_x > 0 : this selects non-negatives (photon ot e+)
  // cl_E < 0.82 : We don't have (almost don't have) positrons with energies higher that this energy
  // cl_d > 60. + 100*(cl_E - 0.85)^2: the energy slope cut
}
//================= End of Energy slope cut =======================      



//====================== Fiducial cuts ===================
// returns false or true
bool tridentTrackEfficiency::fid_ECal(double x, double y)
{
  bool in_fid = false;
  const double x_edge_low = -262.74;
  const double x_edge_high = 347.7;
  const double y_edge_low = 33.54;
  const double y_edge_high = 75.18;
  
  const double x_gap_low = -106.66;
  const double x_gap_high = 42.17;
  const double y_gap_high = 47.18;
  
  y = TMath::Abs(y);
  
  if( x > x_edge_low && x < x_edge_high && y > y_edge_low && y < y_edge_high )
    {
      if( !(x > x_gap_low && x < x_gap_high && y > y_edge_low && y < y_gap_high) )
	{
	  in_fid = true;
	}
    }
  
  return in_fid;
  

}
//============= End of Fiducial cut ======================


//====================== Fiducial cuts ===================
// returns false or true
bool tridentTrackEfficiency::superFid_ECal(double x, double y)
{
  bool in_fid = false;
  const double x_edge_low = -262.74;
  const double x_edge_high = 347.7;
  double y_edge_low = 33.54;
  const double y_edge_high = 75.18;
  
  const double x_gap_low = -106.66;
  const double x_gap_high = 42.17;
  const double y_gap_high = 47.18;
  
  y_edge_low=y_gap_high;

  y = TMath::Abs(y);
  
  if( x > x_edge_low && x < x_edge_high && y > y_edge_low && y < y_edge_high )
    {
      if( !(x > x_gap_low && x < x_gap_high && y > y_edge_low && y < y_gap_high) )
	{
	  in_fid = true;
	}
    }
  
  return in_fid;
  

}
//============= End of Fiducial cut ======================

int tridentTrackEfficiency::matchTrack(int cl){
  
  double delECut=0.5;
  double delXCut=30;
  double delYCut=30;
  int tr=-99;
  
  for (int i = 0; i<n_tr;i++){
    if(fabs(tr_p[i]-cl_E[cl])>delECut)
      continue;
    if(fabs(tr_x[i]-cl_x[cl])>delXCut)
      continue;
    if(fabs(tr_y[i]-cl_y[cl])>delYCut)
      continue;
    tr=i;    
  }  
  return tr;

}


double tridentTrackEfficiency::radiusFromECAL(double x, double z, double b){
  return sqrt(1+b*b)*(x*x+z*z)/(2*(x-b*z));
}

double tridentTrackEfficiency::momFromRadius(double rad,double BEff){
  return TMath::Abs(rad*BEff*2.99792458e-4);
  //return TMath::Abs(rad*0.2*2.99792458e-4);
}

double tridentTrackEfficiency::momFromECalPosition(double x,double z, double b, double Beff){
  return momFromRadius(radiusFromECAL(x,z,b),Beff);
}

bool tridentTrackEfficiency::momFromPositionEclUpperCut(double Ecl, double mFromPosition){
  double slp=1.176;
  double b=0.182;
  double cutVal=Ecl*slp+b;
  if (mFromPosition>cutVal)
    return false;
  return true;
}

#endif // #ifdef tridentTrackEfficiency_cxx
