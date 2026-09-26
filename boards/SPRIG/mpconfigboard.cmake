include(${MICROPY_DIR}/ports/rp2/boards/RPI_PICO/mpconfigboard.cmake)

if (RESIN_BUILD_TYPE STREQUAL "RELEASE")
    add_compile_definitions(RESIN_RELEASE_BUILD=1)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-error=maybe-uninitialized")
elseif (RESIN_BUILD_TYPE STREQUAL "DEBUG")
    add_compile_definitions(RESIN_DEV_BUILD=1)
endif()

if (NOT DEFINED RESIN_DIST_DIR)
    set(RESIN_DIST_DIR "${CMAKE_SOURCE_DIR}/../../dist/${CMAKE_BUILD_TYPE}")
endif()

cmake_language(DEFER CALL copy_resulting_binary)

function(copy_resulting_binary)
    if (TARGET firmware)
        file(MAKE_DIRECTORY "${RESIN_DIST_DIR}")

        add_custom_command(
            TARGET firmware POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "${CMAKE_BINARY_DIR}/firmware.uf2"
                "${RESIN_DIST_DIR}/firmware.uf2"
            COMMENT "Copying firmware.uf2 to ${RESIN_DIST_DIR}/firmware.uf2"
        )
    endif()
endfunction()
