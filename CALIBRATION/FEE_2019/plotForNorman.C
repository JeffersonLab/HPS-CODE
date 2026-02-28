
const int N=7;

int crs[N]={366,367,368,369,370,371,372};

void plotForNorman(){

  TFile *fPost_6=new TFile("input_iter4/fee_10310_10714.root");
  TH1D *hPost_6=0;

  TFile *fPre_6=new TFile("input_iter1/fee_10115_10718.root");
  TH1D *hPre_6=0;

  TFile *fPost_1=new TFile("input_iter3/fee_10030_10064.root");
  TH1D *hPost_1=0;

  TFile *fPre_1=new TFile("input_iter1/fee_10030_10064.root");
  TH1D *hPre_1=0;
   
  for (int ii=0;ii<N;ii++){
    string hname;
    if (crs[ii]<=99){
      hname=string(Form(" %i",crs[ii]));
    }else{
      hname=string(Form("%i",crs[ii]));
    }
   
    if (ii==0){
      hPost_6=(TH1D*)fPost_6->Get(hname.c_str());
      hPre_6=(TH1D*)fPre_6->Get(hname.c_str());
      hPost_1=(TH1D*)fPost_1->Get(hname.c_str());
      hPre_1=(TH1D*)fPre_1->Get(hname.c_str());
    }else{
      hPost_6->Add((TH1D*)fPost_6->Get(hname.c_str()));
      hPre_6->Add((TH1D*)fPre_6->Get(hname.c_str()));
      hPost_1->Add((TH1D*)fPost_1->Get(hname.c_str()));
      hPre_1->Add((TH1D*)fPre_1->Get(hname.c_str()));

    }
  }

  hPost_6->Scale(1./hPost_6->Integral());
  hPost_6->Draw("HIST");

  hPost_1->Scale(1./hPost_1->Integral());
  hPost_1->SetLineStyle(7);
  hPost_1->Draw("HISTSAMES");

  hPre_6->Scale(1./hPre_6->Integral());
  hPre_6->SetLineColor(2);
  hPre_6->Draw("HISTSAMES");

  
  
  hPre_1->Scale(1./hPre_1->Integral());
  hPre_1->SetLineColor(2);
  hPre_1->SetLineStyle(7);
  hPre_1->Draw("HISTSAMES");


}
