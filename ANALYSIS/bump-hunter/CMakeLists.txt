#
# CMakeLists.txt
# 
#

# Specify the minimum CMake version required
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# Set the project name
project(BUMP_HUNTER)

# Set the current version
set(BUMP_HUNTER_VERSION_MAJOR 0)
set(BUMP_HUNTER_VERSION_MINOR 1)

# Set the output directories of the binaries, static and shared libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${BUMP_HUNTER_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${BUMP_HUNTER_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${BUMP_HUNTER_BINARY_DIR}/lib")

# Set additional compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Set the path to additional CMake modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules")

# Require the ROOT libraries.
find_package(ROOT REQUIRED)

# Add the ROOT headers to the build
include_directories(${ROOT_INCLUDE_DIRS})

# Add fit headers to the build
include_directories("${BUMP_HUNTER_SOURCE_DIR}/include/fit")

# Add utils headers to the build
include_directories("${BUMP_HUNTER_SOURCE_DIR}/include/utils")

# Add the utils source to the build
add_subdirectory("${BUMP_HUNTER_SOURCE_DIR}/src/utils")

# Add the fit source to the build
add_subdirectory("${BUMP_HUNTER_SOURCE_DIR}/src/fit")

