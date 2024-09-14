find basecamp/StickyNotes/ -type d | while read -r dir; do
    # Check if sticky_notes_export.csv exists in the current directory
    FILE="$dir/sticky_notes_export.csv"
    if [[ -f "$FILE" ]]; then
        # Check if the file is empty
        if [[ ! -s "$FILE" ]]; then
            echo "Deleting directory: $dir (empty sticky_notes_export.csv)"
            rm -rf "$dir"
        fi
    fi
done
