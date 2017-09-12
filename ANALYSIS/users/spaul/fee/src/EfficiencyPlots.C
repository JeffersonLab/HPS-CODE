#include "../include/xs_model/Carbon.h"
#include "../include/xs_model/CrossSectionComponent.h"
#include "../include/xs_model/CrossSectionUtil.h"
//#include "../include/xs_model/RadiativeCorrection.h"

#include "../include/measurement/MeasurementUtil.h"
#include "../include/omniheader.h"

//create a 2d version of a 1d plot
TH2* to_2d(TH1* h1, TH2* h2){
  h2 = (TH2*) h2->Clone();
  for(int i = 0; i < h2->GetNbinsX(); i++){
    for(int j = 0; j < h2->GetNbinsY(); j++){
      h2->SetBinContent(i, j, h1->GetBinContent(i));
      h2->SetBinError(i, j, h1->GetBinError(i));
    }
  }
  return h2;
}

void EfficiencyPlots(){
  double ebeam = 1.056;
  double Z = 6;
  double mass = 12*AMU;
  TFile* carbon_file = TFile::Open("~/data/fee/tweakpass6_072817/5779.root");
  TH2* theta_vs_phi = (TH2*)carbon_file->Get("85_percent/theta vs phi track extrap cut");
  double lumi = 45837.645e-9/128.*2.213e-3/1.60217662e-19;
  double lumi_err = .0119;
  TH2* mask = (TH2*)TFile::Open("fee_mask.root")->Get("mask");
  TH1* xs_per_mott = get_xs_per_mott(theta_vs_phi, ebeam, mass, Z, lumi, mask);
  apply_lumi_sys_error(xs_per_mott, lumi_err);

  TCanvas* c1 = new TCanvas();
  c1->Divide(2,2);
  c1->cd(1);
  TH1* model = full_carbon_model(ebeam);

  double ecut = ebeam*.85;
  double t = .042;
  double b = 1.34;
  double sigma_e = .045;
  TH1* model_rad_corr = full_carbon_model_with_rad_corr(ebeam, ecut, t, b, sigma_e);

  model->SetFillColor(kRed-8);
  model->Draw("E4,C");

  model_rad_corr->SetFillColor(kRed);
  model_rad_corr->Draw("SAME,E4,C");
  xs_per_mott->Draw("SAME");

  c1->cd(2);
  
  TH1* efficiency = (TH1*)xs_per_mott->Clone();
  efficiency->Divide(model_rad_corr);
  efficiency->SetFillColor(kBlack);
  efficiency->Draw("E4");
  TLine* line = new TLine();
  line->SetLineColor(kRed);
  line->DrawLine(0, 1, .2, 1);

  c1->cd(3);
  TH2 * eff_2d = get_xs_per_mott_2d(theta_vs_phi, ebeam, mass, Z, lumi, mask);
  eff_2d->Divide(to_2d(model_rad_corr, eff_2d));
  bool rebinX = true;
  if(rebinX){
    eff_2d->RebinX(2);
    eff_2d->RebinY(2);
    eff_2d->Scale(1/4.);
  }
  eff_2d->SetMaximum(1.2);
  eff_2d->Draw("COLZ");
}
