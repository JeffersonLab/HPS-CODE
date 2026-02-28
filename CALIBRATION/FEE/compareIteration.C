#include "util/utilities.h"


int calcXX(int ix){
  int xx;
  if (ix<0) xx=ix+23;
  else xx=ix+22;
  return xx;
}

//input Y in the range [0,9]
//returns y as crystal iy [-5,5]
int calcYY(int iy){

  int yy;
  if (iy<0) yy=iy+5;
  else yy=iy+4;

  return yy;
}

void compareIteration(int iX,int iY){

  const int N=442;

  int xx=calcXX(iX);
  int yy=calcYY(iY);
  int dbid=xy2dbid(xx,yy);


  cout<<iX<<" "<<iY<<" positive_indexing: "<<xx<<" "<<yy<<" "<<dbid<<endl;
  TFile *f,*f2,*f3;
  TFile *fMC=new TFile("input_MC/FEE_MC.root");

  TH1D *hMC=(TH1D*)fMC->Get(Form("%3d",dbid));

  
  TH1D *h3=0;
  
  f=new TFile(Form("input_iter3/fee_10101_10115.root"));
  //f=new TFile(Form("input_iter4/10310.4.root"));
  TH1D *h=(TH1D*)f->Get(Form("%3d",dbid));

  f2=new TFile(Form("afterCalib/fee_10101_10115.root"));
  //f2=new TFile(Form("afterCalib/10310.1.root"));
  TH1D *h2=(TH1D*)f2->Get(Form("%3d",dbid));

  f3=new TFile(Form("input_iter1/fee_10115_10718.root"));
  h3=(TH1D*)f3->Get(Form("%3d",dbid));
  
  cout<<h<<" "<<hMC<<endl;
  
  double maxDATA,maxMC;
  maxDATA=h->GetMaximum();
  maxMC=hMC->GetMaximum();

  if (maxDATA>0&&maxMC>0){
    hMC->Scale(maxDATA/maxMC);
  }


  h->Draw();
  h2->SetLineColor(2);
  h2->Draw("HISTSAMES");
  hMC->SetLineColor(3);
  hMC->SetLineWidth(3);
  hMC->SetLineStyle(7);
  hMC->Draw("HISTSAME");
  /*if (h3!=0){
    h3->SetLineColor(4);
    h3->Draw("HISTSAMES");
    }*/
}
