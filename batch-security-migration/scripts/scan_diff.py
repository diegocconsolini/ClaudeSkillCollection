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


def run_scanner(target, scanner):
    if not Path(scanner).exists():
        sys.exit(f"error: scanner not found at {scanner} "
                 f"(override with --scanner PATH)")
    import os
    import tempfile
    out = tempfile.NamedTemporaryFile("r", suffix=".json", delete=False)
    out.close()
    try:
        proc = subprocess.run(
            [sys.executable, str(scanner), target,
             "--output", out.name, "--format", "json"],
            capture_output=True, text=True)
        if proc.returncode != 0:
            sys.exit(f"error: scanner failed on {target}:\n{proc.stderr}")
        return load_findings(out.name)
    finally:
        try:
            os.unlink(out.name)
        except FileNotFoundError:
            pass


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
