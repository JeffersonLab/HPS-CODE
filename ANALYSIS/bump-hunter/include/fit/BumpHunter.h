/**
 * @file BumpHunter.h
 * @brief
 * @author Omar Moreno <omoreno1@ucsc.edu>
 *         Santa Cruz Institute for Particle Physics
 *         University of California, Santa Cruz
 * @date January 14, 2015
 */

#ifndef __BUMP_HUNTER_H__
#define __BUMP_HUNTER_H__

//----------------//   
//   C++ StdLib   //
//----------------//  
#include <cstdio> 
#include <vector>
#include <map>
#include <fstream>
#include <cmath>
#include <exception>

//----------//
//   ROOT   //
//----------//   
#include <TH1.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TFile.h>
#include <Math/ProbFunc.h>

//------------//
//   RooFit   //
//------------//
#include <RooAddPdf.h>
#include <RooArgList.h>
#include <RooDataHist.h>
#include <RooExponential.h>
#include <RooFitResult.h>
#include <RooGaussian.h>
#include <RooChebychev.h>
#include <RooMinuit.h>
#include <RooPlot.h>
#include <RooProfileLL.h>
#include <RooProdPdf.h>
#include <RooRealVar.h>


//---//
#include <HpsFitResult.h>
#include <FitPrinter.h>

class BumpHunter {

    public:

        /** Enum constants used to denote the different background models. */
        enum BkgModel { 
            POLY     = 0,
            EXP_POLY = 1,
            EXP_POLY_X_POLY = 2,
        };

        /** Default Constructor */
        BumpHunter(BkgModel model, int poly_order, int res_factor);

        /** Destructor */
        ~BumpHunter();

        /**
         */
        HpsFitResult* fitWindow(TH1* histogram, double mass_hypothesis, bool bkg_only, bool const_sig = false);

        
        /**
         * Fit the given histogram. If a range is specified, only fit within the 
         * range of interest.
         *
         * @param data The RooFit histogram to fit.
         * @param migrad_only If true, only run migrad.
         * @param range_name The range to fit.
         */        
        HpsFitResult* fit(RooDataHist* data, bool migrad_only, std::string range_name); 
    
        /**
         *
         */
        void calculatePValue(TH1* histogram, HpsFitResult* result, double ap_hypothesis); 


        /** Fit using a background only model. */
        void fitBkgOnly();

        /** Set the histogram bounds. */
        void setBounds(double low_bound, double high_bound); 

        /** Enable/disable debug */
        void enableDebug(bool debug = true) { this->debug = debug; };

        /** Enable batch running. */
        void runBatchMode(bool batch = true) { _batch = batch; };

        /** Write the fit results to a text file */
        void writeResults(bool write_results = true) { _write_results = write_results; }; 

        void getUpperLimit(TH1* histogram, HpsFitResult* result, double ap_mass);

        std::vector<RooDataHist*> generateToys(TH1* histogram, double n_toys, double ap_hypothesis);

        std::vector<HpsFitResult*> runToys(TH1* histogram, double n_toys, double ap_hypothesis);
         
        /** Reset the fit parameters to their initial values. */ 
        void resetParameters(); 

    private: 

        /**
         * Get the HPS mass resolution at the given mass.  The functional form 
         * of the mass resolution was determined using MC.
         *
         * @param mass The mass of interest.
         * @return The mass resolution at the given mass.
         */
        inline double getMassResolution(double mass) { 
            //return 0.0389938364847*mass - 0.0000713783511061; // ideal
            //return 0.0501460737193*mass - 0.0000917925595224; // scaled to moller mass from data
            return 0.0544084899854*mass - 0.0000995949270818; // target position sys +8%
        };
  
        /** 
         * Print debug statement.
         *
         * @param message Debug statement to print.
         */
        void printDebug(std::string message); 
         
        /**
         *
         */
        void getChi2Prob(double min_nll_null, double min_nll, double &q0, double &p_value); 

        
        /**
         *
         */
        FitPrinter* printer{new FitPrinter}; 

        /** A mapping between a variable name and its corresponding RooRealVar. */
        std::map <std::string, RooRealVar*> variable_map;

        std::map <std::string, double> default_values; 
        
        std::map <std::string, double> default_errors; 

        /** Signal + bkg model */
        RooAddPdf* comp_model;  

        /** Bkg only model */
        RooAddPdf* bkg_model;

        /** */
        RooAddPdf* _model; 

        /** Signal PDF */ 
        RooGaussian* signal;

        /** Bkg PDF */
        RooAbsPdf* bkg;

        /** */ 
        RooArgList arg_list;

        /** Output file stream */
        std::ofstream* ofs;

        /** The lower bound of the histogram. */
        //double _lower_bound{-9999};
        double _lower_bound{0.014};

        /** The upper bound of the histogram. */
        //double _upper_bound{-9999};
        double _upper_bound{0.115};

        /** Maximum size of the window */
        double _max_window_size{1.0};

        /** 
         * Resolution multiplicative factor used in determining the fit window 
         * size.
         */
        double _res_factor{13}; 

        /** Size of the background window that will be used to fit. */
        double window_size;

        /** The total number of bins */
        int bins{2000};

        /** Polynomial order used to model the background. */
        int _poly_order;

        /** 
         * Flag denoting if application should run in batch mode.  If set to 
         * true, plots aren't generated and fit results aren't logged.
         */
        bool _batch{false}; 

        /** Debug flag */
        bool debug{false};

        /** Write the results to a file. */
        bool _write_results{false};
};

#endif // __BUMP_HUNTER_H__
