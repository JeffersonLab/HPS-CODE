/**
 *
 * @file bump_hunter.cxx
 * @author Omar Moreno
 *         SLAC National Accelerator Facility
 * @date June 22, 2016
 */

//----------------//
//   C++ StdLib   //
//----------------//
#include <cstdlib>
#include <getopt.h>
#include <iostream>

//----------//
//   ROOT   //
//----------//
#include <TFile.h>

//-----------------//
//   Bump Hunter   //
//-----------------//
#include <BumpHunter.h>
#include <FlatTupleMaker.h>

using namespace std;

int main(int argc, char **argv) { 

    // Name of file to process
    string file_name;

    // Histogram name
    string name = "";

    // Output file name
    string output_file = "";

    // Mass hypothesis
    double mass_hypo = 0; 

    // Default polynomial order to use to model the background
    int poly_order = 7;
   
    // Log fit results
    bool log_fit = false;

    // Run toys
    bool run_toys = false; 
 
    // Parse all the command line arguments.  If there are no valid command
    // line arguments passed, print the usage and exit the application
    static struct option long_options[] = {
        {"file_name",  required_argument, 0, 'i'},
        {"help",       no_argument,       0, 'h'},
        {"log",        no_argument,       0, 'l'},
        {"mass",       required_argument, 0, 'm'}, 
        {"name",       required_argument, 0, 'n'}, 
        {"output",     required_argument, 0, 'o'},
        {"poly",       required_argument, 0, 'p'},
        {"run_toys",   required_argument, 0, 't'},
        {0, 0, 0, 0}
    };

    int option_index = 0;
    int option_char; 
    while ((option_char = getopt_long(argc, argv, "i:hlm:n:o:p:t", long_options, &option_index)) != -1) {
        switch(option_char) {
            case 'i': 
                file_name = optarg;
                break;
            case 'h':
                return EXIT_SUCCESS; 
            case 'l': 
                log_fit = true;
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
                run_toys = true;
                break;
            default: 
                return EXIT_FAILURE;
        }
    }
    
    // Make sure a file was specified by the user.  If not, warn the user and 
    // exit the application.
    if (file_name.empty()) { 
        cerr << "[ BUMP HUNTER ]: Please specify a file to process." << endl;
        cerr << "[ BUMP HUNTER ]: Use --help for usage." << endl;
        return EXIT_FAILURE;
    }

    // Open the ROOT file.  If any problems are encountered, warn the user
    // and exit the application.
    TFile* file = new TFile(file_name.c_str());
    if (file->IsZombie()) { 
        cerr << "[ BUMP HUNTER ]: Failed to open file " << file_name.c_str(); 
        return EXIT_FAILURE;
    }

    TH1* histogram = (TH1*) file->Get(name.c_str()); 

    // Create a new Bump Hunter instance and set the given properties.
    BumpHunter* bump_hunter = new BumpHunter(poly_order);
    if (log_fit) bump_hunter->writeResults(); 
    //bump_hunter->setBounds(.014, .80);  

    // Build the string that will be used for the results file name
    if (output_file.empty()) { 
        output_file = "fit_result_mass" + to_string(mass_hypo) + "_order" +  to_string(poly_order) + ".root"; 
    }
    
    // Create a new flat ntuple and define the variables it will encapsulate.
    FlatTupleMaker* tuple = new FlatTupleMaker(output_file, "results"); 
}
