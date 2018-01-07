#include "../omniheader.h"

//returns dSigma/dOmega



double mott(double theta, double ebeam, double mass, double Z){
   double barns = hbar*hbar/(100);
  return  Z*Z*alpha*alpha/(4*ebeam*ebeam*pow(sin(theta/2),4))
    *pow(cos(theta/2),2)
    /(1+2*(ebeam/mass)*pow(sin(theta/2),2))
    *barns;
  
}


TH1* get_xs_per_mott(TH2* theta_vs_phi, double ebeam, double mass, double Z, double lumi,  TH2* mask){
  TString formula = Form("mott(x, %f, %f, %f)*sin(x)", ebeam, mass, Z);
  TF1* f = new TF1("func_mott", formula, 0, .2);
  theta_vs_phi = (TH2*)(theta_vs_phi->Clone("theta phi"));  //counts per bin in theta and phi
  theta_vs_phi->Sumw2();
  theta_vs_phi->Multiply(mask);  //counts per bin in theta and phi, only in mask

  double dphi = theta_vs_phi->GetYaxis()->GetBinWidth(0);
  double dtheta = theta_vs_phi->GetXaxis()->GetBinWidth(0);

  theta_vs_phi->Scale(1/(lumi*dtheta*dphi));  
  theta_vs_phi->Divide(f);

  TH1* xs_per_mott = (TH1*) theta_vs_phi->ProjectionX("xs_per_mott");
  TH1* mask_proj = (TH1*)mask->ProjectionX("mask proj");

  xs_per_mott->Divide(mask_proj);
  
  return xs_per_mott;
}

TH2* get_xs_per_mott_2d(TH2* theta_vs_phi, double ebeam, double mass, double Z, double lumi,  TH2* mask){
  TString formula = Form("mott(x, %f, %f, %f)*sin(x)", ebeam, mass, Z);
  TF1* f = new TF1("func_mott", formula, 0, .2);
  theta_vs_phi = (TH2*)(theta_vs_phi->Clone("theta phi"));  //counts per bin in theta and phi
  theta_vs_phi->Sumw2();

  double dphi = theta_vs_phi->GetYaxis()->GetBinWidth(0);
  double dtheta = theta_vs_phi->GetXaxis()->GetBinWidth(0);

  theta_vs_phi->Scale(1/(lumi*dtheta*dphi));  
  theta_vs_phi->Divide(f);

  return theta_vs_phi;
}

void apply_lumi_sys_error(TH1* measurement, double rel_error){
  for(int i = 0; i< measurement->GetNbinsX(); i++){
    double y = measurement->GetBinContent(i);
    double dy = measurement->GetBinError(i);
    measurement->SetBinError(i, sqrt(dy*dy + y*y*rel_error*rel_error));
  }
}

void trim(TH2* data, double theta_max){
  for(int i = 0; i< data->GetNbinsX(); i++){
    if(data->GetXaxis()->GetBinCenter(i)<theta_max)
      continue;
    for(int j = 0; j<data->GetNbinsY(); j++){
      data->SetBinContent(i,j, 0);
      data->SetBinError(i,j,0);
    }
  }
}
					  
//removes isolated bins with nonzero contents.  
void remove_blips(TH2* h, int mode){
  if(mode < 0)
    h->Smooth(-mode);
  for(int i = 1; i < h->GetNbinsX(); i++){
    for(int j = 1; j < h->GetNbinsY(); j++){
      if(h->GetBinContent(i,j) != 1)
	continue;

      for(int k = -mode; k<=mode; k++){
	for(int l = -mode; l<=mode; l++){
	  if(h->GetBinContent(i+k,j+l) != 0 && (l !=0 || k != 0))
	    continue;
	}
      }
      h->SetBinContent(i,j, 0);
    }
  }
}

TH2* get_2016_prescaled_hist(TFile* file, TString name, int removeBlips = 0){
  TH2* h1 = (TH2*)file->Get(name + " r1")->Clone("r1");
  //if(removeBlips)
    //   remove_blips(h1, 10);
  h1->Sumw2();
  h1->Scale(1*2);
  
  TH2* h2 = (TH2*)file->Get(name + " r2")->Clone("r2");
  //if(removeBlips)
  //remove_blips(h2, 10);
  h2->Sumw2();
  trim(h2, .125);
  h2->Scale(80*2);

  TH2* h3 = (TH2*)file->Get(name + " r3")->Clone("r3");
  //if(removeBlips)
  //remove_blips(h3, 10);
  h3->Sumw2();
  trim(h3, .085);
  h3->Scale(1300*2);

  TH2* h4 = (TH2*)file->Get(name + " r4")->Clone("r4");
  if(removeBlips){
    remove_blips(h4, removeBlips);
    h4->Smooth();
  }
  h4->Sumw2();
  trim(h4, .063);
  h4->Scale(18000*2);

  //now add them all together
  h1->Add(h2);
  h1->Add(h3);
  h1->Add(h4);
  
  return h1;
}

TH2* get_2016_prescaled_hist_mixed_trigger(TFile* file_s1, TFile* file_s0, TString name){
  TH2* h1 = (TH2*)file_s1->Get(name + " r1")->Clone("r1");
  //if(removeBlips)
    //   remove_blips(h1, 10);
  h1->Sumw2();
  h1->Scale(1*2);
  
  TH2* h2 = (TH2*)file_s1->Get(name + " r2")->Clone("r2");
  //if(removeBlips)
  //remove_blips(h2, 10);
  h2->Sumw2();
  trim(h2, .125);
  h2->Scale(80*2);

  TH2* h3 = (TH2*)file_s1->Get(name + " r3")->Clone("r3");
  //if(removeBlips)
  //remove_blips(h3, 10);
  h3->Sumw2();
  trim(h3, .085);
  h3->Scale(1300*2);

  TH2* h4 = (TH2*)file_s0->Get(name + " r4")->Clone("r4");
  h4->Sumw2();
  trim(h4, .063);
  h4->Scale(4097);

  
  //now add them all together
  h1->Add(h2);
  h1->Add(h3);
  h1->Add(h4);
  
  return h1;
}