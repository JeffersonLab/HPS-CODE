//double iLumi=4577910; //mb^-1...the unblind sample run5772 (most of it)
//double iLumi=5390443; //mb^-1...the unblind sample run5772
//double iLumi=4828938; //mb^-1...the unblind sample run5772 for pass3
double iLumi=4403638.0; //mb^-1

void overlaySlices(){
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);

  int nPlots = 10; 
  TString plotNames[]={"eleMom","posMom",
		       "elePhi0","posPhi0","eleTheta","posTheta",
		       "Coplanarity", "Ediff", "V0PolarAngle", "V0Phi"};
  TString plotXAxis[]={"p(e^{-}) (GeV)","p(e^{+}) (GeV)",
		       "phi(e^{-})","phi(e^{+})","tan#lambda(e^{-})","tan#lambda(e^{+})",
		       "Coplanarity", "E(e^{-}-e^{+}) (GeV)", "V0 Polar Angle", "V0 Phi"};
  //  bool norms[]={false,false,false,false,
  //	   false,false,false,false,
  //		   false,false,false,false};

  bool norms[]={true,true,true,true,
		true,true,true,true,
		true,true,true,true};

  
  
  TString labels[]={"  ESum Slice 1","  ESum Slice 5"};
  int nlabels=2;
  //TString fileLabel="pass4_killTracks";
  TString fileLabel="pass4_useGBL";
  

  /*
    TString labels[]={"pass3_matchECal"};
    int nlabels=1;
    TString fileLabel="pass3_matchECal";
  */
  for(int k=0;k<nPlots;k++){
    //    (overlayDataAndTriTrig(labels,nlabels, plotNames[k],plotXAxis[k],norms[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+"-Slices.pdf");  
    (overlayDataAndTriTrig(labels,nlabels, plotNames[k],plotXAxis[k],norms[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+"-Slices-NormToXS.pdf");  
    //    (overlayDataAndBHRad(labels,nlabels, plotNames[k],plotXAxis[k],norms[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+"-Slices_RadBH.pdf");  
  }  
  
}

/* plot 2d histogram */
TCanvas* plot2dHistogram(TH2D* hist, TString xname, TString yname){
  TCanvas* ct=new TCanvas("ct");
  hist->SetXTitle(xname);
  hist->SetYTitle(yname);
  hist->Draw("colz");
  return ct;
}

/* overlay data and tritrig */
TCanvas* overlayDataAndTriTrig(TString* labels,int nlabels, TString hname,TString xname, bool normToXS){

  //  double ttEvents=16560e3; //pass2
  double ttEvents=9.94e6;//pass4
  double ttXSGen=1.76; //mb
  TString plotDir = "OutputHistograms";
  TString prefix="HPS-EngRun2015-Nominal-v3-4_";
  //  TString postfix="pass4_killTracks";
  TString postfix="pass4_useGBL";
  TCanvas* ct=new TCanvas("ct");

  TFile* d;
  TFile* tt;
  TFile* tttruth;

  TH1D* hd;
  TH1D* htt;
  TH1D* htruth;
  TLegend* leg=new TLegend(0.65,0.75,0.9,0.9);
  d=new TFile(plotDir+"/Data/hps_005772_"+postfix+".root");
  //Full trident diagram MC 
  //    tt=new TFile(plotDir+"/MC/tritrig_"+prefix+labels[i]+".root");   
  tt=new TFile(plotDir+"/MC/tritrig-beam-tri_"+prefix+postfix+".root");   
  tttruth=new TFile(plotDir+"/Truth/tritrigv1_truth.root");

  for(int i=0;i<nlabels;i++){
    TString tmpName=hname;
    tmpName+=labels[i];
    cout<<tmpName<<endl;
    htruth=(TH1D*)tttruth->Get(tmpName);    
    htt=(TH1D*)tt->Get(tmpName);    
    hd=(TH1D*)d->Get(tmpName);
    cout<<"got here"<<endl;
    TString yname="#sigma (#mub)";
    if(normToXS){
      hd->Scale((1/iLumi)*1000.0);
      htt->Scale(ttXSGen/ttEvents*1000.0);
    }else{
      cout<<"Scaling to same area"<<endl;
      cout<<hd->GetEntries()<<endl;
      hd->Scale(10000.0/hd->GetEntries());
      htt->Scale(10000.0/htt->GetEntries());
      htruth->Scale(10000.0/htruth->GetEntries());
      
      yname="Arbitrary";
    }
    cout<<"and here..."<<endl;
    double max=hd->GetMaximum();
    if(htt->GetMaximum()>max)
      max=htt->GetMaximum();
    if(!normToXS && htruth !=NULL && htruth->GetMaximum()>max)
      max=htruth->GetMaximum();
    
    double lwid=3;
    int  ltyp=i+1;
    makePretty(hd, xname,yname, 1,lwid,ltyp);
    makePretty(htt, xname,yname, 2,lwid,ltyp);
    if(!normToXS && htruth != NULL)
      makePretty(htruth, xname,yname, 4,lwid,ltyp);

    cout<<"Made them pretty"<<endl;
    hd->SetMaximum(1.2*max);
    if(i==0)
      hd->Draw();
    else
      hd->Draw("same");
    
    htt->Draw("same");

    leg->AddEntry(hd,"Data "+labels[i],"l");
    leg->AddEntry(htt,"Trident MC "+labels[i],"l");
    if(!normToXS && htruth !=NULL){
      htruth->Draw("same");    
      leg->AddEntry(htruth,"Trident Truth "+labels[i],"l");
    }
    cout<<"Done!"<<endl;
  }  
  leg->Draw();
  return ct; 
}

/*
 *  this has not been modified for slices yet (still takes different files)
 */
TCanvas* overlayDataAndBHRad(TString* labels,int nlabels, TString hname,TString xname, bool normToXS){

  
  double radEvents=4820321.0;//from parsing log files
  double radXSGen=0.120; //mb
  double BHEvents=50*5.95e4; //from parsing logfiles
  double BHXSGen=8.28;//mb
  TString plotDir = "OutputHistograms";
  TString prefix="HPS-EngRun2015-Nominal-v3-4_";
  TString postfix="pass4";

  TCanvas* ct=new TCanvas("ct");

  TFile* d;
  TFile* rad;
  TFile* bh;

  TH1D* hd;
  TH1D* hrad;
  TH1D* hbh;

  d=new TFile(plotDir+"/Data/hps_005772_"+postfix+".root");
  rad=new TFile(plotDir+"/MC/RAD_"+prefix+postfix+".root");
  bh=new TFile(plotDir+"/MC/BH_"+prefix+postfix+".root");
  
  TLegend* leg=new TLegend(0.55,0.75,0.9,0.9);
  for(int i=0;i<nlabels;i++){
    TString tmpName=hname;
    tmpName+=labels[i];
    cout<<tmpName<<endl;    
    hd=(TH1D*)d->Get(tmpName);    
    hrad=(TH1D*)rad->Get(tmpName);
    hbh=(TH1D*)bh->Get(tmpName);
    TString yname="#sigma (#mub)";
    if(normToXS){
      hd->Scale((1/iLumi)*1000.0);
      hrad->Scale(radXSGen/radEvents*1000.0);
      hbh->Scale(BHXSGen/BHEvents*1000.0);
     
    }else{
      hd->Scale(10000.0/hd->GetEntries());
      hrad->Scale(10000.0/hrad->GetEntries());
      hbh->Scale(10000.0/hbh->GetEntries());
      yname="Arbitrary";
    }
    
    if(normToXS){
      hbh->Add(hrad,1);
    }      

    double max=hd->GetMaximum();
    if(hrad->GetMaximum()>max)
      max=hrad->GetMaximum();
    if(hbh->GetMaximum()>max)
      max=hbh->GetMaximum();

    double lwid=3;
    int  ltyp=i+1;
    makePretty(hd, xname,yname, 1,lwid,ltyp);
    makePretty(hrad, xname,yname, 4,lwid,ltyp);
    makePretty(hbh, xname,yname, 2,lwid,ltyp);

    hd->SetMaximum(1.2*max);
    if(i==0)
      hd->Draw();
    else
      hd->Draw("same");

    hrad->Draw("same");
    hbh->Draw("same");    
    leg->AddEntry(hd,"Data "+labels[i],"l");
    leg->AddEntry(hrad,"Radiative MC "+labels[i],"l");
    if(normToXS){
      leg->AddEntry(hbh,"BH+Rad MC "+labels[i],"l");
    }else{
      leg->AddEntry(hbh,"BH MC "+labels[i],"l");
    }         
  }  
  leg->Draw();
  return ct; 
}


  void makePretty(TH1D* h, TString xname, TString yname, int color, double lwid, int ltype=1){
 h->SetLineColor(color);
 h->SetLineWidth(lwid);
 h->SetLineStyle(ltype);
 h->SetXTitle(xname);
 h->SetYTitle(yname);
 h->SetMinimum(0.0);
}

void plotStuff(TFile* tt, TFile* ttbt, double ttEvents, double ttXSGen, double ttbtEvents, double ttbtXSGen, int nplots, TString* names, TString outname, bool sumThem=false){
  
    TCanvas* ct=new TCanvas("ct");
    ct->Divide(3,2);
    for(int i=0;i<nplots;i++){
      ct->cd(i+1);
      TH1D* hd=(TH1D*)d->Get(names[i]);
      TH1D* htt=(TH1D*)tt->Get(names[i]);
      TH1D* httbt=(TH1D*)ttbt->Get(names[i]);
      if(normToXS){
	hd->Scale(1/iLumi);
	htt->Scale(ttXSGen/ttEvents);
	httbt->Scale(ttbtXSGen/ttbtEvents);
      }else{
	hd->Scale(10000.0/hd->GetEntries());
	htt->Scale(10000.0/htt->GetEntries());
	httbt->Scale(10000.0/httbt->GetEntries());
      }
      hd->SetLineColor(1);
      htt->SetLineColor(2);
      httbt->SetLineColor(4);
      if(i==0){
	cout<<"Integrals for "<<names[i]<<endl;
	cout<<hd->Integral()*1000.0<<endl;
	cout<<htt->Integral()*1000.0<<endl;
	cout<<httbt->Integral()*1000.0<<endl;
      }
      if(normToXS&&sumThem){
	httbt->Add(htt,1);
      }      
     
      double max=httbt->GetMaximum();
      if(htt->GetMaximum()>max)
	max=htt->GetMaximum();
      if(hd->GetMaximum()>max)
	max=hd->GetMaximum();

      htt->SetMinimum(0.0);
      hd->SetMinimum(0.0);
      httbt->SetMinimum(0.0);
      
      htt->SetMaximum(max*1.2);
      htt->Draw();
      hd->Draw("same");
      httbt->Draw("same");
      
    }
    
    if(normToXS)
      ct->SaveAs("SummaryPlots/"+outname+"Slices--norm-to-XS.pdf");
    else
      ct->SaveAs("SummaryPlots/"+outname+"Slices-norm-to-total-area.pdf");
    

  }
