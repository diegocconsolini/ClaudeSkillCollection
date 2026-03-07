# Documentation Update Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix 12 verified documentation issues found during fact-based investigation (GitHub Issue #23)

**Architecture:** Direct file edits to CLAUDE.md, README.md, plugin manifests, and desktop skill metadata. No code changes - documentation only.

**Tech Stack:** Markdown, JSON, YAML frontmatter, git, gh CLI

---

### Task 1: Create feature branch

**Files:**
- None (git operation only)

**Step 1: Create and checkout branch**

```bash
git checkout -b docs/fact-based-documentation-update
```

**Step 2: Verify branch**

```bash
git branch --show-current
```
Expected: `docs/fact-based-documentation-update`

---

### Task 2: Fix hardcoded paths in CLAUDE.md (Issue #1)

**Files:**
- Modify: `CLAUDE.md:25-26,152`

**Step 1: Replace line 25**

Replace:
```
**Location:** `/home/diegocc/ClaudeSkillCollection/claude-desktop-skills/`
```
With:
```
**Location:** `./claude-desktop-skills/`
```

**Step 2: Replace line 26**

Replace:
```
**Packages:** `/home/diegocc/ClaudeSkillCollection/claude-desktop-skills/packages/`
```
With:
```
**Packages:** `./claude-desktop-skills/packages/`
```

**Step 3: Replace line 152**

Replace:
```
**Location:** `/home/diegocc/ClaudeSkillCollection/claude-desktop-skills/packages/`
```
With:
```
**Location:** `./claude-desktop-skills/packages/`
```

**Step 4: Verify no more hardcoded paths**

```bash
grep -n "/home/diegocc" CLAUDE.md
```
Expected: No output (no matches)

**Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "fix: replace hardcoded /home/diegocc/ paths with relative paths in CLAUDE.md"
```

---

### Task 3: Fix Skill.md naming and frontmatter documentation (Issues #2, #4, #9)

**Files:**
- Modify: `CLAUDE.md:49-65`

**Step 1: Replace the Package Format section**

Replace lines 49-65 (from `### Package Format` through `**Total Package Size:**`):

```markdown
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
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: clarify plugin vs desktop skill format differences in CLAUDE.md"
```

---

### Task 4: Fix version numbers and sizes in CLAUDE.md (Issues #6, #7, #8, #10)

**Files:**
- Modify: `CLAUDE.md:9,17,29-36,39,81`

**Step 1: Fix wiki page count (line 9)**

Replace: `53 comprehensive pages covering:`
With: `60+ comprehensive pages covering:`

**Step 2: Fix example count (line 17)**

Replace: `- Examples (14 copy-paste examples)`
With: `- Examples (13 copy-paste examples)`

**Step 3: Add version numbers to plugin listings (lines 29-36)**

Replace:
```
✅ **gdpr-auditor** (57 KB) - GDPR compliance auditing
✅ **cybersecurity-policy-generator** (168 KB) - Security policy generator
✅ **incident-response-playbook-creator** (85 KB) - IR playbook creator (11 scenarios)
✅ **security-report-builder** (35 KB) - Security report generator
✅ **pdf-smart-extractor** (17 KB) - PDF extraction with caching
✅ **xlsx-smart-extractor** (16 KB) - Excel extraction with caching
✅ **docx-smart-extractor** (14 KB) - Word extraction with caching
✅ **chrome-devtools-optimizer** (30 KB) - Chrome DevTools token optimizer
```
With:
```
✅ **gdpr-auditor** v1.2.0 (57 KB) - GDPR compliance auditing
✅ **cybersecurity-policy-generator** v1.2.0 (168 KB) - Security policy generator
✅ **incident-response-playbook-creator** v2.2.0 (85 KB) - IR playbook creator (11 scenarios)
✅ **security-report-builder** v1.2.0 (35 KB) - Security report generator
✅ **pdf-smart-extractor** v2.2.0 (17 KB) - PDF extraction with caching
✅ **xlsx-smart-extractor** v2.2.0 (16 KB) - Excel extraction with caching
✅ **docx-smart-extractor** v2.2.0 (14 KB) - Word extraction with caching
✅ **chrome-devtools-optimizer** v1.0.1 (30 KB) - Chrome DevTools token optimizer
```

**Step 4: Fix plugin-security-checker size (line 39)**

Replace: `⏸️ **plugin-security-checker** (9.2 MB)`
With: `⏸️ **plugin-security-checker** v3.2.0 (9.1 MB)`

**Step 5: Fix security-report-builder version in repo structure (line 81)**

Replace: `│   ├── security-report-builder/            # v1.0.1`
With: `│   ├── security-report-builder/            # v1.2.0`

**Step 6: Commit**

```bash
git add CLAUDE.md
git commit -m "fix: correct page counts, sizes, and add version numbers to CLAUDE.md"
```

---

### Task 5: Fix security-report-builder version mismatch (Issue #3)

**Files:**
- Modify: `security-report-builder/.claude-plugin/plugin.json:3`

**Step 1: Update version in plugin.json**

Replace: `"version": "1.0.1",`
With: `"version": "1.2.0",`

**Step 2: Verify version.json matches**

```bash
cat security-report-builder/version.json | grep plugin_version
```
Expected: `"plugin_version": "1.2.0"`

**Step 3: Verify marketplace.json matches**

```bash
grep -A2 '"security-report-builder"' .claude-plugin/marketplace.json | grep version
```
Expected: `"version": "1.2.0"`

**Step 4: Commit**

```bash
git add security-report-builder/.claude-plugin/plugin.json
git commit -m "fix: correct security-report-builder version from 1.0.1 to 1.2.0 in plugin.json"
```

---

### Task 6: Fix desktop security-report-builder Skill.md version (Issue #11)

**Files:**
- Modify: `claude-desktop-skills/security-report-builder/Skill.md` (frontmatter)

**Step 1: Update version in frontmatter metadata**

Replace: `  version: 1.0.1`
With: `  version: 1.2.0`

**Step 2: Commit**

```bash
git add claude-desktop-skills/security-report-builder/Skill.md
git commit -m "fix: correct security-report-builder desktop skill version to 1.2.0"
```

---

### Task 7: Add Claude Desktop Skills section to README.md (Issue #5)

**Files:**
- Modify: `README.md` (insert after the Quick Start section, before Plugin Categories)

**Step 1: Add Desktop Skills section**

Insert before `## 📂 Plugin Categories` (line 68):

```markdown
## 🖥️ Claude Desktop Skills

8 skills are also available as Claude Desktop skill packages for use outside of Claude Code.

**Installation:**
1. Download the ZIP file from `claude-desktop-skills/packages/`
2. Open Claude Desktop → Skills menu → Import Skill
3. Select the downloaded ZIP file

**Available Skills:**

| Skill | Version | Size | Description |
|-------|---------|------|-------------|
| gdpr-auditor | v1.2.0 | 57 KB | GDPR compliance auditing |
| cybersecurity-policy-generator | v1.2.0 | 168 KB | Security policy generator |
| incident-response-playbook-creator | v2.2.0 | 85 KB | IR playbook creator (11 scenarios) |
| security-report-builder | v1.2.0 | 35 KB | Security report generator |
| pdf-smart-extractor | v2.2.0 | 17 KB | PDF extraction with caching |
| xlsx-smart-extractor | v2.2.0 | 16 KB | Excel extraction with caching |
| docx-smart-extractor | v2.2.0 | 14 KB | Word extraction with caching |
| chrome-devtools-optimizer | v1.0.1 | 30 KB | Chrome DevTools token optimizer |

**Note:** plugin-security-checker (v3.2.0, 9.1 MB) exceeds Claude Desktop's 30MB uncompressed limit. See `claude-desktop-skills/README.md` for details.

For migration guide between Claude Code plugins and Desktop skills, see `claude-desktop-skills/MIGRATION_GUIDE.md`.

---

```

**Step 2: Update wiki badge count (line 8)**

Replace: `[![Wiki](https://img.shields.io/badge/wiki-53_pages-purple.svg)]`
With: `[![Wiki](https://img.shields.io/badge/wiki-60%2B_pages-purple.svg)]`

**Step 3: Update wiki link text (line 14)**

Replace: `**[→ Full Documentation Wiki (53 pages)]`
With: `**[→ Full Documentation Wiki (60+ pages)]`

**Step 4: Update examples count (line 25)**

Replace: `| Examples | 14 copy-paste examples for CLAUDE.md, MCP, Workflows, Settings |`
With: `| Examples | 13 copy-paste examples for CLAUDE.md, MCP, Workflows, Settings |`

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: add Claude Desktop Skills section and fix page/example counts in README"
```

---

### Task 8: Add README to empty wiki/ directory (Issue #12)

**Files:**
- Create: `wiki/README.md`

**Step 1: Create wiki/README.md**

```markdown
# Wiki

The project wiki is hosted on GitHub:

https://github.com/diegocconsolini/ClaudeSkillCollection/wiki

This directory is intentionally empty. All wiki content is maintained through the GitHub Wiki interface.
```

**Step 2: Commit**

```bash
git add wiki/README.md
git commit -m "docs: add README to wiki/ directory explaining GitHub Wiki location"
```

---

### Task 9: Create pull request

**Step 1: Push branch**

```bash
git push -u origin docs/fact-based-documentation-update
```

**Step 2: Create PR**

```bash
gh pr create --title "docs: fix 12 documentation issues from fact-based investigation" --body "$(cat <<'EOF'
## Summary

Fixes 12 documentation issues identified through a comprehensive fact-based audit of all project documentation.

Closes #23

## Changes

- **CLAUDE.md:** Fix 3 hardcoded `/home/diegocc/` paths, clarify plugin vs desktop skill formats, fix page/example counts, add version numbers to plugin listings, correct ZIP size
- **README.md:** Add Claude Desktop Skills section, fix wiki page count badge, fix example count
- **security-report-builder plugin.json:** Correct version from 1.0.1 to 1.2.0 (accidentally reverted in commit 4624072)
- **security-report-builder Skill.md:** Correct version to 1.2.0
- **wiki/README.md:** New file explaining GitHub Wiki location

## Investigation Report

See `docs/plans/2026-03-02-documentation-update-design.md` for the full audit findings.

## Test plan

- [ ] Verify no hardcoded `/home/diegocc/` paths remain in CLAUDE.md
- [ ] Verify security-report-builder version is 1.2.0 in plugin.json, marketplace.json, version.json, and Skill.md
- [ ] Verify README.md Desktop Skills section renders correctly
- [ ] Verify wiki badge shows "60+" not "53"
- [ ] Verify all plugin manifest validation commands still pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Step 3: Return PR URL to user**
