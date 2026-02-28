/////////////////////////////////////////////////////////////////////////////////
/* 
Date: 18 July 2017
Author: Holly Szumila, hszumila@jlab.org
Purpose: This code obtains the ratio of the measured elastic peak in MC to the beam energy. 
How to run: In root, run .L thisCode.C fitMCPeaks()
Reads in:
-root histograms
Outputs:
-coeff/MC_constant.txt
-pdf containing fits (must check) 
 */
////////////////////////////////////////////////////////////////////////////////
#define NX 46
#define NY 10
#define NCRY 442

#include "util/utilities.h"
const double EBEAM = 4.556;

//Gets the max bin in each crystal histogram and plots. 
void fitMCPeaks(){
  gStyle->SetStatX(0.4);
  // open the root file histogram
  TFile *f = new TFile("input_MC/FEE_MC.root");

  // make output file
  TCanvas *tcc = new TCanvas("tcc","fits to peak",800,800);
  tcc->SetFillColor(0);
  tcc->SetBorderMode(0);
  tcc->SetBorderSize(0);
  tcc->SetFrameFillColor(0);
  tcc->SetFrameBorderMode(0);
  std::string pdf_file_name = "output_MC/FEEfits.pdf";
  std::string oroot_file_name = "output_MC/FEEfits.root";
  TFile *fout=new TFile(oroot_file_name.c_str(),"recreate");
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
	      crystalSeedE[jx][jy]->Divide(2,1);
	  
	      //get the energy spectra for each crystal	    
	      crystal[jx][jy] = (TH1F*)f->Get(Form("%3d",id));
	      
	      rates[jx][jy] = crystal[jx][jy]->GetEntries(); 
	      
	      crystalSeedE[jx][jy]->cd(1);	  
	      gStyle->SetOptStat(1111);	
	      crystal[jx][jy]->Draw();
	      
	      if (rates[jx][jy] >= 1000) {
		lfit[jx][jy]= CBFit(crystal[jx][jy],1);
		lfit[jx][jy]->SetName(Form("%3d",id));
		crystal[jx][jy]->Fit(lfit[jx][jy],"0QR");

	
		//do again with proper good range
		MPV[jx][jy] = lfit[jx][jy]->GetParameter(2);
		sigma[jx][jy] =  lfit[jx][jy]->GetParameter(3);
		lfit[jx][jy]->SetRange(	MPV[jx][jy]-sigma[jx][jy],MPV[jx][jy]+4*sigma[jx][jy]);

		crystal[jx][jy]->Fit(lfit[jx][jy],"0QR");
		MPV[jx][jy] = lfit[jx][jy]->GetParameter(2)/EBEAM;
		sigma[jx][jy] =  lfit[jx][jy]->GetParameter(3);

		cout<<jx<<" "<<jy<<" "<<	MPV[jx][jy]<<" "<<sigma[jx][jy]<<endl;
		if ((jy==0)&&(jx==0)){
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}
		
		//quality control check
		if (sigma[jx][jy]>0.2)
		  {
		    MPV[jx][jy] = -999;
		    sigma[jx][jy] = -999;
		  }
		
		// Global style settings	      
		crystalSeedE[jx][jy]->cd(2);
		gStyle->SetOptFit(111);
		crystal[jx][jy]->Draw();
		crystal[jx][jy]->SetTitle(Form("Crystal_%d_%d",calcIX(jx),calcIY(jy)));
		lfit[jx][jy]->Draw("lsame");	      
		crystalSeedE[jx][jy]->Update();
		
	
		crystalSeedE[jx][jy]->Print((pdf_file_name).c_str());
		
		 
	
	      }
	      else{//revert to cosmics
		MPV[jx][jy] = -999;
		sigma[jx][jy] = -999;
		
		// Global style settings
		crystalSeedE[jx][jy]->cd(2);
		crystal[jx][jy]->Draw();
		crystalSeedE[jx][jy]->Update();
		
		
		crystalSeedE[jx][jy]->Print((pdf_file_name).c_str());
	      }
	      fout->cd();
	      crystalSeedE[jx][jy]->Write();
	      crystal[jx][jy]->Write();
	      
	      if ((jx==(NX-1))&&(jy==(NY-1))){
		cout<<"CLOSING PDF"<<endl;
		crystalSeedE[jx][jy]->Print((pdf_file_name+")").c_str());
	      }
	  
	  }//end !ishole
	}//end loop x
    }//end loop y
  
  ////////////////////////
  //Plot energy fraction//
  ////////////////////////
  TCanvas *tOff=new TCanvas("tOff","EnergyFraction",1200,800);
  tOff->cd();
  TH2D *ECal=new TH2D("ECal", "Elastic Energy Peak as Fraction of Beam E", 47,-23.5,23.5, 11,-5.5,5.5);
  ECal->SetMinimum(0.5);
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    int id =  xy2dbid(ix,iy);
	    cout<<ix<<" "<<iy<<" "<<MPV[ix][iy]<<endl;
	    if (MPV[ix][iy]>0)	    ECal->Fill(calcIX(ix),calcIY(iy),MPV[ix][iy]);
	 
	  }
	}
    }
  ECal->Draw("colz");	  
  gStyle->SetOptStat(0);
  tOff->Update();
  fout->cd();
  tOff->Write();
  tOff->Print("output_MC/EnergyFraction.png");
  tOff->Close();
  
  ////////////////////////////////////////
  //Plot the occupancies in each crystal
  ////////////////////////////////////////
  TCanvas *occup = new TCanvas("occup","Occupancies",1200,800);
  occup->cd();
  TH2D *ECalF=new TH2D("ECalF", "Crystal Occupancies", 47,-23.5,23.5, 11,-5.5,5.5);
  ECalF->SetMinimum(1.0);
  cout<<"Printing occupanices"<<endl;
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    int id = xy2dbid(ix,iy);		
	    ECalF->Fill(calcIX(ix),calcIY(iy),rates[ix][iy]);
	    ECalF->Draw("colz");	  
	  }  
	}
    }
  gStyle->SetOptStat(0);
  occup->Update();
  fout->cd();
  occup->Write();
  occup->Print("output_MC/CrystalOccupancies.png");
  occup->Close();
  f->Close();

  fout->Write();
  fout->Close();

  //////////////////////////////////////////////////////////////
  //Write out MC ratio factor//////////////////////////////////
  //////////////////////////////////////////////////////////////
  FILE *c = fopen("coeff/MC_constant.txt","w");
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    fprintf(c,"%d %d %.4f\n",ix,iy,MPV[ix][iy]);

	  }
	}
    }

}
