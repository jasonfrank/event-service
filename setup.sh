#!/bin/bash

# Prereqs:
#
#   Python
#   pip (package installer for Python)
#   MySQL
#   SQLite3 (for testing)
#
# If you want to work in a virtual environment, set that up first.
# From a clean install:
#
#   sudo easy_install pip
#   sudo pip install virtualenv
#   virtualenv VIRT
#   source setup.sh
#
# This will give you a working virtual environment. From now on, you
# have to execute the following command when you start a new bash:
#
#   source VIRT/bin/activate
#   source env.sh
#
# That will setup your bash prompt and environment for the project.

[[ -r env.sh ]] && source env.sh

echo "Installing python library dependencies ..."
pip install MySQL-python
pip install web.py
pip install requests
pip install nose
pip install paste

echo "Setting up sqlite db for development ..."
mkdir -p data
sqlite3 data/event.db < db/sqlite_tables.sql
cp example.cfg event.cfg
