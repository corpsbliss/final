#!/bin/bash

# Check if argument (file path) is provided
if [ -z "$1" ]; then
  echo "Error: No file path provided"
  exit 1
fi

# Get the file path from the argument
file_path="$1"

# Define the processed folder path
processed_folder="$(dirname "$file_path")/../processed"

# Create the processed folder if it doesn't exist
if [ ! -d "$processed_folder" ]; then
  mkdir -p "$processed_folder"
fi

# Define the output file path (replaces content each time)
output_file="$processed_folder/processed_output.txt"

# Process the file and overwrite output file
sh ./origin.sh $file_path > $output_file

#echo "Processing file: $file_path" > "$output_file"  # This will replace existing content
#cat "$file_path" >> "$output_file"  # Append file content, modify as needed

# Add any custom processing logic here. For example, filter and overwrite.
# grep "ERROR" "$file_path" > "$output_file"

echo "File processed and saved to $output_file"
