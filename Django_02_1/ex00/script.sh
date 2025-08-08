#!/bin/bash

LOG_FILE="pip_install.log"
PYTHON_PATH="/usr/bin/python3"
VENE_DIR=".django_venv"

# setup venv
$PYTHON_PATH -m venv $VENE_DIR
source $VENE_DIR/bin/activate

# pip version
pip --version

# pip install
python3 -m pip install --upgrade pip
pip install --force-reinstall -r requirement.txt
