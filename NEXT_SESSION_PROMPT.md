# Continue Claude Desktop Skills Migration

## Current Status
Working directory: `/home/diegocc/ClaudeSkillCollection`

**Progress:** 6 of 9 skills complete (Phase 2 of 4)

**Completed:**
- ✅ Phase 1: 5 skills with existing Skill.md converted (gdpr-auditor, cybersecurity-policy-generator, incident-response-playbook-creator, security-report-builder, pdf-smart-extractor)
- ✅ Phase 2 (partial): xlsx-smart-extractor Skill.md created

**Remaining:**
- ⏳ Phase 2: docx-smart-extractor (create Skill.md from agents/docx-smart-extractor.md)
- ⏳ Phase 2: plugin-security-checker (create Skill.md from agents/plugin-security-checker.md)
- ⏳ Phase 3: chrome-devtools-optimizer (create Skill.md from agents/chrome-devtools-optimizer.md - MOST COMPLEX)
- ⏳ Phase 4: Create CHANGELOG.md and MIGRATION_GUIDE.md
- ⏳ Package all 9 skills as ZIP files

## Quick Resume Instructions

Continue the Claude Desktop skills migration project:

1. **Review current state:**
   ```bash
   cd /home/diegocc/ClaudeSkillCollection
   ls -la claude-desktop-skills/
   cat CLAUDE.md  # See project status
   cat /home/diegocc/.claude/plans/fluttering-foraging-torvalds.md  # See full plan
   ```

2. **Create Skill.md for docx-smart-extractor:**
   - Source: `docx-smart-extractor/agents/docx-smart-extractor.md`
   - Transform frontmatter: remove `capabilities`, `tools`, `model`; add `license`, `metadata`
   - Copy scripts and requirements.txt
   - Create: `claude-desktop-skills/docx-smart-extractor/Skill.md`

3. **Create Skill.md for plugin-security-checker:**
   - Source: `plugin-security-checker/agents/plugin-security-checker.md`
   - This is complex (91 pattern agents, extensive scripts)
   - Keep Skill.md <500 lines, move details to references/
   - Copy all scripts/ and references/
   - Create requirements.txt for Python dependencies

4. **Create Skill.md for chrome-devtools-optimizer:**
   - Source: `chrome-devtools-optimizer/agents/chrome-devtools-optimizer.md`
   - **MOST COMPLEX**: Node.js scripts, Gemini API, MCP server dependency
   - Copy: scripts/, references/, patterns/
   - Add comprehensive setup section for MCP + Gemini
   - Include WSL2 instructions

5. **Create documentation:**
   - `claude-desktop-skills/CHANGELOG.md` - version history
   - `claude-desktop-skills/MIGRATION_GUIDE.md` - Claude Code vs Desktop comparison

6. **Package as ZIP files:**
   ```bash
   # Install zip if needed
   sudo apt install zip

   # Package each skill
   cd claude-desktop-skills
   for skill in */; do
     zip -r "../${skill%.zip}.zip" "$skill"
   done
   ```

## Critical Requirements

**File Naming:**
- MUST be `Skill.md` (capital S, lowercase kill)
- NOT `SKILL.md` or `skill.md`

**Frontmatter Format:**
```yaml
---
name: skill-name
description: Clear description including when to use (1-1024 chars)
license: MIT
compatibility: claude-desktop
metadata:
  version: X.Y.Z
  author: Diego Consolini
  category: [security/compliance/productivity]
  runtime: [python3/node.js]
  dependencies: requirements.txt  # if needed
---
```

**ZIP Structure:**
```
skill-name.zip
└── skill-name/
    ├── Skill.md
    ├── scripts/
    ├── references/
    └── requirements.txt (if Python)
```

## Templates

### docx-smart-extractor Frontmatter
```yaml
---
name: docx-smart-extractor
description: Process Word documents (1MB-50MB+) with token optimization through local extraction and caching. Preserves formatting, styles, and document structure.
license: MIT
compatibility: claude-desktop
metadata:
  version: 2.2.0
  author: Diego Consolini
  category: productivity
  runtime: python3
  dependencies: requirements.txt
---
```

### plugin-security-checker Frontmatter
```yaml
---
name: plugin-security-checker
description: Advanced security scanner for Claude Code plugins with 91 specialized pattern agents. Detects vulnerabilities, code obfuscation, and security anti-patterns across plugin manifests, agents, and scripts.
license: MIT
compatibility: claude-desktop
metadata:
  version: 3.2.0
  author: Diego Consolini
  category: security
  runtime: python3
  dependencies: requirements.txt
---
```

### chrome-devtools-optimizer Frontmatter
```yaml
---
name: chrome-devtools-optimizer
description: Reduce token consumption by 70-80% when using Chrome DevTools MCP through smart snapshot strategies and optional Gemini Flash vision processing. Includes decision trees, pattern guides, and automated optimization workflows.
license: MIT
compatibility: claude-desktop
metadata:
  version: 1.0.1
  author: Diego Consolini
  category: productivity
  requires-api: gemini-flash (optional)
  requires-mcp: chrome-devtools
  runtime: node.js
---
```

## Files to Reference

**For docx-smart-extractor:**
- Source: `/home/diegocc/ClaudeSkillCollection/docx-smart-extractor/agents/docx-smart-extractor.md`
- Scripts: `docx-smart-extractor/scripts/`
- Pattern: Similar to xlsx-smart-extractor (already completed)

**For plugin-security-checker:**
- Source: `/home/diegocc/ClaudeSkillCollection/plugin-security-checker/agents/plugin-security-checker.md`
- Scripts: `plugin-security-checker/scripts/` (30+ files)
- References: `plugin-security-checker/references/` (MITRE ATT&CK, CVE data)
- Requirements: `plugin-security-checker/requirements.txt`

**For chrome-devtools-optimizer:**
- Source: `/home/diegocc/ClaudeSkillCollection/chrome-devtools-optimizer/agents/chrome-devtools-optimizer.md`
- Scripts: `chrome-devtools-optimizer/scripts/*.js`
- References: `chrome-devtools-optimizer/references/*.md`
- Patterns: `chrome-devtools-optimizer/patterns/*.md`
- README: `chrome-devtools-optimizer/README.md` (has WSL2 instructions)

## Validation

After creating each skill:
```bash
# Verify structure
ls -la claude-desktop-skills/[skill-name]/Skill.md

# Test if ZIP-able
cd claude-desktop-skills
zip -r test.zip [skill-name]/
unzip -l test.zip  # Should show skill-name/ as root
rm test.zip
```

## Success Criteria

- [ ] All 9 skills have `Skill.md` (correct case)
- [ ] All frontmatter valid (no `capabilities`, `tools`, `model` fields)
- [ ] All scripts/ and references/ copied
- [ ] CHANGELOG.md created
- [ ] MIGRATION_GUIDE.md created
- [ ] All 9 skills packaged as `.zip` files
- [ ] ZIP files have correct structure (skill folder as root)

## Estimated Time Remaining

- docx-smart-extractor: 30 minutes (similar to xlsx)
- plugin-security-checker: 45 minutes (complex, many scripts)
- chrome-devtools-optimizer: 60 minutes (most complex, external deps)
- Documentation: 30 minutes
- Packaging: 15 minutes

**Total: ~3 hours**
