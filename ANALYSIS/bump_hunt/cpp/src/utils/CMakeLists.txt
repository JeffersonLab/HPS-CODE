
add_library(FlatTupleMaker FlatTupleMaker.cxx)
target_link_libraries(FlatTupleMaker
    ${ROOT_LIBRARIES}
)

find_library(HPS_EVENT_LIBRARY HpsEvent $ENV{HPS_DST_PATH}/build/lib)

add_library(EcalUtils EcalUtils.cxx)
target_link_libraries(EcalUtils
    ${HPS_EVENT_LIBRARY}
)

add_library(TrackClusterMatcher TrackClusterMatcher.cxx)
target_link_libraries(TrackClusterMatcher
    ${HPS_EVENT_LIBRARY}
)

add_library(AnalysisUtils AnalysisUtils.cxx)
target_link_libraries(AnalysisUtils
    ${HPS_EVENT_LIBRARY}
)
