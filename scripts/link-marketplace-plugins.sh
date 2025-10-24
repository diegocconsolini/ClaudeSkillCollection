#!/bin/bash
# link-marketplace-plugins.sh
# Automatically create symlinks for marketplace plugins to make them available as skills
#
# Usage: ./link-marketplace-plugins.sh
#
# This script addresses the Claude Code limitation where marketplace-installed plugins
# aren't automatically registered with the skill loader.

set -e

# Configuration
MARKETPLACE_DIR="$HOME/.claude/plugins/marketplaces/security-compliance-marketplace"
SKILLS_DIR="$HOME/.claude/skills"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Claude Code Marketplace Plugin Linker ===${NC}"
echo ""

# Check if marketplace directory exists
if [ ! -d "$MARKETPLACE_DIR" ]; then
    echo -e "${RED}Error: Marketplace directory not found${NC}"
    echo "Expected location: $MARKETPLACE_DIR"
    echo ""
    echo "Please install the marketplace first:"
    echo "  /plugin marketplace add diegocconsolini/ClaudeSkillCollection"
    exit 1
fi

# Check if skills directory exists, create if not
if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${YELLOW}Creating skills directory: $SKILLS_DIR${NC}"
    mkdir -p "$SKILLS_DIR"
fi

echo "Scanning for plugins in:"
echo "  $MARKETPLACE_DIR"
echo ""

# Counter for statistics
linked_count=0
skipped_count=0
error_count=0

# Find all plugins with SKILL.md files
for plugin in "$MARKETPLACE_DIR"/*; do
    # Skip if not a directory
    if [ ! -d "$plugin" ]; then
        continue
    fi

    plugin_name=$(basename "$plugin")

    # Skip hidden directories and meta directories
    if [[ $plugin_name == .* ]] || [[ $plugin_name == "README.md" ]]; then
        continue
    fi

    skill_md="$plugin/SKILL.md"
    skill_link="$SKILLS_DIR/$plugin_name"

    # Check if this is actually a skill (has SKILL.md)
    if [ ! -f "$skill_md" ]; then
        echo -e "${YELLOW}⚠️  Skipping $plugin_name (no SKILL.md found)${NC}"
        ((skipped_count++))
        continue
    fi

    # Check if symlink or directory already exists
    if [ -e "$skill_link" ] || [ -L "$skill_link" ]; then
        if [ -L "$skill_link" ]; then
            # It's a symlink - check if it points to the right place
            current_target=$(readlink "$skill_link")
            if [ "$current_target" == "$plugin" ]; then
                echo -e "${GREEN}✓${NC} $plugin_name (already linked correctly)"
            else
                echo -e "${YELLOW}⚠️  $plugin_name (symlink exists but points elsewhere)${NC}"
                echo "   Current: $current_target"
                echo "   Expected: $plugin"
            fi
        else
            echo -e "${YELLOW}⚠️  Skipping $plugin_name (file/directory already exists)${NC}"
        fi
        ((skipped_count++))
    else
        # Create the symlink
        if ln -s "$plugin" "$skill_link" 2>/dev/null; then
            echo -e "${GREEN}✓ Linked $plugin_name${NC}"
            ((linked_count++))
        else
            echo -e "${RED}✗ Failed to link $plugin_name${NC}"
            ((error_count++))
        fi
    fi
done

echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}Newly linked:${NC} $linked_count"
echo -e "${YELLOW}Skipped:${NC} $skipped_count"
if [ $error_count -gt 0 ]; then
    echo -e "${RED}Errors:${NC} $error_count"
fi
echo ""

if [ $linked_count -gt 0 ]; then
    echo -e "${GREEN}Success!${NC} Linked $linked_count new skill(s)."
    echo ""
    echo "Next steps:"
    echo "1. Restart Claude Code"
    echo "2. Test the skills are available"
    echo ""
    echo "Verify with:"
    echo "  ls -la ~/.claude/skills/"
else
    echo "No new skills were linked."
    if [ $skipped_count -gt 0 ]; then
        echo "All plugins are already available."
    fi
fi

exit 0
