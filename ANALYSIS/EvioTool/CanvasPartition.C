#ifndef __CANVASPARTITION__
#define __CANVASPARTITION__
#include "TROOT.h"
#include "TCanvas.h"
#include "TPad.h"
#include <vector>


// vector<TPad*> ordered like this: (really should fix this)
// 2 5
// 1 4
// 0 3
//

// TCanvas::Divide convention:
// 1 2 
// 3 4
// 5 6

std::vector <TPad*> CanvasPartition(TCanvas *C,const Int_t Nx,const Int_t Ny,
                     const double lMargin = 0.15, const double rMargin = 0.05,
                     const double bMargin = 0.15, const double tMargin = 0.05)
{
    std::vector <TPad*> pad;
   if (!C) return pad;

   // Setup Pad layout:
   const double vSpacing = 0.0;
   const double vStep  = (1.- bMargin - tMargin - (Ny-1) * vSpacing) / Ny;

   const double hSpacing = 0.0;
   const double hStep  = (1.- lMargin - rMargin - (Nx-1) * hSpacing) / Nx;

   double vposd,vposu=0,vmard,vmaru,vfactor;
   double hposl,hposr=0,hmarl,hmarr,hfactor;

   int npads=0;

   for (Int_t i=0;i<Nx;i++) {

      if (i==0) {
         hposl = 0.0;
         hposr = lMargin + hStep;
         hfactor = hposr-hposl;
         hmarl = lMargin / hfactor;
         hmarr = 0.0;
      } else if (i == Nx-1) {
         hposl = hposr + hSpacing;
         hposr = hposl + hStep + rMargin;
         hfactor = hposr-hposl;
         hmarl = 0.0;
         hmarr = rMargin / (hposr-hposl);
      } else {
         hposl = hposr + hSpacing;
         hposr = hposl + hStep;
         hfactor = hposr-hposl;
         hmarl = 0.0;
         hmarr = 0.0;
      }

      for (Int_t j=0;j<Ny;j++) {

         if (j==0) {
            vposd = 0.0;
            vposu = bMargin + vStep;
            vfactor = vposu-vposd;
            vmard = bMargin / vfactor;
            vmaru = 0.0;
         } else if (j == Ny-1) {
            vposd = vposu + vSpacing;
            vposu = vposd + vStep + tMargin;
            vfactor = vposu-vposd;
            vmard = 0.0;
            vmaru = tMargin / (vposu-vposd);
         } else {
            vposd = vposu + vSpacing;
            vposu = vposd + vStep;
            vfactor = vposu-vposd;
            vmard = 0.0;
            vmaru = 0.0;
         }

         C->cd(0);

         char name[16];
         sprintf(name,"pad_%i_%i",i,j);
         TPad* padtmp = (TPad*) gROOT->FindObject(name);
         if (padtmp) delete padtmp;
         pad.push_back(new TPad(name,"",hposl,vposd,hposr,vposu));
         pad[npads]->SetLeftMargin(hmarl);
         pad[npads]->SetRightMargin(hmarr);
         pad[npads]->SetBottomMargin(vmard);
         pad[npads]->SetTopMargin(vmaru);

         pad[npads]->SetFrameBorderMode(0);
         pad[npads]->SetBorderMode(0);
         pad[npads]->SetBorderSize(0);

         pad[npads]->Draw();
         npads++;
      }
   }
   return pad;
}
#endif
