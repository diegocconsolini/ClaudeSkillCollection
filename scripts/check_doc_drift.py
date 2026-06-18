#!/usr/bin/env python3
"""check_doc_drift.py — detect documentation drift (#42 Wiki Auto-Updater, core mechanism).

Derives the real, current numbers from the repo (plugin count, ZIP count, sizes) and
compares them against what README.md / CLAUDE.md claim. Prevents the hardcoded-count
drift found in audit #23 (e.g. "53 wiki pages", "8 of 9 skills", "425 KB").

Usage:
  python3 scripts/check_doc_drift.py          # report drift, exit 1 if any
  python3 scripts/check_doc_drift.py --quiet   # only print drift
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def actual_facts():
    facts = {}
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    if mp.exists():
        facts["marketplace_plugins"] = len(json.loads(mp.read_text())["plugins"])
    pkgs = ROOT / "claude-desktop-skills" / "packages"
    if pkgs.exists():
        zips = sorted(pkgs.glob("*.zip"))
        facts["desktop_zips"] = len(zips)
        facts["desktop_zips_kb"] = round(sum(z.stat().st_size for z in zips) / 1024)
    facts["docs_md_files"] = len(list((ROOT / "docs").glob("*.md"))) if (ROOT / "docs").exists() else 0
    return facts


def find_claims(text):
    """Return claimed numbers we know drift: wiki pages, 'N of M skills', size in KB."""
    claims = {}
    # Only a wiki-context page count (badge/link), not arbitrary "N pages" (e.g. a PDF's
    # page count). Require the word 'wiki' nearby.
    m = re.search(r"wiki[^\n]{0,40}?(\d+)\s*pages|(\d+)\s*pages[^\n]{0,20}?wiki", text, re.I)
    if m:
        claims["wiki_pages"] = int(m.group(1) or m.group(2))
    m = re.search(r"(\d+)\s*of\s*(\d+)\s*skills", text, re.I)
    if m:
        claims["skills_ready"] = (int(m.group(1)), int(m.group(2)))
    m = re.search(r"Total Package Size:\s*([\d,]+)\s*KB", text, re.I)
    if m:
        claims["total_kb"] = int(m.group(1).replace(",", ""))
    return claims


def main():
    quiet = "--quiet" in sys.argv
    facts = actual_facts()
    if not quiet:
        print("Actual repo facts:")
        for k, v in facts.items():
            print(f"  {k}: {v}")
        print()

    drift = []
    for doc in ("README.md", "CLAUDE.md", "claude-desktop-skills/README.md"):
        p = ROOT / doc
        if not p.exists():
            continue
        claims = find_claims(p.read_text(encoding="utf-8", errors="ignore"))
        # skills_ready M should equal marketplace plugin count's desktop subset; we check ZIPs
        if "skills_ready" in claims and "desktop_zips" in facts:
            ready, total = claims["skills_ready"]
            if total != facts["desktop_zips"] and facts["desktop_zips"]:
                drift.append(f"{doc}: claims '{ready} of {total} skills' but {facts['desktop_zips']} ZIPs exist")
        if "total_kb" in claims and "desktop_zips_kb" in facts:
            if abs(claims["total_kb"] - facts["desktop_zips_kb"]) > 20:
                drift.append(f"{doc}: claims '{claims['total_kb']} KB' but ZIPs total {facts['desktop_zips_kb']} KB")
        if "wiki_pages" in claims:
            drift.append(f"{doc}: hardcodes '{claims['wiki_pages']} pages' (wiki is on GitHub; avoid a hardcoded count)")

    if drift:
        print("DOC DRIFT DETECTED:")
        for d in drift:
            print(f"  - {d}")
        return 1
    print("No doc drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
