#include "../include/xs_model/Carbon.h"
#include "../include/xs_model/CrossSectionComponent.h"
#include "../include/xs_model/CrossSectionUtil.h"
//#include "../include/xs_model/RadiativeCorrection.h"

#include "../include/util/GraphUtil.h"
#include "../include/measurement/MeasurementUtil.h"
#include "../include/omniheader.h"
#include "TRandom.h"




void stylize_axes(TH1* h){
  h->SetTitleSize(.05, "XYZ");
  h->SetLabelSize(.05, "XYZ");
  h->SetTitleFont(62, "XYZ");
  h->SetLabelFont(62, "XYZ");
}

//create a 2d version of a 1d plot
TH2* to_2d(TH1* h1, TH2* h2){
  h2 = (TH2*) h2->Clone();
  for(int i = 0; i < h2->GetNbinsX(); i++){
    for(int j = 0; j < h2->GetNbinsY(); j++){
      h2->SetBinContent(i, j, h1->GetBinContent(i));
      h2->SetBinError(i, j, h1->GetBinError(i));
    }
  }
  h2->Sumw2();
  return h2;
}

TH2* transpose(TH2* h1){

  TH2* h2 = new TH2F("transposed", "transposed", h1->GetNbinsY(), h1->GetYaxis()->GetXmin(), h1->GetYaxis()->GetXmax(), h1->GetNbinsX(),h1->GetXaxis()->GetXmin(), h1->GetXaxis()->GetXmax());

  h2->SetEntries(h1->GetEntries());
  for(int i = 1; i< h1->GetNbinsX(); i++){
    for(int j = 1; j < h1->GetNbinsY(); j++){
      h2->SetBinContent(j, i, h1->GetBinContent(i, j));
      h2->SetBinError(j, i, h1->GetBinError(i, j));
    }
  }  
  return h2;
}

void drawMask(TH2* mask, bool isPolar){
  if(isPolar){
    mask = polar_to_cartesian(transpose(mask));
    mask->SetLineWidth(1);
  }
  mask->SetLineColor(kRed);
  
  mask->Draw("SAME,CONT3");
}

void EfficiencyPlots(TH2* data, double ebeam, double lumi, double lumi_err,  TH2* mask, bool smooth_small_theta = 0){
  
  double Z = 6;
  double mass = 12*AMU;
  
  TH1* xs_per_mott = get_xs_per_mott(data, ebeam, mass, Z, lumi, mask);
  xs_per_mott->SetName(Form("xs_per_mott_%f", ebeam));
  apply_lumi_sys_error(xs_per_mott, lumi_err);

  TCanvas* c1 = new TCanvas();
  c1->SetWindowSize(1200, 800);
  c1->Divide(2,2);
  c1->cd(1);
  TH1* model = full_carbon_model(ebeam);

  model->SetTitle("Data vs Model;theta (rad);#sigma/#sigma_{Mott}");
  model->SetStats(0);
  stylize_axes(model);
    
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

  TLegend* legend = new TLegend(0.6, 0.75, .95, .95);
  legend->AddEntry(model, "model (pre rad corr)");
  legend->AddEntry(model_rad_corr, "model (w/ rad corr)");
  legend->AddEntry(xs_per_mott, "data");

  legend->Draw();
  TLatex* info = new TLatex();
  info->DrawLatex(.12, .76, "Target:         C12");
  info->DrawLatex(.12, .68,Form("E_{beam}:           %.3f GeV", ebeam));
  info->DrawLatex(.12, .60, "Energy cut:  85% E_{beam}");
  
  //SECOND QUADRANT
  c1->cd(2);
  


  TH1* efficiency = (TH1*)xs_per_mott->Clone();
  efficiency->Divide(model_rad_corr);
  efficiency->SetFillColor(kBlack);
  efficiency->SetTitle("Efficiency vs theta; theta (rad); efficiency");
  efficiency->SetStats(0);
  stylize_axes(efficiency);
  efficiency->Draw("E4");
  
  TLine* line = new TLine();
  line->SetLineWidth(2);
  line->SetLineColor(kRed);
  line->DrawLine(0, 1, .2, 1);

  
  cout << data->GetNbinsX() << " "  << data->GetNbinsY() << endl;
  TH2 * eff_2d = get_xs_per_mott_2d(data, ebeam, mass, Z, lumi, mask);
  eff_2d->SetName(Form("eff_2d_%f", ebeam));
  eff_2d->SetTitle("Efficiency (polar);theta (rad);phi (rad)");
  eff_2d->SetStats(0);
  stylize_axes(eff_2d);
  
  cout << eff_2d->GetNbinsX() << " "  << eff_2d->GetNbinsY() << endl;
  TH2 * model_2d = to_2d(model_rad_corr, eff_2d);
  cout << " " << model_2d->GetNbinsX() << " "  << model_2d->GetNbinsY() << endl;
  eff_2d->Divide(model_2d);
  bool rebinX = true;
  if(rebinX){
    int rx = 5, ry = 3;
    eff_2d = eff_2d->Rebin2D(rx, ry, "tempname");
    eff_2d->Scale(1./(rx*ry));
  }

  eff_2d->SetMaximum(1.2);
  c1->cd(4);
  eff_2d->DrawCopy("COLZ");

  drawMask(mask, 0);
  

  //THIRD QUADRANT
  c1->cd(3);
  eff_2d = transpose(eff_2d);
  TH2* cart = polar_to_cartesian(eff_2d);
  cart->SetStats(0);
  cart->SetTitle("Efficiency (cartesian); #thetacos(#phi); #thetasin(#phi)");
  cart->SetName(Form("eff2d_%.3f", ebeam));
  cart->SetMaximum(1.2);
  stylize_axes(cart);
  
  cart->GetXaxis()->SetRangeUser(-.15, .2);
  cart->GetYaxis()->SetRangeUser(-.1, .1);
  cart->GetYaxis()->SetTitleOffset(.9);

  cart->Draw("COLZ");

  //special algorithm for smoothing small theta
  if(smooth_small_theta){
    TH2* eff_2d_small_theta = (TH2*)eff_2d->Clone();
    eff_2d_small_theta->RebinX(4);
    eff_2d_small_theta->Scale(1/4.);
    for(int i = 0; i < eff_2d_small_theta->GetNbinsX(); i++){
      for(int j = 0; j < eff_2d_small_theta->GetNbinsY(); j++){
	if(eff_2d_small_theta->GetYaxis()->GetBinCenter(j)>.06)
	  eff_2d_small_theta->SetBinContent(i,j,0);
      }
    }
    TH2* cart_small_theta = polar_to_cartesian(eff_2d_small_theta);
    cart_small_theta->SetMaximum(1.2);
    cart_small_theta->SetFillColorAlpha(kWhite, 0);
    cart_small_theta->Draw("SAME COLZ");
  }
  cart->SetTitleOffset(.9);
  drawMask(mask,1);
  c1->cd(0);
}

void EfficiencyPlots(){
  double ebeam = 1.056;
  TFile* carbon_file = TFile::Open("~/data/fee/tweakpass6_100417/5779.root");
  TString histname = "85_percent/theta vs phi track extrap cut";
    //"85_percent/theta vs phi no track quality cuts";
  TH2* theta_vs_phi = (TH2*)carbon_file->Get(histname);
  double lumi = 45837.645e-9/128.*2.213e-3/1.60217662e-19;
  double lumi_err = .0119;
  TH2* mask = (TH2*)TFile::Open("fee_mask.root")->Get("mask");
  EfficiencyPlots(theta_vs_phi, ebeam, lumi, lumi_err, mask);
  gPad->SaveAs("out/img/2015/hps_fee_efficiency_2015.pdf");
  ebeam = 2.306;
  carbon_file = TFile::Open("~/data/fee/pass1_072817/8054.root");
  theta_vs_phi = get_2016_prescaled_hist(carbon_file, "85_percent/theta vs phi chi2 cut");
  lumi = 142582.897e-9/2*2.213e-3/1.60217662e-19;
  lumi_err = sqrt(lumi_err*lumi_err+.001*.001);
  EfficiencyPlots(theta_vs_phi, ebeam, lumi, lumi_err, mask,1);
  gPad->SaveAs("out/img/2016/hps_fee_efficiency_2016.pdf");
}
