#!/usr/bin/env python3
"""
Version Sync Script for Security Report Builder

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


def sync_readme(version: str, dry_run: bool = True) -> list:
    """Sync version in README.md"""
    changes = []
    readme = Path(__file__).parent.parent / "README.md"

    if readme.exists():
        with open(readme, 'r') as f:
            content = f.read()

        new_content = content

        # Update version at end of file
        pattern = r'\*\*Version:\*\* [\d.]+'
        replacement = f'**Version:** {version}'
        if re.search(pattern, content):
            match = re.search(pattern, content)
            if match.group() != replacement:
                new_content = re.sub(pattern, replacement, new_content)
                changes.append(f"README.md: {match.group()} -> {replacement}")

        if new_content != content:
            if not dry_run:
                with open(readme, 'w') as f:
                    f.write(new_content)

    return changes


def sync_skill_md(version: str, last_updated: str, dry_run: bool = True) -> list:
    """Sync version in SKILL.md"""
    changes = []
    skill_md = Path(__file__).parent.parent / "SKILL.md"

    if skill_md.exists():
        with open(skill_md, 'r') as f:
            content = f.read()

        new_content = content

        # Update version header
        pattern = r'\*\*Version:\*\* [\d.]+'
        replacement = f'**Version:** {version}'
        if re.search(pattern, content):
            match = re.search(pattern, content)
            if match.group() != replacement:
                new_content = re.sub(pattern, replacement, new_content)
                changes.append(f"SKILL.md version: {match.group()} -> {replacement}")

        # Update last updated
        pattern = r'\*\*Last Updated:\*\* [\d-]+'
        replacement = f'**Last Updated:** {last_updated}'
        if re.search(pattern, content):
            match = re.search(pattern, content)
            if match.group() != replacement:
                new_content = re.sub(pattern, replacement, new_content)
                changes.append(f"SKILL.md last_updated: {match.group()} -> {replacement}")

        if new_content != content:
            if not dry_run:
                with open(skill_md, 'w') as f:
                    f.write(new_content)

    return changes


def sync_agent_file(version: str, dry_run: bool = True) -> list:
    """Sync version in agent file"""
    changes = []
    agent_file = Path(__file__).parent.parent / "agents" / "security-report-builder.md"

    if agent_file.exists():
        with open(agent_file, 'r') as f:
            content = f.read()

        new_content = content

        # Update version references (if any)
        pattern = r'Security Report Builder v[\d.]+'
        replacement = f'Security Report Builder v{version}'
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, new_content)
            if new_content != content:
                changes.append(f"agent file: updated version to v{version}")

        if new_content != content:
            if not dry_run:
                with open(agent_file, 'w') as f:
                    f.write(new_content)

    return changes


def sync_config_files(version: str, dry_run: bool = True) -> list:
    """Sync version in config files"""
    changes = []
    config_dir = Path(__file__).parent.parent / "config"

    for config_file in ['severity_rules.json', 'report_config.json']:
        filepath = config_dir / config_file
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)

            if data.get('version') != version:
                changes.append(f"{config_file}: {data.get('version')} -> {version}")
                if not dry_run:
                    data['version'] = version
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2)
                        f.write('\n')

    return changes


def main():
    dry_run = '--apply' not in sys.argv

    print("=" * 60)
    print("Security Report Builder - Version Sync")
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
    frameworks = version_info.get('frameworks', {})
    last_updated = version_info['last_updated']

    print(f"Source: version.json")
    print(f"  Plugin Version: {version}")
    print(f"  Frameworks: ATT&CK {frameworks.get('mitre_attack')}, OWASP {frameworks.get('owasp_top10')}")
    print(f"  Last Updated: {last_updated}")
    print()

    # Collect all changes
    all_changes = []
    all_changes.extend(sync_plugin_json(version, dry_run))
    all_changes.extend(sync_readme(version, dry_run))
    all_changes.extend(sync_skill_md(version, last_updated, dry_run))
    all_changes.extend(sync_agent_file(version, dry_run))
    all_changes.extend(sync_config_files(version, dry_run))

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
