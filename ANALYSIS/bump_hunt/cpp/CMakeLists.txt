# Specify the minimum CMake version required
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# Set the project name
project(BUMP_HUNT)

# Set the current version
set(BUMP_HUNT_VERSION_MAJOR 1)
set(BUMP_HUNT_VERSION_MINOR 0)

# Set the output directories of the binaries, static and shared libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${BUMP_HUNT_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${BUMP_HUNT_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${BUMP_HUNT_BINARY_DIR}/lib")

# Set additional compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Set the path to additional CMake modules
#set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules")

# Include the HpsEvent headers
include_directories("$ENV{HPS_DST_PATH}/include/hps_event")

# Search for ROOT
find_package(ROOT REQUIRED)

# Define useful ROOT functions and macros (e.g. ROOT_GENERATE_DICTIONARY)
include(${ROOT_USE_FILE})

# Include the ROOT headers
include_directories(${ROOT_INCLUDE_DIRS})

# Include utils headers
include_directories("${BUMP_HUNT_SOURCE_DIR}/include/utils")

# Include analysis headers
include_directories("${BUMP_HUNT_SOURCE_DIR}/include/analysis")

# Add utils to the build
add_subdirectory("${BUMP_HUNT_SOURCE_DIR}/src/utils")

# Add analysis to the build
add_subdirectory("${BUMP_HUNT_SOURCE_DIR}/src/analysis")
