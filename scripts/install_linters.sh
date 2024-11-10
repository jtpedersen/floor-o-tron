#!/bin/bash

# Define the virtual environment directory
VENV_DIR="scripts/venv"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment for linters..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at $VENV_DIR."
else
    echo "Virtual environment already exists at $VENV_DIR."
fi

# Define paths to Python and Pip inside the venv
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# Create or update the env.sh file with the environment variables
cat > scripts/env.sh <<EOL
#!/bin/bash
export FLOOROTRON_PYTHON="$VENV_PYTHON"
export FLOOROTRON_PIP="$VENV_PIP"
EOL

# Make env.sh executable
chmod +x scripts/env.sh

# Install linters
source scripts/env.sh
$FLOOROTRON_PIP install --upgrade pip
$FLOOROTRON_PIP install black yamllint

echo "Linters installed in the virtual environment."
echo "Environment variables have been set in scripts/env.sh."
