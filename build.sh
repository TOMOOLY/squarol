#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 build.py
python3 -m fontmake -u sources/Squarol-Regular.ufo -o ttf --output-dir fonts/ttf
python3 postprocess.py fonts/ttf/Squarol-Regular.ttf
