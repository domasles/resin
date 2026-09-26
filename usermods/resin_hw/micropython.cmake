add_library(usermod_resin_hw INTERFACE)

target_sources(usermod_resin_hw INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modresinhw.c
    ${CMAKE_CURRENT_LIST_DIR}/display.c
    ${CMAKE_CURRENT_LIST_DIR}/dma.c
    ${CMAKE_CURRENT_LIST_DIR}/input.c
    ${CMAKE_CURRENT_LIST_DIR}/cdc.c
)

target_include_directories(usermod_resin_hw INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_resin_hw)
