/**
 * @file FitPrinter.h
 * @brief Class used to print a RooFit result to a file.
 * @author Omar Moreno
 *         SLAC National Accelerator Laboratory 
 */

#ifndef __FIT_PRINTER_H__
#define __FIT_PRINTER_H__

//----------//
//   ROOT   //
//----------//
#include <TCanvas.h>
#include <TAxis.h>
#include <TColor.h>

//------------//
//   RooFit   //
//------------//
#include <RooAddPdf.h>
#include <RooDataHist.h>
#include <RooHist.h>
#include <RooPlot.h>
#include <RooRealVar.h>

class FitPrinter { 
    
    public: 

        /** Default constructor */
        FitPrinter();

        /** Destructor */
        ~FitPrinter();

        /** Print the resulting fit and save it to the specified output path. */
        void print(RooRealVar* var, RooDataHist* data, RooAddPdf* model, 
                   std::string range, std::string output_path, int n_bins); 

    private:
        
        /** ROOT canvas */   
        TCanvas* _canvas{new TCanvas{"canvas", "canvas", 900, 800}};
        
        /** Pad used to draw fit. */
        TPad* _main_pad{new TPad{"main_pad", "main_pad", 0.0, 0.2, 1.0, 1.0}}; 
        
        /** Pad used to draw residuals. */
        TPad* _res_pad{new TPad{"main_pad", "main_pad", 0.0, 0.0, 1.0, 0.2}}; 

};  // FitPrinter

#endif // __FIT_PRINTER_H__
