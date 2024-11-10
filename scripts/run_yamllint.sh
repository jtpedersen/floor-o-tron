#!/bin/bash
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
echo "Running yamllint for YAML validation..."

$FLOOROTRON_PYTHON -m yamllint .

if [ $? -ne 0 ]; then
    echo "YAML linting failed. Check the output above for details."
    exit 1
fi

echo "YAML linting passed."
