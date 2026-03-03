# Security & Compliance Marketplace

This is a Claude Code plugin marketplace containing 9 professional security, compliance, and productivity plugins.

## 📚 Documentation Wiki

**Wiki:** https://github.com/diegocconsolini/ClaudeSkillCollection/wiki

53 comprehensive pages covering:
- Getting Started (Installation, First Session, Quick Reference)
- Configuration (CLAUDE.md, Memory Architecture, Settings, Permissions)
- MCP Servers (Transports, Scopes, Authentication, Troubleshooting)
- Plugins (Lifecycle, vs MCP, Creating)
- Context Optimization (What Consumes, Reduction Strategies, Subagent Delegation)
- Session Management (Task-Based Config, When to Restart, Workflow Patterns)
- Platform Guides (macOS, Linux, WSL2, Windows)
- Examples (14 copy-paste examples)
- Troubleshooting

**/claude-guide skill:** Navigate documentation with `/claude-guide [topic]`

## ✅ Claude Desktop Skills Pack v1.0.0 - RELEASED

**Status:** 8 of 9 skills ready for distribution (1 pending size optimization)
**Location:** `./claude-desktop-skills/`
**Packages:** `./claude-desktop-skills/packages/`

### Ready for Distribution (8/9)
✅ **gdpr-auditor** (57 KB) - GDPR compliance auditing
✅ **cybersecurity-policy-generator** (168 KB) - Security policy generator
✅ **incident-response-playbook-creator** (85 KB) - IR playbook creator (11 scenarios)
✅ **security-report-builder** (35 KB) - Security report generator
✅ **pdf-smart-extractor** (17 KB) - PDF extraction with caching
✅ **xlsx-smart-extractor** (16 KB) - Excel extraction with caching
✅ **docx-smart-extractor** (14 KB) - Word extraction with caching
✅ **chrome-devtools-optimizer** (30 KB) - Chrome DevTools token optimizer

### Pending (1/9)
⏸️ **plugin-security-checker** (9.2 MB) - Exceeds Claude Desktop 30MB uncompressed limit
   - Issue: 50MB STIX data in `references/stix/`
   - Options: Remove STIX data OR provide separate download instructions
   - Original data preserved in plugin-security-checker/ directory

### Documentation
✅ **README.md** - Skills catalog and installation guide
✅ **CHANGELOG.md** - Version 1.0.0 release notes
✅ **MIGRATION_GUIDE.md** - Claude Code vs Desktop comparison

### Package Format

**Claude Code Plugins** (root directories) use:
```
plugin-name/
├── .claude-plugin/plugin.json    # Manifest (REQUIRED)
├── SKILL.md                      # Skill definition (all caps)
├── agents/plugin-name.md         # Agent file with YAML frontmatter
├── scripts/ (optional)
├── references/ (optional)
├── version.json (optional)
└── requirements.txt (Python plugins only)
```

**Claude Desktop Skills** (claude-desktop-skills/) use:
```
skill-name.zip
└── skill-name/
    ├── Skill.md                  # Skill definition (capital S)
    ├── scripts/ (optional)
    ├── references/ (optional)
    └── requirements.txt (Python skills only)
```

**Skill.md/SKILL.md frontmatter:**
- Required fields: `name`, `description`
- Desktop-specific fields: `license`, `compatibility`, `metadata`
- Start with `---` (YAML frontmatter)
- Have proper permissions (644, not executable)

**Total Package Size:** 425 KB (8 distributable ZIP files)

## Repository Structure

```
ClaudeSkillCollection/
├── .claude-plugin/marketplace.json         # Marketplace manifest (9 plugins)
│
├── claude-desktop-skills/                  # Claude Desktop Skills Pack
│   ├── README.md                           # Installation guide
│   ├── CHANGELOG.md                        # Version history
│   ├── MIGRATION_GUIDE.md                  # Code vs Desktop comparison
│   ├── packages/                           # Distributable ZIP files (8 ready)
│   ├── gdpr-auditor/                       # v1.2.0
│   ├── cybersecurity-policy-generator/     # v1.2.0
│   ├── incident-response-playbook-creator/ # v2.2.0
│   ├── security-report-builder/            # v1.0.1
│   ├── pdf-smart-extractor/                # v2.2.0
│   ├── xlsx-smart-extractor/               # v2.2.0
│   ├── docx-smart-extractor/               # v2.2.0
│   ├── chrome-devtools-optimizer/          # v1.0.1
│   └── plugin-security-checker/            # v3.2.0 (pending size optimization)
│
├── plugin-security-checker/                # Claude Code plugin
├── gdpr-auditor/                           # Claude Code plugin
├── cybersecurity-policy-generator/         # Claude Code plugin
├── incident-response-playbook-creator/     # Claude Code plugin
├── pdf-smart-extractor/                    # Claude Code plugin
├── xlsx-smart-extractor/                   # Claude Code plugin
├── docx-smart-extractor/                   # Claude Code plugin
├── security-report-builder/                # Claude Code plugin
└── chrome-devtools-optimizer/              # Claude Code plugin
```

## Plugin Manifest Format

All plugins use the correct Claude Code manifest format:

```json
{
  "name": "plugin-name",
  "version": "X.Y.Z",
  "description": "...",
  "author": { "name": "...", "email": "..." },
  "agents": ["./agents/plugin-name.md"]
}
```

**Important:**
- `agents` must be an array of strings ending in `.md`
- Agent paths **MUST** start with `./` (e.g., `"./agents/plugin-name.md"`)
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

## Installation

### Claude Desktop Skills (8 ready for use)

**Location:** `./claude-desktop-skills/packages/`

Import ZIP files directly into Claude Desktop:
1. Open Claude Desktop
2. Go to Skills menu
3. Click "Import Skill"
4. Select ZIP file from packages/ directory

### Claude Code Plugins (9 available)

```bash
# Add marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Install specific plugin
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install pdf-smart-extractor@security-compliance-marketplace
```

## Cache Locations

Smart extractors use unified caching:
- PDF: `~/.claude-cache/pdf/`
- Excel: `~/.claude-cache/xlsx/`
- Word: `~/.claude-cache/docx/`
