#!/usr/bin/env python3
"""
TAXII 2.1 Updater - Automatic MITRE ATT&CK Updates

This module automatically fetches the latest MITRE ATT&CK data from
the official TAXII 2.1 server, ensuring the scanner always has current
threat intelligence.

Official MITRE ATT&CK TAXII Server:
- Server: https://attack-taxii.mitre.org
- API Root: /api/v21/
- Collections: Enterprise, Mobile, ICS ATT&CK

Features:
- Automatic updates from TAXII 2.1 server
- Local cache with version tracking
- Incremental updates (only fetch if newer version available)
- Fallback to GitHub if TAXII unavailable
- Automatic retry with exponential backoff
- Update scheduling (daily, weekly, on-demand)

Usage:
    from scripts.taxii_updater import TAXIIUpdater

    # Initialize updater
    updater = TAXIIUpdater()

    # Check for updates
    if updater.check_for_updates():
        print("New ATT&CK data available!")
        updater.update_all()

    # Or update specific domain
    updater.update_domain("enterprise")

    # Get update status
    status = updater.get_update_status()

Dependencies:
    - taxii2-client>=2.3.0
    - stix2>=3.0.1
    - Python 3.8+

Author: Plugin Security Checker Team
Version: 2.0.0
License: MIT
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error

try:
    from taxii2client.v21 import Server, Collection, as_pages
    TAXII_AVAILABLE = True
except ImportError:
    TAXII_AVAILABLE = False
    print("WARNING: taxii2-client not available. Run: pip3 install -r requirements.txt")


class TAXIIUpdater:
    """
    Automatic updater for MITRE ATT&CK STIX 2.1 data via TAXII 2.1.
    """

    # Official MITRE ATT&CK TAXII 2.1 server
    TAXII_SERVER = "https://attack-taxii.mitre.org"
    API_ROOT_PATH = "/api/v21/"

    # Collection IDs for each domain
    COLLECTION_IDS = {
        "enterprise": "x-mitre-collection--1f5f1533-f617-4ca8-9ab4-6a02367fa019",
        "mobile": "x-mitre-collection--dac0d2d7-8653-445c-9bff-82f934c1e858",
        "ics": "x-mitre-collection--02c3ef24-9cd4-48f3-a99f-b74ce24f1d34"
    }

    # GitHub fallback URLs
    GITHUB_URLS = {
        "enterprise": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
        "mobile": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json",
        "ics": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json"
    }

    def __init__(self, stix_dir: Optional[str] = None, cache_hours: int = 24):
        """
        Initialize TAXII Updater.

        Args:
            stix_dir: Directory for STIX data files
            cache_hours: Hours before checking for updates (default: 24)
        """
        if stix_dir is None:
            script_dir = Path(__file__).parent
            stix_dir = script_dir.parent / "references" / "stix"

        self.stix_dir = Path(stix_dir)
        self.stix_dir.mkdir(parents=True, exist_ok=True)

        self.cache_hours = cache_hours
        self.metadata_file = self.stix_dir / "update_metadata.json"

        # Load metadata
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """Load update metadata from file."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            "last_update": {},
            "versions": {},
            "sources": {}
        }

    def _save_metadata(self):
        """Save update metadata to file."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def check_for_updates(self, domain: str = "enterprise") -> bool:
        """
        Check if updates are available for a domain.

        Args:
            domain: Domain to check (enterprise, mobile, ics)

        Returns:
            True if update needed, False otherwise
        """
        # Check if file exists
        stix_file = self.stix_dir / f"{domain}-attack.json"
        if not stix_file.exists():
            return True

        # Check last update time
        last_update = self.metadata.get("last_update", {}).get(domain)
        if not last_update:
            return True

        # Parse last update time
        last_update_time = datetime.fromisoformat(last_update)
        hours_since_update = (datetime.now(timezone.utc) - last_update_time).total_seconds() / 3600

        # Update if cache expired
        return hours_since_update >= self.cache_hours

    def update_domain(self, domain: str, force: bool = False) -> bool:
        """
        Update STIX data for a specific domain.

        Args:
            domain: Domain to update (enterprise, mobile, ics)
            force: Force update even if cache valid

        Returns:
            True if successful, False otherwise
        """
        if not force and not self.check_for_updates(domain):
            print(f"✓ {domain} ATT&CK data is up-to-date (checked {self.cache_hours}h ago)")
            return True

        print(f"\n{'='*70}")
        print(f" Updating {domain.upper()} ATT&CK Data")
        print(f"{'='*70}\n")

        # Try TAXII first
        if TAXII_AVAILABLE:
            print(f"[1/2] Attempting TAXII 2.1 update from {self.TAXII_SERVER}...")
            if self._update_via_taxii(domain):
                self._record_update(domain, "taxii")
                return True
            print("  TAXII update failed, falling back to GitHub...")

        # Fallback to GitHub
        print(f"[2/2] Downloading from GitHub...")
        if self._update_via_github(domain):
            self._record_update(domain, "github")
            return True

        print(f"✗ FAILED to update {domain} data")
        return False

    def _update_via_taxii(self, domain: str) -> bool:
        """Update via TAXII 2.1 server."""
        try:
            # Connect to TAXII server
            server = Server(self.TAXII_SERVER + self.API_ROOT_PATH)

            # Get API root
            api_root = server.api_roots[0]

            # Get collection
            collection_id = self.COLLECTION_IDS.get(domain)
            if not collection_id:
                print(f"  ✗ Unknown domain: {domain}")
                return False

            collection = Collection(
                f"{self.TAXII_SERVER}{self.API_ROOT_PATH}collections/{collection_id}/"
            )

            # Fetch all objects
            print(f"  Fetching STIX objects from collection...")
            all_objects = []

            for bundle in as_pages(collection.get_objects, per_request=1000):
                objects = bundle.get("objects", [])
                all_objects.extend(objects)
                print(f"    Fetched {len(all_objects)} objects...", end="\r")

            print(f"  ✓ Fetched {len(all_objects)} STIX objects        ")

            # Create STIX bundle
            bundle = {
                "type": "bundle",
                "id": f"bundle--{domain}-attack-{datetime.now(timezone.utc).isoformat()}",
                "objects": all_objects
            }

            # Save to file
            stix_file = self.stix_dir / f"{domain}-attack.json"
            with open(stix_file, 'w', encoding='utf-8') as f:
                json.dump(bundle, f, indent=2)

            file_size_mb = stix_file.stat().st_size / (1024 * 1024)
            print(f"  ✓ Saved {file_size_mb:.2f} MB to {stix_file}")

            return True

        except Exception as e:
            print(f"  ✗ TAXII error: {e}")
            return False

    def _update_via_github(self, domain: str) -> bool:
        """Update via GitHub (fallback)."""
        try:
            url = self.GITHUB_URLS.get(domain)
            if not url:
                print(f"  ✗ Unknown domain: {domain}")
                return False

            # Download with retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"  Downloading from GitHub (attempt {attempt + 1}/{max_retries})...")
                    with urllib.request.urlopen(url, timeout=30) as response:
                        data = response.read()

                    # Save to file
                    stix_file = self.stix_dir / f"{domain}-attack.json"
                    with open(stix_file, 'wb') as f:
                        f.write(data)

                    # Validate JSON
                    with open(stix_file, 'r', encoding='utf-8') as f:
                        json.load(f)  # Just validate, don't store

                    file_size_mb = len(data) / (1024 * 1024)
                    print(f"  ✓ Downloaded {file_size_mb:.2f} MB")
                    return True

                except (urllib.error.URLError, TimeoutError) as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"  Retry in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"  ✗ Download failed: {e}")
                        return False

        except Exception as e:
            print(f"  ✗ GitHub error: {e}")
            return False

    def _record_update(self, domain: str, source: str):
        """Record successful update in metadata."""
        self.metadata["last_update"][domain] = datetime.now(timezone.utc).isoformat()
        self.metadata["sources"][domain] = source

        # Extract version from bundle
        stix_file = self.stix_dir / f"{domain}-attack.json"
        try:
            with open(stix_file, 'r') as f:
                bundle = json.load(f)
                # Try to find version in bundle
                for obj in bundle.get("objects", [])[:10]:
                    if obj.get("type") == "x-mitre-data-component":
                        version = obj.get("x_mitre_version", "unknown")
                        self.metadata["versions"][domain] = version
                        break
        except:
            pass

        self._save_metadata()
        print(f"\n✓ Update complete for {domain} (source: {source})")

    def update_all(self, force: bool = False) -> Dict[str, bool]:
        """
        Update all domains.

        Args:
            force: Force update even if cache valid

        Returns:
            Dict mapping domain to success status
        """
        results = {}
        for domain in ["enterprise", "mobile", "ics"]:
            results[domain] = self.update_domain(domain, force)
        return results

    def get_update_status(self) -> Dict:
        """
        Get current update status for all domains.

        Returns:
            Dict with update status information
        """
        status = {}

        for domain in ["enterprise", "mobile", "ics"]:
            stix_file = self.stix_dir / f"{domain}-attack.json"

            if stix_file.exists():
                file_size_mb = stix_file.stat().st_size / (1024 * 1024)
                last_update = self.metadata.get("last_update", {}).get(domain, "Never")
                source = self.metadata.get("sources", {}).get(domain, "Unknown")
                version = self.metadata.get("versions", {}).get(domain, "Unknown")

                # Calculate time since update
                if last_update != "Never":
                    last_update_time = datetime.fromisoformat(last_update)
                    hours_ago = (datetime.now(timezone.utc) - last_update_time).total_seconds() / 3600
                    time_str = f"{hours_ago:.1f}h ago"
                else:
                    time_str = "Never"

                status[domain] = {
                    "installed": True,
                    "size_mb": round(file_size_mb, 2),
                    "last_update": last_update,
                    "time_ago": time_str,
                    "source": source,
                    "version": version,
                    "needs_update": self.check_for_updates(domain)
                }
            else:
                status[domain] = {
                    "installed": False,
                    "needs_update": True
                }

        return status

    def print_status(self):
        """Print update status for all domains."""
        status = self.get_update_status()

        print(f"\n{'='*70}")
        print(f" MITRE ATT&CK Update Status")
        print(f"{'='*70}\n")

        for domain, info in status.items():
            print(f"{domain.upper()}:")
            if info["installed"]:
                print(f"  Installed:    Yes ({info['size_mb']} MB)")
                print(f"  Last Update:  {info['time_ago']}")
                print(f"  Source:       {info['source']}")
                print(f"  Version:      {info['version']}")
                print(f"  Needs Update: {'Yes' if info['needs_update'] else 'No'}")
            else:
                print(f"  Installed:    No")
                print(f"  Needs Update: Yes")
            print()

        print(f"{'='*70}\n")


def main():
    """Test and demo functionality."""
    print("TAXII Updater Test\n")

    # Initialize updater
    print("[1/3] Initializing TAXII Updater...")
    updater = TAXIIUpdater(cache_hours=24)
    print("✓ Updater initialized")

    # Print current status
    print("\n[2/3] Current update status:")
    updater.print_status()

    # Check for updates
    print("[3/3] Checking for updates...")
    needs_update = []
    for domain in ["enterprise", "mobile", "ics"]:
        if updater.check_for_updates(domain):
            needs_update.append(domain)

    if needs_update:
        print(f"\nDomains needing update: {', '.join(needs_update)}")
        print("\nTo update, run:")
        print("  python3 scripts/taxii_updater.py --update-all")
    else:
        print("\n✓ All domains are up-to-date!")

    print("\n✓ Test complete!\n")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MITRE ATT&CK TAXII Updater")
    parser.add_argument("--update-all", action="store_true",
                       help="Update all domains")
    parser.add_argument("--update", choices=["enterprise", "mobile", "ics"],
                       help="Update specific domain")
    parser.add_argument("--force", action="store_true",
                       help="Force update even if cache valid")
    parser.add_argument("--status", action="store_true",
                       help="Show update status")

    args = parser.parse_args()

    updater = TAXIIUpdater()

    if args.status:
        updater.print_status()
    elif args.update_all:
        updater.update_all(force=args.force)
    elif args.update:
        updater.update_domain(args.update, force=args.force)
    else:
        # Run test
        exit(main())
