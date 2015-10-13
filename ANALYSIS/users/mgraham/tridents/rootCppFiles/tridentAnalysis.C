#define tridentAnalysis_cxx
#include "tridentAnalysis.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TMath.h>
void tridentAnalysis::Loop(TString outfile,bool isData)
{
//   In a ROOT session, you can do:
//      Root > .L tridentAnalysis.C
//      Root > tridentAnalysis t
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



   double ebeam=1.05;
//clean up event first
    int nTrkMax=5;
    int nPosMax=1;
 //v0 cuts   
    double v0Chi2=10;
    double v0PzMax=1.25*ebeam;
    double v0PzMin=0.6;
    double v0PyMax=0.2;//absolute value
    double v0PxMax=0.2;//absolute value
    double v0VzMax=25.0;// mm from target
    double v0VyMax=1.0;// mm from target
    double v0VxMax=2.0;// mm from target
    //  track quality cuts
    double trkChi2=10;
    //    double beamCut=0.8*ebeam;
    double beamCut=0.9;
    double trkPzMin=0.05;
    double trkPyMax=0.2;//absolute value
    double trkPxMax=0.2;//absolute value

    double radCut=0.8*ebeam;

//cluster matching
    bool   reqCluster=true;
    int    nClustMax=3;
    double eneLossFactor=0.7; //average E/p roughly
    double eneOverPCut=0.3; //|(E/p)_meas - (E/p)_mean|<eneOverPCut

    //kill tracks with...
    double killSlopeLT=0.02;//abs(slope)<killSlopeLT

//counters
    int nEvents=0;
    int nPassBasicCuts=0;
    int nPassV0PCuts=0;
    int nPassV0VCuts=0;
    int nPassTrkCuts=0;
 
    int nPassClusterCuts=0;

    TH1D*     tridentMass =new TH1D("TridentMass","Trident Mass (GeV)", 100, 0, 0.100);
    TH1D*     tridentMassVtxCut =new TH1D( "TridentMassBeforeVertex", "Trident Mass (GeV): Before  VtxCut", 100, 0, 0.100);
    TH1D*     tridentVx =new TH1D("Vx", "Trident Vx (mm)", 50, -4, 4);
    TH1D*     tridentVy =new TH1D("Vy","Trident Vy (mm)", 50, -2, 2);
    TH1D*     tridentVz = new TH1D("Vz", "Trident Vz (mm)", 50, -50, 50);
    TH1D*     eSum = new TH1D("eSum", "Energy Sum", 50, 0.3, 1.2);
    TH1D*     eDiff = new TH1D("eDiffoverESum", "Energy Difference", 50, -0.8, 0.8);    
    TH1D*     vertChi2 = new TH1D("vertChi2", "V0 Chi2", 50, 0, 10);    
    TH2D*     ePosvseEle=new TH2D("ePosvseEle","Positron vs Electron Energy",50,0.1,0.9,50,0.1,0.9);
    TH1D*     tanopenY = new TH1D("tanopenY", "tanopenY", 100, 0., 0.16);
    TH1D*     tanopenYThresh = new TH1D("tanopenYThresh", "tanopenYThresh", 100, 0.025, 0.06);
    
    
    TH1D*   eleMom =new TH1D("eleMom","Electron Momentum (GeV)", 100, 0, 1.);
    TH1D*   posMom =new TH1D("posMom","Positron Momentum (GeV)", 100, 0, 1.);

    TH1D*   eled0 =new TH1D("eled0","Electron d0 (mm)", 100, -3, 3);
    TH1D*   posd0 =new TH1D("posd0","Positron d0 (mm)", 100, -3, 3);

    TH1D*   elez0 =new TH1D("elez0","Electron z0 (mm)", 100, -1.5, 1.5);
    TH1D*   posz0 =new TH1D("posz0","Positron z0 (mm)", 100, -1.5, 1.5);


    TH1D*   elephi0 =new TH1D("elephi0","Electron phi0", 100, -0.1, 0.1);
    TH1D*   posphi0 =new TH1D("posphi0","Positron phi0", 100, -0.1, 0.1);

    TH1D*   eleslope =new TH1D("eleslope","Electron slope", 100, -0.08, 0.08);
    TH1D*   posslope =new TH1D("posslope","Positron slope", 100, -0.08, 0.08);

    TH1D*   trkTimeDiff =new TH1D("trkTimeDiff","Ele-Pos Time Difference (ns)", 100, -6, 6);

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
   


    Long64_t nentries = fChain->GetEntriesFast();
    
   Long64_t nbytes = 0, nb = 0;
   int npassFile=0;
   cout<<"Number of entries = "<<nentries<<endl;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if(ientry==0){
	cout<<"# Passed previous file = "<<npassFile<<endl;
	npassFile=0;
      }
	
      if(nEvents%10000 == 0)
	cout<<nEvents<<endl;
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      //      cout<<"Looking for pair trigger"<<endl;
      if(!pair1_trigger&&isData) continue;
      nEvents++;
// basic sanity cuts
      if(n_tracks>nTrkMax) continue;
      if(n_tracks<2) continue;        
      int posCount=0;
      int ipos=-99;
      for(int ifsp=0;ifsp<n_fs_particles;ifsp++){
        if(fs_particles_charge[ifsp]>0){ 
            posCount++;
            ipos=ifsp;
        }
      }
      if(posCount>nPosMax) continue;
      if(posCount<1) continue;
      if(n_uc_vtx_particles!=1)continue; //required only 1 positron --> 1 v0 in event so we can keep it simple...      

      nPassBasicCuts++;// event passed

      //required only 2 tracks = 1 v0 in event so we can keep it simple...      
      //first do vertex/v0 level cuts

      bool passV0cut=false;
      int bestv0index=-99;
      for(int ii=0;ii<n_uc_vtx_particles;ii++){	
	int uc_index=ii;		
	if(uc_vtx_particles_vtx_fit_chi2[uc_index]>v0Chi2) continue;
	if(uc_vtx_particles_pz[uc_index]>v0PzMax) continue;
	if(uc_vtx_particles_pz[uc_index]<v0PzMin) continue;
	if(fabs(uc_vtx_particles_vtx_x[uc_index])>v0VxMax) continue;
	if(fabs(uc_vtx_particles_vtx_y[uc_index])>v0VyMax) continue;
	if(fabs(uc_vtx_particles_vtx_z[uc_index])>v0VzMax) continue;
      }
      nPassV0VCuts++;
      
      tridentVx->Fill(uc_vtx_particles_vtx_x[bestv0index]);
      tridentVy->Fill(uc_vtx_particles_vtx_y[bestv0index]);
      tridentVz->Fill(uc_vtx_particles_vtx_z[bestv0index]);
      tridentMassVtxCut->Fill(uc_vtx_particles_mass[bestv0index]);
      
      //now do track cuts
      int ele=-99;
      int pos=-99;
      for(int ifsp=0;ifsp<n_fs_particles;ifsp++){
	if(fs_particles_charge[ifsp]<0)
	  ele=ifsp;
	else if(fs_particles_charge[ifsp]>0)
	  pos=ifsp;
      }
      
      double pEle=getMomentum(ele);
      double pPos=getMomentum(pos);
 //get the tracks from the "tracks block"...since there are only 2 it should be easy
      int ipos=-99;
      int iele=-99;
      for(int i=0;i<n_tracks;i++){
	if(tracks_omega[i]>0)
	  iele=i;
	else
	  ipos=i;
      }
      
      //      if(fs_particles_px[pos]*fs_particles_px[ele]>0)//require opposite px...forgot about the 30mrad rotation...fix later...
      //	continue;
      if(fs_particles_py[pos]*fs_particles_py[ele]>0)//require opposite py
	continue;
      if(pEle>beamCut||pPos>beamCut)
	continue;
      if(pEle<trkPzMin||pPos<trkPzMin)
	continue;
      //kill some tracks
      if(TMath::Abs(tracks_tan_lambda[iele])<killSlopeLT||TMath::Abs(tracks_tan_lambda[ipos])<killSlopeLT)
	continue;
      nPassTrkCuts++;

      npassFile++;
      ePosvseEle->Fill(pEle,pPos);
      eSum->Fill(pEle+pPos);
      eDiff->Fill((pEle-pPos)/(pEle+pPos));
      tridentMass->Fill(uc_vtx_particles_mass[uc_index]);

      eleMom->Fill(pEle);
      posMom->Fill(pPos);
      
     
      
      eled0->Fill(tracks_d0[iele]);
      elez0->Fill(tracks_z0[iele]);
      elephi0->Fill(TMath::Sin(tracks_phi0[iele]));
      eleslope->Fill(tracks_tan_lambda[iele]);
      
      posd0->Fill(tracks_d0[ipos]);
      posz0->Fill(tracks_z0[ipos]);
      posphi0->Fill(TMath::Sin(tracks_phi0[ipos]));
      posslope->Fill(tracks_tan_lambda[ipos]);

      trkTimeDiff->Fill(tracks_track_time[iele]-tracks_track_time[ipos]);
      vertChi2->Fill(uc_vtx_particles_vtx_fit_chi2[uc_index]);
      
      topenAngle=TMath::Abs(tracks_tan_lambda[iele])+TMath::Abs(tracks_tan_lambda[ipos]);

      tanopenY->Fill(topenAngle);
      tanopenYThresh->Fill(topenAngle);

      for(int i=0;i<n_svt_hits;i++){
	int layer = svt_hits_layer[i];
	if(svt_hits_z[i]<0)
	  tHitBot[layer]->Fill(svt_hits_time[i]);
	else
	  tHitTop[layer]->Fill(svt_hits_time[i]);	  
      }

   }


   TFile* out=new TFile(outfile,"RECREATE");
   tridentMass->Write();
   tridentVx->Write();
   tridentVy->Write();
   tridentVz->Write();
   tridentMassVtxCut->Write();
   ePosvseEle->Write();
   vertChi2->Write();
   eSum->Write();
   eDiff->Write();
   eleMom->Write(); 
   eled0->Write(); 
   elez0->Write();
   elephi0->Write();
   eleslope->Write();
   posMom->Write(); 
   posd0->Write(); 
   posz0->Write();
   posphi0->Write();
   posslope->Write();
   trkTimeDiff->Write();
   tanopenYThresh->Write();
   tanopenY->Write();
   for(int i=1;i<nlayers;i++){
     tHitTop[i]->Write();
     tHitBot[i]->Write();
   }
   out->Close();


   cout<<"\t\t\tTrident Selection Summary"<<endl;
   cout<<"******************************************************************************************"<<endl;
   cout<<"Number of Events:\t\t"<<nEvents<<"\t\t\t"<<(double)nEvents/nEvents<<"\t\t\t"<<(double)nEvents/nEvents<<endl;
   cout<<"N(particle) Cuts:\t\t"<<nPassBasicCuts<<"\t\t\t"<<(double)nPassBasicCuts/nEvents<<"\t\t\t"<<(double)nPassBasicCuts/nEvents<<endl;
   cout<<"V0 Momentum Cuts:\t\t"<<nPassV0PCuts<<"\t\t\t"<<(double)nPassV0PCuts/nPassBasicCuts<<"\t\t\t"<<(double)nPassV0PCuts/nEvents<<endl;
   cout<<"V0 Vertex   Cuts:\t\t"<<nPassV0VCuts<<"\t\t\t"<<(double)nPassV0VCuts/nPassV0PCuts<<"\t\t\t"<<(double)nPassV0VCuts/nEvents<<endl;
   cout<<"Tracking    Cuts:\t\t"<<nPassTrkCuts<<"\t\t\t"<<(double)nPassTrkCuts/nPassV0VCuts<<"\t\t\t"<<(double)nPassTrkCuts/nEvents<<endl;

}
