#ifndef __HPSNT_H__
#define __HPSNT_H__
#include <iostream>
#include "TTree.h"
#include "TChain.h"

#ifndef MAX_NUM_CLUSTERS
#define MAX_NUM_CLUSTERS 20
#endif

struct ssp_t
{
    int trig;
    int ttl,tth;
    int nc;
    int cn[MAX_NUM_CLUSTERS];
    int ce[MAX_NUM_CLUSTERS];
    int cx[MAX_NUM_CLUSTERS];
    int cy[MAX_NUM_CLUSTERS];
    int ct[MAX_NUM_CLUSTERS];
    int ns;
    int si[MAX_NUM_CLUSTERS];
    int smin[MAX_NUM_CLUSTERS];
    int smax[MAX_NUM_CLUSTERS];
    int sn[MAX_NUM_CLUSTERS];
    int st[MAX_NUM_CLUSTERS];
    int np;
    int pi[MAX_NUM_CLUSTERS*10];
    int psum[MAX_NUM_CLUSTERS*10];
    int pdif[MAX_NUM_CLUSTERS*10];
    int pslop[MAX_NUM_CLUSTERS*10];
    int pcop[MAX_NUM_CLUSTERS*10];
    int pt[MAX_NUM_CLUSTERS*10];
    void reset()
    {
        trig=0;
        nc=ns=np=0;
        ttl=tth=-1;
    }
};
struct fadc_raw_t
{
    int adc[46][10][100];
    int pulse[46][10];
    float ped[46][10];
};
struct fadc_int_t
{
    // format 1:
    int pmt1,pmt2;
    int nhits;
    int time[442];
    int adc[442];
    int x[442];
    int y[442];

    // format 2:
    int ADC[47][10];
    int TIME[47][10];

    void reset()
    {
        pmt1=pmt2=-1;
        nhits=0;
        for (int ii=0; ii<47; ii++)
            for (int jj=0; jj<10; jj++)
                ADC[ii][jj]=TIME[ii][jj]=-1;
    }
};
struct fadc_hres_t
{
    // format 1:
    int pmt1,pmt2;
    int nhits;
    int time[3*442];
    int adc[3*442];
    int x[3*442];
    int y[3*442];
    int min[3*442];
    int max[3*442];

    // format 2:
    int ADC[47][10];
    int TIME[47][10];
    int MAX[47][10];
    int MIN[47][10];

    // either:
    float PED[46][10];
    float GAIN[46][10];

    void reset()
    {
        pmt1=pmt2=-1;
        nhits=0;
        for (int ii=0; ii<47; ii++)
            for (int jj=0; jj<10; jj++)
                ADC[ii][jj]=TIME[ii][jj]=-1;
    }
};
///////////////////////////////////////////////////////////////////////

void MakeTreeSSP(TTree *t,ssp_t &s)
{
    if (!t) { std::cerr<<"MakeTreeSSP: Missing Tree"<<std::endl; return; }
    std::cout<<"Creating TTree for SSP Data"<<std::endl;

    t->Branch("trig",&s.trig,"trig/I");

    t->Branch("ttl",&s.ttl,"ttl/I");
    t->Branch("tth",&s.tth,"tth/I");
    
    t->Branch("nc",&s.nc,"nc/I");
    t->Branch("c_n",&s.cn,"c_n[nc]/I");
    t->Branch("c_e",&s.ce,"c_e[nc]/I");
    t->Branch("c_x",&s.cx,"c_x[nc]/I");
    t->Branch("c_y",&s.cy,"c_y[nc]/I");
    t->Branch("c_t",&s.ct,"c_t[nc]/I");

    t->Branch("ns",&s.ns,"ns/I");
    t->Branch("s_i",&s.si,"s_i[ns]/I");
    t->Branch("s_min",&s.smin,"s_min[ns]/I");
    t->Branch("s_max",&s.smax,"s_max[ns]/I");
    t->Branch("s_n",&s.sn,"s_n[ns]/I");
    t->Branch("s_t",&s.st,"s_t[ns]/I");

    t->Branch("np",&s.np,"np/I");
    t->Branch("p_i",&s.pi,"p_i[np]/I");
    t->Branch("p_sum",&s.psum,"p_sum[np]/I");
    t->Branch("p_dif",&s.pdif,"p_dif[np]/I");
    t->Branch("p_slop",&s.pslop,"p_slop[np]/I");
    t->Branch("p_cop",&s.pcop,"p_cop[np]/I");
    t->Branch("p_t",&s.pt,"p_t[np]/I");
}
void MakeTreeFADC(TTree* t,fadc_int_t &t_,const int format)
{
    if (!t) { std::cerr<<"MakeTreeFADC INT: Missing Tree"<<std::endl; return; }
    std::cout<<"Creating TTree for Integral FADCs"<<std::endl;
    if (format==0 || format==1)
    {
        t->Branch("nhits",&t_.nhits,"nhits/I");
        t->Branch("pmt1",&t_.pmt1,"pmt1/I");
        t->Branch("pmt2",&t_.pmt2,"pmt2/I");
        t->Branch("time",&t_.time,"time[nhits]/I");
        t->Branch("adc",&t_.adc,"adc[nhits]/I");
        t->Branch("x",&t_.x,"x[nhits]/I");
        t->Branch("y",&t_.y,"y[nhits]/I");
    }
    if (format==0 || format==2)
    {
        t->Branch("ADC",&t_.ADC,"ADC[47][10]/I");
        t->Branch("TIME",&t_.TIME,"TIME[47][10]/I");
    }
}
void MakeTreeFADC(TTree* t,fadc_raw_t &t_)
{
    if (!t) { std::cerr<<"MakeTreeFADC RAW: Missing Tree"<<std::endl; return; }
    std::cout<<"Creating TTree for Raw FADCs"<<std::endl;
    t->Branch("adc",&t_.adc,"adc[46][10][100]/I");
    t->Branch("pulse",&t_.pulse,"pulse[46][10]/I");
    t->Branch("ped",&t_.ped,"ped[46][10]/F");
}
void MakeTreeFADC(TTree* t,fadc_hres_t &t_,const int format)
{
    if (!t) { std::cerr<<"MakeTreeFADC HRES: Missing Tree"<<std::endl; return; }
    std::cout<<"Creating TTree for HighRes FADCs"<<std::endl;
    if (format==0 || format==1)
    {
        t->Branch("nhits",&t_.nhits,"nhits/I");
        t->Branch("pmt1",&t_.pmt1,"pmt1/I");
        t->Branch("pmt2",&t_.pmt2,"pmt2/I");
        t->Branch("time",&t_.time,"time[nhits]/I");
        t->Branch("adc",&t_.adc,"adc[nhits]/I");
        t->Branch("x",&t_.x,"x[nhits]/I");
        t->Branch("y",&t_.y,"y[nhits]/I");
        t->Branch("max",&t_.max,"max[nhits]/I");
        t->Branch("min",&t_.min,"min[nhits]/I");
    }
    if (format==0 || format==2)
    {
        t->Branch("ADC",&t_.ADC,"ADC[47][10]/I");
        t->Branch("TIME",&t_.TIME,"TIME[47][10]/I");
        t->Branch("MAX",&t_.MAX,"MAX[47][10]/I");
        t->Branch("MIN",&t_.MIN,"MIN[47][10]/I");
    }
    t->Branch("PED",&t_.PED,"PED[46][10]/F");
    t->Branch("GAIN",&t_.GAIN,"GAIN[46][10]/F");
}
TTree* MakeTreeSSP(ssp_t &s_,const char* tname)
{
    TTree *t=new TTree(tname,"");
    MakeTreeSSP(t,s_);
    return t;
}
TTree* MakeTreeFADC(fadc_raw_t &t_,const char* tname)
{
    TTree *t=new TTree(tname,"");
    MakeTreeFADC(t,t_);
    return t;
}
TTree* MakeTreeFADC(fadc_int_t &t_,const char* tname,const int format)
{
    if (format<0 || format>2)
    {
        std::cerr<<"Invalid FADC TTree Format:  "<<format<<std::endl;
        return NULL;
    }
    TTree *t=new TTree(tname,"");
    MakeTreeFADC(t,t_,format);
    return t;
}
TTree* MakeTreeFADC(fadc_hres_t &t_,const char* tname,const int format)
{
    if (format<0 || format>2)
    {
        std::cerr<<"Invalid FADC TTree Format:  "<<format<<std::endl;
        return NULL;
    }
    TTree *t=new TTree(tname,"");
    MakeTreeFADC(t,t_,format);
    return t;
}

///////////////////////////////////////////////////////////////////////

void InitTreeFADC(TTree *t,fadc_raw_t &t_)
{
    if (!t) return;
    t->SetBranchAddress("adc",&t_.adc);
    t->SetBranchAddress("pulse",&t_.pulse);
    t->SetBranchAddress("ped",&t_.ped);
}
void InitTreeFADC(TTree *t,fadc_int_t &t_)
{
    if (!t) return;
    t->SetBranchAddress("pmt1",&t_.pmt1);
    t->SetBranchAddress("pmt2",&t_.pmt2);
    t->SetBranchAddress("nhits",&t_.nhits);
    t->SetBranchAddress("time",&t_.time);
    t->SetBranchAddress("adc",&t_.adc);
    t->SetBranchAddress("x",&t_.x);
    t->SetBranchAddress("y",&t_.y);
    t->SetBranchAddress("ADC",&t_.ADC);
    t->SetBranchAddress("TIME",&t_.TIME);
}
void InitTreeFADC(TTree* t,fadc_hres_t &t_,const int format)
{
    if (!t) return;
    if (format==0 || format==1)
    {
        t->SetBranchAddress("nhits",&t_.nhits);
        t->SetBranchAddress("pmt1",&t_.pmt1);
        t->SetBranchAddress("pmt2",&t_.pmt2);
        t->SetBranchAddress("time",&t_.time);
        t->SetBranchAddress("adc",&t_.adc);
        t->SetBranchAddress("x",&t_.x);
        t->SetBranchAddress("y",&t_.y);
        t->SetBranchAddress("max",&t_.max);
        t->SetBranchAddress("min",&t_.min);
    }
    if (format==0 || format==2)
    {
        t->SetBranchAddress("ADC",&t_.ADC);
        t->SetBranchAddress("TIME",&t_.TIME);
        t->SetBranchAddress("MAX",&t_.MAX);
        t->SetBranchAddress("MIN",&t_.MIN);
    }
    t->SetBranchAddress("PED",&t_.PED);
    t->SetBranchAddress("GAIN",&t_.GAIN);
}
void InitTreeSSP(TTree *t,ssp_t &s)
{
    if (!t) return;

    t->SetBranchAddress("trig",&s.trig);

    t->SetBranchAddress("ttl",&s.ttl);
    t->SetBranchAddress("tth",&s.tth);
    
    t->SetBranchAddress("nc",&s.nc);
    t->SetBranchAddress("c_n",&s.cn);
    t->SetBranchAddress("c_e",&s.ce);
    t->SetBranchAddress("c_x",&s.cx);
    t->SetBranchAddress("c_y",&s.cy);
    t->SetBranchAddress("c_t",&s.ct);

    t->SetBranchAddress("ns",&s.ns);
    t->SetBranchAddress("s_i",&s.si);
    t->SetBranchAddress("s_min",&s.smin);
    t->SetBranchAddress("s_max",&s.smax);
    t->SetBranchAddress("s_n",&s.sn);
    t->SetBranchAddress("s_t",&s.st);

    t->SetBranchAddress("np",&s.np);
    t->SetBranchAddress("p_i",&s.pi);
    t->SetBranchAddress("p_sum",&s.psum);
    t->SetBranchAddress("p_dif",&s.pdif);
    t->SetBranchAddress("p_slop",&s.pslop);
    t->SetBranchAddress("p_cop",&s.pcop);
    t->SetBranchAddress("p_t",&s.pt);
}

void ProgressMeter(const double total,const double current)
{
    static const int maxdots=40;
    const double frac = current/total;
    int ii=0;
    printf("%3.0f%% [",frac*100);
    for ( ; ii < frac*maxdots; ii++) printf("=");
    for ( ; ii < maxdots;      ii++) printf(" ");
    printf("]\r");
    fflush(stdout);
}

#include "TString.h"
#include "TRegexp.h"
int GetRunNumber(const char* filename)
{
    TString ss=filename;
    TRegexp rr="[0-9][0-9][0-9][0-9][0-9][0-9]";
    Ssiz_t ind=ss.Index(rr);
    if ((size_t)ind==std::string::npos) return -1;
    ss.Remove(0,ind+2);
    ss.Resize(4);
    return ss.Atoi();
}

#include "TH1.h"
#include "TObject.h"
#include "TDirectory.h"
void WriteRemainingHistos(const bool filledonly=0)
{
    TObject *oo;
    TIter noo(gDirectory->GetList());
    while ((oo=(TObject*)noo()))
    {
        if (!oo) continue;
        if (!oo->IsA()->InheritsFrom(TH1::Class())) continue;
        if (filledonly && ((TH1*)oo)->GetEntries()>0) continue;
        if (TString(oo->GetName()).Contains("led")) continue;
        oo->Write();
    }
}
#endif
