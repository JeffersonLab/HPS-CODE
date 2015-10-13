#define lookAtHits_cxx
#include "lookAtHits.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void lookAtHits::Loop(TString outfile,bool isData)
{
//   In a ROOT session, you can do:
//      Root > .L lookAtHits.C
//      Root > lookAtHits t
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
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   int nlayers=7;
   TH1D* tHitTop[7];
   TH1D* tHitBot[7];

   TString pre="time (ns) for layer ";
   for(int i=1;i<nlayers;i++){
     TString topName=pre;topName+=i;topName+=" Top";
     tHitTop[i]=new TH1D(topName,topName,100,-16,16);
     TString botName=pre;botName+=i;botName+=" Bot";
     tHitBot[i]=new TH1D(botName,botName,100,-16,16);
   }
   

   cout<<"Start of loop"<<endl;
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      
      for(int i=0;i<n_svt_hits;i++){
	int layer = svt_hits_layer[i];
	if(svt_hits_z[i]<0)
	  tHitBot[layer]->Fill(svt_hits_time[i]);
	else
	  tHitTop[layer]->Fill(svt_hits_time[i]);	  
      }

   }

   TFile* out=new TFile(outfile,"RECREATE");
   for(int i=1;i<nlayers;i++){
     tHitTop[i]->Write();
     tHitBot[i]->Write();
   }

   out->Close();
}
