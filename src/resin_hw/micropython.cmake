add_library(usermod_resin_hw INTERFACE)

file(GLOB USERMOD_RESIN_HW_SOURCES 
    "${CMAKE_CURRENT_LIST_DIR}/*.c"
)

target_sources(usermod_resin_hw INTERFACE
    ${USERMOD_RESIN_HW_SOURCES}
)

target_include_directories(usermod_resin_hw INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_resin_hw)
