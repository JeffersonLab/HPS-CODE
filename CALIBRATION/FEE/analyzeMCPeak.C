/////////////////////////////////////////////////////////////////////////////////
/* 
Date: 18 July 2017
Author: Holly Szumila, hszumila@jlab.org
Modified by: Erbaz Khan (erbaz.khan@unh.edu) - Date: 10 July 2026
Purpose: This code obtains the ratio of the measured elastic peak in MC to the beam energy. 
How to run: In root, run .L thisCode.C fitMCPeaks()
Reads in:
-root histograms
Outputs:
-output_MC/MC_constant.txt -> Copy this to coeff/MC_constant.txt. It's used by analyzeFeePeak.C
to calculate the FEE correction factors.
-png fits (must check) 
 */
////////////////////////////////////////////////////////////////////////////////
#define NX 46
#define NY 10
#define NCRY 442

#include "util/utilities.h"
// const double EBEAM = 1.05;
const double EBEAM = 4.55;

//Gets the max bin in each crystal histogram and plots. 
void fitMCPeaks(){

  // open the root file histogram
  TFile *f = new TFile("input_MC/FEE_MC.root");

  // make output file
  TCanvas *tcc = new TCanvas("tcc","fits to peak",800,800);
  tcc->SetFillColor(0);
  tcc->SetBorderMode(0);
  tcc->SetBorderSize(0);
  tcc->SetFrameFillColor(0);
  tcc->SetFrameBorderMode(0);
  gSystem->mkdir("output_MC/crystal_plots", kTRUE);

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
		if (sigma[jx][jy]>0.20 || sigma[jx][jy]<0)
		  {
		    MPV[jx][jy] = -999;
		    sigma[jx][jy] = -999;
		  }

		gStyle->SetOptStat(1111);
		gStyle->SetOptFit(111);
		crystal[jx][jy]->SetTitle(Form("Crystal %d (ix=%d, iy=%d);Cluster Energy (GeV);Counts",id,calcIX(jx),calcIY(jy)));
		crystal[jx][jy]->Draw();
		lfit[jx][jy]->Draw("lsame");
		crystalSeedE[jx][jy]->Update();

		if (MPV[jx][jy] != -999) {
		  crystalSeedE[jx][jy]->SaveAs(Form("output_MC/crystal_plots/crystal_%d.png",id));
		}
		crystalSeedE[jx][jy]->Close();
	      }
	      else{//revert to cosmics
		MPV[jx][jy] = -999;
		sigma[jx][jy] = -999;

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
  tOff->Print("output_MC/EnergyFraction.png");
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
  occup->Print("output_MC/CrystalOccupancies.png");
  occup->Close();
  f->Close();


  //////////////////////////////////////////////////////////////
  //Write out MC ratio factor//////////////////////////////////
  //////////////////////////////////////////////////////////////
  FILE *c = fopen("output_MC/MC_constant.txt","w");
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    int id = xy2dbid(ix,iy);
	    fprintf(c,"%d,%.4f\n",id,MPV[ix][iy]);

	  }
	}
    }

}
