//double iLumi=4577910; //mb^-1...the unblind sample run5772 (most of it)
//double iLumi=5390443; //mb^-1...the unblind sample run5772
//double iLumi=4828938; //mb^-1...the unblind sample run5772 for pass3
double iLumi=4403638.0; //mb^-1  pass 4

void overlayDifferentCuts(){
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);

  int nh1d=6;
  TString h1dnames[]={"Vx","Vy","Vz","eSum","eDiffoverESum","TridentMass"};
  int nh1dEle=6;
  TString h1dnamesEle[]={"eleMom","eled0","elez0","elephi0","eleslope","trkTimeDiff"};
  int nh1dPos=6;
  TString h1dnamesPos[]={"posMom","posd0","posz0","posphi0","posslope","vertChi2"};

  int nh1d2=6;
  TString h1dnames2[]={"tanopenY","eSumEhnHenry","NCand","minAngle","deltaPhi","deltaTheta"};

  int nh1dTopTimes=6;
  TString h1dnamesTopTimes[]={"time (ns) for layer 1 Top","time (ns) for layer 2 Top",
			      "time (ns) for layer 3 Top","time (ns) for layer 4 Top",
			      "time (ns) for layer 5 Top","time (ns) for layer 6 Top"}

  int nh1dBotTimes=6;
  TString h1dnamesBotTimes[]={"time (ns) for layer 1 Bot","time (ns) for layer 2 Bot",
			      "time (ns) for layer 3 Bot","time (ns) for layer 4 Bot",
			      "time (ns) for layer 5 Bot","time (ns) for layer 6 Bot"}

  int  nh2d=1;
  TString h2dnames[]={"ePosvseEle","coplanarity vs eSum"};
  

  //  TString labels[]={"10022015_BeamEle0pt8_ECal_GBL_v0Mom",
  //		    "10022015_BeamEle0pt8_ECal_GBL_v0Mom_slopeGT0pt2"};

  int nPlots = 27; 
  TString plotNames[]={"eSum", "TridentMass", "TridentMass", "coplanarity",
		       "minAngle","eleMom","posMom",
		       "elephi0","posphi0","eleslope","posslope","eDiffoverESum",
		       "nTrk","nEle","nPos","nClust","nCand",
		       "nTrkCand","nEleCand","nPosCand","nClustCand",
		       "trkTimeDiff","cluTimeDiff","trkCluTimeDiffEle","trkCluTimeDiffPos",
		       "raweleMom","rawposMom"};
  TString plotXAxis[]={"E(e^{+}+e^{-}) (GeV)","m(e^{+}e^{-}) (GeV)","m(e^{+}e^{-}) (GeV)","track-beam coplanarity",
		       "minAngle","trident p(e^{-}) (GeV)","trident p(e^{+}) (GeV)",
		       "phi(e^{-})","phi(e^{+})","tan#lambda(e^{-})","tan#lambda(e^{+})","E(e^{+}-e^{-})E(e^{+}+e^{-})",
		       "Number of Tracks/Event","Number of Electrons/Event",
		       "Number of Positrons/Event","Number of Clusters/Event","Number of Candidates/Event",
		       "Number of Tracks/Event With >0 Candidates","Number of Electrons/Event With >0 Candidates",
		       "Number of Positrons/Event With >0 Candidates","Number of Clusters/Event With >0 Candidates",
		       "Track Time Difference (ns)","Cluster Time Difference (ns)", "Electron Track-Cluster Time (ns)", "Positron Track-Cluster Time (ns)",
		       "all p(e^{-}) (GeV)","all p(e^{+}) (GeV)"};
  //  bool norms[]={false,false,false,false,
  //		false,false,false,
  //		false,false,false,false,false,false,false,false,false,false, 
  //		false, false,false,false, false, false,false,false,false,false};

  bool norms[]={true,false,false,false,
		false,true,true,
		false,false,false,false,false,false,false,false,false,false, 
		false, false,false,false, false, false,false,false,true,true};
  //		false, false,false,false, false, false,false,false,false,false};

  bool logy[]={false,false,false,false,
		false,false,false,
	       false,false,false,false,false,false,true,true,true,true,
	       false, false, false, false,false, false, false, false,false,false};
  //	       false,false,false,false,false,true, true,t rue, true, true,false, false, false, false};
  
  
  
  int nlabels=1;
  //  TString labels[]={"pass4_useGBL_ECalMatch_SuperFiducialCut_MoreThan2Tracks_1Positron"};
  //  TString fileLabel="pass4_useGBL_ECalMatch_SuperFiducialCut_MoreThan2Tracks_1Positron";
  //   TString labels[]={"pass4_useGBL_ECalMatch_SuperFiducialCut_2Tracks_HighESum"};
  //  TString fileLabel="pass4_useGBL_ECalMatch_SuperFiducialCut_2Tracks_HighESum";
  //  TString labels[]={"pass6_useGBL_ECalMatch_SuperFiducialCut_TestWABs"};
  // TString fileLabel="pass6_useGBL_ECalMatch_SuperFiducialCut_TestWABs";
  //  TString labels[]={"pass6_useGBL_ECalMatch_SuperFiducialCut"};
  //  TString fileLabel="pass6_useGBL_ECalMatch_SuperFiducialCut";
  TString labels[]={"pass6_useGBL_ECalMatch"};
  TString fileLabel="pass6_useGBL_ECalMatch";
  //  TString labels[]={"pass6_useGBL_ECalMatch_SuperFiducialCut_AddFakeElectrons"};
  // TString fileLabel="pass6_useGBL_ECalMatch_SuperFiducialCut_AddFakeElectrons";
 

  for(int k=0;k<nPlots;k++){
    //   (overlayDataAndTriTrig(labels,nlabels, plotNames[k],plotXAxis[k],norms[k],logy[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+".pdf");  
    (overlayDataAndBeamTri(labels,nlabels, plotNames[k],plotXAxis[k],norms[k],logy[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+"_WABBeamTri.pdf");  
    //    (overlayPulserAndBeamTri(labels,nlabels, plotNames[k],plotXAxis[k],norms[k],logy[k]))->SaveAs("SinglePlots/Pulser_"+plotNames[k]+"_"+fileLabel+".pdf");  
    //    (overlayDataAndBHRad(labels,nlabels, plotNames[k],plotXAxis[k],norms[k],logy[k]))->SaveAs("SinglePlots/"+plotNames[k]+"_"+fileLabel+"_RadBH.pdf");  
  }  
  /*  make 2d plots */
  /*
  TString plotDir = "OutputHistograms";
  TString thisLabel="pass3_useGBL";
  TString prefix="HPS-EngRun2015-Nominal-v3-1-fieldmap_3.4.1_";

  TFile* d=new TFile(plotDir+"/Data/hps_005772_"+thisLabel+".root");
  TFile*   tt=new TFile(plotDir+"/MC/tritrig_"+prefix+thisLabel+".root");   
  TFile*   rad=new TFile(plotDir+"/MC/Rad_"+prefix+thisLabel+".root");
  TFile*   bh=new TFile(plotDir+"/MC/BH_"+prefix+thisLabel+".root");
  TString xname="p(e^{-}) GeV";
  TString yname="p(e^{+}) GeV";
  //  TString hName="ePosvseEle";
  TString hName="ESumvsEDiff";
  htt=(TH2D*)tt->Get(hName);    
  ( plot2dHistogram(htt,xname,yname))->SaveAs("SinglePlots/"+hName+"_"+thisLabel+"_fullTrident.pdf");
  hd=(TH2D*)d->Get(hName);
  ( plot2dHistogram(hd,xname,yname))->SaveAs("SinglePlots/"+hName+"_"+thisLabel+"_data.pdf");
  hrad=(TH2D*)rad->Get(hName);
  ( plot2dHistogram(hrad,xname,yname))->SaveAs("SinglePlots/"+hName+"_"+thisLabel+"_radiative.pdf");
  hbh=(TH2D*)bh->Get(hName);
  ( plot2dHistogram(hbh,xname,yname))->SaveAs("SinglePlots/"+hName+"_"+thisLabel+"_bh.pdf");
  */
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
TCanvas* overlayDataAndTriTrig(TString* labels,int nlabels, TString hname,TString xname, bool normToXS, bool setLogY=false){

  //  double ttEvents=16560e3; //pass2
  //  double ttEvents=6e6;//pass3
  //  double ttEvents=9.94e6;//pass4
  /* pass-6 tritrig-beam-tri
ifarm1102> python parseAndGetEvents.py
Number Passed = 2242483.0 out of 11616968.0
Average Efficiency = 0.19303513619 from 968 jobs
  */
  double ttEvents=6.875e6;//pass6
  double ttXSGen=1.76; //mb
  /*  pass-6 tritrig-wab-beam-tri   
    ifarm1102> python parseAndGetEvents.py 
    Number Passed = 600289.0 out of 3108259.0
    Average Efficiency = 0.193127084969 from 259 jobs
  */
  double ttwEvents=1.831e6;//pass6


  TString plotDir = "OutputHistograms";
  //  TString prefix="HPS-EngRun2015-Nominal-v3-4_";
  TString prefix="HPS-EngRun2015-Nominal-v4-4_";
  TCanvas* ct=new TCanvas("ct");
  ct->SetLogy(setLogY);
  
  TFile* d;
  TFile* tt;
  TFile* ttw;

  TH1D* hd;
  TH1D* htt;
  TH1D* httw;

  TLegend* leg=new TLegend(0.65,0.8,0.9,0.9);
  for(int i=0;i<nlabels;i++){

    d=new TFile(plotDir+"/Data/hps_005772_"+labels[i]+".root");
    //Full trident diagram MC 
    //    tt=new TFile(plotDir+"/MC/tritrig_"+prefix+labels[i]+".root");   
    tt=new TFile(plotDir+"/MC/tritrig-beam-tri_"+prefix+labels[i]+".root");   
    ttw=new TFile(plotDir+"/MC/tritrig-wab-beam-tri_"+prefix+labels[i]+".root");   
    htt=(TH1D*)tt->Get(hname);    
    httw=(TH1D*)ttw->Get(hname);    
    hd=(TH1D*)d->Get(hname);
    hd->Sumw2();
    htt->Sumw2();
    httw->Sumw2();
    cout<<"Number of events:  Data = "<<hd->GetEntries()<<"; MC = "<<htt->GetEntries()<<endl;
    TString yname="#sigma (#mub)";
    if(normToXS){
      hd->Scale((1/iLumi)*1000.0);
      htt->Scale(ttXSGen/ttEvents*1000.0);
      httw->Scale(ttXSGen/ttwEvents*1000.0);
    }else{
      hd->Scale(10000.0/hd->GetEntries());
      htt->Scale(10000.0/htt->GetEntries());
      httw->Scale(10000.0/httw->GetEntries());
      yname="Arbitrary";
    }
    double max=hd->GetMaximum();
    if(htt->GetMaximum()>max)
      max=htt->GetMaximum();
    if(httw->GetMaximum()>max)
      max=httw->GetMaximum();

    double lwid=3;
    int  ltyp=i+1;
    makePretty(hd, xname,yname, 1,lwid,ltyp);
    makePretty(htt, xname,yname, 2,lwid,ltyp);
    makePretty(httw, xname,yname, 4,lwid,ltyp);

    hd->SetMaximum(1.2*max);
    if(setLogY){
      hd->SetMaximum(10*max);
      hd->SetMinimum(1);
    }
    if(i==0)
      hd->Draw("e");
    else
      hd->Draw("esame");
    
    htt->Draw("same histo");
    httw->Draw("same histo");

    //    leg->AddEntry(hd,"Data "+labels[i],"l");
    //   leg->AddEntry(htt,"Trident MC "+labels[i],"l");

    leg->AddEntry(hd,"Data ","l");
    leg->AddEntry(htt,"tritrig-beam-tri MC ","l");
    leg->AddEntry(httw,"tritrig-wab-beam-tri MC ","l");

  }  
  leg->Draw();
  return ct; 
}

/* overlay data and tritrig */
TCanvas* overlayDataAndBeamTri(TString* labels,int nlabels, TString hname,TString xname, bool normToXS, bool setLogY=false){

  //  double ttEvents=16560e3; //pass2
  //  double ttEvents=6e6;//pass3
  
  double dataNele=1.7e14/625/1000; //total charge / charge-per-bunch @ 50nA == total bunches ... x 1000 

  double btNele=45*5e5*100/1000; // total bunches beam-tri, pass 6 as of May 31, 2016  ... x 1000 
  //  double wbtNele=197*5e5/1000;  //total bunches WAB-beam-tri, pass6 as of May 31, 2016... x 1000 
  //scale wbt to the observed trigger rate
  double wbtNele=903*10*5e5/1000;  //total bunches WAB-beam-tri, pass6 as of June 15, 2016... x 1000 
  cout<<btNele<<endl;

  TString plotDir = "OutputHistograms";
  TString prefix="HPS-EngRun2015-Nominal-v4-4_";
  TCanvas* ct=new TCanvas("ct");
  ct->SetLogy(setLogY);
  
  TFile* d;
  TFile* bt;
  TFile* wbt;

  TH1D* hd;
  TH1D* hbt;
  TH1D* hwbt;

  TLegend* leg=new TLegend(0.75,0.8,0.9,0.9);
  for(int i=0;i<nlabels;i++){

    d=new TFile(plotDir+"/Data/hps_005772_"+labels[i]+".root");
    // d=new TFile(plotDir+"/Data/hps_005772_pass6_useGBL_ECalMatch_SuperFiducialCut_TestWABs.root");
    //Full trident diagram MC 
    //    tt=new TFile(plotDir+"/MC/tritrig_"+prefix+labels[i]+".root");   
    //    tt=new TFile(plotDir+"/MC/beam-tri_"+prefix+labels[i]+".root");   
    bt=new TFile(plotDir+"/MC/beam-tri_"+prefix+labels[i]+".root");   
    wbt=new TFile(plotDir+"/MC/wab-beam-tri_"+prefix+labels[i]+".root");   
    hbt=(TH1D*)bt->Get(hname);    
    hwbt=(TH1D*)wbt->Get(hname);    
    hd=(TH1D*)d->Get(hname);
    hd->Sumw2();
    hbt->Sumw2();
    hwbt->Sumw2();
    hwbt->Rebin(1);
    cout<<hname<<endl;
    cout<<"Data Mean ="<< hd->GetMean()<<";    "<<hbt->GetMean()<<endl;
    cout<<"Number of events:  Data = "<<hd->GetEntries()<<"; MC = "<<hbt->GetEntries()<<endl;
    TString yname="Per 1000 beam bunches";
    if(normToXS){
      hd->Scale(1/dataNele);
      hbt->Scale(1/btNele);
      hwbt->Scale(1/wbtNele);
    }else{
      hd->Scale(10000.0/hd->GetEntries());
      hbt->Scale(10000.0/hbt->GetEntries());
      hwbt->Scale(10000.0/hwbt->GetEntries());
      yname="Arbitrary";
   }
    //    cout<<"Integral after scaling:  Data = "<<hd->GetIntegral()<<"; MC = "<<htt->GetIntegral()<<endl;

    double max=hd->GetMaximum();
    if(hbt->GetMaximum()>max)
      max=hbt->GetMaximum();

    if(hwbt->GetMaximum()>max)
      max=hwbt->GetMaximum();

    double lwid=3;
    int  ltyp=i+1;
    makePretty(hd, xname,yname, 1,lwid,ltyp);
    makePretty(hbt, xname,yname, 2,lwid,ltyp);
    makePretty(hwbt, xname,yname, 4,lwid,ltyp);

    hd->SetMaximum(1.2*max);
    if(setLogY){
      hd->SetMaximum(10*max);
      hd->SetMinimum(1);
    }
    if(i==0)
      hd->Draw("e");
    else
      hd->Draw("esame");
    
    hbt->Draw("same histo");
    hwbt->Draw("same histo");

    //    leg->AddEntry(hd,"Data "+labels[i],"l");
    //   leg->AddEntry(htt,"Trident MC "+labels[i],"l");

    leg->AddEntry(hd,"Data ","l");
    leg->AddEntry(hbt,"Beam-Tri MC ","l");
    leg->AddEntry(hwbt,"WAB-Beam-Tri MC ","l");

  }  
  leg->Draw();
  return ct; 
}

TCanvas* overlayDataAndBHRad(TString* labels,int nlabels, TString hname,TString xname, bool normToXS, bool setLogY=false){

  
  double radEvents=4820321.0;//from parsing log files
  double radXSGen=0.120; //mb
  double BHEvents=50*5.95e4; //from parsing logfiles
  double BHXSGen=8.28;//mb
  TString plotDir = "OutputHistograms";
  TString prefix="HPS-EngRun2015-Nominal-v3-4_";
  TCanvas* ct=new TCanvas("ct");
  ct->SetLogy(setLogY);
  TFile* d;
  TFile* rad;
  TFile* bh;

  TH1D* hd;
  TH1D* hrad;
  TH1D* hbh;
  TLegend* leg=new TLegend(0.55,0.75,0.9,0.9);
  for(int i=0;i<nlabels;i++){
    d=new TFile(plotDir+"/Data/hps_005772_"+labels[i]+".root");
    rad=new TFile(plotDir+"/MC/RAD_"+prefix+labels[i]+".root");
    bh=new TFile(plotDir+"/MC/BH_"+prefix+labels[i]+".root");
    
    hd=(TH1D*)d->Get(hname);    
    hrad=(TH1D*)rad->Get(hname);
    hbh=(TH1D*)bh->Get(hname);
    hd->Sumw2();
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

    if(setLogY){
      hd->SetMaximum(10*max);
      hd->SetMinimum(1);
    }
    if(i==0)
      hd->Draw("e" );
    else
      hd->Draw("e same");

    hrad->Draw("same");
    //    hbh->Draw("same");    
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
}


/* overlay pulser data and pulser-beam-tri */
TCanvas* overlayPulserAndBeamTri(TString* labels,int nlabels, TString hname,TString xname, bool normToXS, bool setLogY=false){

  double dataNele=27059000/1000.0;
  // double btNele=1.4e12;
  double btNele=237500/1000.0; // beam-tri, pass 6 as of May 31, 2016
  double wbtNele=92500/1000.0;
  cout<<btNele<<endl;

  TString plotDir = "OutputHistograms";
  TString prefix="HPS-EngRun2015-Nominal-v4-4_";
  TCanvas* ct=new TCanvas("ct");
  ct->SetLogy(setLogY);
  
  TFile* d;
  TFile* bt;
  TFile* wbt;

  TH1D* hd;
  TH1D* hbt;
  TH1D* hwbt;

  TLegend* leg=new TLegend(0.75,0.8,0.9,0.9);
  for(int i=0;i<nlabels;i++){

    d=new TFile(plotDir+"/Data/hps_00_pulser_"+labels[i]+".root");
    //d=new TFile(plotDir+"/Data/hps_00_pulser_pass6_useGBL_ECalMatch_SuperFiducialCut.root");
    //Full trident diagram MC 
   //    tt=new TFile(plotDir+"/MC/tritrig_"+prefix+labels[i]+".root");   
    //    tt=new TFile(plotDir+"/MC/beam-tri_"+prefix+labels[i]+".root");   
    bt=new TFile(plotDir+"/MC/pulser-beam-tri_"+prefix+labels[i]+".root");   
    wbt=new TFile(plotDir+"/MC/pulser-wab-beam-tri_"+prefix+labels[i]+".root");   
    hbt=(TH1D*)bt->Get(hname);    
    hwbt=(TH1D*)wbt->Get(hname);    
    hd=(TH1D*)d->Get(hname);
    hd->Sumw2();
    hbt->Sumw2();
    hwbt->Sumw2();
    cout<<hname<<endl;
    cout<<"Data Mean ="<< hd->GetMean()<<";    "<<hbt->GetMean()<<endl;
    cout<<"Number of events:  Data = "<<hd->GetEntries()<<"; MC = "<<hbt->GetEntries()<<endl;
    //    TString yname="#sigma (#mub)";
    TString yname="Per 1000 pulser triggers";
    if(normToXS){
      hd->Scale(1/dataNele);
      hbt->Scale(1/btNele);
      hwbt->Scale(1/wbtNele);
    }else{
      hd->Scale(10000.0/hd->GetEntries());
      hbt->Scale(10000.0/hbt->GetEntries());
      hwbt->Scale(10000.0/hwbt->GetEntries());
      yname="Arbitrary";
   }
    //    cout<<"Integral after scaling:  Data = "<<hd->GetIntegral()<<"; MC = "<<htt->GetIntegral()<<endl;

    double max=hd->GetMaximum();
    if(hbt->GetMaximum()>max)
      max=hbt->GetMaximum();

    if(hwbt->GetMaximum()>max)
      max=hwbt->GetMaximum();

    double lwid=3;
    int  ltyp=i+1;
    makePretty(hd, xname,yname, 1,lwid,ltyp);
    makePretty(hbt, xname,yname, 2,lwid,ltyp);
    makePretty(hwbt, xname,yname, 4,lwid,ltyp);
    
    //    hd->SetMaximum(1.5*hd->GetMaximum());
    hd->SetMaximum(1.2*max);
    if(setLogY){
      hd->SetMaximum(10*max);
      hd->SetMinimum(1);
    }
    if(i==0)
      hd->Draw("e");
    else
      hd->Draw("esame");

    hbt->Draw("same histo");
    hwbt->Draw("same histo");

    leg->AddEntry(hd,"Data ","l");
    leg->AddEntry(hbt,"Beam-Tri MC ","l");
    leg->AddEntry(hwbt,"WAB-Beam-Tri MC ","l");

  }  
  leg->Draw();
  return ct; 
}
