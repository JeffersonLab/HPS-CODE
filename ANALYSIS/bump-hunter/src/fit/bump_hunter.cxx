/**
 *
 */

//------------------//
//--- C++ StdLib ---//
//------------------//
#include <cstdlib>
#include <iostream>
#include <getopt.h>
#include <string>
#include <exception>

#include <TFile.h>
#include <TH1.h>
#include <RooFitResult.h>

#include <RootFileReader.h>
#include <BumpHunter.h>
#include <FlatTupleMaker.h>

using namespace std;

int main(int argc, char **argv) { 

    /** Name of file containing the histogram that will be fit. */
    string file_name{""};

    /** The name of the histogram to fit. */
    string name{""};

    /* The path to where the results will be saved. */
    string output_file{""};

    /** The signal hypothesis to use in the fit. */
    double mass_hypo = 0; 

    /** The beam energy (default is 1.056 GeV).  Omar fit the mass resolutions using 1.056 GeV
     MC.  If the beam energy is different than this, then use the resolution
     for mass*(1.056/beam energy) */
    double beam_energy = 1.056;

    /** */
    int res_factor{13};

    /** Polynomial order to use to model the background. */
    int poly_order = 7;

    /** 
     * The number of toys to run for each fit. If toys = 0, the generation 
     * of toys will be skipped.
     */
    int toys = 0;

    /** Flag indicating whether to log all fit results or not. */ 
    bool log_fit = false; 

    /** Flag indicating whether or not to debug*/
    bool debug = false;
    /** Flag indicating whether or not to use e^(poly)*/
    bool exp_poly = false;
    /** Flag indicating whether or not to use e^(-k*x)*poly(x)*/
    bool exp_times_poly = false;
    
    /** step size to use (if performing fits on a grid of mass hypotheses).  0 = no looping*/
    double mass_step = 0;
    /** maximum mass hypothesis to perform fit on.  0 = no looping.*/
    double max_mass_hypo = 0;
    
    // Parse all the command line arguments.  If there are no valid command
    // line arguments passed, print the usage and exit the application
    static struct option long_options[] = {
        {"res_factor", required_argument, 0, 'f'},
        {"file_name",  required_argument, 0, 'i'},
        {"help",       no_argument,       0, 'h'},
        {"log",        no_argument,       0, 'l'},
		{"debug",      no_argument,       0, 'd'},
		{"exp",        no_argument,       0, 'e'},
		{"beam_energy",required_argument, 0, 'b'},
        {"mass",       required_argument, 0, 'm'}, 
        {"name",       required_argument, 0, 'n'}, 
        {"output",     required_argument, 0, 'o'},
        {"poly",       required_argument, 0, 'p'},
        {"toys",       required_argument, 0, 't'},
        {"mass_step", required_argument, 0, 's'},
        {"max_mass_hypo",required_argument, 0, 'x'},
        {0, 0, 0, 0}
    };
    
    int option_index = 0;
    int option_char; 
    while ((option_char = getopt_long(argc, argv, "f:i:hldecb:m:n:o:p:t:s:x:", long_options, &option_index)) != -1) {
        switch(option_char) {
            case 'f': 
                res_factor = atoi(optarg); 
                break;
            case 'i': 
                file_name = optarg;
                break;
            case 'h':
                return EXIT_SUCCESS; 
            case 'l': 
                log_fit = true;
                break;
            case 'd':
                debug = true;
                break;
            case 'e':
            	exp_poly = true;
            	break;
            case 'c':
				exp_times_poly = true;
				break;
            case 'b':
            	beam_energy = atof(optarg);
            	break;
            case 'm': 
                mass_hypo = atof(optarg); 
                break;
            case 'n': 
                name = optarg; 
                break; 
            case 'o':
                output_file = optarg;
                break;
            case 'p': 
                poly_order = atoi(optarg);
                break;
            case 't':
                toys = atoi(optarg);
                break;
            case 's':
            	mass_step = atof(optarg);
            	break;
            case 'x':
            	max_mass_hypo = atof(optarg);
            	break;
            default: 
                return EXIT_FAILURE;
        }
    }

    // Make sure a file was specified by the user.  If not, warn the user and 
    // exit the application.
    if (file_name.empty()) { 
        cerr << "[ EVALUATOR ]: Please specify a file to process." << endl;
        cerr << "[ EVALUATOR ]: Use --help for usage." << endl;
        return EXIT_FAILURE;
    }

	if(max_mass_hypo== 0 && mass_step==0){
		max_mass_hypo = 999;
		mass_step = 9999;
	} else if(max_mass_hypo ==0 || mass_step == 0){
		cerr << "[ EVALUATOR ]: Either use single-mass mode (neither -x or -s with args), or loop mode (both -x and -s args)." << endl;
        cerr << "[ EVALUATOR ]: Use --help for usage." << endl;
        return EXIT_FAILURE;
	}

    // Open the ROOT file.  If any problems are encountered, warn the user
    // and exit the application.
    TFile* file = new TFile(file_name.c_str());
    if (file->IsZombie()) { 
        cerr << "[ EVALUATOR ]: Failed to open file " << file_name.c_str(); 
        return EXIT_FAILURE;
    }

    TH1* histogram = (TH1*) file->Get(name.c_str()); 

// Create a new flat ntuple and define the variables it will encapsulate.
    FlatTupleMaker* tuple = new FlatTupleMaker(output_file, "results"); 

    tuple->addVariable("ap_mass");
    tuple->addVariable("bkg_total"); 
    tuple->addVariable("bkg_window_size");  
    tuple->addVariable("bkg_yield"); 
    tuple->addVariable("bkg_yield_err");  
    tuple->addVariable("edm");
    tuple->addVariable("invalid_nll"); 
    tuple->addVariable("minuit_status"); 
    tuple->addVariable("nll");
    tuple->addVariable("p_value");
    tuple->addVariable("poly_order");
    tuple->addVariable("q0");
    tuple->addVariable("res_factor");  
    tuple->addVariable("sig_yield");
    tuple->addVariable("sig_yield_err");
    tuple->addVariable("window_size");
    tuple->addVariable("upper_limit");
    tuple->addVariable("toy_upper_limit_median");
    tuple->addVariable("toy_upper_limit_16_pctl");
    tuple->addVariable("toy_upper_limit_84_pctl");
    tuple->addVariable("toy_sig_yield_mean");
    tuple->addVariable("toy_sig_yield_sigma");
     
    tuple->addVector("toy_bkg_yield");  
    tuple->addVector("toy_bkg_yield_err");  
    tuple->addVector("toy_edm");
    tuple->addVector("toy_invalid_nll");
    tuple->addVector("toy_minuit_status");
    tuple->addVector("toy_nll");
    tuple->addVector("toy_p_value");
    tuple->addVector("toy_q0");
    tuple->addVector("toy_sig_yield");  
    tuple->addVector("toy_sig_yield_err");  
    tuple->addVector("toy_upper_limits"); 
      

	for(;mass_hypo<=max_mass_hypo; mass_hypo+= mass_step){ //loop through the masses in a given range
    
    // Create a new Bump Hunter instance and set the given properties.
    BumpHunter* bump_hunter = new BumpHunter(poly_order, res_factor, exp_poly ? 1 : exp_times_poly ? 2 : 0);
    if (log_fit) bump_hunter->writeResults();  
    if (debug) bump_hunter->setDebug(debug);
    // Build the string that will be used for the results file name
    if (output_file.empty()) { 
        output_file = "fit_result_mass" + to_string(mass_hypo) + "_order" +  to_string(poly_order) + ".root"; 
    }

    bump_hunter->beam_energy = beam_energy;



    HpsFitResult* result = bump_hunter->fitWindow(histogram, mass_hypo, false);
     
    // Retrieve all of the result of interest. 

    double bkg_yield     = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getVal();
    double bkg_yield_err = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getError();
    double sig_yield     = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("signal yield"))->getVal();
    double sig_yield_err = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("signal yield"))->getError();
    double nll = result->getRooFitResult()->minNll();
    double invalid_nll = result->getRooFitResult()->numInvalidNLL();
    double minuit_status = result->getRooFitResult()->status();
    double edm = result->getRooFitResult()->edm(); 
    
    tuple->setVariableValue("ap_mass",          mass_hypo);  
    tuple->setVariableValue("bkg_total",        result->getBkgTotal()); 
    tuple->setVariableValue("bkg_window_size",  result->getBkgWindowSize()); 
    tuple->setVariableValue("bkg_yield",        bkg_yield);  
    tuple->setVariableValue("bkg_yield_err",    bkg_yield_err);
    tuple->setVariableValue("edm",              edm); 
    tuple->setVariableValue("invalid_nll",      invalid_nll); 
    tuple->setVariableValue("minuit_status",    minuit_status);
    tuple->setVariableValue("nll",              nll); 
    tuple->setVariableValue("p_value",          result->getPValue());
    tuple->setVariableValue("poly_order",       poly_order);
    tuple->setVariableValue("q0",               result->getQ0()); 
    tuple->setVariableValue("sig_yield",        sig_yield); 
    tuple->setVariableValue("res_factor",       res_factor);  
    tuple->setVariableValue("sig_yield_err",    sig_yield_err);
    tuple->setVariableValue("window_size",      result->getWindowSize());  
    tuple->setVariableValue("upper_limit",      result->getUpperLimit());

    std::vector<HpsFitResult*> results{bump_hunter->runToys(histogram, toys, mass_hypo)}; 

    double all_toy_upper_limits[toys];
    double sum_sig_yield = 0;
    double sum_sig_yield_sqr = 0;
    int i = 0;

    for (auto& result : results) {
   
        double bkg_yield     = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getVal();
        double bkg_yield_err = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getError();
        double sig_yield     = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("signal yield"))->getVal();
        double sig_yield_err = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("signal yield"))->getError();
        double nll           = result->getRooFitResult()->minNll();
        double invalid_nll   = result->getRooFitResult()->numInvalidNLL();
        double minuit_status = result->getRooFitResult()->status();
        double edm           = result->getRooFitResult()->edm(); 

        tuple->addToVector("toy_bkg_yield",        bkg_yield);  
        tuple->addToVector("toy_bkg_yield_err",    bkg_yield_err);
        tuple->addToVector("toy_edm",              edm); 
        tuple->addToVector("toy_invalid_nll",      invalid_nll); 
        tuple->addToVector("toy_minuit_status",    minuit_status);
        tuple->addToVector("toy_nll",              nll); 
        tuple->addToVector("toy_p_value",          result->getPValue());
        tuple->addToVector("toy_q0",               result->getQ0()); 
        tuple->addToVector("toy_sig_yield",        sig_yield); 
        tuple->addToVector("toy_sig_yield_err",    sig_yield_err);
        tuple->addToVector("toy_upper_limits",     result->getUpperLimit());
        all_toy_upper_limits[i++] = result->getUpperLimit();
        sum_sig_yield += sig_yield;
        sum_sig_yield_sqr += sig_yield*sig_yield;

    }
    std::sort(all_toy_upper_limits, all_toy_upper_limits+toys);
    double toy_median_upper_limit =
    		(toys %2 == 0) ? (all_toy_upper_limits[toys/2-1] + all_toy_upper_limits[toys/2])/2.
    				: all_toy_upper_limits[toys/2];
    double toy_upper_limit_16_percentile = all_toy_upper_limits[(int)(toys*16./100)];
    double toy_upper_limit_84_percentile = all_toy_upper_limits[(int)(toys*84./100)];
    tuple->setVariableValue("toy_upper_limit_median", toy_median_upper_limit);
    tuple->setVariableValue("toy_upper_limit_16_pctl", toy_upper_limit_16_percentile);
    tuple->setVariableValue("toy_upper_limit_84_pctl", toy_upper_limit_84_percentile);


    tuple->setVariableValue("toy_sig_yield_mean", sum_sig_yield/toys);
    tuple->setVariableValue("toy_sig_yield_sigma", sqrt((sum_sig_yield_sqr*toys-sum_sig_yield*sum_sig_yield)/(toys*(toys-1))));


    // Fill the ntuple
    tuple->fill(); 

    // Delete the fit results from memory
    delete result;  

    delete bump_hunter; 
    }
    // Close the ntuple
    tuple->close(); 

    delete file;
}
