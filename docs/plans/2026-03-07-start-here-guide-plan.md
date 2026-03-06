# Start Here Guide — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a hub-and-spoke "Start Here" guide in the GitHub Wiki with 5 pages, consolidate QUICKSTART.md, and update existing docs to link to it.

**Architecture:** 5 wiki pages created via `gh` CLI (wiki API). Hub page links to 4 sub-pages. QUICKSTART.md becomes a redirect. README.md gets a Start Here badge. claude-guide skill gets a "start" topic.

**Tech Stack:** GitHub Wiki (Markdown), `gh` CLI, git

**Important:** The wiki/ directory is a gitlink to the GitHub Wiki repo. Wiki pages must be created by cloning the wiki repo separately (`git clone https://github.com/diegocconsolini/ClaudeSkillCollection.wiki.git`), adding files, and pushing. They cannot be added via the main repo.

---

### Task 1: Create branch and clone wiki repo

**Files:**
- Clone: `ClaudeSkillCollection.wiki/` (temporary working directory)

**Step 1: Create feature branch in main repo**

```bash
git checkout main
git pull origin main
git checkout -b feature/start-here-guide
```

**Step 2: Clone the wiki repo for editing**

```bash
cd /tmp
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.wiki.git
cd ClaudeSkillCollection.wiki
ls *.md | head -20
```

Expected: List of existing wiki markdown files.

**Step 3: Verify wiki structure**

```bash
wc -l *.md | tail -5
```

Expected: Line counts for existing wiki pages.

---

### Task 2: Create hub page — Start-Here.md (#27)

**Files:**
- Create: `/tmp/ClaudeSkillCollection.wiki/Start-Here.md`

**Step 1: Write the hub page**

Create `/tmp/ClaudeSkillCollection.wiki/Start-Here.md` with the following content (~80 lines):

```markdown
# Start Here

Welcome to the Security & Compliance Marketplace for Claude Code. Whether you're setting up Claude Code for the first time or looking for security tools, this guide gets you productive in 5 minutes.

## What's Your Goal?

| I want to... | Go to |
|---|---|
| Set up Claude Code for my project | [CLAUDE.md Templates](Start-Here:-CLAUDE.md-Templates) |
| Use security or compliance tools | [Security & Compliance Path](Start-Here:-Security-&-Compliance-Path) |
| Extract documents (PDF, Excel, Word) | [Plugin Installation](Start-Here:-Plugin-Installation) |
| I already use Claude Code — show me plugins | [Plugin Installation](Start-Here:-Plugin-Installation) |

## 5-Minute Setup Checklist

1. **Install Claude Code** — [Download](https://claude.com/claude-code) if you haven't already
2. **Create CLAUDE.md** in your project root — use our [templates](Start-Here:-CLAUDE.md-Templates)
3. **Add the marketplace:**
   ```bash
   /plugin marketplace add diegocconsolini/ClaudeSkillCollection
   ```
4. **Install a plugin** (pick one from [Plugin Installation](Start-Here:-Plugin-Installation)):
   ```bash
   /plugin install gdpr-auditor@security-compliance-marketplace
   ```
5. **Enable and restart** — run `/plugin`, enable the plugin, restart Claude Code

Done. You're ready to go.

## Top 5 Mistakes to Avoid

| Mistake | Why it's bad | Do this instead |
|---|---|---|
| CLAUDE.md over 300 lines | Wastes context tokens every session | Keep under 150 lines, use `.claude/rules/` for extras |
| Putting style guides in CLAUDE.md | Duplicates what linters already do | Use ESLint/Prettier/Black and reference them |
| Adding secrets or credentials | CLAUDE.md is committed to git | Use `.env` files and `.gitignore` |
| Installing marketplace with local path | Breaks remote updates | Always use `owner/repo` format |
| Never restarting sessions | Context fills up, Claude slows down | Start fresh sessions for new tasks |

## Deep Dive Resources

- [Your First Session](Start-Here:-Your-First-Session) — What to do after installing Claude Code
- [CLAUDE-CODE-GUIDE.md](https://github.com/diegocconsolini/ClaudeSkillCollection/blob/main/CLAUDE-CODE-GUIDE.md) — Comprehensive reference (918 lines)
- [Full Wiki](Home) — 60+ pages of documentation
- [Plugin READMEs](https://github.com/diegocconsolini/ClaudeSkillCollection#-plugin-categories) — Detailed docs for each plugin
```

**Step 2: Verify line count**

```bash
wc -l /tmp/ClaudeSkillCollection.wiki/Start-Here.md
```

Expected: Under 100 lines.

**Step 3: Commit to wiki repo**

```bash
cd /tmp/ClaudeSkillCollection.wiki
git add Start-Here.md
git commit -m "docs: add Start Here hub page (#27)"
```

---

### Task 3: Create CLAUDE.md Templates sub-page (#28)

**Files:**
- Create: `/tmp/ClaudeSkillCollection.wiki/Start-Here:-CLAUDE.md-Templates.md`

**Step 1: Write the templates page**

Create the file with (~100 lines):

- **Section 1: Decision Tree** — Which structure fits your project?
  - Simple project (<5 files): Just CLAUDE.md (~50 lines)
  - Medium project (5-20 files): CLAUDE.md + 2-3 rules in `.claude/rules/`
  - Complex project (20+ files, monorepo): Full modular structure

- **Section 2: Minimal Template** (~20 lines of template)
  ```markdown
  # Project Name
  ## Tech Stack
  - [language/framework]
  ## Quick Commands
  npm run dev    # Start dev server
  npm run build  # Build for production
  npm run test   # Run tests
  ## Key Patterns
  - [One important pattern, e.g., "All API routes in src/routes/"]
  ```

- **Section 3: Standard Template** (~30 lines of template)
  Same as minimal plus: Architecture section, Error handling conventions, Testing strategy, with `.claude/rules/coding.md` and `.claude/rules/workflow.md` examples.

- **Section 4: Before/After Example**
  Real case: 991 lines reduced to 110 lines + 4 modular rules. Saved ~1700 tokens per session.

- **Section 5: Checklist**
  - [ ] Tech stack documented
  - [ ] 3-5 common commands listed
  - [ ] One architectural pattern described
  - [ ] Under 150 lines
  - [ ] No secrets, no style guides

**Step 2: Verify line count**

```bash
wc -l /tmp/ClaudeSkillCollection.wiki/Start-Here:-CLAUDE.md-Templates.md
```

Expected: Under 100 lines.

**Step 3: Commit**

```bash
cd /tmp/ClaudeSkillCollection.wiki
git add "Start-Here:-CLAUDE.md-Templates.md"
git commit -m "docs: add CLAUDE.md Templates sub-page (#28)"
```

---

### Task 4: Create Your First Session sub-page (#29)

**Files:**
- Create: `/tmp/ClaudeSkillCollection.wiki/Start-Here:-Your-First-Session.md`

**Step 1: Write the first session page**

Create the file with (~80 lines):

- **Section 1: First Commands** — Run after installing Claude Code
  - `claude` — start a session
  - `/status` — check what's loaded
  - `/help` — see all commands
  - `/quit` — end session cleanly

- **Section 2: How CLAUDE.md Works** — Claude Code merges all CLAUDE.md files found. Priority table (simplified from CLAUDE-CODE-GUIDE.md):

  | Priority | Location | Scope |
  |---|---|---|
  | 1 (highest) | Enterprise policy | Org-wide |
  | 2 | `./CLAUDE.md` | Project (shared) |
  | 3 | `./.claude/rules/*.md` | Modular rules |
  | 4 | `./CLAUDE.local.md` | Personal |
  | 5 (lowest) | `~/.claude/CLAUDE.md` | Global |

- **Section 3: Session Management** — When to start new sessions
  - New task = new session
  - Context filling up = new session
  - Switch projects = new session

- **Section 4: Try This (3 minutes)** — Hands-on example
  1. Create a minimal CLAUDE.md (from templates page)
  2. Start Claude Code with `claude`
  3. Ask "What do you know about this project?"
  4. Verify Claude reads your CLAUDE.md

**Step 2: Verify and commit**

```bash
wc -l /tmp/ClaudeSkillCollection.wiki/"Start-Here:-Your-First-Session.md"
cd /tmp/ClaudeSkillCollection.wiki
git add "Start-Here:-Your-First-Session.md"
git commit -m "docs: add Your First Session sub-page (#29)"
```

---

### Task 5: Create Security & Compliance Path sub-page (#30)

**Files:**
- Create: `/tmp/ClaudeSkillCollection.wiki/Start-Here:-Security-&-Compliance-Path.md`

**Step 1: Write the security paths page**

Create the file with (~100 lines). 4 role-based paths, each with 3 steps:

**Path 1: DPO / Privacy Officer**
- Install: `gdpr-auditor`, `docx-smart-extractor`
- First run: "Audit my application for GDPR compliance"
- Key output: Compliance report with Article references

**Path 2: CISO / Security Manager**
- Install: `cybersecurity-policy-generator`, `security-report-builder`
- First run: "Generate an Information Security Policy for a 200-person healthcare company"
- Key output: Framework-compliant policy documents

**Path 3: Security Engineer**
- Install: `plugin-security-checker`, `incident-response-playbook-creator`
- First run: "Scan this plugin directory for vulnerabilities: ./my-plugin"
- Key output: Security scan with MITRE ATT&CK mapping

**Path 4: DevOps / Compliance Analyst**
- Install: `pdf-smart-extractor`, `xlsx-smart-extractor`
- First run: "Extract and analyze this compliance framework PDF: ./nist-csf.pdf"
- Key output: Extracted content with 12-103x token reduction

**Step 2: Verify and commit**

```bash
wc -l /tmp/ClaudeSkillCollection.wiki/"Start-Here:-Security-&-Compliance-Path.md"
cd /tmp/ClaudeSkillCollection.wiki
git add "Start-Here:-Security-&-Compliance-Path.md"
git commit -m "docs: add Security & Compliance Path sub-page (#30)"
```

---

### Task 6: Create Plugin Installation sub-page (#31)

**Files:**
- Create: `/tmp/ClaudeSkillCollection.wiki/Start-Here:-Plugin-Installation.md`

**Step 1: Write the installation page**

Create the file with (~60 lines). Consolidate from QUICKSTART.md:

- **Section 1: Claude Code Installation**
  ```bash
  /plugin marketplace add diegocconsolini/ClaudeSkillCollection
  /plugin install <plugin-name>@security-compliance-marketplace
  ```
  Important: Always use GitHub format, not local paths.

- **Section 2: Claude Desktop Installation**
  1. Download ZIP from `claude-desktop-skills/packages/`
  2. Open Claude Desktop > Skills > Import Skill
  3. Select ZIP file

- **Section 3: All Plugins** (table format)

  | Plugin | Version | Category | Description |
  |---|---|---|---|
  | plugin-security-checker | 3.2.0 | Security | Scan plugins for vulnerabilities (91 agents) |
  | gdpr-auditor | 1.2.0 | Security | GDPR compliance auditing |
  | cybersecurity-policy-generator | 1.2.0 | Security | Generate policies from 51 templates |
  | incident-response-playbook-creator | 2.2.0 | Security | IR playbooks (11 scenarios) |
  | security-report-builder | 1.2.0 | Security | Executive-ready security reports |
  | pdf-smart-extractor | 2.2.0 | Productivity | Extract large PDFs (12-103x reduction) |
  | xlsx-smart-extractor | 2.2.0 | Productivity | Extract Excel workbooks (20-100x reduction) |
  | docx-smart-extractor | 2.2.0 | Productivity | Extract Word documents (10-50x reduction) |
  | chrome-devtools-optimizer | 1.0.1 | Productivity | Reduce DevTools token usage 70-80% |
  | claude-guide | 1.0.0 | Productivity | Documentation navigator |

- **Section 4: Verification**
  ```bash
  /plugin  # Check installed plugins
  ```

**Step 2: Verify and commit**

```bash
wc -l /tmp/ClaudeSkillCollection.wiki/"Start-Here:-Plugin-Installation.md"
cd /tmp/ClaudeSkillCollection.wiki
git add "Start-Here:-Plugin-Installation.md"
git commit -m "docs: add Plugin Installation sub-page (#31)"
```

---

### Task 7: Push wiki changes

**Step 1: Push all wiki commits**

```bash
cd /tmp/ClaudeSkillCollection.wiki
git log --oneline
git push origin master
```

Expected: 5 commits pushed, 5 new wiki pages live.

**Step 2: Verify pages are accessible**

```bash
gh api repos/diegocconsolini/ClaudeSkillCollection/pages 2>/dev/null || echo "Check manually"
```

Verify at: https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here

---

### Task 8: Update README.md — add Start Here link (#32 part 1)

**Files:**
- Modify: `README.md` (lines 1-10)

**Step 1: Add Start Here badge after existing badges**

Find (line 8):
```markdown
[![Wiki](https://img.shields.io/badge/wiki-53_pages-purple.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki)
```

Add after it:
```markdown
[![Start Here](https://img.shields.io/badge/Start_Here-guide-brightgreen.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here)
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add Start Here badge to README.md (#32)"
```

---

### Task 9: Replace QUICKSTART.md with redirect (#32 part 2)

**Files:**
- Modify: `QUICKSTART.md` (full rewrite)

**Step 1: Replace QUICKSTART.md content**

Replace entire file with:

```markdown
# Quick Start Guide

This guide has moved to the wiki for easier maintenance and navigation.

**[Start Here — Quick Start Guide](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here)**

## Quick Links

- [CLAUDE.md Templates](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here:-CLAUDE.md-Templates)
- [Your First Session](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here:-Your-First-Session)
- [Security & Compliance Path](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here:-Security-&-Compliance-Path)
- [Plugin Installation](https://github.com/diegocconsolini/ClaudeSkillCollection/wiki/Start-Here:-Plugin-Installation)

## Emergency Quick Install

If you just need the install command:

```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install gdpr-auditor@security-compliance-marketplace
```

Then enable via `/plugin` and restart Claude Code.
```

**Step 2: Commit**

```bash
git add QUICKSTART.md
git commit -m "docs: replace QUICKSTART.md with redirect to wiki (#32)"
```

---

### Task 10: Update claude-guide skill — add "start" topic (#32 part 3)

**Files:**
- Modify: `claude-guide/agents/claude-guide.md` (line 56, topic mapping table)
- Modify: `claude-guide/SKILL.md` (topic list)

**Step 1: Add "start" to topic mapping table**

In `claude-guide/agents/claude-guide.md`, find the topic mapping table (line 47-59) and add a new row:

```markdown
| start, begin, new, onboard | Start Here Guide |
```

**Step 2: Add start topic response template**

After the "For /claude-guide examples" section (line 113), add:

```markdown
### For "/claude-guide start"

Respond with Start Here overview:
- Link to wiki Start Here page
- 5-Minute Setup Checklist (abbreviated)
- Decision tree: developer vs security/compliance
- Link to CLAUDE.md Templates
```

**Step 3: Update SKILL.md topic list**

In `claude-guide/SKILL.md`, add `start` to the available topics list.

**Step 4: Commit**

```bash
git add claude-guide/agents/claude-guide.md claude-guide/SKILL.md
git commit -m "docs: add 'start' topic to claude-guide skill (#32)"
```

---

### Task 11: Create PR and close sub-issues

**Step 1: Push branch**

```bash
git push -u origin feature/start-here-guide
```

**Step 2: Create PR**

```bash
gh pr create --title "feat: add Start Here quick-start guide (wiki + docs)" --body "$(cat <<'PREOF'
## Summary

- Created 5 wiki pages (hub + 4 sub-pages) for new user onboarding
- Added Start Here badge to README.md
- Replaced QUICKSTART.md with redirect to wiki
- Added "start" topic to claude-guide skill

## Wiki Pages Created
1. **Start-Here** — Hub page with decision tree and 5-min checklist
2. **Start-Here: CLAUDE.md Templates** — Copy-paste templates by project size
3. **Start-Here: Your First Session** — First commands and hands-on example
4. **Start-Here: Security & Compliance Path** — 4 role-based onboarding paths
5. **Start-Here: Plugin Installation** — Consolidated from QUICKSTART.md

## Test plan
- [ ] Verify all 5 wiki pages render at wiki/Start-Here
- [ ] Verify all inter-page links work
- [ ] Verify README.md Start Here badge links correctly
- [ ] Verify QUICKSTART.md redirect links work
- [ ] Verify `/claude-guide start` returns Start Here info
- [ ] Verify each wiki page is under 100 lines

Closes #22, closes #27, closes #28, closes #29, closes #30, closes #31, closes #32

Generated with [Claude Code](https://claude.com/claude-code)
PREOF
)"
```

---

## Batch Execution Strategy

| Batch | Tasks | Dependencies |
|---|---|---|
| 1 | T1 (branch + clone wiki) | None |
| 2 | T2, T3, T4, T5, T6 (all wiki pages — parallel) | T1 |
| 3 | T7 (push wiki) | T2-T6 |
| 4 | T8, T9, T10 (repo file updates — parallel) | T7 |
| 5 | T11 (PR) | T8-T10 |
