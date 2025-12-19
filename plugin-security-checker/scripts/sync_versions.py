#!/usr/bin/env python3
"""
Version Sync Script

Synchronizes version numbers across all plugin files from version.json
(single source of truth).

Usage:
    python3 scripts/sync_versions.py           # Preview changes
    python3 scripts/sync_versions.py --apply   # Apply changes
"""

import json
import re
import sys
from pathlib import Path


def load_version_info() -> dict:
    """Load version info from version.json"""
    script_dir = Path(__file__).parent
    version_file = script_dir.parent / "version.json"
    with open(version_file, 'r') as f:
        return json.load(f)


def sync_plugin_json(version: str, dry_run: bool = True) -> list:
    """Sync version in .claude-plugin/plugin.json"""
    changes = []
    plugin_json = Path(__file__).parent.parent / ".claude-plugin" / "plugin.json"

    if plugin_json.exists():
        with open(plugin_json, 'r') as f:
            data = json.load(f)

        if data.get('version') != version:
            changes.append(f"plugin.json: {data.get('version')} -> {version}")
            if not dry_run:
                data['version'] = version
                with open(plugin_json, 'w') as f:
                    json.dump(data, f, indent=2)
                    f.write('\n')

    return changes


def sync_readme(version: str, threat_intel: dict, dry_run: bool = True) -> list:
    """Sync version in README.md"""
    changes = []
    readme = Path(__file__).parent.parent / "README.md"

    if readme.exists():
        with open(readme, 'r') as f:
            content = f.read()

        new_content = content

        # Update header version
        expected_header = f'# Plugin Security Checker v{version}'
        pattern = r'# Plugin Security Checker v[\d.]+'
        match = re.search(pattern, content)
        if match and match.group() != expected_header:
            new_content = re.sub(pattern, expected_header, new_content)
            changes.append(f"README.md header: {match.group()} -> {expected_header}")

        # Update ATT&CK version in table
        for source, ver in threat_intel.items():
            if source == 'mitre_attack':
                pattern = r'\| MITRE ATT&CK \(Enterprise\) \| v[\d.]+ \|'
                replacement = f'| MITRE ATT&CK (Enterprise) | {ver} |'
                new_content = re.sub(pattern, replacement, new_content)

                pattern = r'\| MITRE ATT&CK \(Mobile\) \| v[\d.]+ \|'
                replacement = f'| MITRE ATT&CK (Mobile) | {ver} |'
                new_content = re.sub(pattern, replacement, new_content)

                pattern = r'\| MITRE ATT&CK \(ICS\) \| v[\d.]+ \|'
                replacement = f'| MITRE ATT&CK (ICS) | {ver} |'
                new_content = re.sub(pattern, replacement, new_content)

        if new_content != content:
            changes.append(f"README.md: updated version references")
            if not dry_run:
                with open(readme, 'w') as f:
                    f.write(new_content)

    return changes


def sync_agent_file(version: str, dry_run: bool = True) -> list:
    """Sync version in agent file"""
    changes = []
    agent_file = Path(__file__).parent.parent / "agents" / "plugin-security-checker.md"

    if agent_file.exists():
        with open(agent_file, 'r') as f:
            content = f.read()

        new_content = content

        # Update version references
        pattern = r'Plugin Security Checker v[\d.]+'
        replacement = f'Plugin Security Checker v{version}'
        new_content = re.sub(pattern, replacement, new_content)

        pattern = r'## Core Features \(v[\d.]+\)'
        replacement = f'## Core Features (v{version})'
        new_content = re.sub(pattern, replacement, new_content)

        if new_content != content:
            changes.append(f"agent file: updated version to v{version}")
            if not dry_run:
                with open(agent_file, 'w') as f:
                    f.write(new_content)

    return changes


def sync_threat_mappings(threat_intel: dict, last_updated: str, dry_run: bool = True) -> list:
    """Sync threat intel versions in threat_mappings.json"""
    changes = []
    mappings_file = Path(__file__).parent.parent / "references" / "threat_mappings.json"

    if mappings_file.exists():
        with open(mappings_file, 'r') as f:
            data = json.load(f)

        updated = False
        for key, value in threat_intel.items():
            if data.get('frameworks', {}).get(key) != value:
                changes.append(f"threat_mappings.json: {key} -> {value}")
                data['frameworks'][key] = value
                updated = True

        if data.get('last_updated') != last_updated:
            changes.append(f"threat_mappings.json: last_updated -> {last_updated}")
            data['last_updated'] = last_updated
            updated = True

        if updated and not dry_run:
            with open(mappings_file, 'w') as f:
                json.dump(data, f, indent=2)
                f.write('\n')

    return changes


def main():
    dry_run = '--apply' not in sys.argv

    print("=" * 60)
    print("Plugin Security Checker - Version Sync")
    print("=" * 60)
    print()

    if dry_run:
        print("MODE: Preview (use --apply to make changes)")
    else:
        print("MODE: Apply changes")
    print()

    # Load version info
    version_info = load_version_info()
    version = version_info['plugin_version']
    threat_intel = version_info['threat_intel']
    last_updated = version_info['last_updated']

    print(f"Source: version.json")
    print(f"  Plugin Version: {version}")
    print(f"  ATT&CK Version: {threat_intel.get('mitre_attack')}")
    print(f"  Last Updated: {last_updated}")
    print()

    # Collect all changes
    all_changes = []
    all_changes.extend(sync_plugin_json(version, dry_run))
    all_changes.extend(sync_readme(version, threat_intel, dry_run))
    all_changes.extend(sync_agent_file(version, dry_run))
    all_changes.extend(sync_threat_mappings(threat_intel, last_updated, dry_run))

    if all_changes:
        print("Changes:")
        for change in all_changes:
            print(f"  - {change}")
    else:
        print("No changes needed - all versions are in sync!")

    print()
    if dry_run and all_changes:
        print("Run with --apply to apply these changes.")


if __name__ == '__main__':
    main()
