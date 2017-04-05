
add_library(TridentAnalysis TridentAnalysis.cxx)
target_link_libraries(TridentAnalysis
    FlatTupleMaker
    AnalysisUtils
    EcalUtils
    TrackClusterMatcher
    ${HPS_EVENT_LIBRARY}
)

add_library(TridentDataAnalysis TridentDataAnalysis.cxx)
target_link_libraries(TridentDataAnalysis 
    TridentAnalysis
)

add_executable(trident_selector trident_selector.cxx)
target_link_libraries(trident_selector
    TridentAnalysis
    TridentDataAnalysis
    ${ROOT_LIBRARIES}
)
