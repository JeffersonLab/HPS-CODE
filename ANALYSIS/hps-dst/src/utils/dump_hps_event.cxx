/**
 *  @section purpose: 
 *      Print detailed information about an LCEvent.  Specificaly, the size, 
 *      type and names of collections in an LCEvent are printed.
 *  @author:    Omar Moreno <omoreno1@ucsc.edu>
 *              Santa Cruz Institute for Particle Physics
 *              University of California, Santa Cruz
 *  @date: May 21, 2013
 *
 */

 //--- C++ ---//
#include <iostream>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>

//--- LCIO ---//
#include <IO/LCReader.h>
#include <IOIMPL/LCFactory.h>
#include <EVENT/LCEvent.h>
#include <Exceptions.h>
#include <UTIL/LCTOOLS.h>

using namespace std; 

void displayUsage();

int main( int argc, char **argv )
{

	// Parse the command line arguments
	static struct option long_options[] =
	{
	    {"input", required_argument, 0, 'i'},
	    {"help", no_argument, 0, 'h'},
	    {0, 0, 0, 0}
	};

	string lcio_file_name = "";

	int option_char = 0;
	int option_index = 0;
	// Parse any command line arguments. If there are no valid command line
	// arguments given, print the usage.
    while((option_char = getopt_long(argc, argv, "i:h", long_options, &option_index)) != -1){

        switch(option_char){
			case 'i':
				lcio_file_name = optarg;
				break;
			case 'h':
				displayUsage();
				return EXIT_SUCCESS;
			default:
				displayUsage();
				return EXIT_FAILURE;
		}
	}

    // If an LCIO file is not specified, exit te program
    if(lcio_file_name.length() == 0){
    	cout << "\nPlease specify an LCIO file to process." << endl;
    	cout << "Use the -h flag for usage\n" << endl;
    	return EXIT_FAILURE;
    }

	// Create the LCIO reader and open the LCIO file specified by the user.
	// If the file doesn't exist or can't be opened, notify the user and exit
	IO::LCReader *lc_reader = IOIMPL::LCFactory::getInstance()->createLCReader();
	try{
		lc_reader->open(lcio_file_name.c_str());
	} catch(IO::IOException e){
		cout << "File " << lcio_file_name << " cannot be opened!" << endl;
		return EXIT_FAILURE;
	}

	// Read the first event in the LCIO file
	EVENT::LCEvent *event = lc_reader->readNextEvent();

    // Dump the collections present in the event
    UTIL::LCTOOLS::dumpEvent(event);

    lc_reader->close();

	return EXIT_SUCCESS;

}

void displayUsage()
{
    cout << "\nUsage: dump_hps_event [OPTIONS] LCIO_INPUT_FILE" << endl;
    cout << "An LCIO_INPUT_FILE must be specified.\n"  << endl;
    cout << "OPTIONS:\n "
         << "\t -i Input LCIO file name \n"
         << "\t -h Display this help and exit \n"
         << endl;
}
