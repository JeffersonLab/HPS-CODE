/////////////////////////////////////////////////////////////////////////////////
/* 
Date: 18 July 2017
Author: Holly Szumila, hszumila@jlab.org
Purpose: This code performs a single iteration of the FEE claibration. 
How to run: In root, run .L thisCode.C fitPeaks(N) where N is the iteration number, starting with 1. 
Reads in:
-mc constants
-root histograms from current iteration
-previous global total
-cosmic gains
Outputs:
-next iterative factor
-updated global coefficient, cGlobal, this excludes cosmics (not for final db)
-pdf containing fits (must check) 
 */
////////////////////////////////////////////////////////////////////////////////
#define NX 46
#define NY 10
#define NCRY 442

#include "util/utilities.h"
const double EBEAM = 1.05;

//Gets the max bin in each crystal histogram and plots. 
void fitPeaks(int ITER){

  //Read in iteration coefficients (for iteration 0, =1):
  float prevC[NCRY]={};
  float previous;
  string line1;
  int cid1;
  if (ITER>1){
    FILE *myfile1 = fopen(Form("coeff/c%d.txt",ITER-1), "r");
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
  TFile *f = new TFile(Form("input_iter%d/FEE_c%d.root",ITER,ITER));

  // make output file
  TCanvas *tcc = new TCanvas("tcc","fits to peak",800,800);
  tcc->SetFillColor(0);
  tcc->SetBorderMode(0);
  tcc->SetBorderSize(0);
  tcc->SetFrameFillColor(0);
  tcc->SetFrameBorderMode(0);
  std::string pdf_file_name = Form("output_iter%d/FEEfits.pdf",ITER);

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
		lfit[jx][jy]= CBFit(crystal[jx][jy]);
		crystal[jx][jy]->Fit(lfit[jx][jy],"0QR");
		
		MPV[jx][jy] = lfit[jx][jy]->GetParameter(2)/EBEAM;
		sigma[jx][jy] =  lfit[jx][jy]->GetParameter(3);
		
		//quality control check
		if (sigma[jx][jy]>0.08 || sigma[jx][jy]<0)
		  {
		    MPV[jx][jy] = -999;
		    sigma[jx][jy] = -999;
		  }
		
		// Global style settings	      
		crystalSeedE[jx][jy]->cd(2);
		gStyle->SetOptFit(111);
		crystal[jx][jy]->Draw();
		crystal[jx][jy]->SetTitle(Form("Crystal_%d_%d",jx,jy));
		lfit[jx][jy]->Draw("lsame");	      
		crystalSeedE[jx][jy]->Update();
		
		if (id==1){
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}
		else if (id==442){
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}
		else {
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}
		crystalSeedE[jx][jy]->Close();
	      }
	      else{//revert to cosmics
		MPV[jx][jy] = -999;
		sigma[jx][jy] = -999;
		
		// Global style settings
		crystalSeedE[jx][jy]->cd(2);
		crystal[jx][jy]->Draw();
		crystalSeedE[jx][jy]->Update();
		
		if (id==1){
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}
		else if (id==442){
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}
		else {
		  crystalSeedE[jx][jy]->Print((pdf_file_name+"(").c_str());
		}		
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
  TH2D *ECal=new TH2D("ECal", "Elastic Energy Peak as Fraction of Beam E", 49,-1.5,47.5, 12,-1.5,10.5);
  ECal->SetMinimum(0.2);
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    int id =  xy2dbid(ix,iy);
	    ECal->SetBinContent(ix+3,iy+2,MPV[ix][iy]);
	    ECal->Draw("colz");	  
	  }
	}
    }
  gStyle->SetOptStat(0);
  tOff->Update();
  tOff->Print(Form("output_iter%d/EnergyFraction.png",ITER));
  tOff->Close();
  
  ////////////////////////////////////////
  //Plot the occupancies in each crystal
  ////////////////////////////////////////
  TCanvas *occup = new TCanvas("occup","Occupancies",1200,800);
  occup->cd();
  TH2D *ECalF=new TH2D("ECalF", "Crystal Occupancies", 49,-1.5,47.5, 12,-1.5,10.5);
  ECalF->SetMinimum(1.0);
  cout<<"Printing occupanices"<<endl;
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    int id = xy2dbid(ix,iy);		
	    ECalF->SetBinContent(ix+3,iy+2,rates[ix][iy]);
	    ECalF->Draw("colz");	  
	  }  
	}
    }
  gStyle->SetOptStat(0);
  occup->Update();
  occup->Print(Form("output_iter%d/CrystalOccupancies.png",ITER));
  occup->Close();
  f->Close();


  //////////////////////////////////////////////////////////////
  //Write out iteration factor//////////////////////////////////
  //////////////////////////////////////////////////////////////
  cout<<"Printing iteration factor"<<endl;
  //iteration factor:
  FILE *c = fopen(Form("output_iter%d/c%d.txt",ITER,ITER),"a+");
  //global running gain:
  FILE *cc = fopen(Form("coeff/cGlobal_%d.txt",ITER),"a+");
  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  if (!ishole(ix,iy)){
	    int id = xy2dbid(ix,iy);
	    fprintf(c,"%d,%.4f\n",id,prevC[id-1]*mcG[id-1]/MPV[ix][iy]);
	    fprintf(cc,"%d,%.4f\n",id,ccosmic[id-1]*prevC[id-1]*mcG[id-1]/MPV[ix][iy]);

	  }
	}
    }

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


  TLegend * leg = new TLegend(0.3,0.65,0.48,0.95);
  leg->SetHeader("Row in y");
  leg->AddEntry(Form("grp[%d]",9),"y=5","lep");
  leg->AddEntry(Form("grp[%d]",8),"y=4","lep");
  leg->AddEntry(Form("grp[%d]",7),"y=3","lep");
  leg->AddEntry(Form("grp[%d]",6),"y=2","lep");
  leg->AddEntry(Form("grp[%d]",5),"y=1","lep");
  leg->AddEntry(Form("grp[%d]",4),"y=-1","lep");
  leg->AddEntry(Form("grp[%d]",3),"y=-2","lep");
  leg->AddEntry(Form("grp[%d]",2),"y=-3","lep");
  leg->AddEntry(Form("grp[%d]",1),"y=-4","lep");
  leg->AddEntry(Form("grp[%d]",0),"y=-5","lep");
  leg->Draw();
  
  scr->Update();
  scr->Print(Form("output_iter%d/Elasticmean.C",ITER));
  scr->Close();
}
