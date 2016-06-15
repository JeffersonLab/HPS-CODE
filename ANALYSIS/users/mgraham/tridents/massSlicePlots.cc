//double iLumi=4577910; //mb^-1...the unblind sample run5772 (most of it)
//double iLumi=5390443; //mb^-1...the unblind sample run5772
//double iLumi=4828938; //mb^-1...the unblind sample run5772 for pass3
double iLumi=4403638.0; //mb^-1
bool overlayTriTrig = false;
bool normToXS=false;
void massSlicePlots(){
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);

  /*
  int nPlots = 13; 
  TString plotNames[]={"eleMom","posMom",
		       "elePhi0","posPhi0","eleTheta","posTheta",
		       "Coplanarity", "Ediff", "V0PolarAngle", "V0Phi",
		       "vertX","vertY","vertZ"};
  TString plotXAxis[]={"p(e^{-}) (GeV)","p(e^{+}) (GeV)",
		       "phi(e^{-})","phi(e^{+})","tan#lambda(e^{-})","tan#lambda(e^{+})",
		       "Coplanarity", "E(e^{-}-e^{+}) (GeV)", "V0 Polar Angle (radians)", "V0 Phi(radians)  ",
		       "Vx (mm)", "Vy (mm)","Vz (mm)" };
  bool norms[]={false,false,false,false,
		   false,false,false,false,
		false,false,false,false,
		false,false,false};
  */

  int nPlots = 1; 
  TString plotNames[]={"vertZ"};
  TString plotXAxis[]={"Vz (mm)" };
  bool norms[]={false};
  
  int nlabels=10;
  TString labels[10];
  for(int i=1;i<nlabels+1;i++){
    labels[i-1]="Mass Slice ";labels[i-1]+=i;
  }
  //TString fileLabel="pass4_killTracks";
  
  int flabels=2;
  TString fileLabels[]={"pass4_IsoCut_1pt0_v0chi2_10_useGBL", "pass4_IsoCut_1pt0_v0chi2_10"}
  TString outputPlotLabel = "compare_GBL";
  
  //  TString outputPlotLabel = "pass4_IsoCut_1pt0_v0chi2_10_useGBL";

  /*
    TString labels[]={"pass3_matchECal"};
    int nlabels=1;
    TString fileLabel="pass3_matchECal";
  */
  for(int i=0;i<nlabels;i++){
    for(int k=0;k<nPlots;k++){
      (overlayDataAndTriTrig(labels[i], flabels,fileLabels,plotNames[k],plotXAxis[k],norms[k]))->SaveAs("VertexPlots/"+plotNames[k]+"_"+labels[i]+outputPlotLabel+".pdf");  
      //    (overlayDataAndBHRad(labels,nlabels, plotNames[k],plotXAxis[k],norms[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+"-Slices_RadBH.pdf");  
    }  
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
TCanvas* overlayDataAndTriTrig(TString label,int nflabels, TString* fileLabels,  TString hname,TString xname, bool scale){

  //  double ttEvents=16560e3; //pass2
  double ttEvents=6e6;//pass3
  double ttXSGen=1.76; //mb
  TString plotDir = "VertexHistograms";
  TString prefix="HPS-EngRun2015-Nominal-v3-4_";
  //  TString postfix="pass4_killTracks";
  //  TString postfix="pass4";
  TCanvas* ct=new TCanvas("ct");
  ct->SetLogy();

  TFile* d;
  TFile* tt;

  TH1D* hd;
  TH1D* htt;

  TLegend* leg=new TLegend(0.65,0.75,0.9,0.9);
  double max=-9999;

  for(int i=0;i<nflabels;i++){
    cout<<fileLabels[i]<<endl;
    d=new TFile(plotDir+"/Data/hps_005772_"+fileLabels[i]+".root");
    //Full trident diagram MC 
    tt=new TFile(plotDir+"/MC/tritrig-beam-tri_"+prefix+fileLabels[i]+".root");   
    TString tmpName=hname;
    tmpName+="  ";
    tmpName+=label;
    cout<<tmpName<<endl;
    htt=(TH1D*)tt->Get(tmpName);    
    hd=(TH1D*)d->Get(tmpName);
    cout<<"got here"<<endl;
    TString yname="#sigma (#mub)";
    if(scale && normToXS){
      hd->Scale((1/iLumi)*1000.0);
      htt->Scale(ttXSGen/ttEvents*1000.0);
    }else if (scale) {
      cout<<"Scaling to same area"<<endl;
      cout<<hd->GetEntries()<<endl;
      hd->Scale(10000.0/hd->GetEntries());
      htt->Scale(10000.0/htt->GetEntries());
      yname="Arbitrary";
    } else {
      cout<<"Not Scaling"<<endl;
      yname="Events";
    }
    cout<<"and here..."<<endl;

    int  hdmax=hd->GetMaximum();
    if(hdmax>max){
      max=hdmax;
    }      
    if(overlayTriTrig && htt->GetMaximum()>max)
      max=htt->GetMaximum();
    
    double lwid=3;
    int  ltyp=i+1;
    makePretty(hd, xname,yname, 1,lwid,ltyp);
    if(overlayTriTrig)
      makePretty(htt, xname,yname, 2,lwid,ltyp);

    cout<<"Made them pretty"<<endl;
    
    hd->SetMaximum(1.2*max);
    if(i==0)
      hd->Draw();
    else
      hd->Draw("same");
    
    if(overlayTriTrig)
      htt->Draw("same");

    leg->AddEntry(hd,"Data "+fileLabels[i],"l");
    if (overlayTriTrig)
      leg->AddEntry(htt,"Trident MC "+fileLabels[i],"l");
    cout<<"Done!"<<endl;
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
 h->SetMinimum(0.0001);
}

