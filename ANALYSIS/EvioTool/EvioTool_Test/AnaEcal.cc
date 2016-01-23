#include "EvioEvent.h"
#include "EvioTool.h"
#include "AnaEcal.hh"

int main(int argc, char** argv)
{
    int itmp;
    unsigned int ii,jj,kk,ll;
    
    int NEV=-1;
    int DEBUG=0;
    bool DOPED=0;
    bool DOTREE=0;
    bool DOHIST=1;
    bool SMALLRANGE=0;
    int TRIGGER=-1;
    int FORMAT=0;
    bool DOMIPCUT=1;
    bool READFADCS=1;
    bool DOSSPTREE=1;
    TString ETFILENAME="";
    vector <TString> IFILENAMES;
    TString IFILENAME="";
    TString OFILENAME="";
    TString OTREENAME="Thps";
    int RUNNO=0;

    const char* usage="\nAnaEcal [options]\n"
                      "\t-n # events\n"
                      "\t-r ET filename\n"
                      "\t-i input EVIO filename (or filelist name)\n"
                      "\t-o output ROOT filename\n"
                      "\t-d debug level\n"
                      "\t-p do pedestal\n"
                      "\t-s small range\n"
                      "\t-H don't save histos\n"
                      "\t-t make ntuple\n"
                      "\t-M disable MIP cut\n"
                      "\t-T trigger\n"
                      "\t-f ntuple format\n"
                      "\t-F disable reading FADCs\n"
                      "\t-S disable SSP ntuple\n"
                      "\t-h print usage\n";

    while ( (itmp=getopt(argc,argv,"n:r:i:o:d:T:f:FSMhHtps")) != -1)
    {
        switch (itmp)
        {
            case 'n':
                NEV=atoi(optarg);
                break;
            case 'r':
                ETFILENAME=optarg;
                break;
            case 'i':
                IFILENAME=optarg;
                break;
            case 'o':
                OFILENAME=optarg;
                break;
            case 'd':
                DEBUG=atoi(optarg);
                break;
            case 's':
                SMALLRANGE=1;
                break;
            case 'p':
                DOPED=1;
                break;
            case 't':
                DOTREE=1;
                break;
            case 'H':
                DOHIST=0;
                break;
            case 'T':
                TRIGGER=atoi(optarg);
                break;
            case 'f':
                FORMAT=atoi(optarg);
                break;
            case 'M':
                DOMIPCUT=0;
                break;
            case 'F':
                READFADCS=0;
                break;
            case 'S':
                DOSSPTREE=0;
                break;
            case 'h':
                cout<<usage<<endl;
                exit(0);
            default:
                cout<<usage<<endl;
                exit(1);
        }
    }

    if (IFILENAME=="" || OFILENAME=="")
    {
        cerr<<"Must specify input (-i) and output (-o) files."<<endl<<usage<<endl;
        exit(1);
    }
    if (!gSystem->AccessPathName(OFILENAME))
    {
        cerr<<"Output file "<<OFILENAME<<" already exists."<<endl;
        exit(1);
    }
 
    SpecsECal ss;
    //ss.readGainsFromHolly("gainValue_8Dec.txt");

    EVIO_Event_t *evt=new EVIO_Event_t;
    EvioEventInit(evt);
    EvioTool *etool=new EvioTool();

    if (ETFILENAME!="")
    {
        etool->et_file_name=ETFILENAME;
        etool->et_port=11111;
        etool->et_host_name="localhost";
        if (etool->openEt())
        {
            cerr<<"Error opening ET ring.\n"<<endl;
            exit(1);
        }
    }
    else
    {
        if (gSystem->AccessPathName(IFILENAME))
        {
            cerr<<"Input file "<<IFILENAME<<" does not exist."<<endl;
            exit(1);
        }
        if (IFILENAME.EndsWith(".txt") || IFILENAME.EndsWith(".list"))
        {
            IFILENAMES=GetFilelist(IFILENAME.Data());
            if (IFILENAMES.size()==0)
            {
                cerr<<"No input files."<<endl;
                exit(1);
            }
            cout<<"Reading "<<IFILENAMES.size()<<" EVIO files from "<<IFILENAME<<endl;
        }
        else if (IFILENAME.EndsWith(".root"))
        {
            cerr<<"Not ready for reading ROOT file."<<endl;
            exit(1);
        }
        else 
        {
            cout<<"Reading "<<IFILENAME<<" ...."<<endl;
            RUNNO=GetRunNumber(IFILENAME.Data());
            IFILENAMES.push_back(IFILENAME);
        }
    }
    etool->fDebug=DEBUG;
    if (!READFADCS) etool->fIgnoreFADC=1;

    const int range[2]={SMALLRANGE?0:0,SMALLRANGE?30:ss.NSAMPS};
    const int nrange=range[1]-range[0]-1;

    fadc_raw_t traw_;
    fadc_int_t tint_;
    fadc_hres_t thres_;
    ssp_t tssp_;

    for (int ix=0; ix<ss.XOFFSET*2; ix++)
    {
        for (int iy=0; iy<ss.YOFFSET*2; iy++)
        {
            if (!ss.lookupXYIndex[ix][iy]) continue;
            thres_.PED[ix][iy] =ss.lookupXYIndex[ix][iy]->PED;
            thres_.GAIN[ix][iy]=ss.lookupXYIndex[ix][iy]->GAIN;
        }
    }


    TFile *ofile=new TFile(OFILENAME,"CREATE");
    TTree *otree=NULL;
    if (DOTREE && DOSSPTREE) otree=MakeTreeSSP(tssp_,OTREENAME.Data());

    TH1D *hraw[ss.NCRATS][ss.NSLOTS][ss.NCHANS];
    TH1D *hsamp[ss.NCRATS][ss.NSLOTS][ss.NCHANS];
    TH1D *hpulse[ss.NCRATS][ss.NSLOTS][ss.NCHANS];

    TH1D *hsampT=new TH1D("hsampT","",100,-0.5,99.5);
    TH2D *hpmtpmt=new TH2D("hpmtpmt","",400,0,500,400,0,500);
    TH2D *hpmtpmtI=new TH2D("hpmtpmtI","",400,9000,20000,400,13000,24000);
    
    for (int ii=0; ii<ss.NCRATS; ii++)
    {
        for (int jj=0; jj<ss.NSLOTS; jj++)
        {
            for (unsigned int kk=0; kk<ss.NCHANS; kk++)
            {
                TString stub;
                // name pmt/led channels:
                if (jj==ss.NSLOTS-1 && kk>12)
                {
                    const TString stub1=(ii==ss.NCRATS-1)?"pmt":"led";
                    stub=Form("%s%d",stub1.Data(),kk-13);
                }
                // name ecal channels crate_slot_channel
                else stub=Form("%d_%.2d_%.2d",ii+1,jj+1,kk);
                hraw[ii][jj][kk]=new TH1D(
                        Form("hraw_%s",stub.Data()),"",   500,    0,   500);
                hpulse[ii][jj][kk]=new TH1D(
                        Form("hpulse_%s",stub.Data()),"",5000, 5000, 200000);
                hsamp[ii][jj][kk]=new TH1D(
                        Form("hsamp_%s",stub.Data()),"",  100, -0.5,  99.5);
            }
        }
    }

    int nevread=0; 
    int nchanT=0;
    int nchan[ss.NCRATS][ss.NSLOTS][ss.NCHANS]={};

    bool initted=0;
    long nevfile;
    long nev2read=0;
    bool isRAWMODE=0;
    bool isINTMODE=0;
    bool isHRESMODE=0;
    
    int mode = READFADCS ? 0 : -1;

    bool NSAMPERROR=0;

///////////////////////////////////////////////////////////////

    // FILE LOOP:
    for (unsigned int ifile=0; ifile<IFILENAMES.size(); ifile++)
    {
        etool->open(IFILENAMES[ifile].Data(),nullptr);

        // EVENT LOOP:
        while (etool->read() && (nev2read<=0 || nevread<nev2read))
        {
            tint_.nhits=0;

            nevread++;

            if (nev2read>100 && nevread%(nev2read/100)==0) ProgressMeter(nev2read,nevread); 


            // load structs:
            etool->parse(evt);

            // for RAW mode, read the whole event and load these arrays:
            // (NOTE, since they're declared this way in the event loop, they are zeroed for every event)
            float fadc[ss.NCRATS][ss.NSLOTS][ss.NCHANS][ss.NSAMPS]={};
            float fadcI[ss.NCRATS][ss.NSLOTS][ss.NCHANS]={};

            if (evt->FADC_13.size() > 0) isRAWMODE=1;  // MODE-1 RAW MODE
            if (evt->FADC_15.size() > 0) isINTMODE=1;  // MODE-3 PULSE MODE
            if (evt->FADC_21.size() > 0) isHRESMODE=1; // MODE-7 HIGHRESMODE
            if (isRAWMODE+isINTMODE+isHRESMODE > 1)
            {
                std::cerr<<"Not ready for multi-mode."<<std::endl;
                exit(1);
            }
            if (DOTREE && mode==0 && READFADCS)
            {
                if (isRAWMODE)
                {
                    mode=1;
                    if (otree) MakeTreeFADC(otree,traw_);
                    else otree=MakeTreeFADC(traw_,"Tadc");
                }
                else if (isINTMODE)
                {
                    mode=3;
                    if (otree) MakeTreeFADC(otree,tint_,FORMAT);
                    else otree=MakeTreeFADC(tint_,"Tadc",0);
                }
                else if (isHRESMODE)
                {
                    mode=7;
                    if (otree) MakeTreeFADC(otree,thres_,FORMAT);
                    else otree=MakeTreeFADC(thres_,"Tadc",0);
                }
            }

            if (!initted && (isRAWMODE || isINTMODE || isHRESMODE))
            {
                initted=1;
                nevfile=GetEvioNevents(IFILENAMES) * (isRAWMODE ? 1 : 100);
                std::cout<<"Approximate # Events in EVIO File(s): "<<nevfile<<std::endl;
                nev2read = NEV<0 ? nevfile : (NEV>nevfile?nevfile:NEV);
                std::cout<<"Processing "<<nev2read<<" Events."<<std::endl;
            }

            tint_.reset();
            thres_.reset();
            tssp_.reset();

            const int trigger=evt->trigger;
            const trigger_t trigbits(evt);
            tssp_.trig=trigger;

//            std::cerr<<evt->ntrig<<" "<<evt->trig_time<<std::endl;

            FillTreeSSP(tssp_,evt);

            if (!READFADCS)
            {
                otree->Fill();
                continue;
            }

            // PULSE, SLOT LOOP:
            for (unsigned int ii=0; ii<evt->FADC_15.size(); ii++)
            {
                const FADC_data_f15_t dd = evt->FADC_15[ii];
                
                if (dd.crate != etool->ECAL_FADC_CRATE1 &&
                    dd.crate != etool->ECAL_FADC_CRATE2)
                {
                    std::cerr<<"NABOCRATE:  "<<dd.crate<<std::endl;
                    continue;
                }

                const int crat = (dd.crate==etool->ECAL_FADC_CRATE1) ? 1 : 2;
                const int slot = dd.slot;
                //const int trig = dd.trig;
                //const int time = dd.time; // what is this?

                if (TRIGGER >= 0 && trigger!=TRIGGER) continue;
                
                if (!ss.IsValidSlot(slot))
                {
                    std::cerr<<"Invalid Slot:  "<<slot<<std::endl;
                    continue;
                }
                
                // CHANNEL LOOP:
                for (unsigned int jj=0; jj<dd.data.size(); jj++)
                {
                    const FADC_chan_f15_t ddd = dd.data[jj];
                    const int chan = ddd.chan;

//                    std::cerr<<"D "<<crat<<" "<<slot<<" "<<trig<<" "<<chan<<std::endl;

                    if (ddd.time.size() != ddd.adc.size())
                    {
                        std::cerr<<"NABOMISMATCH "<<std::endl;
                        continue;
                    }

                    for (unsigned int kk=0; kk<ddd.time.size(); kk++)
                    {

                        const int adc  = ddd.adc[kk];
                        const int time = ddd.time[kk];
//                        std::cerr<<"J "<<adc<<" "<<time<<std::endl;

                        if (slot!=20 || chan<13)
                        {



                            const int ix = ss.fadc2xIndex(crat,slot,chan);
                            const int iy = ss.fadc2yIndex(crat,slot,chan);
                            const int xx = ss.fadc2x(crat,slot,chan);
                            const int yy = ss.fadc2y(crat,slot,chan);
                            const int ll=tint_.nhits;

//                            std::cerr<<"F "<<ix<<" "<<iy<<" "<<ll<<endl;

                            tint_.time[ll] = time;
                            tint_.adc[ll] = adc;
                            tint_.x[ll] = xx;
                            tint_.y[ll] = yy;
                            tint_.nhits++;
                            
                            tint_.ADC[ix][iy] = adc;
                            tint_.TIME[ix][iy] = time;

//                            std::cerr<<"Z"<<std::endl;
                        }
                        else if (crat==2 && slot==20)
                        {
                            if (chan==13) 
                            {
//                                std::cerr<<"PMT1:  "<<time<<" "<<adc<<std::endl;
                                tint_.pmt1=adc;
                                tint_.ADC[2*ss.XOFFSET][0]=adc;
                                tint_.TIME[2*ss.XOFFSET][0]=time;
                            }
                            else if (chan==14) 
                            {
//                                std::cerr<<"PMT2:  "<<time<<" "<<adc<<std::endl;
                                tint_.pmt2=adc;
                                tint_.ADC[2*ss.XOFFSET][1]=adc;
                                tint_.TIME[2*ss.XOFFSET][1]=time;
                            }
                        }
                    }
                }
            }
            // HIGHRES, SLOT LOOP:
            for (unsigned int ii=0; ii<evt->FADC_21.size(); ii++)
            {
                const FADC_data_f21_t dd = evt->FADC_21[ii];
                
                if (dd.crate != etool->ECAL_FADC_CRATE1 &&
                    dd.crate != etool->ECAL_FADC_CRATE2)
                {
                    std::cerr<<"NABOCRATE:  "<<dd.crate<<std::endl;
                    continue;
                }

                const int crat = (dd.crate==etool->ECAL_FADC_CRATE1) ? 1 : 2;
                const int slot = dd.slot;
                //const int trig = dd.trig;
                //const int time = dd.time; // what is this?

                if (TRIGGER >= 0 && trigger!=TRIGGER) continue;
                
                if (!ss.IsValidSlot(slot))
                {
                    std::cerr<<"Invalid Slot:  "<<slot<<std::endl;
                    continue;
                }
                
                // CHANNEL LOOP:
                for (unsigned int jj=0; jj<dd.data.size(); jj++)
                {
                    const FADC_chan_f21_t ddd = dd.data[jj];
                    const int chan = ddd.chan;

//                    std::cerr<<"D "<<crat<<" "<<slot<<" "<<trig<<" "<<chan<<std::endl;

                    if (ddd.time.size() != ddd.adc.size())
                    {
                        std::cerr<<"NABOMISMATCH "<<std::endl;
                        continue;
                    }

                    // PULSE LOOP:
                    for (unsigned int kk=0; kk<ddd.time.size(); kk++)
                    {
                        const int adc  = ddd.adc[kk];
                        const int time = ddd.time[kk];
                        const int min  = ddd.min[kk];
                        const int max  = ddd.max[kk];

//                        std::cerr<<"J "<<adc<<" "<<time<<std::endl;

                        if (slot!=20 || chan<13)
                        {
                            const int ix = ss.fadc2xIndex(crat,slot,chan);
                            const int iy = ss.fadc2yIndex(crat,slot,chan);
                            const int xx = ss.fadc2x(crat,slot,chan);
                            const int yy = ss.fadc2y(crat,slot,chan);
                            const int ll=thres_.nhits;

//                            std::cerr<<"F "<<ll<<" "<<dd.crate<<" "<<
//                                crat<<" "<<slot<<" "<<chan<<" ("<<ix<<","<<iy<<")=("<<xx<<","<<yy<<")"<<
//                                "adc="<<adc<<" "<<"time="<<time<<endl;

                            thres_.time[ll] = time;
                            thres_.adc[ll] = adc;
                            thres_.x[ll] = xx;
                            thres_.y[ll] = yy;
                            thres_.min[ll] = min;
                            thres_.max[ll] = max;
                            thres_.nhits++;
                            
                            thres_.ADC[ix][iy] = adc;
                            thres_.TIME[ix][iy] = time;
                            thres_.MIN[ix][iy] = min;
                            thres_.MAX[ix][iy] = min;

//                            std::cerr<<"Z"<<std::endl;
                        }
                        else if (crat==2 && slot==20)
                        {
                            if (chan==13) 
                            {
//                                std::cerr<<"PMT1:  "<<time<<" "<<adc<<std::endl;
                                tint_.pmt1=adc;
                                tint_.ADC[2*ss.XOFFSET][0]=adc;
                                tint_.TIME[2*ss.XOFFSET][0]=time;
                            }
                            else if (chan==14) 
                            {
//                                std::cerr<<"PMT2:  "<<time<<" "<<adc<<std::endl;
                                tint_.pmt2=adc;
                                tint_.ADC[2*ss.XOFFSET][1]=adc;
                                tint_.TIME[2*ss.XOFFSET][1]=time;
                            }
                        }
                    }
                }
            }

            if (!isRAWMODE) 
            {
                if (otree) otree->Fill();
                continue;
            }

            bool FOUNDECALFADCDATA=0;

            // RAW, SLOT LOOP:
            for (unsigned int ii=0; ii<evt->FADC_13.size(); ii++)
            {
                const FADC_data_f13_t dd = evt->FADC_13[ii];

                if (dd.crate != etool->ECAL_FADC_CRATE1 &&
                    dd.crate != etool->ECAL_FADC_CRATE2)
                {
                    std::cerr<<"NABOCRATE:  "<<dd.crate<<std::endl;
                    continue;
                }

                const int crate = (dd.crate==etool->ECAL_FADC_CRATE1) ? 0 : 1;
                const int slot = dd.slot-1;

                if (!ss.IsValidSlot(dd.slot)) continue; // just in case

                FOUNDECALFADCDATA=1;

                // CHANNEL LOOP:
                for (unsigned int jj=0; jj<dd.data.size(); jj++)
                {
                    const FADC_chan_f13_t ddd=dd.data[jj];
                    const int chan=ddd.chan;
                    if (!NSAMPERROR && ddd.samples.size()!=ss.NSAMPS)
                    {
                        NSAMPERROR=1;
                        std::cerr<<"NABOSAMP:  "<<ddd.samples.size()<<std::endl;
                        continue;
                    }
                    if (chan<0 || chan>15)
                    {
                        std::cerr<<"NABOCHAN:  "<<chan<<std::endl;
                        continue;
                    }
                    // LOOP OVER SAMPLES:
                    for (unsigned int samp=0; samp<ddd.samples.size(); samp++)
                    {
                            fadc[crate][slot][chan][samp]=ddd.samples[samp];
                    }
                } // END CHANNEL LOOP
            } // END SLOT LOOP

            ///////////////////////////////////////////////////////////////

            if (!FOUNDECALFADCDATA) continue;

            for (ii=0; ii<ss.NCRATS; ii++)
            {
                for (jj=0; jj<ss.NSLOTS; jj++)
                {
                    for (kk=0; kk<ss.NCHANS; kk++)
                    {
                        const int ix=ss.fadc2xIndex(ii+1,jj+1,kk);
                        const int iy=ss.fadc2yIndex(ii+1,jj+1,kk);
                        //cerr<<ii<<" "<<jj<<" "<<kk<<" "<<ix<<" "<<iy<<endl;
                        fadcI[ii][jj][kk]=0;
                        const int lmin = ss.IsECalChannel(jj+1,kk) ? range[0] : 0;
                        const int lmax = ss.IsECalChannel(jj+1,kk) ? range[1] : ss.NSAMPS;
                        //const int nsamps = lmax-lmin;
                        for (ll=0; ll<ss.NSAMPS; ll++)
                        {
//                          if (fadc[ii][jj][kk][ll]==0)
//                          {
//                            std::cerr<<ii<<" "<<jj<<" "<<kk<<" "<<std::endl;
//                          }

//                            traw_.adc[ii][jj][kk][ll] = fadc[ii][jj][kk][ll];
                            if (ix>=0 && iy>=0)
                                traw_.adc[ix][iy][ll] = fadc[ii][jj][kk][ll];
                            if (ll>=lmin && ll<lmax)
                                fadcI[ii][jj][kk] += fadc[ii][jj][kk][ll];
                        }
//                        traw_.pulse[ii][jj][kk]=fadcI[ii][jj][kk];
//                        traw_.ped[ii][jj][kk]=ss.getPedestalFADC(ii+1,jj+1,kk);
/*
                        if (ix>=0 && iy>=0)
                        {
                            traw_.pulse[ix][iy]=fadcI[ii][jj][kk];
                            traw_.ped[ix][iy]=ss.getPedestalFADC(ii+1,jj+1,kk);
                        }
*/
                    }
                }
            }


            // do these before pedestal subtraction, just because I defined cuts before:
            const int sumpmt1=fadcI[ss.NCRATS-1][ss.NSLOTS-1][ss.CHANPMT0];
            const int sumpmt2=fadcI[ss.NCRATS-1][ss.NSLOTS-1][ss.CHANPMT1];
            
//            const bool isMIP=(sumpmt1>12000 && sumpmt2>15500);
  
            const bool isMIP = sumpmt1 > 13500 && sumpmt2 > 17500;

            if ((!DOMIPCUT || isMIP) && otree) otree->Fill();

            hpmtpmtI->Fill(sumpmt1,sumpmt2);

            for (ll=0; ll<ss.NSAMPS; ll++)
                hpmtpmt->Fill(fadc[ss.NCRATS-1][ss.NSLOTS-1][13][ll],
                              fadc[ss.NCRATS-1][ss.NSLOTS-1][14][ll]);
            
            if (DOPED)
            {
                // do pedestal subtraction:
                for (ii=0; ii<ss.NCRATS; ii++)
                {
                    for (jj=0; jj<ss.NSLOTS; jj++)
                    {
                        for (kk=0; kk<ss.NCHANS; kk++)
                        {
                            const float ped=ss.getPedestalFADC(ii+1,jj+1,kk);
                            const int nsamps=ss.IsECalChannel(jj+1,kk) ? nrange : ss.NSAMPS;

                            fadcI[ii][jj][kk] -= ped*nsamps;//ss.NSAMPS;
                            
                            for (ll=0; ll<ss.NSAMPS; ll++)
                            {
                                fadc[ii][jj][kk][ll] -= ped;
                            }
                        }
                    }
                }
            }

            for (ii=0; ii<ss.NCRATS; ii++)
            {
                for (jj=0; jj<ss.NSLOTS; jj++)
                {
                    if (!ss.IsValidSlot(jj+1)) continue;
                    for (kk=0; kk<ss.NCHANS; kk++)
                    {
                        // PMT CHANNELS:
                        if ( ss.IsPmtChannel(jj+1,kk) )
                        {
                            hpulse[ii][jj][kk]->Fill(fadcI[ii][jj][kk]);
                            for (ll=0; ll<ss.NSAMPS; ll++)
                            {
                                if (!DOMIPCUT || isMIP)
                                {
                                    hraw[ii][jj][kk]->Fill(fadc[ii][jj][kk][ll]);
                                    hsamp[ii][jj][kk]->Fill(ll,fadc[ii][jj][kk][ll]);
                                }
                            }
                            if (!DOMIPCUT || isMIP)
                                nchan[ii][jj][kk]++;
                        }
                        // ECAL CHANNELS: 
                        else if (ss.IsECalChannel(jj+1,kk) && (!DOMIPCUT || isMIP) )
                        {
                            hpulse[ii][jj][kk]->Fill(fadcI[ii][jj][kk]);
                            for (ll=0; ll<ss.NSAMPS; ll++)
                            {
                                hraw[ii][jj][kk]->Fill(fadc[ii][jj][kk][ll]);
                                hsamp[ii][jj][kk]->Fill(ll,fadc[ii][jj][kk][ll]);
                                hsampT->Fill(ll,fadc[ii][jj][kk][ll]);
                            }
                            nchan[ii][jj][kk]++;
                            nchanT++;
                        }
                    }
                }
            }

        } // END EVENT LOOP
    } // END FILE LOOP


    // scale sampling histograms to get average:
    if (nchanT>0) hsampT->Scale(1./nchanT);
    for (ii=0; ii<ss.NCRATS; ii++)
        for (jj=0; jj<ss.NSLOTS; jj++)
            for (kk=0; kk<ss.NCHANS; kk++)
                if (nchan[ii][jj][kk]>0) 
                    hsamp[ii][jj][kk]->Scale(1./nchan[ii][jj][kk]);

   

///////////////////////////////////////////////////////////////
    if (DOHIST)
    {
        TDirectory *ecaldir=ofile->mkdir("ECal");
        TDirectory *rawdir=ecaldir->mkdir("RAW");
        TDirectory *intdir=ecaldir->mkdir("PULSE");
        TDirectory *sampdir=ecaldir->mkdir("SAMP");
        for (ii=0; ii<ss.NCRATS; ii++)
        {
            for (jj=0; jj<ss.NSLOTS; jj++)
            {
                for (kk=0; kk<ss.NCHANS; kk++)
                {
                    // leave last 3 channels of last slot:
                    if (jj==ss.NSLOTS-1 && kk>12) continue;

                    // put in ecaldir if in real slot on first crate:
                    //else if (ii==0 && ss.IsValidSlot(jj+1))
                    else if (ss.IsValidSlot(jj+1))
                    {
                        const float min=hsamp[ii][jj][kk]->GetMinimum();
                        const float max=hsamp[ii][jj][kk]->GetMaximum();
                        const float ddd=max-min;
                        hsamp[ii][jj][kk]->SetMinimum(min-ddd*0.3);
                        hsamp[ii][jj][kk]->SetMaximum(max+ddd*0.3);

                        hpulse[ii][jj][kk]->SetDirectory(intdir);
                        hraw[ii][jj][kk]->SetDirectory(rawdir);
                        hsamp[ii][jj][kk]->SetDirectory(sampdir);
                    }
                    // delete everything else:
                    else
                    {
                        hpulse[ii][jj][kk]->Delete();
                        hraw[ii][jj][kk]->Delete();
                        hsamp[ii][jj][kk]->Delete();
                    }
                }
            }
        }
        ecaldir->Write();
        WriteRemainingHistos();
    }

    std::cout<<std::endl;
    if (otree) 
    {
        std::cout<<"Number of Events in Ntuple:   "<<otree->GetEntries()<<std::endl;
        otree->Write();
    }
    ofile->Close();
    cout<<"Read "<<nevread<<" Events."<<endl;

}

