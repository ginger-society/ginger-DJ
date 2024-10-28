#!/bin/bash

# Function to rename files and directories recursively
rename_files_folders() {
    for item in "$1"/*; do
        # Check if the item is a directory, if so, rename it recursively
        if [ -d "$item" ]; then
            rename_files_folders "$item"
        fi

        # Get the base name and path of the item
        base_name=$(basename "$item")
        dir_name=$(dirname "$item")

        # Replace 'ginger' with 'gingerdj' in the base name
        new_base_name=${base_name//ginger/gingerdj}
        
        # Rename the item if necessary
        if [ "$base_name" != "$new_base_name" ]; then
            mv "$item" "$dir_name/$new_base_name"
            echo "Renamed: $item -> $dir_name/$new_base_name"
        fi
    done
}

# Run the function on the current directory
rename_files_folders "$(pwd)"
