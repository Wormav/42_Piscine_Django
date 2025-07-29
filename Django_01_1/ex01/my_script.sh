#!/bin/bash

# print version pip
pip3 --version

# upgrade pip
python3 -m pip install --upgrade pip

# upgade setuptools
python3 -m pip install --upgrade setuptools

# install path for github
pip3 install --upgrade --force-reinstall git+https://github.com/jaraco/path.git#egg=path \
--target=local_lib > install.log 2>&1

# if install ok run my_program
if [ $? -eq 0 ]; then
  python3 my_program.py
else
  echo "Fail install error"
fi