# Marketplace Installation Workaround

## The Problem

When you install plugins from this marketplace using Claude Code's plugin UI, they download successfully but don't appear as available skills. This is due to a design limitation in Claude Code where:

- **Marketplace plugins install to:** `~/.claude/plugins/marketplaces/security-compliance-marketplace/<plugin>/`
- **Skill loader only scans:** `~/.claude/skills/`

There's no automatic bridge between these two locations.

## The Workaround

After installing a plugin via the marketplace UI, you must manually create a symlink:

### Step 1: Install via Marketplace UI

```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install gdpr-auditor@security-compliance-marketplace
```

Status will show "✓ Installed" but the skill won't load yet.

### Step 2: Create Symlink Manually

```bash
ln -s ~/.claude/plugins/marketplaces/security-compliance-marketplace/gdpr-auditor ~/.claude/skills/gdpr-auditor
```

### Step 3: Restart Claude Code

The skill will now be available.

## Automated Helper Script

Use this script to automatically link all installed marketplace plugins:

```bash
#!/bin/bash
# File: link-marketplace-plugins.sh

MARKETPLACE_DIR="$HOME/.claude/plugins/marketplaces/security-compliance-marketplace"
SKILLS_DIR="$HOME/.claude/skills"

if [ ! -d "$MARKETPLACE_DIR" ]; then
    echo "Error: Marketplace not found at $MARKETPLACE_DIR"
    exit 1
fi

echo "Linking marketplace plugins to skills directory..."

for plugin in "$MARKETPLACE_DIR"/*; do
    if [ -d "$plugin" ] && [ -f "$plugin/SKILL.md" ]; then
        plugin_name=$(basename "$plugin")
        skill_link="$SKILLS_DIR/$plugin_name"

        if [ -e "$skill_link" ]; then
            echo "⚠️  Skipping $plugin_name (already exists)"
        else
            ln -s "$plugin" "$skill_link"
            echo "✓ Linked $plugin_name"
        fi
    fi
done

echo ""
echo "Done! Restart Claude Code to use the skills."
```

### Usage:

```bash
chmod +x link-marketplace-plugins.sh
./link-marketplace-plugins.sh
```

## Verification

After linking and restarting, verify skills are available:

```bash
ls -la ~/.claude/skills/

# Should show symlinks like:
# gdpr-auditor -> /home/user/.claude/plugins/marketplaces/security-compliance-marketplace/gdpr-auditor
```

## Why This Happens

This is a **Claude Code architectural limitation**, not a problem with this marketplace:

1. `/plugin install` downloads to the marketplace directory
2. Claude Code's skill loader only scans `~/.claude/skills/` at startup
3. No automatic registration happens after marketplace installation

## The Proper Fix (For Claude Code Developers)

Claude Code should automatically create symlinks in `~/.claude/skills/` when installing marketplace plugins, or modify the skill loader to scan marketplace directories. This would make the `/plugin install` command truly one-step.

## Alternative: Direct Installation

If you prefer to avoid symlinks, install directly to the skills directory:

```bash
cd ~/.claude/skills/
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git
ln -s claude-skills-collection/gdpr-auditor ./gdpr-auditor
ln -s claude-skills-collection/cybersecurity-policy-generator ./cybersecurity-policy-generator
```

This bypasses the marketplace system entirely.

## Reporting This Issue

If you believe this should be fixed in Claude Code itself, please report it:
- Claude Code GitHub: https://github.com/anthropics/claude-code/issues

## Summary

**Current State:**
1. ❌ `/plugin install` → Skill doesn't load
2. ✅ Manual symlink → Skill loads

**Desired State:**
1. ✅ `/plugin install` → Skill loads automatically

Until Claude Code implements auto-registration, use the symlink workaround or the helper script provided above.
