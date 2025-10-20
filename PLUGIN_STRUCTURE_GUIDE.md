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
- [ ] Tested plugin loads correctly in Claude Code
- [ ] Verified agents are invocable

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
