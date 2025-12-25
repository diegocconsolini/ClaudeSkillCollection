# Migration Guide: Claude Code Plugins → Claude Desktop Skills

This guide explains the differences between Claude Code plugins and Claude Desktop skills, and helps you choose the right version for your needs.

## Table of Contents

- [Overview](#overview)
- [Key Differences](#key-differences)
- [Frontmatter Comparison](#frontmatter-comparison)
- [When to Use Which](#when-to-use-which)
- [Installation Guide](#installation-guide)
- [Feature Parity](#feature-parity)
- [Troubleshooting](#troubleshooting)

## Overview

The ClaudeSkillCollection repository contains **two versions** of each tool:

1. **Claude Code Plugins** - For Claude Code CLI users
2. **Claude Desktop Skills** - For Claude Desktop app users

**These are NOT conversions or replacements.** Both versions coexist:
- Original plugins remain in the repository root
- Desktop skills are in the `claude-desktop-skills/` directory
- Same functionality, different packaging format

## Key Differences

| Aspect | Claude Code Plugin | Claude Desktop Skill |
|--------|-------------------|---------------------|
| **Entry File** | `agents/*.md` | `Skill.md` |
| **File Case** | Any case | **Exactly** `Skill.md` (capital S) |
| **Location** | `.claude-plugin/plugin.json` | Root of skill directory |
| **Frontmatter Fields** | `capabilities`, `tools`, `model` | `license`, `compatibility`, `metadata` |
| **Installation** | `/plugin marketplace add` | Import ZIP via Claude Desktop |
| **Packaging** | Git repository | ZIP file with skill folder as root |
| **CLI Support** | ✅ Yes | ❌ No |
| **Desktop Support** | ❌ No | ✅ Yes |

## Frontmatter Comparison

### Claude Code Plugin Format

```yaml
---
name: gdpr-auditor
description: GDPR compliance auditing...
capabilities: ["gdpr-compliance-audit", "data-protection-analysis"]
tools: Read, Grep, Glob, Bash
model: inherit
---
```

**Fields:**
- `capabilities` - List of plugin capabilities (array)
- `tools` - Tools the agent can use (array or string)
- `model` - Model override (typically "inherit")

### Claude Desktop Skill Format

```yaml
---
name: gdpr-auditor
description: GDPR compliance auditing that analyzes code, databases, and configs for EU data protection compliance
license: MIT
compatibility: claude-desktop
metadata:
  version: 1.2.0
  author: Diego Consolini
  category: compliance
  runtime: python3
  dependencies: requirements.txt
---
```

**Fields:**
- `license` - License type (e.g., "MIT")
- `compatibility` - Platform compatibility (e.g., "claude-desktop")
- `metadata` - Additional metadata object
  - `version` - Semantic version
  - `author` - Creator name
  - `category` - Skill category
  - `runtime` - Runtime environment (python3, node.js)
  - `dependencies` - Dependencies file (if applicable)

### Transformation Rules

When converting from Claude Code to Desktop:

1. **Remove these fields:**
   - `capabilities` (not supported)
   - `tools` (not supported, becomes implicit)
   - `model` (not supported)

2. **Add these fields:**
   - `license: MIT`
   - `compatibility: claude-desktop`
   - `metadata` object with version, author, category

3. **Preserve these fields:**
   - `name` (unchanged)
   - `description` (may be enhanced)

4. **Optional additions:**
   - `allowed-tools` (if specific tool restrictions needed)
   - `metadata.requires-api` (for external API dependencies)
   - `metadata.requires-mcp` (for MCP server dependencies)

## When to Use Which

### Use Claude Code Plugins If:

- ✅ You use Claude Code CLI (`/claude` command)
- ✅ You want marketplace integration (`/plugin marketplace`)
- ✅ You prefer command-line workflows
- ✅ You need Git-based version control
- ✅ You're developing plugins (easier testing)
- ✅ You use hooks or custom commands

**Installation:**
```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install gdpr-auditor@security-compliance-marketplace
```

### Use Claude Desktop Skills If:

- ✅ You use Claude Desktop app (macOS, Windows)
- ✅ You prefer GUI-based workflows
- ✅ You want simpler installation (drag-and-drop ZIP)
- ✅ You don't need Git integration
- ✅ You want portability (ZIP files)
- ✅ You're sharing skills with non-technical users

**Installation:**
1. Download ZIP file
2. Open Claude Desktop
3. Go to Skills menu
4. Import ZIP file

## Installation Guide

### Claude Code Plugin Installation

**Option 1: From Marketplace**
```bash
# Add marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Install specific plugin
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install pdf-smart-extractor@security-compliance-marketplace
/plugin install plugin-security-checker@security-compliance-marketplace
```

**Option 2: Local Development**
```bash
# Clone repository
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Add as local marketplace
/plugin marketplace add file:///path/to/ClaudeSkillCollection

# Install from local
/plugin install gdpr-auditor@ClaudeSkillCollection
```

### Claude Desktop Skill Installation

**Option 1: Individual Skills**
1. Download `skill-name.zip` from releases
2. Open Claude Desktop
3. Menu → Skills → Import Skill
4. Select ZIP file
5. Confirm import

**Option 2: Batch Import**
1. Download all 9 ZIP files
2. Open Claude Desktop
3. Menu → Skills → Import Skill
4. Select all ZIP files at once
5. Confirm batch import

**Important:** ZIP structure must be:
```
skill-name.zip
└── skill-name/
    ├── Skill.md
    └── [other files...]
```

If the skill folder is not the root, Claude Desktop will reject it.

## Feature Parity

All skills have **identical functionality** between Claude Code and Desktop versions:

### Security & Compliance
| Skill | Claude Code | Desktop | Notes |
|-------|-------------|---------|-------|
| gdpr-auditor | ✅ v1.2.0 | ✅ v1.2.0 | Same analysis engine |
| cybersecurity-policy-generator | ✅ v1.2.0 | ✅ v1.2.0 | Same templates |
| incident-response-playbook-creator | ✅ v2.2.0 | ✅ v2.2.0 | Same 11 scenarios |
| security-report-builder | ✅ v1.0.1 | ✅ v1.0.1 | Same report formats |
| plugin-security-checker | ✅ v3.2.0 | ✅ v3.2.0 | Same 91 agents |

### Productivity & Optimization
| Skill | Claude Code | Desktop | Notes |
|-------|-------------|---------|-------|
| pdf-smart-extractor | ✅ v2.2.0 | ✅ v2.2.0 | Same cache system |
| xlsx-smart-extractor | ✅ v2.2.0 | ✅ v2.2.0 | Same chunking |
| docx-smart-extractor | ✅ v2.2.0 | ✅ v2.2.0 | Same extraction |
| chrome-devtools-optimizer | ✅ v1.0.1 | ✅ v1.0.1 | Same optimization |

**No feature differences** - Scripts, references, and functionality are identical.

## File Structure Comparison

### Claude Code Plugin Structure

```
gdpr-auditor/
├── .claude-plugin/
│   └── plugin.json          # Manifest
├── agents/
│   └── gdpr-auditor.md      # Agent file
├── scripts/                 # Python scripts
├── references/              # Reference data
└── requirements.txt         # Dependencies
```

### Claude Desktop Skill Structure

```
gdpr-auditor.zip
└── gdpr-auditor/
    ├── Skill.md             # Entry file (REQUIRED)
    ├── scripts/             # Python scripts
    ├── references/          # Reference data
    └── requirements.txt     # Dependencies
```

**Key differences:**
1. No `.claude-plugin/` directory needed
2. Single `Skill.md` instead of `agents/*.md`
3. Must be packaged as ZIP for distribution
4. ZIP must have skill folder as root (not nested)

## Caching Behavior

Both versions use the **same cache locations**:

### Smart Extractors
- **PDF:** `~/.claude-cache/pdf/`
- **Excel:** `~/.claude-cache/xlsx/`
- **Word:** `~/.claude-cache/docx/`

**Cross-compatible:** Extractions from Claude Code plugins work with Desktop skills and vice versa.

### Chrome DevTools Optimizer
- **Config:** `~/.config/chrome-devtools-optimizer/config.json`

**Gemini API key is shared** between both versions.

## Dependencies

### Python Skills

Both versions require the same dependencies:

```bash
# Install for any Python skill
pip3 install -r requirements.txt
```

**Dependencies are identical:**
- pdf-smart-extractor: `pymupdf`
- xlsx-smart-extractor: `openpyxl`, `pandas`
- docx-smart-extractor: `python-docx`
- plugin-security-checker: `stix2`, `taxii2-client`, `mitreattack-python`

### Node.js Skills

**chrome-devtools-optimizer:**
- Uses `npx` for dependencies (no package.json)
- Same Gemini API requirement
- Same Chrome DevTools MCP server requirement

## Troubleshooting

### Issue: "Skill import failed - invalid structure"

**Cause:** ZIP structure is incorrect.

**Solution:**
```bash
# Correct structure
skill-name.zip
└── skill-name/
    ├── Skill.md
    └── ...

# Incorrect structure (will fail)
skill-name.zip
└── Skill.md  # Missing skill-name/ folder
```

### Issue: "Skill.md not found"

**Cause:** Entry file must be exactly `Skill.md` (capital S, lowercase kill).

**Solution:**
- ❌ `SKILL.md` (all caps) - WRONG
- ❌ `skill.md` (all lowercase) - WRONG
- ✅ `Skill.md` (capital S) - CORRECT

### Issue: Scripts not working in Desktop skill

**Cause:** Scripts may reference relative paths incorrectly.

**Solution:**
- Verify scripts are in `scripts/` directory
- Check that paths are relative to skill root
- Test script execution from skill directory

### Issue: Cache not shared between versions

**Cause:** Cache paths are platform-specific.

**Solution:**
- Verify cache location exists: `ls ~/.claude-cache/`
- Check permissions: `chmod 755 ~/.claude-cache/`
- Re-extract document to regenerate cache

### Issue: Dependencies missing in Desktop skill

**Cause:** Requirements not installed or in wrong location.

**Solution:**
```bash
# Navigate to skill directory
cd ~/.claude/skills/skill-name/  # or wherever extracted

# Install dependencies
pip3 install -r requirements.txt
```

## Version Alignment

All skills maintain **version parity** between Claude Code and Desktop:

- Same version number (e.g., v2.2.0)
- Same feature set
- Same scripts and references
- Same bug fixes

**Updates are synchronized** - When a Claude Code plugin is updated, the Desktop skill receives the same update.

## Migration Checklist

If you're switching from Claude Code to Desktop (or vice versa):

### From Claude Code to Desktop
- [ ] Download skill ZIP files
- [ ] Import into Claude Desktop
- [ ] Verify cache directories exist
- [ ] Install Python/Node.js dependencies
- [ ] Test basic functionality
- [ ] (Optional) Uninstall Claude Code plugin

### From Desktop to Claude Code
- [ ] Clone ClaudeSkillCollection repository
- [ ] Add marketplace to Claude Code
- [ ] Install plugins via `/plugin install`
- [ ] Verify cache directories exist
- [ ] Install Python/Node.js dependencies
- [ ] Test basic functionality
- [ ] (Optional) Remove Desktop skills

**Note:** You can use both simultaneously - they share the same cache.

## Best Practices

1. **Choose one primary version**
   - Use Desktop for GUI workflows
   - Use Claude Code for CLI workflows
   - Mixing both can cause confusion

2. **Keep dependencies updated**
   - Both versions use same requirements
   - Update once, works for both

3. **Share cache directories**
   - Extract documents once
   - Query from either version
   - Saves time and tokens

4. **Version control**
   - Claude Code plugins work with Git
   - Desktop skills distributed as ZIPs
   - Choose based on workflow

5. **Updates**
   - Subscribe to repository releases
   - Check CHANGELOG.md for updates
   - Update both versions simultaneously

## Support

For issues specific to:
- **Claude Code plugins:** Check plugin documentation
- **Desktop skills:** Check Skill.md in each ZIP
- **Both:** Report to ClaudeSkillCollection repository

## License

Both Claude Code plugins and Desktop skills are MIT licensed.

## Credits

Migration guide created as part of the ClaudeSkillCollection project by Diego Consolini.

---

**Last Updated:** 2025-12-25
**Version:** 1.0.0
