#!/bin/bash
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
echo "Running JSON validation using Python's json.tool..."

find . -name "*.json" | while read -r file; do
    echo "JSON validating: $file"
    $FLOOROTRON_PYTHON -m json.tool "$file" > /dev/null
    if [ $? -ne 0 ]; then
        echo "JSON validation failed for $file"
        exit 1
    fi
done

echo "JSON validation passed."
