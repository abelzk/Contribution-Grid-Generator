#!/bin/bash

# Install dependencies
pip install requests

# Run the Python script
python scripts/github_snake.py

# Commit and push the generated SVG
git config --global user.email "github-actions@github.com"
git config --global user.name "GitHub Actions"
git add github-snake.svg
git commit -m "Update GitHub contribution snake"
git push