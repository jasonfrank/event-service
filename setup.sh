#!/bin/bash

# Prereqs:
#
#   Python
#   pip (package installer for Python)
#   MySQL
#
# If you want to work in a virtual environment, set that up first.
# From a clean install:
#
#   sudo easy_install pip
#   sudo pip install virtualenv
#   virtualenv VIRT
#
# This will give you a working virtual environment. From now on, you
# have to execute the following command when you start a new bash:
#
#   source VIRT/bin/activate
#
# That will setup your bash prompt and environment for the project.

# Add MySQL to lib path
echo "Adding MySQL to lib path ..."
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib:$DYLD_LIBRARY_PATH

# Install deps
echo "Installing python library dependencies ..."
pip install MySQL-python
pip install web.py
pip install requests
pip install nose
