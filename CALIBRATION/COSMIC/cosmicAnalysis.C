/////////////////////////////////////////////////////////////////// 
// Author: Holly Szumila 
// Email: hszumila@jlab.org
// Updated: 30 June 2017
//
// This code calculates the gains for individual crystals in the 
// HPS Ecal for data taken with a cosmic trigger.
// This code takes in ROOT files that can be produced with
// arrays for each crystal containing the adc counts in each event.
// This file can be compiled in ROOT as:
// .L cosmicAnalysis.C++
// geoCut(0) 
// getGain()
//
// Pedestals are calculated per event 
// Ntuple arrays are indexed by crystals' x/y 
// Range of x is 0-45 (46 crystals in x)
// Range of y is 0-9 (10 crystals in y)
// Hole around the beam: (12<x<22 && 4<y<6)
// Number of time samples is 100 (4ns per sample)
//
// Tune-able parameters:
//signal window, originally 35-55, now shifted by 15
#define MINS 35//50 
#define MAXS 55//70
//pedestal window
#define MINP 10
#define MAXP 30
// difference in window
#define NWIN 20
//threshold in mV
#define THR 3.5 //for 2016, 2.5 for 2015
#define NSAMPINT 20


// Don't change these
#define NX 46
#define NY 10
#define NSAMP 100
#define NR 11
#define ADC2V 0.25
///////////////////////////////////////////////////////////////////
#include "TH1.h"
#include "TNtuple.h"
#include "TPad.h"
#include "TTree.h"
#include "TMath.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TDirectory.h"
#include "TF1.h"
#include "TPaveText.h"


#include "dependency/chainfilelist.C"
#include "dependency/MyRootUtil.C"
#include "dependency/ProgressMeter.C"
#include "dependency/langaus.C"
#include "dependency/functions.C"


//use namespace standard;


// rawGeoCut is used to plot the mip signal (pedestal subtracted) and 
// use cuts to plot the value (cuts on raw value in time window and geometric)
// set q to 0 for strict, set q to 1 for loose
// strict means that there must be a hit both above and below
// loose means that there can be hit above or below
void geoCut(int q)
{
  
  // Chain files
  TChain *t=chainfiledir("input","Tadc");

  fadc_t t_;
  InitTreeFADC(t,t_);
  
  // Output file
  TFile *f=new TFile("mipSigCut.root","RECREATE");
  
  // New pedestal per channel, integrated
  TH1D *mipSigCut[NX][NY];
  int pedestal[NX][NY]={};
  int pulse[NX][NY]={};
  float signal[NX][NY]={};

  
  gROOT->SetBatch(true);

 // Create histograms
  for (int jx=0; jx<NX; jx++)
    {
      for (int jy=0; jy<NY; jy++)
	{
	  if (!ishole(jx,jy))
	    {
	      mipSigCut[jx][jy]=new TH1D(Form("Cry_%.2d_%d",jx,jy),"",80,5,70);
	      mipSigCut[jx][jy]->SetTitle(Form("Crystal %.2d,%d",jx,jy));
	      mipSigCut[jx][jy]->GetXaxis()->SetTitle("Peak in mV, ped subtracted");
	    } // end !ishole
	} // end jy iteration
    } //end jx iteration
  
  
  // Loop through events
  for (int ii=0;ii<t->GetEntries();ii++)
    {
      ProgressMeter(t->GetEntries(),ii);
      t->GetEntry(ii);

      // loop over crystal y
      for (int iy=0; iy<NY; iy++)
	{
	  // loop over crystal x
	  int trigger = 0;
	  for (int ix=0; ix<NX; ix++)
	    {
	      if (!ishole(ix,iy))
		{
		  // loop over time samples, integrate adc values, use for pedestal
		  pedestal[ix][iy] = 0;		  
		  for (int nTime=MINP; nTime<MAXP; nTime++)
		    {
		      const int adc=t_.adc[ix][iy][nTime];
		      pedestal[ix][iy] += adc;
		    }// end loop over time samples

		   // loop over time samples, integrate adc values, use for signal and trigger
		  pulse[ix][iy] = 0;
		  for (int nTime=MINS; nTime<MAXS; nTime++)
		    {
		      const int adc=t_.adc[ix][iy][nTime];
		      double peak = (adc-pedestal[ix][iy]/NWIN)*ADC2V;
		      if (peak > THR) {trigger=1;}
		      pulse[ix][iy] += adc;		      
		    }// end loop over time samples

		  // subtract pedestal from pulse and plot
		  if (trigger == 1)
		    {
		      signal[ix][iy] = (pulse[ix][iy] - pedestal[ix][iy])*ADC2V;

		      // Crystal has passed threshold trigger cut, now must pass geometry cuts
		      int geomCut0=0;//0 passes, ix+1
		      int geomCut1=0;//0 passes, ix-1
		      int geomCut2=0;//0 passes, iy+1
		      int geomCut3=0;//0 passes, iy-1
		     
		      int geomCut4=0;//0 passes, if iy is 9,4, iy-2
		      int geomCut5=0;//0 passes, if iy is 0,5, iy+2

		      //define geometry cuts-no other hit on left and right passing raw thresh
		      // loop over time samples, integrate adc values
		      if (!ishole(ix+1,iy) && (ix+1)<46)
			{
			  pedestal[ix+1][iy] = 0;
			  // calculate the pedestal for the crystal ix+1
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix+1][iy][nTime]; 
			      pedestal[ix+1][iy] += ped;
			    }// end loop over time samples			  
			  // check if hit in adj crystal passes threshold
			  pulse[ix+1][iy] = 0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix+1][iy][nTime];
			      double peak = (adc-pedestal[ix+1][iy]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut0=1;
				  break;
				}
			    }// end loop over time samples
			}

		      if (!ishole(ix-1,iy) && (ix-1)>-1)
			{
			  pedestal[ix-1][iy]=0;
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix-1][iy][nTime]; 
			      pedestal[ix-1][iy] += ped;
			    }// end loop over time samples
			  // check if hit in adj crystal passes threshold
			  pulse[ix-1][iy] =0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix-1][iy][nTime];
			      double peak = (adc-pedestal[ix-1][iy]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut1=1;
				  break;
				}
			    }// end loop over time samples
			}
		      
		      if (!ishole(ix,iy+1) && (iy+1)<10 && iy!=4)
			{
			  geomCut2=1;
			  pedestal[ix][iy+1]=0;
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix][iy+1][nTime]; 
			      pedestal[ix][iy+1] += ped;
			    }// end loop over time samples
			  //check if hit in adj crystal passes threshold
			  pulse[ix][iy+1] =0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix][iy+1][nTime];
			      double peak = (adc-pedestal[ix][iy+1]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut2=0;
				  break;
				}
			    }// end loop over time samples
			}
		      
		      if (!ishole(ix,iy-1) && (iy-1)>-1 && iy!=5)
			{
			  geomCut3=1;
			  pedestal[ix][iy-1]=0;
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix][iy-1][nTime]; 
			      pedestal[ix][iy-1] += ped;
			    }// end loop over time samples
			  //check if hit in adj crystal passes threshold
			  pulse[ix][iy-1] =0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix][iy-1][nTime];
			      double peak = (adc-pedestal[ix][iy-1]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut3=0;
				  break;
				}
			    }// end loop over time samples
			}

		      /////////////////////Add in additional vert geom constraint for edges/////////
		      // if the crystal is along an edge, it must have a hit two above or two below
		      // since it does not have 1 above and 1 below
		      if(iy==9 || iy==4 || ishole(ix,iy+1)) //look at iy-2
			{
			  geomCut4=1;
			  pedestal[ix][iy-2]=0;
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix][iy-2][nTime]; 
			      pedestal[ix][iy-2] += ped;
			    }// end loop over time samples
			  pulse[ix][iy-2] =0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix][iy-2][nTime];
			      double peak = (adc-pedestal[ix][iy-2]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut4=0;
				  break;
				}
			    }// end loop over time samples
			} //end for iy-2
		      if(iy==0 || iy==5 || ishole(ix,iy-1)) //look at iy+2
			{
			  geomCut5=1;
			  pedestal[ix][iy+2]=0;
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix][iy+2][nTime]; 
			      pedestal[ix][iy+2] += ped;
			    }// end loop over time samples
			  pulse[ix][iy+2] =0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix][iy+2][nTime];
			      double peak = (adc-pedestal[ix][iy+2]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut5=0;
				  break;
				}
			    }// end loop over time samples
			} //end for iy+2

		      /////////////////////////////////////////////////////////////////////////////
		      if (q==0) //strict geometry cut
			{
			  if(geomCut0==0&&geomCut1==0&&geomCut2==0&&geomCut3==0&&geomCut4==0&&geomCut5==0)
			    {
			      mipSigCut[ix][iy]->Fill(signal[ix][iy]);
			    }
			}
		      else if (q==1) //loose geometry cut
			{
			  if(geomCut0==0&&geomCut1==0) 
			    {
			      if(geomCut2==0||geomCut3==0) 
				{
				  mipSigCut[ix][iy]->Fill(signal[ix][iy]);
				}
			    }
			}

		    } // end of trigger==1
	      
		} //end !ishole
	      
	    }// end loop over x
	     
	}// end loop over y
	  
    }//end entry loop
  
  WriteRemainingHistos(1);

  f->Close();
}
//////////////////////////////////////////////////////////////////////////////

void countingCut(int nCounts){
  // nCounts is the number of hits in a column in a half of the Ecal,
  // this was originally set to 2. Can be used when there is a bad
  // crystal in a column.
  
  // Chain files
  TChain *t=chainfiledir("input","Tadc");

  fadc_t t_;
  InitTreeFADC(t,t_);

  // Output file
  TFile *f=new TFile("mipSigCut.root","RECREATE");
  // New pedestal per channel, integrated
  TH1D *mipSigCut[NX][NY];
  int pedestal[NX][NY]={};
  int pulse[NX][NY]={};
  float signal[NX][NY]={};



 // Create histograms
  for (int jx=0; jx<NX; jx++)
    {
      for (int jy=0; jy<NY; jy++)
	{
	  if (!ishole(jx,jy))
	    {
	      mipSigCut[jx][jy]=new TH1D(Form("Cry_%.2d_%d",jx,jy),"",80,5,70);
	      mipSigCut[jx][jy]->SetTitle(Form("Crystal %.2d,%d",jx,jy));
	      mipSigCut[jx][jy]->GetXaxis()->SetTitle("Peak in mV, ped subtracted");


	    } // end !ishole
	} // end jy iteration
    } //end jx iteration

  // Loop through events
  for (int ii=0;ii<t->GetEntries();ii++)
    {
      ProgressMeter(t->GetEntries(),ii);

      t->GetEntry(ii);
      // loop over crystal y
      for (int iy=0; iy<NY; iy++)
	{
	  // loop over crystal x
	  int trigger = 0;
	  for (int ix=0; ix<NX; ix++)
	    {
	      if (!ishole(ix,iy))
		{
		  // loop over time samples, integrate adc values, use for pedestal
		  pedestal[ix][iy] = 0;		  
		  for (int nTime=MINP; nTime<MAXP; nTime++)
		    {
		      const int adc=t_.adc[ix][iy][nTime];
		      pedestal[ix][iy] += adc;
		      
		    }// end loop over time samples

		   // loop over time samples, integrate adc values, use for signal and trigger
		  pulse[ix][iy] = 0;
		  for (int nTime=MINS; nTime<MAXS; nTime++)
		    {
		      const int adc=t_.adc[ix][iy][nTime];
		      double peak = (adc-pedestal[ix][iy]/NWIN)*ADC2V;
		      if (peak > THR) {trigger=1;}
		      pulse[ix][iy] += adc;
		      
		    }// end loop over time samples

		  // subtract pedestal from pulse and plot
		  if (trigger==1)
		    {
		      signal[ix][iy] = (pulse[ix][iy] - pedestal[ix][iy])*ADC2V;
		      int geomCut0=0;//0 passes, ix+1
		      int geomCut1=0;//0 passes, ix-1

		      //Check that crystal to immediate left and right are not above threshold
		      if (!ishole(ix+1,iy) && (ix+1)<46)
			{		       
			  pedestal[ix+1][iy] = 0;
			  // calculate the pedestal for the crystal ix+1
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix+1][iy][nTime]; 
			      pedestal[ix+1][iy] += ped;
			    }// end loop over time samples
			  
			  // check if hit in adj crystal passes threshold
			  pulse[ix+1][iy] = 0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix+1][iy][nTime];
			      double peak = (adc-pedestal[ix+1][iy]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut0=1;
				  break;
				}
			    }// end loop over time samples
			}

		      if (!ishole(ix-1,iy) && (ix-1)>-1)
			{
			  pedestal[ix-1][iy]=0;
			  for (int nTime=MINP; nTime<MAXP; nTime++)
			    {
			      const int ped = t_.adc[ix-1][iy][nTime]; 
			      pedestal[ix-1][iy] += ped;
			    }// end loop over time samples
			  pulse[ix-1][iy] =0;
			  for (int nTime=MINS; nTime<MAXS; nTime++)
			    {
			      const int adc=t_.adc[ix-1][iy][nTime];
			      double peak = (adc-pedestal[ix-1][iy]/NWIN)*ADC2V;
			      if (peak > THR) 
				{
				  geomCut1=1;
				  break;
				}
			    }// end loop over time samples
			}

		      //if crystals to left and right are below threshold
		      if (geomCut0==0 && geomCut1==0)
			{
			  int counter = 0;
			  
			  //Count the number of crystals in the column that are above threshold, in that half of ecal
			  //top half:
			  if (iy>4)//top half
			    {
			      for (int ny=5; ny<10; ny++)
				{
				  if (iy != ny)
				    {
				      // get the pedestal
				      pedestal[ix][ny] = 0;
				      for (int nTime=MINP; nTime<MAXP; nTime++)
					{
					  const int ped = t_.adc[ix][ny][nTime]; 
					  pedestal[ix][ny] += ped;
					}
				      // get the signal and subtract the pedestal
				      pulse[ix][ny] = 0;
				      for (int nTime=MINS; nTime<MAXS; nTime++)
					{
					  const int adc=t_.adc[ix][ny][nTime];
					  pulse[ix][ny] += adc;
					}
				      double peak = (pulse[ix][ny]-pedestal[ix][ny])*ADC2V;
				      if (peak > THR) 
					{
					  counter++;					  
					}
				    }
				}
			    }// top half
			  
			  //bottom half:
			  else //bottom half 
			    {
			      for (int ny=0; ny<4; ny++)
				{
				  if (iy != ny)
				    {
				      // get the pedestal
				      pedestal[ix][ny] = 0;
				      for (int nTime=MINP; nTime<MAXP; nTime++)
					{
					  const int ped = t_.adc[ix][ny][nTime]; 
					  pedestal[ix][ny] += ped;
					}
				      // get the signal and subtract the pedestal
				      pulse[ix][ny] = 0;
				      for (int nTime=MINS; nTime<MAXS; nTime++)
					{
					  const int adc=t_.adc[ix][ny][nTime];
					  pulse[ix][ny] += adc;
					}
				      double peak = (pulse[ix][ny]-pedestal[ix][ny])*ADC2V;
				      if (peak > THR) 
					{
					  counter++;
					}
				    }
				}
			    }// bottom half
			  
			  if (counter >= nCounts)
			    {
			      mipSigCut[ix][iy]->Fill(signal[ix][iy]);
			    }
			}
		    }
		}
	    }
	}
    }
  WriteRemainingHistos(1);
  
  f->Close();
}

/////////////////////////////////////////////////////////////////////////////
// This is the code that fits the integrated histograms
void getGain(){

  // open the root file histogram
  TFile *f = new TFile("mipSigCut.root");

  Double_t MPV[NX][NY]={};
  TF1 *lfit[NX][NY];
  TH1D *mipSigCut[NX][NY];
  //  TF1 *fcosmic=CosmicSignal();
  //  fcosmic->SetLineColor(4);

  TCanvas *canvas = new TCanvas("canvas","cosmic fits", 700, 700);
  canvas->SetFillColor(0);
  canvas->SetBorderMode(0);
  canvas->SetBorderSize(0);
  canvas->SetFrameFillColor(0);
  canvas->SetFrameBorderMode(0);
  std::string pdf_file_name = "output/cosmicFits.pdf";

  gROOT->SetBatch(true);

  
  int ii=0;
  canvas->Update();

  
  for (int jy=0; jy<NY; jy++)
	{
	  // loop over crystal x
	  for (int jx=0; jx<NX; jx++)
	    {
	      // skip the hole
	      if (!ishole(jx,jy))
		{
		  mipSigCut[jx][jy] = (TH1D*)f->Get(Form("Cry_%.2d_%d",jx,jy));
		  
		  if (mipSigCut[jx][jy]) {
		      mipSigCut[jx][jy]->GetXaxis()->SetRange(10,70);
		      ///using convolution fit//
		      // Setting fit range and start values
		      Double_t fr[2];
		      Double_t sv[4], pllo[4], plhi[4], fp[4], fpe[4];
		      //fr[0]=mipSigCut[jx][jy]->GetMean()-10.0;
		      fr[0] = 0.3*mipSigCut[jx][jy] ->GetMean();
		      //fr[1]=mipSigCut[jx][jy]->GetMean()+20.0;
		      fr[1] = 3.0*mipSigCut[jx][jy] ->GetMean();
		      /*
			if(mipSigCut[jx][jy] ->GetMean() < 20.0)
			{
			fr[0]=0.5*25.0;
			fr[1]=3.0*25.0;
			}
		      */
		      pllo[0]=0.5; pllo[1]=15.0; pllo[2]=0.1*mipSigCut[jx][jy]->GetEntries(); pllo[3]=1;
		      plhi[0]=5.0; plhi[1]=40.0; plhi[2]=0.75*mipSigCut[jx][jy]->GetEntries(); plhi[3]=7.0;
		      sv[0]=1.8; sv[1]=mipSigCut[jx][jy]->GetMean(); sv[2]=0.5*mipSigCut[jx][jy] ->GetEntries(); sv[3]=2.0;
		      Double_t chisqr;
		      Int_t    ndf;		  
		      lfit[jx][jy] = langaufit(mipSigCut[jx][jy],fr,sv,pllo,plhi,fp,fpe,&chisqr,&ndf);
		      ///using convolution fit///
		      Double_t SNRPeak, SNRFWHM;
		      langaupro(fp,SNRPeak,SNRFWHM);		  
		      printf("Fitting done\nPlotting results...\n");		  
		      // Global style settings
		      gStyle->SetOptStat(1111);
		      gStyle->SetOptFit(111);
		      gStyle->SetLabelSize(0.03,"x");
		      gStyle->SetLabelSize(0.03,"y");		  
		      mipSigCut[jx][jy]->GetXaxis()->SetRange(8,70);
		      mipSigCut[jx][jy]->Draw();
		      lfit[jx][jy]->Draw("lsame");		      
		      MPV[jx][jy] = SNRPeak;

		      TPaveText *t = new TPaveText(0.1,0.8,0.3,0.9,"brNDC");
		      t->AddText(Form("Peak at %.3f",MPV[jx][jy]));
		      t->AddText(Form("Gain is %.3f",18.3/(MPV[jx][jy]*4)));
		      t->Draw("lsame");
		      canvas->Print( (pdf_file_name + "(").c_str());
		      gPad->Update();
		      gPad->SaveAs(Form("output/Cry_%d_%d.C",jx,jy));
		      gPad->Print(Form("output/Cry_%d_%d.png",jx,jy));

		    ii++;
		    
		  }//end if mipSigCut[][]
		}//end ishole
	    }//end loop x
	}//end loop y
  canvas->Print( (pdf_file_name + ")").c_str());

	  
  //Plot gain values
  //Fit histograms and put into colorful view of calorimeter with MPV:
  TCanvas *gainC=new TCanvas("gainC","GainCalibrations",1200,800);
  gainC->cd();
  TH2D *ECal=new TH2D("ECal", "Gain Calibration", 49,-1.5,47.5, 12,-1.5,10.5);


  for (int iy=0; iy<NY; iy++)
    {
      // loop over crystal x
      for (int ix=0; ix<NX; ix++)
	{
	  // skip the hole
	  if (!ishole(ix,iy))
	    {
	      if (MPV[ix][iy]>-900){
		ECal->SetBinContent(ix+3,iy+2,18.3/(MPV[ix][iy]*4));
		ECal->Draw("colz");
	      }
	      
	    }
	}
    }
  gStyle->SetOptStat(0);
  gainC->Update();
  gainC->Print(Form("output/gainFactor.png"));
  gainC->Close();

  //Look at rates:
  TCanvas *rateC=new TCanvas("rateC","CosmicRates",1200,800);
  rateC->cd();
  TH2D *Rates=new TH2D("Rates", "ECal Occupancy", 49,-1.5,47.5, 12,-1.5,10.5);
  for (int ly=0; ly<NY; ly++)
    {
      // loop over crystal x
      for (int lx=0; lx<NX; lx++)
	{
	  // skip the hole
	  if (!ishole(lx,ly))
	    {
	      if(mipSigCut[lx][ly]){
		Rates->SetBinContent(lx+3,ly+2,mipSigCut[lx][ly]->GetEntries());      
		Rates->Draw("colz");
	      }	      
	    }
	}
    }
 gStyle->SetOptStat(0);
 rateC->Update();
 rateC->Print(Form("output/cosmicOccupancy.png"));
 rateC->Close();

 f->Close();

 ofstream gainsOut;
 gainsOut.open("output/gains4db.txt");
 ofstream gainsDAQ;
 gainsDAQ.open("output/gains4DAQconversion.txt");
 gainsOut<<"ecal_channel_id, gain"<<endl;
  for (int ny=0; ny<NY; ny++)
   {
     // loop over crystal x
     for (int nx=0; nx<NX; nx++)
       {
	 // skip the hole
	 if (!ishole(nx,ny))
	   {
	     float val = 18.3/(MPV[nx][ny]*4);
	     if (MPV[nx][ny]>-900 ){
	       int dbid = xy2dbid(nx,ny);
	       cout<<nx<<","<<ny<<"\t"<<calcIX(nx)<<","<<calcIY(ny)<<"\tdbid\t"<<dbid<<"\t"<<val<<endl;
	       gainsOut<<dbid<<","<<val<<endl;
	       gainsDAQ<<nx<<"\t"<<ny<<"\t"<<val<<endl;
	     }
	   }
       }
   }
  gainsDAQ.close();
  gainsOut.close();
  
 
}


//Draws raw adc readout for x,y crystal
void view(const int ix,const int iy)
{
  int kk=0;
  if (ix<0 || iy<0 || ix>=NX || iy>=NY) { cerr<<"What? "<<ix<<" "<<iy<<endl;return;}
  TChain *t=chainfiledir("input","Tadc");
  fadc_t t_;
  InitTreeFADC((TTree*)t,t_);
  TH1D *h=new TH1D("h","",NSAMP,-0.5,NSAMP-0.5);
  const bool doped=0;
  for (int ii=0; ii<t->GetEntries(); ii++)
    {
      t->GetEntry(ii);
      int trigger=0;
      for (int jj=0; jj<NSAMP; jj++)
        {
	  const int adc=t_.adc[ix][iy][jj];
	  float ped = 0;
	  for (int ii=0; ii<30; ii++){
	    ped +=t_.adc[ix][iy][ii];
	  }
	  float pedestal=ped/30;
	  
	  if (jj>30 && (adc-pedestal)*ADC2V>THR) trigger=1;
	  if (doped) h->SetBinContent(jj+1,(adc-pedestal)*ADC2V);
	  else       h->SetBinContent(jj+1,adc*ADC2V);
	}           
      if (trigger==1){
	h->Draw();
	gPad->Update();
	gPad->SaveAs(Form("%d.C",kk));
	kk++;     
	if (getchar()=='q') return;
      }
    }
}
// Draws raw readout for specific number of events in specified column having hit about thresh
void setlim(TH1* h)
{
    const double min=h->GetMinimum();
    const double max=h->GetMaximum();
    const double ddd=max-min;
    h->SetMinimum(min-ddd*0.5);
    h->SetMaximum(max+ddd*0.5);
}
void view(const int ix)
{
    gStyle->SetOptStat(0);
    TLegend *leg=new TLegend(0.85,0.6,0.95,0.95,"Row");

    const bool doped=0;
    if (ix<0 || ix>=NX) { cerr<<"What? "<<ix<<" "<<endl;return;}
    TChain *t=chainfiledir("input","Tadc");
    fadc_t t_;
    InitTreeFADC((TTree*)t,t_);
    TH1D *h[NY];
    for (int iy=0; iy<NY; iy++)
    {
        h[iy]=new TH1D(Form("hy_%d",iy),"",NSAMP,-0.5,NSAMP-0.5);
        h[iy]->SetLineColor(iy==0 ? MyColors(9) : MyColors());
        h[iy]->GetYaxis()->SetTitle("ADC (mV)");
        h[iy]->GetXaxis()->SetTitle("Time (4 ns)");
        leg->AddEntry(h[iy],Form("%d",iy<5?iy-5:iy-4),"L");
    }

    for (int ii=0; ii<t->GetEntries(); ii++)
    {
        t->GetEntry(ii);
        int trig[NY]={};
        for (int iy=0; iy<NY; iy++)
        {
            for (int jj=0; jj<NSAMP; jj++)
            {
                const int adc=t_.adc[ix][iy][jj];
		float ped = 0;
		for (int ii=0; ii<30; ii++){
		  ped +=t_.adc[ix][iy][ii];
		}
		float pedestal=ped/30;

                if (jj>30 && (adc-pedestal)*ADC2V>THR ) trig[iy]=1;
                if (doped) h[iy]->SetBinContent(jj+1,(adc-pedestal)*ADC2V);
                else       h[iy]->SetBinContent(jj+1,adc*ADC2V);
            }
            if (!ishole(ix,iy) && h[iy]->Integral(1,NSAMP)>0)
            {
                //setlim(h);
                if (doped) {h[iy]->SetMinimum(-20*ADC2V); h[iy]->SetMaximum(20*ADC2V);}
                else       {h[iy]->SetMinimum(30*ADC2V);  h[iy]->SetMaximum(200*ADC2V);}
                h[iy]->DrawCopy(iy==0?"":"SAME");
                
            }
            h[iy]->Reset("ICE");
        }
        int ntrig=0;
        for (int iy=0; iy<NY; iy++) ntrig += trig[iy];
        if (ntrig>4)
        {
            leg->Draw();
            gPad->Update();
            gPad->SaveAs(Form("%d.C",ii));
            if (getchar()=='q') return;
        }
    }
}
