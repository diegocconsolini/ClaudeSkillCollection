#!/usr/bin/env python3
"""
GDPR Security Audit Script - Static File Analysis Tool

Scans source code and configuration files for common security patterns and issues
that affect GDPR compliance (encryption, authentication, access control, audit logging).

IMPORTANT - STATIC ANALYSIS ONLY:
This script analyzes static code and configuration files. It does NOT:
- Perform penetration testing or vulnerability exploitation
- Connect to running systems or production environments
- Test actual security controls or authentication
- Execute code or simulate attacks
- Access live servers, databases, or networks
- Require system credentials or elevated privileges
- Monitor runtime security behavior

Analyzes: Source code, configuration files, security-related code patterns
Purpose: Identify security implementation patterns in code for GDPR Article 32 compliance
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Security patterns to check
SECURITY_CHECKS = {
    "encryption_at_rest": {
        "description": "Encryption of personal data at rest",
        "positive_patterns": [
            r'encrypt|aes|cipher',
            r'@Encrypted|@Column.*encrypted',
            r'bcrypt|scrypt|argon2',
        ],
        "negative_patterns": [
            r'password\s*=\s*[\'"][^\'"]+[\'"]',  # Hardcoded passwords
            r'MD5|SHA1(?!0)',  # Weak hashing
        ]
    },
    "encryption_in_transit": {
        "description": "Encryption in transit (HTTPS/TLS)",
        "positive_patterns": [
            r'https://',
            r'ssl|tls',
            r'secure\s*=\s*True',
        ],
        "negative_patterns": [
            r'http://(?!localhost|127\.0\.0\.1)',  # HTTP in production
            r'verify\s*=\s*False',  # SSL verification disabled
        ]
    },
    "access_control": {
        "description": "Access control and authorization",
        "positive_patterns": [
            r'@RequiresAuthentication|@Authorize',
            r'authenticate|authorize|checkPermission',
            r'if.*is_authenticated|if.*has_permission',
            r'protect|guard|middleware.*auth',
        ],
        "negative_patterns": []
    },
    "audit_logging": {
        "description": "Audit logging for personal data access",
        "positive_patterns": [
            r'logger\.|log\.',
            r'audit|logging',
            r'track.*access|record.*access',
        ],
        "negative_patterns": []
    },
    "input_validation": {
        "description": "Input validation and sanitization",
        "positive_patterns": [
            r'validate|sanitize|escape',
            r'@Valid|@NotNull|@Size',
            r'strip_tags|filter|clean',
        ],
        "negative_patterns": [
            r'eval\(|exec\(',  # Dangerous execution
            r'dangerouslySetInnerHTML',  # XSS risk
        ]
    },
    "password_handling": {
        "description": "Secure password handling",
        "positive_patterns": [
            r'bcrypt|scrypt|argon2|pbkdf2',
            r'password_hash|hashPassword',
        ],
        "negative_patterns": [
            r'password\s*=\s*[\'"][^\'"]+[\'"]',  # Hardcoded passwords
            r'\.password(?!\s*=\s*hash)',  # Plain text password storage
        ]
    },
    "sql_injection": {
        "description": "SQL injection protection",
        "positive_patterns": [
            r'parameterized|prepared.*statement',
            r'\.execute\([^+]*\?',  # Parameterized queries
            r'ORM|SQLAlchemy|Hibernate|Entity',
        ],
        "negative_patterns": [
            r'execute\([^)]*\+[^)]*\)',  # String concatenation in SQL
            r'f[\'"].*SELECT.*\{',  # F-string in SQL
        ]
    },
    "api_authentication": {
        "description": "API authentication and key management",
        "positive_patterns": [
            r'Bearer.*token',
            r'Authorization.*header',
            r'api_key.*env|os\.getenv',
        ],
        "negative_patterns": [
            r'api_key\s*=\s*[\'"][a-zA-Z0-9]{20,}[\'"]',  # Hardcoded API keys
            r'token\s*=\s*[\'"][a-zA-Z0-9]{20,}[\'"]',
        ]
    }
}

def check_file_security(file_path: Path) -> Dict[str, Any]:
    """Check a single file for security issues."""
    findings = {
        "file": str(file_path),
        "issues": [],
        "good_practices": []
    }

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

            for check_name, check_info in SECURITY_CHECKS.items():
                # Check for positive patterns (good practices)
                for pattern in check_info["positive_patterns"]:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            findings["good_practices"].append({
                                "check": check_name,
                                "description": check_info["description"],
                                "line": line_num,
                                "context": line.strip()[:100]
                            })

                # Check for negative patterns (issues)
                for pattern in check_info["negative_patterns"]:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            findings["issues"].append({
                                "check": check_name,
                                "description": check_info["description"],
                                "severity": "High",
                                "line": line_num,
                                "issue": pattern,
                                "context": line.strip()[:100],
                                "gdpr_impact": "May violate Article 32 (Security of processing)"
                            })
    except Exception as e:
        findings["error"] = str(e)

    return findings if (findings["issues"] or findings["good_practices"]) else None

def scan_directory(directory: str) -> Dict[str, Any]:
    """Scan directory for security issues."""
    extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cs', '.rb', '.go', '.php', '.sql']
    all_findings = []
    root_path = Path(directory)

    for ext in extensions:
        for file_path in root_path.rglob(f'*{ext}'):
            # Skip common directories
            if any(part in file_path.parts for part in ['node_modules', 'venv', '.git', 'dist', 'build', 'test']):
                continue

            findings = check_file_security(file_path)
            if findings:
                all_findings.append(findings)

    return analyze_security(all_findings)

def analyze_security(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze security findings."""
    total_issues = sum(len(f.get("issues", [])) for f in findings)
    total_good_practices = sum(len(f.get("good_practices", [])) for f in findings)

    # Count issues by category
    issues_by_category = {}
    for f in findings:
        for issue in f.get("issues", []):
            category = issue["check"]
            if category not in issues_by_category:
                issues_by_category[category] = 0
            issues_by_category[category] += 1

    # Identify high-risk areas
    high_risk_files = [
        f for f in findings
        if len(f.get("issues", [])) > 3
    ]

    return {
        "findings": findings,
        "summary": {
            "total_files_scanned": len(findings),
            "total_security_issues": total_issues,
            "total_good_practices": total_good_practices,
            "issues_by_category": issues_by_category,
            "high_risk_files": len(high_risk_files),
            "critical_issues": [
                f for f in findings
                if any(issue.get("severity") == "High" for issue in f.get("issues", []))
            ]
        }
    }

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python security_audit.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"Running GDPR security audit on {directory}...")
    results = scan_directory(directory)

    print(json.dumps(results, indent=2))

    # Summary
    print(f"\n{'='*60}")
    print("GDPR Security Audit Summary")
    print(f"{'='*60}")
    print(f"Files scanned: {results['summary']['total_files_scanned']}")
    print(f"Security issues found: {results['summary']['total_security_issues']}")
    print(f"Good practices found: {results['summary']['total_good_practices']}")
    print(f"High-risk files: {results['summary']['high_risk_files']}")

    if results['summary']['issues_by_category']:
        print(f"\nIssues by category:")
        for category, count in results['summary']['issues_by_category'].items():
            print(f"  - {category}: {count}")

if __name__ == "__main__":
    main()
