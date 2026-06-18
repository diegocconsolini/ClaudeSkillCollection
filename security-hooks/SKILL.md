---
name: security-hooks
description: Use this skill to install ready-made Claude Code hooks for security — a ConfigChange compliance audit trail (logs every settings/skill change), plus PreToolUse guards and optional HTTP notifications for security-relevant events. Covers command, http, and prompt hook types.
license: MIT
---

# Security Hooks Collection

Ready-made [hooks](https://code.claude.com/docs/en/hooks) for security and compliance.
Copy the entries you want from [`hooks/hooks.json`](hooks/hooks.json) into your
`.claude/settings.json` (or a plugin's `hooks/hooks.json`), then review them in `/hooks`.

## What's included

| Hook | Event | Purpose |
|---|---|---|
| **Config audit trail** | `ConfigChange` | Appends every settings/skills change to `~/.claude/security-audit.log` (JSONL) — compliance evidence. (#41) |
| **Dangerous-bash guard** | `PreToolUse` (Bash) | Prompt-hook that flags destructive shell commands before they run. |
| **Sensitive-file write guard** | `PreToolUse` (Write/Edit) | Warns on writes to credential/financial file patterns. |
| **HTTP notify (optional)** | `ConfigChange` / `SessionEnd` | POSTs a security event to a webhook (Slack/SIEM). Off until you set the URL. (#35) |

## Install

```bash
# inspect the ready-made config
cat hooks/hooks.json

# merge the entries you want into your settings (review in /hooks afterwards)
# (the audit-trail command writes to ~/.claude/security-audit.log)
```

The `ConfigChange` event (v2.1.49) matches `user_settings`, `project_settings`,
`local_settings`, `policy_settings`, `skills`. HTTP hooks (v2.1.63) POST JSON and read a
JSON response. All hooks receive `session_id`, `cwd`, `permission_mode`, `hook_event_name`.

> Security note: hooks run with your privileges. Review every entry before enabling; the
> command hook here only **appends to a local log** and never executes scanned content.
