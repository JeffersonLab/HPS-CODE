/////////////////////////////////////////////////////////////////////////////////
/* 
Date: 1 Feb 2016
Author: Holly Szumila, hszumila@jlab.org
Purpose: This code performs a single iteration of the FEE claibration. 
How to run: In root, run .L thisCode.C fitPeaks(N) where N is the iteration number, starting with 1. 
Reads in:
-mc constants
-root histograms from current iteration
-converter for index to coordinates
-previous global total
-cosmic gains
Outputs:
-next iterative factor
-updated global coefficient, cGlobal, this excludes cosmics (not for final db)
-pdf containing fits (must check)
-updated 
 */
////////////////////////////////////////////////////////////////////////////////

#include "util/utilities.h"
const double EBEAM = 1.05;

//Gets the max bin in each crystal histogram and plots. 
void fitPeaks(int ITER){

  //Read in iteration coefficients (for iteration 0, =1):
  float prevC[46][10]={};
  float previous;
  int idX1, idY1;
  string line1;
  if (ITER>1){
    std::fstream myfile1(Form("coeff/c%d.txt",ITER-1), std::ios_base::in);
    while(getline(myfile1, line1)){
      myfile1>>idX1>>idY1>>previous;
      prevC[idX1][idY1] = previous;
    }
  }
  else {
    prevC[idX1][idY1] = 1.0;
  }
    
  //Read in MC constant fractions:
  std::fstream myfile2("coeff/MC_constant.txt", std::ios_base::in);
  float mcG[46][10]={};
  float mcgains;
  int idX2, idY2;
  string line2;
  while(getline(myfile2, line2)){
    myfile2>>idX2>>idY2>>mcgains;
    mcG[idX2][idY2] = mcgains;
  }

  //Read in crystal id index converter
  std::fstream myfile3("util/indexConverter.txt", std::ios_base::in);
  int cid[47][11]={};
  int index;
  int idX3, idY3;
  string line3;
  while(getline(myfile3, line3)){
    myfile3>>idX3>>idY3>>index;
    cid[idX3][idY3] = index;
  }

  //Read in cosmics gain values
  std::fstream myfile4("coeff/cosmic.txt", std::ios_base::in);
  int ccosmic[46][10]={};
  int cCosmic;
  int idX4, idY4;
  string line4;
  while(getline(myfile4, line4)){
    myfile4>>idX4>>idY4>>cCosmic;
    ccosmic[idX4][idY4] = cCosmic;
  }

  // open the root file histogram
  TFile *f = new TFile(Form("input_iter%d/FEE_c%d.root",ITER,ITER));

  float MPV[47][11]={};
  TH1F *crystal[47][11];
  TF1 *lfit[47][11];
  float sigma[47][11]={};
  int rates[47][11]={};

  TCanvas *crystalSeedE[47][11];
  gROOT->SetBatch(kTRUE); 

  for (int jy=0; jy<11; jy++)
    {
      // loop over crystal x
      for (int jx=0; jx<47; jx++)
	{
	  int id = cid[jx][jy];
	  
	  if (id!=0){
	    
	    //make canvas for each crystal
	    crystalSeedE[jx][jy] = new TCanvas(Form("crystalSeedE_%d_%d",jx-23,jy-5),Form("crystalSeedE_%d_%d",jx-23,jy-5),600,400);
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
	      crystal[jx][jy]->SetTitle(Form("Crystal_%d_%d",jx-23,jy-5));
	      lfit[jx][jy]->Draw("lsame");	      
	      crystalSeedE[jx][jy]->Update();
	      
	      if (jx==0 &&jy==0){
		crystalSeedE[jx][jy]->Print(Form("output_iter%d/FEEfits.pdf(",ITER));
	      }
	      else if (jy==10&&jx==46){
		crystalSeedE[jx][jy]->Print(Form("output_iter%d/FEEfits.pdf)",ITER));
	      }
	      else {
		crystalSeedE[jx][jy]->Print(Form("output_iter%d/FEEfits.pdf",ITER));
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
	      
	      if (jx==0 &&jy==0){
		crystalSeedE[jx][jy]->Print(Form("output_iter%d/FEEfits.pdf(",ITER));
	      }
	      else if (jy==10&&jx==46){
		crystalSeedE[jx][jy]->Print(Form("output_iter%d/FEEfits.pdf)",ITER));
	      }
	      else {
		crystalSeedE[jx][jy]->Print(Form("output_iter%d/FEEfits.pdf",ITER));
	      }
	      
	      crystalSeedE[jx][jy]->Close();
	    }//end else
	   
	  }//end int id
	  
	}//end loop x
    }//end loop y
	  

  
  ////////////////////////
  //Plot energy fraction//
  ////////////////////////
  TCanvas *tOff=new TCanvas("tOff","EnergyFraction",1200,800);
  tOff->cd();
  TH2D *ECal=new TH2D("ECal", "Elastic Energy Peak as Fraction of Beam E", 50,-1.5,48.5, 13,-1.5,11.5);
  ECal->SetMinimum(0.2);
  for (int iy=0; iy<11; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<47; ix++)
	{

	  int id = cid[ix][iy];
	  if(id !=0){
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
  TH2D *ECalF=new TH2D("ECalF", "Crystal Occupancies", 50,-1.5,48.5, 13,-1.5,11.5);
  ECalF->SetMinimum(1.0);
  occup->SetLogz();

  for (int iy=0; iy<11; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<47; ix++)
	{
	  int id = cid[ix][iy];
	  if (id!=0){

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
  FILE *c = fopen(Form("output_iter%d/c%d.txt",ITER,ITER),"a+");
  for (int ny=0; ny<11; ny++)
    {
      // loop over crystal x
      for (int nx=0; nx<47; nx++)
	{
	  if(!(ny>=4&&ny<=6&&nx>12&&nx<22)){//skip the hole
	    if (ny<5 && nx<23) {
	      if (MPV[nx][ny]>0){
		fprintf(c,"%d\t %d\t %.4f\n",nx,ny,prevC[nx][ny]*mcG[nx][ny]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx,ny,prevC[nx][ny]);}
	    }
	    if (ny>5 && nx<23) {
	      if (MPV[nx][ny]>0){
		fprintf(c,"%d\t %d\t %.4f\n",nx,ny-1,prevC[nx][ny-1]*mcG[nx][ny-1]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx,ny-1,prevC[nx][ny-1]);}
	    }
	    if (ny<5 && nx>23) {
	      if (MPV[nx][ny]>0){
		fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny,prevC[nx-1][ny]*mcG[nx-1][ny]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny,prevC[nx-1][ny]);}
	    }
	    if (ny>5 && nx>23) {
	      if (MPV[nx][ny]>0){		
		fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny-1,prevC[nx-1][ny-1]*mcG[nx-1][ny-1]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny-1,prevC[nx-1][ny-1]);}
	    }
	  }
	}
    }
  //////////////////////////////////////////////////////////////////////////////////
  //Write out global, running gain. Includes cosmics. Not used to iterate.//////////
  //////////////////////////////////////////////////////////////////////////////////
  FILE *c = fopen(Form("coeff/cGlobal_%d.txt",ITER),"a+");
  for (int ny=0; ny<11; ny++)
    {
      // loop over crystal x
      for (int nx=0; nx<47; nx++)
	{
	  if(!(ny>=4&&ny<=6&&nx>12&&nx<22)){//skip the hole
	    if (ny<5 && nx<23) {
	      if (MPV[nx][ny]>0){
		fprintf(c,"%d\t %d\t %.4f\n",nx,ny,ccosmic[nx][ny]*prevC[nx][ny]*mcG[nx][ny]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx,ny,ccosmic[nx][ny]*prevC[nx][ny]);}
	    }
	    if (ny>5 && nx<23) {
	      if (MPV[nx][ny]>0){
		fprintf(c,"%d\t %d\t %.4f\n",nx,ny-1,ccosmic[nx][ny-1]*prevC[nx][ny-1]*mcG[nx][ny-1]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx,ny-1,ccosmic[nx][ny-1]*prevC[nx][ny-1]);}
	    }
	    if (ny<5 && nx>23) {
	      if (MPV[nx][ny]>0){
		fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny,ccosmic[nx-1][ny]*prevC[nx-1][ny]*mcG[nx-1][ny]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny,ccosmic[nx-1][ny]*prevC[nx-1][ny]);}
	    }
	    if (ny>5 && nx>23) {
	      if (MPV[nx][ny]>0){		
		fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny-1,ccosmic[nx-1][ny-1]*prevC[nx-1][ny-1]*mcG[nx-1][ny-1]/MPV[nx][ny]);}
	      else {fprintf(c,"%d\t %d\t %.4f\n",nx-1,ny-1,ccosmic[nx-1][ny-1]*prevC[nx-1][ny-1]);}
	    }
	  }
	}
    }
  
  //////////////////////////////////////////////////////////////
  //Make plot to show peak position by crystal, sigma by crystal
  //////////////////////////////////////////////////////////////
  const Int_t n = 47;
  Double_t xPos[n]={};

for (Int_t i=0;i<47; i++){
  if(i<23 || i>23){xPos[i] = i-23;}
  else {xPos[i]=0;}
  }

  Double_t p5[n]={},p4[n]={},p3[n]={},p2[n]={},p1[n]={},m1[n]={},m2[n]={},m3[n]={},m4[n]={},m5[n]={};

for (int ix=-23;ix<=23;ix++)
    {
      if (ix<23){
	p5[ix+23] = mcG[ix+23][9]/MPV[ix+23][10];

	p4[ix+23] = mcG[ix+23][8]/MPV[ix+23][9];

	p3[ix+23] = mcG[ix+23][7]/MPV[ix+23][8];
	
	p2[ix+23] = mcG[ix+23][6]/MPV[ix+23][7];
	
	if (!(ix>12&&ix<22)){
	  p1[ix+23] = mcG[ix+23][5]/MPV[ix+23][6];
	  
	  m1[ix+23] = mcG[ix+23][4]/MPV[ix+23][4];
	}
	m2[ix+23] = mcG[ix+23][3]/MPV[ix+23][3];
	
	m3[ix+23] = mcG[ix+23][2]/MPV[ix+23][2];
	
	m4[ix+23] = mcG[ix+23][1]/MPV[ix+23][1];
	
	m5[ix+23] = mcG[ix+23][0]/MPV[ix+23][0];
      }
      if (ix>23){
	p5[ix+23] = mcG[ix+22][9]/MPV[ix+23][10];

	p4[ix+23] = mcG[ix+22][8]/MPV[ix+23][9];

	p3[ix+23] = mcG[ix+22][7]/MPV[ix+23][8];
	
	p2[ix+23] = mcG[ix+22][6]/MPV[ix+23][7];
	
	if (!(ix>12&&ix<22)){

	  p1[ix+23] = mcG[ix+22][5]/MPV[ix+23][6];
	
	  m1[ix+23] = mcG[ix+22][4]/MPV[ix+23][4];
	}
	m2[ix+23] = mcG[ix+22][3]/MPV[ix+23][3];
	
	m3[ix+23] = mcG[ix+22][2]/MPV[ix+23][2];
	
	m4[ix+23] = mcG[ix+22][1]/MPV[ix+23][1];
	
	m5[ix+23] = mcG[ix+22][0]/MPV[ix+23][0];
      }
    }
TMultiGraph *mg = new TMultiGraph();
  mg->SetMinimum(0.0);
  mg->SetMaximum(1.5);
 
  
  //y=5
  TFile *out=new TFile("scratch.root","RECREATE");
  TCanvas *scr=new TCanvas("scr","xxxx",1200,800);
  scr->cd();
  
  TGraphErrors *grp5 = new TGraphErrors(n,xPos,p5,0,0);
  grp5->SetName("grp5");
  grp5->SetLineColor(7);
  grp5->SetMarkerStyle(31);
  grp5->SetMarkerSize(1.5);
  grp5->SetMarkerColor(7);
  // grp5->Draw("AP");
  grp5->Write();
  mg->Add(grp5);
  

//y=4
  TGraphErrors *grp4 = new TGraphErrors(n,xPos,p4,0,0);
  grp4->SetName("grp4");
  grp4->SetMinimum(0.01);
  grp4->SetMaximum(0.03);
  grp4->SetMarkerStyle(31);
  grp4->SetMarkerSize(1.5);
  grp4->SetMarkerColor(40);
  grp4->SetLineColor(40);
  //  grp4->Draw("AP");
  grp4->Write();
  mg->Add(grp4);

//y=3
  TGraphErrors *grp3 = new TGraphErrors(n,xPos,p3,0,0);
  grp3->SetName("grp3");
  grp3->SetMinimum(0.01);
  grp3->SetMaximum(0.03);
  grp3->SetMarkerStyle(31);
  grp3->SetMarkerSize(1.5);
  grp3->SetMarkerColor(9);
  grp3->SetLineColor(9);
  //  grp3->Draw("AP");
  grp3->Write();
  mg->Add(grp3);


//y=2
  TGraphErrors *grp2 = new TGraphErrors(n,xPos,p2,0,0);
  grp2->SetName("grp2");
  grp2->SetMinimum(0.01);
  grp2->SetMaximum(0.03);
  grp2->SetMarkerStyle(31);
  grp2->SetMarkerSize(1.5);
  grp2->SetMarkerColor(8);
  grp2->SetLineColor(8);
  // grp2->Draw("AP");
  grp2->Write();
  mg->Add(grp2);
  

//y=1

  TGraphErrors *grp1 = new TGraphErrors(n,xPos,p1,0,0);
  grp1->SetName("grp1");
  grp1->SetMinimum(0.01);
  grp1->SetMaximum(0.03);
  grp1->SetMarkerStyle(31);
  grp1->SetMarkerSize(1.5);
  grp1->SetMarkerColor(1);
  grp1->SetLineColor(1);
  //  grp1->Draw("AP");
  grp1->Write();
  mg->Add(grp1);


//y=-1
  TGraphErrors *grm1 = new TGraphErrors(n,xPos,m1,0,0);
  grm1->SetName("grm1");
  grm1->SetMinimum(0.01);
  grm1->SetMaximum(0.03);
  grm1->SetMarkerStyle(31);
  grm1->SetMarkerSize(1.5);
  grm1->SetMarkerColor(2);
  grm1->SetLineColor(2);
  //  grm1->Draw("AP");
  grm1->Write();
  mg->Add(grm1);


//y=-2
  TGraphErrors *grm2 = new TGraphErrors(n,xPos,m2,0,0);
  grm2->SetName("grm2");
  grm2->SetMinimum(0.01);
  grm2->SetMaximum(0.03);
  grm2->SetMarkerStyle(31);
  grm2->SetMarkerSize(1.5);
  grm2->SetMarkerColor(3);
  grm2->SetLineColor(3);
  grm2->Draw("AP");
  grm2->Write();
  mg->Add(grm2);


//y=-3
  TGraphErrors *grm3 = new TGraphErrors(n,xPos,m3,0,0);
  grm3->SetName("grm3");
  grm3->SetMinimum(0.01);
  grm3->SetMaximum(0.03);
  grm3->SetMarkerStyle(31);
  grm3->SetMarkerSize(1.5);
  grm3->SetMarkerColor(4);
  grm3->SetLineColor(4);
  //  grm3->Draw("AP");
  grm3->Write();
  mg->Add(grm3);


//y=-4
  TGraphErrors *grm4 = new TGraphErrors(n,xPos,m4,0,0);
  grm4->SetName("grpm4");
  grm4->SetMinimum(0.01);
  grm4->SetMaximum(0.03);
  grm4->SetMarkerStyle(31);
  grm4->SetMarkerSize(1.5);
  grm4->SetMarkerColor(5);
  grm4->SetLineColor(5);
  //  grm4->Draw("AP");
  grm4->Write();
  mg->Add(grm4);


//y=-5

  TGraphErrors *grm5 = new TGraphErrors(n,xPos,m5,0,0);
  grm5->SetName("grm5");
  grm5->SetMinimum(0.01);
  grm5->SetMaximum(0.03);
  grm5->SetMarkerStyle(31);
  grm5->SetMarkerSize(1.5);
  grm5->SetMarkerColor(6);
  grm5->SetLineColor(6);
  // grm5->Draw("AP");
  grm5->Write();
  mg->Add(grm5);

  mg->Draw("ap");
  mg->SetTitle("Elastic Peak Position");
  mg->GetXaxis()->SetTitle("x crystal index, viewed from back of calorimeter");
  mg->GetYaxis()->SetTitle("MC Elastic Peak / Data Elastic Peak");


  TLegend * leg = new TLegend(0.3,0.65,0.48,0.95);
  leg->SetHeader("Row in y");
  leg->AddEntry("grp5","y=5","lep");
  leg->AddEntry("grp4","y=4","lep");
  leg->AddEntry("grp3","y=3","lep");
  leg->AddEntry("grp2","y=2","lep");
  leg->AddEntry("grp1","y=1","lep");
  leg->AddEntry("grm1","y=-1","lep");
  leg->AddEntry("grm2","y=-2","lep");
  leg->AddEntry("grm3","y=-3","lep");
  leg->AddEntry("grm4","y=-4","lep");
  leg->AddEntry("grm5","y=-5","lep");

  leg->Draw();
  
  scr->Update();
  scr->Print(Form("output_iter%d/Elasticmean.C",ITER));
  scr->Close();
  

}


