# Claude Code Issue Template

Use this template to report the marketplace plugin loading issue to the Claude Code team.

---

**Title:** Marketplace-installed plugins don't auto-register as available skills

**Issue Type:** Bug / Feature Request

**Priority:** Medium

**Component:** Plugin System / Skill Loader

---

## Description

When plugins are installed from a marketplace using `/plugin install <plugin>@<marketplace>`, they download successfully but don't automatically become available as skills. This requires users to manually create symlinks to make marketplace plugins usable.

## Current Behavior

1. User runs: `/plugin marketplace add diegocconsolini/ClaudeSkillCollection`
2. User runs: `/plugin install gdpr-auditor@security-compliance-marketplace`
3. Plugin downloads to: `~/.claude/plugins/marketplaces/security-compliance-marketplace/gdpr-auditor/`
4. Status shows: "✓ Installed"
5. User tries to use the skill: `/skill gdpr-auditor` or invokes via natural language
6. Result: `Error: Unknown skill: gdpr-auditor`

## Root Cause

**Architectural disconnect between plugin installation and skill discovery:**

- **Plugin installation location:** `~/.claude/plugins/marketplaces/<marketplace>/<plugin>/`
- **Skill loader scan location:** `~/.claude/skills/` only
- **No automatic bridge:** Installation doesn't register plugins with the skill loader

## Expected Behavior

When a user installs a plugin via `/plugin install`, it should be immediately available as a skill without any additional manual steps:

1. User runs: `/plugin install gdpr-auditor@security-compliance-marketplace`
2. Plugin downloads and is automatically registered
3. User can immediately use the skill
4. No manual symlink creation required

## Workaround

Users must manually create symlinks after marketplace installation:

```bash
ln -s ~/.claude/plugins/marketplaces/security-compliance-marketplace/gdpr-auditor ~/.claude/skills/gdpr-auditor
```

Then restart Claude Code.

## Impact

**Severity:** Medium-High
- Affects all marketplace plugins
- Creates confusing user experience
- Undermines the purpose of the marketplace system
- Requires users to understand filesystem symlinks
- Not documented in the UI

**User Impact:**
- Users think installation failed when it actually succeeded
- Requires technical knowledge of symlinks and shell commands
- Breaks the "install and use" expectation
- Reduces marketplace adoption

## Proposed Solutions

### Solution 1: Auto-Registration During Installation (Recommended)

Modify `/plugin install` to automatically create symlinks in `~/.claude/skills/` when installing marketplace plugins.

**Implementation:**
```
When: /plugin install <plugin>@<marketplace>
Then:
  1. Download to: ~/.claude/plugins/marketplaces/<marketplace>/<plugin>/
  2. Auto-create symlink: ~/.claude/skills/<plugin> -> marketplace location
  3. Register in manifest: ~/.claude/plugins/installed.json
  4. Notify user: "✓ Installed and registered"
```

**Benefits:**
- Zero user intervention
- Works with existing skill loader
- Backward compatible
- Easy rollback

### Solution 2: Unified Skill Discovery

Modify the skill loader to scan multiple directories including marketplace locations.

**Implementation:**
```python
def load_skills():
    scan_directory("~/.claude/skills/")  # Current behavior
    scan_directory("~/.claude/plugins/marketplaces/*/")  # Add this
```

**Benefits:**
- No symlinks needed
- More elegant solution
- Supports future plugin sources easily

### Solution 3: Central Skill Registry

Create a manifest file mapping skills to their locations.

**Implementation:**
```json
// ~/.claude/skills/registry.json
{
  "skills": [
    {
      "name": "gdpr-auditor",
      "source": "marketplace",
      "path": "~/.claude/plugins/marketplaces/security-compliance-marketplace/gdpr-auditor"
    }
  ]
}
```

## Steps to Reproduce

1. Install Claude Code (any version with marketplace support)
2. Add a marketplace: `/plugin marketplace add diegocconsolini/ClaudeSkillCollection`
3. Install a plugin: `/plugin install gdpr-auditor@security-compliance-marketplace`
4. Verify installation: `/plugin` → Shows as installed
5. Try to use the skill: Ask Claude "Audit my code for GDPR compliance"
6. Observe: Skill is not recognized

## Environment

- **OS:** Linux / macOS / Windows
- **Claude Code Version:** [Version]
- **Marketplace:** security-compliance-marketplace
- **Plugin:** gdpr-auditor (but affects all marketplace plugins)

## Additional Context

This issue affects all community marketplaces that use the `/plugin marketplace add` and `/plugin install` workflow. It's a fundamental design limitation that reduces the utility of the marketplace system.

**Workaround documentation:** https://github.com/diegocconsolini/ClaudeSkillCollection/blob/main/docs/marketplace-installation-workaround.md

## Related Issues

- [Link to any related GitHub issues if they exist]

## Community Impact

This issue is blocking adoption of community marketplaces. Several users have reported confusion when plugins don't work after "successful" installation.

---

**Suggested Labels:** bug, plugins, marketplace, skill-loader, enhancement
**Suggested Milestone:** Next release
**Suggested Assignee:** Claude Code plugin system maintainer
