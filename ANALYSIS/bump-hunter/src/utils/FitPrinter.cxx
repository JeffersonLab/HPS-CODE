/**
 * @file FitPrinter.cxx
 * @brief Class used to print a RooFit result to a file.
 * @author Omar Moreno
 *         SLAC National Accelerator Laboratory 
 */

#include "FitPrinter.h"

FitPrinter::FitPrinter() {
}

FitPrinter::~FitPrinter() {
    delete _canvas;
}

void FitPrinter::print(RooPlot* plot, RooDataHist* data, RooAddPdf* model, std::string range) {

    data->plotOn(plot);
    model->plotOn(plot,
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str())); 
    model->plotOn(plot, 
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()),  
                  RooFit::Components("bkg"), 
                  RooFit::LineStyle(kDashed),
                  RooFit::LineColor(kGreen));
    model->plotOn(plot, 
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()),  
                  RooFit::Components("signal"), 
                  RooFit::LineStyle(kDashed),
                  RooFit::LineColor(kRed));

    plot->Draw();
    std::string output = range + "fit.png"; 
    _canvas->SaveAs(output.c_str());
}
