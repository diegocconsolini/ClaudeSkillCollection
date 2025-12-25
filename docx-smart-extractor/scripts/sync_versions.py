#!/usr/bin/env python3
"""
Unified Version Synchronization for DOCX Smart Extractor

Single source of truth: version.json
Syncs version across: plugin.json, README.md, SKILL.md
"""

import json
import re
import sys
from pathlib import Path


def load_version_config():
    version_file = Path(__file__).parent.parent / "version.json"
    if not version_file.exists():
        print(f"ERROR: {version_file} not found")
        sys.exit(1)
    with open(version_file) as f:
        return json.load(f)


def update_plugin_json(version: str, dry_run: bool = True) -> bool:
    plugin_file = Path(__file__).parent.parent / ".claude-plugin" / "plugin.json"
    if not plugin_file.exists():
        print(f"  SKIP: {plugin_file} not found")
        return False
    with open(plugin_file) as f:
        data = json.load(f)
    current = data.get("version", "unknown")
    if current == version:
        print(f"  OK: plugin.json already at {version}")
        return True
    if dry_run:
        print(f"  WOULD UPDATE: plugin.json {current} -> {version}")
        return False
    data["version"] = version
    with open(plugin_file, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"  UPDATED: plugin.json {current} -> {version}")
    return True


def update_markdown_file(filepath: Path, version: str, dry_run: bool = True) -> bool:
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return False
    content = filepath.read_text()
    original = content
    patterns = [
        (r'\*\*Version:\*\*\s*\d+\.\d+\.\d+', f'**Version:** {version}'),
        (r'\*\*\d+\.\d+\.\d+\*\*\s*-\s*Production', f'**{version}** - Production'),
        (r'Version:\s*\d+\.\d+\.\d+', f'Version: {version}'),
    ]
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    if content == original:
        print(f"  OK: {filepath.name} (no version patterns or already current)")
        return True
    if dry_run:
        print(f"  WOULD UPDATE: {filepath.name}")
        return False
    filepath.write_text(content)
    print(f"  UPDATED: {filepath.name}")
    return True


def main():
    dry_run = "--apply" not in sys.argv
    print("=" * 60)
    print("DOCX Smart Extractor - Version Synchronization")
    print("=" * 60)
    config = load_version_config()
    version = config["plugin_version"]
    print(f"\nSource: version.json | Target: {version}")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLYING'}\n")
    base_dir = Path(__file__).parent.parent
    files = [
        ("plugin.json", lambda: update_plugin_json(version, dry_run)),
        ("README.md", lambda: update_markdown_file(base_dir / "README.md", version, dry_run)),
        ("SKILL.md", lambda: update_markdown_file(base_dir / "SKILL.md", version, dry_run)),
    ]
    print("Checking files:")
    results = [f() for _, f in files]
    print()
    if all(results):
        print("All files in sync!")
    elif dry_run:
        print("Run with --apply to update.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
