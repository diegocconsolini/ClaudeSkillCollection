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
├── security-report-builder/           # v1.2.0 - Security report generator
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

## Unified Version System

Plugins with version.json use a unified version control system:

```bash
# Check version sync status
python3 <plugin>/scripts/sync_versions.py

# Apply version updates to all files
python3 <plugin>/scripts/sync_versions.py --apply
```

**Plugins with unified versioning:**
- plugin-security-checker (v3.2.0)
- security-report-builder (v1.2.0)

---

## Session Summary (2025-12-20)

### Completed This Session

| Commit | Plugin | Version | Issue |
|--------|--------|---------|-------|
| `ac8e000` | plugin-security-checker | v3.2.0 | #6 ✅ Closed |
| `ee6fbd8` | security-report-builder | v1.2.0 | #13 ✅ Closed |

**plugin-security-checker v3.2.0:**
- Unified version system (version.json + sync_versions.py)
- ATT&CK v18.1, ATLAS v4.5.0, OWASP 2021/2023, CWE 4.14
- --update and --check-updates CLI flags

**security-report-builder v1.2.0:**
- Unified version system implemented
- Fixed: scan_result_parser.py - parse_file() results list bug
- Fixed: context_analyzer.py - case-insensitive rule matching
- Fixed: generate_report.py - logger initialization
- Added: references/framework_mappings.json
- Updated: agent frontmatter (name, trigger, tools)

### Remaining Plugin Reviews

| Issue | Plugin | Version | Status |
|-------|--------|---------|--------|
| #7 | gdpr-auditor | v1.2.0 | Pending |
| #8 | cybersecurity-policy-generator | v1.2.0 | Pending |
| #9 | incident-response-playbook-creator | v2.2.0 | Pending |
| #10 | pdf-smart-extractor | v2.2.0 | Pending |
| #11 | xlsx-smart-extractor | v2.2.0 | Pending |
| #12 | docx-smart-extractor | v2.2.0 | Pending |
| #14 | chrome-devtools-optimizer | v1.0.1 | Pending |

### Review Checklist for Each Plugin

1. Check plugin.json manifest format (agents as array of .md strings)
2. Check agent file frontmatter (name, description, trigger, tools)
3. Validate all JSON files
4. Test main scripts compile and run
5. Implement unified version system (version.json + sync_versions.py)
6. Update marketplace.json with new version
