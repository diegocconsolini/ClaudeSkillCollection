---
name: batch-security-migration
description: Use when applying the same security fix across many files or repos at once — large-scale vulnerability remediation. Provides 7 copy-paste /batch recipes (XSS, HTTPS, SQLi, input validation, log PII, secret rotation, CVE patches) each with a safety tier and false-positive trap, plus scan_diff.py to prove the migration introduced no new HIGH/CRITICAL findings.
license: MIT
metadata:
  version: 1.0.0
  author: Diego Consolini
---

# Batch Security Migration

Turn Claude Code's **built-in `/batch`** into a security-migration tool. This skill
does **not** reinvent `/batch` — `/batch` already fans work out into worktree-isolated
per-unit PRs. This skill supplies the *recipes*, the *safety tiers*, and an objective
*before/after gate* (`scripts/scan_diff.py`).

## When to use

You have the same vulnerability class in many places (dozens of files, or many repos)
and want to fix them in one coordinated pass with per-unit review and a regression gate.

## Safety tiers

| Tier | Meaning |
|---|---|
| 🟢 safe | Mechanical text substitution; review only the flagged dynamic cases. |
| 🟡 review | Semantic change; the per-unit PR review **is** the gate. |
| 🔴 manual | Never full-auto — high blast radius. Drive `/batch` one unit at a time with a human + test run per unit. |

## Pre-scan checklist

1. Clean git tree (`git status` empty) — `/batch` needs a clean base.
2. Run a **baseline scan**: `scan_plugin.py <target> --output before.json --format json`.
3. Confirm `/batch` is available (Claude Code ≥ 2.1.63).
4. Scope to a subdirectory first; don't run repo-wide on the first pass.
5. Ensure the existing test suite passes **before** you start.

## Recipes

| # | Recipe | Tier | False-positive trap | Verify |
|---|---|---|---|---|
| 1 | XSS: `innerHTML` → `textContent` | 🟢 safe | dynamic-HTML assignment is intentional in a few spots | grep should drop for static cases |
| 2 | HTTPS: `http://` → `https://` | 🟢 safe | `localhost` / `127.0.0.1` / example URLs must be excluded | no `http://` outside the allowlist |
| 3 | SQLi: string-concat → parameterized | 🟡 review | not every concatenated string is a query | per-unit PR review |
| 4 | Input validation on route handlers | 🟡 review | may add a dependency; verify handler coverage | tests + handler list |
| 5 | Log sanitization: strip PII from logs | 🟡 review | regex over-match can corrupt non-PII logs | check redaction correctness |
| 6 | Secret rotation: hardcoded key → env var | 🔴 manual | **test fixtures look like real secrets** | manual per unit + secret scan |
| 7 | Dependency CVE patch updates | 🔴 manual | **a patch can break an API** | test run per bump |

### 1. XSS: `innerHTML` → `textContent` (🟢)
`/batch` over files matching `grep -rl 'innerHTML' src/`: "Replace `element.innerHTML = x`
with `element.textContent = x` where `x` is plain text. Leave intentional HTML injection
(templating, sanitized fragments) and add a `// reviewed: dynamic HTML` comment instead."
Verify: `grep -rn 'innerHTML' src/` returns only reviewed cases.

### 2. HTTPS: `http://` → `https://` (🟢)
`/batch`: "Replace `http://` with `https://` in source and config. Do NOT touch
`localhost`, `127.0.0.1`, `0.0.0.0`, `example.com`, or XML namespace URIs."
Verify: `grep -rn 'http://' . | grep -v -E 'localhost|127\.0\.0\.1|example\.'` is empty.

### 3. SQLi: parameterized queries (🟡)
`/batch`: "Convert string-concatenated SQL into parameterized queries for the driver in
use. Each file is its own PR — flag any query you can't safely parameterize." Review every
per-unit PR; this is semantic.

### 4. Input validation on route handlers (🟡)
`/batch`: "Add input validation to each Express/route handler using the project's existing
validation library. If none exists, flag the unit instead of adding a new dependency."
Verify handler coverage and that no unintended dependency was added.

### 5. Log sanitization: strip PII (🟡)
`/batch`: "Wrap log statements that emit email/SSN/credit-card values in the project's
redaction helper. Don't redact non-PII." Check redaction correctness — regexes over-match.

### 6. Secret rotation: hardcoded key → env var (🔴 manual)
Drive `/batch` **one unit at a time**. "Replace a hardcoded secret with `os.environ[...]`
/ `process.env...` and add it to `.env.example`." **Trap:** test fixtures and example keys
look like real secrets — never full-auto. After: rotate every real key that was exposed.

### 7. Dependency CVE patch updates (🔴 manual)
Drive `/batch` **one bump at a time**. "Update <pkg> to the patched version for <CVE>."
**Trap:** patches can break APIs — run the full test suite per bump before merging.

## Post-migration workflow

1. Merge the per-unit PRs `/batch` produced.
2. Re-scan: `scan_plugin.py <target> --output after.json --format json`.
3. Gate: `python3 scripts/scan_diff.py before.json after.json`
   - exit 0 + "GATE: PASS" → no new HIGH/CRITICAL; ship.
   - exit 1 + "GATE: FAIL" → triage the listed NEW findings, or re-run with `--report-only`
     once you've justified them.

Or let scan_diff run both scans for you:
`python3 scripts/scan_diff.py --scan <target_before> <target_after>`
