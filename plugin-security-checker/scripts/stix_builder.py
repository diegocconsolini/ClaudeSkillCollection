#!/usr/bin/env python3
"""
STIX 2.1 Object Builder for Plugin Security Scanner

This module creates STIX 2.1 objects and bundles from scan results,
enabling standardized threat intelligence sharing and integration
with SIEM/SOAR platforms.

STIX Objects Created:
- Indicator: Detection patterns for vulnerable code
- Malware: Malicious plugins (if confirmed)
- Tool: Security scanner itself
- Identity: Plugin author, scanner operator
- Vulnerability: CVE/CWE references
- Attack Pattern: MITRE ATT&CK techniques
- Relationship: Links between objects (uses, mitigates, indicates)
- Sighting: Observed instances of vulnerabilities

Usage:
    from scripts.stix_builder import STIXBuilder

    # Initialize builder
    builder = STIXBuilder(
        scanner_name="Plugin Security Checker",
        scanner_version="2.0.0"
    )

    # Create indicator from scan finding
    indicator = builder.create_indicator_from_finding(finding)

    # Create vulnerability object
    vuln = builder.create_vulnerability(
        cve_id="CVE-2025-54795",
        description="Command Injection via subprocess",
        cvss_score=8.7
    )

    # Build complete STIX bundle from scan
    bundle = builder.create_bundle_from_scan(scan_result)

    # Export to JSON
    bundle_json = bundle.serialize(pretty=True)

Dependencies:
    - stix2>=3.0.1
    - Python 3.8+

Author: Plugin Security Checker Team
Version: 2.0.0
License: MIT
"""

import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import stix2
    STIX2_AVAILABLE = True
except ImportError:
    STIX2_AVAILABLE = False
    print("WARNING: stix2 library not available. Run: pip3 install -r requirements.txt")


class STIXBuilder:
    """
    Builder for creating STIX 2.1 objects from plugin scan results.
    """

    def __init__(self, scanner_name: str = "Plugin Security Checker",
                 scanner_version: str = "2.0.0",
                 operator_name: str = "Security Team"):
        """
        Initialize STIX Builder.

        Args:
            scanner_name: Name of the security scanner
            scanner_version: Version of the scanner
            operator_name: Name of the organization/person running scans
        """
        if not STIX2_AVAILABLE:
            raise ImportError("stix2 library not available. Run: pip3 install -r requirements.txt")

        self.scanner_name = scanner_name
        self.scanner_version = scanner_version
        self.operator_name = operator_name

        # Create Identity objects
        self.scanner_identity = self._create_scanner_identity()
        self.operator_identity = self._create_operator_identity()

        # Create Tool object for scanner
        self.scanner_tool = self._create_scanner_tool()

        # Cache for created objects
        self.cache = {
            "identities": {},
            "vulnerabilities": {},
            "attack_patterns": {},
            "indicators": {}
        }

    def _create_scanner_identity(self) -> 'stix2.Identity':
        """Create STIX Identity for the scanner tool."""
        return stix2.Identity(
            id=f"identity--{uuid.uuid5(uuid.NAMESPACE_DNS, self.scanner_name)}",
            name=self.scanner_name,
            identity_class="system",
            description=f"Automated security scanner for Claude Code plugins (v{self.scanner_version})",
            created=datetime.now(timezone.utc)
        )

    def _create_operator_identity(self) -> 'stix2.Identity':
        """Create STIX Identity for the scanner operator."""
        return stix2.Identity(
            id=f"identity--{uuid.uuid5(uuid.NAMESPACE_DNS, self.operator_name)}",
            name=self.operator_name,
            identity_class="organization",
            description="Security team operating the plugin security scanner",
            created=datetime.now(timezone.utc)
        )

    def _create_scanner_tool(self) -> 'stix2.Tool':
        """Create STIX Tool object for the scanner."""
        return stix2.Tool(
            id=f"tool--{uuid.uuid5(uuid.NAMESPACE_DNS, f'{self.scanner_name}-{self.scanner_version}')}",
            name=self.scanner_name,
            description="Security scanner for Claude Code plugins and skills. Detects dangerous code patterns, credential leaks, obfuscation, and malicious behavior.",
            tool_types=["static-analysis"],
            tool_version=self.scanner_version,
            created_by_ref=self.scanner_identity.id
        )

    def create_indicator_from_finding(self, finding: Dict) -> 'stix2.Indicator':
        """
        Create STIX Indicator from a scan finding.

        Args:
            finding: Scan finding dict with severity, file, line, description

        Returns:
            STIX Indicator object
        """
        # Build indicator pattern
        pattern = self._build_indicator_pattern(finding)

        # Determine indicator types
        indicator_types = self._determine_indicator_types(finding)

        # Build name
        name = f"{finding.get('category', 'Unknown')}: {finding.get('description', 'Security Issue')}"

        # Create indicator
        indicator = stix2.Indicator(
            name=name,
            description=finding.get("description", ""),
            pattern=pattern,
            pattern_type="stix",
            indicator_types=indicator_types,
            valid_from=datetime.now(timezone.utc),
            created_by_ref=self.scanner_identity.id,
            object_marking_refs=[stix2.TLP_WHITE.id],
            custom_properties={
                "x_severity": finding.get("severity", "UNKNOWN"),
                "x_category": finding.get("category", "Unknown"),
                "x_file": finding.get("file", ""),
                "x_line": finding.get("line", 0),
                "x_cvss_score": finding.get("cvss_score", 0.0)
            }
        )

        return indicator

    def _build_indicator_pattern(self, finding: Dict) -> str:
        """
        Build STIX pattern from finding.

        STIX patterns use a simple expression language.
        For code patterns, we use file objects.
        """
        file_path = finding.get("file", "unknown.py")
        code_snippet = finding.get("code_snippet", "")

        # Build STIX pattern
        if code_snippet:
            # Escape quotes in code snippet
            escaped_code = code_snippet.replace("'", "\\'")
            pattern = f"[file:name = '{file_path}' AND file:content_ref.payload_bin MATCHES '{escaped_code}']"
        else:
            pattern = f"[file:name = '{file_path}']"

        return pattern

    def _determine_indicator_types(self, finding: Dict) -> List[str]:
        """Determine STIX indicator types from finding."""
        category = finding.get("category", "").lower()

        # Map categories to STIX indicator types
        type_mapping = {
            "dangerous function": ["malicious-code"],
            "credential exposure": ["credential-leak"],
            "obfuscation": ["malicious-code"],
            "code quality": ["anomalous-activity"],
            "network request": ["anomalous-activity"],
            "malicious behavior": ["malicious-code"]
        }

        return type_mapping.get(category, ["unknown"])

    def create_vulnerability(self, cve_id: Optional[str] = None,
                           cwe_id: Optional[str] = None,
                           description: str = "",
                           cvss_score: float = 0.0) -> 'stix2.Vulnerability':
        """
        Create STIX Vulnerability object.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2025-54795")
            cwe_id: CWE identifier (e.g., "CWE-78")
            description: Vulnerability description
            cvss_score: CVSS v3 base score

        Returns:
            STIX Vulnerability object
        """
        # Use CVE as name if available, otherwise CWE
        name = cve_id or cwe_id or "Unknown Vulnerability"

        # Build external references
        external_refs = []
        if cve_id:
            external_refs.append(stix2.ExternalReference(
                source_name="cve",
                external_id=cve_id,
                url=f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            ))
        if cwe_id:
            external_refs.append(stix2.ExternalReference(
                source_name="cwe",
                external_id=cwe_id,
                url=f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-', '')}.html"
            ))

        # Create vulnerability
        vuln = stix2.Vulnerability(
            name=name,
            description=description,
            external_references=external_refs if external_refs else None,
            created_by_ref=self.scanner_identity.id,
            custom_properties={
                "x_cvss_score": cvss_score
            }
        )

        # Cache it
        if cve_id:
            self.cache["vulnerabilities"][cve_id] = vuln

        return vuln

    def create_attack_pattern(self, technique_id: str, name: str,
                             description: str = "") -> 'stix2.AttackPattern':
        """
        Create STIX Attack Pattern (MITRE ATT&CK technique).

        Args:
            technique_id: ATT&CK technique ID (e.g., "T1059.006")
            name: Technique name (e.g., "Python")
            description: Technique description

        Returns:
            STIX Attack Pattern object
        """
        # Check cache
        if technique_id in self.cache["attack_patterns"]:
            return self.cache["attack_patterns"][technique_id]

        # Build external reference to ATT&CK
        external_ref = stix2.ExternalReference(
            source_name="mitre-attack",
            external_id=technique_id,
            url=f"https://attack.mitre.org/techniques/{technique_id.replace('.', '/')}"
        )

        # Create attack pattern
        attack_pattern = stix2.AttackPattern(
            name=name,
            description=description,
            external_references=[external_ref],
            created_by_ref=self.scanner_identity.id
        )

        # Cache it
        self.cache["attack_patterns"][technique_id] = attack_pattern

        return attack_pattern

    def create_relationship(self, source_ref: str, relationship_type: str,
                          target_ref: str, description: str = "") -> 'stix2.Relationship':
        """
        Create STIX Relationship between two objects.

        Args:
            source_ref: Source object ID
            relationship_type: Type of relationship (e.g., "uses", "indicates", "mitigates")
            target_ref: Target object ID
            description: Optional description

        Returns:
            STIX Relationship object
        """
        return stix2.Relationship(
            source_ref=source_ref,
            relationship_type=relationship_type,
            target_ref=target_ref,
            description=description,
            created_by_ref=self.scanner_identity.id
        )

    def create_sighting(self, sighting_of_ref: str, count: int = 1,
                       observed_data_refs: Optional[List[str]] = None) -> 'stix2.Sighting':
        """
        Create STIX Sighting (observed instance of indicator/vulnerability).

        Args:
            sighting_of_ref: ID of what was sighted (indicator, vulnerability, etc.)
            count: Number of times sighted
            observed_data_refs: Optional list of observed data object IDs

        Returns:
            STIX Sighting object
        """
        now = datetime.now(timezone.utc)
        # Add 1 second to last_seen to ensure it's after first_seen
        last_seen = now + timedelta(seconds=1)

        return stix2.Sighting(
            sighting_of_ref=sighting_of_ref,
            count=count,
            observed_data_refs=observed_data_refs,
            created_by_ref=self.operator_identity.id,
            first_seen=now,
            last_seen=last_seen
        )

    def create_bundle_from_scan(self, scan_result: Dict) -> 'stix2.Bundle':
        """
        Create complete STIX Bundle from scan result.

        Args:
            scan_result: Full scan result dict with metadata and findings

        Returns:
            STIX Bundle containing all relevant objects
        """
        objects = []

        # Add core identities and tool
        objects.append(self.scanner_identity)
        objects.append(self.operator_identity)
        objects.append(self.scanner_tool)

        # Create plugin identity
        plugin_name = scan_result.get("metadata", {}).get("plugin_name", "Unknown Plugin")
        plugin_identity = stix2.Identity(
            name=plugin_name,
            identity_class="system",
            description=f"Claude Code plugin: {plugin_name}",
            created_by_ref=self.scanner_identity.id
        )
        objects.append(plugin_identity)

        # Process findings
        findings = scan_result.get("findings", [])
        for finding in findings:
            # Create indicator from finding
            indicator = self.create_indicator_from_finding(finding)
            objects.append(indicator)

            # Create sighting
            sighting = self.create_sighting(indicator.id, count=1)
            objects.append(sighting)

            # Create vulnerability if CVE present
            cve_id = finding.get("cve_id")
            if cve_id:
                vuln = self.create_vulnerability(
                    cve_id=cve_id,
                    description=finding.get("description", ""),
                    cvss_score=finding.get("cvss_score", 0.0)
                )
                objects.append(vuln)

                # Link indicator to vulnerability
                rel = self.create_relationship(
                    source_ref=indicator.id,
                    relationship_type="indicates",
                    target_ref=vuln.id,
                    description=f"Indicator detects {cve_id}"
                )
                objects.append(rel)

            # Create attack pattern if ATT&CK technique present
            attack_id = finding.get("attack_id")
            if attack_id:
                attack_pattern = self.create_attack_pattern(
                    technique_id=attack_id,
                    name=finding.get("attack_name", attack_id),
                    description=f"MITRE ATT&CK technique {attack_id}"
                )
                objects.append(attack_pattern)

                # Link indicator to attack pattern
                rel = self.create_relationship(
                    source_ref=indicator.id,
                    relationship_type="indicates",
                    target_ref=attack_pattern.id,
                    description=f"Indicator detects usage of {attack_id}"
                )
                objects.append(rel)

        # Create bundle (Bundle objects don't support created_by_ref)
        bundle = stix2.Bundle(objects=objects)

        return bundle

    def save_bundle(self, bundle: 'stix2.Bundle', output_file: Path):
        """
        Save STIX Bundle to JSON file.

        Args:
            bundle: STIX Bundle to save
            output_file: Path to output file
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(bundle.serialize(pretty=True))

        print(f"✓ STIX bundle saved to: {output_file}")
        print(f"  Objects: {len(bundle.objects)}")


def main():
    """Test and demo functionality."""
    print("STIX Builder Test\n")

    # Initialize builder
    print("[1/3] Initializing STIX Builder...")
    builder = STIXBuilder(
        scanner_name="Plugin Security Checker",
        scanner_version="2.0.0",
        operator_name="Security Research Team"
    )
    print("✓ Builder initialized")

    # Test: Create indicator from sample finding
    print("\n[2/3] Creating indicator from sample finding...")
    finding = {
        "severity": "CRITICAL",
        "category": "Dangerous Function",
        "file": "scripts/exploit.py",
        "line": 42,
        "code_snippet": "subprocess.run(cmd, shell=True)",
        "description": "Command injection via subprocess with shell=True",
        "cvss_score": 8.7,
        "cve_id": "CVE-2025-54795",
        "attack_id": "T1059.006",
        "attack_name": "Python"
    }

    indicator = builder.create_indicator_from_finding(finding)
    print(f"✓ Created indicator: {indicator.name}")

    # Test: Create vulnerability
    vuln = builder.create_vulnerability(
        cve_id="CVE-2025-54795",
        description="Command Injection via subprocess",
        cvss_score=8.7
    )
    print(f"✓ Created vulnerability: {vuln.name}")

    # Test: Create attack pattern
    attack = builder.create_attack_pattern(
        technique_id="T1059.006",
        name="Python",
        description="Adversaries may abuse Python for execution"
    )
    print(f"✓ Created attack pattern: {attack.name}")

    # Test: Create complete bundle
    print("\n[3/3] Creating complete STIX bundle from scan...")
    scan_result = {
        "metadata": {
            "plugin_name": "test-plugin",
            "risk_level": "CRITICAL",
            "total_findings": 1
        },
        "findings": [finding]
    }

    bundle = builder.create_bundle_from_scan(scan_result)
    print(f"✓ Created STIX bundle with {len(bundle.objects)} objects")

    # Print bundle summary
    object_types = {}
    for obj in bundle.objects:
        obj_type = obj.type
        object_types[obj_type] = object_types.get(obj_type, 0) + 1

    print("\nBundle contents:")
    for obj_type, count in sorted(object_types.items()):
        print(f"  - {obj_type}: {count}")

    print("\n✓ All tests passed!\n")
    return 0


if __name__ == "__main__":
    exit(main())
