#!/bin/bash

# Source the environment variables
source "$(dirname "$0")/env.sh"

set -e

# Check if the --fix parameter is provided
if [ "$1" == "--fix" ]; then
    echo "Running Black to format Python files (fix mode)..."
    $FLOOROTRON_PYTHON -m black .
else
    echo "Running Black for Python formatting check..."
    $FLOOROTRON_PYTHON -m black . --check
fi

# Check the exit status and handle errors
if [ $? -ne 0 ]; then
    if [ "$1" == "--fix" ]; then
        echo "Black encountered issues while formatting."
    else
        echo "Black formatting check failed. Run './scripts/run_black.sh --fix' to auto-format."
    fi
    exit 1
fi

echo "Black formatting complete."
