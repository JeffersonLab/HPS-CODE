#
#	@author: Omar Moreno <omoreno1@ucsc.edu>
#	@date: December 06, 2013
#

# Specify the minimum CMake version required
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# Set the name of the project.  This should be changed to whatever the user
# desires.
project(DST_EXAMPLES)

# Set the current version of the analysis package.
set(DST_EXAMPLES_VERSION_MAJOR 1)
set(DST_EXAMPLES_VERSION_MINOR 0) 

# Set the output directories of the binaries, static and shared libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${DST_EXAMPLES_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${DST_EXAMPLES_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${DST_EXAMPLES_BINARY_DIR}/lib")

# Set the path to additional Cmake modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")

# Find ROOT
find_package(ROOT REQUIRED)

# Include the ROOT headers    
include_directories(${ROOT_INCLUDE_DIRS})

# Include the LCIO headers
include_directories("$ENV{LCIO}/include")

# Find the necessary LCIO libraries
find_library(LCIO_DICT_LIB lcioDict $ENV{LCIO}/lib)
find_library(LCIO_LIB lcio $ENV{LCIO}/lib)

# Create the analysis example executable
add_executable(analysis_lcio_example analysis_lcio_example.cxx)
target_link_libraries(analysis_lcio_example ${LCIO_LIB} ${ROOT_CORE_LIBRARY} ${ROOT_HIST_LIBRARY} ${ROOT_GPAD_LIBRARY})


