#include "../include/omniheader.h"

void PlotPrescales2016(char* save = 0){
  TCanvas* c1 = new TCanvas();
  TH1* s1 = new TH1D("single1", "single1", 47, -23.5, 23.5);
  TH1* s0 = new TH1D("single0", "single0", 47, -23.5, 23.5);
  for(int j = -23; j<=23; j++){
    int i = 0;
    if(j <= 0)
      i = 23+j;
    else
      i = j+24;
    if(j == 0){
      s0->SetBinContent(i, 0.01);
      s1->SetBinContent(i, 0.01);
    }
    s0->SetBinContent(i, 4097);
    double prescaleSSP = 0;
    if(j <= -13 || j>=6)
      prescaleSSP = 1;
    else if (j <= -9 || j >= 2)
      prescaleSSP = 80;
    else if (j <= -7  || j >= -2)
      prescaleSSP = 1300;
    else 
      prescaleSSP = 18000;
    s1->SetBinContent(i, 2*prescaleSSP);
  }
  s1->SetTitle("Trigger Prescales (2016);Cluster Seed Hit Index ix; Prescale");
  s1->SetLineColor(kRed);
  s1->SetStats(0);
  s0->SetLineColor(kBlue);
  s1->Draw();
  s0->Draw("SAME");
  TLegend* legend = new TLegend(.75, .85, .95, .95);
  legend->AddEntry(s0, "Single0 Trigger");
  legend->AddEntry(s1, "Single1 Trigger");
  legend->Draw();
  c1->SetLogy();
  if(save != 0)
     c1->SaveAs(save);
}
