
TString evtType[]={"gemL1","gemL2","epemL1L1","epemL1L2","epemL2L1","epemL2L2"};
Double_t nEvtType[]={406872,21407,77719,4249,19634,1021};



Double_t fitFcn(Double_t* x,Double_t* par) {
  Double_t swab=par[0];
  Double_t stri=par[1];
  Double_t fconv=par[2];
  Double_t fL1=par[3];
  Double_t iL1=par[4];
  Double_t xx=x[0];
  cout<<xx<<endl;
  if(xx<1) 
    cout<<"xx==0 "<< (1-fconv)*(1-iL1)*swab<<endl;
    return (1-fconv)*(1-iL1)*swab; //gemL1
  if(xx<2)  
    return    (1-fconv)*iL1*swab; //geml2
  if(xx<3) 
    return fL1*(1-iL1)*(1-iL1)*fconv*swab+ (1-iL1)*(1-iL1)*stri;//epemL1L1
  if (xx<4) 
    return fL1*iL1*(1-iL1)*fconv*swab+iL1*(1-iL1)*stri; //epemL1L2
  if(xx<5) 
    return (1-fL1)*(1-iL1)*fconv*swab+fL1*iL1*(1-iL1)*fconv*swab+iL1*(1-iL1)*stri; //epemL2L1
  if(xx<6 )
    (1-fL1)*iL1*fconv*swab+fL1*iL1*iL1*fconv*swab+iL1*iL1*stri;  //epemL2L2
  return 0.0;
}    

void WABTri0dFit(){
  TH1I* typeData=new TH1I("typeData","typeData",6,0,6);
  for(int i=0;i<6;i++){
    typeData->SetBinContent(i,nEvtType[i]);
  }
  TF1* tfunc=new TF1("f",fitFcn,0,5,5);
  
  //
  tfunc->SetParName(0,"swab");
  tfunc->SetParameter(0,420000);
  tfunc->SetParLimits(0,300000,9999999);
  //
  tfunc->SetParName(1,"stri");
  tfunc->SetParameter(1,80000);
  tfunc->SetParLimits(1,10000,999999);
  //
  tfunc->SetParName(2,"fconv");
  tfunc->SetParameter(2,0.03);
  tfunc->SetParLimits(2,0.0,0.1);
  //
  tfunc->SetParName(3,"fL1");
  tfunc->SetParameter(3,0.33);
  tfunc->SetParLimits(3,0.05,0.66);
  //
  tfunc->SetParName(4,"iL1");
  tfunc->SetParameter(4,0.06);
  tfunc->SetParLimits(4,0.001,0.20);

  cout<<"tfunc Eval(0) = "<<tfunc->Eval(0)<<endl;
  cout<<"tfunc Eval(1) = "<<tfunc->Eval(1)<<endl;
  cout<<"tfunc Eval(2) = "<<tfunc->Eval(2)<<endl;
  cout<<"tfunc Eval(3) = "<<tfunc->Eval(3)<<endl;
  cout<<"tfunc Eval(4) = "<<tfunc->Eval(4)<<endl;
  //    tfunc.SetParameter(0,"SigmaWAB",55555,444,0,999999)
  //    tfunc.SetParameter(1,"SigmaTRI",33333,333,0,999999)
  //   tfunc.SetParameter(2,"fconv",0.03,0.001,0,0.1)
  //    tfunc.SetParameter(3,"fL1",0.33,0.005,0,1.0)
  //    tfunc.SetParameter(4,"iL1",0.06,0.005,0,0.20)
  
  typeData->Fit(tfunc);
  
}






