#ifndef SPECSECAL__hh
#define SPECSECAL__hh
#include <iostream>
#include "TH2.h"
#include "TBox.h"
#include "TPad.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TString.h"
#include "TSystem.h"
#include "CanvasPartition.C"
struct ECalChannel
{
    int JOUT,CHAN,HV,LEDCHAN,APD,LEDCRATE;
    int FADCSLOT,FADCCHAN,FADCCRATE;
    int SPLITTER,PREAMP,X,Y,DBID;
    float LEDDRIVER,PED,PEDRMS,GAIN;
    float LEDDELAY,LEDAMPHI,LEDAMPLO,TOFFSET;
    TString MB;
    int XINDEX,YINDEX;
    void print()
    {
        printf( "%3d "
                "%3d %2d "
                "%3d %3d "
                "%3d %2.1f "
                "%1d %2d %2d %2d "
                "%2d %2d %2s %3d"
                "%9.2f %5.1f %3.1f"
                "%6.1f %6.1f %6.1f"
                "%6.1f"
                "\n",
                DBID,
                X,Y,
                APD,PREAMP,
                LEDCHAN,LEDDRIVER,
                FADCCRATE,FADCSLOT,FADCCHAN,SPLITTER,
                HV,JOUT,MB.Data(),CHAN,
                GAIN,PED,PEDRMS,
                LEDDELAY,LEDAMPHI,LEDAMPLO,
                TOFFSET
              );
    }
    ECalChannel()
    {
        JOUT=CHAN=HV=LEDCHAN=APD=LEDCRATE=0;
        FADCSLOT=FADCCHAN=FADCCRATE=0;
        SPLITTER=PREAMP=X=Y=0;
        LEDDRIVER=PED=PEDRMS=0;
        LEDAMPHI=1201.;
        LEDAMPLO=1200.;
        LEDDELAY=TOFFSET=0;
        GAIN=0.227;
        DBID=-1;
        MB="--";
        XINDEX=YINDEX=-1;
    }
};


// USER INTERFACE DEFINED ACCORDING TO HARDWARE NUMBERS:
// CRATE = 1-2
// SLOT  = 1-20
// CHAN  = 0-15

class SpecsECal 
{
    private:
        TH2* hview;
        TCanvas *cview;
        TCanvas *canny[4];
        std::vector <TPad*>paddy[4];
        TBox *boxes[442];
        bool loadMap(const char* dir);
        void loadLookups();
        void SetDBID();
        void makeHist();
        void makeBoxes();
        void makeCanny();

    public:
        std::vector <ECalChannel> chans;
        //std::vector <ECalChannel> *chans;
        ECalChannel* lookupFADC[2][20][16];
        ECalChannel* lookupXY[100][100];
        ECalChannel* lookupXYIndex[46][10];
        ECalChannel* lookupLED[2][300];
        ECalChannel* lookupChan[4][300];
        ECalChannel* lookupDBID[442];
        
        static const int NCRATS=2;
        static const int NSLOTS=20;
        static const int NCHANS=16;
        static const int NSAMPS=100;
        static const int CHANPMT0=13;
        static const int CHANPMT1=14;
        static const int NECALCHANS=442;
        static const int XOFFSET=23;
        static const int YOFFSET=5;
        static const int COSMICWIDTH=22; // # of samples

        SpecsECal();
    
        void print();
        void printXY();   // ordered by y/x
        void printChan(); // ordered by signal channel

        void led2xy(const int,const int);
        void led2fadc(const int,const int);
        int led2fadcslot(const int,const int);
        int led2fadcchan(const int,const int);

        FILE *OpenOutFile(const char* ofilename);
        void WriteDB_ecal_calibrations(const char*);
        void WriteDB_ecal_channels(const char*);
        void WriteDB_ecal_leds(const char*);
        void WriteDB_ecal_gains(const char*);
        void WriteDB_ecal_time_shifts(const char*);
        void WriteDB_bad_channels(const char*);

        bool IsValidSlot(const int);
        bool IsValidChannel(const int,const int);
        bool IsValidChannel(const int,const int,const int);
        bool IsValidXY(const int,const int);
        bool IsValidXYIndex(const int,const int);

        bool IsECalChannel(const int,const int);
        bool IsPmtChannel(const int,const int);

        int fadc2y(const int,const int,const int);
        int fadc2x(const int,const int,const int);
        int fadc2yIndex(const int,const int,const int);
        int fadc2xIndex(const int,const int,const int);
        int x2xIndex(const int);
        int y2yIndex(const int);

        float getPedestalFADC(const int,const int,const int);
        float getPedestalXY(const int,const int);
        float getGainXY(const int,const int);
       
        int xy2led(const int,const int);
        int xy2fadcslot(const int,const int);
        int xy2fadcchan(const int,const int);
        int xy2jout(const int xx,const int yy);
        int xy2hv(const int xx,const int yy);

        inline float adc2gev(const float adc){return 2.1 * 3/2 * adc/4095;};

        std::vector <ECalChannel*> getHV(const char*,const int);
        std::vector <ECalChannel*> getJOUT(const char*,const int);

        inline TH2* getHist(){return hview;}
        TCanvas* getCanvas();
        void drawCanvas();
        void drawChannels();
        void drawJOUT(const char*,const int,const int);
        void drawHV(const char*,const int,const int);
        
        void setRoughGains();
        void printGainsForDAQ(const int crate,const char*);
        void printPedsForDAQ(const int,const char*);
        
        bool loadPedestals(const char* dir=".");
        bool readGainsFromHolly(const char*);
        bool readPedsFromHolly(const char*);
        bool readGainsFromDB(const char*);

        void convertPedsFromHolly(const char* ifile,const char* ofile=NULL);
        void convertGainsFromHolly(const char* ifile,const char* ofile=NULL);

        double getGain(const int ix,const int iy);
};
SpecsECal::SpecsECal()
{
    const char* dir=gSystem->Getenv("HPS_PARMS");
    
    cview=NULL;
    hview=NULL;
    loadMap(dir);
    loadLookups();
    loadPedestals(dir);
    makeHist();
    makeBoxes();
//    makeCanny();

}
void SpecsECal::setRoughGains()
{
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        float gain=0.167;
        if (chans[ii].DBID<=0) continue;
        if (chans[ii].MB == "LT")
        {
            if (chans[ii].HV>5 && chans[ii].HV%2==0)
                gain/=1.5;
        }
        else if (chans[ii].MB == "LB")
        {
            if (chans[ii].HV>13 && chans[ii].HV<23
                    && chans[ii].HV%2==0)
                gain/=1.5;
        }
        chans[ii].GAIN=gain;
    }
}
void SpecsECal::printGainsForDAQ(const int crate,const char* ofilename)
{
    FILE *fout=OpenOutFile(ofilename);
    for (unsigned ii=3; ii<=20; ii++)
    {
        if (ii>9 && ii<14) continue;
        fprintf(fout,"FADC250_SLOT %d\n",ii);
        fprintf(fout,"FADC250_GAIN");
        for (unsigned int jj=0; jj<16; jj++)
        {
            fprintf(fout," %.3f",lookupFADC[crate-1][ii-1][jj]->GAIN);
        }
        fprintf(fout,"\n");
    }
    if (fout!=stdout) fclose(fout);
}
void SpecsECal::printPedsForDAQ(const int crate,const char* ofilename)
{
    FILE *fout=OpenOutFile(ofilename);
    for (int slot=3; slot<=9; slot++)
    {
        for (int chan=0; chan<16; chan++)
        {
            const float ped=lookupFADC[crate-1][slot-1][chan]->PED;
            const float pedrms=lookupFADC[crate-1][slot-1][chan]->PEDRMS;
            fprintf(fout,"%2d %3d %10.3f %6.3f 0\n",slot,chan,ped,pedrms);
        }
    }
    for (int slot=14; slot<=20; slot++)
    {
        for (int chan=0; chan<16; chan++)
        {
            const float ped=lookupFADC[crate-1][slot-1][chan]->PED;
            const float pedrms=lookupFADC[crate-1][slot-1][chan]->PEDRMS;
            fprintf(fout,"%2d %3d %10.3f %6.3f 0\n",slot,chan,ped,pedrms);
        }
    }
    if (fout!=stdout) fclose(fout);
}

void SpecsECal::SetDBID()
{
    // create channel_id for conditions database
    // (default is -1, set in ECalChannel constructor)
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        int ix=chans[ii].X;
        int iy=chans[ii].Y;
        if (!IsValidXY(ix,iy)) continue;
        if (ix<0) ix+=XOFFSET;
        else      ix+=XOFFSET-1;
        if (iy<0) iy+=YOFFSET;
        else      iy+=YOFFSET-1;
        iy = YOFFSET*2 - iy - 1;
        int dbid = ix + 2*XOFFSET*iy + 1;
        if      (chans[ii].Y == 1  && chans[ii].X>-10) dbid-=9;
        else if (chans[ii].Y == -1 && chans[ii].X<-10) dbid-=9;
        else if (chans[ii].Y < 0) dbid-=18;
        chans[ii].DBID = dbid;
//        std::cout<<chans[ii].X<<" "<<chans[ii].Y<<" "<<ix<<" "<<iy<<" "<<chans[ii].DBID<<std::endl;
    }
}
bool SpecsECal::loadMap(const char* dir)
{
    const TString fname=Form("%s/ecalwiring.csv",dir);
    FILE *ff;
    char buf[256];
    if (NULL == (ff=fopen(fname,"r")))
    {
        std::cerr<<"Missing Input File: "<<fname<<std::endl;
        return 0;
    }
    int ll=0;
    while ((fgets(buf,256,ff)) != NULL)
    {
        if (ll++==0) continue; // skip first line
        const char* sep=", \t";
        ECalChannel ee;
        ee.X=atoi((char*)strtok(buf,sep));
        ee.Y=atoi((char*)strtok(NULL,sep));
        ee.APD=atoi((char*)strtok(NULL,sep));
        ee.PREAMP=atoi((char*)strtok(NULL,sep));
        ee.LEDCHAN=atoi((char*)strtok(NULL,sep));
        ee.LEDDRIVER=atof((char*)strtok(NULL,sep));
        ee.FADCSLOT=atoi((char*)strtok(NULL,sep));
        ee.FADCCHAN=atoi((char*)strtok(NULL,sep));
        ee.SPLITTER=atoi((char*)strtok(NULL,sep));
        ee.HV=atoi((char*)strtok(NULL,sep));
        ee.JOUT=atoi((char*)strtok(NULL,sep));
        ee.MB=(char*)strtok(NULL,sep);
        ee.CHAN=atoi((char*)strtok(NULL,sep));
        //ee.GAIN=atoi((char*)strtok(NULL,sep));
        ee.FADCCRATE=ee.MB.Contains("T")?1:2;
        ee.LEDCRATE=ee.FADCCRATE;
        ee.XINDEX=x2xIndex(ee.X);
        ee.YINDEX=y2yIndex(ee.Y);
        chans.push_back(ee);
    }
    std::cout<<"SpecsECal: Read "<<ll-1<<" ECAL Channel Mappings."<<std::endl;

    // manually add non-ECAL channels to the list:
    // (last three channels on last slot of both crates)
    for (int ii=0; ii<2; ii++)
    {
        for (int jj=NCHANS-3; jj<NCHANS; jj++)
        {
            ECalChannel pp;
            pp.FADCCRATE=ii+1;
            pp.FADCSLOT=NSLOTS;
            pp.FADCCHAN=jj;
            chans.push_back(pp);
        }
    }
    
    // set ECAL index for the conditions database:
    SetDBID();
    
    return (ll-1 == NECALCHANS);
}
bool SpecsECal::loadPedestals(const char* dir)
{
    const TString fname[2]={
        Form("%s/fadc37_mode1.ped",dir),
        Form("%s/fadc39_mode1.ped",dir)};
    FILE *ff;
    char buf[256];
    int nped=0;
    for (int crat=0; crat<NCRATS; crat++)
    {
        if (NULL == (ff=fopen(fname[crat],"r")))
        {
            std::cerr<<"Missing Input File: "<<fname[crat]<<std::endl;
            std::cerr<<"All(?) pedestals will be zero."<<std::endl;
            return 0;
        }
        while ((fgets(buf,256,ff)) != NULL)
        {
            const char* sep=", \t";
            const int slot=atoi((char*)strtok(buf,sep))-1;
            const int chan=atoi((char*)strtok(NULL,sep));
            const float ped=atof((char*)strtok(NULL,sep));
            const float rms=atof((char*)strtok(NULL,sep));
            if (crat<0 || crat>=NCRATS || slot<0 || slot>=NSLOTS || chan<0 || chan>=NCHANS)
            {
                std::cerr<<"Peds: Invalid FADC:  "<<crat<<" "<<slot<<" "<<chan<<std::endl;
                continue;
            }
            nped++;
            lookupFADC[crat][slot][chan]->PED=ped;
            lookupFADC[crat][slot][chan]->PEDRMS=rms;
        }
        fclose(ff);
    }
    std::cout<<"SpecsECal: Read "<<nped<<" FADC Pedestals."<<std::endl;
    return 1;
}
void SpecsECal::loadLookups()
{
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        ECalChannel ee=chans[ii];
        const int crat=ee.FADCCRATE-1;
        const int slot=ee.FADCSLOT-1;
        const int chan=ee.FADCCHAN;
        const int xx=ee.X+XOFFSET;
        const int yy=ee.Y+YOFFSET;
        if (crat<0 || crat>=NCRATS || slot<0 || slot>=NSLOTS || chan<0 || chan>=NCHANS)
        {
            std::cerr<<"Lookup: Invalid FADC:  "<<crat<<" "<<slot<<" "<<chan<<std::endl;
            continue;
        }
        lookupFADC[crat][slot][chan]=&chans[ii];
        if (xx<0 || xx>=2*XOFFSET+1 || yy<0 || yy>=2*YOFFSET+1)
        {
            std::cerr<<"Lookup: Invalid XY:  "<<xx<<" "<<yy<<std::endl;
            continue;
        }
        // the rest is only for ECAL channels:
        if (ee.DBID<1) continue;
        lookupXY[xx][yy]=&chans[ii];
        const int ix = ee.X<0 ? xx : xx-1;
        const int iy = ee.Y<0 ? yy : yy-1;
        //std::cerr<<ix<<" "<<iy<<std::endl;
        lookupXYIndex[ix][iy]=&chans[ii];
        lookupLED[crat][ee.LEDCHAN]=&chans[ii];
        const int iside = ee.MB.Contains("L") ? 0 : 1;
        lookupChan[iside][ee.CHAN-1]=&chans[ii];
//        std::cout<<ee.DBID-1<<std::endl;
        lookupDBID[ee.DBID-1]=&chans[ii];
//        std::cout<<lookupDBID[ee.DBID-1]->X;
//        std::cout<<ix<<" "<<iy<<std::endl;
    }
}
int SpecsECal::xy2led(const int xx,const int yy)
{
    if (!lookupXY[xx+XOFFSET][yy+YOFFSET]) return -1;
    if (!IsValidXY(xx,yy)) return -9999;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->LEDCHAN;
}
void SpecsECal::led2fadc(const int crat,const int led)
{
    if (!lookupLED[crat-1][led]) return;
    std::cout<<lookupLED[crat-1][led]->FADCSLOT<<" "<<lookupLED[crat-1][led]->FADCCHAN<<std::endl;
}
void SpecsECal::led2xy(const int crat,const int led)
{
    if (!lookupLED[crat-1][led]) return;
    std::cout<<lookupLED[crat-1][led]->X<<" "<<lookupLED[crat-1][led]->Y<<std::endl;
}
int SpecsECal::led2fadcchan(const int crat,const int led)
{
    if (!lookupLED[crat-1][led]) return -1;
    return lookupLED[crat-1][led]->FADCCHAN;
}
int SpecsECal::led2fadcslot(const int crat,const int led)
{
    if (!lookupLED[crat-1][led]) return -1;
    return lookupLED[crat-1][led]->FADCSLOT;
}
void SpecsECal::print()
{
    for (unsigned int ii=0; ii<chans.size(); ii++)
        chans[ii].print();
}
void SpecsECal::printXY()
{
    for (int ix=0; ix<2*XOFFSET+1; ix++)
    {
        for (int iy=2*YOFFSET; iy>YOFFSET; iy--)
        {
            if(!lookupXY[ix][iy] || lookupXY[ix][iy]->DBID<=0) continue;
            lookupXY[ix][iy]->print();
        }
    }
    for (int ix=0; ix<2*XOFFSET+1; ix++)
    {
        for (int iy=0; iy<YOFFSET; iy++)
        {
            if(!lookupXY[ix][iy] || lookupXY[ix][iy]->DBID<=0) continue;
            lookupXY[ix][iy]->print();
        }
    }
}
void SpecsECal::printChan()
{
    for (int ii=0; ii<2; ii++)
    {
        for (int jj=1; jj<300; jj++)
        {
            if (!lookupChan[ii][jj]) continue;
            lookupChan[ii][jj]->print();
        }
    }
}


bool SpecsECal::IsValidSlot(const int slot)
{
    if (slot<3 || slot>NSLOTS) return 0;
    if (slot>9 && slot<14) return 0;
    return 1;
}
bool SpecsECal::IsValidChannel(const int slot,const int chan)
{
    if (!IsValidSlot(slot)) return 0;
    if (chan<0 || chan>=NCHANS) return 0;
    return 1;
}
bool SpecsECal::IsValidChannel(const int crate,const int slot,const int chan)
{
    if (crate<1 || crate>NCRATS) return 0;
    return IsValidChannel(slot,chan);
}
bool SpecsECal::IsValidXY(const int xx,const int yy)
{
    if (abs(xx)>XOFFSET || abs(yy)>YOFFSET) return 0;
    if (xx==0 || yy==0) return 0;
    if (abs(yy)<2 && xx>=-10 && xx<=-2) return 0;
    return 1;
}
bool SpecsECal::IsValidXYIndex(const int ix,const int iy)
{
    const int xx = ix<XOFFSET ? ix : ix+1;
    const int yy = iy<YOFFSET ? iy : iy+1; 
    return IsValidXY(xx,yy);
}
bool SpecsECal::IsECalChannel(const int slot,const int chan)
{
    if (!IsValidSlot(slot)) return 0;
    if (slot==NSLOTS && chan>=NCHANS-3) return 0;
    return 1;
}
bool SpecsECal::IsPmtChannel(const int slot,const int chan)
{
    return (slot==NSLOTS && chan>=NCHANS-3 && chan<NCHANS);
}



float SpecsECal::getPedestalFADC(const int crate,const int slot,const int chan)
{
    if (!IsValidChannel(crate,slot,chan)) return 0;
    return lookupFADC[crate-1][slot-1][chan]->PED;
}
float SpecsECal::getPedestalXY(const int xx,const int yy)
{
    if (abs(xx)>XOFFSET || abs(yy)>YOFFSET) return -9999;
    if (xx==0 || yy==0) return -9999;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->PED;
}
float SpecsECal::getGainXY(const int xx,const int yy)
{
    if (abs(xx)>XOFFSET || abs(yy)>YOFFSET) return -9999;
    if (xx==0 || yy==0) return -9999;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->GAIN;
}

int SpecsECal::fadc2xIndex(const int crate,const int slot,const int chan)
{
    const int ix=fadc2x(crate,slot,chan);
    return x2xIndex(ix);
//    if (ix<0) return ix+XOFFSET;
//    if (ix>0) return ix-1+XOFFSET;
//    return -1;
}
int SpecsECal::fadc2yIndex(const int crate,const int slot,const int chan)
{
    const int iy=fadc2y(crate,slot,chan);
    return y2yIndex(iy);
//    if (iy<0) return iy+YOFFSET;
//    if (iy>0) return iy-1+YOFFSET;
//    return -1;
}
int SpecsECal::x2xIndex(const int xx)
{
    if (abs(xx)>2*XOFFSET) return -1;
    if (xx<0) return xx+XOFFSET;
    if (xx>0) return xx+XOFFSET-1;
    return -1;
}
int SpecsECal::y2yIndex(const int yy)
{
    if (abs(yy)>2*YOFFSET) return -1;
    if (yy<0) return yy+YOFFSET;
    if (yy>0) return yy+YOFFSET-1;
    return -1;
}
int SpecsECal::fadc2x(const int crate,const int slot,const int chan)
{
    if (!IsValidChannel(crate,slot,chan)) return 0;
    return lookupFADC[crate-1][slot-1][chan]->X;
}
int SpecsECal::fadc2y(const int crate,const int slot,const int chan)
{
    if (!IsValidChannel(crate,slot,chan)) return 0;
    return lookupFADC[crate-1][slot-1][chan]->Y;
}
int SpecsECal::xy2fadcslot(const int xx,const int yy)
{
    if (!IsValidXY(xx,yy)) return -8888;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->FADCSLOT;
}
int SpecsECal::xy2fadcchan(const int xx,const int yy)
{
    if (!IsValidXY(xx,yy)) return -8888;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->FADCCHAN;
}
int SpecsECal::xy2jout(const int xx,const int yy)
{
    if (!IsValidXY(xx,yy)) return -8888;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->JOUT;
}
int SpecsECal::xy2hv(const int xx,const int yy)
{
    if (!IsValidXY(xx,yy)) return -8888;
    return lookupXY[xx+XOFFSET][yy+YOFFSET]->HV;
}


void SpecsECal::makeHist()
{
//    std::cerr<<"Making hist ..."<<std::endl;
    if (hview) return;
    hview=new TH2D("hSpecsECal","",49,-XOFFSET-1,XOFFSET+1,12,-YOFFSET-1,YOFFSET+1);
    hview->GetXaxis()->SetNdivisions(49);
    hview->GetYaxis()->SetNdivisions(13);
    hview->GetXaxis()->SetTickLength(0.012);
    hview->GetYaxis()->SetTickLength(0.004);
}
void SpecsECal::makeBoxes()
{
//    static bool called=0;
//    if (called) return;
    const float off=0.45;
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        if (chans[ii].DBID<1) continue;
        const float xx=(float)chans[ii].X;
        const float yy=(float)chans[ii].Y;
        const int id=chans[ii].DBID-1;
        boxes[id]=new TBox(xx-off,yy-off,xx+off,yy+off);
        boxes[id]->SetFillStyle(0);
        boxes[id]->SetLineStyle(1);
    }
//    called=1;
}
void SpecsECal::drawCanvas()
{
    getCanvas();
    cview->Draw();
}
TCanvas* SpecsECal::getCanvas()
{
    if (cview) return cview;
    const float ysize=400;
    const float aspect=(2.*XOFFSET)/(2.*YOFFSET+3.);
    cview=new TCanvas("cSpecsECal","",aspect*ysize,ysize);
    gPad->SetMargin(0.03,0.005,0.08,0.01);
    return cview;
}
void SpecsECal::drawChannels()
{
    for (unsigned int ii=0; ii<442; ii++)//boxes.size(); ii++)
        boxes[ii]->DrawClone();
}
void SpecsECal::makeCanny()
{
    const char* cname[4]={"RT","LT","RB","LB"};
    for (int ii=0; ii<4; ii++)
    {
        canny[ii]=new TCanvas(Form("canny_%s",cname[ii]),"",1200,200);
        paddy[ii]=CanvasPartition(canny[ii],XOFFSET,YOFFSET);
    }
}
FILE *SpecsECal::OpenOutFile(const char* ofilename)
{
    FILE *fout=NULL;
    if (ofilename)
    {
        if (!gSystem->AccessPathName(ofilename))
            std::cerr<<"File already exists:  "<<ofilename<<std::endl;
        else
            fout=fopen(ofilename,"w");
    }
    if (!fout) fout=stdout;
    return fout;
}
void SpecsECal::WriteDB_ecal_channels(const char* ofilename)
{
    FILE *fout=OpenOutFile(ofilename);
    fprintf(fout,"channel_id x y crate slot channel\n");
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        if (chans[ii].DBID > 0)
        {
            fprintf(fout,"%d %d %d %.2f %.0f %.0f\n",
                    chans[ii].DBID,chans[ii].LEDCRATE,chans[ii].LEDCHAN,
                    chans[ii].LEDDELAY,chans[ii].LEDAMPLO,chans[ii].LEDAMPHI);
        }
    }
    if (fout!=stdout) fclose(fout);
}
void SpecsECal::WriteDB_ecal_leds(const char* ofilename)
{
    FILE *fout=OpenOutFile(ofilename);
    fprintf(fout,"ecal_channel_id crate number time_delay amplitude_high amplitude_low\n"); 
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        if (chans[ii].DBID > 0)
        {
            fprintf(fout,"%d %d %d %.2f %.0f %.0f\n",
                    chans[ii].DBID,chans[ii].LEDCRATE,chans[ii].LEDCHAN,
                    chans[ii].LEDDELAY,chans[ii].LEDAMPLO,chans[ii].LEDAMPHI);
        }
    }
    if (fout!=stdout) fclose(fout);
}
void SpecsECal::WriteDB_ecal_gains(const char* ofilename)
{
    FILE *fout=OpenOutFile(ofilename);
    fprintf(fout,"ecal_channel_id gain\n");
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        if (chans[ii].DBID > 0)
        {
            fprintf(fout,"%d %.3f\n",
                    chans[ii].DBID,chans[ii].GAIN);
        }
    }
    if (fout!=stdout) fclose(fout);
}
void SpecsECal::WriteDB_ecal_time_shifts(const char*){}
void SpecsECal::WriteDB_bad_channels(const char*){}
void SpecsECal::WriteDB_ecal_calibrations(const char* ofilename)
{
    FILE *fout=OpenOutFile(ofilename);
    fprintf(fout,"ecal_channel_id pedestal noise\n");
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
        if (chans[ii].DBID > 0)
        {
            fprintf(fout,"%d %.2f %.2f\n",
                    chans[ii].DBID,chans[ii].PED,chans[ii].PEDRMS);
        }
    }
    if (fout!=stdout) fclose(fout);
}
std::vector <ECalChannel*> SpecsECal::getHV(const char* mb,const int hv)
{
    std::vector <ECalChannel*> xy;
    for (unsigned int ii=0; ii<chans.size(); ii++)
        if (chans[ii].MB==mb && chans[ii].HV==hv)
            xy.push_back(&chans[ii]);
    return xy;
}
std::vector <ECalChannel*> SpecsECal::getJOUT(const char* mb,const int jout)
{
    std::vector <ECalChannel*> xy;
    for (unsigned int ii=0; ii<chans.size(); ii++)
        if (chans[ii].MB==mb && chans[ii].JOUT==jout)
            xy.push_back(&chans[ii]);
    return xy;
}
void SpecsECal::drawJOUT(const char* mb,const int jout,const int col)
{
    std::vector <ECalChannel*> xy=getJOUT(mb,jout);
    for (unsigned int ii=0; ii<xy.size(); ii++)
    {
        const int id=xy[ii]->DBID;
        if (id<1) continue;
        const int oldcol=boxes[id-1]->GetLineColor();
        boxes[id-1]->SetLineColor(col);
        boxes[id-1]->DrawClone();
        boxes[id-1]->SetLineColor(oldcol);
    }
}
void SpecsECal::drawHV(const char* mb,const int hv,const int col)
{
    std::vector <ECalChannel*> xy=getHV(mb,hv);
    for (unsigned int ii=0; ii<xy.size(); ii++)
    {
        const int id=xy[ii]->DBID;
        if (id<1) continue;
        const int oldcol=boxes[id-1]->GetLineColor();
        boxes[id-1]->SetLineColor(col);
        boxes[id-1]->DrawClone();
        boxes[id-1]->SetLineColor(oldcol);
    }
}
void testJOUT(const char* mb,const int jout)
{
    static SpecsECal s;
    std::vector <ECalChannel*> xy=s.getJOUT(mb,jout);
    for (unsigned int ii=0; ii<xy.size(); ii++)
        std::cout<<xy[ii]->X<<" "<<xy[ii]->Y<<std::endl;
}
void testHV(const char* mb,const int hv)
{
    static SpecsECal s;
    std::vector <ECalChannel*> xy=s.getHV(mb,hv);
    for (unsigned int ii=0; ii<xy.size(); ii++)
    {
        std::cout<<xy[ii]->X<<" "<<xy[ii]->Y<<std::endl;
        std::cout<<xy[ii]->XINDEX<<" "<<xy[ii]->YINDEX<<std::endl;
    }
}
void testDRAW()
{
    static SpecsECal s;
    gStyle->SetOptStat(0);
    TH1 *h=s.getHist();
    s.getCanvas();
    h->Draw();
    s.drawChannels();
    s.drawHV("LT",1,kCyan);
    s.drawJOUT("RT",7,kMagenta);
}
bool SpecsECal::readGainsFromDB(const char* filename)
{
    int dbid;
    float gain;
    FILE *f=fopen(filename,"r");
    while (fscanf(f,"%d %f",&dbid,&gain)==2)
    {
//        std::cerr<<dbid<<std::endl;
        //lookupDBID[dbid-1]->GAIN=gain;
        for (unsigned int ii=0; ii<chans.size(); ii++)
        {
            if (chans[ii].DBID == dbid)
            {
                chans[ii].GAIN = gain;
            }
        }
    }
    fclose(f);
    return 1;
}
bool SpecsECal::readGainsFromHolly(const char* filename)
{
    int ix,iy;
    float gain;
    FILE *f=fopen(filename,"r");
    while (fscanf(f,"%d %d %f",&ix,&iy,&gain)==3)
    {
//        std::cerr<<ix<<" "<<iy<<std::endl;
//        std::cerr<<lookupXYIndex[ix][iy]<<std::endl;
        lookupXYIndex[ix][iy]->GAIN=gain;
    }
    fclose(f);
    return 1;
}
bool SpecsECal::readPedsFromHolly(const char* filename)
{
    int ix,iy;
    float ped,rms;
    FILE *f=fopen(filename,"r");
    while (fscanf(f,"%d %d %f %f",&ix,&iy,&ped,&rms)==4)
    {
//        std::cerr<<ix<<" "<<iy<<std::endl;
        lookupXYIndex[ix][iy]->PED=ped;
        lookupXYIndex[ix][iy]->PEDRMS=rms;
    }
    fclose(f);
    return 1;
}
void SpecsECal::convertPedsFromHolly(const char* ifilename,const char* ofilename)
{
    readPedsFromHolly(ifilename);
    WriteDB_ecal_calibrations(ofilename);
    printPedsForDAQ(1,ofilename?Form("%s_fadc37.ped",ofilename):NULL);
    printPedsForDAQ(2,ofilename?Form("%s_fadc39.ped",ofilename):NULL);
}
void SpecsECal::convertGainsFromHolly(const char* ifilename,const char* ofilename)
{
    readGainsFromHolly(ifilename);
    WriteDB_ecal_gains(ofilename);
    printGainsForDAQ(1,ofilename?Form("%s_fadc37.gain",ofilename):NULL);
    printGainsForDAQ(2,ofilename?Form("%s_fadc39.gain",ofilename):NULL);
}
double SpecsECal::getGain(const int ix,const int iy)
{
    std::cout<<chans.size()<<std::endl;
    for (unsigned int ii=0; ii<chans.size(); ii++)
    {
//        std::cerr<<chans[ii].XINDEX<<" "<<chans[ii].YINDEX<<std::endl;
        if (chans[ii].XINDEX==ix && chans[ii].YINDEX==iy)
        {
            return chans[ii].GAIN;
        }
    }
    return 0;
}
#endif
