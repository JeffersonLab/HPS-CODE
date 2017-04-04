
add_library(FlatTupleMaker FlatTupleMaker.cxx)
target_link_libraries(FlatTupleMaker
    ${ROOT_CORE_LIBRARY}
    ${ROOT_RIO_LIB}
)

add_library(EcalUtils EcalUtils.cxx)
target_link_libraries(EcalUtils
    ${HPS_EVENT_LIBRARY}
)
