// getGainCOSMIC2019.C
//
// Adapted from getGain() in cosmicAnalysis.C (Holly Szumila-Vance) to fit
// against the per-crystal MIP-signal histograms that hps-java's
// CosmicCalibrationInt driver (org.hps.analysis.ecal.cosmic) writes directly
// during EvioToLcio + CosmicCalibration.lcsim reconstruction, instead of
// against a locally-produced mipSigCut.root from geoCut()/countingCut().
//
// Those histograms are named "Cry_sel<N>_<x>_<y>" (N=1..5, x not zero-padded)
// rather than cosmicAnalysis.C's own "Cry_%.2d_%d" convention, and live
// directly inside the per-run/per-job ROOT files produced by the COSMIC2019
// production pipeline (COSMIC2019/data/swif.py + doMerge.csh), not in a file
// literally named mipSigCut.root.
//
// cosmicAnalysis.C's own geoCut()/countingCut() step is not needed here:
// the selection is already applied by the Java driver. This script only
// reproduces the getGain() fitting step.
//
// Differences from the original getGain():
//  - infile / histogram-name prefix / output tag are parameters, not hardcoded
//  - skips crystals with < 20 histogram entries (unstable langaus fit otherwise)
//  - MPV is explicitly sentinel-initialized to -999 before any fit attempt,
//    fixing a latent bug in the original where a zero-initialized MPV array
//    combined with the ">-900" success check would silently treat a MISSING
//    histogram as a valid MPV=0 fit, producing a divide-by-zero gain
//  - each crystal's fit is saved as its own PNG in a subdirectory
//    (output/plots_<tag>/Cry_<x>_<y>.png) instead of a combined multi-page
//    PDF plus individual .C dumps
//
// Usage (from this directory, so "dependency/" and "output/" resolve):
//   root -l -b -q 'getGainCOSMIC2019.C+("path/to/file.root","Cry_sel1","sixthTest_9179")'

// Don't change these (needed by dependency/functions.C, mirrors cosmicAnalysis.C):
#define NX 46
#define NY 10
#define NSAMP 100
#define NR 11
#define ADC2V 0.25

#include "TH1.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TNtuple.h"
#include "TPad.h"
#include "TTree.h"
#include "TMath.h"
#include "TF1.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TDirectory.h"
#include "TPaveText.h"
#include "TString.h"
#include "TSystem.h"
#include <fstream>
#include "dependency/chainfilelist.C"
#include "dependency/MyRootUtil.C"
#include "dependency/ProgressMeter.C"
#include "dependency/langaus.C"
#include "dependency/functions.C"

void getGainCOSMIC2019(const char* infile, const char* selPrefix="Cry_sel1", const char* tag="test")
{
    TFile *f = new TFile(infile);
    if (!f || f->IsZombie()) {
        std::cerr << "Cannot open " << infile << std::endl;
        return;
    }

    TString plotdir = Form("output/plots_%s", tag);
    gSystem->mkdir(plotdir, kTRUE);

    Double_t MPV[NX][NY]={};
    Double_t ENTRIES[NX][NY]={};
    TF1 *lfit[NX][NY];
    TH1D *mipSigCut[NX][NY];

    TCanvas *canvas = new TCanvas("canvas","cosmic fits", 700, 700);
    canvas->SetFillColor(0);
    canvas->SetBorderMode(0);
    canvas->SetBorderSize(0);
    canvas->SetFrameFillColor(0);
    canvas->SetFrameBorderMode(0);

    gROOT->SetBatch(true);

    int nAttempted = 0;
    int nFit = 0;

    for (int jy=0; jy<NY; jy++)
    {
        for (int jx=0; jx<NX; jx++)
        {
            MPV[jx][jy] = -999;
            if (ishole(jx,jy)) continue;

            TString hname = Form("%s_%d_%d", selPrefix, jx, jy);
            mipSigCut[jx][jy] = (TH1D*)f->Get(hname);
            if (!mipSigCut[jx][jy]) continue;

            ENTRIES[jx][jy] = mipSigCut[jx][jy]->GetEntries();
            if (mipSigCut[jx][jy]->GetEntries() < 20) continue;  // too few for a stable langaus fit

            nAttempted++;
            mipSigCut[jx][jy]->GetXaxis()->SetRange(10,70);

            Double_t fr[2];
            Double_t sv[4], pllo[4], plhi[4], fp[4], fpe[4];
            fr[0] = 0.3*mipSigCut[jx][jy]->GetMean();
            fr[1] = 3.0*mipSigCut[jx][jy]->GetMean();

            pllo[0]=0.5; pllo[1]=15.0; pllo[2]=0.1*mipSigCut[jx][jy]->GetEntries(); pllo[3]=1;
            plhi[0]=5.0; plhi[1]=40.0; plhi[2]=0.75*mipSigCut[jx][jy]->GetEntries(); plhi[3]=7.0;
            sv[0]=1.8; sv[1]=mipSigCut[jx][jy]->GetMean(); sv[2]=0.5*mipSigCut[jx][jy]->GetEntries(); sv[3]=2.0;

            Double_t chisqr;
            Int_t ndf;
            lfit[jx][jy] = langaufit(mipSigCut[jx][jy],fr,sv,pllo,plhi,fp,fpe,&chisqr,&ndf);

            Double_t SNRPeak, SNRFWHM;
            langaupro(fp,SNRPeak,SNRFWHM);

            gStyle->SetOptStat(1111);
            gStyle->SetOptFit(111);
            gStyle->SetLabelSize(0.03,"x");
            gStyle->SetLabelSize(0.03,"y");
            mipSigCut[jx][jy]->GetXaxis()->SetRange(8,70);
            mipSigCut[jx][jy]->GetXaxis()->SetTitle("Peak in mV, ped subtracted");
            mipSigCut[jx][jy]->GetYaxis()->SetTitle("Events");
            mipSigCut[jx][jy]->Draw();
            lfit[jx][jy]->Draw("lsame");
            MPV[jx][jy] = SNRPeak;

            TPaveText *t = new TPaveText(0.1,0.8,0.3,0.9,"brNDC");
            t->AddText(Form("Peak : %.3f",MPV[jx][jy]));
            t->AddText(Form("Gain: %.3f",18.3/(MPV[jx][jy]*4)));
            t->Draw("lsame");
            canvas->Update();
            canvas->SaveAs(Form("%s/Cry_%d_%d.png", plotdir.Data(), jx, jy));

            nFit++;
        }
    }

    std::cout << "Attempted fits: " << nAttempted << "  Successful (non-crash) fits: " << nFit << std::endl;
    std::cout << "Per-crystal plots written to " << plotdir << "/" << std::endl;

    std::ofstream gainsOut(Form("output/gains4db_%s.txt", tag));
    std::ofstream gainsDAQ(Form("output/gains4DAQconversion_%s.txt", tag));
    gainsOut << "ecal_channel_id, gain" << std::endl;
    for (int ny=0; ny<NY; ny++)
    {
        for (int nx=0; nx<NX; nx++)
        {
            if (ishole(nx,ny)) continue;
            if (MPV[nx][ny] <= -900) continue;
            float val = 18.3/(MPV[nx][ny]*4);
            int dbid = xy2dbid(nx,ny);
            gainsOut << dbid << "," << val << std::endl;
            gainsDAQ << nx << "\t" << ny << "\t" << val << std::endl;
        }
    }
    gainsOut.close();
    gainsDAQ.close();

    std::cout << "Wrote output/gains4db_" << tag << ".txt and output/gains4DAQconversion_" << tag << ".txt" << std::endl;
}
