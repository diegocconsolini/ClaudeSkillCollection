# Security & Compliance Marketplace

This is a Claude Code plugin marketplace containing 9 professional security, compliance, and productivity plugins.

## 🚧 ACTIVE PROJECT: Claude Desktop Skills Migration (In Progress)

**Status:** Phase 2 of 4 (6/9 skills complete)
**Location:** `/home/diegocc/ClaudeSkillCollection/claude-desktop-skills/`
**Plan:** `/home/diegocc/.claude/plans/fluttering-foraging-torvalds.md`

### Completed Skills (6/9)
✅ gdpr-auditor - Ready for packaging
✅ cybersecurity-policy-generator - Ready for packaging
✅ incident-response-playbook-creator - Ready for packaging
✅ security-report-builder - Ready for packaging
✅ pdf-smart-extractor - Ready for packaging
✅ xlsx-smart-extractor - Ready for packaging

### Remaining Skills (3/9)
⏳ docx-smart-extractor - Need to create Skill.md
⏳ plugin-security-checker - Need to create Skill.md
⏳ chrome-devtools-optimizer - Need to create Skill.md (most complex)

### Remaining Tasks
- [ ] Create Skill.md for 3 remaining skills
- [ ] Create CHANGELOG.md
- [ ] Create MIGRATION_GUIDE.md
- [ ] Install `zip` utility
- [ ] Package all 9 skills as `.zip` files (required format for Claude Desktop)

**CRITICAL:** All skills must be packaged as ZIP files with structure:
```
skill-name.zip
└── skill-name/
    ├── Skill.md (case sensitive!)
    └── [scripts/, references/, etc.]
```

## Repository Structure

```
ClaudeSkillCollection/
├── .claude-plugin/marketplace.json    # Marketplace manifest (9 plugins)
├── plugin-security-checker/           # v3.2.0 - Plugin vulnerability scanner
├── gdpr-auditor/                      # v1.2.0 - GDPR compliance auditing
├── cybersecurity-policy-generator/    # v1.2.0 - Security policy generator
├── incident-response-playbook-creator/# v2.2.0 - IR playbook generator
├── pdf-smart-extractor/               # v2.2.0 - PDF extraction with caching
├── xlsx-smart-extractor/              # v2.2.0 - Excel extraction with caching
├── docx-smart-extractor/              # v2.2.0 - Word extraction with caching
├── security-report-builder/           # v1.0.1 - Security report generator
└── chrome-devtools-optimizer/         # v1.0.1 - Chrome DevTools token optimizer
```

## Plugin Manifest Format

All plugins use the correct Claude Code manifest format:

```json
{
  "name": "plugin-name",
  "version": "X.Y.Z",
  "description": "...",
  "author": { "name": "...", "email": "..." },
  "agents": ["agents/plugin-name.md"]
}
```

**Important:**
- `agents` must be an array of strings ending in `.md`
- Do NOT use: `$schema`, `category`, `requirements`, `scripts` (unsupported)
- Plugin manifest goes in `.claude-plugin/plugin.json`

## Agent File Format

All agent files have YAML frontmatter:

```yaml
---
name: agent-name
description: What this agent does
trigger: When to use this agent
tools: [Bash, Read, Write, Grep, Glob]
---

# Agent instructions here...
```

## Development Commands

```bash
# Validate all plugin manifests
for plugin in */; do
  if [ -f "$plugin/.claude-plugin/plugin.json" ]; then
    node -e "JSON.parse(require('fs').readFileSync('$plugin/.claude-plugin/plugin.json'))" && echo "✓ $plugin"
  fi
done

# Check agents format
node -e "const p=JSON.parse(require('fs').readFileSync('plugin/.claude-plugin/plugin.json')); console.log(Array.isArray(p.agents) && p.agents.every(a => typeof a === 'string' && a.endsWith('.md')))"
```

## Adding to Claude Code

```bash
# Add marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Install specific plugin
/plugin install plugin-security-checker@security-compliance-marketplace
```

## Cache Locations

Smart extractors use unified caching:
- PDF: `~/.claude-cache/pdf/`
- Excel: `~/.claude-cache/xlsx/`
- Word: `~/.claude-cache/docx/`
