#!/usr/bin/env python3
"""
Batch scanner for marketplace repos using IntelligentOrchestrator v3.0.0
Scans 305 repos with minimal token usage
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from intelligent_orchestrator import IntelligentOrchestrator


def scan_marketplace_batch(repos_dir: str, output_dir: str):
    """Scan all repos in marketplace directory"""

    repos_path = Path(repos_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all repo directories
    repos = sorted([d for d in repos_path.iterdir() if d.is_dir() and d.name.startswith('repo-')])

    print("=" * 80)
    print(f"Plugin Security Checker v3.0.0 - Marketplace Batch Scan")
    print(f"IntelligentOrchestrator with 91 Agents + Consensus Voting")
    print("=" * 80)
    print(f"Repos Directory: {repos_path}")
    print(f"Output Directory: {output_path}")
    print(f"Found: {len(repos)} repositories")
    print("")

    # Initialize orchestrator
    patterns_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded.json"
    orchestrator = IntelligentOrchestrator(
        patterns_file=str(patterns_file),
        max_memory_mb=500,
        enable_adaptive_routing=True
    )

    # Scan results
    results = {
        'scan_date': datetime.now().isoformat(),
        'total_repos': len(repos),
        'scanned': 0,
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0,
        'clean': 0,
        'findings': []
    }

    # Scan each repo
    for i, repo_dir in enumerate(repos, 1):
        repo_name = repo_dir.name
        print(f"[{i}/{len(repos)}] Scanning {repo_name}...")

        # Find all Python and JavaScript files
        py_files = list(repo_dir.rglob('*.py'))
        js_files = list(repo_dir.rglob('*.js'))

        all_detections = []

        # Scan Python files
        for py_file in py_files:
            try:
                code = py_file.read_text(encoding='utf-8', errors='ignore')
                detections = orchestrator.scan_file(str(py_file), code)
                all_detections.extend(detections)
            except Exception as e:
                print(f"  Error scanning {py_file.name}: {e}")

        # Scan JavaScript files
        for js_file in js_files:
            try:
                code = js_file.read_text(encoding='utf-8', errors='ignore')
                detections = orchestrator.scan_file(str(js_file), code)
                all_detections.extend(detections)
            except Exception as e:
                print(f"  Error scanning {js_file.name}: {e}")

        # Determine risk level
        if all_detections:
            critical_count = sum(1 for d in all_detections if d.severity == 'CRITICAL')
            high_count = sum(1 for d in all_detections if d.severity == 'HIGH')
            medium_count = sum(1 for d in all_detections if d.severity == 'MEDIUM')
            low_count = sum(1 for d in all_detections if d.severity == 'LOW')

            if critical_count > 0:
                risk = 'CRITICAL'
                results['critical'] += 1
            elif high_count > 0:
                risk = 'HIGH'
                results['high'] += 1
            elif medium_count > 0:
                risk = 'MEDIUM'
                results['medium'] += 1
            else:
                risk = 'LOW'
                results['low'] += 1

            print(f"  {risk}: {len(all_detections)} findings (C:{critical_count} H:{high_count} M:{medium_count} L:{low_count})")

            results['findings'].append({
                'repo': repo_name,
                'risk': risk,
                'total_detections': len(all_detections),
                'critical': critical_count,
                'high': high_count,
                'medium': medium_count,
                'low': low_count,
                'files_scanned': len(py_files) + len(js_files)
            })
        else:
            print(f"  CLEAN")
            results['clean'] += 1
            results['findings'].append({
                'repo': repo_name,
                'risk': 'CLEAN',
                'total_detections': 0,
                'files_scanned': len(py_files) + len(js_files)
            })

        results['scanned'] += 1

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = output_path / f"marketplace_scan_{timestamp}.json"

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Export orchestrator findings
    atlas_file = output_path / f"atlas_export_{timestamp}.json"
    orchestrator.export_findings(str(atlas_file))

    # Print summary
    print("")
    print("=" * 80)
    print("SCAN COMPLETE")
    print("=" * 80)
    print(f"Total Repos: {results['total_repos']}")
    print(f"Scanned: {results['scanned']}")
    print("")
    print("Risk Distribution:")
    print(f"  CRITICAL  : {results['critical']:4d} ({results['critical']/results['scanned']*100:5.1f}%)")
    print(f"  HIGH      : {results['high']:4d} ({results['high']/results['scanned']*100:5.1f}%)")
    print(f"  MEDIUM    : {results['medium']:4d} ({results['medium']/results['scanned']*100:5.1f}%)")
    print(f"  LOW       : {results['low']:4d} ({results['low']/results['scanned']*100:5.1f}%)")
    print(f"  CLEAN     : {results['clean']:4d} ({results['clean']/results['scanned']*100:5.1f}%)")
    print("")
    print(f"Results saved to: {results_file}")
    print(f"ATLAS export: {atlas_file}")

    # Get orchestrator stats
    stats = orchestrator.get_statistics()
    print("")
    print("Orchestrator Statistics:")
    print(f"  Memory usage: {stats['memory_usage_mb']:.2f} MB / {stats['memory_limit_mb']:.2f} MB")
    print(f"  Total detections: {stats['total_detections']}")
    print(f"  Consensus detections: {stats['consensus_detections']}")
    print(f"  Conflicts resolved: {stats['conflicts_resolved']}")


if __name__ == "__main__":
    repos_dir = sys.argv[1] if len(sys.argv) > 1 else "marketplace-repos-2025"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "v3_scan_results"

    scan_marketplace_batch(repos_dir, output_dir)
