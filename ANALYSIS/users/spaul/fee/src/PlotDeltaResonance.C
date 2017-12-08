#include "../include/omniheader.h"
#include "../include/xs_model/Carbon.h"

CarbonDeltaResonance * cdr = new CarbonDeltaResonance(2.306, 2.306*.85);
double delta(double theta, double eprime){
  double Q2 = 4*pow(sin(theta/2),2)*2.306*eprime;
  double omega = 2.306-eprime;
  return cdr->response(Q2, omega)*(Q2/(Q2+omega*omega)+pow(tan(theta/2),2));
}

double delta_smear(double theta, double eprime, double smear){
  double tot = 0;
  double dz = .1;
  for(double z = -4; z<4; z+=dz){
    tot += dz *delta(theta, eprime + z*smear)*exp(-z*z/2)/sqrt(2*TMath::Pi());
  }
  return tot;
}
void PlotDeltaResonance(){
  
  //TTree* ntuple = (TTree*) TFile::Open("/Users/spaul/data/hps_008054_nt_FEE_3.11.1.root")->Get("ntuple");   
   TTree* ntuple = (TTree*) TFile::Open("/Users/spaul/data/8054_loose_fee.root")->Get("ntuple");
  TString cut = "fspClE>0 && fspMatchChisq<10 && isSingle1 && abs(fspClT-56)<6 && fspClHits >=2 && isPulserTrigger";
  TString  fiducial = "abs(fspClY) > 30 && abs(fspClY)<83 && !(abs(fspClY)< 44 && fspClX > -100 && fspClX < -30)";
  cut = cut + "&& " + fiducial;
  
  TString theta_form = "atan(hypot(cos(.0305)*fspPX-sin(.0305)*fspPZ, fspPY)/fspPZ)";

  double theta = .100;
  double dtheta = .005;
  
  ntuple->Draw("fspClE>>h(100, 1.5, 2.5)", cut + Form(" && abs(" + theta_form + "- %f) < %f",theta, dtheta), "COLZ");
  TH1* h = ntuple->GetHistogram();

  
  TF1* f1 = new TF1("f1", Form("[0]*(gausn(2)+[1]*delta_smear(%f, x, 2.306*.033))", theta), 1.5, 3);
  //TF1* f1  =  new TF1("f1", "delta(theta, x)", 0, 3);
  f1->FixParameter(2,1);
  f1->FixParameter(3, 2.306/(1+2*2.306/.938*pow(sin(theta/2),2)));
  f1->FixParameter(4, .033*2.306);
  f1->SetParameter(0, 1);
  f1->SetParameter(1, 1);
  f1->Draw("");
  h->Fit(f1, "", "", 1.6, 2.5);
}
