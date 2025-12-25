#!/bin/bash
# sync-wiki.sh - Sync local wiki changes to GitHub

set -e

WIKI_DIR="/home/diegocc/ClaudeSkillCollection/wiki"
REPO_DIR="/home/diegocc/ClaudeSkillCollection"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Claude Code Wiki Sync ===${NC}"

# Check if wiki directory exists
if [ ! -d "$WIKI_DIR" ]; then
    echo -e "${RED}Error: Wiki directory not found at $WIKI_DIR${NC}"
    echo "Clone it first:"
    echo "  git clone https://github.com/diegocconsolini/ClaudeSkillCollection.wiki.git wiki"
    exit 1
fi

# Navigate to wiki directory
cd "$WIKI_DIR"

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}No changes to sync.${NC}"
    exit 0
fi

# Show status
echo -e "${YELLOW}Changes detected:${NC}"
git status --short

# Prompt for confirmation
read -p "Do you want to sync these changes? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Sync cancelled."
    exit 0
fi

# Get commit message
read -p "Enter commit message: " commit_message

if [ -z "$commit_message" ]; then
    commit_message="Wiki update: $(date +%Y-%m-%d)"
fi

# Stage all changes
git add .

# Commit
git commit -m "$commit_message"

# Push
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push

echo -e "${GREEN}=== Sync complete! ===${NC}"
echo "View wiki at: https://github.com/diegocconsolini/ClaudeSkillCollection/wiki"

# Update page count
page_count=$(ls "$WIKI_DIR"/*.md 2>/dev/null | wc -l)
echo -e "${GREEN}Total wiki pages: $page_count${NC}"
