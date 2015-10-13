//double iLumi=4577910; //mb^-1...the unblind sample run5772 (most of it)
double iLumi=5390443; //mb^-1...the unblind sample run5772
bool normToXS=false;
bool triFull=false;

TFile* d;

void overlayPlots(){

  double ttEvents=16560e3;
  double ttbtEvents=8.77e4;
  double ttXSGen=1.76; //mb
  
  double radEvents=3e6;
  double radXSGen=0.120; //mb
  double BHEvents=5e6;
  double BHXSGen=8.28;//mb

  //  TString label="10022015_RequireClusters";
  
  TString label="10022015_BeamEle0pt8_ECal_GBL";
  //  TString label="10022015_BeamEle0pt8";
  //TString label="10022015_BHCut0pt8";
  //  TString label="10022015_RadCut0pt8";

  TString plotDir = "OutputHistograms";
  d=new TFile(plotDir+"/Data/hps_005772_"+label+".root");
  //Full trident diagram MC 
  TFile* tt=new TFile(plotDir+"/MC/tritrig_HPS-EngRun2015-Nominal-v3_"+label+".root");
  TFile* ttbt=new TFile(plotDir+"/MC/tritrig-beam-tri_HPS-EngRun2015-Nominal-v3_"+label+".root");
  
  TFile* rad=new TFile(plotDir+"/MC/Rad_HPS-EngRun2015-Nominal-v3_"+label+".root");
  TFile* bh=new TFile(plotDir+"/MC/BH_HPS-EngRun2015-Nominal-v3_"+label+".root");
  

  int nh1d=6;
  TString h1dnames[]={"Vx","Vy","Vz","eSum","eDiffoverESum","TridentMass"};
  int nh1dEle=6;
  TString h1dnamesEle[]={"eleMom","eled0","elez0","elephi0","eleslope","trkTimeDiff"};
  int nh1dPos=6;
  TString h1dnamesPos[]={"posMom","posd0","posz0","posphi0","posslope","vertChi2"};

  int nh1d2=4;
  TString h1dnames2[]={"tanopenY","tanopenYThresh","NCand","minAngle"};


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
    //cout<<"Integrals for "<<names[i]<<endl;
    //cout<<hd->Integral()<<endl;
    //cout<<htt->Integral()<<endl;
    //cout<<httbt->Integral()<<endl;
    if(normToXS&&sumThem){
      httbt->Add(htt,1);
    }      
    double max=httbt->GetMaximum();
    if(htt->GetMaximum()>max)
      max=htt->GetMaximum();
    if(hd->GetMaximum()>max)
      max=hd->GetMaximum();

    htt->SetMaximum(max*1.2);
    htt->Draw();
    hd->Draw("same");
    httbt->Draw("same");
      
  }

  if(normToXS)
    ct->SaveAs("SummaryPlots/"+outname+"-norm-to-XS.pdf");
  else
    ct->SaveAs("SummaryPlots/"+outname+"-norm-to-total-area.pdf");


  }
