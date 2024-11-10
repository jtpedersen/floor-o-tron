#!/bin/bash

# Ensure the script runs from the root of the git repository
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Create the .git/hooks/pre-commit script
HOOK_FILE="$REPO_ROOT/.git/hooks/pre-commit"

echo "#!/bin/bash" > "$HOOK_FILE"
echo "" >> "$HOOK_FILE"
echo "echo 'Running all pre-commit hooks...'" >> "$HOOK_FILE"

# Find and add all pre-commit-* scripts in the scripts directory to the main pre-commit script
find "$SCRIPT_DIR" -type f -name 'pre-commit-*' | while read -r script; do
    echo "source \"$script\"" >> "$HOOK_FILE"
    echo "echo 'Completed $script'" >> "$HOOK_FILE"
done

# Make sure the .git/hooks/pre-commit script is executable
chmod a+x "$HOOK_FILE"
echo "Created and set permissions for .git/hooks/pre-commit"

# Run install_linters.sh to set up the linters
echo "Running install_linters.sh to set up the linters..."
"$SCRIPT_DIR/install_linters.sh"

echo "Git hooks and linters setup complete."
