#!/usr/bin/env bash
# audit_config_change.sh — append a ConfigChange event to a local audit log (JSONL).
# Wired to the ConfigChange hook; receives the hook JSON on stdin. Appends only; never
# executes any received content. Exit 0 = allow the change (non-blocking audit trail).

set -euo pipefail

LOG="${SECURITY_AUDIT_LOG:-$HOME/.claude/security-audit.log}"
mkdir -p "$(dirname "$LOG")"

# Read the hook payload from stdin (may be empty if invoked manually).
payload="$(cat 2>/dev/null || true)"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Pull a few common fields if jq is available; otherwise store the raw payload.
if command -v jq >/dev/null 2>&1 && [ -n "$payload" ]; then
  printf '%s\n' "$payload" | jq -c \
    --arg ts "$ts" \
    '{audited_at:$ts, event:(.hook_event_name // "ConfigChange"), matcher:(.matcher // null), cwd:(.cwd // null), session_id:(.session_id // null), permission_mode:(.permission_mode // null)}' \
    >> "$LOG"
else
  printf '{"audited_at":"%s","event":"ConfigChange","raw":%s}\n' \
    "$ts" "$(printf '%s' "${payload:-null}" | sed 's/"/\\"/g; s/^/"/; s/$/"/')" >> "$LOG"
fi

exit 0
