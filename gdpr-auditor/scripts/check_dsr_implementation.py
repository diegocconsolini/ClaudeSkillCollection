#!/usr/bin/env python3
"""
GDPR Data Subject Rights (DSR) Implementation Checker - Static File Analysis Tool

Scans source code for data subject rights endpoint definitions and implementation patterns
(access, portability, erasure, rectification, objection, consent management).

IMPORTANT - STATIC ANALYSIS ONLY:
This script analyzes static source code files. It does NOT:
- Test live API endpoints or make HTTP requests
- Execute code or test actual functionality
- Verify if endpoints work correctly at runtime
- Connect to running applications or servers
- Require API keys, credentials, or authentication
- Monitor live traffic or API usage

Analyzes: Source code files containing API route definitions, endpoint handlers
Purpose: Verify data subject rights are implemented in code for GDPR compliance
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Data Subject Rights to check for
DSR_REQUIREMENTS = {
    "right_to_access": {
        "description": "Right to access personal data (Article 15)",
        "patterns": [
            r'(/api)?/.*data.*export',
            r'(/api)?/.*user.*data',
            r'(/api)?/.*profile.*download',
            r'def\s+export_user_data',
            r'function\s+exportUserData',
            r'getUserData|getMyData',
        ]
    },
    "right_to_portability": {
        "description": "Right to data portability (Article 20)",
        "patterns": [
            r'(/api)?/.*export',
            r'(/api)?/.*download.*data',
            r'\.json|\.csv|\.xml.*export',
            r'format\s*=\s*[\'\"](json|csv|xml)',
        ]
    },
    "right_to_erasure": {
        "description": "Right to erasure/deletion (Article 17)",
        "patterns": [
            r'(/api)?/.*delete.*account',
            r'(/api)?/.*user.*delete',
            r'def\s+delete_user',
            r'function\s+deleteUser',
            r'deleteAccount|removeUser',
            r'GDPR.*delete|erasure',
        ]
    },
    "right_to_rectification": {
        "description": "Right to rectification (Article 16)",
        "patterns": [
            r'(/api)?/.*user.*update',
            r'(/api)?/.*profile.*edit',
            r'def\s+update_user',
            r'function\s+updateUser',
            r'PUT.*user|PATCH.*user',
        ]
    },
    "right_to_object": {
        "description": "Right to object to processing (Article 21)",
        "patterns": [
            r'(/api)?/.*opt.*out',
            r'(/api)?/.*unsubscribe',
            r'(/api)?/.*consent.*withdraw',
            r'marketing.*preferences',
            r'optOut|withdrawConsent',
        ]
    },
    "consent_management": {
        "description": "Consent management (Article 7)",
        "patterns": [
            r'(/api)?/.*consent',
            r'cookie.*consent|consent.*cookie',
            r'def\s+update_consent',
            r'function\s+updateConsent',
            r'acceptCookies|manageCookies',
        ]
    }
}

def check_file_for_dsr(file_path: Path) -> Dict[str, Any]:
    """Check a single file for DSR implementations."""
    findings = {
        "file": str(file_path),
        "implementations": []
    }

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

            for right, info in DSR_REQUIREMENTS.items():
                for pattern in info["patterns"]:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            findings["implementations"].append({
                                "right": right,
                                "description": info["description"],
                                "line": line_num,
                                "matched_pattern": pattern,
                                "context": line.strip()
                            })
    except Exception as e:
        findings["error"] = str(e)

    return findings if findings["implementations"] else None

def scan_directory(directory: str) -> Dict[str, Any]:
    """Scan directory for DSR implementations."""
    extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cs', '.rb', '.go', '.php']
    all_findings = []
    root_path = Path(directory)

    for ext in extensions:
        for file_path in root_path.rglob(f'*{ext}'):
            # Skip common directories
            if any(part in file_path.parts for part in ['node_modules', 'venv', '.git', 'dist', 'build']):
                continue

            findings = check_file_for_dsr(file_path)
            if findings:
                all_findings.append(findings)

    return analyze_dsr_coverage(all_findings)

def analyze_dsr_coverage(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze DSR implementation coverage."""
    coverage = {right: False for right in DSR_REQUIREMENTS.keys()}

    for file_findings in findings:
        for impl in file_findings.get("implementations", []):
            coverage[impl["right"]] = True

    missing_rights = [right for right, implemented in coverage.items() if not implemented]

    return {
        "findings": findings,
        "coverage": coverage,
        "missing_rights": missing_rights,
        "compliance_percentage": (len([v for v in coverage.values() if v]) / len(coverage)) * 100,
        "summary": {
            "total_files_with_dsr": len(findings),
            "total_dsr_implementations": sum(len(f["implementations"]) for f in findings),
            "implemented_rights": [right for right, implemented in coverage.items() if implemented],
            "missing_rights": [
                {
                    "right": right,
                    "description": DSR_REQUIREMENTS[right]["description"],
                    "risk": "High - Required by GDPR"
                }
                for right in missing_rights
            ]
        }
    }

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python check_dsr_implementation.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"Checking {directory} for GDPR Data Subject Rights implementations...")
    results = scan_directory(directory)

    print(json.dumps(results, indent=2))

    # Summary
    print(f"\n{'='*60}")
    print("GDPR Data Subject Rights Implementation Summary")
    print(f"{'='*60}")
    print(f"Compliance: {results['compliance_percentage']:.1f}%")
    print(f"\nImplemented Rights ({len(results['summary']['implemented_rights'])}):")
    for right in results['summary']['implemented_rights']:
        print(f"  ✓ {right}: {DSR_REQUIREMENTS[right]['description']}")

    if results['summary']['missing_rights']:
        print(f"\nMissing Rights ({len(results['summary']['missing_rights'])}):")
        for missing in results['summary']['missing_rights']:
            print(f"  ✗ {missing['right']}: {missing['description']}")
            print(f"    Risk: {missing['risk']}")

if __name__ == "__main__":
    main()
