#
#   @file: CMakeList.txt
#   @author: Omar Moreno <omoreno1@ucsc.edu>
#   @date: December 06, 2013
#


# Find the necessary LCIO libraries
find_library(LCIO_LIB lcio $ENV{LCIO}/lib)

add_library(TriggerData TriggerData.cxx)
target_link_libraries(TriggerData
    ${LCIO_LIB}
)

set_source_files_properties(EcalHit.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(EcalHit EcalHit.cxx)
target_link_libraries(EcalHit
    ${ROOT_CORE_LIBRARY}
)

set_source_files_properties(EcalCluster.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(EcalCluster EcalCluster.cxx)
target_link_libraries(EcalCluster
    ${ROOT_CORE_LIBRARY}
    EcalHit
)

set_source_files_properties(SvtHit.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(SvtHit SvtHit.cxx)
target_link_libraries(SvtHit
    ${ROOT_CORE_LIBRARY}
)

set_source_files_properties(SvtTrack.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(SvtTrack SvtTrack.cxx)
target_link_libraries(SvtTrack
    ${ROOT_CORE_LIBRARY}
)

set_source_files_properties(GblStripData.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(GblStripData GblStripData.cxx)
target_link_libraries( GblStripData
    ${ROOT_CORE_LIBRARY}
    ${ROOT_PHYSICS_LIBRARY}
)

set_source_files_properties(GblTrack.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(GblTrack GblTrack.cxx)
target_link_libraries( GblTrack
    ${ROOT_CORE_LIBRARY}
    ${ROOT_MATRIX_LIBRARY}
)

set_source_files_properties(GblTrackData.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(GblTrackData GblTrackData.cxx)
target_link_libraries( GblTrackData
    ${ROOT_CORE_LIBRARY}
    ${ROOT_MATRIX_LIBRARY}
    ${ROOT_MATHCORE_LIBRARY}
    SvtTrack
    GblStripData
    GblTrack
)

set_source_files_properties(HpsMCParticle.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(HpsMCParticle HpsMCParticle.cxx)
target_link_libraries(HpsMCParticle
    ${ROOT_CORE_LIBRARY}
)

set_source_files_properties(HpsParticle.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(HpsParticle HpsParticle.cxx)
target_link_libraries(HpsParticle
    ${ROOT_CORE_LIBRARY}
)

set_source_files_properties(MuonCluster.cxx APPEND_STRING PROPERTY COMPILE_FLAGS " -fPIC ")
add_library(MuonCluster MuonCluster.cxx)
target_link_libraries(MuonCluster
    ${ROOT_CORE_LIBRARY}
)

file(GLOB HPS_EVENT_DIC_SRC "${HPS_EVENT_DIC_DIR}/*.cxx")

add_library(HpsEvent SHARED HpsEvent.cxx ${HPS_EVENT_DIC_SRC})
target_link_libraries(HpsEvent
    ${ROOT_CORE_LIBRARY}
    EcalHit
    EcalCluster
    SvtHit
    SvtTrack
    GblStripData
    GblTrack
    GblTrackData
    HpsMCParticle
    HpsParticle
    MuonCluster
)
