//////////////////////////////////////////////////////////
double GausPoly(double *x,double *p)
{
  return p[0]*TMath::Gaus(x[0],p[1],p[2],0);//+p[3]*x[0]*x[0]*TMath::Exp(p[4]*x[0])+p[5];
  //return (0.5*p[0]*p[1]/TMath::Pi()) / TMath::Max(1.e-10,(x[0]-p[2])*(x[0]-p[2])+ .25*p[1]*p[1]) +p[3]*x[0]*x[0]*TMath::Exp(p[4]*x[0])+p[5]*x[0]+p[6];
}

TF1 *GausPoly(const float xlo,const float xhi)
{
    const int npar=3;
    static int ncalls=0;
    TF1 *f=new TF1(Form("fGausPoly_%d",ncalls++),GausPoly,xlo,xhi,npar);
    f->SetParName(0,"Integral");
    f->SetParName(1,"Mean");
    f->SetParName(2,"Sigma");
    
    return f;
}


TF1* test(TH1* h)
{
  //Look for peak
  //h->GetXaxis()->SetRange(0.7,1.0);

  // choose good initial parameters:
  float Par1 =  h->GetBinCenter(h->GetMaximumBin());
  float lowEnd, highEnd;
  //h->GetXaxis()->SetRange(0.45,1.3);


  lowEnd = Par1-0.04; //0.4*h->GetRMS();//Par1-0.5*h->GetRMS();
  highEnd = Par1+0.1;//0.9*h->GetRMS();//Par1+2*h->GetRMS();
  
  //Fit Range:
  TF1 *f;  
  
  f=GausPoly(lowEnd,highEnd);
  
  f->SetParameter(0,h->GetMaximum()); // integral (bin width?)
  f->SetParameter(1,Par1); // mean peak

  if (h->GetRMS()>0.1){
    f->SetParameter(2,h->GetRMS()/2); // sigma
    f->SetParLimits(2,0.03,h->GetRMS());
  }
  else{
    f->SetParameter(2,h->GetRMS()/3); // sigma
    //f->SetParLimits(2,0.03,0.06);
  }
  
  f->SetParLimits(1,lowEnd,highEnd);
  

  return f;
}

float findMaximum(TF1* f1, TH1F* h){
  //Look for peak
  h->GetXaxis()->SetRange(0.7,1.0);
  
  // choose good initial parameters:
  float Par1 =  h->GetBinCenter(h->GetMaximumBin());
  float lowEnd, highEnd;

  lowEnd = Par1-0.5*h->GetRMS();
  highEnd = Par1+2*h->GetRMS();

  float maxPeak = f1->GetMaximum(Par1-0.4*h->GetRMS(),Par1+1.9*h->GetRMS());

  return maxPeak;

}
