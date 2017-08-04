/**
 * @file FitPrinter.cxx
 * @brief Class used to print a RooFit result to a file.
 * @author Omar Moreno
 *         SLAC National Accelerator Laboratory 
 */

#include "FitPrinter.h"

FitPrinter::FitPrinter() {
    //_canvas->Divide(1, 2);
    _main_pad->Draw();
    _res_pad->Draw(); 
}

FitPrinter::~FitPrinter() {
    delete _canvas;
}

void FitPrinter::print(RooRealVar* var, RooDataHist* data, RooAddPdf* model, 
                       std::string range, std::string output_path, int n_bins, double mass_hypothesis, bool bkg_only) {

    std::cout << "[ FitPrinter ]: Bins: " << n_bins << std::endl;
    gDirectory->mkdir("plots");
    gDirectory->cd("plots");
    RooPlot* plot = var->frame(); 
    data->plotOn(plot, 
                 RooFit::MarkerSize(.4),
                 RooFit::MarkerColor(kAzure+2),
                 RooFit::LineColor(kAzure+2));
    model->plotOn(plot,
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()), 
                  RooFit::LineColor(kRed + 2)); 
    model->plotOn(plot, 
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()),  
                  RooFit::Components("bkg"), 
                  RooFit::LineStyle(kDashed),
                  RooFit::LineColor(kGreen + 2));
    model->plotOn(plot, 
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()),  
                  RooFit::Components("signal"), 
                  RooFit::LineColor(kOrange+10));
    plot->GetYaxis()->SetTitleOffset(1.6);

    plot->SetTitle(Form("Invariant Mass (A' = %.3f MeV) %s", mass_hypothesis*1000, bkg_only ? " (background-only)" : ""));
    plot->SetName(Form("Invariant_Mass_%.3f_MeV%s", mass_hypothesis*1000, bkg_only ? "_bkg_only" : ""));

    RooPlot* tmp_plot = var->frame(); 
    data->plotOn(tmp_plot, RooFit::Binning(int(n_bins/4)));
    model->plotOn(tmp_plot, 
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()),  
                  RooFit::Components("bkg"), 
                  RooFit::LineStyle(kDashed),
                  RooFit::LineColor(kGreen));

    RooHist* residuals = tmp_plot->residHist();
    tmp_plot->Delete();
    residuals->SetMarkerSize(.4);

    RooPlot* res_plot = var->frame();
    res_plot->addPlotable(residuals, "P");
    /*model->plotOn(res_plot, 
                  RooFit::Range(range.c_str()), 
                  RooFit::NormRange(range.c_str()),  
                  RooFit::Components("signal"), 
                  RooFit::LineStyle(kDashed),
                  RooFit::LineColor(kRed));*/
    res_plot->SetMinimum(-1000);
    res_plot->SetMaximum(1000);
    res_plot->SetTitle(Form("Residuals (A' = %.3f MeV) %s", mass_hypothesis*1000, mass_hypothesis*1000, bkg_only ? " (background-only)" : ""));
    res_plot->SetName(Form("Residuals_%.3f_MeV%s", mass_hypothesis*1000, bkg_only ? "_bkg_only" : ""));
    res_plot->GetYaxis()->SetTitle("Residual");
    res_plot->GetYaxis()->SetTitleSize(0.05);
    res_plot->GetYaxis()->SetLabelSize(0.05);
    res_plot->GetYaxis()->SetTitleOffset(1);
    
    _main_pad->cd();
    plot->Draw();

    _res_pad->cd(); 
    res_plot->Draw(); 

    std::cout << "[ FitPrinter ]: Saving file to: " << output_path << std::endl;

    gDirectory->cd("..");
    _canvas->SaveAs(output_path.c_str());
}
