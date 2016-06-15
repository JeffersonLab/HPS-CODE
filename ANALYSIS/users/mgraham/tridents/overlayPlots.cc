//double iLumi=4577910; //mb^-1...the unblind sample run5772 (most of it)
//double iLumi=5390443; //mb^-1...the unblind sample run5772
//double iLumi=4828938; //mb^-1...the unblind sample run5772 for pass3
double iLumi=4403638.0; //mb^-1
bool normToXS=false;
bool triFull=true;
bool killTracks=false;
TFile* tttruth;
TFile* d;

void overlayPlots(){

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
  TString label="pass4_useGBL_ECalMatch";
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
  
  //  TFile* rad=new TFile(plotDir+"/MC/RAD_"+prefix+label+".root");
  //TFile* bh=new TFile(plotDir+"/MC/BH_"+prefix+label+".root");
  

  int nh1d=6;
  TString h1dnames[]={"Vx","Vy","Vz","eSum","eDiffoverESum","TridentMass"};
  int nh1dEle=6;
  TString h1dnamesEle[]={"eleMom","eled0","elez0","elephi0","eleslope","trkTimeDiff"};
  int nh1dPos=6;
  TString h1dnamesPos[]={"posMom","posd0","posz0","posphi0","posslope","vertChi2"};

  int nh1d2=3;
  //  TString h1dnames2[]={"openAngle","eSumEhnHenry","NCand","minAngle","deltaTheta","deltaPhi"};
  TString h1dnames2[]={"openAngle","deltaTheta","deltaPhi"};


  int nh1dTopTimes=6;
  TString h1dnamesTopTimes[]={"time (ns) for layer 1 Top","time (ns) for layer 2 Top",
			      "time (ns) for layer 3 Top","time (ns) for layer 4 Top",
			      "time (ns) for layer 5 Top","time (ns) for layer 6 Top"}


  int nh1dBotTimes=6;
  TString h1dnamesBotTimes[]={"time (ns) for layer 1 Bot","time (ns) for layer 2 Bot",
			      "time (ns) for layer 3 Bot","time (ns) for layer 4 Bot",
			      "time (ns) for layer 5 Bot","time (ns) for layer 6 Bot"}

  int  nh2d=1;
  TString h2dnames[]={"ePosvseEle"};
  
  if(triFull){
    plotStuff(tt,ttbt, ttEvents, ttXSGen, ttbtEvents, ttXSGen, nh1d,h1dnames,"v0summary-FullTri"+label);
    plotStuff(tt,ttbt, ttEvents, ttXSGen, ttbtEvents, ttXSGen,nh1d2,h1dnames2,"v0summary2-FullTri"+label);
    plotStuff(tt,ttbt, ttEvents, ttXSGen, ttbtEvents, ttXSGen,nh1dPos,h1dnamesPos,"positrons-FullTri"+label);
    plotStuff(tt,ttbt, ttEvents, ttXSGen, ttbtEvents, ttXSGen,nh1dEle,h1dnamesEle,"electrons-FullTri"+label);
    ratioPlot(ttbt, ttbtEvents, ttXSGen, "eVsSlopeEle","eVsSlopeEle-DataMC-Ratio"+label);
    ratioPlot(ttbt, ttbtEvents, ttXSGen, "eVsSlopePos","eVsSlopePos-DataMC-Ratio"+label);
    ratioPlot(ttbt, ttbtEvents, ttXSGen, "eVsPhiEle","eVsPhiEle-DataMC-Ratio"+label);
    ratioPlot(ttbt, ttbtEvents, ttXSGen, "eVsPhiPos","eVsPhiPos-DataMC-Ratio"+label);
  }  else{				
    plotStuff(rad,bh, radEvents,radXSGen, BHEvents, BHXSGen, nh1d,h1dnames,"v0summary-radBH"+label,true);
    plotStuff(rad,bh, radEvents,radXSGen, BHEvents, BHXSGen,nh1d2,h1dnames2,"v0summary2-radBH"+label,true);
    plotStuff(rad,bh, radEvents,radXSGen, BHEvents, BHXSGen,nh1dPos,h1dnamesPos,"positrons-radBH"+label,true);
    plotStuff(rad,bh, radEvents,radXSGen, BHEvents, BHXSGen,nh1dEle,h1dnamesEle,"electrons-radBH"+label,true);
  }
}


void plotStuff(TFile* tt, TFile* ttbt, double ttEvents, double ttXSGen, double ttbtEvents, double ttbtXSGen, int nplots, TString* names, TString outname, bool sumThem=false){
  
    TCanvas* ct=new TCanvas("ct");
    ct->Divide(3,2);
    TH1D* htttruth;
    for(int i=0;i<nplots;i++){
      cout<<"Doing "<<names[i]<<endl;
      ct->cd(i+1);
      TH1D* hd=(TH1D*)d->Get(names[i]);
      TH1D* htt=(TH1D*)tt->Get(names[i]);
      TH1D* httbt=(TH1D*)ttbt->Get(names[i]);
      if(normToXS){
	hd->Scale(1/iLumi);
	//	htt->Scale(ttXSGen/ttEvents);
	httbt->Scale(ttbtXSGen/ttbtEvents);
      }else{
	htttruth= (TH1D*) tttruth->Get(names[i]);
	hd->Scale(10000.0/hd->GetEntries());
	//	htt->Scale(10000.0/htt->GetEntries());
	httbt->Scale(10000.0/httbt->GetEntries());
	if(htttruth != NULL) {
	  htttruth->Scale(10000.0/htttruth->GetEntries());
	  htttruth->SetLineColor(2);
	}
      }
      hd->SetLineColor(1);
      //      htt->SetLineColor(2);
      httbt->SetLineColor(4);
      if(i==0){
	cout<<"Integrals for "<<names[i]<<endl;
	cout<<hd->Integral()*1000.0<<endl;
	//	cout<<htt->Integral()*1000.0<<endl;
	cout<<httbt->Integral()*1000.0<<endl;
      }
      if(normToXS&&sumThem){
	httbt->Add(htt,1);
      }      
     
      double max=httbt->GetMaximum();
      //      if(htt->GetMaximum()>max)
      //max=htt->GetMaximum();
      if(hd->GetMaximum()>max)
	max=hd->GetMaximum();
      
      //      htt->SetMaximum(max*1.2);
      // htt->Draw();
      httbt->SetMaximum(max*1.2);
       httbt->Draw();
      hd->Draw("same");
      //      if(!normToXS && htttruth != NULL)
      // 	htttruth->Draw("same");
      //      httbt->Draw("same");
      
    }
    
    if(normToXS)
      ct->SaveAs("SummaryPlots/"+outname+"-norm-to-XS.pdf");
    else
      ct->SaveAs("SummaryPlots/"+outname+"-norm-to-total-area.pdf");
    
    
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
