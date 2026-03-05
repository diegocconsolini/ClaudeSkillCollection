# Audit Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all 15 verified issues from the complete project audit (GitHub Issue #25)

**Architecture:** Sequential fixes grouped by priority. Critical issues first (data exposure, missing files, broken SKILL.md), then High (XSS, missing SKILL.md, missing deps), then Medium. Each task is one logical change with a commit.

**Tech Stack:** Python, Markdown, YAML, JSON, git, gh CLI

**Repo:** `/Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection`
**Branch:** Create `fix/audit-issues-25` from current HEAD
**Issue:** #25

---

### Task 1: Create feature branch

**Step 1: Create and checkout branch**

```bash
git checkout main && git pull && git checkout -b fix/audit-issues-25
```

**Step 2: Verify**

```bash
git branch --show-current
```
Expected: `fix/audit-issues-25`

---

### Task 2: Remove sensitive business data from repo (C1)

**Context:** The repo is PUBLIC. 14+ financial/business files in `docs/` are git-tracked. These include AOP financials, pricing sheets, contracting trackers, and employee activity logs.

**Files:**
- Modify: `.gitignore`
- Delete from git tracking: 14+ files in `docs/`

**Step 1: Add patterns to .gitignore to prevent re-adding**

Append to `.gitignore`:

```
# Sensitive business/financial documents
docs/*.xlsm
docs/*.xlsx
docs/*.csv
docs/*.pbix
docs/*.zip
```

**Step 2: Remove sensitive files from git tracking (keep local copies)**

```bash
git rm --cached "docs/AOP24 IT Operations Financials.xlsm"
git rm --cached "docs/AOP25 IT Operations Financials (Diego Local Edit).xlsm"
git rm --cached "docs/AOP25 IT Operations Financials .xlsm"
git rm --cached "docs/AOP26 preview IT Operations Financials .xlsm"
git rm --cached "docs/AOP26 preview IT Operations Financials Final.xlsm"
git rm --cached "docs/5.A Pricing Sheet 250331 HCLTech JDE.xlsx"
git rm --cached "docs/CONTRACTING TRACKER-MUSIC 3.xlsx"
git rm --cached "docs/Finance Overview template.xlsx"
git rm --cached "docs/Security and Compliance AOP26 Review version.xlsx"
git rm --cached "docs/Security and Compliance AOP26 Review version v2.xlsx"
git rm --cached "docs/Security and Compliance AOP26 Review version v3.xlsx"
git rm --cached "docs/Security and Compliance AOP26 Review version v4.xlsx"
git rm --cached "docs/AOP2024 Cyber details.xlsx"
git rm --cached "docs/ABM-ActivityLog_Oct-22-2025_6-59-58.csv"
git rm --cached "docs/AOP Dashboard.pbix"
git rm --cached "docs/iTerm2-3_6_5.zip"
git rm --cached "docs/iTermAI-1.1.zip"
```

Also remove the CCM bundle xlsx files:

```bash
git rm --cached "docs/CCMv4.0.12+CAIQv4.0.3-Bundle_Generated-at_2024-06-03/CAIQv4.0.3_STAR-Security-Questionnaire_Generated-at_2024-06-03.xlsx"
git rm --cached "docs/CCMv4.0.12+CAIQv4.0.3-Bundle_Generated-at_2024-06-03/CCMv4.0.12_Generated-at_2024-06-03.xlsx"
```

**Step 3: Verify files still exist locally but not in git**

```bash
ls "docs/AOP24 IT Operations Financials.xlsm"  # Should exist on disk
git ls-files -- "docs/*.xlsm"  # Should return nothing
```

**Step 4: Commit**

```bash
git add .gitignore
git commit -m "security: remove sensitive business/financial data from git tracking

Files removed from tracking (kept locally):
- AOP financial spreadsheets (6 files)
- Pricing sheets and contracting trackers
- Employee activity log
- Application installers

Added .gitignore patterns to prevent re-adding.

Note: Files remain in git history. Consider BFG Repo-Cleaner
for complete removal if needed.

Fixes part of #25 (C1)"
```

---

### Task 3: Create requirements.txt for incident-response-playbook-creator (C2)

**Files:**
- Create: `incident-response-playbook-creator/requirements.txt`

**Step 1: Create requirements.txt**

Write to `incident-response-playbook-creator/requirements.txt`:

```
jinja2>=3.0.0
```

**Step 2: Verify the import matches**

```bash
grep "from jinja2" incident-response-playbook-creator/scripts/generate_playbook_markdown.py
```
Expected: `from jinja2 import Template`

**Step 3: Commit**

```bash
git add incident-response-playbook-creator/requirements.txt
git commit -m "fix: add missing requirements.txt for incident-response-playbook-creator

Script generate_playbook_markdown.py has hard import of jinja2
with no try/except. Without requirements.txt users have no way
to know they need to install it.

Fixes #25 (C2)"
```

---

### Task 4: Add missing files to desktop security-report-builder (C3)

**Files:**
- Create: `claude-desktop-skills/security-report-builder/requirements.txt`
- Create: `claude-desktop-skills/security-report-builder/config/branding.json`
- Create: `claude-desktop-skills/security-report-builder/config/report_config.json`
- Create: `claude-desktop-skills/security-report-builder/config/severity_rules.json`
- Create: `claude-desktop-skills/security-report-builder/references/framework_mappings.json`

**Step 1: Copy files from root plugin**

```bash
cp security-report-builder/requirements.txt claude-desktop-skills/security-report-builder/requirements.txt
mkdir -p claude-desktop-skills/security-report-builder/config
cp security-report-builder/config/branding.json claude-desktop-skills/security-report-builder/config/
cp security-report-builder/config/report_config.json claude-desktop-skills/security-report-builder/config/
cp security-report-builder/config/severity_rules.json claude-desktop-skills/security-report-builder/config/
mkdir -p claude-desktop-skills/security-report-builder/references
cp security-report-builder/references/framework_mappings.json claude-desktop-skills/security-report-builder/references/
```

**Step 2: Verify all files exist**

```bash
ls claude-desktop-skills/security-report-builder/requirements.txt
ls claude-desktop-skills/security-report-builder/config/
ls claude-desktop-skills/security-report-builder/references/
```

**Step 3: Commit**

```bash
git add claude-desktop-skills/security-report-builder/requirements.txt \
        claude-desktop-skills/security-report-builder/config/ \
        claude-desktop-skills/security-report-builder/references/
git commit -m "fix: add missing requirements.txt, config/, and references/ to desktop security-report-builder

Skill.md metadata declares dependencies: requirements.txt but the file
was missing. Also missing config/ (branding, report config, severity rules)
and references/framework_mappings.json needed for MITRE mappings.

Copied from root security-report-builder/ plugin.

Fixes #25 (C3)"
```

---

### Task 5: Add missing requirements.txt to desktop pdf-smart-extractor (C4)

**Files:**
- Create: `claude-desktop-skills/pdf-smart-extractor/requirements.txt`

**Step 1: Copy from root plugin**

```bash
cp pdf-smart-extractor/requirements.txt claude-desktop-skills/pdf-smart-extractor/requirements.txt
```

**Step 2: Verify**

```bash
cat claude-desktop-skills/pdf-smart-extractor/requirements.txt
```
Expected: `pymupdf>=1.23.0`

**Step 3: Commit**

```bash
git add claude-desktop-skills/pdf-smart-extractor/requirements.txt
git commit -m "fix: add missing requirements.txt to desktop pdf-smart-extractor

Skill.md metadata declares dependencies: requirements.txt but file was missing.

Fixes #25 (C4)"
```

---

### Task 6: Add YAML frontmatter to 3 root SKILL.md files (C5)

**Files:**
- Modify: `incident-response-playbook-creator/SKILL.md`
- Modify: `pdf-smart-extractor/SKILL.md`
- Modify: `security-report-builder/SKILL.md`

**Step 1: Add frontmatter to incident-response-playbook-creator/SKILL.md**

Prepend before the existing `# Incident Response Playbook Creator` line:

```yaml
---
name: incident-response-playbook-creator
description: Create comprehensive incident response playbooks based on NIST SP 800-61r3, CISA federal playbooks, and regulatory requirements (GDPR Article 33/34, HIPAA Breach Notification). Covers 11 incident scenarios with step-by-step procedures.
license: MIT
---

```

**Step 2: Add frontmatter to pdf-smart-extractor/SKILL.md**

Prepend before the existing `# PDF Smart Extractor` line:

```yaml
---
name: pdf-smart-extractor
description: Extract and analyze large PDFs (1MB-50MB+) with minimal token usage through local extraction, semantic chunking, and persistent caching. Uses PyMuPDF for extraction and SHAKE256 for cache keys.
license: MIT
---

```

**Step 3: Add frontmatter to security-report-builder/SKILL.md**

Prepend before the existing `# Security Report Builder` line:

```yaml
---
name: security-report-builder
description: Transform plugin security scanner results into professional reports (HTML, PDF, DOCX) with intelligent false positive filtering and MITRE ATT&CK/OWASP integration. Reduces false positive rate from 85-90% to under 20%.
license: MIT
---

```

**Step 4: Verify all start with ---**

```bash
for f in incident-response-playbook-creator pdf-smart-extractor security-report-builder; do
  echo "=== $f ===" && head -1 "$f/SKILL.md"
done
```
Expected: All show `---`

**Step 5: Commit**

```bash
git add incident-response-playbook-creator/SKILL.md pdf-smart-extractor/SKILL.md security-report-builder/SKILL.md
git commit -m "fix: add YAML frontmatter to 3 root SKILL.md files missing it

incident-response-playbook-creator, pdf-smart-extractor, and
security-report-builder SKILL.md files started with # Heading
instead of --- YAML frontmatter.

Fixes #25 (C5)"
```

---

### Task 7: Fix XSS in generate_complete_report.py (H1)

**Files:**
- Modify: `plugin-security-checker/scripts/generate_complete_report.py`

**Step 1: Add html import at top of file (after line 9)**

After `from pathlib import Path`, add:

```python
import html as html_module
```

**Step 2: Add escape helper function (after the imports, before first function)**

```python
def _esc(value) -> str:
    """HTML-escape a value from untrusted scan data."""
    return html_module.escape(str(value) if value is not None else '')
```

**Step 3: Wrap all finding data interpolations in _esc()**

In the HTML generation sections (around lines 645-680), replace every f-string interpolation of finding/plugin data. The pattern is:

Replace: `{plugin}` → `{_esc(plugin)}`
Replace: `{finding.get('description', 'Security Issue')}` → `{_esc(finding.get('description', 'Security Issue'))}`
Replace: `{finding.get('category')}` → `{_esc(finding.get('category'))}`
Replace: `{finding.get('subcategory')}` → `{_esc(finding.get('subcategory'))}`
Replace: `{finding.get('file')}` → `{_esc(finding.get('file'))}`
Replace: `{finding.get('impact', 'N/A')}` → `{_esc(finding.get('impact', 'N/A'))}`
Replace: `{finding.get('recommendation', 'Review code manually')}` → `{_esc(finding.get('recommendation', 'Review code manually'))}`
Replace: `{finding['code_snippet']}` → `{_esc(finding.get('code_snippet', ''))}`

Apply this pattern to ALL finding data interpolations throughout the file. Search for `finding.get(` and `finding[` in f-string contexts and wrap each with `_esc()`.

**Step 4: Verify no unescaped finding data remains**

```bash
grep -n "finding.get\|finding\[" plugin-security-checker/scripts/generate_complete_report.py | grep -v "_esc" | grep -v "^.*#" | grep "html +="
```
Expected: No output (all finding interpolations wrapped)

**Step 5: Commit**

```bash
git add plugin-security-checker/scripts/generate_complete_report.py
git commit -m "security: add HTML escaping to generate_complete_report.py

All finding data (descriptions, code snippets, categories, file paths)
from scanned plugins is now escaped before HTML interpolation.
Prevents XSS if a scanned plugin contains <script> in its code.

Fixes #25 (H1)"
```

---

### Task 8: Fix XSS in generate_html_report.py (H2)

**Files:**
- Modify: `plugin-security-checker/scripts/generate_html_report.py`

**Step 1: Add html import after line 7**

```python
import html as html_module
```

**Step 2: Add escape helper**

```python
def _esc(value) -> str:
    """HTML-escape a value from untrusted scan data."""
    return html_module.escape(str(value) if value is not None else '')
```

**Step 3: Wrap plugin data interpolations**

Around lines 474-501, replace:
- `{plugin['name']}` → `{_esc(plugin['name'])}`
- `{plugin['verdict']}` → `{_esc(plugin['verdict'])}`
- `{plugin['findings']}` is numeric, safe to leave

Apply to ALL plugin name/verdict interpolations in the file.

**Step 4: Commit**

```bash
git add plugin-security-checker/scripts/generate_html_report.py
git commit -m "security: add HTML escaping to generate_html_report.py

Plugin names and verdicts from scan results now escaped before
HTML interpolation.

Fixes #25 (H2)"
```

---

### Task 9: Fix XSS in security-report-builder html_generator.py (H3)

**Files:**
- Modify: `security-report-builder/scripts/generators/html_generator.py`

**Step 1: Add html import after line 7**

After `import logging`, add:

```python
import html as html_module
```

**Step 2: Add autoescape to Jinja2 Environment (line 37)**

Replace:
```python
                self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
```
With:
```python
                self.env = Environment(
                    loader=FileSystemLoader(str(self.template_dir)),
                    autoescape=True
                )
```

**Step 3: Add escape helper**

After the class imports section, add a module-level helper:

```python
def _esc(value) -> str:
    """HTML-escape a value from untrusted scan data."""
    return html_module.escape(str(value) if value is not None else '')
```

**Step 4: Wrap finding data interpolations in _generate_inline_html method**

Around lines 495-541, wrap all finding data:
- `{plugin.get('plugin_name', 'unknown')}` → `{_esc(plugin.get('plugin_name', 'unknown'))}`
- `{plugin['risk_score']}` is numeric, safe
- `{plugin['risk_level']}` → `{_esc(plugin['risk_level'])}`
- `{category}` → `{_esc(category)}`
- `{plugin}` (when it's a name string) → `{_esc(plugin)}`
- `{description}` → `{_esc(description)}`
- `{code[:500]}` → `{_esc(code[:500])}`
- `{tech}` → `{_esc(tech)}`
- `{cat}` → `{_esc(cat)}`

**Step 5: Commit**

```bash
git add security-report-builder/scripts/generators/html_generator.py
git commit -m "security: add HTML escaping and Jinja2 autoescape to html_generator.py

Added autoescape=True to Jinja2 Environment. All finding data
(categories, descriptions, code snippets, framework tags) now
escaped before HTML interpolation.

Fixes #25 (H3)"
```

---

### Task 10: Create missing SKILL.md for 4 root plugins (H4)

**Files:**
- Create: `plugin-security-checker/SKILL.md`
- Create: `xlsx-smart-extractor/SKILL.md`
- Create: `docx-smart-extractor/SKILL.md`
- Create: `chrome-devtools-optimizer/SKILL.md`

**Step 1: Create plugin-security-checker/SKILL.md**

```markdown
---
name: plugin-security-checker
description: Advanced security scanner for Claude Code plugins with 91 specialized pattern detection agents. Performs static code analysis to detect vulnerabilities, code obfuscation, hardcoded credentials, and security anti-patterns. Features MITRE ATT&CK/ATLAS framework mapping and consensus voting across agents.
license: MIT
---

# Plugin Security Checker

Scan Claude Code plugins for security vulnerabilities before installation.

## Usage

Invoke when you need to analyze a plugin for security risks, detect dangerous patterns, or generate security reports.
```

**Step 2: Create xlsx-smart-extractor/SKILL.md**

```markdown
---
name: xlsx-smart-extractor
description: Extract and analyze large Excel spreadsheets with minimal token usage through local extraction with openpyxl, semantic sheet chunking, and persistent SHAKE256-based caching. Supports multi-sheet workbooks and formula extraction.
license: MIT
---

# Excel Smart Extractor

Extract and query large Excel files efficiently with persistent caching.

## Usage

Invoke when you need to analyze Excel spreadsheets, extract specific sheets or ranges, or query cached spreadsheet data.
```

**Step 3: Create docx-smart-extractor/SKILL.md**

```markdown
---
name: docx-smart-extractor
description: Extract and analyze large Word documents with minimal token usage through local extraction with python-docx, semantic chunking by headings, and persistent SHAKE256-based caching. Preserves document structure and formatting metadata.
license: MIT
---

# Word Document Smart Extractor

Extract and query large Word documents efficiently with persistent caching.

## Usage

Invoke when you need to analyze Word documents, extract specific sections, or query cached document data.
```

**Step 4: Create chrome-devtools-optimizer/SKILL.md**

```markdown
---
name: chrome-devtools-optimizer
description: Optimize Chrome DevTools usage for token efficiency. Provides patterns for screenshot analysis, DOM inspection, and network monitoring with minimal context window consumption. Supports optional Gemini Flash integration for image analysis.
license: MIT
---

# Chrome DevTools Optimizer

Optimize Chrome DevTools integration for minimal token usage.

## Usage

Invoke when working with Chrome DevTools MCP server to reduce token consumption during browser debugging and analysis tasks.
```

**Step 5: Verify all 4 files start with ---**

```bash
for d in plugin-security-checker xlsx-smart-extractor docx-smart-extractor chrome-devtools-optimizer; do
  echo "=== $d ===" && head -1 "$d/SKILL.md"
done
```
Expected: All show `---`

**Step 6: Commit**

```bash
git add plugin-security-checker/SKILL.md xlsx-smart-extractor/SKILL.md docx-smart-extractor/SKILL.md chrome-devtools-optimizer/SKILL.md
git commit -m "feat: create missing SKILL.md for 4 root plugins

Added SKILL.md with YAML frontmatter to:
- plugin-security-checker
- xlsx-smart-extractor
- docx-smart-extractor
- chrome-devtools-optimizer

Fixes #25 (H4)"
```

---

### Task 11: Add __main__ guard to demo_learning.py (H5)

**Files:**
- Modify: `plugin-security-checker/scripts/demo_learning.py`

**Step 1: Read the full file to understand structure**

The file is 143 lines. Line 1-12 are shebang/docstring/imports. Lines 14-143 are all module-level executable code (prints, orchestrator creation, scanning).

**Step 2: Wrap lines 14-143 in __main__ guard**

After the imports (after line 12), insert:

```python

if __name__ == "__main__":
```

Then indent all remaining lines (14-143) by 4 spaces.

**Step 3: Verify the file still runs**

```bash
cd /Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection
python -c "import ast; ast.parse(open('plugin-security-checker/scripts/demo_learning.py').read()); print('Syntax OK')"
```
Expected: `Syntax OK`

**Step 4: Commit**

```bash
git add plugin-security-checker/scripts/demo_learning.py
git commit -m "fix: add __main__ guard to demo_learning.py

All demo/scan code now runs only when executed directly,
not when imported as a module.

Fixes #25 (H5)"
```

---

### Task 12: Create requirements.txt for cybersecurity-policy-generator (H6)

**Files:**
- Create: `cybersecurity-policy-generator/requirements.txt`

**Step 1: Create requirements.txt**

Write to `cybersecurity-policy-generator/requirements.txt`:

```
# Optional dependencies for document generation
# Scripts handle missing packages gracefully via try/except
python-docx>=0.8.11
markdown2>=2.4.0
weasyprint>=60.0
```

**Step 2: Commit**

```bash
git add cybersecurity-policy-generator/requirements.txt
git commit -m "fix: add missing requirements.txt for cybersecurity-policy-generator

generate_docx_html_pdf.py uses python-docx, markdown2, and weasyprint.
Imports are wrapped in try/except but users had no way to discover
what to install.

Fixes #25 (H6)"
```

---

### Task 13: Update CLAUDE.md desktop skills ready count (H7)

**Files:**
- Modify: `CLAUDE.md`

**Step 1: After Tasks 4 and 5 are complete, the count is back to 8**

No change needed - Tasks 4 and 5 restore the missing files, making the "8 of 9" claim accurate again.

**Step 2: Verify by checking both desktop skills now have requirements.txt**

```bash
ls claude-desktop-skills/security-report-builder/requirements.txt
ls claude-desktop-skills/pdf-smart-extractor/requirements.txt
```
Expected: Both exist

**This task requires no file changes - it's resolved by Tasks 4 and 5.**

---

### Task 14: Fix docx-smart-extractor version mismatch (M1)

**Files:**
- Modify: `docx-smart-extractor/requirements.txt`

**Step 1: Update requirements.txt to match version.json**

Replace contents of `docx-smart-extractor/requirements.txt`:

```
python-docx>=1.1.0
```

**Step 2: Verify version.json matches**

```bash
grep "python-docx" docx-smart-extractor/version.json
```
Expected: `"python-docx": ">=1.1.0"`

**Step 3: Commit**

```bash
git add docx-smart-extractor/requirements.txt
git commit -m "fix: align docx-smart-extractor requirements.txt with version.json

Changed python-docx minimum from >=0.8.11 to >=1.1.0 to match
the version declared in version.json.

Fixes #25 (M1)"
```

---

### Task 15: Fix stale version comment in plugin-security-checker requirements.txt (M2)

**Files:**
- Modify: `plugin-security-checker/requirements.txt`

**Step 1: Update version comment on line 2**

Replace:
```
# Version: 2.0.0 (STIX 2.1 Integration)
```
With:
```
# Version: 3.2.0 (STIX 2.1 Integration)
```

**Step 2: Commit**

```bash
git add plugin-security-checker/requirements.txt
git commit -m "fix: update stale version comment in plugin-security-checker requirements.txt

Comment said 2.0.0 but plugin is at 3.2.0.

Fixes #25 (M2)"
```

---

### Task 16: Add claude-guide to marketplace.json (M3)

**Files:**
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Read current marketplace.json to understand format**

Read `.claude-plugin/marketplace.json` and find the plugins array.

**Step 2: Add claude-guide entry**

Add to the plugins array (maintaining alphabetical order or at the end):

```json
    {
      "name": "claude-guide",
      "version": "1.0.0",
      "description": "Navigate the ClaudeSkillCollection documentation wiki with /claude-guide [topic]. Provides quick access to 60+ wiki pages covering installation, configuration, MCP servers, plugins, context optimization, and troubleshooting.",
      "author": {
        "name": "Diego Consolini",
        "email": "diego@diegocon.nl"
      },
      "keywords": ["documentation", "wiki", "navigation", "help"],
      "agents": ["./agents/claude-guide.md"]
    }
```

**Step 3: Update plugin count in marketplace.json header (if present)**

Check if there's a count field and update from 9 to 10.

**Step 4: Validate JSON**

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('Valid JSON')"
```
Expected: `Valid JSON`

**Step 5: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: add claude-guide to marketplace.json

Registers the documentation navigation skill in the marketplace
manifest. Updates plugin count from 9 to 10.

Fixes #25 (M3)"
```

---

### Task 17: Create pull request

**Step 1: Push branch**

```bash
git push -u origin fix/audit-issues-25
```

**Step 2: Create PR**

```bash
gh pr create --title "fix: resolve 15 verified audit issues from complete project audit" --body "$(cat <<'EOF'
## Summary

Fixes all 15 verified issues from the complete project audit.

Closes #25

## Changes by Priority

### Critical (5)
- **C1:** Remove 14+ sensitive business/financial files from git tracking, add .gitignore patterns
- **C2:** Add `requirements.txt` for incident-response-playbook-creator (hard jinja2 dependency)
- **C3:** Add missing `requirements.txt`, `config/`, `references/` to desktop security-report-builder
- **C4:** Add missing `requirements.txt` to desktop pdf-smart-extractor
- **C5:** Add YAML frontmatter to 3 root SKILL.md files

### High (7)
- **H1:** Add HTML escaping to `generate_complete_report.py` (XSS fix)
- **H2:** Add HTML escaping to `generate_html_report.py` (XSS fix)
- **H3:** Add HTML escaping + Jinja2 autoescape to `html_generator.py` (XSS fix)
- **H4:** Create missing SKILL.md for 4 root plugins
- **H5:** Add `__main__` guard to `demo_learning.py`
- **H6:** Add `requirements.txt` for cybersecurity-policy-generator
- **H7:** Resolved by C3+C4 (desktop skills count now accurate)

### Medium (3)
- **M1:** Align docx-smart-extractor requirements.txt with version.json
- **M2:** Fix stale version comment in plugin-security-checker requirements.txt
- **M3:** Add claude-guide to marketplace.json

## Test plan

- [ ] Verify `git ls-files -- "docs/*.xlsm" "docs/*.xlsx" "docs/*.csv"` returns empty
- [ ] Verify `python -c "from jinja2 import Template"` works (jinja2 installed)
- [ ] Verify all desktop skills with `dependencies: requirements.txt` have the file
- [ ] Verify all 9 root SKILL.md files start with `---`
- [ ] Verify no unescaped `finding.get(` in HTML f-strings in report generators
- [ ] Verify `demo_learning.py` has `if __name__ == "__main__":`
- [ ] Verify marketplace.json is valid JSON with 10 plugins
- [ ] Run `python3 -c "import ast; ast.parse(open('file').read())"` on all modified .py files

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Step 3: Return PR URL**

---

### Task 18: Update CLAUDE.md and README.md plugin count (if M3 approved)

**Files:**
- Modify: `CLAUDE.md` line 3
- Modify: `README.md` line 3 and badges

**Step 1: Update CLAUDE.md**

Replace: `This is a Claude Code plugin marketplace containing 9 professional security, compliance, and productivity plugins.`
With: `This is a Claude Code plugin marketplace containing 10 professional security, compliance, and productivity plugins.`

**Step 2: Update README.md badge**

Replace: `[![Plugins](https://img.shields.io/badge/plugins-9-green.svg)]`
With: `[![Plugins](https://img.shields.io/badge/plugins-10-green.svg)]`

**Step 3: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: update plugin count from 9 to 10 after adding claude-guide

Fixes #25 (M3 follow-up)"
```
