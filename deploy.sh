#!/bin/bash
# Deploy Velocitia IPTV Kodi Repository to GitHub Pages
#
# Prerequisites:
#   1. Create GitHub account (or use existing)
#   2. Create organization: velocitia-iptv (or change name below)
#   3. Install gh CLI: brew install gh
#   4. Login: gh auth login
#
# Usage: bash deploy.sh

set -e

REPO_NAME="kodi-repo"
ORG_NAME="velocitia-iptv"  # Change to your GitHub username if not using org

echo "=== Velocitia IPTV - Deploy to GitHub Pages ==="
echo ""

# Step 1: Check gh CLI
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI (gh) not found. Install with: brew install gh"
    exit 1
fi

# Step 2: Generate repo files
echo "1. Generating repository files..."
cd "$(dirname "$0")"
/opt/homebrew/bin/python3 generate_repo.py

# Step 3: Copy M3U playlist
echo ""
echo "2. Copying M3U playlist..."
cp ../all-channels.m3u .

# Step 4: Initialize git
echo ""
echo "3. Initializing git repository..."
git init
git add -A
git commit -m "feat: initial Velocitia IPTV Kodi repository with 28 channels"

# Step 5: Create GitHub repo
echo ""
echo "4. Creating GitHub repository..."
gh repo create "${ORG_NAME}/${REPO_NAME}" --public --description "Velocitia IPTV - Kodi Repository with 28+ live TV channels" --source=. --push

# Step 6: Enable GitHub Pages
echo ""
echo "5. Enabling GitHub Pages..."
gh api repos/${ORG_NAME}/${REPO_NAME}/pages -X POST -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || echo "   Pages may already be enabled or needs manual setup"

echo ""
echo "=== DONE ==="
echo ""
echo "Your repo: https://github.com/${ORG_NAME}/${REPO_NAME}"
echo "Your site: https://${ORG_NAME}.github.io/${REPO_NAME}/"
echo ""
echo "Users can install by adding this URL in Kodi File Manager:"
echo "  https://${ORG_NAME}.github.io/${REPO_NAME}/"
