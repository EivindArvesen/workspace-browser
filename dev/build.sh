#!/usr/bin/env bash

rm -rf build/ dist/
#rm *.log # *.spec

# python pyinstaller/Makespec.py --onefile --windowed application.py # -i <FILE.icns>, --icon=<FILE.icns>
# python pyinstaller/Build.py application.spec

pyinstaller main.spec
