#!/bin/bash

# Run the Python script to generate the SVG
python3 scripts/fetch_contributions.py

# Ensure changes are detected by updating the file timestamp
touch contribution_snake.svg

# Check if there are changes in the working tree
if ! git diff --quiet; then
    echo "Changes detected, committing updated SVG..."
    git config --global user.name "github-actions[bot]"
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
    git add contribution_snake.svg
    git commit -m "Auto-update contribution snake SVG"
    git push
else
    echo "No changes detected, nothing to commit."
fi
