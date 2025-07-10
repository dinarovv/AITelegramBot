#!/bin/bash

echo "Installing Python packages from requirements.txt..."
pip install -r ./libs/requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "Error occurred during installation."
else
    echo
    echo "All packages installed successfully!"
fi

read -p "Press Enter to continue..."
