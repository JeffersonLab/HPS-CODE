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

//------------//
//   RooFit   //
//------------//
#include <RooAddPdf.h>
#include <RooDataHist.h>
#include <RooPlot.h>

class FitPrinter { 
    
    public: 

        /** Default constructor */
        FitPrinter();

        /** Destructor */
        ~FitPrinter();

        /** Print the resulting fit */
        void print(RooPlot* plot, RooDataHist* data, RooAddPdf* model, std::string range); 

    private:
        
        /** ROOT canvas */   
        TCanvas* _canvas{new TCanvas{"canvas", "canvas", 600, 600}}; 

};  // FitPrinter

#endif // __FIT_PRINTER_H__
