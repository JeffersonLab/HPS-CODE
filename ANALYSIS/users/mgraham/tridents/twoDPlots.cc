//double iLumi=4577910; //mb^-1...the unblind sample run5772 (most of it)
//double iLumi=5390443; //mb^-1...the unblind sample run5772
//double iLumi=4828938; //mb^-1...the unblind sample run5772 for pass3
double iLumi=4403638.0; //mb^-1
bool normToXS=false;
bool triFull=true;
bool killTracks=false;
TFile* tttruth;
TFile* d;

void twoDPlots(){

  //  double ttEvents=16560e3; //pass2 
  double ttEvents=6e6; //pass3
  //  double ttbtEvents=8.77e4;//pass3 
  double ttbtEvents=9.94e6;
  double ttXSGen=1.76; //mb
  
  double radEvents=3e6;
  double radXSGen=0.120; //mb
  double BHEvents=5e6;
  double BHXSGen=8.28;//mb

  //  TString prefix="HPS-EngRun2015-Nominal-v3-1-fieldmap_3.4.1_";
  //  TString prefix="FIXEDJAR_tritrig-egsv3-triv2-g4v1_HPS-EngRun2015-Nominal-v3-4-fieldmap_3.5_";
  TString prefix="HPS-EngRun2015-Nominal-v3-4_";

  //  TString label="pass3_nominal";
  TString label="pass4_useGBL_ECalMatch_SuperFiducialCut";
  //TString label="pass4_killTracks";
  //  TString label="10022015_BeamEle0pt8";
  //TString label="10022015_BHCut0pt8";
  //  TString label="10022015_RadCut0pt8";

  TString plotDir = "OutputHistograms";
  d=new TFile(plotDir+"/Data/hps_005772_"+label+".root");
  
  tttruth=new TFile(plotDir+"/Truth/tritrigv1_truth.root");
  if(killTracks)
    label+="_killTracks_0pt5";
  //Full trident diagram MC 
  TFile* tt=new TFile(plotDir+"/MC/tritrig_"+prefix+label+".root");
  TFile* ttbt=new TFile(plotDir+"/MC/tritrig-beam-tri_"+prefix+label+".root");
  
  TFile* rad=new TFile(plotDir+"/MC/RAD_"+prefix+label+".root");
  TFile* bh=new TFile(plotDir+"/MC/BH_"+prefix+label+".root");
  

  int  nh2d=12;
  TString h2dnames[]={"EclXEclYEle"    , "EclXEclYPos"   , "eVsPhiEle"     , "eVsPhiPos"     , "EclEPtrkEle", "EclEPtrkPos",
		      "EclTimePtrkEle",  "EclTimePtrkPos", "TrkTimePtrkEle",  "TrkTimePtrkPos",
		      "TrkTimeEclTimeEle","TrkTimeEclTimePos" };
  TString h2dXnames[]={"Cluster X (mm)", "Cluster X (mm)", "Momentum (GeV)", "Momentum (GeV)", "Momentum (GeV)", "Momentum (GeV)", 
		       "Momentum (GeV)","Momentum (GeV)", "Momentum (GeV)","Momentum (GeV)",
		       "Cluster Time (ns)", "Cluster Time (ns)"}; 
  TString h2dYnames[]={"Cluster Y (mm)", "Cluster Y (mm)", "phi (radians)" , "phi (radians)" , "Cluster Energy (GeV)","Cluster Energy (GeV)",
		       "Cluster Time (ns)",   "Cluster Time (ns)", "Track Time (ns)","Track Time (ns)",
		       "Track Time (ns)","Track Time (ns)"}; 
  

  plot2DStuff(ttbt, nh2d,h2dnames,h2dXnames,h2dYnames,"tritrig-beam-tri-"+label);
  plot2DStuff(rad, nh2d,h2dnames,h2dXnames,h2dYnames,"rad-"+label);
  plot2DStuff(bh, nh2d,h2dnames,h2dXnames,h2dYnames,"bh-"+label);
  plot2DStuff(d, nh2d,h2dnames,h2dXnames,h2dYnames,"run5772-"+label);

}


void plot2DStuff(TFile* tt, int nplots, TString* names, TString* xnames, TString* ynames, TString outname){
  
    TCanvas* ct=new TCanvas("ct");
    //    ct->Divide(3,2);
    for(int i=0;i<nplots;i++){
      cout<<"Doing "<<names[i]<<endl;
      TH1D* htt=(TH1D*)tt->Get(names[i]);
      /*
	if(normToXS){
	htt->Scale(ttXSGen/ttEvents);
	}else{
	htt->Scale(10000.0/htt->GetEntries());
	}
      */
      htt->SetXTitle(xnames[i]);
      htt->SetYTitle(ynames[i]);
      htt->Draw("colz");
      ct->SaveAs("twoDPlots/"+outname+names[i]+".pdf");
    }    
}

void ratioPlot(TFile* ttbt,  double ttbtEvents, double ttbtXSGen, TString plotName, TString outname, bool sumThem=false){
  TCanvas* ct=new TCanvas("ct");
  gStyle->SetOptStat(0);
  cout<<"Doing "<<plotName<<endl;
  TH1* hd=(TH1*)d->Get(plotName);
  TH1* httbt=(TH1*)ttbt->Get(plotName);
  hd->Sumw2();
  httbt->Sumw2();
  if(normToXS){
    hd->Scale(1/iLumi);
    httbt->Scale(ttbtXSGen/ttbtEvents);
  }else{
    hd->Scale(10000.0/hd->GetEntries());
    httbt->Scale(10000.0/httbt->GetEntries());
  }

  TH1* ratio=hd->Clone();
  ratio->Divide(httbt);
  ratio->SetMaximum(3);
  ratio->Draw("colz");//what does colz do for 1d plots? 
  if(normToXS)
    ct->SaveAs("RatioPlots/"+outname+"-norm-to-XS.pdf");
  else
    ct->SaveAs("RatioPlots/"+outname+"-norm-to-total-area.pdf");


}
