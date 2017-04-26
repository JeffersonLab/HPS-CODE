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

void FitPrinter::print(RooRealVar* var, RooDataHist* data, RooAddPdf* model, 
                       std::string range, std::string output_path) {

    RooPlot* plot = var->frame(); 
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

    std::cout << "[ FitPrinter ]: Saving file to: " << output_path << std::endl;
    _canvas->SaveAs(output_path.c_str());
}
