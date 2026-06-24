# batch-security-migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the 13th marketplace plugin `batch-security-migration` — a recipe skill that turns Claude Code's built-in `/batch` into a security-migration tool, plus an objective `scan_diff.py` validation gate that fails on any new HIGH/CRITICAL finding.

**Architecture:** A knowledge-surface `SKILL.md` (7 `/batch` security recipes, each with a safety tier and false-positive trap) + one executable `scripts/scan_diff.py` that runs `plugin-security-checker` before/after a migration and diffs findings. No agent, no custom orchestrator (built-in `/batch` owns fan-out; "wrap, don't reinvent").

**Tech Stack:** Python 3 stdlib only (`json`, `argparse`, `subprocess`, `pathlib`, `unittest`). Markdown SKILL.md. JSON manifests.

## Global Constraints

- **Plugin name:** `batch-security-migration` (dir, `name` field, marketplace `name`, SKILL.md `name` all identical).
- **Required frontmatter:** only `name` + `description`. `license: MIT` is repo convention. Non-standard keys go under `metadata:`.
- **Author (verbatim, matches every other plugin):** `{ "name": "Diego Consolini", "email": "diego@diegocon.nl" }`.
- **Scanner invocation (verified v3.2.0):** `scan_plugin.py <path> --output <file> --format json`. stdout carries a human banner — only `--output` yields clean JSON. JSON top-level keys: `metadata, summary, findings, disclaimer`. `summary.severity_counts` has exactly `CRITICAL, HIGH, MEDIUM, LOW, INFO`. Each finding has keys `id, severity, category, subcategory, file, line, column, code_snippet, description, explanation, impact, recommendation, cvss_score, cve_reference, owasp_reference, remediation_effort, false_positive_likelihood`.
- **Finding identity key (excludes unstable `id`):** `(severity, category, subcategory, file, line, description)`. Verified: a real finding's `id` is `FINDING-013` (sequential, not stable across scans).
- **Scanner location, script-relative:** from `batch-security-migration/scripts/scan_diff.py`, the scanner is at `../../plugin-security-checker/scripts/scan_plugin.py`. `--scanner PATH` overrides.
- **Zero third-party deps.** stdlib only.
- **Doc-drift:** `scripts/check_doc_drift.py` derives the plugin count from `marketplace.json` (currently 12 → must read 13 after this plan, exit 0). No hardcoded counts to edit.
- **Safety tiers (approved):** secret-rotation (recipe 6) and dependency-CVE-updates (recipe 7) stay 🔴 manual (never full-auto). Recipes 1–2 🟢 safe, 3–5 🟡 review.

---

### Task 1: Plugin scaffold + manifest

**Files:**
- Create: `batch-security-migration/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: the plugin directory and a valid `plugin.json` that `node -e "JSON.parse(...)"` accepts. Later tasks add `SKILL.md` and `scripts/` under this dir.

- [ ] **Step 1: Write the manifest**

Create `batch-security-migration/.claude-plugin/plugin.json`:

```json
{
  "name": "batch-security-migration",
  "version": "1.0.0",
  "description": "Recipe skill that turns Claude Code's built-in /batch into a security-migration tool: 7 copy-paste batch recipes (XSS, HTTPS, SQLi, input validation, log PII, secret rotation, CVE patches) with per-recipe safety tiers and false-positive traps, plus scan_diff.py — a before/after plugin-security-checker gate that fails on any new HIGH/CRITICAL finding.",
  "author": { "name": "Diego Consolini", "email": "diego@diegocon.nl" },
  "keywords": ["batch", "security", "migration", "vulnerability", "remediation", "xss", "sqli", "scan-diff", "regression-gate"]
}
```

- [ ] **Step 2: Verify the JSON parses**

Run: `node -e "const p=require('fs').readFileSync('batch-security-migration/.claude-plugin/plugin.json','utf8'); const j=JSON.parse(p); console.log(j.name, j.version, '| keys:', Object.keys(j).join(','))"`
Expected: `batch-security-migration 1.0.0 | keys: name,version,description,author,keywords` (no `agents` key — this is skill-only, and plugin.json does not require one).

- [ ] **Step 3: Commit**

```bash
git add batch-security-migration/.claude-plugin/plugin.json
git commit -m "feat(batch-security-migration): add plugin manifest (skill-only, no agent)"
```

---

### Task 2: `scan_diff.py` — finding identity + diff core (TDD)

**Files:**
- Create: `batch-security-migration/scripts/scan_diff.py`
- Test: `batch-security-migration/scripts/test_scan_diff.py`

**Interfaces:**
- Consumes: scanner JSON shape from Global Constraints.
- Produces:
  - `load_findings(path: str) -> list[dict]` — reads a scan JSON file, returns `data["findings"]` (raises `SystemExit` with a clear message on parse failure / missing file).
  - `finding_key(f: dict) -> tuple` — returns `(f["severity"], f["category"], f["subcategory"], f["file"], f["line"], f["description"])`.
  - `diff_findings(before: list[dict], after: list[dict]) -> dict` — returns `{"new": [...], "fixed": [...], "unchanged": [...]}` (lists of finding dicts from `after` for new/unchanged, from `before` for fixed), keyed by `finding_key`.
  - `has_blocking(new: list[dict]) -> bool` — True if any finding in `new` has `severity` in `{"HIGH", "CRITICAL"}`.

- [ ] **Step 1: Write the failing tests**

Create `batch-security-migration/scripts/test_scan_diff.py`:

```python
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "scan_diff.py"

# Real scanner finding shape (verified against plugin-security-checker v3.2.0).
def make_finding(severity, category="Cat", subcategory="Sub", file="f.py",
                 line=1, description="desc", fid="FINDING-001"):
    return {
        "id": fid, "severity": severity, "category": category,
        "subcategory": subcategory, "file": file, "line": line, "column": 0,
        "code_snippet": "x", "description": description, "explanation": "e",
        "impact": "i", "recommendation": "r", "cvss_score": 9.8,
        "cve_reference": None, "owasp_reference": None,
        "remediation_effort": "HIGH", "false_positive_likelihood": "LOW",
    }

def write_scan(findings):
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for f in findings:
        counts[f["severity"]] += 1
    data = {"metadata": {}, "summary": {"severity_counts": counts, "categories": {}},
            "findings": findings, "disclaimer": "x"}
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(data, fh)
    fh.close()
    return fh.name


class TestCore(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import scan_diff
        self.m = scan_diff

    def test_finding_key_excludes_id(self):
        a = make_finding("HIGH", fid="FINDING-001")
        b = make_finding("HIGH", fid="FINDING-999")
        self.assertEqual(self.m.finding_key(a), self.m.finding_key(b))

    def test_diff_new_fixed_unchanged(self):
        before = [make_finding("LOW", description="stays"),
                  make_finding("CRITICAL", description="gets-fixed")]
        after = [make_finding("LOW", description="stays"),
                 make_finding("HIGH", description="brand-new")]
        d = self.m.diff_findings(before, after)
        self.assertEqual([f["description"] for f in d["new"]], ["brand-new"])
        self.assertEqual([f["description"] for f in d["fixed"]], ["gets-fixed"])
        self.assertEqual([f["description"] for f in d["unchanged"]], ["stays"])

    def test_has_blocking_true_on_high(self):
        self.assertTrue(self.m.has_blocking([make_finding("HIGH")]))
        self.assertTrue(self.m.has_blocking([make_finding("CRITICAL")]))

    def test_has_blocking_false_on_medium_and_below(self):
        self.assertFalse(self.m.has_blocking([make_finding("MEDIUM"),
                                              make_finding("LOW"),
                                              make_finding("INFO")]))

    def test_load_findings_bad_file_exits(self):
        with self.assertRaises(SystemExit):
            self.m.load_findings("/no/such/file.json")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 batch-security-migration/scripts/test_scan_diff.py -v 2>&1 | tail -20`
Expected: FAIL / ERROR — `scan_diff` module not found (file doesn't exist yet).

- [ ] **Step 3: Write the minimal implementation**

Create `batch-security-migration/scripts/scan_diff.py`:

```python
#!/usr/bin/env python3
"""scan_diff.py — before/after plugin-security-checker regression gate.

Runs (or consumes) two plugin-security-checker scans, diffs their findings, and
exits 1 if the migration introduced any new HIGH/CRITICAL finding.

Zero third-party deps (stdlib only).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

BLOCKING = {"HIGH", "CRITICAL"}
# Scanner location relative to this script: batch-security-migration/scripts/ -> repo root
DEFAULT_SCANNER = (Path(__file__).resolve().parent.parent.parent
                   / "plugin-security-checker" / "scripts" / "scan_plugin.py")


def load_findings(path):
    """Read a scanner JSON file; return its findings list. Exit on failure."""
    try:
        with open(path) as fh:
            data = json.load(fh)
    except FileNotFoundError:
        sys.exit(f"error: scan file not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: could not parse {path}: {exc}")
    return data.get("findings", [])


def finding_key(f):
    """Identity of a finding, excluding the unstable sequential `id`."""
    return (f["severity"], f["category"], f["subcategory"],
            f["file"], f["line"], f["description"])


def diff_findings(before, after):
    before_keys = {finding_key(f) for f in before}
    after_keys = {finding_key(f) for f in after}
    return {
        "new": [f for f in after if finding_key(f) not in before_keys],
        "fixed": [f for f in before if finding_key(f) not in after_keys],
        "unchanged": [f for f in after if finding_key(f) in before_keys],
    }


def has_blocking(new):
    return any(f["severity"] in BLOCKING for f in new)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 batch-security-migration/scripts/test_scan_diff.py -v 2>&1 | tail -20`
Expected: PASS — 5 tests OK.

- [ ] **Step 5: Commit**

```bash
git add batch-security-migration/scripts/scan_diff.py batch-security-migration/scripts/test_scan_diff.py
git commit -m "feat(batch-security-migration): scan_diff core — finding identity + diff (TDD)"
```

---

### Task 3: `scan_diff.py` — CLI, scanning, report, exit codes (TDD)

**Files:**
- Modify: `batch-security-migration/scripts/scan_diff.py` (append CLI + `run_scanner` + `render` + `main`)
- Test: `batch-security-migration/scripts/test_scan_diff.py` (add CLI-level subprocess tests)

**Interfaces:**
- Consumes: `load_findings`, `diff_findings`, `has_blocking` from Task 2; `DEFAULT_SCANNER`.
- Produces:
  - `run_scanner(target: str, scanner: Path) -> list[dict]` — runs `scan_plugin.py <target> --output <tmp> --format json`, returns findings; exits with scanner stderr on non-zero.
  - `render(diff: dict, before: list, after: list) -> str` — compact per-severity before→after table + NEW findings list.
  - `main(argv=None) -> int` — argparse CLI. Two input modes: two JSON files (positional `before after`) OR `--scan BEFORE_DIR AFTER_DIR`. Flags: `--report-only` (force exit 0), `--scanner PATH`. Returns 1 if `has_blocking(diff["new"])` and not `--report-only`, else 0.
  - Module run guard: `if __name__ == "__main__": sys.exit(main())`.

- [ ] **Step 1: Write the failing tests** (append inside `test_scan_diff.py`, before the `if __name__` line)

```python
class TestCLI(unittest.TestCase):
    def run_cli(self, args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              capture_output=True, text=True)

    def test_new_high_exits_1(self):
        before = write_scan([])
        after = write_scan([make_finding("HIGH", description="brand-new")])
        r = self.run_cli([before, after])
        self.assertEqual(r.returncode, 1)
        self.assertIn("brand-new", r.stdout)

    def test_fixed_finding_exits_0(self):
        before = write_scan([make_finding("CRITICAL", description="was-here")])
        after = write_scan([])
        r = self.run_cli([before, after])
        self.assertEqual(r.returncode, 0)
        self.assertIn("was-here", r.stdout)  # listed under FIXED

    def test_report_only_suppresses_exit_1(self):
        before = write_scan([])
        after = write_scan([make_finding("HIGH", description="brand-new")])
        r = self.run_cli([before, after, "--report-only"])
        self.assertEqual(r.returncode, 0)

    def test_identity_keying_same_finding_diff_id_is_unchanged(self):
        before = write_scan([make_finding("HIGH", description="same", fid="FINDING-001")])
        after = write_scan([make_finding("HIGH", description="same", fid="FINDING-777")])
        r = self.run_cli([before, after])
        self.assertEqual(r.returncode, 0)  # not new -> no block

    def test_scan_mode_end_to_end(self):
        # Smoke test: --scan over two real plugin dirs runs the real scanner.
        # gdpr-auditor has 0 findings both sides -> no new HIGH -> exit 0.
        repo = SCRIPT.resolve().parent.parent.parent
        target = str(repo / "gdpr-auditor")
        r = self.run_cli(["--scan", target, target])
        self.assertEqual(r.returncode, 0, msg=r.stderr)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 batch-security-migration/scripts/test_scan_diff.py -v 2>&1 | tail -25`
Expected: the new `TestCLI` tests FAIL — `main` not defined / no CLI behavior; `TestCore` still passes.

- [ ] **Step 3: Append the implementation** to `scan_diff.py`:

```python
def run_scanner(target, scanner):
    if not Path(scanner).exists():
        sys.exit(f"error: scanner not found at {scanner} "
                 f"(override with --scanner PATH)")
    import tempfile
    out = tempfile.NamedTemporaryFile("r", suffix=".json", delete=False)
    out.close()
    proc = subprocess.run(
        [sys.executable, str(scanner), target,
         "--output", out.name, "--format", "json"],
        capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"error: scanner failed on {target}:\n{proc.stderr}")
    return load_findings(out.name)


def render(diff, before, after):
    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
    def counts(findings):
        c = {k: 0 for k in order}
        for f in findings:
            c[f["severity"]] = c.get(f["severity"], 0) + 1
        return c
    cb, ca = counts(before), counts(after)
    lines = ["Severity   before -> after"]
    for sev in order:
        lines.append(f"  {sev:<8} {cb[sev]:>5} -> {ca[sev]:<5}")
    lines.append("")
    lines.append(f"new: {len(diff['new'])}  fixed: {len(diff['fixed'])}  "
                 f"unchanged: {len(diff['unchanged'])}")
    if diff["new"]:
        lines.append("\nNEW findings:")
        for f in diff["new"]:
            lines.append(f"  [{f['severity']}] {f['file']}:{f['line']} "
                         f"{f['description']}")
    if diff["fixed"]:
        lines.append("\nFIXED findings:")
        for f in diff["fixed"]:
            lines.append(f"  [{f['severity']}] {f['file']}:{f['line']} "
                         f"{f['description']}")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Diff two plugin-security-checker scans; fail on new HIGH/CRITICAL.")
    p.add_argument("before", nargs="?", help="before scan JSON (omit when using --scan)")
    p.add_argument("after", nargs="?", help="after scan JSON (omit when using --scan)")
    p.add_argument("--scan", nargs=2, metavar=("BEFORE_DIR", "AFTER_DIR"),
                   help="scan two plugin dirs with the bundled scanner instead of "
                        "passing pre-made JSON files")
    p.add_argument("--scanner", default=str(DEFAULT_SCANNER),
                   help="path to scan_plugin.py (default: bundled plugin-security-checker)")
    p.add_argument("--report-only", action="store_true",
                   help="print the diff but always exit 0 (escape hatch)")
    args = p.parse_args(argv)

    if args.scan:
        before = run_scanner(args.scan[0], Path(args.scanner))
        after = run_scanner(args.scan[1], Path(args.scanner))
    elif args.before and args.after:
        before = load_findings(args.before)
        after = load_findings(args.after)
    else:
        p.error("provide two scan JSON files, or use --scan BEFORE_DIR AFTER_DIR")

    diff = diff_findings(before, after)
    if not before and not after:
        print("no findings; nothing to compare")
        return 0
    print(render(diff, before, after))

    if has_blocking(diff["new"]) and not args.report_only:
        print("\nGATE: FAIL — new HIGH/CRITICAL finding(s) introduced.")
        return 1
    print("\nGATE: PASS — no new HIGH/CRITICAL findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 batch-security-migration/scripts/test_scan_diff.py -v 2>&1 | tail -25`
Expected: PASS — all 10 tests OK (5 core + 5 CLI). The `--scan` smoke test invokes the real scanner on `gdpr-auditor` (0 findings) → exit 0.

- [ ] **Step 5: Make the script executable + commit**

```bash
chmod +x batch-security-migration/scripts/scan_diff.py
git add batch-security-migration/scripts/scan_diff.py batch-security-migration/scripts/test_scan_diff.py
git commit -m "feat(batch-security-migration): scan_diff CLI, scan mode, report, exit codes (TDD)"
```

---

### Task 4: `SKILL.md` — the recipe knowledge surface

**Files:**
- Create: `batch-security-migration/SKILL.md`

**Interfaces:**
- Consumes: `scripts/scan_diff.py` (referenced in the post-migration workflow).
- Produces: a loadable skill manifest. Frontmatter `name` must equal the dir name `batch-security-migration`.

- [ ] **Step 1: Write SKILL.md**

Create `batch-security-migration/SKILL.md`:

```markdown
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
```

- [ ] **Step 2: Verify frontmatter parses and name matches the dir**

Run: `python3 -c "import re,sys; t=open('batch-security-migration/SKILL.md').read(); m=re.match(r'^---\n(.*?)\n---', t, re.S); body=m.group(1); assert 'name: batch-security-migration' in body, 'name mismatch'; assert 'description:' in body, 'no description'; print('frontmatter OK')"`
Expected: `frontmatter OK`

- [ ] **Step 3: Commit**

```bash
git add batch-security-migration/SKILL.md
git commit -m "feat(batch-security-migration): SKILL.md — 7 /batch recipes with safety tiers"
```

---

### Task 5: Marketplace registration + doc-drift verification

**Files:**
- Modify: `.claude-plugin/marketplace.json` (add 13th entry)

**Interfaces:**
- Consumes: the plugin dir from Tasks 1–4.
- Produces: a 13-entry marketplace; `check_doc_drift.py` reads 13 and exits 0.

- [ ] **Step 1: Add the marketplace entry**

Insert this object into the `plugins` array in `.claude-plugin/marketplace.json` (after the `security-hooks` entry — it mirrors that entry's shape exactly):

```json
{
  "name": "batch-security-migration",
  "description": "Recipe skill that turns Claude Code's built-in /batch into a security-migration tool: 7 copy-paste batch recipes (XSS innerHTML→textContent, HTTP→HTTPS, SQLi parameterization, input validation, log PII redaction, secret rotation, dependency CVE patches), each with a safety tier and false-positive trap, plus scan_diff.py — a before/after plugin-security-checker gate that fails on any new HIGH/CRITICAL finding.",
  "source": "./batch-security-migration",
  "version": "1.0.0",
  "author": {
    "name": "Diego Consolini",
    "email": "diego@diegocon.nl"
  },
  "category": "security",
  "keywords": [
    "batch",
    "security",
    "migration",
    "vulnerability",
    "remediation",
    "xss",
    "sqli",
    "scan-diff",
    "regression-gate"
  ],
  "homepage": "https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/batch-security-migration",
  "repository": "https://github.com/diegocconsolini/ClaudeSkillCollection",
  "license": "MIT"
}
```

- [ ] **Step 2: Verify the marketplace parses and now has 13 plugins**

Run: `python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); ns=[p['name'] for p in d['plugins']]; print(len(ns), 'plugins'); assert 'batch-security-migration' in ns; assert len(ns)==len(set(ns)), 'dup names'; print('OK, no dupes')"`
Expected: `13 plugins` then `OK, no dupes`.

- [ ] **Step 3: Run the doc-drift checker**

Run: `python3 scripts/check_doc_drift.py; echo "exit: $?"`
Expected: `marketplace_plugins: 13` and `No doc drift detected.` and `exit: 0`.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(batch-security-migration): register 13th marketplace plugin"
```

---

### Task 6: Full-suite verification + self-scan (no new exposure)

**Files:** none (verification only).

**Interfaces:** consumes everything above.

- [ ] **Step 1: Run the plugin's own tests once more from a clean state**

Run: `python3 batch-security-migration/scripts/test_scan_diff.py -v 2>&1 | tail -5`
Expected: `OK` (10 tests).

- [ ] **Step 2: Self-scan the new plugin with the marketplace's own scanner**

Run: `python3 plugin-security-checker/scripts/scan_plugin.py batch-security-migration --output /tmp/bsm_scan.json --format json >/dev/null 2>&1; python3 -c "import json; s=json.load(open('/tmp/bsm_scan.json'))['summary']['severity_counts']; print(s); assert s['CRITICAL']==0 and s['HIGH']==0, 'new plugin must not ship HIGH/CRITICAL'; print('clean')"`
Expected: severity_counts printed, then `clean` (the plugin we ship must not itself trip the gate it enforces). If HIGH/CRITICAL appear, triage them before finishing — likely a recipe-example string the scanner reads as a real IOC; move it into a code fence or rephrase.

- [ ] **Step 3: Confirm working tree is clean and nothing sensitive was added**

Run: `git status --short && git log --oneline -6`
Expected: clean tree (gitwatch may have an unrelated auto-commit — that's fine and local-only); the last several commits are the 5 feature commits above.

- [ ] **Step 4: Final commit if Step 2 required a fix** (otherwise skip)

```bash
git add batch-security-migration/
git commit -m "fix(batch-security-migration): de-trip self-scan finding"
```

---

## Self-Review

**Spec coverage:**
- Recipe skill wrapping built-in `/batch` → Task 4 (SKILL.md, 7 recipes). ✅
- 7 recipes with safety tiers + false-positive traps → Task 4 table + per-recipe sections; tiers match approved decision (6 & 7 are 🔴). ✅
- Pre-scan checklist + post-migration workflow → Task 4. ✅
- `scan_diff.py` validation gate, identity excludes `id`, exit 1 on new HIGH+, `--report-only`, `--scan` mode, script-relative scanner with `--scanner` override → Tasks 2–3. ✅
- Tests (new HIGH→exit1, fixed→exit0, --report-only, identity keying, --scan e2e) → Task 3 maps 1:1 to the spec's 5 test cases. ✅
- plugin.json (no agents array) + marketplace 13th entry → Tasks 1, 5. ✅
- Doc-drift 12→13 → Task 5 Step 3. ✅
- Error handling (scanner not found, malformed JSON, scanner non-zero, empty-both) → `run_scanner` / `load_findings` / `main` empty-both branch in Task 3. ✅

**Placeholder scan:** No TBD/TODO; every code step has complete content. ✅

**Type consistency:** `finding_key` signature identical across Tasks 2–3; `diff_findings` returns `{"new","fixed","unchanged"}` consumed unchanged by `render`/`main`; `has_blocking` used in `main` exactly as defined. ✅
```