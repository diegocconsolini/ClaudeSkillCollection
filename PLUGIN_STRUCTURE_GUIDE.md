# Claude Code Plugin Structure Guide

**Official Documentation Reference:** https://docs.claude.com/en/docs/claude-code/plugins-reference

---

## ⚠️ CRITICAL: Never Fabricate Plugin Structures

**ALWAYS** consult the official Claude Code documentation before creating plugin structures. Do NOT invent or guess field formats based on what "looks right" or what you see in other plugins.

**What went wrong previously:**
- I fabricated an `agents` field structure with object arrays containing `name`, `description`, `prompt` fields
- This structure **does not exist** in the official Claude Code specification
- It broke the **entire marketplace** from loading ANY plugins
- All 4 plugins had to be completely restructured

**Lesson:** When in doubt, READ THE DOCS. Don't speculate.

---

## Official Plugin Structure

### Directory Layout

```
your-plugin/
├── plugin.json              # REQUIRED: Plugin manifest
├── README.md                # REQUIRED: User-facing documentation
├── agents/                  # OPTIONAL: Specialized agents
│   └── agent-name.md       # Agent definition with frontmatter
├── commands/                # OPTIONAL: Slash commands
│   └── command-name.md     # Command definition
├── skills/                  # OPTIONAL: Skills (deprecated, use agents)
│   └── skill-name.md
├── hooks/                   # OPTIONAL: Event hooks
│   └── hook-name.sh
├── scripts/                 # OPTIONAL: Helper scripts
│   └── your-script.py
├── templates/               # OPTIONAL: Template files
├── references/              # OPTIONAL: Reference data
└── output/                  # OPTIONAL: Generated output
```

---

## plugin.json Schema

### Required Fields

```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Clear description of what the plugin does",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "license": "MIT"
}
```

### Optional Fields

```json
{
  "homepage": "https://github.com/username/repo/tree/main/plugin-name",
  "repository": "https://github.com/username/repo",
  "category": "security",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "requirements": {
    "python": ">=3.8",
    "dependencies": [
      "package>=version"
    ]
  },
  "agents": "./agents/",
  "commands": "./commands/",
  "skills": "./skills/",
  "hooks": "./hooks/",
  "scripts": {
    "script-name": "python3 scripts/script.py"
  }
}
```

---

## Agents Field - OFFICIAL FORMATS ONLY

### ✅ CORRECT Format 1: Directory Path (String)

```json
{
  "agents": "./agents/"
}
```

**What this means:** All `.md` files in the `agents/` directory are agent definitions.

### ✅ CORRECT Format 2: Array of File Paths

```json
{
  "agents": [
    "./agents/agent1.md",
    "./agents/agent2.md"
  ]
}
```

**What this means:** Only these specific files are agent definitions.

### ❌ WRONG - FABRICATED Structure (DO NOT USE)

```json
{
  "agents": [
    {
      "name": "agent-name",
      "description": "Agent description",
      "prompt": "./SKILL.md"
    }
  ]
}
```

**This structure is INVENTED and will break the marketplace.**

---

## Agent File Format

**Location:** `agents/your-agent-name.md`

**File Naming Convention:**
- Agent file name determines the agent identifier
- If plugin is named `my-plugin` and agent file is `my-agent.md`, the full agent name is `my-plugin:my-agent`
- If plugin is named `my-plugin` and agent file is `my-plugin.md`, the full agent name is `my-plugin:my-plugin`

**IMPORTANT:** Agent invocation uses fully qualified names: `plugin-name:agent-name`

**Structure:**
```markdown
---
description: Clear description of what this agent specializes in (1-2 sentences)
capabilities: ["capability1", "capability2", "capability3"]
---

# Agent Name

Your agent instructions go here...

## When to Use This Agent

Describe trigger conditions...

## Capabilities

Detail what the agent can do...

## Examples

Provide usage examples...
```

### Frontmatter Fields

- **description** (required): Short description of agent's purpose
- **capabilities** (required): Array of capability strings

---

## ⚠️ CRITICAL: Agent Frontmatter is MANDATORY

**COMMON MISTAKE THAT BREAKS MARKETPLACE LOADING:**

If you forget to add YAML frontmatter to your agent file, the plugin **will NOT appear** in Claude Code marketplace, even if:
- plugin.json is valid
- The plugin is committed and pushed to repository
- All other files are correct
- Marketplace.json includes the plugin entry

**What happened with docx-smart-extractor (October 2025):**
1. Created complete plugin with all scripts, README, plugin.json
2. Committed and pushed to repository
3. Added to marketplace.json v1.5.0
4. Plugin did NOT appear in Claude Code (showed 4 plugins instead of 6)
5. **Root cause:** Agent file started with `# DOCX Smart Extractor Agent` instead of frontmatter

### ❌ WRONG - Missing Frontmatter (Plugin Won't Load)

```markdown
# DOCX Smart Extractor Agent

## Overview

The DOCX Smart Extractor enables efficient analysis...
```

**Result:** Plugin exists in repository but is invisible in Claude Code marketplace.

### ✅ CORRECT - With Required Frontmatter

```markdown
---
description: Extract and analyze Word documents (1MB-50MB+) with minimal token usage through local extraction, semantic chunking by headings, and intelligent caching.
capabilities: ["word-extraction", "table-extraction", "heading-structure", "token-optimization", "document-analysis", "policy-documents", "contract-analysis", "technical-reports"]
---

# DOCX Smart Extractor Agent

## Overview

The DOCX Smart Extractor enables efficient analysis...
```

**Result:** Plugin loads correctly and appears in marketplace.

### Validation Checklist Before Committing Agent Files

**ALWAYS verify these steps before committing:**

1. ✅ Agent file has YAML frontmatter block (starts with `---`)
2. ✅ Frontmatter has `description` field (string, 1-2 sentences)
3. ✅ Frontmatter has `capabilities` field (array of strings)
4. ✅ Frontmatter closes with `---` on its own line
5. ✅ Content starts AFTER the closing `---`
6. ✅ No other content appears before the frontmatter

**Quick validation command:**
```bash
# Check if agent file has frontmatter
head -5 agents/your-agent.md | grep -c "^---$"
# Should return "2" (opening and closing ---)
```

**If this returns 0 or 1, your agent file is missing frontmatter and the plugin will fail to load.**

---

**Verified Reality (as of October 20, 2025):**
- All 4 working plugins use agent filenames matching plugin names
- Example: `pdf-smart-extractor` plugin → `agents/pdf-smart-extractor.md` → invoked as `pdf-smart-extractor:pdf-smart-extractor`
- This creates redundant naming but is the working pattern observed in production

### Example Agent File

```markdown
---
description: Extract and analyze large PDFs with minimal token usage through local extraction and semantic chunking.
capabilities: ["pdf-extraction", "semantic-chunking", "token-optimization", "large-document-analysis"]
---

# PDF Smart Extractor

## When to Use This Agent

Use this agent when:
- User provides a PDF file path with file size >1MB
- User encounters "PDF too large" errors
- User needs to analyze technical documentation (NIST, ISO, AWS guides)

## Capabilities

1. **Local PDF Extraction** - Extract 100% of PDF content using PyMuPDF
2. **Semantic Chunking** - Split text at intelligent boundaries
3. **Efficient Querying** - Search chunks by keywords with 12-103x token reduction
4. **Persistent Caching** - One-time extraction, instant reuse

## Examples

[Detailed examples here...]
```

---

## Category Values

**Valid categories** (as seen in marketplace):
- `security` - Security and compliance tools
- `productivity` - General productivity tools
- `development` - Development tools
- `data` - Data analysis and processing
- `ai` - AI and machine learning tools

---

## Keywords Best Practices

- Use lowercase with hyphens (e.g., `security-policy`, not `Security Policy`)
- Include framework names (e.g., `iso-27001`, `nist-csf`, `gdpr`)
- Include technology names (e.g., `python`, `pymupdf`, `pdf`)
- Include use case keywords (e.g., `compliance`, `audit`, `incident-response`)
- Aim for 8-15 keywords for discoverability

---

## Requirements Field

### Python Dependencies

```json
{
  "requirements": {
    "python": ">=3.8",
    "dependencies": [
      "pymupdf>=1.23.0",
      "jinja2>=3.0.0",
      "pyyaml>=6.0"
    ]
  }
}
```

### Node.js Dependencies

```json
{
  "requirements": {
    "node": ">=18.0.0",
    "dependencies": [
      "typescript@^5.0.0",
      "axios@^1.6.0"
    ]
  }
}
```

---

## Scripts Field

Define callable scripts for your plugin:

```json
{
  "scripts": {
    "extract": "python3 scripts/extract_pdf.py",
    "chunk": "python3 scripts/semantic_chunker.py",
    "query": "python3 scripts/query_pdf.py"
  }
}
```

**Usage:** Scripts can be invoked via the plugin's workflow.

---

## Marketplace Integration

### marketplace.json Structure

Located at: `.claude-plugin/marketplace.json`

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "marketplace-name",
  "version": "1.0.0",
  "description": "Marketplace description",
  "owner": {
    "name": "Owner Name",
    "email": "owner@example.com"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "source": "./plugin-directory",
      "version": "1.0.0",
      "author": {
        "name": "Author Name",
        "email": "author@example.com"
      },
      "category": "security",
      "keywords": ["keyword1", "keyword2"],
      "homepage": "https://github.com/username/repo/tree/main/plugin-name",
      "repository": "https://github.com/username/repo",
      "license": "MIT"
    }
  ]
}
```

**Key Points:**
- `source` field points to plugin directory (relative path)
- Each plugin in marketplace must have a valid `plugin.json` in its source directory
- Marketplace metadata should match plugin.json metadata

### ⚠️ CRITICAL: Version Synchronization Between Files

**IMPORTANT:** When you update plugin versions, you MUST update versions in TWO places:

1. **Individual plugin.json files** - `your-plugin/plugin.json`
2. **Marketplace catalog** - `.claude-plugin/marketplace.json`

**Why both are required:**
- Claude Code's `/plugin` command reads from `.claude-plugin/marketplace.json` to display the marketplace UI
- Updating only the individual `plugin.json` files will NOT update the version shown in Claude Code
- Both files must be kept in sync for users to see correct version numbers

**Example workflow for version updates:**

```bash
# Step 1: Update individual plugin.json files
# Edit: cybersecurity-policy-generator/plugin.json
#   "version": "1.0.0" → "version": "1.1.0"

# Edit: gdpr-auditor/plugin.json
#   "version": "1.0.0" → "version": "1.1.0"

# Step 2: Update marketplace.json with matching versions
# Edit: .claude-plugin/marketplace.json
#   Find each plugin entry and update its version field:
#   "version": "1.0.0" → "version": "1.1.0"

# Step 3: Commit both changes together
git add */plugin.json .claude-plugin/marketplace.json
git commit -m "Bump plugin versions to x.1.0"
git push origin main

# Step 4: Wait 1-5 minutes for GitHub CDN to update

# Step 5: In Claude Code, refresh marketplace
/plugin marketplace refresh  # or similar command

# Step 6: Verify versions in Claude Code
/plugin  # Check that new versions are displayed
```

**Real-World Issue (October 2025):**
- Updated 7 plugin.json files from x.0.0 → x.1.0
- Pushed to GitHub and waited for CDN refresh
- Claude Code still showed old versions (x.0.0)
- **Root cause:** `.claude-plugin/marketplace.json` was not updated
- **Solution:** Updated marketplace.json versions to match plugin.json versions
- Result: Versions immediately appeared correctly in Claude Code after push

**Verification checklist when updating versions:**
- [ ] Updated version in individual plugin's `plugin.json`
- [ ] Updated version in `.claude-plugin/marketplace.json` entry
- [ ] Both version numbers match exactly
- [ ] Committed and pushed both files together
- [ ] Waited 1-5 minutes for GitHub CDN cache
- [ ] Refreshed marketplace in Claude Code
- [ ] Verified new version displays in `/plugin` UI

---

## Testing Plugin Structure

### 1. Validate JSON Files

```bash
# Validate plugin.json
python3 -m json.tool plugin.json

# Validate marketplace.json
python3 -m json.tool .claude-plugin/marketplace.json
```

### 2. Check Directory Structure

```bash
# Verify required files exist
ls -la plugin.json README.md

# Check agents directory if defined
ls -la agents/

# Verify agent files have frontmatter
head -n 5 agents/*.md
```

### 3. Verify Frontmatter Format

Agent files MUST start with:
```markdown
---
description: ...
capabilities: [...]
---
```

**Not:**
```markdown
---
name: ...
description: ...
license: ...
---
```

The `name` and `license` fields belong in `plugin.json`, NOT in agent frontmatter.

---

## Observed Agent Behavior (Reality Check)

**Test Date:** October 20, 2025

### Agent Invocation Names

When Claude Code loads plugins, agents are registered with **fully qualified names** in the format: `plugin-name:agent-name`

**Example from actual error message:**
```
Error: Agent type 'cybersecurity-policy-generator' not found.
Available agents: ..., cybersecurity-policy-generator:cybersecurity-policy-generator, ...
```

**What this means:**
- ❌ **Incorrect invocation:** `cybersecurity-policy-generator` (fails)
- ✅ **Correct invocation:** `cybersecurity-policy-generator:cybersecurity-policy-generator` (works)

**Observed pattern in working plugins:**
- Plugin: `pdf-smart-extractor`
  - Agent file: `agents/pdf-smart-extractor.md`
  - Invocation: `pdf-smart-extractor:pdf-smart-extractor`

- Plugin: `gdpr-auditor`
  - Agent file: `agents/gdpr-auditor.md`
  - Invocation: `gdpr-auditor:gdpr-auditor`

- Plugin: `incident-response-playbook-creator`
  - Agent file: `agents/incident-response-playbook-creator.md`
  - Invocation: `incident-response-playbook-creator:incident-response-playbook-creator`

**Key Insight:**
- Agent filename (without .md) becomes the second part of the qualified name
- Plugin name becomes the first part
- Both parts are required for invocation

### Built-in Agents (No Prefix)

Built-in Claude Code agents don't require plugin prefix:
- `general-purpose`
- `Explore`
- `debugger`
- `code-reviewer`
- `python-pro`
- etc.

Only **plugin-provided agents** require the `plugin-name:agent-name` format.

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Fabricating Plugin Structures
**Wrong:** Creating plugin.json fields that don't exist in the official docs
**Right:** Only use fields documented in https://docs.claude.com/en/docs/claude-code/plugins-reference

### ❌ Mistake 2: Using SKILL.md at Plugin Root
**Wrong:** `your-plugin/SKILL.md`
**Right:** `your-plugin/agents/your-agent.md`

Agent definitions belong in the `agents/` directory, not at the plugin root.

### ❌ Mistake 3: Missing Frontmatter
**Wrong:**
```markdown
# Agent Name
Instructions...
```

**Right:**
```markdown
---
description: What the agent does
capabilities: ["cap1", "cap2"]
---

# Agent Name
Instructions...
```

### ❌ Mistake 4: Wrong Frontmatter Fields
**Wrong:**
```yaml
---
name: agent-name
description: ...
license: MIT
---
```

**Right:**
```yaml
---
description: ...
capabilities: [...]
---
```

### ❌ Mistake 5: Inconsistent Metadata
**Wrong:** Different versions/descriptions in plugin.json vs marketplace.json
**Right:** Ensure all metadata matches across files

---

## Checklist for New Plugins

- [ ] Created `plugin.json` with required fields ($schema, name, version, description, author, license)
- [ ] Added optional fields (homepage, repository, category, keywords) for discoverability
- [ ] If using agents: Set `"agents": "./agents/"` in plugin.json
- [ ] Created `agents/` directory
- [ ] Created agent files in `agents/` with proper frontmatter (description, capabilities)
- [ ] Validated all JSON files with `python3 -m json.tool`
- [ ] Created comprehensive `README.md` with usage examples
- [ ] Added plugin to `.claude-plugin/marketplace.json` if publishing
- [ ] **IMPORTANT:** Ensured version in `plugin.json` matches version in `.claude-plugin/marketplace.json`
- [ ] Tested plugin loads correctly in Claude Code
- [ ] Verified agents are invocable

## Checklist for Version Updates

- [ ] Updated version in individual plugin's `plugin.json`
- [ ] Updated version in `.claude-plugin/marketplace.json` entry for the same plugin
- [ ] Verified both version numbers match exactly
- [ ] Validated both JSON files with `python3 -m json.tool`
- [ ] Committed both files together in same commit
- [ ] Pushed to remote repository
- [ ] Waited 1-5 minutes for GitHub CDN cache to update
- [ ] Refreshed marketplace in Claude Code (`/plugin marketplace refresh` or restart)
- [ ] Verified new version displays correctly in `/plugin` UI

---

## Real-World Examples

### Example 1: PDF Smart Extractor

**Directory Structure:**
```
pdf-smart-extractor/
├── plugin.json
├── README.md
├── SKILL.md (legacy, for reference)
├── agents/
│   └── pdf-smart-extractor.md
├── scripts/
│   ├── extract_pdf.py
│   ├── semantic_chunker.py
│   └── query_pdf.py
├── examples/
├── output/
└── templates/
```

**plugin.json:**
```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "pdf-smart-extractor",
  "version": "1.0.0",
  "description": "Extract and analyze large PDFs (3MB-10MB+) with minimal token usage.",
  "author": {
    "name": "Diego Consolini",
    "email": "diego@diegocon.nl"
  },
  "license": "MIT",
  "category": "productivity",
  "keywords": ["pdf", "extraction", "token-optimization"],
  "requirements": {
    "python": ">=3.8",
    "dependencies": ["pymupdf>=1.23.0"]
  },
  "agents": "./agents/",
  "scripts": {
    "extract": "python3 scripts/extract_pdf.py",
    "chunk": "python3 scripts/semantic_chunker.py",
    "query": "python3 scripts/query_pdf.py"
  }
}
```

**agents/pdf-smart-extractor.md:**
```markdown
---
description: Extract and analyze large PDFs with minimal token usage through local extraction and semantic chunking.
capabilities: ["pdf-extraction", "semantic-chunking", "token-optimization", "large-document-analysis"]
---

# PDF Smart Extractor

[Agent instructions...]
```

### Example 2: GDPR Auditor

**Directory Structure:**
```
gdpr-auditor/
├── plugin.json
├── README.md
├── agents/
│   └── gdpr-auditor.md
├── references/
│   └── gdpr-articles.json
└── scripts/
    └── audit_code.py
```

**plugin.json:**
```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "gdpr-auditor",
  "version": "1.0.0",
  "description": "Comprehensive GDPR compliance auditing plugin.",
  "author": {
    "name": "Diego Consolini",
    "email": "diego@diegocon.nl"
  },
  "license": "MIT",
  "category": "security",
  "keywords": ["gdpr", "compliance", "privacy", "audit"],
  "agents": "./agents/"
}
```

**agents/gdpr-auditor.md:**
```markdown
---
description: Comprehensive GDPR compliance auditing that analyzes code, databases, and configurations for EU data protection.
capabilities: ["gdpr-compliance-audit", "privacy-analysis", "data-protection-assessment"]
---

# GDPR Auditor

[Agent instructions...]
```

---

## Version History

**v1.0 (Current)** - October 20, 2025
- Initial documentation based on official Claude Code Plugins Reference
- Documented correct `agents` field format (string path or array of file paths)
- Documented agent frontmatter format (description + capabilities)
- Added real-world examples from working plugins
- Created comprehensive checklist for plugin creation

---

## References

- **Official Claude Code Plugins Reference:** https://docs.claude.com/en/docs/claude-code/plugins-reference
- **Plugin Schema:** https://anthropic.com/claude-code/plugin.schema.json
- **Marketplace Schema:** https://anthropic.com/claude-code/marketplace.schema.json

---

**Remember:** When in doubt, ALWAYS consult the official documentation. Never fabricate or guess plugin structures.
