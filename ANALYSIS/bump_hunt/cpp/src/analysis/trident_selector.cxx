/**
 * @file trident_selector.cxx
 * @brief Application used to execute trident selector.
 * @author Omar Moreno, SLAC National Accelerator Laboratory
 */


//----------------//
//   C++ StdLib   //
//----------------//
#include <cstdlib>
#include <fstream>
#include <getopt.h>
#include <iostream>
#include <list>
#include <string>

//----------//
//   ROOT   //
//----------//
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>

//--------------//
//   Analysis   //
//--------------//
#include <HpsAnalysis.h>
#include <TridentDataAnalysis.h>
#include <TridentAnalysis.h>

using namespace std; 

void printUsage();

int main(int argc, char **argv) { 
    
    string dst_file_name{""};
    string file_list_name{""};
    int event_count{-1}; 
    bool is_mc{false};

    // Parse all the command line arguments.  If there are no valid command
    // line arguments passed, print the usage and exit the application
    static struct option long_options[] = {
        {"file_name",  required_argument, 0, 'i'},
        {"file_list",  required_argument, 0, 'l'},
        {"events",     required_argument, 0, 'n'},
        {"mc",         no_argument,       0, 'm'},
        {"help",       no_argument,       0, 'h'},
        {0, 0, 0, 0}
    };

    int option_index{0};
    int option_char; 
    while ((option_char = getopt_long(argc, argv, "i:l:n:mh", long_options, &option_index)) != -1) {

        switch(option_char){
            case 'i': 
                dst_file_name = optarg;
               break;
            case 'l':
                file_list_name = optarg;
                break; 
            case 'n':
                event_count = atoi(optarg);
                break;
            case 'm':
                is_mc = true;
                break;
            case 'h':
                printUsage();
                return EXIT_SUCCESS; 
            default: 
                printUsage(); 
                return EXIT_FAILURE;
        }
    }
    
    // If a DST file or a list of files was not specified, warn the user 
    // and exit the application.  Also exit if both a file and a list of files
    // has been specified
    if (dst_file_name.empty() && file_list_name.empty()) { 
        cerr << "\n[ TRIDENT SELECTOR ]: Please specify a DST file to process." << endl;
        cerr << "[ TRIDENT SELECTOR ]: Use --help for usage.\n" << endl;
        return EXIT_FAILURE;
    } else if (!dst_file_name.empty() && !file_list_name.empty()) { 
        cerr << "\n[ TRIDENT SELECTOR ]: Cannot specify both an DST file name and a "
             << "list of files." << endl;
        cerr << "[ TRIDENT SELECTOR ]: Use --help for usage.\n" << endl;
        return EXIT_FAILURE;
    } 
    
    // Create a list of files to process
    list<string> files; 
    string file;
    if (!dst_file_name.empty()) { 
        files.push_back(dst_file_name); 
    } else if (!file_list_name.empty()) { 
        
        ifstream file_list(file_list_name.c_str(), ifstream::in);
        if (!file_list.is_open()) { 
            cerr << "\n[ TRIDENT SELECTOR ]: Failed to open file " << file_list_name << endl;
            return EXIT_FAILURE;
        }
        
        while (file_list >> file) { 
            files.push_back(file); 
        }
        file_list.close();
    }
    
    HpsAnalysis* analysis{nullptr};
    if (is_mc) {
        analysis = new TridentAnalysis();
    } else { 
        analysis = new TridentDataAnalysis();
    }
        
    cout << "[ TRIDENT SELECTOR ]: Initializing analysis: " << analysis->toString() << endl;
    analysis->initialize();

    // Create a pointer to an HpsEvent object in order to read the TClonesArrays
    // collections
    HpsEvent *event = new HpsEvent();

    // Loop over all input files and process them
    for (list<string>::iterator files_it = files.begin(); files_it != files.end(); ++files_it) {
        
        // Open the ROOT file.  If the file can't be opened, exit the 
        // application
        TFile* file = new TFile((*files_it).c_str());

        cout << "[ TRIDENT SELECTOR ]: Processing file: " << *files_it << endl;

        // Get the TTree "HPS_EVENT" containing the HpsEvent branch and all
        // other collections
        TTree* tree = (TTree*) file->Get("HPS_Event");
    
        // Get the HpsEvent branch from the TTree and set the branch address to
        // the pointer created above
        TBranch *b_event = tree->GetBranch("Event");
        b_event->SetAddress(&event);
        
        // Loop over all of the events and process them
        for (int entry = 0; entry < tree->GetEntries(); ++entry) {
        
            // Print the event number every 500 events
            if((entry+1)%10000 == 0){
                std::cout << "[ TRIDENT SELECTOR ]: Event: " << entry+1 << endl;
            }
        
            // Read the ith entry from the tree.  This "fills" HpsEvent and allows
            // access to all collections
            tree->GetEntry(entry);

            analysis->processEvent(event);
        
            if (entry+1 == event_count) break;
        }
        
        // Delete the file
        delete file; 
    }

    // Finalize all of the analyses and free them
    analysis->finalize();

    return EXIT_SUCCESS;  

}

void printUsage() { 

}
