#!/bin/bash

# Base directory containing the lab folders
BASE_DIR="/var/home/mark/Documents/semester6/Communications"
OUTPUT_DIR="/var/home/mark/Documents/semester6/Communications" # Or any other directory where you want to save PDFs

# Lab directories to process
LAB_DIRS=("lab3" "lab4" "lab5" "lab6")

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

for LAB_DIR_NAME in "${LAB_DIRS[@]}"; do
    CURRENT_LAB_PATH="$BASE_DIR/$LAB_DIR_NAME"
    OUTPUT_PDF="$OUTPUT_DIR/${LAB_DIR_NAME}.pdf"

    if [ -d "$CURRENT_LAB_PATH" ]; then
        echo "Processing directory: $CURRENT_LAB_PATH"

        # Find all image files (png, jpg, jpeg) in the current lab directory
        # and store them in an array.
        # The -print0 and read -d $'\0' handles filenames with spaces.
        mapfile -d $'\0' IMAGE_FILES < <(find "$CURRENT_LAB_PATH" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) -print0 | sort -z)

        if [ ${#IMAGE_FILES[@]} -gt 0 ]; then
            echo "Found ${#IMAGE_FILES[@]} images. Creating PDF: $OUTPUT_PDF"
            # Use convert (from ImageMagick) to create the PDF
            # The IFS= read -r -d $'\0' part is to correctly pass filenames with spaces
            convert "${IMAGE_FILES[@]}" "$OUTPUT_PDF"
            if [ $? -eq 0 ]; then
                echo "Successfully created $OUTPUT_PDF"
            else
                echo "Error creating $OUTPUT_PDF"
            fi
        else
            echo "No image files found in $CURRENT_LAB_PATH"
        fi
    else
        echo "Directory $CURRENT_LAB_PATH does not exist."
    fi
    echo "----------------------------------------"
done

echo "All processing complete."
