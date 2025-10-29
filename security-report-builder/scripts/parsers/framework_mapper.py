#!/usr/bin/env python3
"""
Map security findings to frameworks (MITRE ATT&CK, ATLAS, OWASP, CWE).
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrameworkMapper:
    """Map security findings to threat intelligence frameworks."""

    def __init__(self, mappings_file: Optional[Path] = None):
        """
        Initialize framework mapper.

        Args:
            mappings_file: Path to framework mappings JSON
        """
        self.mappings = {}
        self.attack_techniques = {}
        self.atlas_techniques = {}
        self.owasp_categories = {}
        self.cwe_weaknesses = {}

        if mappings_file:
            self.load_mappings(mappings_file)

    def load_mappings(self, mappings_file: Path) -> None:
        """
        Load framework mappings from JSON file.

        Args:
            mappings_file: Path to mappings JSON
        """
        if not mappings_file.exists():
            logger.warning(f"Mappings file not found: {mappings_file}")
            return

        try:
            with open(mappings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.mappings = data.get('mappings', {})
            logger.info(f"Loaded {len(self.mappings)} framework mappings")

            # Build reverse lookup indices
            self._build_indices()

        except Exception as e:
            logger.error(f"Error loading mappings: {e}")

    def _build_indices(self) -> None:
        """Build reverse lookup indices for frameworks."""
        for pattern_id, mapping in self.mappings.items():
            # ATT&CK techniques
            for technique in mapping.get('att&ck_techniques', []):
                if technique not in self.attack_techniques:
                    self.attack_techniques[technique] = []
                self.attack_techniques[technique].append(pattern_id)

            # ATLAS techniques
            for technique in mapping.get('atlas_techniques', []):
                if technique not in self.atlas_techniques:
                    self.atlas_techniques[technique] = []
                self.atlas_techniques[technique].append(pattern_id)

            # OWASP categories
            for category in mapping.get('owasp_categories', []):
                if category not in self.owasp_categories:
                    self.owasp_categories[category] = []
                self.owasp_categories[category].append(pattern_id)

            # CWE weaknesses
            for cwe in mapping.get('cwe_ids', []):
                if cwe not in self.cwe_weaknesses:
                    self.cwe_weaknesses[cwe] = []
                self.cwe_weaknesses[cwe].append(pattern_id)

    def map_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a finding with framework mappings.

        Args:
            finding: Security finding dictionary

        Returns:
            Finding enriched with framework data
        """
        enriched = finding.copy()

        # Get category/pattern from finding
        category = finding.get('category', '')
        pattern = finding.get('pattern', '')

        # Look up mappings
        mapping_key = category or pattern
        if mapping_key in self.mappings:
            mapping = self.mappings[mapping_key]

            # Add framework references if not already present
            if 'att&ck_techniques' not in enriched:
                enriched['att&ck_techniques'] = mapping.get('att&ck_techniques', [])

            if 'atlas_techniques' not in enriched:
                enriched['atlas_techniques'] = mapping.get('atlas_techniques', [])

            if 'owasp_categories' not in enriched:
                enriched['owasp_categories'] = mapping.get('owasp_categories', [])

            if 'cwe_ids' not in enriched:
                enriched['cwe_ids'] = mapping.get('cwe_ids', [])

            # Add descriptions
            enriched['framework_descriptions'] = {
                'att&ck': mapping.get('att&ck_description', ''),
                'atlas': mapping.get('atlas_description', ''),
                'owasp': mapping.get('owasp_description', ''),
                'cwe': mapping.get('cwe_description', '')
            }

        return enriched

    def get_attack_coverage(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze MITRE ATT&CK coverage from findings.

        Args:
            findings: List of security findings

        Returns:
            ATT&CK coverage statistics
        """
        techniques = set()
        tactics = defaultdict(int)

        for finding in findings:
            for technique in finding.get('att&ck_techniques', []):
                techniques.add(technique)

                # Extract tactic from technique ID (e.g., T1059.006)
                # In real implementation, would lookup from STIX data
                if technique.startswith('T'):
                    base_technique = technique.split('.')[0]
                    # Simplified mapping - real impl would use STIX
                    tactic = self._infer_tactic(base_technique)
                    tactics[tactic] += 1

        return {
            'total_techniques': len(techniques),
            'techniques': sorted(techniques),
            'tactics': dict(tactics),
            'coverage_percent': self._calculate_coverage(len(techniques), 'attack')
        }

    def get_atlas_coverage(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze MITRE ATLAS coverage from findings.

        Args:
            findings: List of security findings

        Returns:
            ATLAS coverage statistics
        """
        techniques = set()
        tactics = defaultdict(int)

        for finding in findings:
            for technique in finding.get('atlas_techniques', []):
                techniques.add(technique)

                # Extract tactic (e.g., AML.T0043)
                if technique.startswith('AML'):
                    tactic = self._infer_atlas_tactic(technique)
                    tactics[tactic] += 1

        return {
            'total_techniques': len(techniques),
            'techniques': sorted(techniques),
            'tactics': dict(tactics),
            'coverage_percent': self._calculate_coverage(len(techniques), 'atlas')
        }

    def get_owasp_coverage(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze OWASP Top 10 coverage from findings.

        Args:
            findings: List of security findings

        Returns:
            OWASP coverage statistics
        """
        categories = defaultdict(int)

        for finding in findings:
            for category in finding.get('owasp_categories', []):
                categories[category] += 1

        return {
            'total_categories': len(categories),
            'categories': dict(categories),
            'most_common': sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def get_cwe_coverage(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze CWE weakness coverage from findings.

        Args:
            findings: List of security findings

        Returns:
            CWE coverage statistics
        """
        weaknesses = defaultdict(int)

        for finding in findings:
            for cwe in finding.get('cwe_ids', []):
                weaknesses[cwe] += 1

        return {
            'total_weaknesses': len(weaknesses),
            'weaknesses': dict(weaknesses),
            'most_common': sorted(weaknesses.items(), key=lambda x: x[1], reverse=True)[:10]
        }

    def _infer_tactic(self, technique_id: str) -> str:
        """Infer ATT&CK tactic from technique (simplified)."""
        # Simplified mapping - real implementation would use STIX data
        tactic_map = {
            'T1059': 'Execution',
            'T1203': 'Execution',
            'T1055': 'Privilege Escalation',
            'T1068': 'Privilege Escalation',
            'T1027': 'Defense Evasion',
            'T1140': 'Defense Evasion',
            'T1071': 'Command and Control',
            'T1090': 'Command and Control'
        }
        return tactic_map.get(technique_id, 'Unknown')

    def _infer_atlas_tactic(self, technique_id: str) -> str:
        """Infer ATLAS tactic from technique (simplified)."""
        # Simplified mapping - real implementation would use STIX data
        tactic_map = {
            'AML.T0043': 'Model Access',
            'AML.T0040': 'ML Attack Staging',
            'AML.T0015': 'Evade ML Model'
        }
        return tactic_map.get(technique_id, 'Unknown')

    def _calculate_coverage(self, found: int, framework: str) -> float:
        """Calculate coverage percentage."""
        # Total techniques in each framework (approximate)
        totals = {
            'attack': 200,  # ~200 techniques in ATT&CK
            'atlas': 40     # ~40 techniques in ATLAS
        }
        total = totals.get(framework, 100)
        return round((found / total) * 100, 2) if total > 0 else 0.0

    def generate_framework_summary(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive framework summary.

        Args:
            findings: List of security findings

        Returns:
            Framework analysis summary
        """
        return {
            'mitre_attack': self.get_attack_coverage(findings),
            'mitre_atlas': self.get_atlas_coverage(findings),
            'owasp': self.get_owasp_coverage(findings),
            'cwe': self.get_cwe_coverage(findings),
            'total_findings': len(findings)
        }


def main():
    """CLI interface for testing the mapper."""
    import argparse

    parser = argparse.ArgumentParser(description='Map findings to security frameworks')
    parser.add_argument('findings', help='Input JSON file with findings')
    parser.add_argument('--mappings', help='Framework mappings file',
                       default='../references/framework_mappings.json')

    args = parser.parse_args()

    # Load mapper
    mapper = FrameworkMapper(Path(args.mappings))

    # Load findings
    with open(args.findings, 'r') as f:
        data = json.load(f)
        findings = data.get('all_findings', [])

    # Enrich findings
    enriched = [mapper.map_finding(f) for f in findings]

    # Generate summary
    summary = mapper.generate_framework_summary(enriched)

    print(json.dumps(summary, indent=2))

    return 0


if __name__ == '__main__':
    exit(main())
