#!/bin/bash

set -e

# setup virtualenv
if [ ! -d VIRT ] ; then
    venvbin="`which virtualenv`"
    if [[ "$venvbin" = "" ]] ; then
        syspipbin="`which pip`"
        if [[ "$syspipbin" = "" ]] ; then
            syseasybin="`which easy_install`"
            if [[ "$syseasybin" = "" ]] ; then
                echo "Cannot find easy_install program for python"
                exit 1;
            fi
            echo "Installing pip ..."
            "$syseasybin" pip
            syspipbin="`which pip`"
        fi
        echo "Installing virtualenv ..."
        "$syspipbin" install virtualenv
        venvbin="`which virtualenv`"
    fi
    "$venvbin" VIRT
fi
echo "Activating virtual environment VIRT ..."
source VIRT/bin/activate

# Add MySQL to lib path
echo "Adding MySQL to lib path ..."
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib:$DYLD_LIBRARY_PATH

# Install deps
echo "Installing python library dependencies ..."
VIRT/bin/pip install MySQL-python
VIRT/bin/pip install web.py
VIRT/bin/pip install requests
