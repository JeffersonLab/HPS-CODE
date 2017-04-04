
add_library(TridentAnalysis TridentAnalysis.cxx)
target_link_libraries(TridentAnalysis
    ${HPS_EVENT_LIBRARY}
    AnalysisUtils
    FlatTupleMaker
    EcalUtils
    TrackClusterMatcher
)

add_library(TridentDataAnalysis TridentDataAnalysis.cxx)
target_link_libraries(TridentDataAnalysis 
    TridentAnalysis
)
