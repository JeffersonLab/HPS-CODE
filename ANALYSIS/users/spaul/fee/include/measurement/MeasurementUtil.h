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
