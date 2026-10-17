#!/bin/bash
set -e

CONFIG="${1:-debug}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(realpath $SCRIPT_DIR/..)"
DIST_DIR="$PROJECT_ROOT/dist"

BOARD_DIR="$PROJECT_ROOT/src/boards/SPRIG"
RESIN_HW_DIR="$PROJECT_ROOT/src/resin_hw"
RESIN_PY_MANIFEST="$PROJECT_ROOT/src/resin_py/manifest.py"

if [ "$CONFIG" == "release" ]; then
    BUILD_DIR="$PROJECT_ROOT/build/release"
    OUT_DIR="$DIST_DIR/release"
    BUILD_TYPE="Release"
elif [ "$CONFIG" == "debug" ]; then
    BUILD_DIR="$PROJECT_ROOT/build/debug"
    OUT_DIR="$DIST_DIR/debug"
    BUILD_TYPE="Debug"
fi

mkdir -p "$OUT_DIR"

echo "Generating CMake [$CONFIG] project"

cmake -S "$PROJECT_ROOT/micropython/ports/rp2" \
    -B "$BUILD_DIR" \
    -G Ninja \
    -D MICROPY_BOARD=SPRIG \
    -D MICROPY_BOARD_DIR="$BOARD_DIR" \
    -D USER_C_MODULES="$RESIN_HW_DIR" \
    -D MICROPY_FROZEN_MANIFEST="$RESIN_PY_MANIFEST" \
    -D CMAKE_BUILD_TYPE="$BUILD_TYPE" \
    -D RESIN_DIST_DIR="$OUT_DIR" \
    -D RESIN_BUILD_TYPE="$(echo "$CONFIG" | tr '[:lower:]' '[:upper:]')"

echo ""
echo "Project generation completed - $CONFIG configuration"
echo "Build directory:  $BUILD_DIR"
echo "Artifact output:  $OUT_DIR"
echo ""
echo "To build firmware:"
echo "  cmake --build $BUILD_DIR"
