#!/usr/bin/env python3
"""
Integrated Security Scanner with STIX 2.1 Threat Intelligence
Combines pattern detection with ATT&CK + ATLAS + OWASP enrichment

Features:
- 70+ dangerous code patterns
- MITRE ATT&CK + ATLAS threat intelligence
- OWASP API Security Top 10 + Top 10 Web mapping
- CWE + CVE references
- STIX 2.1 bundle generation
- Threat actor attribution
- Mitigation recommendations

Version: 2.0.0
"""

import json
import re
import os
import sys
import ast
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from stix_manager import STIXManager
    from stix_builder import STIXBuilder
    STIX_AVAILABLE = True
except ImportError:
    print("WARNING: STIX modules not available. Run from scripts/ directory.")
    STIX_AVAILABLE = False


class IntegratedScanner:
    """
    Production security scanner with full threat intelligence integration.
    """

    def __init__(self, enable_stix: bool = True):
        """Initialize scanner with STIX enrichment."""
        self.script_dir = Path(__file__).parent
        self.root_dir = self.script_dir.parent

        # Load pattern databases
        self.patterns = self._load_patterns()
        self.threat_mappings = self._load_threat_mappings()

        # Initialize STIX (if available)
        self.stix_enabled = enable_stix and STIX_AVAILABLE
        if self.stix_enabled:
            self.stix_manager = STIXManager()
            self.stix_builder = STIXBuilder()

            # Load ATT&CK and ATLAS data
            print("Loading MITRE threat intelligence...")
            self.stix_manager.load_attack_data("enterprise")
            self.stix_manager.load_attack_data("atlas")
            print(f"✓ Loaded ATT&CK ({len(self.stix_manager.get_all_techniques('enterprise'))} techniques)")
            print(f"✓ Loaded ATLAS ({len(self.stix_manager.get_all_techniques('atlas'))} AI/ML techniques)")
        else:
            self.stix_manager = None
            self.stix_builder = None

        # Statistics
        self.stats = {
            "files_scanned": 0,
            "findings": 0,
            "by_severity": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        }

    def _load_patterns(self) -> Dict:
        """Load expanded dangerous functions database."""
        patterns_file = self.root_dir / "references" / "dangerous_functions_expanded.json"
        if not patterns_file.exists():
            # Fall back to original
            patterns_file = self.root_dir / "references" / "dangerous_functions.json"

        with open(patterns_file, 'r') as f:
            return json.load(f)

    def _load_threat_mappings(self) -> Dict:
        """Load threat intelligence mappings."""
        mappings_file = self.root_dir / "references" / "threat_mappings.json"
        if not mappings_file.exists():
            return {"mappings": {}}

        with open(mappings_file, 'r') as f:
            return json.load(f)

    def scan_file(self, file_path: Path, language: str) -> List[Dict]:
        """
        Scan a single file for security issues.

        Args:
            file_path: Path to file to scan
            language: 'python' or 'javascript'

        Returns:
            List of findings with STIX enrichment
        """
        findings = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return [{
                "file": str(file_path),
                "category": "Scan Error",
                "severity": "INFO",
                "description": f"Could not read file: {e}"
            }]

        # Get patterns for this language
        lang_patterns = self.patterns.get(language, {})

        # Scan for dangerous functions
        for severity_level in ["critical", "high", "medium", "low"]:
            patterns_at_level = lang_patterns.get(severity_level, {})

            for func_name, func_info in patterns_at_level.items():
                pattern = func_info.get("detection_pattern")
                if not pattern:
                    continue

                # Search for pattern
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)

                for match in matches:
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1

                    # Create base finding
                    finding = {
                        "file": str(file_path),
                        "line": line_num,
                        "category": "Dangerous Function",
                        "severity": func_info.get("severity", "MEDIUM"),
                        "function": func_name,
                        "description": func_info.get("description", ""),
                        "code_snippet": match.group(0),
                        "risk": func_info.get("risk", ""),
                        "safe_alternative": func_info.get("safe_alternative", ""),
                        "cvss": func_info.get("cvss", 0.0)
                    }

                    # Enrich with STIX if available
                    if self.stix_enabled:
                        finding = self._enrich_with_stix(finding, func_name, func_info)

                    findings.append(finding)
                    self.stats["findings"] += 1
                    self.stats["by_severity"][finding["severity"]] += 1

        # Scan for obfuscation
        obfuscation_findings = self._scan_obfuscation(file_path, content, language)
        findings.extend(obfuscation_findings)

        # Scan for credentials
        credential_findings = self._scan_credentials(file_path, content)
        findings.extend(credential_findings)

        self.stats["files_scanned"] += 1
        return findings

    def _enrich_with_stix(self, finding: Dict, func_name: str, func_info: Dict) -> Dict:
        """
        Enrich finding with MITRE ATT&CK + ATLAS threat intelligence.

        Adds:
        - ATT&CK technique details
        - ATLAS technique details (if AI/ML related)
        - Threat actor attribution
        - Mitigations
        - CWE/CVE references
        - OWASP mappings
        """
        # Get ATT&CK technique ID from func_info or mappings
        attack_id = func_info.get("attack_id")
        atlas_id = func_info.get("atlas_id")

        if not attack_id:
            # Try to find in threat_mappings
            mapping_key = func_name.replace(".", "_")
            mapping = self.threat_mappings.get("mappings", {}).get(mapping_key)
            if mapping:
                if "attack" in mapping:
                    attack_id = mapping["attack"]["technique_id"]
                if "atlas" in mapping and mapping["atlas"]:
                    atlas_id = mapping["atlas"]["technique_id"]

        # Enrich with ATT&CK
        if attack_id and self.stix_manager:
            attack_pattern = self.stix_manager.get_attack_pattern(attack_id, "enterprise")
            if attack_pattern:
                finding["attack"] = {
                    "id": attack_id,
                    "name": attack_pattern.get("name"),
                    "tactic": attack_pattern.get("x_mitre_tactics", ["Unknown"])[0] if attack_pattern.get("x_mitre_tactics") else "Unknown",
                    "description": attack_pattern.get("description", "")[:200] + "...",
                    "url": f"https://attack.mitre.org/techniques/{attack_id}"
                }

                # Get threat actors
                groups = self.stix_manager.get_intrusion_sets_using_technique(attack_id, "enterprise")
                if groups:
                    finding["threat_actors"] = [g.get("name") for g in groups[:5]]  # Top 5

                # Get mitigations
                mitigations = self.stix_manager.get_mitigations(attack_id, "enterprise")
                if mitigations:
                    finding["mitigations"] = [
                        {
                            "name": m.get("name"),
                            "description": m.get("description", "")[:150] + "..."
                        }
                        for m in mitigations[:3]  # Top 3
                    ]

        # Enrich with ATLAS (AI/ML)
        if atlas_id and self.stix_manager:
            atlas_pattern = self.stix_manager.get_attack_pattern(atlas_id, "atlas")
            if atlas_pattern:
                finding["atlas"] = {
                    "id": atlas_id,
                    "name": atlas_pattern.get("name"),
                    "description": atlas_pattern.get("description", "")[:200] + "...",
                    "url": f"https://atlas.mitre.org/techniques/{atlas_id}"
                }

        # Add CWE/CVE/OWASP from func_info
        if "cwe" in func_info:
            finding["cwe"] = func_info["cwe"]

        if "cve_reference" in func_info:
            finding["cve"] = func_info["cve_reference"]

        if "owasp_api" in func_info:
            finding["owasp_api"] = func_info["owasp_api"]

        return finding

    def _scan_obfuscation(self, file_path: Path, content: str, language: str) -> List[Dict]:
        """Scan for obfuscation patterns."""
        findings = []

        obfuscation_patterns = self.patterns.get("obfuscation", {})

        for category, patterns in obfuscation_patterns.items():
            for pattern_name, pattern_info in patterns.items():
                # Skip if wrong language
                if isinstance(pattern_info, dict):
                    pattern = pattern_info.get("detection_pattern")
                    if not pattern:
                        continue

                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1

                        finding = {
                            "file": str(file_path),
                            "line": line_num,
                            "category": "Obfuscation",
                            "severity": pattern_info.get("severity", "MEDIUM"),
                            "pattern": pattern_name,
                            "description": pattern_info.get("description", ""),
                            "code_snippet": match.group(0)[:100],
                            "cvss": pattern_info.get("cvss", 5.0)
                        }

                        # Add ATT&CK for obfuscation (T1027)
                        if self.stix_enabled:
                            attack_pattern = self.stix_manager.get_attack_pattern("T1027", "enterprise")
                            if attack_pattern:
                                finding["attack"] = {
                                    "id": "T1027",
                                    "name": attack_pattern.get("name"),
                                    "tactic": "Defense Evasion"
                                }

                        findings.append(finding)
                        self.stats["findings"] += 1
                        self.stats["by_severity"][finding["severity"]] += 1

        return findings

    def _scan_credentials(self, file_path: Path, content: str) -> List[Dict]:
        """Scan for hardcoded credentials."""
        findings = []

        credential_patterns = self.patterns.get("credentials", {}).get("api_keys", {})

        for key_type, key_info in credential_patterns.items():
            pattern = key_info.get("detection_pattern")
            if not pattern:
                continue

            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1

                finding = {
                    "file": str(file_path),
                    "line": line_num,
                    "category": "Credential Exposure",
                    "severity": key_info.get("severity", "HIGH"),
                    "credential_type": key_type,
                    "description": key_info.get("description", ""),
                    "code_snippet": match.group(0)[:20] + "...",  # Redact
                    "cvss": key_info.get("cvss", 8.0)
                }

                # Add ATT&CK for credentials (T1552.001)
                if self.stix_enabled:
                    finding["attack"] = {
                        "id": "T1552.001",
                        "name": "Unsecured Credentials: Credentials In Files",
                        "tactic": "Credential Access"
                    }

                    finding["cwe"] = "CWE-798"
                    finding["owasp"] = "A02:2021 - Cryptographic Failures"

                findings.append(finding)
                self.stats["findings"] += 1
                self.stats["by_severity"][finding["severity"]] += 1

        return findings

    def generate_stix_bundle(self, findings: List[Dict], plugin_name: str) -> Optional[Dict]:
        """
        Generate STIX 2.1 bundle from scan findings.

        Args:
            findings: List of scan findings
            plugin_name: Name of scanned plugin

        Returns:
            STIX bundle dict or None if STIX not available
        """
        if not self.stix_enabled or not self.stix_builder:
            return None

        # Create scan result summary
        scan_result = {
            "plugin_name": plugin_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "findings_count": len(findings),
            "severity_distribution": self.stats["by_severity"],
            "findings": findings
        }

        # Generate STIX bundle
        try:
            bundle = self.stix_builder.create_bundle_from_scan(scan_result)
            return json.loads(bundle.serialize())
        except Exception as e:
            print(f"WARNING: Could not generate STIX bundle: {e}")
            return None

    def calculate_risk_score(self, findings: List[Dict]) -> Dict:
        """
        Calculate security risk score (FIXED - excludes code quality).

        Only security findings count toward risk:
        - Dangerous Functions
        - Obfuscation
        - Credential Exposure
        - Malicious Behavior

        Code Quality findings = INFO severity (0 points)
        """
        severity_weights = {
            "CRITICAL": 100,
            "HIGH": 75,
            "MEDIUM": 50,
            "LOW": 25,
            "INFO": 0  # Code quality doesn't count as security risk
        }

        total_score = 0
        security_findings = []

        for finding in findings:
            category = finding.get("category", "")

            # Only count security categories
            if category in ["Dangerous Function", "Obfuscation", "Credential Exposure", "Malicious Behavior"]:
                severity = finding.get("severity", "INFO")
                total_score += severity_weights.get(severity, 0)
                security_findings.append(finding)

        # Determine risk level
        if total_score >= 200:
            risk_level = "CRITICAL"
        elif total_score >= 100:
            risk_level = "HIGH"
        elif total_score >= 50:
            risk_level = "MEDIUM"
        elif total_score > 0:
            risk_level = "LOW"
        else:
            risk_level = "NONE"

        return {
            "risk_score": total_score,
            "risk_level": risk_level,
            "security_findings": len(security_findings),
            "total_findings": len(findings)
        }

    def print_report(self, findings: List[Dict], plugin_name: str):
        """Print human-readable security report."""
        print(f"\n{'='*80}")
        print(f" Security Scan Report: {plugin_name}")
        print(f"{'='*80}\n")

        # Calculate risk
        risk = self.calculate_risk_score(findings)

        print(f"Risk Score: {risk['risk_score']} ({risk['risk_level']})")
        print(f"Security Findings: {risk['security_findings']}")
        print(f"Total Findings: {risk['total_findings']}\n")

        # Severity distribution
        print("Severity Distribution:")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            count = sum(1 for f in findings if f.get("severity") == severity)
            if count > 0:
                print(f"  {severity}: {count}")

        print(f"\n{'='*80}\n")

        # Detailed findings
        for i, finding in enumerate(findings, 1):
            print(f"[{i}] {finding['severity']} - {finding['category']}")
            print(f"    File: {finding['file']}:{finding.get('line', '?')}")
            print(f"    {finding['description']}")

            # ATT&CK info
            if "attack" in finding:
                attack = finding["attack"]
                print(f"    ATT&CK: {attack['id']} - {attack['name']} ({attack.get('tactic', 'Unknown')})")

            # ATLAS info (AI/ML)
            if "atlas" in finding:
                atlas = finding["atlas"]
                print(f"    ATLAS: {atlas['id']} - {atlas['name']} (AI/ML Threat)")

            # CWE/CVE
            if "cwe" in finding:
                print(f"    CWE: {finding['cwe']}")
            if "cve" in finding:
                print(f"    CVE: {finding['cve']}")

            # OWASP
            if "owasp_api" in finding:
                print(f"    OWASP API: {finding['owasp_api']}")

            # Threat actors
            if "threat_actors" in finding:
                print(f"    Known Threat Actors: {', '.join(finding['threat_actors'][:3])}")

            print()


def main():
    """Test integrated scanner."""
    import argparse

    parser = argparse.ArgumentParser(description="Integrated Security Scanner with STIX enrichment")
    parser.add_argument("plugin_path", help="Path to plugin directory or file")
    parser.add_argument("--no-stix", action="store_true", help="Disable STIX enrichment")
    parser.add_argument("--output-stix", help="Output STIX bundle to file")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Initialize scanner
    scanner = IntegratedScanner(enable_stix=not args.no_stix)

    # Scan plugin
    plugin_path = Path(args.plugin_path)
    all_findings = []

    if plugin_path.is_file():
        # Single file
        language = "python" if plugin_path.suffix == ".py" else "javascript"
        findings = scanner.scan_file(plugin_path, language)
        all_findings.extend(findings)
    elif plugin_path.is_dir():
        # Directory
        for py_file in plugin_path.rglob("*.py"):
            findings = scanner.scan_file(py_file, "python")
            all_findings.extend(findings)

        for js_file in plugin_path.rglob("*.js"):
            findings = scanner.scan_file(js_file, "javascript")
            all_findings.extend(findings)

    # Print report
    if args.format == "text":
        scanner.print_report(all_findings, plugin_path.name)
    elif args.format == "json":
        risk = scanner.calculate_risk_score(all_findings)
        output = {
            "plugin": plugin_path.name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "risk": risk,
            "findings": all_findings,
            "statistics": scanner.stats
        }
        print(json.dumps(output, indent=2))

    # Generate STIX bundle if requested
    if args.output_stix:
        bundle = scanner.generate_stix_bundle(all_findings, plugin_path.name)
        if bundle:
            with open(args.output_stix, 'w') as f:
                json.dump(bundle, f, indent=2)
            print(f"\n✓ STIX bundle saved to {args.output_stix}")

    return 0 if scanner.stats["by_severity"]["CRITICAL"] == 0 else 1


if __name__ == "__main__":
    exit(main())
