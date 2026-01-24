#!/bin/bash

set -euo pipefail

DIR=""
OUTPUT_FILE="$(dirname "$0")/raw_targets.txt"

while getopts "d:" opt; do
    case $opt in
        d) DIR="$OPTARG" ;;
        ?) echo "wrong script usage. USAGE = ./script -d dir_path"; exit 1;;
    esac
done

if [ -z "$DIR" ]; then
    echo "wrong script usage. USAGE = ./script -d dir_path"
    exit 1
elif [ ! -d "$DIR" ]; then
    echo "Not a valid directory. Please enter a valid dir path"
    exit 1
fi

# while read -r line; do
#     echo "$line" >> "$OUTPUT_FILE"
# done < <(find "$DIR" -type d -mtime +7 \( -name "venv" -o -name "node_modules" -o -name "build" -o -name ".terraform*" \))

# Faster Method
find "$DIR" -type d \( -name "venv" -o -name ".venv" -o -name "node_modules" -o -name "build" -o -name ".terraform*" \) > "$OUTPUT_FILE"