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
-next iterative factor: this excludes cosmics (not for final db)
-updated global coefficient, cGlobal
-pdf containing fits (must check) 
 */
////////////////////////////////////////////////////////////////////////////////
#define NX 46
#define NY 10
#define NCRY 442

#include "util/utilities.h"
const double EBEAM = 4.556;

const double COSMIC_FACTOR = .908;


//Gets the max bin in each crystal histogram and plots. 
void fitPeaks(int ITER){
  gStyle->SetStatX(0.4);
  //Read in iteration coefficients (for iteration 0, =1):
  float prevC[ITER][NCRY];
  float previous;
  string line1;
  int cid1;
  int iix,iiy;
  std::string line;
 
  cout<<"GOING TO OPEN PREVIOUS COEFF"<<endl;
  if (ITER>1){
    for (int it=1;it<ITER;it++){
      ifstream myfile1(Form("coeff/c%d.txt",it));
      std::getline(myfile1, line ); //read first line
      while (!myfile1.eof()){
	std::getline(myfile1, line );
	std::replace(line.begin(),line.end(), ',', ' '); // replace all ',' to ' '
	std::istringstream linestrm(line);
	linestrm>>cid1>>previous;
	prevC[it][cid1-1] = previous;
      }
      myfile1.close();
    }
  }
  
  for (int ik=0; ik<NCRY; ik++){
    prevC[0][ik] = 1.0;
  }
  
  cout<<"DONE"<<endl;
  
  //Read in MC constant fractions:
  cout<<"GOING TO OPEN MC SAMPLING FRACTIONS"<<endl;
  float mcG[NCRY]={};
  float mcgains;
  int cid2;
  string line2;
  FILE *myfile2 = fopen("coeff/MC_constant.txt", "r");
  while (fscanf(myfile2, "%d%d%f",&iix,&iiy, &mcgains)>0){
    cid2=xy2dbid(iix,iiy);
    mcG[cid2-1] = mcgains;
  }
  fclose(myfile2);
  cout<<"DONE"<<endl;
  cout<<"GOING TO OPEN COSMIC GAINS"<<endl;
  //Read in cosmics gain values
  float ccosmic[NCRY]={};
  float cCosmic;
  int cid3;
  string line3;
  ifstream myfile3("coeff/cosmics.txt");
  while (!myfile3.eof()){
    std::getline(myfile3,line);
    std::replace(line.begin(),line.end(),',',' '); //replace all ',' to ' '
    std::istringstream linestrm(line);
    linestrm>>cid3>>cCosmic;
    ccosmic[cid3-1]=cCosmic;
    cout<<cid3<<" "<<cCosmic<<endl;
  }
  myfile3.close();
  cout<<"DONE"<<endl;
  cout<<"GOING TO OPEN THE ROOT FILE WITH DATA"<<endl;
 
  // open the root file histogram
  TFile *f = new TFile(Form("input_iter%d/FEE_c%d.root",ITER,ITER));

  TFile *fMC = new TFile("input_MC/FEE_MC.root");

  // make output file
  TCanvas *tcc = new TCanvas("tcc","fits to peak",800,800);
  tcc->SetFillColor(0);
  tcc->SetBorderMode(0);
  tcc->SetBorderSize(0);
  tcc->SetFrameFillColor(0);
  tcc->SetFrameBorderMode(0);
  std::string pdf_file_name = Form("output_iter%d/FEEfits%d.pdf",ITER,ITER);
  std::string oroot_file_name = Form("output_iter%d/FEEfits%d.root",ITER,ITER);
  TFile *fout=new TFile(oroot_file_name.c_str(),"recreate");
  
  float MPV[NX][NY]={};
  TH1F *crystal[NX][NY];
  TH1F *crystalMC[NX][NY];

  TH1F *crystalSeed[NX][NY];
  TH1F *crystalSeedMC[NX][NY];

  TGraph *calibPoint[NX][NY];
  
  TF1 *lfit[NX][NY];
  float sigma[NX][NY]={};
  int rates[NX][NY]={};

  TH2D *ECalStatus=new TH2D("ECalStatus", "Crystal status", 47,-23.5,23.5, 11,-5.5,5.5);

  TCanvas *crystalCanvas[NX][NY];
  gROOT->SetBatch(kTRUE); 
  tcc->Update();
  double maxData,maxMC;
  for (int jy=0; jy<NY; jy++)
    {
      // loop over crystal x
      for (int jx=0; jx<NX; jx++)
	{
	  if (!ishole(jx,jy)){
	      int id = xy2dbid(jx,jy);	      
	      //make canvas for each crystal
	      crystalCanvas[jx][jy] = new TCanvas(Form("crystalCanvas_%d_%d",jx,jy),Form("crystalCanvas_%d_%d",jx,jy),600,400);
	      crystalCanvas[jx][jy]->Divide(2,2);

	  
	      
	      //get the energy spectra for each crystal	    
	      crystal[jx][jy] = (TH1F*)f->Get(Form("%3d",id));
	      crystal[jx][jy]->SetTitle(Form("%d%d",calcIX(jx),calcIY(jy)));

	      crystalSeed[jx][jy] = (TH1F*)f->Get(Form("%3d_seed",id));
	      crystalSeed[jx][jy]->SetTitle(Form("%d%d_seed",calcIX(jx),calcIY(jy)));
	      
	      //get MC
	      crystalMC[jx][jy] = (TH1F*)fMC->Get(Form("%3d",id));
	      crystalSeedMC[jx][jy] = (TH1F*)fMC->Get(Form("%3d_seed",id));
	      rates[jx][jy] = crystal[jx][jy]->GetEntries(); 

	      //draw the seed hit
	      crystalCanvas[jx][jy]->cd(1);	  
	      gStyle->SetOptStat(1111);	
	      crystalSeed[jx][jy]->Draw();
	      maxData=crystalSeed[jx][jy]->GetMaximum();
	      maxMC=crystalSeedMC[jx][jy]->GetMaximum();
	      if ((maxMC>0)&&(maxData>0)){
		crystalSeedMC[jx][jy]->Scale(maxData/maxMC);
		crystalSeedMC[jx][jy]->SetLineColor(2);
		crystalSeedMC[jx][jy]->Draw("HISTSAME");
	      }

	     
	      
	      crystalCanvas[jx][jy]->cd(3);	  
	      gStyle->SetOptStat(1111);	
	      crystal[jx][jy]->Draw();

	      //Draw the MC for comparison
	      maxData=crystal[jx][jy]->GetMaximum();
	      maxMC=crystalMC[jx][jy]->GetMaximum();
	      if ((maxMC>0)&&(maxData>0)){
		crystalMC[jx][jy]->Scale(maxData/maxMC);
		crystalMC[jx][jy]->SetLineColor(2);
		crystalMC[jx][jy]->Draw("HISTSAME");
	      }
	      if ((jy==0)&&(jx==0)){
		crystalCanvas[jx][jy]->Print((pdf_file_name+"(").c_str());
	      }
	      
	      if (rates[jx][jy] >= 1000) {
		cout<<jx<<" "<<jy<<" FIT START "<<endl;
		lfit[jx][jy]= CBFit(crystal[jx][jy]);
		crystal[jx][jy]->Fit(lfit[jx][jy],"0QR");

		//do again with proper good range
		MPV[jx][jy] = lfit[jx][jy]->GetParameter(2);
		sigma[jx][jy] =  lfit[jx][jy]->GetParameter(3);
		lfit[jx][jy]->SetRange(	MPV[jx][jy]-sigma[jx][jy],MPV[jx][jy]+4*sigma[jx][jy]);

		crystal[jx][jy]->Fit(lfit[jx][jy],"0QR");
		MPV[jx][jy] = lfit[jx][jy]->GetParameter(2)/EBEAM;
		sigma[jx][jy] =  lfit[jx][jy]->GetParameter(3);
		
		//quality control check
		if ((fabs(sigma[jx][jy])>.2)) {		 
		  MPV[jx][jy] = -1; //use cosmics 
		  sigma[jx][jy] = -999;
		}
		//Special cases
		if (ITER==1){	  
		  switch(id){
		  case 414: //(-6,-5)
		    MPV[jx][jy]=4.375/EBEAM;
		    break;
		  case 421: //(2,-5)
		    MPV[jx][jy]=4.359/EBEAM;
		    break;
		  case 422: //(3,-5)
		    MPV[jx][jy]=4.132/EBEAM;
		    break;
		  case 423: //(4,-5)
		    MPV[jx][jy]=4.267/EBEAM;
		    break;
		  case 424: //(5,-5)
		    MPV[jx][jy]=4.283/EBEAM;
		    break;
		  case 373: //(-1,-4)
		    MPV[jx][jy]=4.65/EBEAM;
		    break;
		  case 375: //(2,-4)
		    MPV[jx][jy]=4.62/EBEAM;
		    break;
		  case 381: //(8,-4)
		    MPV[jx][jy]=4.492/EBEAM;
		    break;
		  case 285: //(4,-2)
		    MPV[jx][jy]=4.314/EBEAM;
		    break;
		  case 152:
		  case 153:
		  case 154:
		  case 107:
		    MPV[jx][jy]=-1;
		    break;
		  case 52: //(-18,4)
		    MPV[jx][jy]=4.177/EBEAM;
		    break;
		  case 266: //(-16,-2)
		    MPV[jx][jy]=3.76/EBEAM;
		    break;
		  case 319: //(-9,-3)
		    MPV[jx][jy]=4.4/EBEAM;
		    break;
		  case 332: //(5,-3)
		    MPV[jx][jy]=4.433/EBEAM;
		    break;
		  case 287: //(6,-2)
		    MPV[jx][jy]=4.134/EBEAM;
		    break;
		  case 58: //(-12,4)
		    MPV[jx][jy]=4.455/EBEAM;
		    break;
		  case 162: //(1,2)
		    MPV[jx][jy]=4.321/EBEAM;
		    break;
		  default:
		    break;
		  }
		}else if (ITER==2){
		  switch(id){
		  case 406: //(-14,-5)
		    MPV[jx][jy]=4.125/EBEAM;
		    break; 
		  case 152:
		  case 153:
		  case 154:
		  case 107:
		    MPV[jx][jy]=-1;
		    break;
		  case 127: //12,3
		    MPV[jx][jy]=4.25/EBEAM;
		    break;
		  case 52: //(-18,4)
		    MPV[jx][jy]=4.177/EBEAM;
		    break;
		  default:
		    break;
		  }
		}else if (ITER==3){
		  switch(id){
		  case 152:
		  case 153:
		  case 154:
		  case 107:
		    MPV[jx][jy]=-1;
		    break;
		  default:
		    break;
		  }
		}else if (ITER==4){
		    switch(id){
		    case 152:
		    case 153:
		    case 154:
		    case 107:
		    MPV[jx][jy]=-1;
		    break;
		    
		    default:
		      break;
		    }
		}

			if ((calcIY(jy)==-5)||(calcIY(jy)==5)){
		  MPV[jx][jy]=-1;
		}
		
		if ((calcIY(jy)==-1)||(calcIY(jy)==1)){
		  MPV[jx][jy]=-1;
		  }

	
		
		if (MPV[jx][jy]>0){
		  ECalStatus->Fill(calcIX(jx),calcIY(jy),1.);
		}else{
		  ECalStatus->Fill(calcIX(jx),calcIY(jy),2.);
		}

		
		// Global style settings	      
		crystalCanvas[jx][jy]->cd(4);
		gStyle->SetOptFit(111);
		crystal[jx][jy]->Draw();
		crystal[jx][jy]->SetTitle(Form("Crystal_%d_%d",calcIX(jx),calcIY(jy)));
		lfit[jx][jy]->Draw("lsame");
		crystalCanvas[jx][jy]->Modified();
		crystalCanvas[jx][jy]->Update();

		
		//DRAW THE CALIB
	      crystalCanvas[jx][jy]->cd(2);
	      calibPoint[jx][jy]=new TGraph();
	      for (int it=0;it<ITER;it++){
		calibPoint[jx][jy]->SetPoint(it,it,prevC[it][id-1]);
	      }
	      calibPoint[jx][jy]->SetPoint(ITER,ITER,prevC[ITER-1][id-1]*mcG[id-1]/MPV[jx][jy]);
	      calibPoint[jx][jy]->SetMarkerStyle(20);
	      calibPoint[jx][jy]->Draw("AP");

		
	      crystalCanvas[jx][jy]->Print((pdf_file_name).c_str());
		
		//crystalCanvas[jx][jy]->Close();
	      }
	      else{//revert to cosmics
		MPV[jx][jy] = -1; //fix the coeff to 1
		sigma[jx][jy] = -999;
		ECalStatus->Fill(calcIX(jx),calcIY(jy),3.);
		
		//DRAW THE CALIB
		crystalCanvas[jx][jy]->cd(2);
		calibPoint[jx][jy]=new TGraph();
		for (int it=0;it<ITER;it++){
		  calibPoint[jx][jy]->SetPoint(it,it,prevC[it][id-1]);
		}
	
		
		calibPoint[jx][jy]->SetMarkerStyle(20);
		calibPoint[jx][jy]->Draw("AP");

		
		// Global style settings
		crystalCanvas[jx][jy]->cd(4);
		crystal[jx][jy]->Draw();
		crystalCanvas[jx][jy]->Modified();
		crystalCanvas[jx][jy]->Update();
		crystalCanvas[jx][jy]->Print((pdf_file_name).c_str());		
		//crystalCanvas[jx][jy]->Close();
	      }//end else


	      
	      
	      fout->cd();
	      crystalCanvas[jx][jy]->SetName(Form("c_%i_%i",calcIX(jx),calcIY(jy)));
	      crystalCanvas[jx][jy]->Write();

	      if ((jx==(NX-1))&&(jy==(NY-1))){
		cout<<"CLOSING PDF"<<endl;
		crystalCanvas[jx][jy]->Print((pdf_file_name+")").c_str());
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
  ECal->SetMinimum(0.2);
  for (int iy=0; iy<NY; iy++){
      // loop over crystal x
    for (int ix=0; ix<NX; ix++){
	  if (!ishole(ix,iy)){
	    int id =  xy2dbid(ix,iy);
	    if (MPV[ix][iy]>0) ECal->Fill(calcIX(ix),calcIY(iy),MPV[ix][iy]);
	    cout<<calcIX(ix)<<" "<<calcIY(iy)<<" "<<MPV[ix][iy]<<endl;
	  }
    }
  }
  ECal->Draw("colz");	  
  fout->cd();
  ECal->Write();
  ECalStatus->Write();
  gStyle->SetOptStat(0);
  tOff->Update();
  tOff->Print(Form("output_iter%d/EnergyFraction.png",ITER));

  ECalStatus->Draw("colz");
  tOff->Update();
  tOff->Print(Form("output_iter%d/fitStatus.png",ITER));
  
  tOff->Close();

  ///////////////////////////////////////
  //Plot this gain / cosmic gain////////
  //////////////////////////////////////
  TH2D *ECalGainR=new TH2D("ECalGainR", "Gain ratio: this / cosmic", 47,-23.5,23.5, 11,-5.5,5.5);
  TH1D *ECalGainR1D=new TH1D("EcalGainR1D","Gain ratio:this/cosmic",200,0.5,1.5);
  cout<<"Printing gain ratio"<<endl;
  for (int iy=0; iy<NY; iy++) {
    // loop over crystal x
    for (int ix=0; ix<NX; ix++) {
      if (!ishole(ix,iy)){
	int id = xy2dbid(ix,iy);
	 double data=prevC[ITER-1][id-1]*mcG[id-1]/MPV[ix][iy];
	 if (MPV[ix][iy]<0){
	   data=COSMIC_FACTOR;
	 }else{
	   ECalGainR1D->Fill(data);
	 }
	 ECalGainR->Fill(calcIX(ix),calcIY(iy),data);

      }  
    }
  }
  ECalGainR->Draw("colz");
  ECalGainR->Write();
  ECalGainR1D->Write();
  ////////////////////////////////////////
  //Plot the occupancies in each crystal
  
  ////////////////////////////////////////
  TCanvas *occup = new TCanvas("occup","Occupancies",1200,800);
  occup->cd();
  TH2D *ECalF=new TH2D("ECalF", "Crystal Occupancies", 47,-23.5,23.5, 11,-5.5,5.5);
  ECalF->SetMinimum(1.0);
  cout<<"Printing occupanices"<<endl;
  for (int iy=0; iy<NY; iy++)  {
    for (int ix=0; ix<NX; ix++)	{
      if (!ishole(ix,iy)){
	int id = xy2dbid(ix,iy);		
	ECalF->Fill(calcIX(ix),calcIY(iy),rates[ix][iy]);
      }  
    }
  }
  ECalF->Draw("colz");	  
  fout->cd();
  ECalF->Write();
  ECalGainR->Write();
  gStyle->SetOptStat(0);
  occup->Update();
  occup->Print(Form("output_iter%d/CrystalOccupancies.png",ITER));
  occup->Close();
  f->Close();
  fout->Close();


  //////////////////////////////////////////////////////////////
  //Write out iteration factor//////////////////////////////////
  //////////////////////////////////////////////////////////////
  cout<<"Printing iteration factor"<<endl;
  //iteration factor:
  FILE *c = fopen(Form("output_iter%d/c%d.txt",ITER,ITER),"w+");
  fprintf(c,"# COMMENT DO NOT TOUCH\n");
  
  //global running gain:
  FILE *cc = fopen(Form("coeff/cGlobal_%d.txt",ITER),"w+");
  for (int iy=0; iy<NY; iy++)    {
    for (int ix=0; ix<NX; ix++)	{
      if (!ishole(ix,iy)){
	int id = xy2dbid(ix,iy);
	double data=prevC[ITER-1][id-1]*mcG[id-1]/MPV[ix][iy];
	if (MPV[ix][iy]<0) data=COSMIC_FACTOR;
	fprintf(c,"%d,%.4f\n",id,data);
	fprintf(cc,"%d,%.4f\n",id,ccosmic[id-1]*data);
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
  int npoints[NY]={};
  TGraph *grp[NY];
  for (int iy=0; iy<NY; iy++){
    grp[iy]=new TGraph();
    for (int ix=0; ix<NX; ix++){
      if (!ishole(ix,iy)){
	int id = xy2dbid(ix,iy);
	if (MPV[ix][iy]>0){
	  grp[iy]->SetPoint(npoints[iy],xPos[ix],mcG[id-1]/MPV[ix][iy]);
	  npoints[iy]++;
	}
      }
    }
  }

  TMultiGraph *mg = new TMultiGraph();
  mg->SetMinimum(0.0);
  mg->SetMaximum(1.5);
  
  TCanvas *scr=new TCanvas("scr","xxxx",1200,800);
  scr->cd();
  
  
  for (int yy=0;yy<NY;yy++){
 
    grp[yy]->SetName(Form("grp%i",yy));
    grp[yy]->SetLineColor(yy==9 ? yy+2 : yy+1);
    grp[yy]->SetLineWidth(3);
    grp[yy]->SetMarkerStyle(31);
    grp[yy]->SetMarkerSize(2);
    grp[yy]->SetMarkerColor(yy==9 ? yy+2 : yy+1);
   
    mg->Add(grp[yy],"LP");
  }

  mg->Draw("A");
  mg->SetTitle("Elastic Peak Position");
  mg->GetXaxis()->SetTitle("x crystal index, viewed from back of calorimeter");
  mg->GetYaxis()->SetTitle("MC Elastic Peak / Data Elastic Peak");

 
  TLegend* leg = new TLegend(0.8,0.65,0.95,0.95);
  leg->SetHeader("Row in y");
  // leg->AddEntry(Form("grp[%d]",9),"y=5","lep");
  for (int ii=0;ii<NY;ii++){
    int iyy;
    if (ii<5) iyy=5-ii;
    else iyy=4-ii;
    leg->AddEntry(grp[9-ii],Form("y=%i",iyy),"lep");
  }
  leg->Draw();
  
  scr->Update();
  scr->Print(Form("output_iter%d/Elasticmean.C",ITER));
  scr->Print(Form("output_iter%d/Elasticmean.png",ITER));
  scr->Close();
}
