#!/bin/zsh

# Define the target file path
TARGET_FILE="/usr/local/munki/middleware_bunny.py"

# Define the URL to download the file from if it doesn't exist
FILE_URL="https://raw.githubusercontent.com/ofirgalcon/bunny.net-middleware/main/middleware_bunny.py"

# Check if the file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "File not found: $TARGET_FILE"
    echo "Downloading from $FILE_URL..."
    
    # Use curl to download the file and save it to the target location
    curl -s -o "$TARGET_FILE" "$FILE_URL"
    
    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "File downloaded successfully and saved to $TARGET_FILE"
    else
        echo "Failed to download the file. Please check the URL and your internet connection."
    fi
else
    echo "File already exists: $TARGET_FILE"
fi
