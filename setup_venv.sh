#!/bin/bash

# Exit on error
set -e

# Define the virtual environment directory
VENV_DIR=".venv"

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install .[dev]

echo "Virtual environment setup complete. Activate it with: source $VENV_DIR/bin/activate"
