#include "TH1.h"
#include "TCanvas.h"
#include "TNtuple.h"
#include "TPad.h"
#include "TTree.h"
#include "TMath.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "TGraphErrors.h"
#include "TDirectory.h"
#include "TF1.h"
#include "TROOT.h"
#include <vector>
#include "unistd.h"
#include "TSystem.h"
#include "TBranch.h"
#include "TGraphErrors.h"
#include "TFile.h"
#include "TH2.h"
#include "Riostream.h"

typedef long long long64;

const std::string encoder_string = "system:6,layer:2,ix:-8,iy:-6";

///////////////////////////////////////////////////////////////////////////////////////
float findTime(float y, float a, float b){
  //y = ax+b
  float x = (y-b)/a;
  return x;
}

//time in ns and energy in GeV
float correctTimeWalk(float time, float energy){

  const float p0 = 0.9509;
  const float p1 = -33.21;
  const float p2 = 0.2614;
  const float p3 = -0.9128;
  const float p4 = 0.6251;

  return time - (exp(p0+p1*energy) + p2 + p3*energy + p4*energy*energy);

}

Double_t CrystalBall(Double_t *x,Double_t *par) {

  Double_t sigma = ((Double_t)par[3]);
  if (par[3]<0){sigma = -par[3];}


  Double_t t = (x[0]-par[2])/sigma;
  if (par[0] < 0) t = -t;

  Double_t absAlpha = fabs((Double_t)par[0]);

  if (t >= -absAlpha) {
    return par[4]*exp(-0.5*t*t);
  }
  else {
    Double_t a =  TMath::Power(par[1]/absAlpha,par[1])*exp(-0.5*absAlpha*absAlpha);
    Double_t b= par[1]/absAlpha - absAlpha; 

    return par[4]*(a/TMath::Power(b - t, par[1]));
  }
  
}
TF1 *CBFit(TH1 *h1){
  float max = h1->GetBinCenter(h1->GetMaximumBin());
  TF1 *crystal = new TF1("crystal",CrystalBall,0.029,0.036,5);
  Double_t peakEntry = h1->GetBinContent(h1->GetMaximumBin());
  float rms = h1->GetRMS();
  crystal->SetParameters(1,4.5,max,rms/5,peakEntry);
  //crystal->FixParameter(0,1.1);
  crystal->SetParLimits(0,0.5,2);
  crystal->FixParameter(1,4.5);
  //crystal->SetParLimits(1,0,30);
  crystal->SetParNames("#alpha","n","#mu","#sigma","A");
  return crystal;

}

