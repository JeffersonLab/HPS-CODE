/////////////////////////////////////////////////////////////////// 
// Author: Holly Szumila 
// Email: hvanc001@odu.edu
// Updated: 25 Jan 2016
//
// This code calculates the gains for individual crystals in the 
// HPS Ecal. This code takes in ROOT files that can be produced with
// vectors for each crystal containing the adc counts in each event.
// This file can be compiled in ROOT as:
// .L cosmicAnalysis.C++
// rawGeoCut(0)
// getGain()
//
// Pedestals are calculated per event 
// Ntuple arrays are indexed by crystals' x/y 
// Range of x is 0-45 (46 crystals in x)
// Range of y is 0-9 (10 crystals in y)
// Hole around the beam: (12<x<22 && 4<y<6)
// Number of time samples is 100 (4ns per sample)
//
#define NX 46
#define NY 10
#define NSAMP 100
#define NR 11
#define ADC2V 0.25
//signal window, originally 35-55, now shifted by 15
#define MINS 35//50 
#define MAXS 55//70
//pedestal window
#define MINP 10
#define MAXP 30
// difference in window
#define NWIN 20
//threshold in mV
#define THR 2.5
#define NSAMPINT 20
//
///////////////////////////////////////////////////////////////////
#include "TH1.h"
#include "TNtuple.h"
#include "TPad.h"
#include "TTree.h"
#include "TMath.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TDirectory.h"
#include "dependency/chainfilelist.C"
#include "dependency/MyRootUtil.C"
#include "dependency/ProgressMeter.C"
#include "TF1.h"
#include "dependency/langaus.C"

//use namespace standard;

// This removes the crystals in the electron hole
bool ishole(const int x,const int y)
{
    return (x>12 && x<22 && y>3 && y<6);
}
// Loads the initial ROOT file containing the raw data
struct fadc_t
{
  int adc[NX][NY][NSAMP]; // adc value for each time sample
  int pulse[NX][NY];      // adc integrated over first NSAMPINT samples
  float ped[NX][NY];      // pedestal
};
void InitTreeFADC(TTree *t,fadc_t &t_)
{
    if (!t) return;
    t->SetBranchAddress("adc",&t_.adc);
    t->SetBranchAddress("pulse",&t_.pulse);
    t->SetBranchAddress("ped",&t_.ped);
}
TChain *CHAIN=NULL;
fadc_t FADC;
void LoadTree()
{
    if (CHAIN) return;
    CHAIN=chainfiledir("cosmicInput","Tadc");
    InitTreeFADC((TTree*)CHAIN,FADC);
}
// rawGeoCut is used to plot the mip signal (pedestal subtracted) and 
// use cuts to plot the value (cuts on raw value in time window and geometric)
// set q to 0 for strict, set q to 1 for loose

void rawGeoCut(int q)
{
  
  // Chain files
  TChain *t=chainfiledir("cosmicInput","Tadc");

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

void rawCountingCut(){
  // Chain files
  TChain *t=chainfiledir("cosmicInput","Tadc");

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
			  
			  if (counter >= 2)
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

void getGain(){

  // open the root file histogram
  TFile *f = new TFile("mipSigCut.root");

  Double_t MPV[NX][NY]={};
  TF1 *lfit[NX][NY];
  TH1D *mipSigCut[NX][NY];
  //  TF1 *fcosmic=CosmicSignal();
  //  fcosmic->SetLineColor(4);
  
  int ii=0;
  
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

		    ///using convolution fit//
		    // Setting fit range and start values
		    Double_t fr[2];
		    Double_t sv[4], pllo[4], plhi[4], fp[4], fpe[4];
		    fr[0]=0.3*mipSigCut[jx][jy] ->GetMean();
		    fr[1]=3.0*mipSigCut[jx][jy] ->GetMean();
		    
		    if(mipSigCut[jx][jy] ->GetMean() < 20.0)
		      {
			fr[0]=0.5*25.0;
			fr[1]=3.0*25.0;
		      }
		  
		    pllo[0]=0.5; pllo[1]=12.0; pllo[2]=50.0; pllo[3]=0.4;
		    plhi[0]=5.0; plhi[1]=50.0; plhi[2]=2000.0; plhi[3]=7.0;
		    sv[0]=1.8; sv[1]=25.0; sv[2]=500.0; sv[3]=3.0;
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
		    		    
		    gPad->Update();
		    gPad->SaveAs(Form("convolFit/Cry_%d_%d.C",jx,jy));
		    ii++;

		    MPV[jx][jy] = SNRPeak; 
		    
		  }//end if mipSigCut[][]
		}//end ishole
	    }//end loop x
	}//end loop y

	  
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
  gainC->Print(Form("gainFactor.png"));
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
 rateC->Print(Form("cosmicOccupancy.png"));
 rateC->Close();

 f->Close();

 ofstream gainsOut;
 gainsOut.open("gains.txt");
  for (int ny=0; ny<NY; ny++)
   {
     // loop over crystal x
     for (int nx=0; nx<NX; nx++)
       {
	 // skip the hole
	 if (!ishole(nx,ny))
	   {
	     float val = 18.3/(MPV[nx][ny]*4);
	     if (MPV[nx][ny]>-900){
	       gainsOut<<nx<<"\t"<<ny<<"\t"<<val<<endl;
	       //fprintf("%d \t %d \t %f",nx,ny,val);
	     }
	     else{gainsOut<<nx<<"\t"<<ny<<"\t"<<0.2<<endl;}

	   }
       }
   }
  gainsOut.close();
 
}


