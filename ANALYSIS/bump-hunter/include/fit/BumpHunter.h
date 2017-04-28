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
         * Fit the given histogram in the range window_start, window_end.
         *
         * @param histogram The histogram to fit.
         * @param window_start
         * @param window_end
         * @param window_step 
         */
        //std::map<double, HpsFitResult*> fitWindow(TH1* histogram, double window_start, double window_end, double window_step);

        /**
         */
        HpsFitResult* fitWindow(TH1* histogram, double ap_hypothesis, bool bkg_only);


        /**
         */
        HpsFitResult* fitWindow(RooDataHist* data, double ap_hypothesis, bool bkg_only, bool const_sig = false);
        
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
        void calculatePValue(RooDataHist* data, HpsFitResult* result, double ap_hypothesis); 


        /** Fit using a background only model. */
        void fitBkgOnly();

        /** Set the histogram bounds. */
        void setBounds(double low_bound, double high_bound); 

        /** Enable/disable debug */
        void setDebug(bool debug = true) { this->debug = debug; };

        /** Write the fit results to a text file */
        void writeResults(bool write_results = true) { _write_results = write_results; }; 

        void getUpperLimit(TH1* histogram, HpsFitResult* result, double ap_mass);

        void getUpperLimit(RooDataHist* data, HpsFitResult* result, double ap_mass);

        std::vector<RooDataHist*> generateToys(TH1* histogram, double n_toys, double ap_hypothesis);

        std::vector<HpsFitResult*> runToys(TH1* histogram, double n_toys, double ap_hypothesis);
         
    private: 

        /**
         * Get the HPS mass resolution at the given mass.  The functional form 
         * of the mass resolution was determined using MC.
         *
         * @param mass The mass of interest.
         * @return The mass resolution at the given mass.
         */
        inline double getMassResolution(double mass) { 
            //return -6.166*mass*mass*mass + 0.9069*mass*mass -0.00297*mass + 0.000579; 
            return -6.782*mass*mass*mass + 0.9976*mass*mass -0.003266*mass + 0.0006373; 
        };
  
        /** 
         * Print debug statement.
         *
         * @param message Debug statement to print.
         */
        void printDebug(std::string message); 
         

        /** Reset the fit parameters to their initial values. */ 
        void resetParameters(); 

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

        /** 
         * The lower bound of the histogram. This is determined by searching
         * for the first filled bin.
         */
        double lower_bound{0};

        /** 
         * The upper bound of the histogram. This is determined by searching
         * for the last filled bin.
         */
        double upper_bound{0};

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

        /** Debug flag */
        bool debug{false};

        /** Write the results to a file. */
        bool _write_results{false};
};

#endif // __BUMP_HUNTER_H__
