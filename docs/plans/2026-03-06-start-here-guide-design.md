# Design: "Claude Code Start Here" Quick-Start Guide

**Issue:** #22
**Date:** 2026-03-06
**Status:** Approved

## Scope

- **Content:** Both Claude Code basics AND marketplace plugin onboarding
- **Location:** GitHub Wiki (hub-and-spoke structure)
- **Audience:** Both general developers and security/compliance professionals
- **Consolidation:** QUICKSTART.md content moves into wiki; file becomes redirect

## Architecture: Hub-and-Spoke Wiki Pages

```
Start-Here.md (Hub - ~80 lines)
|-- Start-Here:-CLAUDE.md-Templates.md (~100 lines)
|   Decision tree, copy-paste templates by project size
|-- Start-Here:-Your-First-Session.md (~80 lines)
|   What to do after installing Claude Code
|-- Start-Here:-Security-&-Compliance-Path.md (~100 lines)
|   Role-based guide: DPO, CISO, security engineer
|-- Start-Here:-Plugin-Installation.md (~60 lines)
|   Consolidated from QUICKSTART.md
```

Total: ~420 lines across 5 pages (avg 84 lines each).

## Page Designs

### 1. Hub Page: Start-Here.md (~80 lines)

**Purpose:** Single entry point for all new users.

**Sections:**
1. Welcome banner - "New to Claude Code or this marketplace?"
2. "What's your goal?" decision tree:
   - "Set up Claude Code for my project" -> CLAUDE.md Templates
   - "Security/compliance tools" -> Security & Compliance Path
   - "Extract documents (PDF/Excel/Word)" -> Plugin Installation
   - "Already use Claude Code, show me plugins" -> Plugin Installation
3. 5-Minute Setup Checklist (numbered steps, zero to first plugin)
4. Top 5 Common Mistakes (inline, keeps hub standalone-useful)
5. Deep Dive Links (CLAUDE-CODE-GUIDE.md, wiki index, plugin READMEs)

### 2. CLAUDE.md Templates (~100 lines)

**Purpose:** Core of issue #22. Decision tree + copy-paste templates.

**Sections:**
1. Project complexity decision tree (simple <5 files / medium / complex)
2. Minimal CLAUDE.md template (~50 lines)
3. Standard template (~100-150 lines) with .claude/rules/ structure
4. Real before/after example (991 -> 110 lines TPRM case)
5. New CLAUDE.md checklist

### 3. Your First Session (~80 lines)

**Purpose:** Bridge "I installed Claude Code" to "I'm productive."

**Sections:**
1. First commands to run after installation
2. How Claude Code reads CLAUDE.md (merge behavior)
3. Memory architecture overview (simplified 5-level table)
4. Session management basics (when to start new sessions)
5. "Try this" - 3-minute hands-on example

### 4. Security & Compliance Path (~100 lines)

**Purpose:** Role-based onboarding for security/compliance professionals.

**Paths:**
1. DPO/Privacy Officer -> gdpr-auditor, docx-smart-extractor
2. CISO/Security Manager -> cybersecurity-policy-generator, security-report-builder
3. Security Engineer -> plugin-security-checker, incident-response-playbook-creator
4. DevOps/Compliance -> pdf-smart-extractor, xlsx-smart-extractor

Each path: 3 steps (install -> configure -> first run example)

### 5. Plugin Installation (~60 lines)

**Purpose:** Consolidated from QUICKSTART.md. Both Claude Code and Desktop.

**Sections:**
1. Claude Code plugin installation (marketplace add -> plugin install)
2. Claude Desktop skill import (ZIP files from packages/)
3. Plugin-by-plugin quick descriptions (table)
4. Verification steps

## Changes to Existing Files

| File | Change |
|------|--------|
| README.md | Add "Start Here" badge/link at top of file |
| QUICKSTART.md | Replace with redirect to wiki Start-Here page |
| CLAUDE-CODE-GUIDE.md | No changes (stays as deep reference) |
| claude-guide/ skill | Add "start" topic pointing to wiki Start-Here |

## Investigation Findings

### Existing Documentation Inventory
- README.md (1,308 lines) - Marketplace overview
- QUICKSTART.md (302 lines) - Installation-focused, to be consolidated
- CLAUDE-CODE-GUIDE.md (918 lines) - Comprehensive reference, keep as-is
- PLUGIN_STRUCTURE_GUIDE.md (758 lines) - Plugin development reference
- CONTRIBUTING.md (548 lines) - Contribution guidelines
- claude-guide/ skill (179 lines) - CLI reference navigator
- GitHub Wiki (60+ pages) - Deep-dive reference docs

### Gaps Identified
1. No single "Start Here" entry point
2. No role-based onboarding paths
3. No CLAUDE.md templates or decision trees
4. No "first session" guidance
5. QUICKSTART.md is installation-only, not onboarding
6. Three competing entry points (README vs QUICKSTART vs CLAUDE-CODE-GUIDE)
7. No beginner-friendly workflow guidance

## Success Criteria

- Each wiki page under 100 lines
- New user productive in 5 minutes (from zero to first plugin running)
- Clear role-based paths for security/compliance personas
- Copy-paste CLAUDE.md templates that work immediately
- No duplication with existing CLAUDE-CODE-GUIDE.md (link, don't repeat)
