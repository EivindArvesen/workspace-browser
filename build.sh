#!/usr/bin/env bash

rm -rf build/ dist/
pyinstaller main.spec
