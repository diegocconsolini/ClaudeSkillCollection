#!/usr/bin/env python3
"""
Rescan all marketplace plugins with integrated_scanner.py v2.0.0
Compares results with old scanner to show improvements
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def scan_plugin_v2(plugin_path: Path) -> dict:
    """Scan plugin with new integrated scanner v2.0.0"""
    script_path = Path(__file__).parent / "integrated_scanner.py"

    try:
        # Run scanner with --no-stix for speed, --json for output
        result = subprocess.run(
            [sys.executable, str(script_path), str(plugin_path), "--no-stix"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse output for findings
        output = result.stderr + result.stdout
        findings = []
        risk_score = 0

        # Extract risk score
        for line in output.split('\n'):
            if 'Risk Score:' in line:
                parts = line.split(':')[1].strip().split()
                if parts:
                    risk_score = int(parts[0])
            elif line.strip().startswith('[') and '] ' in line:
                # Parse finding line: [1] CRITICAL - Dangerous Function
                findings.append(line.strip())

        return {
            'success': True,
            'risk_score': risk_score,
            'findings_count': len(findings),
            'findings': findings,
            'output': output
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def find_all_plugins(base_dir: Path) -> list:
    """Find all plugin directories (containing plugin.json)"""
    plugins = []

    for plugin_json in base_dir.rglob('plugin.json'):
        plugin_dir = plugin_json.parent
        plugins.append(plugin_dir)

    return plugins

def main():
    print("=" * 80)
    print(" Plugin Security Checker v2.0.0 - Full Marketplace Rescan")
    print(" With MITRE ATT&CK + ATLAS + 70+ Patterns")
    print("=" * 80)
    print()

    # Paths
    script_dir = Path(__file__).parent.parent  # plugin-security-checker/
    test_plugins_dir = Path.cwd() / "test_plugins_full"
    output_dir = script_dir / "v2_marketplace_scan_results"
    output_dir.mkdir(exist_ok=True)

    print(f"Base Directory: {test_plugins_dir}")
    print(f"Output Directory: {output_dir}")
    print(f"Scan Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Find all plugins
    print("Discovering plugins...")
    plugins = find_all_plugins(test_plugins_dir)
    print(f"✓ Found {len(plugins)} plugins")
    print()

    # Scan all plugins
    results = []
    risk_distribution = defaultdict(int)
    severity_distribution = defaultdict(int)

    print("Scanning plugins...")
    for i, plugin_path in enumerate(plugins, 1):
        plugin_name = plugin_path.name
        repo_name = plugin_path.parent.parent.name if 'repo-' in str(plugin_path) else 'unknown'

        print(f"[{i}/{len(plugins)}] Scanning {repo_name}/{plugin_name}...", end=' ')

        scan_result = scan_plugin_v2(plugin_path)

        if scan_result['success']:
            risk_score = scan_result['risk_score']
            findings_count = scan_result['findings_count']

            # Determine risk level
            if risk_score >= 1000:
                risk_level = 'CRITICAL'
            elif risk_score >= 500:
                risk_level = 'HIGH'
            elif risk_score >= 200:
                risk_level = 'MEDIUM'
            elif risk_score > 0:
                risk_level = 'LOW'
            else:
                risk_level = 'CLEAN'

            risk_distribution[risk_level] += 1

            print(f"{risk_level} (Score: {risk_score}, Findings: {findings_count})")

            results.append({
                'plugin_name': plugin_name,
                'plugin_path': str(plugin_path),
                'repo': repo_name,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'findings_count': findings_count,
                'findings': scan_result['findings']
            })

            # Save individual report if has findings
            if findings_count > 0:
                report_path = output_dir / f"{repo_name}_{plugin_name}_report.txt"
                report_path.write_text(scan_result['output'])
        else:
            print(f"ERROR: {scan_result.get('error', 'Unknown')}")
            results.append({
                'plugin_name': plugin_name,
                'plugin_path': str(plugin_path),
                'repo': repo_name,
                'risk_level': 'ERROR',
                'error': scan_result.get('error')
            })

    print()
    print("=" * 80)
    print(" SCAN COMPLETE")
    print("=" * 80)
    print()

    # Summary
    print("Risk Distribution:")
    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'CLEAN']:
        count = risk_distribution.get(level, 0)
        percentage = (count / len(plugins) * 100) if plugins else 0
        print(f"  {level:10s}: {count:4d} ({percentage:5.2f}%)")

    print()

    # High-risk plugins
    high_risk = [r for r in results if r.get('risk_level') in ['CRITICAL', 'HIGH']]
    if high_risk:
        print(f"High-Risk Plugins Found: {len(high_risk)}")
        print()
        for result in high_risk:
            print(f"  - {result['repo']}/{result['plugin_name']}")
            print(f"    Risk: {result['risk_level']} (Score: {result['risk_score']})")
            print(f"    Findings: {result['findings_count']}")
            print()
    else:
        print("✓ No high-risk plugins found!")

    # Save results
    summary_path = output_dir / f"SCAN_SUMMARY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary_path.write_text(json.dumps({
        'scan_date': datetime.now().isoformat(),
        'scanner_version': '2.0.0',
        'total_plugins': len(plugins),
        'risk_distribution': dict(risk_distribution),
        'high_risk_plugins': high_risk,
        'all_results': results
    }, indent=2))

    print(f"✓ Full results saved to: {summary_path}")
    print()

if __name__ == '__main__':
    main()
