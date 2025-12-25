#!/usr/bin/env python3
"""
Plugin Security Checker v3.0.0 - Main Scanner
Uses IntelligentOrchestrator with 91 specialized agents

Scans a single plugin with consensus voting and ATLAS export
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Import v3.0.0 components
from intelligent_orchestrator import IntelligentOrchestrator


def scan_plugin_v3(plugin_path: str, output_file: str = None, format: str = "text"):
    """
    Scan plugin using IntelligentOrchestrator v3.0.0

    Args:
        plugin_path: Path to plugin directory
        output_file: Optional output file for results
        format: Output format (text, json)
    """
    plugin_dir = Path(plugin_path)

    if not plugin_dir.exists():
        print(f"Error: Plugin directory not found: {plugin_path}")
        sys.exit(1)

    print("=" * 80)
    print(f"Plugin Security Checker v3.0.0")
    print(f"IntelligentOrchestrator with 91 Agents + Consensus Voting")
    print("=" * 80)
    print(f"Plugin: {plugin_dir}")
    print("")

    # Initialize orchestrator
    patterns_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded.json"

    print("[*] Initializing IntelligentOrchestrator...")
    orchestrator = IntelligentOrchestrator(
        patterns_file=str(patterns_file),
        max_memory_mb=500,
        enable_adaptive_routing=True
    )
    print(f"    ✓ 91 specialized agents loaded")
    print(f"    ✓ AccuracyCache initialized")
    print(f"    ✓ Consensus voting enabled")
    print("")

    # Find all code files
    print("[*] Discovering files...")
    py_files = list(plugin_dir.rglob('*.py'))
    js_files = list(plugin_dir.rglob('*.js'))
    all_files = py_files + js_files

    print(f"    Found {len(py_files)} Python files")
    print(f"    Found {len(js_files)} JavaScript files")
    print(f"    Total: {len(all_files)} files to scan")
    print("")

    # Scan all files
    print("[*] Scanning with 91 agents...")
    all_detections = []
    files_scanned = 0

    for code_file in all_files:
        try:
            code = code_file.read_text(encoding='utf-8', errors='ignore')
            detections = orchestrator.scan_file(str(code_file), code)

            if detections:
                all_detections.extend(detections)
                print(f"    {code_file.name}: {len(detections)} detections")

            files_scanned += 1

        except Exception as e:
            print(f"    Error scanning {code_file.name}: {e}")

    print("")
    print(f"[*] Scan complete: {files_scanned}/{len(all_files)} files scanned")
    print("")

    # Analyze results
    if all_detections:
        # Count by severity
        critical = sum(1 for d in all_detections if d.severity == 'CRITICAL')
        high = sum(1 for d in all_detections if d.severity == 'HIGH')
        medium = sum(1 for d in all_detections if d.severity == 'MEDIUM')
        low = sum(1 for d in all_detections if d.severity == 'LOW')

        # Determine risk level
        if critical > 0:
            risk_level = "CRITICAL"
            verdict = "DO NOT INSTALL"
        elif high > 0:
            risk_level = "HIGH"
            verdict = "REVIEW CAREFULLY"
        elif medium > 0:
            risk_level = "MEDIUM"
            verdict = "REVIEW"
        else:
            risk_level = "LOW"
            verdict = "MINOR ISSUES"

        print("=" * 80)
        print("FINDINGS SUMMARY")
        print("=" * 80)
        print(f"Risk Level: {risk_level}")
        print(f"Verdict: {verdict}")
        print(f"Total Detections: {len(all_detections)}")
        print("")
        print("By Severity:")
        print(f"  CRITICAL: {critical}")
        print(f"  HIGH:     {high}")
        print(f"  MEDIUM:   {medium}")
        print(f"  LOW:      {low}")
        print("")

        # Show top findings
        print("Top Findings:")
        severity_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        for i, det in enumerate(sorted(all_detections,
                                      key=lambda x: severity_order.get(x.severity, 0),  # Handle unknown severities
                                      reverse=True)[:5], 1):
            print(f"{i}. [{det.severity}] Line {det.line_number}: {det.explanation[:60]}...")
            print(f"   Voting agents: {det.vote_count} ({', '.join(det.voting_agents[:3])})")
            print(f"   Confidence: {det.confidence:.0%}")
            print("")

    else:
        risk_level = "CLEAN"
        verdict = "NO ISSUES FOUND"
        print("=" * 80)
        print("SCAN RESULTS")
        print("=" * 80)
        print(f"✓ No security issues detected")
        print(f"✓ {files_scanned} files scanned")
        print("")
        print("Note: This does NOT guarantee safety. Always review code manually.")
        print("")

    # Get orchestrator statistics
    stats = orchestrator.get_statistics()
    print("=" * 80)
    print("ORCHESTRATOR STATISTICS")
    print("=" * 80)
    print(f"Memory usage: {stats['memory_usage_mb']:.2f} MB / {stats['memory_limit_mb']:.2f} MB")
    print(f"Scans completed: {stats['scans_completed']}")
    print(f"Total detections: {stats['total_detections']}")
    print(f"Consensus detections: {stats['consensus_detections']}")
    print(f"Conflicts resolved: {stats['conflicts_resolved']}")
    print("")

    # Export results
    if output_file or format == "json":
        output_path = Path(output_file) if output_file else Path(f"scan_{plugin_dir.name}.json")

        results = {
            'metadata': {
                'plugin_path': str(plugin_dir),
                'scan_date': datetime.now().isoformat(),
                'scanner_version': '3.0.0',
                'files_scanned': files_scanned,
                'risk_level': risk_level,
                'verdict': verdict
            },
            'summary': {
                'total_detections': len(all_detections),
                'critical': critical if all_detections else 0,
                'high': high if all_detections else 0,
                'medium': medium if all_detections else 0,
                'low': low if all_detections else 0
            },
            'detections': [
                {
                    'severity': d.severity,
                    'line': d.line_number,
                    'file': d.file_path,
                    'confidence': d.confidence,
                    'voting_agents': d.voting_agents,
                    'vote_count': d.vote_count,
                    'attack_id': d.primary_attack_id,
                    'atlas_id': d.primary_atlas_id,
                    'explanation': d.explanation
                }
                for d in all_detections
            ],
            'orchestrator_stats': stats
        }

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✓ Results saved to: {output_path}")

    # Export ATLAS findings
    atlas_file = Path(f"atlas_{plugin_dir.name}.json")
    orchestrator.export_findings(str(atlas_file))
    print(f"✓ ATLAS export: {atlas_file}")
    print("")

    return len(all_detections), risk_level


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plugin Security Checker v3.0.0 - Scan Claude Code plugin"
    )
    parser.add_argument("plugin_path", help="Path to plugin directory")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text",
                       help="Output format")

    args = parser.parse_args()

    detections, risk = scan_plugin_v3(args.plugin_path, args.output, args.format)

    # Exit code based on risk
    if risk in ["CRITICAL", "HIGH"]:
        sys.exit(1)
    else:
        sys.exit(0)
