# Design — `batch-security-migration` plugin (issue #40)

**Date:** 2026-06-22
**Issue:** #40 — Batch Security Migration Skill (Large-Scale Vulnerability Fixes)
**Status:** approved design → implementation

## Goal

A **recipe skill** that turns Claude Code's built-in `/batch` command into a security-
migration tool. It does **not** reinvent `/batch` (the built-in already fans out into
worktree-isolated per-unit PRs). It provides:

1. Seven copy-paste `/batch` security recipes, each with an **automation-safety tier** and
   its specific false-positive trap.
2. A pre-scan checklist (what to verify before running a batch migration).
3. An objective **post-migration validation gate** (`scan_diff.py`) that runs
   `plugin-security-checker` before and after and fails on any *new* HIGH/CRITICAL finding.

This is the 13th marketplace plugin. It dogfoods the marketplace's own scanner and follows
the repo's "wrap, don't reinvent" convention (same principle as the SBOM toolkit).

## Why a recipe skill, not an orchestrator

Issue #40's explicit deliverable list is recipes + validation, and Claude Code ships a
built-in `/batch` (v2.1.63) that already does worktree fan-out + per-unit PRs. Building a
parallel orchestrator would duplicate a platform feature. The design-doc one-liner
("`/batch-fix` that takes a transform + file-list") is superseded by the issue body, which is
the authoritative spec.

## Components

### 1. `SKILL.md` (the knowledge surface)

Frontmatter: `name: batch-security-migration`, a `description` that triggers on
"batch security fix / large-scale vulnerability migration", `license: MIT`. (Only `name` +
`description` are required; `license` is repo convention.)

Body: a **recipe table** — one row per recipe — with columns:

| Recipe | `/batch` command | Tier | False-positive trap | Verify |
|---|---|---|---|---|

The 7 recipes and their tiers:

| # | Recipe | Tier | Note |
|---|---|---|---|
| 1 | XSS: `innerHTML` → `textContent` | 🟢 safe | mechanical; review only dynamic-HTML cases |
| 2 | HTTPS: `http://` → `https://` (skip localhost) | 🟢 safe | exclude `localhost`/`127.0.0.1`/example URLs |
| 3 | SQLi: string-concat → parameterized queries | 🟡 review | semantic; per-unit PR review is the gate |
| 4 | Input validation on Express route handlers | 🟡 review | may add deps; verify handler coverage |
| 5 | Log sanitization: strip PII (email/SSN/CC) from logs | 🟡 review | regex over-match risk; check redaction correctness |
| 6 | Secret rotation: hardcoded keys → env-var refs | 🔴 manual | **test fixtures look like secrets** — never full-auto |
| 7 | Dependency CVE patch updates | 🔴 manual | **patches can break APIs** — needs test run per bump |

Each row links to a short "details" subsection with the exact command, the trap spelled out,
and a one-line verification grep (e.g. recipe 1 → `grep -rn 'innerHTML' src/` should drop to
zero for static cases).

Plus two short sections:
- **Pre-scan checklist** — clean git tree, run baseline scan, confirm `/batch` available, scope
  to a subdir, ensure tests pass first.
- **Post-migration workflow** — merge per-unit PRs → run `scan_diff.py baseline.json after.json`
  → green gate or triage new findings.

### 2. `scripts/scan_diff.py` (the validation gate)

**Contract** (verified against scanner v3.2.0):
- Scanner is invoked as `scan_plugin.py <path> --format json --output <file>` (stdout carries
  a human banner; only `--output` yields clean JSON).
- JSON shape: `summary.severity_counts.{CRITICAL,HIGH,MEDIUM,LOW,INFO}` and `findings[]` where
  each finding has `severity, category, subcategory, file, line, description` (the sequential
  `id` is NOT stable across scans → excluded from identity).

**Behavior:**
- Two modes of input: either two pre-made scan JSONs (`scan_diff.py before.json after.json`),
  or two target dirs with `--scan` (it runs the scanner itself for each).
- Finding identity key = `(severity, category, subcategory, file, line, description)`.
- Computes: `new` (in after, not before), `fixed` (in before, not after), `unchanged`.
- Prints a compact table: per-severity before→after counts + the list of NEW findings.
- **Exit code:** `1` if any finding in `new` is `HIGH` or `CRITICAL`; `0` otherwise.
- `--report-only` forces exit `0` (still prints the table) — the escape hatch.
- Locates `scan_plugin.py` via a script-relative path (`../../plugin-security-checker/
  scripts/scan_plugin.py`), with a `--scanner PATH` override, matching the repo's
  script-relative convention. Fails with a clear message if not found.
- Zero third-party deps (stdlib `json`, `argparse`, `subprocess`, `pathlib`).

### 3. Plugin packaging

- `.claude-plugin/plugin.json`: `name`, `version: 1.0.0`, `description`, `author`
  (Diego Consolini / diego@diegocon.nl), `keywords`. No `agents` array (this plugin ships a
  skill + script, not an agent) — note plugin.json does not *require* agents.
- `marketplace.json`: 13th entry mirroring `security-hooks` (category `security`, license MIT,
  `source: ./batch-security-migration`, homepage/repository URLs).

## Data flow

```
user picks recipe ──> runs /batch "<recipe command>"  (built-in: worktree fan-out + PRs)
                                   │
        baseline scan ◄───────────┤ (before)
                                   ▼
                       merge per-unit PRs
                                   │
                                   ▼
            scan_diff.py before.json after.json
                                   │
                 ┌─────────────────┴─────────────────┐
            no new HIGH+                         new HIGH+ found
            exit 0 (green)                       exit 1 (triage) / --report-only
```

## Error handling

- Scanner not found → clear error naming the path tried + the `--scanner` override.
- Malformed/missing scan JSON → explicit "could not parse <file>" with the exception.
- Scanner non-zero exit during `--scan` → surface its stderr, abort the diff.
- Empty findings on both sides → "no findings; nothing to compare", exit 0.

## Testing

`scan_diff.py` is the only executable, so it gets the tests:
1. **new HIGH finding → exit 1**: craft before.json (0 findings) + after.json (1 HIGH) → assert exit 1 + finding listed under NEW.
2. **fixed finding → exit 0**: before has 1 CRITICAL, after has 0 → exit 0, listed under FIXED.
3. **`--report-only` suppresses exit 1**: same as test 1 but with the flag → exit 0.
4. **identity keying**: same finding with a *different* `id` but same (severity,category,file,line,desc) → counted as unchanged, not new.
5. **`--scan` mode end-to-end**: two tiny temp dirs → runs the real scanner, produces a diff (smoke test; tolerant of scanner version).

Tests use Python stdlib `unittest` + temp files; no network, no third-party deps.

## Out of scope (YAGNI)

- No custom fan-out / worktree mechanism (built-in `/batch` owns that).
- No new scanner patterns (scan_diff consumes existing scanner output).
- No HTML/markdown report rendering (the compact table is enough; the scanner already has
  `--format html` if a user wants a full report).

## Doc-drift impact

Marketplace goes 12 → 13 plugins. `scripts/check_doc_drift.py` derives counts, so no
hardcoded numbers to update — but I will run it to confirm it still passes at 13.
