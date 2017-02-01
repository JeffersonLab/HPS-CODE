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

    // Parse all the command line arguments.  If there are no valid command
    // line arguments passed, print the usage and exit the application
    static struct option long_options[] = {
        {"res_factor", required_argument, 0, 'f'},
        {"file_name",  required_argument, 0, 'i'},
        {"help",       no_argument,       0, 'h'},
        {"log",        no_argument,       0, 'l'},
		{"debug",      no_argument,       0, 'd'},
		{"exp",        no_argument,       0, 'e'},
        {"mass",       required_argument, 0, 'm'}, 
        {"name",       required_argument, 0, 'n'}, 
        {"output",     required_argument, 0, 'o'},
        {"poly",       required_argument, 0, 'p'},
        {"toys",       required_argument, 0, 't'},
        {0, 0, 0, 0}
    };
    
    int option_index = 0;
    int option_char; 
    while ((option_char = getopt_long(argc, argv, "f:i:hldem:n:o:p:t:", long_options, &option_index)) != -1) {
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

    // Open the ROOT file.  If any problems are encountered, warn the user
    // and exit the application.
    TFile* file = new TFile(file_name.c_str());
    if (file->IsZombie()) { 
        cerr << "[ EVALUATOR ]: Failed to open file " << file_name.c_str(); 
        return EXIT_FAILURE;
    }

    TH1* histogram = (TH1*) file->Get(name.c_str()); 

    // Create a new Bump Hunter instance and set the given properties.
    BumpHunter* bump_hunter = new BumpHunter(poly_order, res_factor, exp_poly);
    if (log_fit) bump_hunter->writeResults();  
    if (debug) bump_hunter->setDebug(debug);
    // Build the string that will be used for the results file name
    if (output_file.empty()) { 
        output_file = "fit_result_mass" + to_string(mass_hypo) + "_order" +  to_string(poly_order) + ".root"; 
    }

    // Create a new flat ntuple and define the variables it will encapsulate.
    FlatTupleMaker* tuple = new FlatTupleMaker(output_file, "results"); 

    tuple->addVariable("ap_mass"); 
    tuple->addVariable("sig_yield");
    tuple->addVariable("sig_yield_err");
    tuple->addVariable("bkg_yield"); 
    tuple->addVariable("bkg_yield_err");
    tuple->addVariable("bkg_total");
    tuple->addVariable("bkg_window_size");  
    tuple->addVariable("nll");
    tuple->addVariable("invalid_nll"); 
    tuple->addVariable("minuit_status");
    tuple->addVariable("edm");
    tuple->addVariable("q0"); 
    tuple->addVariable("p_value"); 
    tuple->addVariable("upper_limit");
    tuple->addVariable("window_size"); 
    
    tuple->addVector("toy_upper_limits");
    tuple->addVector("toy_sig_yield");  
    tuple->addVector("toy_sig_yield_err");  
    tuple->addVector("toy_bkg_yield");  
    tuple->addVector("toy_bkg_yield_err");  


    HpsFitResult* fit_result = bump_hunter->fitWindow(histogram, mass_hypo, false);
     
    // Retrieve all of the result of interest. 
    double bkg_yield = ((RooRealVar*) fit_result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getVal();
    double bkg_yield_error = ((RooRealVar*) fit_result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getError();
    double nll = fit_result->getRooFitResult()->minNll();
    double invalid_nll = fit_result->getRooFitResult()->numInvalidNLL();
    double minuit_status = fit_result->getRooFitResult()->status();
    double edm = fit_result->getRooFitResult()->edm(); 
            
    // Set the values of the results that will be written to the ntuple.
    tuple->setVariableValue("ap_mass", mass_hypo);  
    tuple->setVariableValue("bkg_yield", bkg_yield);  
    tuple->setVariableValue("bkg_yield_error", bkg_yield_error);
    tuple->setVariableValue("bkg_total", fit_result->getBkgTotal()); 
    tuple->setVariableValue("bkg_window_size", fit_result->getBkgWindowSize()); 
    tuple->setVariableValue("nll", nll); 
    tuple->setVariableValue("invalid_nll", invalid_nll); 
    tuple->setVariableValue("minuit_status", minuit_status);
    tuple->setVariableValue("edm", edm); 
    tuple->setVariableValue("window_size", fit_result->getWindowSize());  

        
    // If this isn't a background only fit evaluation, skip it.
    double signal_yield = ((RooRealVar*) fit_result->getRooFitResult()->floatParsFinal().find("signal yield"))->getVal();
    double signal_yield_error = ((RooRealVar*) fit_result->getRooFitResult()->floatParsFinal().find("signal yield"))->getError();
    tuple->setVariableValue("sig_yield", signal_yield);  
    tuple->setVariableValue("sig_yield_err", signal_yield_error);
    tuple->setVariableValue("p_value", fit_result->getPValue());
    tuple->setVariableValue("q0", fit_result->getQ0()); 
    tuple->setVariableValue("upper_limit", fit_result->getUpperLimit());

    // Fill the ntuple
    tuple->fill(); 

    // Delete the fit results from memory
    delete fit_result;  

    // Close the ntuple
    tuple->close(); 

    delete bump_hunter; 
    delete file;
}
