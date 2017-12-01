#include "../include/xs_model/Carbon.h"
#include "../include/xs_model/CrossSectionComponent.h"
#include "../include/xs_model/CrossSectionUtil.h"
//#include "../include/xs_model/RadiativeCorrection.h"

#include "../include/util/GraphUtil.h"
#include "../include/measurement/MeasurementUtil.h"
#include "../include/omniheader.h"

TH2* unweighted(TFile* file, TString name){
  TH2* h1 = (TH2*)file->Get(name + " r1")->Clone();
  h1->Add((TH2*)file->Get(name + " r2"));
  h1->Add((TH2*)file->Get(name + " r3"));
  h1->Add((TH2*)file->Get(name + " r4"));

  return h1;
  
}


TH2* theta_to_2d(TH1* source, TH2* templat, bool isUxuy){
  TString name = source->GetName();
  if(isUxuy)
    name += "_uxuy";
  else
    name += "_thetaphi";
  TH2* ret = (TH2*) templat->Clone();
  ret->SetName(name);
  for(int i = 0; i < ret->GetNbinsX(); i++){
    for(int j = 0; j < ret->GetNbinsY(); j++){
      double theta;
      if(isUxuy)
	theta = sqrt(pow(ret->GetXaxis()->GetBinCenter(i),2) + pow(ret->GetYaxis()->GetBinCenter(j),2));
      else theta = ret->GetXaxis()->GetBinCenter(i);
      //if(isUxuy) cout << theta << endl;
      double z = 0, dz = 0;

      if(theta < .02)
	theta = .02;
      if(theta > .170)
	theta = .170;
      for(int k = 0; k < source->GetNbinsX(); k++){
	double x1 = source->GetXaxis()->GetBinCenter(k);
	double x2 = source->GetXaxis()->GetBinCenter(k+1);
	double dOmega = ret->GetXaxis()->GetBinWidth(1)*ret->GetYaxis()->GetBinWidth(1);
	if(!isUxuy) dOmega *= sin(theta);
	//else dOmega*= 
	if(x1 < theta && x2 >=theta){
	  double z1 = source->GetBinContent(k);
	  double z2 = source->GetBinContent(k+1);
	  double dz1 = source->GetBinError(k);
	  double dz2 = source->GetBinError(k+1);
	  z = (z1+(theta-x1)*(z2-z1)/(x2-x1))*dOmega;
	  //if(isUxuy) cout << theta << " " << z << endl;
	  dz = (dz1+(theta-x1)*(dz2-dz1)/(x2-x1))*dOmega;
	  //break;
	}
      }
      
      
      ret->SetBinContent(i, j, z);
      ret->SetBinError(i, j, dz);
    }
  }
  return ret;
  
}

void antipode_test(TH2* thetaphi_eff){
  TCanvas* c4 = new TCanvas();
  bool smear = 1;
  TH1* thetaphi_bk = (TH1*)thetaphi_eff->Clone();
  if(smear){
    for(int i = 0; i < thetaphi_eff->GetNbinsX(); i++){
      for(int j = 0; j < thetaphi_eff->GetNbinsY(); j++){
	double z = 0;
	for(int k = -50; k <= 50; k+=5){
	  for(int l = -50; l<= 50; l+=5){
	    if(i+k>0&& i+k <= thetaphi_eff->GetNbinsX() && j+l>0 && j+l < thetaphi_eff->GetNbinsY()){
	      double g = exp(-k*k/(2*24*24)-l*l/(2*12*12));
	      z+= thetaphi_bk->GetBinContent(i+k,j+l)*g;
	    }
	  }
	}
	thetaphi_eff->SetBinContent(i, j,z);
	//thetaphi_eff->SetBinError(i, j, thetaphi_eff->GetBinError(i, j));
      }
    }
  }
  
  TH2* antipode = (TH2*) thetaphi_eff->Clone();
  for(int i = 0; i< antipode->GetNbinsX(); i++){
    for(int j = 0; j< antipode->GetNbinsY(); j++){
      int deltaj = antipode->GetNbinsY()/2;
      int jprime = j> deltaj ? j - deltaj : j + deltaj;
      antipode->SetBinContent(i, j, thetaphi_eff->GetBinContent(i,jprime));
      antipode->SetBinError(i, j, thetaphi_eff->GetBinError(i, jprime));
    }
  }

  
  
  antipode->Draw("COLZ");
  new TCanvas();
  TH2* product_efficiency = (TH2*) thetaphi_eff->Clone();
  product_efficiency->Multiply(antipode);
  product_efficiency->Draw("COLZ");

  new TCanvas();
  TH1* projection = product_efficiency->ProjectionX();
  projection->Draw();
}
 
  

map<char*, TCanvas*> DissertationEfficiencyPlots(TH2* uxuy, TH2* thetaphi, TH1* model, TString prepend_title = "", bool isWeighted = 0){
  map<char*, TCanvas*> canvases;

  TCanvas* c0 = new TCanvas();
  canvases["uxuy"] = c0;
  uxuy->SetStats(0);
  uxuy->Draw("COLZ");
  uxuy->SetTitle(prepend_title+" angular distribution" + (isWeighted ? " (weighted)" : "")  + ";ux;uy;# of particles");
  uxuy->GetXaxis()->SetRangeUser(-.15, .19);
  uxuy->GetYaxis()->SetRangeUser(-.1, .1);
  c0->SetWindowSize(700, 400);
  c0->SetLogz();
  
  TCanvas* c01 = new TCanvas();
  canvases["thetaphi"] = c01;
  thetaphi->SetStats(0);
  thetaphi->SetTitle(";#theta (rad);#phi (rad);# of particles");
  thetaphi->Draw("COLZ");
  c01->SetLogz();
  c01->SetWindowSize(700, 400);

  if(model == NULL){
    return canvases;
  }
  TH2* uxuy_eff = (TH2*) uxuy->Clone();
  TH2* thetaphi_eff = (TH2*) thetaphi->Clone();

  TH2* model_uxuy =  theta_to_2d(model, uxuy, 1);
  cout << model_uxuy->GetBinContent(100, 100) << endl;
  TH2* model_thetaphi = theta_to_2d(model, thetaphi, 0);

  uxuy_eff->Divide(model_uxuy);
  thetaphi_eff->Divide(model_thetaphi);


  

  TCanvas* c1 = new TCanvas();
  canvases["uxuy_eff"] = c1;
  c1->SetWindowSize(700, 400);
  uxuy_eff->SetTitle(prepend_title+" efficiency;ux;uy;efficiency");
  uxuy_eff->SetMaximum(1.5);
  uxuy_eff->Draw("COLZ");

  TCanvas* c2 = new TCanvas();
  c2->SetWindowSize(700, 400);
  canvases["thetaphi_eff"] = c2;
  thetaphi_eff->SetMaximum(1.5);
  thetaphi_eff->SetTitle(";#theta (rad);#phi (rad);efficiency");
  thetaphi_eff->Draw("COLZ");


  int firstbintop, lastbintop, firstbinbot, lastbinbot;
  for(int i = 0; i< uxuy->GetNbinsY(); i++){
    double y1 = uxuy->GetYaxis()->GetBinCenter(i);
    double y2 = uxuy->GetYaxis()->GetBinCenter(i+1);
    if(y1 <= .036 && y2 >= .036)
      firstbintop = i;
    if(y1 <= .05 && y2 >= .05)
      lastbintop = i;
    if(y1 <= -.036 && y2 >= -.036)
      lastbinbot = i;
    if(y1 <= -.05 && y2 >= -.05)
      firstbinbot = i;
   }
  
  TH1* slice_top = uxuy->ProjectionX("_top", firstbintop, lastbintop);
  TH1* slice_bot = uxuy->ProjectionX("_bot", firstbinbot, lastbinbot);

  //stat-error-only versions to overlay with the total-error plots
  TH1* slice_top_stat = (TH1*) slice_top->Clone();
  TH1* slice_bot_stat = (TH1*) slice_bot->Clone();
  
  TH1* slice_model = model_uxuy->ProjectionX("model_top", firstbintop, lastbintop);
  TH1* slice_model_no_err = (TH1*)slice_model->Clone();
  for(int i = 0; i < slice_model->GetNbinsX(); i++){
    int biny = (firstbintop+lastbintop)/2;
    double bin_error = model_uxuy->GetBinError(i, biny)*slice_model->GetBinContent(i)/ model_uxuy->GetBinContent(i, biny);
    
    slice_model->SetBinError(i, bin_error);
    slice_model_no_err->SetBinError(i, 0);
  }
  TCanvas* c3 = new TCanvas();
  canvases["slices"] = c3;
  slice_top->SetStats(0);
  slice_top->Divide(slice_model);
  slice_bot->Divide(slice_model);
  slice_top_stat->Divide(slice_model_no_err);
  slice_bot_stat->Divide(slice_model_no_err);
  //slice_top->SetLineColor(kRed);
  //slice_bot->SetLineColor(kBlack);
  slice_top->SetTitle(prepend_title + " u_{x} vs efficiency;u_{x}; efficiency");

  bool useFill = 1;
  if(useFill){
    slice_top->SetFillStyle(3245);
    slice_bot->SetFillStyle(3254);
    slice_top->Smooth();
    slice_bot->Smooth();
    slice_top->SetFillColor(kRed-9);
    slice_bot->SetFillColor(kGray+1);
    slice_top->SetLineColor(kRed);
    slice_bot->SetLineColor(kBlack);
    slice_top_stat->SetLineColor(kRed);
    slice_bot_stat->SetLineColor(kBlack);
    slice_bot->Draw("E3");
    slice_top->Draw("E3 SAME");
    slice_top_stat->Draw("SAME");
    slice_bot_stat->Draw("SAME");
    
  }
  else{
    slice_top->Draw("");
    slice_bot->Draw("SAME");
  }
  
  TLegend * ary = new TLegend(.70, .85, .95, .95);
  ary->AddEntry(slice_top, "top");
  ary->AddEntry(slice_bot, "bottom");
  ary->Draw();


  //antipode_test(thetaphi_eff);

   return canvases;
}

void DissertationEfficiencyPlots(char* save = 0){

  double lumi = 45837.645e-9/128.*2.213e-3/1.60217662e-19;
  double lumi_err = .0119;
  
  TFile* file_2015 = TFile::Open("~/data/fee/tweakpass6_112817/5779.root");
  TString cutlevel = " chi2 cut";//" track extrap cut";
  TH2* thetaphi_2015 = (TH2*)file_2015->Get("85_percent/theta vs phi"+cutlevel);
  TH2* uxuy_2015 = (TH2*)file_2015->Get("85_percent/ux vs uy"+cutlevel);

  thetaphi_2015->SetStats(0);
  uxuy_2015->SetStats(0);
  thetaphi_2015->SetTitle("theta vs phi;theta (rad);phi (rad)");
  uxuy_2015->SetTitle("dx/dz vs dy/dz; dx/dz; dy/dz");
  
  double ebeam = 1.056;
  double ecut = ebeam*.85;
  double t = .042;
  double b = 1.34;
  double sigma_e = .045;
  
  TH1* model_2015 = full_carbon_model_with_rad_corr(ebeam, ecut, t, b, sigma_e);
  TF1* mott_2015 = new TF1("f", "mott(x, 1.056, 12*.938, 6)", 0, .2);
  model_2015->Multiply(mott_2015);
  model_2015->Scale(lumi);

  //  model_2015->Draw("");
  map<char*, TCanvas*> canvases_2015 = DissertationEfficiencyPlots(uxuy_2015, thetaphi_2015, model_2015, "Run 5779");

  TFile* file_2016 = TFile::Open("~/data/fee/pass1_112817a/8054.root");
  TH2* uxuy_2016_uw = unweighted(file_2016,"85_percent/ux vs uy"+cutlevel);
  TH2* thetaphi_2016_uw = unweighted(file_2016,"85_percent/theta vs phi"+cutlevel);
  
  TH2* thetaphi_2016 = get_2016_prescaled_hist(file_2016,"85_percent/theta vs phi"+cutlevel, -3);
  thetaphi_2016->Rebin2D(2,2);
  TH2* uxuy_2016 = get_2016_prescaled_hist(file_2016,"85_percent/ux vs uy"+cutlevel, -3);
  uxuy_2016->Rebin2D(1,1);

  TH1* model_2016 = full_carbon_model_with_rad_corr(2.306, 2.306*.85, t, b, .033);
  TF1* mott_2016 = new TF1("f", "mott(x, 2.306, 12*.938, 6)", 0, .2);
  model_2016->Multiply(mott_2016);

  double lumi_2016 = lumi = 142582.897e-9/2*2.213e-3/1.60217662e-19;
  model_2016->Scale(lumi_2016);

  map<char*, TCanvas*> canvases_2016 = DissertationEfficiencyPlots(uxuy_2016, thetaphi_2016, model_2016, "Run 8054", 1);

  map<char*, TCanvas*> canvases_2016_unweighted = DissertationEfficiencyPlots(uxuy_2016_uw, thetaphi_2016_uw, 0, "Run 8054");
  /* 
     now save the canvases
   */
  if(save != 0){
    TString dir = save;
    canvases_2015["uxuy"]->SaveAs(dir + "/5779_uxuy.pdf");
    canvases_2015["thetaphi"]->SaveAs(dir + "/5779_thetaphi.pdf");
    canvases_2015["uxuy_eff"]->SaveAs(dir + "/5779_uxuy_eff.pdf");
    canvases_2015["thetaphi_eff"]->SaveAs(dir + "/5779_thetaphi_eff.pdf");
    canvases_2015["slices"]->SaveAs(dir + "/5779_slice.pdf");

    canvases_2016["uxuy"]->SaveAs(dir + "/8054_uxuy_weighted.pdf");
    canvases_2016["thetaphi"]->SaveAs(dir + "/8054_thetaphi_weighted.pdf");
    canvases_2016["uxuy_eff"]->SaveAs(dir + "/8054_uxuy_eff.pdf");
    canvases_2016["thetaphi_eff"]->SaveAs(dir + "/8054_thetaphi_eff.pdf");
    canvases_2016["slices"]->SaveAs(dir + "/8054_slice.pdf");

    canvases_2016_unweighted["uxuy"]->SaveAs(dir + "/8054_uxuy.pdf");
    canvases_2016_unweighted["thetaphi"]->SaveAs(dir + "/8054_thetaphi.pdf");
  }
  
}
