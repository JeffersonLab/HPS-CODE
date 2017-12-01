#include "CrossSectionComponent.h"
#include "RadiativeCorrection.h"
#include "../xs_model/Tungsten.h"
#include "../xs_model/Carbon.h"
#include "TH1.h"
#ifndef CROSS_SECTION_UTIL_H
#define CROSS_SECTION_UTIL_H

bool useOldQuasi = 1;

TH1 * generate_histogram_from_xs(CrossSectionComponent * xs, TString name = "h", double theta_min = 0, double theta_max = .200, int nbins = 400){
  TH1* h = new TH1D(name, name, nbins, theta_min, theta_max);
  for(int i = 0; i<nbins; i++){
    double theta = (i+.5)*(theta_max-theta_min)/nbins;
    double xs_per_mott = xs->get_xs_per_mott(theta);
    double sys_error = xs->get_relative_sys_error_on_xs(theta)*xs_per_mott;
    h->SetBinContent(i, xs_per_mott);
    h->SetBinError(i, sys_error);
  }
  return h;
}

TH1* full_carbon_model(double ebeam){
  TH1* h1 = generate_histogram_from_xs(new CarbonElastic(ebeam), "full carbon model");
  if(useOldQuasi)
    h1->Add(generate_histogram_from_xs(new CarbonQuasielastic(ebeam), "qua"));
  else
    h1->Add((TH1*)TFile::Open(Form("voodoo/%d.root",(int)(ebeam*1000)))->Get("quasi_plus_delta"));
  h1->Add(generate_histogram_from_xs(new CarbonInelastic3Minus(ebeam), "ine3m"));
  h1->Add(generate_histogram_from_xs(new CarbonInelastic2Plus(ebeam), "ine2p"));
  return h1;
}

TH1* get_rad_corr_hist(SimpleCrossSectionComponent * xs_component, double ecut, double t, double b, double sigma_e, const int nint = 5, TString name = "h", double theta_min = 0, double theta_max = .200, int nbins = 400){
  double ebeam = xs_component->_ebeam;
  TH1* h = new TH1D(name, name, nbins, theta_min, theta_max);
  IntegralRadiativeCorrection* rad_corr
    = new IntegralRadiativeCorrection(ebeam, ecut, t, b, sigma_e);

  //calculate for a few values of theta, and then interpolate
  double y[nint];
  double x[nint];
  for(int i = 0; i< nint; i++){
    double theta = theta_min + (theta_max-theta_min)*i/(nint-1);
    //replace 0 with 1 mrad
    if(theta == 0)
      theta = .001;
    x[i] = theta;
    y[i] = rad_corr->get_correction_factor(theta);
  }
  
  for(int i = 0; i< nbins; i++){
    double theta = (i+.5)*(theta_max-theta_min)/nbins;
    double rad_corr_val = 0;  //TODO fill this in
    for(int i = 0; i< nint-1; i++){
      if(theta < x[i+1] && theta >= x[i]){
	rad_corr_val = y[i]+(theta-x[i])*(y[i+1]-y[i])/(x[i+1]-x[i]);
      }
    }
    double rad_corr_err = .005; //TODO fill this in
    if(!isnan(rad_corr_val))
      h->SetBinContent(i, rad_corr_val);
    h->SetBinError(i, rad_corr_err);
  }
  return h;
}

TH1* full_carbon_model_with_rad_corr(double ebeam, double ecut, double t, double b, double sigma_e){
  SimpleCrossSectionComponent * ele =  new CarbonElastic(ebeam);
  TH1* h_ele = generate_histogram_from_xs(ele, "ele");
  h_ele->Multiply(get_rad_corr_hist(ele, ecut, t, b, sigma_e));
  TH1* full = (TH1*)h_ele->Clone("full carbon model");


  TH1* h_qua;
  if(useOldQuasi){
    SimpleCrossSectionComponent * qua = new CarbonQuasielastic(ebeam);
    h_qua = generate_histogram_from_xs(qua, "qua");
    h_qua->Multiply(get_rad_corr_hist(qua, ecut, t, b, sigma_e));
    //cout << "got qua" << endl;
  }
  else{
    h_qua = (TH1*)TFile::Open(Form("voodoo/%d.root",(int)(ebeam*1000)))->Get("quasi_plus_delta");
  }
  //cout << h_qua->GetNbinsX() << endl;
  // return full;
  
  full->Add(h_qua);

  SimpleCrossSectionComponent * ine3m = new CarbonInelastic3Minus(ebeam);
  TH1* h_ine3m = generate_histogram_from_xs(ine3m, "ine3m");
  h_ine3m->Multiply(get_rad_corr_hist(ine3m, ecut, t, b, sigma_e));
  full->Add(h_ine3m);
 cout << "got 3m" << endl;
  SimpleCrossSectionComponent * ine2p = new CarbonInelastic2Plus(ebeam);
  TH1* h_ine2p = generate_histogram_from_xs(ine2p, "ine3m");
  h_ine2p->Multiply(get_rad_corr_hist(ine2p, ecut, t, b, sigma_e));
  full->Add(h_ine2p);
   cout << "got full" << endl;
  return full;
}

TH1* full_tungsten_model_with_rad_corr(double ebeam, double ecut, double t, double b, double sigma_e){
  SimpleCrossSectionComponent * ele =  new TungstenElastic(ebeam);
  TH1* h_ele = generate_histogram_from_xs(ele, "ele");
  h_ele->Multiply(get_rad_corr_hist(ele, ecut, t, b, sigma_e));
  TH1* full = (TH1*)h_ele->Clone("full_carbon_model");
  
  SimpleCrossSectionComponent * qua = new TungstenQuasielastic(ebeam);
  TH1* h_qua = generate_histogram_from_xs(qua, "qua");
  h_qua->Multiply(get_rad_corr_hist(qua, ecut, t, b, sigma_e));
  full->Add(h_qua);
  
  return full;
}
#endif
