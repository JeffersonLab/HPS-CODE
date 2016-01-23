
#include "TPad.h"
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TSystem.h"
//#include "TStopwatch.h"
#include "TDirectory.h"

#include "EvioTool/EvioEvent.h"
#include "EvioTool/EvioTool.h"
using namespace std;

#define NCRATS 2
#define NSLOTS 20
#define NCHANS 16
#define NSAMPS 100

struct fadc_t
{
    int crate,slot,chan,samp[100];
};

void Time_it(const char* eviofilename,const int nev=-1)
{

    //gSystem->Load("build/Release/libEvioTool.so");

    gSystem->Load("SpecsECal_hh.so");
    gSystem->Load("lib/Darwin-x86_64/libEvioTool.so");

    gSystem->Load("AutoDict_vector_FADC_data_f13_t__cxx.so");
    gSystem->Load("AutoDict_vector_FADC_chan_f13_t__cxx.so");
    //gSystem->Load("AutoDict_vector_TBox___cxx.so");


    EVIO_Event_t *evt=new EVIO_Event_t;
    EvioTool *ev=new EvioTool(eviofilename);
    ev->fDebug=0; //100;
    int i=0;

    //SpecsECal specs("./ecalwiring.csv");

    if (!gSystem->AccessPathName("f.root"))
    {
        std::cerr<<"f.root already exists."<<std::endl;
        return;
    }

    TFile *f=new TFile("f.root","CREATE");
    TH1D *hraw[NCRATS][NSLOTS][NCHANS];
    TH1D *hint[NCRATS][NSLOTS][NCHANS];
    TH1D *hsamp[NCRATS][NSLOTS][NCHANS];
    TH1D *hsampT=new TH1D("hsampT","",100,-0.5,99.5);
    TH2D *hpmtpmt=new TH2D("hpmtpmt","",400,0,500,400,0,500);
    TH2D *hpmtpmtI=new TH2D("hpmtpmtI","",400,9000,20000,400,13000,24000);

/*
    TTree *t=new TTree("Tfadc","");
    t->Branch("crate",&t_.crate);
    t->Branch("slot",&t_.slot);
    t->Branch("chan",&t_.chan);
    t->Branch("samp",&t_.samp,"samp[100]/I");
*/
    for (unsigned int ii=0; ii<NCRATS; ii++)
    {
        for (unsigned int jj=0; jj<NSLOTS; jj++)
        {
            for (unsigned int kk=0; kk<NCHANS; kk++)
            {
                TString stub;
                // name pmt/led channels:
                if (jj==NSLOTS-1 && kk>12)
                {
                    const TString stub1=(ii==NCRATS-1)?"pmt":"led";
                    stub=Form("%s%d",stub1.Data(),kk-13);
                }
                // name ecal channels crate_slot_channel
                else stub=Form("%d_%.2d_%.2d",ii+1,jj+1,kk);
                hraw[ii][jj][kk]=new TH1D(
                        Form("hraw_%s",stub.Data()),"",    500,    0,   500);
                hint[ii][jj][kk]=new TH1D(
                        Form("hint_%s",stub.Data()),"",   1000, 5000, 20000);
                hsamp[ii][jj][kk]=new TH1D(
                        Form("hsamp_%s",stub.Data()),"",   100, -0.5,  99.5);
            }
        }
    }
    
    int nchanT=0;
    int nchan[2][NSLOTS][NCHANS]={};

    while(ev->read() && (nev<0 || i<nev))
    {
        i++;
        //ProgressMeter(i++,nev);

        ev->parse(evt);

        int sumpmt1=0,sumpmt2=0;
        int pmt1[100]={},pmt2[100]={};

        for (unsigned int ii=0; ii<evt->FADC_13.size(); ii++)
        {
            const FADC_data_f13_t dd = evt->FADC_13[ii];

            if (dd.crate != ev->ECAL_FADC_CRATE1 &&
                dd.crate != ev->ECAL_FADC_CRATE2)
            {
                std::cerr<<"WTFCRATE:  "<<dd.crate<<std::endl;
                continue;
            }

            const int crate = (dd.crate==ev->ECAL_FADC_CRATE1) ? 0 : 1;
            const int slot = dd.slot-1;

            // ignore invalid slots:
            if (slot<3 || slot>20) continue;
            if (slot>9 && slot<14) continue;

            for (unsigned int jj=0; jj<dd.data.size(); jj++)
            {
                const FADC_chan_f13_t ff=dd.data[jj];
                const int chan=ff.chan;

                if (ff.samples.size()!=NSAMPS)
                {
                    std::cerr<<"WTFSAMP:  "<<ff.samples.size()<<std::endl;
                    continue;
                }
                if (chan<0 || chan>15)
                {
                    std::cerr<<"WTFCHAN:  "<<chan<<std::endl;
                    continue;
                }

//                t_.crate=crate;
//                t_.slot=slot;
//                t_.chan=chan;

                int pulseint=0;

                nchanT++;
                nchan[crate][slot][chan]++;

                for (unsigned int samp=0; samp<ff.samples.size(); samp++)
                {
//                    t_.samp[samp]=ff.samples[samp];
                    const int adc=ff.samples[samp];

                    pulseint += adc;
                    
                    hraw[crate][slot][chan]->Fill(adc);
                    hsamp[crate][slot][chan]->Fill(samp,adc);
                    
                    // NON-ECAL CHANNELS:
                    if (slot==NSLOTS-1 && chan>12)
                    {
                        // COSMIC PMTs:
                        if (crate==1)
                        {
                            if      (chan==13) pmt1[samp]=adc;
                            else if (chan==14) pmt2[samp]=adc;
                        }
                    }
                    // ECAL CHANNELS:
                    else
                    {
                        hsampT->Fill(samp,adc);
                    }

                }

                // pulse histo:
                hint[crate][slot][chan]->Fill(pulseint);

                // COSMIC PMT ONLY:
                if (crate==NCRATS-1 && slot==NSLOTS-1)
                {
                    if      (chan==13) sumpmt1=pulseint;
                    else if (chan==14) sumpmt2=pulseint;
                }

            }
        }

        hpmtpmtI->Fill(sumpmt1,sumpmt2);
        for (unsigned int ii=0; ii<NSAMPS; ii++)
            hpmtpmt->Fill(pmt1[ii],pmt2[ii]);

    }
  
    // scale sampling histograms to get average:
    if (nchanT>0) hsampT->Scale(1./nchanT);
    for (unsigned int ii=0; ii<NCRATS; ii++)
        for (unsigned int jj=0; jj<NSLOTS; jj++)
            for (unsigned int kk=0; kk<NCHANS; kk++)
                if (nchan[ii][jj][kk]>0) 
                    hsamp[ii][jj][kk]->Scale(1./nchan[ii][jj][kk]);


    for (unsigned int ii=0; ii<NCRATS; ii++)
    {
        const int crate=ii+1;
        for (unsigned int jj=0; jj<NSLOTS; jj++)
        {
            const int slot=jj+1;
            for (unsigned int kk=0; kk<NCHANS; kk++)
            {
                // some slots are not used:
                if (slot<3 || slot>20) continue;
                if (slot>9 && slot<14) continue;

                // only save PMT channels on 2nd crate:
                if (crate==1 || (slot==20 && (kk==13 || kk==14)))
                {
                    hint[ii][jj][kk]->Write();
                    hraw[ii][jj][kk]->Write();
                    hsamp[ii][jj][kk]->Write();
                }
                
            }
        }
    }
    hsampT->Write();
    hpmtpmt->Write();
    hpmtpmtI->Write();

/*
    TObject *oo;
    TIter noo(gDirectory->GetList());
    while ((oo=(TObject*)noo()))
    {
        if (oo->IsA()->InheritsFrom(TH1::Class()))
            if (((TH1*)oo)->GetEntries()>0)
                oo->Write();
    }
*/
    f->Close();
}
void view()
{
//    TFile *file=new TFile("f.root","READ");
    for (unsigned int ii=1; ii<2; ii++)
    {
        for (unsigned int jj=0; jj<=NSLOTS; jj++)
        {
            for (unsigned int kk=0; kk<NCHANS; kk++)
            {
                const TString hname=Form("hsamp_%d_%.2d_%.2d",ii,jj,kk);
                cerr<<hname<<endl;
                //TH1 *z=(TH1*)file->Get(hname);
                TH1 *z=(TH1*)gDirectory->Get(hname);
                if (!z) continue;

                z->Scale(1/.20);

                float min=z->GetMinimum();
                float max=z->GetMaximum();
                const float ddd=max-min;
                min -= ddd*0.3;
                max += ddd*0.3;
                z->SetMinimum(min);
                z->SetMaximum(max);
                z->Draw();
                gPad->Update();
                getchar();
            }
        }
    }
}
