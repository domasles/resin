#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

USER_C_MODULES_PATH="$PROJECT_ROOT/usermods/resin_hw"
BOARD_DIR="$PROJECT_ROOT/boards"
DIST_DIR="$PROJECT_ROOT/dist"

CONFIG="${1:-debug}"

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
      -D MICROPY_BOARD_DIR="$BOARD_DIR/SPRIG" \
      -D USER_C_MODULES="$USER_C_MODULES_PATH" \
      -D CMAKE_BUILD_TYPE="$BUILD_TYPE" \
      -D RESIN_DIST_DIR="$OUT_DIR" \
      -D RESIN_BUILD_TYPE="$(echo "$CONFIG" | tr '[:lower:]' '[:upper:]')"

echo ""
echo "Project generation completed for [$CONFIG]!"
echo "Build directory:  $BUILD_DIR"
echo "Artifact output:  $OUT_DIR"
echo ""
echo "To build firmware:"
echo "  cmake --build $BUILD_DIR"
