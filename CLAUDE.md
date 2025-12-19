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

## Session Summary (2025-12-19)

### Completed: security-report-builder v1.2.0

**Changes Made:**
1. Implemented unified version system (version.json + sync_versions.py)
2. Fixed bug: `scan_result_parser.py` - parse_file() wasn't adding to results list
3. Fixed bug: `context_analyzer.py` - rule keys not normalized to lowercase
4. Fixed bug: `generate_report.py` - logger used before defined
5. Added `references/framework_mappings.json` (was empty)
6. Updated agent frontmatter (added name, trigger, tools)
7. Updated marketplace.json with enhanced description

**Test Results:** ✅ All passing
- HTML report generation working
- Context-aware analysis correctly identifies false positives
- Version sync verified across all files

### Pending Commits

1. **plugin-security-checker v3.2.0** - Ready to commit (Issue #6)
2. **security-report-builder v1.2.0** - Ready to commit (Issue #13)

### Remaining Plugin Reviews (Issues #7-#12, #14)

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

1. Check plugin.json manifest format
2. Check agent file frontmatter (name, description, trigger, tools)
3. Validate JSON files
4. Test main scripts
5. Implement unified version system if missing
6. Update marketplace.json
