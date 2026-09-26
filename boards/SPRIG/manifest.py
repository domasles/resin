# Freeze resin package into firmware
include("$(PORT_DIR)/boards/manifest.py")
freeze("../../resin_py/src")
