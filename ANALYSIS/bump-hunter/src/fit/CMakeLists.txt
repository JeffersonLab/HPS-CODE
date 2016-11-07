
find_library(ROO_FIT RooFit $ENV{ROOTSYS}/lib)
find_library(ROO_FIT_CORE RooFitCore $ENV{ROOTSYS}/lib)
find_library(ROOT_GPAD_LIB Gpad $ENV{ROOTSYS}/lib)
find_library(ROOT_MATH_LIB MathCore $ENV{ROOTSYS}/lib)

add_library(HpsFitResult HpsFitResult.cxx
    ${ROO_FIT}
    ${ROO_FIT_CORE}
)

add_library(BumpHunter BumpHunter.cxx)
target_link_libraries(BumpHunter
    ${ROOT_GPAD_LIB}
    ${ROO_FIT}
    ${ROO_FIT_CORE}
    ${ROOT_MATH_LIB}
    HpsFitResult
)

add_executable(bump_hunt_evaluator bump_hunt_evaluator.cxx)
target_link_libraries(bump_hunt_evaluator
    ${ROOT_CORE_LIB}
    ${ROOT_RIO_LIB}
    ${ROOT_HIST_LIB}  
    ${ROO_FIT}
    ${ROO_FIT_CORE}
    RootFileReader
    BumpHunter
    FlatTupleMaker
    HpsFitResult
)

add_executable(set_upper_limits set_upper_limits.cxx)
target_link_libraries(set_upper_limits
    ${ROOT_CORE_LIB}
    ${ROOT_RIO_LIB}
    ${ROOT_HIST_LIB} 
    ${ROOT_TREE_LIB} 
    ${ROO_FIT}
    ${ROO_FIT_CORE}
    BumpHunter
    FlatTupleMaker
    HpsFitResult
)
