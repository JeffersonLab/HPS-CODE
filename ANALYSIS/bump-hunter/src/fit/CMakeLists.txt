
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
    FitPrinter
    RooPow
)

add_executable(bump_hunter bump_hunter.cxx)
target_link_libraries(bump_hunter
    ${ROOT_CORE_LIB}
    ${ROOT_RIO_LIB}
    ${ROOT_HIST_LIB} 
    ${ROOT_TREE_LIB} 
    ${ROO_FIT}
    ${ROO_FIT_CORE}
    BumpHunter
    FlatTupleMaker
    HpsFitResult
    RooPow
)

add_executable(evaluator evaluator.cxx)
target_link_libraries(evaluator
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
