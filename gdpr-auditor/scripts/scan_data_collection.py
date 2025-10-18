#!/usr/bin/env python3
"""
GDPR Data Collection Scanner - Static File Analysis Tool

Scans source code files for data collection patterns including forms, inputs,
API endpoint definitions, cookies, local storage, and analytics tracking.

IMPORTANT - STATIC ANALYSIS ONLY:
This script analyzes static source code files. It does NOT:
- Connect to running applications or live systems
- Execute code or simulate user interactions
- Make network requests or API calls
- Access live databases or servers
- Monitor runtime behavior
- Require system credentials or access

Analyzes: Source code files (.py, .js, .tsx, .html, .php, .java, etc.)
Purpose: Identify data collection points in code for GDPR compliance review
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Patterns that indicate data collection
DATA_COLLECTION_PATTERNS = {
    "form_fields": [
        r'<input[^>]*name=[\"\']([^\"\']+)[\"\']',
        r'<textarea[^>]*name=[\"\']([^\"\']+)[\"\']',
        r'<select[^>]*name=[\"\']([^\"\']+)[\"\']',
        r'formData\.append\([\'"]([^\'"]+)[\'"]',
        r'\.name\s*=\s*[\'"]([^\'"]+)[\'"]',
    ],
    "email_collection": [
        r'type=[\"\']email[\"\']',
        r'email\s*[:=]',
        r'@mail|mailto:',
    ],
    "personal_data_fields": [
        r'\b(email|phone|address|name|firstname|lastname|birthday|ssn|passport|license)\b',
        r'\b(dob|birth_date|social_security|credit_card|card_number)\b',
    ],
    "cookies": [
        r'document\.cookie',
        r'setCookie',
        r'getCookie',
        r'Cookies\.set',
    ],
    "local_storage": [
        r'localStorage\.setItem',
        r'sessionStorage\.setItem',
    ],
    "analytics": [
        r'google-analytics|ga\(',
        r'gtag\(',
        r'fbq\(',
        r'_paq\.push',
        r'mixpanel',
    ],
    "api_endpoints": [
        r'@app\.route\([\'"]([^\'"]+)',
        r'router\.(get|post|put|patch|delete)\([\'"]([^\'"]+)',
        r'app\.(get|post|put|patch|delete)\([\'"]([^\'"]+)',
    ],
}

def scan_file(file_path: Path) -> Dict[str, Any]:
    """Scan a single file for data collection patterns."""
    findings = {
        "file": str(file_path),
        "issues": []
    }

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

            for category, patterns in DATA_COLLECTION_PATTERNS.items():
                for pattern in patterns:
                    for line_num, line in enumerate(lines, 1):
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            findings["issues"].append({
                                "category": category,
                                "line": line_num,
                                "pattern": pattern,
                                "matched_text": match.group(0),
                                "context": line.strip()
                            })
    except Exception as e:
        findings["error"] = str(e)

    return findings if findings["issues"] else None

def scan_directory(directory: str, extensions: List[str] = None) -> List[Dict[str, Any]]:
    """Scan directory for data collection patterns."""
    if extensions is None:
        extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.php', '.java', '.cs', '.rb', '.go']

    all_findings = []
    root_path = Path(directory)

    for ext in extensions:
        for file_path in root_path.rglob(f'*{ext}'):
            # Skip common directories to ignore
            if any(part in file_path.parts for part in ['node_modules', 'venv', '.git', 'dist', 'build']):
                continue

            findings = scan_file(file_path)
            if findings:
                all_findings.append(findings)

    return all_findings

def main():
    """Main entry point for the scanner."""
    if len(sys.argv) < 2:
        print("Usage: python scan_data_collection.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"Scanning {directory} for data collection patterns...")
    findings = scan_directory(directory)

    print(f"\nFound {len(findings)} files with data collection patterns\n")
    print(json.dumps(findings, indent=2))

    # Summary
    total_issues = sum(len(f["issues"]) for f in findings)
    print(f"\n{'='*60}")
    print(f"Summary: {total_issues} potential data collection points found in {len(findings)} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
