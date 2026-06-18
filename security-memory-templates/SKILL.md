---
name: security-memory-templates
description: Use this skill to seed Claude Code's auto-memory with pre-built security/compliance patterns — known-safe code patterns, false-positive suppressions for the plugin-security-checker, org compliance rules, and supply-chain best practices. Helps Claude apply consistent security judgment across sessions.
license: MIT
---

# Security Memory Templates

Pre-built [auto-memory](https://code.claude.com/docs/en/memory#auto-memory) entries for
security work. Auto-memory lives at `~/.claude/projects/<project>/memory/` — `MEMORY.md`
is the index loaded each session; topic files are loaded on demand.

## Usage

```
/security-memory-templates           # show available templates
/security-memory-templates install   # copy selected templates into this project's memory
```

To apply a template, copy it into your project's memory dir and add a one-line pointer to
`MEMORY.md`:

```bash
PROJ_MEM=~/.claude/projects/$(echo "$PWD" | sed 's#/#-#g')/memory
cp templates/false-positive-suppressions.md "$PROJ_MEM/"
echo '- [FP suppressions](false-positive-suppressions.md) — known-safe patterns to not re-flag' >> "$PROJ_MEM/MEMORY.md"
```

## Templates

| File | What it seeds |
|---|---|
| `templates/false-positive-suppressions.md` | Patterns the plugin-security-checker can safely treat as non-issues |
| `templates/supply-chain-rules.md` | npm/PyPI install-time hardening rules (ignore-scripts, cooldown, provenance) |
| `templates/compliance-context.md` | Skeleton for org-specific GDPR/SOC2/ISO rules |

Each template follows the auto-memory frontmatter format (`name`, `description`,
`metadata.type`). Edit freely — they're plain markdown.

> Note: these are *seeds*, not live behavior. Claude reads them like any memory; keep them
> truthful (a stale suppression that names a removed pattern is worse than none).
