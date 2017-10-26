# Find the required ROOT libraries
find_library(ROOT_TREE_LIB Tree $ENV{ROOTSYS}/lib)
find_library(ROOT_CORE_LIB Core $ENV{ROOTSYS}/lib)
find_library(ROOT_RIO_LIB RIO $ENV{ROOTSYS}/lib)
find_library(ROOT_PHYSICS_LIB Physics $ENV{ROOTSYS}/lib)
find_library(ROOT_HIST_LIB Hist $ENV{ROOTSYS}/lib)
find_library(ROOT_GPAD_LIB Gpad $ENV{ROOTSYS}/lib)
find_library(ROOT_GRAF_LIB Graf $ENV{ROOTSYS}/lib)
find_library(ROO_FIT RooFit $ENV{ROOTSYS}/lib)
find_library(ROO_FIT_CORE RooFitCore $ENV{ROOTSYS}/lib)

add_library(RootFileReader RootFileReader.cxx)
target_link_libraries(RootFileReader 
    ${ROOT_CORE_LIB}
    ${ROOT_GPAD_LIB}
    ${ROOT_TREE_LIB}
    ${ROOT_RIO_LIB}
    ${ROOT_PHYSICS_LIB}
    ${ROOT_HIST_LIB}
)

add_library(FlatTupleMaker FlatTupleMaker.cxx)
target_link_libraries(FlatTupleMaker
    ${ROOT_CORE_LIBRARY}
    ${ROOT_RIO_LIB}
)

add_library(FitPrinter FitPrinter.cxx)
target_link_libraries(FitPrinter
    ${ROOT_GPAD_LIB}
    ${ROO_FIT}
    ${ROO_FIT_CORE}
)

add_library(RooPow RooPow.cxx)
target_link_libraries(RooPow
    ${ROO_FIT}
    ${ROO_FIT_CORE}
     ${ROOT_CORE_LIB}
    ${ROOT_GPAD_LIB}
    ${ROOT_TREE_LIB}
    ${ROOT_RIO_LIB}
    ${ROOT_PHYSICS_LIB}
    ${ROOT_HIST_LIB}
)