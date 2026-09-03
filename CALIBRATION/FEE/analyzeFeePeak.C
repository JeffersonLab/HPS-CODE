/////////////////////////////////////////////////////////////////////////////////
/*
Date: 10 July 2026
Author: Erbaz Khan (Modified Holly Szumila's 2015/2016 macro.)
Purpose: This code performs a single iteration of the FEE claibration.
How to run: In root, run .L thisCode.C fitPeaks(N,P) where N is the iteration number, starting with 1,
and P is the period number. 2019 data had 6 termperature stable windows (periods), that were calibrated independently.
If there is no such thing, then there will be only one period. Output directory is named output_iter<N>_p<P>.
Reads in:
-mc constants
-root histograms from current iteration
-previous global total
-cosmic gains
Outputs:
-next iterative FEE correction factor
-updated global coefficient, cGlobal, this excludes cosmics
-png fits plots (must check)

NOTE: Once the FEE iterations are over, we need to correct the uncorrected crystals
to bring them corrected and uncorrected crystals on the same scale.
Mean of the ratio corrected_gains/baseline_gains for all the corrected crystals can
be used as the correction factor for the uncorrected crystals. This step is not done
this macro. We also need to test whether to exclude the edge rows based on how stable
their FEE fit is.
 */
////////////////////////////////////////////////////////////////////////////////
#define NX 46
#define NY 10
#define NCRY 442

#include <TPaveStats.h>
#include "util/utilities.h"
//const double EBEAM = 1.05; // original 2015 value
// const double EBEAM = 3.742; // 2021 value
const double EBEAM = 4.55;

//Gets the max bin in each crystal histogram and plots.
void fitPeaks(int ITER, int PERIOD){

  //Read in iteration coefficients (for iteration 0, =1):
  float prevC[NCRY]={};
  float previous;
  string line1;
  int cid1;
  if (ITER>1){
    FILE *myfile1 = fopen(Form("output_iter%d_p%d/c%d.txt",ITER-1,PERIOD,ITER-1), "r");
    while (fscanf(myfile1, "%d,%f",&cid1, &previous)>0){
      prevC[cid1-1] = previous;
    }
    fclose(myfile1);
  }
  else{
    for (int ik=0; ik<NCRY; ik++){
      prevC[ik] = 1.0;
    }
  }

  //Read in MC constant fractions:
  float mcG[NCRY]={};
  float mcgains;
  int cid2;
  string line2;
  FILE *myfile2 = fopen("coeff/MC_constant.txt", "r");
  while (fscanf(myfile2, "%d,%f",&cid2, &mcgains)>0){
    mcG[cid2-1] = mcgains;
  }
  fclose(myfile2);

  //Read in cosmics gain values
  float ccosmic[NCRY]={};
  float cCosmic;
  int cid3;
  string line3;
  FILE *myfile3 = fopen("coeff/cosmic.txt", "r");
  while (fscanf(myfile3, "%d,%f",&cid3, &cCosmic)>0){
    ccosmic[cid3-1] = cCosmic;
  }
  fclose(myfile3);

  // open the root file histogram
  TFile *f = new TFile(Form("input_iter%d/FEE_c%d_p%d_10103.root",ITER,ITER,PERIOD));

  // make output file
  TCanvas *tcc = new TCanvas("tcc","fits to peak",800,800);
  tcc->SetFillColor(0);
  tcc->SetBorderMode(0);
  tcc->SetBorderSize(0);
  tcc->SetFrameFillColor(0);
  tcc->SetFrameBorderMode(0);
  gSystem->mkdir(Form("output_iter%d_p%d/crystal_plots",ITER,PERIOD), kTRUE);

  float MPV[NX][NY]={};
  TH1F *crystal[NX][NY];
  TF1 *lfit[NX][NY];
  float sigma[NX][NY]={};
  int rates[NX][NY]={};

  TCanvas *crystalSeedE[NX][NY];
  gROOT->SetBatch(kTRUE);
  tcc->Update();
  for (int jy=0; jy<NY; jy++)
  {
    // loop over crystal x
    for (int jx=0; jx<NX; jx++)
    {
      if (!ishole(jx,jy)){
        int id = xy2dbid(jx,jy);
        //make canvas for each crystal
        crystalSeedE[jx][jy] = new TCanvas(Form("crystalSeedE_%d_%d",jx,jy),Form("crystalSeedE_%d_%d",jx,jy),600,400);

        //get the energy spectra for each crystal
        crystal[jx][jy] = (TH1F*)f->Get(Form("%3d",id));

        rates[jx][jy] = crystal[jx][jy]->GetEntries();

        if (rates[jx][jy] >= 1000) {
          lfit[jx][jy]= CBFit(crystal[jx][jy]);
          crystal[jx][jy]->Fit(lfit[jx][jy],"0QR");

          MPV[jx][jy] = lfit[jx][jy]->GetParameter(2)/EBEAM;
          sigma[jx][jy] =  lfit[jx][jy]->GetParameter(3);

          //quality control check
          //if (sigma[jx][jy]>0.08 || sigma[jx][jy]<0) // original cut for 1.05 GeV beam
          if (sigma[jx][jy]> 0.24 || sigma[jx][jy]<0) {
            MPV[jx][jy] = -999;
            sigma[jx][jy] = -999;
          }

          gStyle->SetOptStat(1111);
          gStyle->SetOptFit(111);
          crystal[jx][jy]->SetTitle(Form("Crystal %d (ix=%d, iy=%d);Cluster Energy (GeV);Counts",id,calcIX(jx),calcIY(jy)));
          crystal[jx][jy]->Draw();
          lfit[jx][jy]->Draw("lsame");
          crystalSeedE[jx][jy]->Update();

          // Legend positioning and formatting for single crystal energy plots
          TPaveStats *st = (TPaveStats*)crystal[jx][jy]->FindObject("stats");
          if (st) {
              st->SetX1NDC(0.70); st->SetX2NDC(0.98);
              st->SetY1NDC(0.70); st->SetY2NDC(0.99);
              st->SetTextSize(0.038);
              crystalSeedE[jx][jy]->Modified();
          }

          if (MPV[jx][jy] != -999) {
            crystalSeedE[jx][jy]->SaveAs(Form("output_iter%d_p%d/crystal_plots/crystal_%d.png",ITER,PERIOD,id));
          }
          crystalSeedE[jx][jy]->Close();
        }
        else {//revert to cosmics
          MPV[jx][jy] = -999;
          sigma[jx][jy] = -999;

          // low-entry crystal, no fit — just draw raw histogram
          crystal[jx][jy]->SetTitle(Form("Crystal %d (ix=%d, iy=%d) - insufficient entries;Cluster Energy (GeV);Counts",id,calcIX(jx),calcIY(jy)));
          crystal[jx][jy]->Draw();
          crystalSeedE[jx][jy]->Update();
          crystalSeedE[jx][jy]->Close();
        }//end else
      }//end !ishole
    }//end loop x
  }//end loop y

  ////////////////////////
  //Plot energy fraction//
  ////////////////////////
  TCanvas *tOff=new TCanvas("tOff","EnergyFraction",1200,800);
  tOff->cd();
  TH2D *ECal=new TH2D("ECal", "Elastic Energy Peak as Fraction of Beam E; seed ix;seed iy", 47,-23.5,23.5, 11,-5.5,5.5);
  ECal->SetMinimum(0.2);

  ECal->GetYaxis()->SetNdivisions(11);
  for (int iy=0; iy<NY; iy++)
  {
    // loop over crystal x
    for (int ix=0; ix<NX; ix++)
    {
      if (!ishole(ix,iy)){
        int id =  xy2dbid(ix,iy);
        ECal->SetBinContent(ECal->GetXaxis()->FindBin(calcIX(ix)), ECal->GetYaxis()->FindBin(calcIY(iy)), MPV[ix][iy]);
        ECal->Draw("colz");
      }
    }
  }
  gStyle->SetOptStat(0);
  tOff->Update();
  tOff->Print(Form("output_iter%d_p%d/EnergyFraction.png",ITER,PERIOD));
  tOff->Close();

  ////////////////////////////////////////
  //Plot the occupancies in each crystal
  ////////////////////////////////////////
  TCanvas *occup = new TCanvas("occup","Occupancies",1200,800);
  occup->cd();
  TH2D *ECalF=new TH2D("ECalF", "Crystal Occupancies; seed ix; seed iy", 47,-23.5,23.5, 11,-5.5,5.5);
  ECalF->SetMinimum(1.0);

  ECalF->GetYaxis()->SetNdivisions(11);
  cout<<"Printing occupanices"<<endl;
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
      {
        if (!ishole(ix,iy)){
          int id = xy2dbid(ix,iy);
          ECalF->SetBinContent(ECalF->GetXaxis()->FindBin(calcIX(ix)), ECalF->GetYaxis()->FindBin(calcIY(iy)), rates[ix][iy]);
          ECalF->Draw("colz");
        }
      }
    }
  gStyle->SetOptStat(0);
  occup->Update();
  occup->Print(Form("output_iter%d_p%d/CrystalOccupancies.png",ITER,PERIOD));
  occup->Close();
  f->Close();


  //////////////////////////////////////////////////////////////
  //////////////// Write out iteration factor //////////////////
  //////////////////////////////////////////////////////////////
  cout<<"Printing iteration factor"<<endl;
  //iteration factor:
  FILE *c = fopen(Form("output_iter%d_p%d/c%d.txt",ITER,PERIOD,ITER),"w");
  //global running gain:
  FILE *cc = fopen(Form("output_iter%d_p%d/cGlobal_%d.txt",ITER,PERIOD,ITER),"w");
  //ecal gains copy, with zeroed-out dead crystals:
  FILE *eg = fopen(Form("output_iter%d_p%d/ecalGains_%d.txt",ITER,PERIOD,ITER),"w");
  fprintf(eg,"# COMMENT\n");
  //ecal gains copy, dead crystals zeroed and edge rows (y=-5,-1,1,5) set to 1.0 (uncorrected):
  FILE *egr = fopen(Form("output_iter%d_p%d/ecalGains_rowexcl_%d.txt",ITER,PERIOD,ITER),"w");
  fprintf(egr,"# COMMENT\n");
  int deadCrystals[5] = {153,198,267,275,334};

  for (int iy=0; iy<NY; iy++) {
    // loop over crystal x
    for (int ix=0; ix<NX; ix++) {
      if (!ishole(ix,iy)) {
        int id = xy2dbid(ix,iy);

        bool isDead = false;
        for (int ideadi=0; ideadi<5; ideadi++) {
          if (id==deadCrystals[ideadi]) isDead = true;
        }
        int row = calcIY(iy);
        bool isEdgeRow = (row==-5 || row==-1 || row==1 || row==5);

        if (MPV[ix][iy] == -999 || mcG[id-1] == -999) {
            // fit failed — carry forward previous factor unchanged
            fprintf(c,"%d,%.4f\n",id,prevC[id-1]);
            fprintf(cc,"%d,%.4f\n",id,ccosmic[id-1]*prevC[id-1]);
            fprintf(eg,"%d,%.4f\n",id,isDead ? 0.0 : prevC[id-1]);
            fprintf(egr,"%d,%.4f\n",id,isDead ? 0.0 : (isEdgeRow ? 1.0 : prevC[id-1]));
        }
        else {
            fprintf(c,"%d,%.4f\n",id,prevC[id-1]*mcG[id-1]/MPV[ix][iy]);
            fprintf(cc,"%d,%.4f\n",id,ccosmic[id-1]*prevC[id-1]*mcG[id-1]/MPV[ix][iy]);
            fprintf(eg,"%d,%.4f\n",id,isDead ? 0.0 : prevC[id-1]*mcG[id-1]/MPV[ix][iy]);
            fprintf(egr,"%d,%.4f\n",id,isDead ? 0.0 : (isEdgeRow ? 1.0 : prevC[id-1]*mcG[id-1]/MPV[ix][iy]));
        }
      }
    }
  }
  fclose(c);
  fclose(cc);
  fclose(eg);
  fclose(egr);
 
  //////////////////////////////////////////////////////////////
  //Make plot to show peak position by crystal, sigma by crystal
  //////////////////////////////////////////////////////////////
  Double_t xPos[NX]={};

  for (Int_t i=0;i<NX; i++){
    xPos[i] = calcIX(i);
  }
  Double_t row[NY][NX]={};

  for (int iy=0; iy<NY; iy++){
    for (int ix=0; ix<NX; ix++){
      if (!ishole(ix,iy)){
        int id = xy2dbid(ix,iy);
        row[iy][ix] = mcG[id-1]/MPV[ix][iy];
      }
      else {row[iy][ix]=-1;}
    }
  }

  TMultiGraph *mg = new TMultiGraph();
  mg->SetMinimum(0.0);
  mg->SetMaximum(1.5);

  TFile *out=new TFile("scratch.root","RECREATE");
  TCanvas *scr=new TCanvas("scr","xxxx",1200,800);
  scr->cd();

  TGraphErrors *grp[NY];
  for (int yy=0;yy<NY;yy++){
    grp[yy]= new TGraphErrors(NX,xPos,row[yy],0,0);
    grp[yy]->SetLineColor(yy);
    grp[yy]->SetMarkerStyle(31);
    grp[yy]->SetMarkerSize(1.5);
    grp[yy]->SetMarkerColor(yy);
    grp[yy]->Write();
    mg->Add(grp[yy]);
  }

  mg->Draw("ap");
  mg->SetTitle("Elastic Peak Position");
  mg->GetXaxis()->SetTitle("x crystal index, viewed from back of calorimeter");
  mg->GetYaxis()->SetTitle("MC Elastic Peak / Data Elastic Peak");


  TLegend * leg = new TLegend(0.85,0.55,0.95,0.92);
  leg->SetHeader("Row in y");
  leg->AddEntry(grp[9],"y=5","lep");
  leg->AddEntry(grp[8],"y=4","lep");
  leg->AddEntry(grp[7],"y=3","lep");
  leg->AddEntry(grp[6],"y=2","lep");
  leg->AddEntry(grp[5],"y=1","lep");
  leg->AddEntry(grp[4],"y=-1","lep");
  leg->AddEntry(grp[3],"y=-2","lep");
  leg->AddEntry(grp[2],"y=-3","lep");
  leg->AddEntry(grp[1],"y=-4","lep");
  leg->AddEntry(grp[0],"y=-5","lep");
  leg->Draw();

  scr->Update();
  scr->Print(Form("output_iter%d_p%d/Elasticmean.png",ITER,PERIOD));
  scr->Close();
}
