#!/usr/bin/env bash

ENV=raskolnikov-browser

# Install Miniconda if there if the default Anaconda-path is not present.
if [ "$(uname)" == "Darwin" ]; then
    [[ ! -d $HOME/anaconda ]] && curl -L https://repo.continuum.io/miniconda/Miniconda-latest-MacOSX-x86_64.sh | bash
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    [[ ! -d $HOME/anaconda ]] && curl -L https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh | bash
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    [[ ! -d $HOME/anaconda ]] && curl -L https://repo.continuum.io/miniconda/Miniconda-latest-Windows-x86_64.sh | bash
fi
# Maybe support 32-bit versions as well?

#conda env create -f environment.yml -n $ENV
conda create --name $ENV --file requirements.txt
source activate $ENV
pip install git+https://github.com/pyinstaller/pyinstaller.git@develop
source deactivate
