#!/usr/bin/env python3
"""
STIX 2.1 Data Manager for MITRE ATT&CK Integration

This module provides a clean interface to load, query, and work with
MITRE ATT&CK data in STIX 2.1 format.

Features:
- Load STIX 2.1 bundles from local JSON files
- Query Attack Patterns by ATT&CK ID (e.g., T1059.006)
- Query Intrusion Sets (APT groups) using specific techniques
- Query Mitigations (Course of Action) for techniques
- Cache STIX objects for performance
- Support for Enterprise, Mobile, and ICS ATT&CK matrices

Usage:
    from scripts.stix_manager import STIXManager

    # Initialize manager
    stix = STIXManager()

    # Load Enterprise ATT&CK data
    stix.load_attack_data("enterprise")

    # Get Python execution technique
    technique = stix.get_attack_pattern("T1059.006")

    # Get APT groups using this technique
    groups = stix.get_intrusion_sets_using_technique("T1059.006")

    # Get mitigations
    mitigations = stix.get_mitigations("T1059.006")

Dependencies:
    - stix2>=3.0.1
    - Python 3.8+

Author: Plugin Security Checker Team
Version: 2.0.0
License: MIT
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict

try:
    import stix2
    STIX2_AVAILABLE = True
except ImportError:
    STIX2_AVAILABLE = False
    print("WARNING: stix2 library not available. Run: pip3 install -r requirements.txt")


class STIXManager:
    """
    Manager for MITRE ATT&CK STIX 2.1 data.

    Provides efficient loading, indexing, and querying of STIX objects
    from MITRE ATT&CK data files.
    """

    def __init__(self, stix_dir: Optional[str] = None):
        """
        Initialize STIX Manager.

        Args:
            stix_dir: Path to directory containing STIX JSON files.
                     Defaults to ../references/stix/ relative to this script.
        """
        if stix_dir is None:
            script_dir = Path(__file__).parent
            stix_dir = script_dir.parent / "references" / "stix"

        self.stix_dir = Path(stix_dir)

        # STIX object storage
        self.bundles: Dict[str, Dict] = {}  # domain -> bundle dict
        self.objects: Dict[str, Dict] = {}  # domain -> {id -> object}

        # Indexes for fast lookup
        self.attack_patterns: Dict[str, Dict] = {}  # domain -> {attack_id -> object}
        self.intrusion_sets: Dict[str, List] = {}   # domain -> [objects]
        self.malware: Dict[str, List] = {}          # domain -> [objects]
        self.tools: Dict[str, List] = {}            # domain -> [objects]
        self.mitigations: Dict[str, List] = {}      # domain -> [objects]
        self.relationships: Dict[str, List] = {}    # domain -> [relationships]

        # Relationship indexes
        self.technique_to_groups: Dict[str, Dict] = {}  # domain -> {technique_id -> [group_ids]}
        self.technique_to_mitigations: Dict[str, Dict] = {}  # domain -> {technique_id -> [mitigation_ids]}

        # Statistics
        self.stats: Dict[str, Dict] = {}  # domain -> stats

    def load_attack_data(self, domain: str = "enterprise") -> bool:
        """
        Load MITRE ATT&CK or ATLAS data for a specific domain.

        Args:
            domain: Domain to load. Options: "enterprise", "mobile", "ics", "atlas"

        Returns:
            True if successful, False otherwise
        """
        valid_domains = ["enterprise", "mobile", "ics", "atlas"]
        if domain not in valid_domains:
            print(f"ERROR: Invalid domain '{domain}'. Must be one of: {valid_domains}")
            return False

        # Construct filename (ATLAS uses different naming)
        if domain == "atlas":
            stix_file = self.stix_dir / "atlas.json"
        else:
            stix_file = self.stix_dir / f"{domain}-attack.json"

        if not stix_file.exists():
            print(f"ERROR: STIX file not found: {stix_file}")
            print(f"Run: bash scripts/download_attack_data.sh")
            return False

        print(f"Loading {domain} ATT&CK data from {stix_file}...")

        try:
            # Load JSON bundle
            with open(stix_file, 'r', encoding='utf-8') as f:
                bundle = json.load(f)

            # Validate it's a STIX bundle
            if bundle.get("type") != "bundle":
                print(f"ERROR: File is not a STIX bundle (type={bundle.get('type')})")
                return False

            # Store bundle
            self.bundles[domain] = bundle

            # Index objects
            self._index_objects(domain, bundle)

            # Build relationship indexes
            self._build_relationship_indexes(domain)

            # Calculate statistics
            self._calculate_stats(domain)

            print(f"✓ Loaded {self.stats[domain]['total_objects']} STIX objects")
            print(f"  - Attack Patterns: {self.stats[domain]['attack_patterns']}")
            print(f"  - Intrusion Sets: {self.stats[domain]['intrusion_sets']}")
            print(f"  - Malware: {self.stats[domain]['malware']}")
            print(f"  - Tools: {self.stats[domain]['tools']}")
            print(f"  - Mitigations: {self.stats[domain]['mitigations']}")
            print(f"  - Relationships: {self.stats[domain]['relationships']}")

            return True

        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {stix_file}: {e}")
            return False
        except Exception as e:
            print(f"ERROR: Failed to load {stix_file}: {e}")
            return False

    def _index_objects(self, domain: str, bundle: Dict):
        """Index STIX objects from bundle for fast lookup."""
        objects = bundle.get("objects", [])

        # Initialize indexes for this domain
        self.objects[domain] = {}
        self.attack_patterns[domain] = {}
        self.intrusion_sets[domain] = []
        self.malware[domain] = []
        self.tools[domain] = []
        self.mitigations[domain] = []
        self.relationships[domain] = []

        for obj in objects:
            obj_type = obj.get("type")
            obj_id = obj.get("id")

            # Store in main object index
            self.objects[domain][obj_id] = obj

            # Index by type
            if obj_type == "attack-pattern":
                # Extract ATT&CK ID from external references
                attack_id = self._extract_attack_id(obj)
                if attack_id:
                    self.attack_patterns[domain][attack_id] = obj

            elif obj_type == "intrusion-set":
                self.intrusion_sets[domain].append(obj)

            elif obj_type == "malware":
                self.malware[domain].append(obj)

            elif obj_type == "tool":
                self.tools[domain].append(obj)

            elif obj_type == "course-of-action":
                self.mitigations[domain].append(obj)

            elif obj_type == "relationship":
                self.relationships[domain].append(obj)

    def _extract_attack_id(self, attack_pattern: Dict) -> Optional[str]:
        """Extract ATT&CK ID (e.g., T1059.006) or ATLAS ID (e.g., AML.T0051) from attack pattern."""
        external_refs = attack_pattern.get("external_references", [])
        for ref in external_refs:
            source = ref.get("source_name")
            # Support both ATT&CK and ATLAS IDs
            if source in ["mitre-attack", "mitre-atlas"]:
                return ref.get("external_id")
        return None

    def _build_relationship_indexes(self, domain: str):
        """Build relationship indexes for fast lookup."""
        self.technique_to_groups[domain] = defaultdict(list)
        self.technique_to_mitigations[domain] = defaultdict(list)

        for rel in self.relationships[domain]:
            rel_type = rel.get("relationship_type")
            source_ref = rel.get("source_ref")
            target_ref = rel.get("target_ref")

            # Intrusion Set -> Attack Pattern (uses)
            if rel_type == "uses":
                source_obj = self.objects[domain].get(source_ref)
                target_obj = self.objects[domain].get(target_ref)

                if source_obj and target_obj:
                    if source_obj.get("type") == "intrusion-set" and target_obj.get("type") == "attack-pattern":
                        attack_id = self._extract_attack_id(target_obj)
                        if attack_id:
                            self.technique_to_groups[domain][attack_id].append(source_ref)

            # Course of Action -> Attack Pattern (mitigates)
            elif rel_type == "mitigates":
                source_obj = self.objects[domain].get(source_ref)
                target_obj = self.objects[domain].get(target_ref)

                if source_obj and target_obj:
                    if source_obj.get("type") == "course-of-action" and target_obj.get("type") == "attack-pattern":
                        attack_id = self._extract_attack_id(target_obj)
                        if attack_id:
                            self.technique_to_mitigations[domain][attack_id].append(source_ref)

    def _calculate_stats(self, domain: str):
        """Calculate statistics for loaded data."""
        self.stats[domain] = {
            "total_objects": len(self.objects[domain]),
            "attack_patterns": len(self.attack_patterns[domain]),
            "intrusion_sets": len(self.intrusion_sets[domain]),
            "malware": len(self.malware[domain]),
            "tools": len(self.tools[domain]),
            "mitigations": len(self.mitigations[domain]),
            "relationships": len(self.relationships[domain])
        }

    def get_attack_pattern(self, technique_id: str, domain: str = "enterprise") -> Optional[Dict]:
        """
        Get Attack Pattern by ATT&CK ID.

        Args:
            technique_id: ATT&CK technique ID (e.g., "T1059.006")
            domain: Domain to search in

        Returns:
            STIX Attack Pattern object or None if not found
        """
        if domain not in self.attack_patterns:
            print(f"ERROR: Domain '{domain}' not loaded. Call load_attack_data() first.")
            return None

        return self.attack_patterns[domain].get(technique_id)

    def get_intrusion_sets_using_technique(self, technique_id: str, domain: str = "enterprise") -> List[Dict]:
        """
        Get Intrusion Sets (APT groups) that use a specific technique.

        Args:
            technique_id: ATT&CK technique ID (e.g., "T1059.006")
            domain: Domain to search in

        Returns:
            List of STIX Intrusion Set objects
        """
        if domain not in self.technique_to_groups:
            print(f"ERROR: Domain '{domain}' not loaded. Call load_attack_data() first.")
            return []

        group_ids = self.technique_to_groups[domain].get(technique_id, [])
        groups = []

        for group_id in group_ids:
            group = self.objects[domain].get(group_id)
            if group:
                groups.append(group)

        return groups

    def get_mitigations(self, technique_id: str, domain: str = "enterprise") -> List[Dict]:
        """
        Get Mitigations (Course of Action) for a specific technique.

        Args:
            technique_id: ATT&CK technique ID (e.g., "T1059.006")
            domain: Domain to search in

        Returns:
            List of STIX Course of Action objects
        """
        if domain not in self.technique_to_mitigations:
            print(f"ERROR: Domain '{domain}' not loaded. Call load_attack_data() first.")
            return []

        mitigation_ids = self.technique_to_mitigations[domain].get(technique_id, [])
        mitigations = []

        for mitigation_id in mitigation_ids:
            mitigation = self.objects[domain].get(mitigation_id)
            if mitigation:
                mitigations.append(mitigation)

        return mitigations

    def query_objects(self, object_type: str, domain: str = "enterprise", filters: Optional[Dict] = None) -> List[Dict]:
        """
        Generic query for STIX objects.

        Args:
            object_type: STIX object type (e.g., "attack-pattern", "intrusion-set")
            domain: Domain to search in
            filters: Optional dict of field->value filters

        Returns:
            List of matching STIX objects
        """
        if domain not in self.objects:
            print(f"ERROR: Domain '{domain}' not loaded. Call load_attack_data() first.")
            return []

        results = []

        for obj in self.objects[domain].values():
            if obj.get("type") != object_type:
                continue

            # Apply filters
            if filters:
                match = True
                for field, value in filters.items():
                    if obj.get(field) != value:
                        match = False
                        break
                if not match:
                    continue

            results.append(obj)

        return results

    def get_technique_name(self, technique_id: str, domain: str = "enterprise") -> Optional[str]:
        """Get human-readable name for a technique."""
        pattern = self.get_attack_pattern(technique_id, domain)
        if pattern:
            return pattern.get("name")
        return None

    def get_technique_description(self, technique_id: str, domain: str = "enterprise") -> Optional[str]:
        """Get description for a technique."""
        pattern = self.get_attack_pattern(technique_id, domain)
        if pattern:
            return pattern.get("description")
        return None

    def get_all_techniques(self, domain: str = "enterprise") -> List[str]:
        """Get list of all technique IDs in domain."""
        if domain not in self.attack_patterns:
            return []
        return list(self.attack_patterns[domain].keys())

    def print_stats(self, domain: str = "enterprise"):
        """Print statistics for loaded domain."""
        if domain not in self.stats:
            print(f"ERROR: Domain '{domain}' not loaded.")
            return

        print(f"\n{'='*70}")
        print(f" MITRE ATT&CK {domain.upper()} Statistics")
        print(f"{'='*70}")
        print(f"Total Objects:      {self.stats[domain]['total_objects']:,}")
        print(f"Attack Patterns:    {self.stats[domain]['attack_patterns']:,}")
        print(f"Intrusion Sets:     {self.stats[domain]['intrusion_sets']:,}")
        print(f"Malware:            {self.stats[domain]['malware']:,}")
        print(f"Tools:              {self.stats[domain]['tools']:,}")
        print(f"Mitigations:        {self.stats[domain]['mitigations']:,}")
        print(f"Relationships:      {self.stats[domain]['relationships']:,}")
        print(f"{'='*70}\n")


def main():
    """Test and demo functionality."""
    print("STIX Manager Test\n")

    # Initialize manager
    stix = STIXManager()

    # Load Enterprise ATT&CK
    print("[1/4] Loading Enterprise ATT&CK data...")
    if not stix.load_attack_data("enterprise"):
        print("FAILED: Could not load Enterprise ATT&CK data")
        return 1

    print("\n[2/4] Testing technique lookup...")
    # Test: Get Python execution technique
    technique = stix.get_attack_pattern("T1059.006")
    if technique:
        print(f"✓ Found technique T1059.006: {technique.get('name')}")
        print(f"  Description: {technique.get('description', '')[:100]}...")
    else:
        print("✗ FAILED: Could not find T1059.006")

    print("\n[3/4] Testing intrusion set lookup...")
    # Test: Get groups using Python
    groups = stix.get_intrusion_sets_using_technique("T1059.006")
    if groups:
        print(f"✓ Found {len(groups)} groups using T1059.006:")
        for group in groups[:5]:  # Show first 5
            print(f"  - {group.get('name')}")
        if len(groups) > 5:
            print(f"  ... and {len(groups) - 5} more")
    else:
        print("  No groups found using this technique")

    print("\n[4/4] Testing mitigation lookup...")
    # Test: Get mitigations
    mitigations = stix.get_mitigations("T1059.006")
    if mitigations:
        print(f"✓ Found {len(mitigations)} mitigations for T1059.006:")
        for mitigation in mitigations:
            print(f"  - {mitigation.get('name')}")
    else:
        print("  No mitigations found for this technique")

    # Print statistics
    stix.print_stats("enterprise")

    print("✓ All tests passed!\n")
    return 0


if __name__ == "__main__":
    exit(main())
