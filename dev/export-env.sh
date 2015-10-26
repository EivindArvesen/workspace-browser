#!/usr/bin/env bash

ENV=raskolnikov-browser

# conda env export -n $ENV > environment.yml
conda list -n $ENV -e > requirements.txt # && pip freeze >> requirements.txt
