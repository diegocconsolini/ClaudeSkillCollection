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
