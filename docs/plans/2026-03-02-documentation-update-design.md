# Documentation Update Design - Fact-Based Investigation

**Date:** 2026-03-02
**Status:** Approved
**Scope:** All 12 actionable documentation issues across CLAUDE.md, README.md, plugin manifests, and desktop skill metadata

## Investigation Summary

A comprehensive fact-based audit was performed across:
- CLAUDE.md (project instructions)
- README.md (public-facing documentation)
- .claude-plugin/marketplace.json (plugin registry)
- All 9 plugin.json manifests
- All claude-desktop-skills packages
- GitHub Wiki (60+ pages)
- Official Claude Code documentation (March 2026)

## Issues Found

### Critical (Breaking/Accuracy)

#### Issue 1: Hardcoded machine paths in CLAUDE.md
- **Location:** CLAUDE.md lines 25, 26, 152
- **Current:** `/home/diegocc/ClaudeSkillCollection/claude-desktop-skills/`
- **Problem:** Machine-specific path; actual current path is `/Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection/`
- **Fix:** Replace with relative paths (`./claude-desktop-skills/` and `./claude-desktop-skills/packages/`)

#### Issue 2: Inconsistent Skill.md naming documentation
- **Location:** CLAUDE.md line 54
- **Current:** Claims `Skill.md (capital S, lowercase kill - REQUIRED)`
- **Reality:** Root plugins use `SKILL.md` (all caps); desktop skills use `Skill.md` (mixed case)
- **Fix:** Document both formats clearly, distinguishing Claude Code plugins from Desktop skills

#### Issue 3: security-report-builder version mismatch
- **Location:** `security-report-builder/.claude-plugin/plugin.json` vs `.claude-plugin/marketplace.json`
- **Current:** plugin.json = 1.0.1, marketplace.json = 1.2.0, version.json = 1.2.0
- **Root cause:** Commit 4624072 accidentally reverted plugin.json from 1.2.0 to 1.0.1 while fixing agent path syntax
- **Fix:** Update plugin.json to 1.2.0; update claude-desktop-skills Skill.md frontmatter to 1.2.0

#### Issue 4: Incorrect required frontmatter fields
- **Location:** CLAUDE.md line 63
- **Current:** Claims `name`, `description`, `license` are required
- **Reality:** `license` is not an official SKILL.md frontmatter field per Claude docs; only desktop skills include it
- **Fix:** Clarify that `name` and `description` are required; `license` is project-specific metadata for desktop skills only

### High Priority (Documentation Gaps)

#### Issue 5: README.md missing Claude Desktop Skills section
- **Location:** README.md
- **Current:** Only documents Claude Code plugin installation
- **Fix:** Add "Claude Desktop Skills" section with installation instructions and skills catalog

#### Issue 6: Wiki page count incorrect
- **Location:** CLAUDE.md line 9, README.md
- **Current:** Claims "53 comprehensive pages"
- **Actual:** 60+ pages
- **Fix:** Update count to "60+"

#### Issue 7: Example count incorrect
- **Location:** CLAUDE.md line 17
- **Current:** Claims "14 copy-paste examples"
- **Actual:** 13 example pages
- **Fix:** Update to "13"

#### Issue 8: No version numbers in CLAUDE.md plugin listings
- **Location:** CLAUDE.md plugin list section
- **Current:** Only lists file sizes
- **Fix:** Add version numbers alongside file sizes

#### Issue 9: No differentiation between plugin formats
- **Location:** CLAUDE.md
- **Current:** Describes one package format for all
- **Reality:** Root plugins have SKILL.md + agents/ + version.json; Desktop skills have Skill.md, no agents/
- **Fix:** Add separate format documentation for each type

### Medium Priority (Consistency)

#### Issue 10: plugin-security-checker ZIP size
- **Location:** CLAUDE.md line 39
- **Current:** "9.2 MB"
- **Actual:** 9.1 MB
- **Fix:** Update to "9.1 MB"

#### Issue 11: Desktop security-report-builder Skill.md version
- **Location:** claude-desktop-skills/security-report-builder/Skill.md
- **Current:** Version 1.0.1 in frontmatter
- **Fix:** Update to 1.2.0

#### Issue 12: Empty wiki/ directory
- **Location:** wiki/ at repo root
- **Current:** Empty directory
- **Fix:** Either remove or add a README explaining wiki is on GitHub

## Positive Findings (No Action Needed)

- GitHub Wiki uses correct `~/.claude/` notation (no hardcoded paths)
- marketplace.json is valid JSON with correct structure
- 8 of 9 plugin versions match across manifests (except issue 3)
- claude-desktop-skills/README.md, CHANGELOG.md, MIGRATION_GUIDE.md are accurate
- GitHub issue templates exist at .github/ISSUE_TEMPLATE/
- All 9 plugins have valid .claude-plugin/plugin.json manifests

## Files to Modify

1. `CLAUDE.md` - Issues 1, 2, 4, 6, 7, 8, 9, 10
2. `README.md` - Issues 5, 6
3. `security-report-builder/.claude-plugin/plugin.json` - Issue 3
4. `claude-desktop-skills/security-report-builder/Skill.md` - Issue 11
5. `wiki/README.md` (new) - Issue 12

## Execution Strategy

1. Create GitHub issue with full investigation findings
2. Create branch `docs/fact-based-documentation-update`
3. Fix all files in order (CLAUDE.md first, then README.md, then manifests)
4. Create PR referencing the issue

## References

- Official Claude Code docs: https://code.claude.com/docs/en/skills
- Official plugins reference: https://code.claude.com/docs/en/plugins-reference
- Official subagents reference: https://code.claude.com/docs/en/sub-agents
- Anthropic skills repo: https://github.com/anthropics/skills
