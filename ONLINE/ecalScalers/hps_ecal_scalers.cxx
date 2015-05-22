#include "hps_ecal_scalers.h"

ClassImp(hps_ecal_scalers_app)

int hps_ecal_scalers_app::reconnect_to_server()
{
    for (int i=0; i<2; i++)
    {
        crate_hps[i]->Close();
        crate_hps[i]->Delete();
    }
    return connect_to_server();
}

int hps_ecal_scalers_app::connect_to_server()
{
    // HARD-CODING CRATES hps1/2/12/11:
    int crates[2];
    if (scalerType == SCALER_TYPE_FADC250) 
    {
        crates[0]=1;
        crates[1]=2;
    }
    else if (scalerType == SCALER_TYPE_DSC2)
    {
        crates[0]=12;
        crates[1]=11;
    }
    else exit(-1);

    for(int i = 0; i < 2; i++)
    {
        char buf[100];
        sprintf(buf, "hps%d", crates[i]);
        crate_hps[i] = new CrateMsgClient(buf, 6102);
        if(!crate_hps[i]->IsValid()) return -1;
    }
    return 0;
}

int hps_ecal_scalers_app::read_scalers()
{
    unsigned int *buf;
    int len;

    static const int ref = scalerType==SCALER_TYPE_FADC250 ? 16 : 68;
    static const int off = scalerType==SCALER_TYPE_FADC250 ? 0 : 51;

    for(int crate = 0; crate < 2; crate++)
    {
        for(int slot = 0; slot <= 20; slot++)
        {
            if(hps_crate_map[crate][slot] == scalerType)
            {
                if(!crate_hps[crate]->ScalerReadBoard(slot, &buf, &len)) return -3;
                if(scalerType==SCALER_TYPE_DSC2 || len == 17)
                {
                    for(int ch = 0; ch < 16; ch++)
                        hps_ecal_crate_slot_scalers[crate][slot][ch] = buf[off+ch];
                    hps_ecal_crate_slot_ref[crate][slot] = buf[ref];
                }
                delete [] buf;
            }
        }
    }
    return 0;
}

void hps_ecal_scalers_app::normalize_scalers()
{
    float ref, scaled, ref1;
    int ref2;

    if (scalerType == SCALER_TYPE_FADC250) 
    {
        ref1 = 488281.25f;
        ref2 = 1;
    }
    else if (scalerType == SCALER_TYPE_DSC2) 
    {
        ref1 = 125.0E6f;
        ref2 = 1250;
    }
    else 
    {
        exit(-1);
    }
        

    for(int crate = 0; crate < 2; crate++)
    {
        for(int slot = 0; slot <= 20; slot++)
        {
            if(hps_crate_map[crate][slot] == scalerType)
            {
                if(hps_ecal_crate_slot_ref[crate][slot] <= 0)
                {
                    printf("Error in normalize_scalers(): hps_ecal_crate_slot_ref[%d][%d]=%d not valid\n", crate, slot, hps_ecal_crate_slot_ref[crate][slot]);
                    ref = 1;
                }
                else
                    ref = ref1 / (float)hps_ecal_crate_slot_ref[crate][slot];

                for(int ch = 0; ch < 16; ch++)
                {
                    scaled = (float)hps_ecal_crate_slot_scalers[crate][slot][ch] * ref / ref2;
                    hps_ecal_crate_slot_scalers[crate][slot][ch] = (int)scaled;
                }
            }
        }
    }
}

totalrates_t hps_ecal_scalers_app::get_total_rate()
{
    totalrates_t rr={0,0,0,0,0,0};
    for (int crate=0; crate<2; crate++)
    {
        for (int slot=0; slot<=20; slot++)
        {
            for (int chan=0; chan<16; chan++)
            {
                if (slot==20 && chan>12) continue;
                const int xx=hps_ecal_crate_slot_scalers[crate][slot][chan];
                rr.total += xx; 
                if (crate==0) rr.top += xx;
                else          rr.bottom += xx;
            }
        }
    }
    return rr;
}

int hps_ecal_scalers_app::get_ch(int x, int y)
{
    int x_pos = 23;
    int y_pos = 1;
    int idx = 0;

    while(x_pos > -23)
    {
        if((x == x_pos) && (y == y_pos))
        {
            if(idx < 7*16)
                return 3*16+idx;
            else
                return 7*16+idx;
        }
        idx++;
        if(y_pos >= 5)
        {
            x_pos--;
            if((x_pos <= -1) && (x_pos >= -9))
                y_pos = 2;
            else
                y_pos = 1;
        }
        else
            y_pos++;
    }
    return -1;
}

void hps_ecal_scalers_app::draw_scalers()
{
    static bool called=0;

    static TPaveText tt1(0.1,0.9,0.3,1.0,"NDC");
    static TPaveText tt2(0.7,0.91,0.9,0.99,"NDC");
    static TPaveText ttT(-22+13+0.05,6-5,-22+22,7-5-0.05);
    static TPaveText ttB(-22+13+0.05,4-5+0.05,-22+22,5-5);
    static TPaveText ttM(-22+0+0.05,5-5+0.05,-22+13,6-5.01);
    static TBox bb;
    static TLine ll;
    static TText tarrow(14.5,0.3,"Beam Left");
    static TArrow arrow(19,0.5,23,0.5,0.02,"|>");
    static TPaveText tdatime(-5,-6.5,5,-5.8);

    if (!called)
    {
        called=1;
        bb.SetFillStyle(1001);
        bb.SetFillColor(kWhite);
        bb.SetLineWidth(1);
        bb.SetLineColor(kBlack);
        tt1.SetBorderSize(0);
        tt2.SetBorderSize(0);
        tt1.SetFillColor(kWhite);
        tt2.SetFillColor(kWhite);
        ttT.SetBorderSize(0);
        ttB.SetBorderSize(0);
        ttT.SetFillColor(kWhite);
        ttB.SetFillColor(kWhite);
        ttM.SetBorderSize(0);
        ttM.SetFillColor(kWhite);
        ttM.SetTextColor(kRed);
        arrow.SetAngle(40);
        arrow.SetFillColor(kBlack);
        arrow.SetLineWidth(2);
        tdatime.SetFillColor(kWhite);
        tdatime.SetBorderSize(0);
        tdatime.SetLineWidth(0);
    }

    const int histoUnits = scalerType == SCALER_TYPE_FADC250 ? 1e3 : 1; // seconds

    unsigned int max=0;
    if (!doAccumulate) pH->Reset();
    if (!doAccumulate) pH2->Reset();
    pH->SetMinimum(0.1);
    pH2->SetMinimum(0.1);
    for(int x = -23; x <= 23; x++)
    {
        for(int y = 1; y <= 5; y++)
        {
            int ch = get_ch(x, y);

            if(ch >= 0)
            {
                // one TH2I for number display:
                pH->Fill(x, y, (float)hps_ecal_crate_slot_scalers[0][ch/16][ch%16]/histoUnits);
                pH->Fill(x, -y, (float)hps_ecal_crate_slot_scalers[1][ch/16][ch%16]/histoUnits);
                
                // one TH2D for color display:
                pH2->Fill(x, y, (float)hps_ecal_crate_slot_scalers[0][ch/16][ch%16]/histoUnits);
                pH2->Fill(x, -y, (float)hps_ecal_crate_slot_scalers[1][ch/16][ch%16]/histoUnits);

                // just look at crystals adjacent to beam hole for maximum:
                if (y<3 && (x>=-11 || x<=1))
                {
                    if (hps_ecal_crate_slot_scalers[0][ch/16][ch%16] > max) 
                        max=hps_ecal_crate_slot_scalers[0][ch/16][ch%16];
                    if (hps_ecal_crate_slot_scalers[1][ch/16][ch%16] > max) 
                        max=hps_ecal_crate_slot_scalers[1][ch/16][ch%16];
                }
            }
        }
    }

    bb.DrawBox(-9+0.05,-1,0,1.97);
    bb.DrawBox(-24,0,24.05,0.97);
    ll.DrawLine(pH->GetXaxis()->GetXmin(),pH->GetYaxis()->GetXmin(),
                pH->GetXaxis()->GetXmax(),pH->GetYaxis()->GetXmin());
    ll.DrawLine(pH->GetXaxis()->GetXmin(),pH->GetYaxis()->GetXmax(),
                pH->GetXaxis()->GetXmax(),pH->GetYaxis()->GetXmax());
    ll.DrawLine(pH->GetXaxis()->GetXmin(),pH->GetYaxis()->GetXmin(),
                pH->GetXaxis()->GetXmin(),0);
    ll.DrawLine(pH->GetXaxis()->GetXmax(),pH->GetYaxis()->GetXmin(),
                pH->GetXaxis()->GetXmax(),0);
    ll.DrawLine(pH->GetXaxis()->GetXmin(),pH->GetYaxis()->GetXmax(),
                pH->GetXaxis()->GetXmin(),1);
    ll.DrawLine(pH->GetXaxis()->GetXmax(),pH->GetYaxis()->GetXmax(),
                pH->GetXaxis()->GetXmax(),1);
    ll.DrawLine(pH->GetXaxis()->GetXmax(),0,0,0);
    ll.DrawLine(pH->GetXaxis()->GetXmax(),1,0,1);
    ll.DrawLine(pH->GetXaxis()->GetXmin(),0,-9,0);
    ll.DrawLine(pH->GetXaxis()->GetXmin(),1,-9,1);
    ll.DrawLine(-9,-1,0,-1);
    ll.DrawLine(-9,2,0,2);
    ll.DrawLine(-9,1,-9,2);
    ll.DrawLine(-9,-1,-9,0);
    ll.DrawLine(0,-1,0,0);
    ll.DrawLine(0,1,0,2);
                


    const totalrates_t rr=get_total_rate();
    tt1.Clear();
    tt2.Clear();
    ttT.Clear();
    ttB.Clear();
    ttM.Clear();
    
    const int textUnits = scalerType == SCALER_TYPE_FADC250 ? 1e6 : 1e3;
    const char* stringUnit = textUnits == 1e6 ? "M" : "k";
    
    tt1.AddText(Form("Total:  %.1E Hz",(float)rr.total));
    tt2.AddText(Form("Total:  %.2f %sHz",(float)rr.total/textUnits,stringUnit));
    ttT.AddText(Form("%.2f %sHz",(float)rr.top/textUnits,stringUnit));
    ttB.AddText(Form("%.2f %sHz",(float)rr.bottom/textUnits,stringUnit));
    ttM.AddText(Form("MAX SINGLE CRYSTAL = %.2f kHz",(float)max/1e3));
    tt1.Draw();
    tt2.Draw();
    ttT.Draw();
    ttB.Draw();
    ttM.Draw();
    
    arrow.Draw();
    tarrow.Draw();

    TDatime datime;
    tdatime.Clear();
    tdatime.AddText(Form("%d/%d/%d %.2d:%.2d:%2d",
                datime.GetDay(),datime.GetMonth(),datime.GetYear(),
                datime.GetHour(),datime.GetMinute(),datime.GetSecond()));
    tdatime.Draw();

    gPad->SetLogz(doLogScale);

    pCanvas->GetCanvas()->Modified();
    pCanvas->GetCanvas()->Update();
}

int hps_ecal_scalers_app::get_crate_map()
{
    unsigned int *map;
    int len;

    for(int crate = 0; crate < 2; crate++)
    {
        if(!crate_hps[crate]->GetCrateMap(&map, &len)) return -4;
        if(len > 22) return -5;

        for(int slot = 0; slot < len; slot++)
        {
            hps_crate_map[crate][slot] = map[slot];
            printf("crate %d, slot %d, type %d\n", crate, slot, map[slot]);
        }
        delete [] map;
    }
    return 0;
}

void hps_ecal_scalers_app::refresh_scalers()
{
    if(read_scalers() < 0) DoExit();

    normalize_scalers();
    draw_scalers();

    TTimer::SingleShot(updatePeriod, "hps_ecal_scalers_app", this, "refresh_scalers()");
}

void hps_ecal_scalers_app::DoExit()
{
    gApplication->Terminate();
}

hps_ecal_scalers_app::~hps_ecal_scalers_app()
{
    Cleanup();
}

void hps_ecal_scalers_app::button_LogEnable()
{
    pCanvas->GetCanvas()->SetLogz(!pCanvas->GetCanvas()->GetLogz());
}

void hps_ecal_scalers_app::button_Save()
{
    TClass* clGMainFrame = TClass::GetClass("TGMainFrame");
    TGWindow* win = 0;

    TTimeStamp tt;
    TString tstub=tt.AsString("lc");
    tstub.ReplaceAll(" ","_");

    gPad->SaveAs(Form("%s/screenshots/ECALSCALERS_%s.png",
                gSystem->Getenv("HOME"),tstub.Data()));
    std::cerr<<"AL:SFHDLA"<<std::endl;
    return;

    static TString dir("printouts");
    TGFileInfo fi;
    const char *myfiletypes[] = 
    { 
        "All files","*",
        "PNG files","*.png",
        "GIF files","*.gif",
        "JPG files","*.jpg",
        0,
        0 
    };

    fi.fFileTypes = myfiletypes;
    fi.fIniDir    = StrDup(dir.Data());

    new TGFileDialog(gClient->GetRoot(), 0, kFDSave, &fi);

    if(fi.fFilename != NULL) 
    {
        printf("saving to file: %s\n", fi.fFilename);
        TIter iWin(gClient->GetListOfWindows());
        while ((win = (TGWindow*)iWin()))
        {
            if(win->InheritsFrom(clGMainFrame))
            {
                TImage *img = TImage::Create();
                img->FromWindow(win->GetId());
                TString dog=gSystem->BaseName(fi.fFilename);
                dog.ReplaceAll(".","__"+tstub+".");
                dog=Form("%s/screenshots/EcalScalers_FADC_%s",
                        gSystem->Getenv("HOME"),dog.Data());
                if (scalerType==SCALER_TYPE_DSC2)
                    dog.ReplaceAll("FADC","DSC2");
                std::cout<<"Saving as:   "<<dog<<std::endl;
                img->WriteImage(dog);
                img->WriteImage(fi.fFilename);
                break;
            }
        }
    }
}

hps_ecal_scalers_app::hps_ecal_scalers_app(const TGWindow *p, UInt_t w, UInt_t h,int scalerType2) : TGMainFrame(p, w, h) 
{
    printf("hps_ecal_scalers_app started...\n");

    enableButtons=0;
    doLogScale=1; // default: yes, log
    updatePeriod=1000; // default: 1s
    scalerType=scalerType2;//SCALER_TYPE_FADC250; // default: FADC, not DSC
    doAccumulate=0;

    SetCleanup(kDeepCleanup);

    Connect("CloseWindow()", "hps_ecal_scalers_app", this, "DoExit()");
    DontCallClose();

    TGCompositeFrame *pTF;
    TGTextButton *pB;

    AddFrame(pTF= new TGHorizontalFrame(this), new TGLayoutHints(kLHintsExpandX));

    if (enableButtons)
    {
        pTF->AddFrame(pB = new TGTextButton(pTF, new TGHotString("LogToggle")), new TGLayoutHints(kLHintsLeft | kLHintsCenterX));
        pB->Connect("Clicked()", "hps_ecal_scalers_app", this, "button_LogEnable()");
        pTF->AddFrame(pB = new TGTextButton(pTF, new TGHotString("Save")), new TGLayoutHints(kLHintsLeft | kLHintsCenterX));
        pB->Connect("Clicked()", "hps_ecal_scalers_app", this, "button_Save()");
        pTF->AddFrame(pB = new TGTextButton(pTF, new TGHotString("Exit")), new TGLayoutHints(kLHintsLeft | kLHintsCenterX));
        pB->Connect("Clicked()", "hps_ecal_scalers_app", this, "DoExit()");
    }

    AddFrame(pTF = new TGVerticalFrame(this), new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));
    pTF->AddFrame(pCanvas = new TRootEmbeddedCanvas("c1", pTF, w, h), new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));

    pCanvas->GetCanvas()->SetBorderMode(0);
    pCanvas->GetCanvas()->cd();

    TString title="HPS FADC Scalers";
    if (scalerType == SCALER_TYPE_DSC2)
        title=title.ReplaceAll("FADC","DSC2");

    pH2 = new TH2D(title+"2", ";X;Y", 46, -22.0, 24.0, 11, -5.0, 6.0);
    pH2->SetStats(0);
    pH2->GetXaxis()->CenterLabels();
    pH2->GetXaxis()->SetNdivisions(46, kFALSE);
    pH2->GetXaxis()->SetTickLength(0);
    pH2->GetYaxis()->CenterLabels();
    pH2->GetYaxis()->SetNdivisions(11, kFALSE);
    pH2->GetYaxis()->SetTickLength(0);
    pH2->GetYaxis()->SetTitleOffset(0.5);
    pH2->Draw("COLZ");
    
    pH = new TH2I(title, ";X;Y", 46, -22.0, 24.0, 11, -5.0, 6.0);
    pH->SetStats(0);
    pH->GetXaxis()->CenterLabels();
    pH->GetXaxis()->SetNdivisions(46, kFALSE);
    pH->GetXaxis()->SetTickLength(0);
    pH->GetYaxis()->CenterLabels();
    pH->GetYaxis()->SetNdivisions(11, kFALSE);
    pH->GetYaxis()->SetTickLength(0);
    pH->GetYaxis()->SetTitleOffset(0.5);
    pH->Draw("TEXTSAME");

    TText tt;
    tt.SetTextColor(kBlack);
    tt.SetTextAngle(90);
    tt.DrawText(25.2,0,scalerType==SCALER_TYPE_FADC250 ? "kHz":"Hz");
    tt.SetTextAngle(0);
    tt.SetTextColor(kRed);
    tt.SetTextSize(0.08);

    TString title2="FADC SCALERS";
    if (scalerType==SCALER_TYPE_DSC2)
        title2.ReplaceAll("FADC","DSC2");
    tt.DrawTextNDC(0.38,0.92,title2);

    std::cout<<title2<<" "<<title<<" "<<std::endl;

    gPad->SetLogz(doLogScale);
    gPad->SetGrid(1,1);
    gPad->SetLeftMargin(0.05);
    gStyle->SetGridStyle(1);
    gStyle->SetGridColor(kGray);

    int x = -23;
    for(int n = 1; n <= 46; n++)
    {
        pH->GetXaxis()->SetBinLabel(n,Form("%d", x));
        pH2->GetXaxis()->SetBinLabel(n,Form("%d", x));
        x++;
        if(x == 0) x++;
    }

    memset(hps_ecal_crate_slot_scalers, 0, sizeof(hps_ecal_crate_slot_scalers));
    memset(hps_ecal_crate_slot_ref, 0xFF, sizeof(hps_ecal_crate_slot_ref));

    if(connect_to_server() < 0) DoExit();
    if(get_crate_map() < 0) DoExit();

    TString title3="ECAL FADC SCALERS";
    if (scalerType == SCALER_TYPE_DSC2)
        title3=title3.ReplaceAll("FADC","DSC2");

    SetWindowName(title3);
    MapSubwindows();
    Resize();
    MapWindow();

    TTimer::SingleShot(updatePeriod, "hps_ecal_scalers_app", this, "refresh_scalers()");
}

//void hps_ecal_scalers_app_run()
//{
//    new hps_ecal_scalers_app(gClient->GetRoot(), 1500, 500);
//}

void setupColorScale()
{
    Double_t __stops[5] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t __red[5]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
    Double_t __green[5] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
    Double_t __blue[5]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(5, __stops, __red, __green, __blue, 255);
    gStyle->SetNumberContours(255);
}

int main(int argc,char* argv[])
{
    // DEFAULTS:
    int updatePeriod=1000; // milliseconds
    bool doLogScale=1;
    bool enableButtons=0;
    bool doAccumulate=0;
    int scalerType=SCALER_TYPE_FADC250;
    
    const char* usage="hps_scalers [options]\n"
        "\t-l    linear scale (default is log)\n"
        "\t-t #  update period (milliseconds)\n"
        "\t-d    use discriminators (default = FADCs)\n"
        "\t-a    accumulate counts\n"
        "\t-b    enable buttons (broken)\n";

    int itmp;
    while ( (itmp=getopt(argc,argv,"ldat:")) != -1 )
    {
        switch (itmp)
        {
            case 'l':
                doLogScale=0;
                break;
            case 't':
                updatePeriod=atoi(optarg);
                break;
            case 'd':
                scalerType=SCALER_TYPE_DSC2;
                break;
            case 'b':
                enableButtons=1;
                break;
            case 'a':
                doAccumulate=1;
                break;
            default:
                std::cout<<usage<<std::endl;
                exit(1);
        }
    }

    setupColorScale();

    TApplication asdf("asdf",&argc,argv);

    hps_ecal_scalers_app *qwer=new hps_ecal_scalers_app(gClient->GetRoot(), 1500, 450, scalerType);
    
    qwer->doLogScale=doLogScale;
    qwer->updatePeriod=updatePeriod;
    qwer->enableButtons=enableButtons;
    qwer->doAccumulate=doAccumulate;

    asdf.Run();
    
    return 0;
}
