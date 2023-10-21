#!/bin/bash

# Script to create a new Jupyter Notebook based on a template and inject the project path

# Check the number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: ./notebook </path-in-project/file_name.ipynb>"
    exit 1
fi

# Variables
TEMPLATE_NAME="notebook"
RELATIVE_TARGET_PATH=notebooks/$1
PROJECT_ROOT=$(pwd)  # Assuming the script is executed from the project root
TEMPLATE_DIR="$PROJECT_ROOT/manage/templates"
FULL_TEMPLATE_PATH="$TEMPLATE_DIR/$TEMPLATE_NAME.ipynb"
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

# Create directories if they don't exist
mkdir -p "$(dirname "$RELATIVE_TARGET_PATH")"

# Read template and replace the placeholder
cat "$FULL_TEMPLATE_PATH" | sed "s|project_path|$PROJECT_ROOT|g" > "$RELATIVE_TARGET_PATH".ipynb

# Success message
if [ $? -eq 0 ]; then
    echo "Notebook template successfully copied to $RELATIVE_TARGET_PATH with project path set."
else
    echo "Error copying the notebook template."
fi
