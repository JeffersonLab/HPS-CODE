#include "util/utilities.h"
#include <map>
#include <string>
#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TApplication.h"

#include "RooRealVar.h"

#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooPolyVar.h"
#include "RooHistPdf.h"
#include "RooPolynomial.h"
#include "RooAddPdf.h"
#include "RooPlot.h"


TApplication gui("GUI",0,NULL);

using namespace std;
using namespace RooFit;

map<int,TFile*> data; //run_number -> TFile
map<int,map<int,TH1D*>> hdata; //run_number --> map<id,TH1D*>

map<int,double> mdata; //clusterID --> ratio

//as in hps-java
double xmin=0.5;
double xmax=6.;
double nx=200;

int runMIN=14000;
int runMAX=15000;



int runZERO=14316;
int runPRE=14369;
int runPOST=14575;

//x is -23..23
//y is -5..5
int getClusterID(int x,int y){
   int ix=calcX(x);
   int iy=calcY(y);
   int id=xy2dbid(ix,iy);
   int ret=id;
   if (x<=-20) ret=-1; 
   else if (x<=-18) ret=-2;
   else if (x==-17) ret=-3;
   else if (x>=20) ret=-4;
   else if (x>=18) ret=-5;
   else if (x==17) ret=-6;
   else if (x==16) ret=-7;
   else if (x==15) ret=-8;
   return ret;
}

//fit hDataPre to hDataPost using a scale factor for X axis
double fitHist(TH1D *hDataPre,TH1D *hDataPost){
  double s0=1;
  RooRealVar E("E","E",xmin*s0,xmax*s0);
  RooDataHist data("data","data",E,hDataPost);

  RooRealVar E2("E2","E2",0,500);
  RooDataHist histdata("histdata","histdata",E2,hDataPre);

  RooRealVar scale("scale","scale",s0,0,1.2);
  RooRealVar p0("p0","p0",0.);
  RooPolyVar Ef("Ef","Ef",E,RooArgSet(p0,scale));
   
  RooHistPdf histpdf("histpdf","histpdf",Ef,E2,histdata,2);

  RooPolynomial pol0("pol0","pol0",Ef,RooArgList());
  RooRealVar f0("f0","f0",1.,0.8,1.0);
      
  RooAddPdf model("model","model",RooArgList(histpdf,pol0),RooArgList(f0));
      
  
  model.fitTo(data);
  s0=scale.getValV();
  return 1./s0;
  
}

//x is -23..23 in the input map
//y is -5..5 in the input map
map<int,TH1D*> clusterHistos(map<pair<int,int>,TH1D*> data,string f){
  map<int,TH1D*> ret;

  //create clustered histograms and sum
  for (int ix=0;ix<46;ix++){
    for (int iy=0;iy<10;iy++){
      if (ishole(ix,iy)) continue;
      int xx=calcIX(ix);
      int yy=calcIY(iy);
      int clusterID=getClusterID(xx,yy);
      if (ret.find(clusterID)==ret.end()){
	ret[clusterID]=new TH1D(Form("%3d_%s",clusterID,f.c_str()),Form("%3d",clusterID),nx,xmin,xmax);
      }
      ret[clusterID]->Add(data[std::make_pair(xx,yy)]);
    }
  }
  
  return ret;
}


TH2D* plotRatio(map<int,TH1D*> clusPre,map<int,TH1D*> clusPos){
  
  static int isFirst=1;
  mdata.clear();
  TH2D *hR=new TH2D("hR","hR",47,-23.5,23.5,11,-5.5,5.5);
 
  for (int ix=0;ix<46;ix++){
    for (int iy=0;iy<10;iy++){
      if (ishole(ix,iy)) continue;
      int xx=calcIX(ix);
      int yy=calcIY(iy);
      int clusterID=getClusterID(xx,yy);
      if (mdata.find(clusterID)!=mdata.end()){
	hR->Fill(xx,yy,100*mdata[clusterID]);
	continue;
      }
      
      TH1D *hPre=clusPre[clusterID];
      TH1D *hPost=clusPos[clusterID];

      double peakPre,peakPost,ratio;

      peakPre=hPre->GetBinCenter(hPre->GetMaximumBin());
      peakPost=hPost->GetBinCenter(hPost->GetMaximumBin());


      double s0=1.;
      RooRealVar Q("Q","Q",xmin*s0,xmax*s0);
      RooDataHist data("data","data",Q,hPost);
      
      RooRealVar E("E","E",0,10);
      RooDataHist histdata("histdata","histdata",E,hPre);
      
      RooRealVar scale("scale","scale",s0,0.5,1.1);
      RooRealVar p0("p0","p0",0.);
      RooPolyVar Qf("Qf","Qf",Q,RooArgSet(p0,scale));
      
      RooHistPdf histpdf("histpdf","histpdf",Qf,E,histdata,4);
      
      RooPolynomial pol0("pol0","pol0",Qf,RooArgList());
      RooRealVar f0("f0","f0",1.,0.8,1.0);
      
      RooAddPdf model("model","model",RooArgList(histpdf,pol0),RooArgList(f0));
      
      model.fitTo(data);
      s0=scale.getValV();
      s0=1./s0;
      mdata[clusterID]=s0;
      
      
      TCanvas *c=new TCanvas("c","c");
      c->Divide(1,2);
      c->cd(1);
      hPost->SetLineColor(2);
      hPost->Draw("HIST");
      hPre->Scale(hPost->Integral()/hPre->Integral());
      hPre->Draw("HISTSAME");
      c->cd(2);
      RooPlot* frame = Q.frame();
      data.plotOn(frame,MarkerColor(kRed));
      histpdf.plotOn(frame);
      model.plotOn(frame);
      frame->Draw();
      if (isFirst){
	c->Print(Form("fits.pdf("));
	isFirst=0;
      }else{
	c->Print(Form("fits.pdf"));
      }
      
      if (s0>0){
	hR->Fill(xx,yy,100*s0);
      }
    }
  }
  return hR;
}

//sum all the histos in the range, return a map:
//(x,y) --> h
//x is -23..23
//y is -5..5
map<pair<int,int>,TH1D*> sumData(int runMin,int runMax){

  map<pair<int,int>,TH1D*> retData;
  for (int ix=0;ix<46;ix++){
    for (int iy=0;iy<10;iy++){
      if (ishole(ix,iy)) continue;
      int xx=calcIX(ix);
      int yy=calcIY(iy);
      int id=xy2dbid(ix,iy);

      std::pair<int,int> mkey=std::make_pair(xx,yy);
      retData[mkey]=new TH1D(Form("%3d_%i_%i",id,runMin,runMax),Form("%3d_%i_%i",id,runMin,runMax),nx,xmin,xmax);

      map<int,TFile*>::iterator data_it;
      for (data_it=data.begin();data_it!=data.end();data_it++){
	int mrun=(*data_it).first;
	if ((mrun>=runMin)&&(mrun<=runMax)){
	  TFile* mfile=(*data_it).second;
	  TH1D* h=(TH1D*)mfile->Get(Form("%3d_seed",id));
	  retData[mkey]->Add(h);
	}
      }
    }
  }
  return retData;
}

//x is -23..23
//y is -5..5
TGraph *stripChart(int xx,int yy){

  int ix=calcX(xx);
  int iy=calcY(yy);
  int id=xy2dbid(ix,iy);
  int counter=0;
  
  map<int,TFile*>::iterator data_it;
  TGraph *g=new TGraph();
  for (data_it=data.begin();data_it!=data.end();data_it++){
    int mrun=(*data_it).first;
    cout<<mrun<<endl;
    TFile* mfile=(*data_it).second;
    TH1D* h=(TH1D*)mfile->Get(Form("%3d",id));
    double peak=h->GetBinCenter(h->GetMaximumBin());
    if (h->GetEntries()>500){
      h->Fit("gaus","R","",peak-0.05,peak+0.2);
      peak=h->GetFunction("gaus")->GetParameter(1);
      g->SetPoint(counter++,mrun,peak);
    }
  }
  return g;
}


TGraph *stripChartFit(int xx,int yy){ 


  int ix=calcX(xx);
  int iy=calcY(yy);
  int id=xy2dbid(ix,iy);
  int counter=0;
  map<int,TFile*>::iterator data_it;
  TGraph *g=new TGraph();
  for (data_it=data.begin();data_it!=data.end();data_it++){
    int mrun=(*data_it).first;
    TFile* mfile=(*data_it).second;
    TH1D* h=(TH1D*)mfile->Get(Form("%3d",id));
  
    if (h==0) continue;
    double peak=h->GetBinCenter(h->GetMaximumBin());
   
   
    if (h->GetEntries()>1000){
      TF1 *lfit=CBFit(h);
      h->Fit(lfit,"0QR");
      peak=lfit->GetParameter(2);
     
      if ((peak>2)&&(peak<5)){
	g->SetPoint(counter++,mrun,peak);
      }
      
    }
  }
  return g;
}

TGraphErrors *stripChartFit2(int xx,int yy){ 
  int ix=calcX(xx);
  int iy=calcY(yy);
  int id=xy2dbid(ix,iy);
  int counter=0;
  map<int,map<int,TH1D*>>::iterator data_it;
  TGraphErrors *g=new TGraphErrors();
  for (data_it=hdata.begin();data_it!=hdata.end();data_it++){
    
    int mrun=(*data_it).first;
    map<int,TH1D*> dataTmp=(*data_it).second;
    
 
    TH1D* h=dataTmp[id];
  
    if (h==0) continue;
    double peak=h->GetBinCenter(h->GetMaximumBin());
    double epeak=0;
   
    if (h->GetEntries()>1000){
      TF1 *lfit=CBFit(h);
      h->Fit(lfit,"QR");
      peak=lfit->GetParameter(2);
      epeak=lfit->GetParError(2);
      if ((peak>2)&&(peak<5)&&(fabs(epeak/peak)<.3)){
	g->SetPoint(counter,mrun,peak);
	g->SetPointError(counter++,0,epeak);
      }
      
    }
  }
  return g;
}







void readData(){
  for (int iRun=14000;iRun<15000;iRun++){
    string fName=string(Form("input_iter2/%d.2.root",iRun));
    ifstream f(fName.c_str());
    cout<<"TEST: "<<iRun<<endl;
    if (f.good()){
      f.close();
      cout<<"LOAD: "<<iRun<<endl;
      data[iRun]=new TFile(fName.c_str());
    }
  }
}

void clusterData(int Nmerge=10){

  int iRun=14000;
  int iRunFirst,iRunLast;
  int xx,yy,id;
  
  while(iRun<=15000){
    map<int,TH1D*> dataTmp;
    int ii=0;
   
    while (ii<Nmerge){

      //is the data there? If not, increment iRun, and continue
      if(iRun>=runMAX) return;
      if (data.find(iRun) == data.end()) {
	cout<<iRun<<" not exists "<<ii<<endl;
	iRun++;
	continue;
      }
      if (ii==0){
	iRunFirst=iRun;
      }

      
      cout<<iRun<<" exists :"<<ii<<endl;
      //If it is, read the file
      TFile *mfile=data[iRun];

      //loop on all crystals
      for (int ix=0;ix<46;ix++){
	for (int iy=0;iy<10;iy++){
	  if (ishole(ix,iy)) continue;
	  xx=calcIX(ix);
	  yy=calcIY(iy);
	  id=xy2dbid(ix,iy);
	  if (ii==0){
	    dataTmp[id]=(TH1D*)mfile->Get(Form("%3d",id));
	  }
	  else{
	    dataTmp[id]->Add((TH1D*)mfile->Get(Form("%3d",id)));	
	  }
	}
      }
      iRunLast=iRun;
      ii++;
      iRun++;
    }
    // cout<<iRunFirst<<" "<<iRunLast<<" "<<endl;cin.get();
    hdata[(iRunFirst+iRunLast)/2]=dataTmp;
  }
}


void closeData(){
   map<int,TFile*>::iterator data_it;
   for (data_it=data.begin();data_it!=data.end();data_it++){
     TFile* mfile=(*data_it).second;
     mfile->Close();
     delete mfile;
   }
}

double getSlope(double ratio){

  double ret=0;
  double deltaPre=runPRE-runZERO;
  double deltaPost=runPOST-runZERO;

  ret=(1-ratio)/(ratio*deltaPre-deltaPost);
  return ret;
}


int main(){

  //gROOT->SetBatch();
  readData();
  clusterData(1);

  map<pair<int,int>,TH1D*> dataPre;
  map<pair<int,int>,TH1D*> dataPost;

  dataPre=sumData(runPRE-50,runPRE+50);
  dataPost=sumData(runPOST-50,runPOST+50);

  map<int,TH1D*> dataPreClus;
  map<int,TH1D*> dataPostClus;

  dataPreClus=clusterHistos(dataPre,"PRE");
  dataPostClus=clusterHistos(dataPost,"POST");
  

  TH2D *hR=plotRatio(dataPreClus,dataPostClus);
 
  TCanvas *c=new TCanvas("c","c");
  TFile *fout=new TFile("runs.root","recreate");
  int xx=-1;int yy=1;

  int ix=calcX(xx);
  int iy=calcY(yy);
  int id=xy2dbid(ix,iy);

  cout<<xx<<" "<<yy<<" "<<ix<<" "<<iy<<" "<<id<<endl;

  std::map<int,TGraphErrors*> datas;
  
  //c->Print("runs.pdf(");
  for (int ix=0;ix<46;ix++){
    for (int iy=0;iy<10;iy++){
      if (ishole(ix,iy)) continue;
      xx=calcIX(ix);
      yy=calcIY(iy);
      id=xy2dbid(ix,iy);
      cout<<"StripFit "<<xx<<" "<<yy<<endl;
      TGraphErrors *g1=stripChartFit2(xx,yy);
      g1->SetName(Form("%i__%i_%i",id,xx,yy));
      cout<<xx<<" "<<yy<<" "<<g1->GetN()<<endl;
      if (g1->GetN()>5){
	g1->SetMarkerStyle(20);
	g1->GetXaxis()->SetRangeUser(1150,1700);
	g1->Draw("AP");
	g1->SetTitle(Form("%i_%i_%i",id,xx,yy));
	fout->cd();
	datas[id]=g1;
	//c->Print("runs.pdf");
      }
    }
  }
  fout->cd();
  std::map<int,TGraphErrors*>::iterator itG;
  for (itG=datas.begin();itG!=datas.end();itG++){
    itG->second->Write();
  }

  /* std::map<int,map<int,TH1D*>>::iterator it;
  for (it=hdata.begin();it!=hdata.end();it++){
    int runn=it->first;
    std::map<int,TH1D*> mapTmp=it->second;
    std::map<int,TH1D*>::iterator it2;
    for (it2=mapTmp.begin();it2!=mapTmp.end();it2++){
      int id=it2->first;
      TH1D *hh=(TH1D*)it2->second;
      cout<<"WRITE: "<<id<<" "<<runn<<endl;
      hh->SetName(Form("%i__%i",id,runn));
      hh->Write();
    }
    }*/
  cout<<"WRITE DONE "<<endl;




  
  //c->Print("runs.pdf)");
  // fout->Write();
  // fout->Close();
  
  
  xx=-13;
  yy=2;
 
  /*TGraph *g2=stripChart(xx,yy); 
  g2->SetMarkerStyle(20);
  g2->SetMarkerColor(2);
  g2->Draw("AP");
  gui.Run(1);*/
  //TH1D *hPre=dataPreClus[getClusterID(-8,-3)];
  //TH1D *hPost=dataPostClus[getClusterID(-8,-3)];

  
  //hPre->Draw("HIST");
  //hPost->Draw("HISTSAMES");
  //g1->Draw("AP");
  //g2->Draw("PSAME");


  //xmin=hPost->GetBinCenter(hPost->GetMaximumBin())-0.2;
  //xmax=hPost->GetBinCenter(hPost->GetMaximumBin())+1.;

  ofstream ofile("slopes.new.dat");
  ofile<<"#COMMENT DO NOT TOUCH. ID and SLOPE"<<endl;
  for (int ix=0;ix<46;ix++){
    for (int iy=0;iy<10;iy++){
      if (ishole(ix,iy)) continue;
      int xx=calcIX(ix);
      int yy=calcIY(iy);
      int id=xy2dbid(ix,iy);
      int cluster=getClusterID(xx,yy);
      double slope=getSlope(mdata[cluster]);
      ofile<<id<<","<<slope<<endl;
    }
  }
  

  TCanvas *c2=new TCanvas("c2","c2");
  hR->Draw("colz");  
  hR->SetMaximum(105);
  hR->SetMinimum(85);
  c2->Modified();
  c2->Update();
  c2->Print("fits.pdf)");
  gui.Run(1);
  
  closeData();
}








