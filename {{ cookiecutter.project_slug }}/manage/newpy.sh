#!/bin/bash

# Script to copy Python templates to the specified directory

# Check the number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: ./newpy <template_name> </path-in-project/script_name.py>"
    exit 1
fi

# Variables
TEMPLATE_NAME=$1
RELATIVE_TARGET_PATH=$2
PROJECT_ROOT=$(pwd)  # Assuming the script is executed from the project root
TEMPLATE_DIR="$PROJECT_ROOT/manage/templates"
FULL_TEMPLATE_PATH="$TEMPLATE_DIR/$TEMPLATE_NAME.py"
ABSOLUTE_TARGET_PATH=$(realpath "$RELATIVE_TARGET_PATH")

# Verify the template exists
if [ ! -f "$FULL_TEMPLATE_PATH" ]; then
    echo "The template $TEMPLATE_NAME does not exist in $TEMPLATE_DIR."
    exit 1
fi

# Verify that the target directory is within the project
if [[ "$ABSOLUTE_TARGET_PATH" != $PROJECT_ROOT/* ]]; then
    echo "The target must be within the project directory."
    exit 1
fi

# Create directories if they don't exist and copy the file
mkdir -p "$(dirname "$RELATIVE_TARGET_PATH")" && cp "$FULL_TEMPLATE_PATH" "$RELATIVE_TARGET_PATH"

# Success message
if [ $? -eq 0 ]; then
    echo "Template $TEMPLATE_NAME successfully copied to $RELATIVE_TARGET_PATH."
else
    echo "Error copying the template."
fi

