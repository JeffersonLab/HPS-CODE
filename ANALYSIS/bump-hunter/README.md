The Heavy Photon Search Bump Hunter
===================================

Overview
--------

Requirements
------------

Building the project requires the following build tools:
* [GCC >= 4.8](https://gcc.gnu.org/install/)
* [CMake >= 2.8.12](http://www.cmake.org/cmake/help/install.html)

The project has the following dependencies:
* [ROOT data analysis framework](http://root.cern.ch/drupal/content/installing-root-source)
** Compatible with both ROOT versions 5 and 6 if build with cmake.

Installation
------------

##### Cloning the Repository from GitHub #####

The project is stored in a public GitHub repository.  The code can be 
"cloned" i.e. copied to a users local machine by issuing the following commands
from a terminal

	cd /path/to/workdir
	git clone https://github.com/JeffersonLab/HPS-CODE.git

A github account is not required to clone the source code.

##### Building the Project #####

Before building the project, the following environmental variables need to be set:

	ROOTSYS=/path/to/root

The project can then be built as follows:

	cd HPS-CODE/ANALYSIS/bump-hunter
	mkdir build; cd build
	cmake ..
	make

Running the Bump Hunter
------------------------

Running the bump hunter can be done as follows:

    bump_hunter -i <input_file.root> -m <mass> -n <histogram name> -o <output_file.root> -p <polynomial order>

The arguments to the command are as follows:
* input_file.root : A file containing a histogram that will be scanned 
                    for a resonance, <mass> is the mass hypothesis
* histogram name:  The name of the histogram
* output_file.root:  The output file where results will be written to 
* polynomial order: The order to the polynomial that will be used to model the 
                    background.

Maintainers
-----------

* Omar Moreno (SLAC National Accelerator Laboratory) 
