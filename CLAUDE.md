# Security & Compliance Marketplace

This is a Claude Code plugin marketplace containing 9 professional security, compliance, and productivity plugins.

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
