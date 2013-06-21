#!/bin/bash

# Export environment variables for Gupta Event API

# Needed for MySQL bindings
export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_LIBRARY_PATH"

# Needed to use libs in gupta directory (bug?)
export PYTHONPATH="$PYTHONPATH"
