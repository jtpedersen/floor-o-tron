#!/bin/bash

# Source the environment variables
source "$(dirname "$0")/env.sh"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

set -e
set -x

$FLOOROTRON_PYTHON -m unittest discover -s $REPO_ROOT/duty-cycle-controller -p "test_*.py"

# Check the exit status and handle errors
if [ $? -ne 0 ]; then
    echo "Unit tests failed!!!"
    exit 1
fi

