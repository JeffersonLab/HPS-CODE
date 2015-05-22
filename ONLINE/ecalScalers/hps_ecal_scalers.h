// Header
#include <stdio.h>
#include <stdlib.h>
#include <TClass.h>
#include <TCanvas.h>
#include <TH2.h>
#include <TPaveText.h>
#include <TH2Poly.h>
#include <TSystem.h>
#include <TStyle.h>
#include <TRootEmbeddedCanvas.h>
#include <TApplication.h>
#include <TGFileDialog.h>
#include <TGButton.h>
#include <TImage.h>
#include <TArrow.h>
#include <THashList.h>
#include <TTimeStamp.h>
#include <TColor.h>

#include <unistd.h>
#include <iostream>

#include "CrateMsgClient.h"

struct totalrates_t
{
    int top,bottom,left,right,total,max;
};


class hps_ecal_scalers_app : public TGMainFrame
{
    private:
        int connect_to_server();
        int reconnect_to_server();
        int read_scalers();
        int get_ch(int x, int y);
        int get_crate_map();
        int hps_crate_map[2][22];

        unsigned int hps_ecal_crate_slot_scalers[2][22][16];
        unsigned int hps_ecal_crate_slot_ref[2][22];

        totalrates_t get_total_rate();

        void draw_scalers();
        void normalize_scalers();

        CrateMsgClient *crate_hps[2];
        TCanvas *pTC;
        TH2I *pH;
        TH2D *pH2;
        TRootEmbeddedCanvas *pCanvas;

        int hpsCrates[2];

    public:
        hps_ecal_scalers_app(const TGWindow *p, UInt_t w, UInt_t h, int scalerType);
        ~hps_ecal_scalers_app();

        void DoExit();
        void button_Save();
        void button_LogEnable();
        void refresh_scalers();

        bool enableButtons;
        bool doLogScale;
        int updatePeriod;
        int scalerType;
        bool doAccumulate;

        ClassDef(hps_ecal_scalers_app, 0)
};
