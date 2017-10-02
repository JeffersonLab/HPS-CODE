/**
 * @file bump_hunter.cxx
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 * @brief Application used to scan a distribution for resonances.
 */

//----------------//
//   C++ StdLib   //
//----------------//
#include <cstdlib>
#include <iostream>
#include <getopt.h>
#include <string>
#include <exception>

//----------//
//   ROOT   //
//----------//
#include <TFile.h>
#include <TH1.h>
#include <RooFitResult.h>

//-----------------//
//   Bump Hunter   //
//-----------------//
#include "RootFileReader.h"
#include "BumpHunter.h"
#include "FlatTupleMaker.h"

using namespace std;

int main(int argc, char **argv) { 

    // PDF used to model the background.
    BumpHunter::BkgModel model{BumpHunter::BkgModel::POLY};

    // Name of file containing the histogram that will be fit. 
    string file_path{""};

    // The name of the histogram to fit. 
    string hist_name{""};

    // The path to where the results will be saved. 
    string output_file{""};

    // Range to scan histogram for a resonance.
    string range{""};

    // The signal hypothesis to use in the fit. 
    double mass_hypo = 0; 

    // The factor that determines the size of the mass window as
    //      window_size = (mass_resolution*win_factor)
    int win_factor{13};

    // Order of polynomial used to model the background. 
    int poly_order{7};

    // The number of toys to run for each fit. If toys = 0, the generation 
    // of toys will be skipped.
    int toys{0};

    // Enable debug
    bool debug{false}; 

    // Flag indicating whether to log all fit results or not. 
    bool log_fit{false};

    // Scan the whole histogram.  
    bool scan{false}; 

    // Parse all the command line arguments.  If there are no valid command
    // line arguments passed, print the usage and exit the application
    static struct option long_options[] = {
        {"exp_poly",   no_argument,       0, 'c'},
        {"debug",      no_argument,       0, 'd'},
        {"exp",        no_argument,       0, 'e'},
        {"help",       no_argument,       0, 'h'},
        {"input",      required_argument, 0, 'i'},
        {"log",        no_argument,       0, 'l'},
        {"mass",       required_argument, 0, 'm'}, 
        {"name",       required_argument, 0, 'n'}, 
        {"output",     required_argument, 0, 'o'},
        {"poly",       required_argument, 0, 'p'},
        {"range",      required_argument, 0, 'r'},  
        {"scan",       no_argument,       0, 's'},
        {"toys",       required_argument, 0, 't'},
        {"win_factor", required_argument, 0, 'w'},
        {0, 0, 0, 0}
    };
    
    int option_index = 0;
    int option_char; 
    while ((option_char = getopt_long(argc, argv, "cdehi:lm:n:o:p:r:st:w:", long_options, &option_index)) != -1) {
        switch(option_char) {
            case 'c': 
                model = BumpHunter::BkgModel::EXP_POLY_X_POLY;
                break;
            case 'd': 
                debug = true;
                break;
            case 'e': 
                model = BumpHunter::BkgModel::EXP_POLY;
                break; 
            case 'h':
                return EXIT_SUCCESS;
            case 'i': 
                file_path = optarg;
                break;
            case 'l': 
                log_fit = true;
                break;
            case 'm': 
                mass_hypo = atof(optarg); 
                break;
            case 'n': 
                hist_name = optarg; 
                break; 
            case 'o':
                output_file = optarg;
                break;
            case 'p': 
                poly_order = atoi(optarg);
                break;
            case 'r': 
                range = optarg; 
                break;
            case 's': 
                scan = true;
                break;
            case 't':
                toys = atoi(optarg);
                break;
            case 'w': 
                win_factor = atoi(optarg); 
                break;
            default: 
                return EXIT_FAILURE;
        }
    }

    // Make sure a file was specified by the user.  If not, warn the user and 
    // exit the application.
    if (file_path.empty()) { 
        cerr << "[ Bump Hunter ]: Please specify a file to process." << endl;
        cerr << "[ Bump Hunter ]: Use --help for usage." << endl;
        return EXIT_FAILURE;
    }

    // Open the ROOT file.  If any problems are encountered, warn the user
    // and exit the application.
    TFile* file = new TFile(file_path.c_str());
    if (file->IsZombie()) { 
        cerr << "[ Bump Hunter ]: Failed to open file " << file_path.c_str(); 
        return EXIT_FAILURE;
    }

    // Check if the histogram name has been specified.  If not, warn the user
    // and exit the application.
    if (hist_name.empty()) { 
        cerr << "[ Bump Hunter ]: Please specify the name of the histogram to fit." << endl;
        cerr << "[ Bump Hunter ]: Use --help for usage." << endl;
        return EXIT_FAILURE;
    }

    TH1* histogram = (TH1*) file->Get(hist_name.c_str()); 

    // Create a new Bump Hunter instance and set the given properties.
    BumpHunter* bump_hunter = new BumpHunter(model, poly_order, win_factor);
    if (log_fit) bump_hunter->writeResults(); 
    if (debug) bump_hunter->enableDebug();  
    
    // Build the string that will be used for the results file name
    if (output_file.empty()) { 
        output_file = "fit_result_mass" + to_string(mass_hypo) + "_order" +  
                       to_string(poly_order) + 
                       "_win_factor" + to_string(win_factor) + 
                       ".root"; 
    }

    // Create a new flat ntuple and define the variables it will contain.
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
    tuple->addVariable("win_factor"); 
    tuple->addVariable("sig_yield");  
    tuple->addVariable("sig_yield_err"); 
    tuple->addVariable("window_size"); 
    tuple->addVariable("upper_limit");

    if (toys != 0) {
        
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
    }

    std::vector<HpsFitResult*> results; 
    if (scan) {
        double start = atof(range.substr(0, range.find(",")).c_str());
        double end = atof(range.substr(range.find(",")).c_str()+1);
        
        while (start <= end) {
            cout << "Searching for resonance at mass " << start << endl; 
            results.push_back(bump_hunter->fitWindow(histogram, start, false));
            start += 0.001; 
        }

    } else {
        results.push_back(bump_hunter->fitWindow(histogram, mass_hypo, false)); 
    }

    cout << "Total results: " << results.size() << endl;

    for (auto& result : results) { 
        
        // Retrieve all of the result of interest. 
        double bkg_yield     = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getVal();
        double bkg_yield_err = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("bkg yield"))->getError();
        double sig_yield     = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("signal yield"))->getVal();
        double sig_yield_err = static_cast<RooRealVar*>(result->getRooFitResult()->floatParsFinal().find("signal yield"))->getError();
        double nll = result->getRooFitResult()->minNll();
        double invalid_nll = result->getRooFitResult()->numInvalidNLL();
        double minuit_status = result->getRooFitResult()->status();
        double edm = result->getRooFitResult()->edm(); 
    
        tuple->setVariableValue("ap_mass",          result->getMass());  
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
        tuple->setVariableValue("win_factor",       win_factor);  
        tuple->setVariableValue("sig_yield_err",    sig_yield_err);
        tuple->setVariableValue("window_size",      result->getWindowSize());  
        tuple->setVariableValue("upper_limit",      result->getUpperLimit());


        if (toys != 0) {
            
            std::vector<HpsFitResult*> tresults{bump_hunter->runToys(histogram, toys, mass_hypo)}; 
            
            for (auto& tresult : tresults) {
   
                double bkg_yield     = static_cast<RooRealVar*>(tresult->getRooFitResult()->floatParsFinal().find("bkg yield"))->getVal();
                double bkg_yield_err = static_cast<RooRealVar*>(tresult->getRooFitResult()->floatParsFinal().find("bkg yield"))->getError();
                double sig_yield     = static_cast<RooRealVar*>(tresult->getRooFitResult()->floatParsFinal().find("signal yield"))->getVal();
                double sig_yield_err = static_cast<RooRealVar*>(tresult->getRooFitResult()->floatParsFinal().find("signal yield"))->getError();
                double nll           = tresult->getRooFitResult()->minNll();
                double invalid_nll   = tresult->getRooFitResult()->numInvalidNLL();
                double minuit_status = tresult->getRooFitResult()->status();
                double edm           = tresult->getRooFitResult()->edm(); 

                tuple->addToVector("toy_bkg_yield",        bkg_yield);  
                tuple->addToVector("toy_bkg_yield_err",    bkg_yield_err);
                tuple->addToVector("toy_edm",              edm); 
                tuple->addToVector("toy_invalid_nll",      invalid_nll); 
                tuple->addToVector("toy_minuit_status",    minuit_status);
                tuple->addToVector("toy_nll",              nll); 
                tuple->addToVector("toy_p_value",          tresult->getPValue());
                tuple->addToVector("toy_q0",               tresult->getQ0()); 
                tuple->addToVector("toy_sig_yield",        sig_yield); 
                tuple->addToVector("toy_sig_yield_err",    sig_yield_err);
                tuple->addToVector("toy_upper_limits",     tresult->getUpperLimit());
            }
        }

        // Fill the ntuple
        tuple->fill(); 
    }

    // Delete the fit results from memory
    //delete result;  

    // Close the ntuple
    tuple->close(); 

    delete bump_hunter; 
    delete file;
}
