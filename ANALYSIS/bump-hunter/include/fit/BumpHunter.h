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
#include <cmath>
#include <cstdio> 
#include <exception>
#include <fstream>
#include <map>
#include <ctime>
#include <vector>

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
#include <RooRandom.h>
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
         * Perform a search for a resonance at the given mass hypothesis.
         *
         * @param histogram Histogram containing the mass spectrum that will be
         *                  used to search for a resonance.
         * @param mass_hypothesis The mass of interest.
         */
        HpsFitResult* performSearch(TH1* histogram, double mass_hypothesis); 

        /** 
         * Given the mass of interest, setup the window parameters and 
         * initialize the fit parameters.  This includes setting the size of the
         * window and the window edges as well as estimating the initial value
         * of some fit parameters.
         *
         * @param histogram Histogram containing the mass spectrum that will be
         *                  used to search for a resonance.
         * @param mass_hypothesis The mass of interest.
         */
        void initialize(TH1* histogram, double &mass_hypothesis); 

        /**
         * Fit the given histogram. If a range is specified, only fit within the 
         * range of interest.
         *
         * @param data The RooFit histogram to fit.
         * @param migrad_only If true, only run migrad.
         * @param range_name The range to fit.
         
         */        
        HpsFitResult* fit(RooDataHist* data, std::string range_name); 
   
        /**
         *
         */
        void calculatePValue(HpsFitResult* result); 


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

        /** Get the signal upper limit. */
        void getUpperLimit(RooDataHist* data, std::string range_name, HpsFitResult* result); 

        /** Reset the fit parameters to their initial values. */ 
        void resetParameters(); 
        
        /** Reset the fit parameters to their initial values. */ 
        void resetParameters(HpsFitResult* result); 

        /** */
        //std::vector<HpsFitResult*> generateToys(double n_toys);
        std::vector<TH1*> generateToys(TH1* histogram, double n_toys);

    private: 

        /**
         * Get the HPS mass resolution at the given mass.  The functional form 
         * of the mass resolution was determined using MC.
         *
         * @param mass The mass of interest.
         * @return The mass resolution at the given mass.
         */
        inline double getMassResolution(double mass) { 
            //return -6.2*mass*mass*mass + 0.91*mass*mass - 0.00297*mass + 0.000579; 
            //return 0.0389938364847*mass - 0.0000713783511061; // ideal
            //return 0.0501460737193*mass - 0.0000917925595224; // scaled to moller mass from data
            return 0.0532190838657*mass - 0.0000922283032152; // scaled to moller mass + sys
        };

        /**
         *
         */
        double correctMass(double mass); 
  
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


        double getFitChi2(RooDataHist* data); 

        /**
         *
         */
        FitPrinter* printer{new FitPrinter()}; 

        /** A mapping between a variable name and its corresponding RooRealVar. */
        std::map <std::string, RooRealVar*> variable_map;

        std::map <std::string, double> default_values; 
        
        std::map <std::string, double> default_errors; 

        /** Background only fit result. */
        HpsFitResult* bkg_only_result_{nullptr};

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
    
        /** Mass variable. */
        RooRealVar* mass_{nullptr};

        RooDataHist* data_{nullptr};

        /** Output file stream */
        std::ofstream* ofs;

        /** Name of the range used by the fit. */
        std::string range_name_{""}; 

        /** 
         * Size of the background window used to calculate the amount of 
         * bkg/mev.
         */
        double _bkg_window_size{-9999};

        /** Total number of events withing the background window. */
        double _bkg_window_integral{-9999}; 

        /** The lower bound of the histogram. */
        //double _lower_bound{-9999};
        double _lower_bound{0.014};

        /** The upper bound of the histogram. */
        //double _upper_bound{-9999};
        double _upper_bound{0.115};

        double integral_{0}; 

        /** 
         * Resolution multiplicative factor used in determining the fit window 
         * size.
         */
        double _res_factor{13}; 

        /** Size of the background window that will be used to fit. */
        double _window_size{0};

        /** The total number of bins */
        int bins_{0};

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

        double window_start_{0}; 

        double window_end_{0};

        double mass_hypothesis_{0};  
};

#endif // __BUMP_HUNTER_H__
