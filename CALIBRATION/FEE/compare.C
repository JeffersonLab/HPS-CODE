void compare(){

  TFile *fPre=new TFile("runs.preSlope.root");
  TFile *fPost=new TFile("runs.postSlope.root");



  TGraphErrors *g1Pre=(TGraphErrors*)fPre->Get("325__-3_-3");
  TGraphErrors *g1Post=(TGraphErrors*)fPost->Get("325__-3_-3");

  cout<<g1Pre<<" "<<g1Post<<endl;
  
  g1Post->SetMarkerColor(2);
  g1Post->SetLineColor(2);

  g1Pre->Draw("AP");
  g1Post->Draw("PSAME");
    




}
