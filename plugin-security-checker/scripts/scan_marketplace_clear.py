#!/usr/bin/env python3
"""
Clear Marketplace Scanner - Properly Categorizes What's Being Scanned

CATEGORIES (CRYSTAL CLEAR):
1. Valid Claude Code Plugins WITH code → SCAN THESE
2. Valid Claude Code Plugins WITHOUT code → SKIP (docs only)
3. Invalid plugins (has .claude-plugin but no plugin.json) → SKIP
4. Non-plugin repos with code → SKIP (not Claude plugins)
5. Empty repos → SKIP

SCAN RESULTS CLEARLY SHOW:
- What category each repo belongs to
- How many files in each category
- What was actually scanned vs skipped
- Why things were skipped
"""

import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

from intelligent_orchestrator import IntelligentOrchestrator


@dataclass
class RepoClassification:
    """Clear classification of what a repo is"""
    name: str
    category: str  # "VALID_PLUGIN_WITH_CODE", "VALID_PLUGIN_NO_CODE", "INVALID_PLUGIN", "NON_PLUGIN", "EMPTY"
    has_plugin_json: bool
    code_files: int
    py_files: int
    js_files: int
    ts_files: int
    should_scan: bool
    skip_reason: Optional[str]


@dataclass
class ScanResults:
    """Clear scan results"""
    scan_date: str
    total_repos: int

    # Category counts
    valid_plugins_with_code: int
    valid_plugins_no_code: int
    invalid_plugins: int
    non_plugins: int
    empty_repos: int

    # What was actually scanned
    repos_scanned: int
    files_scanned: int
    detections_found: int

    # Breakdown by confidence
    high_confidence: int
    medium_confidence: int
    low_confidence: int

    # Learning metrics
    conflicts_resolved: int
    consensus_detections: int

    # Performance
    scan_time_seconds: float
    memory_mb: float

    # Details
    classifications: List[Dict]
    scanned_plugins: List[Dict]
    skipped_summary: Dict[str, int]


class ClearMarketplaceScanner:
    """Scanner with CLEAR categorization and reporting"""

    def __init__(self, marketplace_dir: str):
        self.marketplace_dir = Path(marketplace_dir)
        self.patterns_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded.json"

        # Results
        self.classifications: List[RepoClassification] = []
        self.scan_results: List[Dict] = []

    def classify_repos(self):
        """Step 1: Classify ALL repos clearly"""

        print("=" * 80)
        print("STEP 1: CLASSIFYING ALL REPOS")
        print("=" * 80)
        print()

        repos = sorted([d for d in self.marketplace_dir.iterdir() if d.is_dir()])

        for i, repo in enumerate(repos, 1):
            plugin_json = repo / '.claude-plugin' / 'plugin.json'
            has_plugin_dir = (repo / '.claude-plugin').exists()

            # Count code files
            py_files = list(repo.rglob('*.py'))
            js_files = list(repo.rglob('*.js'))
            ts_files = list(repo.rglob('*.ts'))

            code_count = len(py_files) + len(js_files) + len(ts_files)

            # Determine category
            is_valid_plugin = False
            if plugin_json.exists():
                try:
                    with open(plugin_json) as f:
                        data = json.load(f)
                        if 'name' in data or 'id' in data:
                            is_valid_plugin = True
                except:
                    pass

            if is_valid_plugin and code_count > 0:
                category = "VALID_PLUGIN_WITH_CODE"
                should_scan = True
                skip_reason = None
            elif is_valid_plugin and code_count == 0:
                category = "VALID_PLUGIN_NO_CODE"
                should_scan = False
                skip_reason = "Documentation only - no code files"
            elif has_plugin_dir and not is_valid_plugin:
                category = "INVALID_PLUGIN"
                should_scan = False
                skip_reason = "Missing or invalid .claude-plugin/plugin.json"
            elif not has_plugin_dir and code_count > 0:
                category = "NON_PLUGIN"
                should_scan = False
                skip_reason = "Not a Claude Code plugin (no .claude-plugin directory)"
            else:
                category = "EMPTY"
                should_scan = False
                skip_reason = "Empty repository"

            classification = RepoClassification(
                name=repo.name,
                category=category,
                has_plugin_json=plugin_json.exists(),
                code_files=code_count,
                py_files=len(py_files),
                js_files=len(js_files),
                ts_files=len(ts_files),
                should_scan=should_scan,
                skip_reason=skip_reason
            )

            self.classifications.append(classification)

            # Show progress every 50 repos
            if i % 50 == 0:
                print(f"  Classified {i}/{len(repos)} repos...")

        print(f"  ✓ Classified all {len(repos)} repos")
        print()

    def print_classification_summary(self):
        """Print clear summary of what we found"""

        total = len(self.classifications)

        valid_with_code = [c for c in self.classifications if c.category == "VALID_PLUGIN_WITH_CODE"]
        valid_no_code = [c for c in self.classifications if c.category == "VALID_PLUGIN_NO_CODE"]
        invalid = [c for c in self.classifications if c.category == "INVALID_PLUGIN"]
        non_plugins = [c for c in self.classifications if c.category == "NON_PLUGIN"]
        empty = [c for c in self.classifications if c.category == "EMPTY"]

        print("=" * 80)
        print("CLASSIFICATION SUMMARY")
        print("=" * 80)
        print()
        print(f"Total repos analyzed: {total}")
        print()
        print("Categories:")
        print(f"  ✅ VALID Claude Code Plugins WITH code:    {len(valid_with_code):3d} ({len(valid_with_code)/total*100:5.1f}%) → WILL SCAN")
        print(f"  📄 VALID Claude Code Plugins WITHOUT code: {len(valid_no_code):3d} ({len(valid_no_code)/total*100:5.1f}%) → SKIP (docs only)")
        print(f"  ⚠️  INVALID plugins (missing plugin.json):  {len(invalid):3d} ({len(invalid)/total*100:5.1f}%) → SKIP")
        print(f"  ❌ NON-plugins (has code, no .claude-plugin): {len(non_plugins):3d} ({len(non_plugins)/total*100:5.1f}%) → SKIP")
        print(f"  📭 EMPTY repos:                            {len(empty):3d} ({len(empty)/total*100:5.1f}%) → SKIP")
        print()
        print(f"WILL SCAN: {len(valid_with_code)} plugins")
        print(f"WILL SKIP: {total - len(valid_with_code)} repos")
        print()

        # Show what will be scanned
        total_files = sum(c.code_files for c in valid_with_code)
        print(f"Files to scan in valid plugins:")
        print(f"  Python (.py):     {sum(c.py_files for c in valid_with_code):5d}")
        print(f"  JavaScript (.js): {sum(c.js_files for c in valid_with_code):5d}")
        print(f"  TypeScript (.ts): {sum(c.ts_files for c in valid_with_code):5d}")
        print(f"  Total:            {total_files:5d}")
        print()

        # Show the plugins we'll scan
        print(f"Plugins to scan ({len(valid_with_code)}):")
        for i, c in enumerate(valid_with_code, 1):
            print(f"  {i:2d}. {c.name:50s} {c.code_files:4d} files ({c.py_files} py, {c.js_files} js, {c.ts_files} ts)")
        print()

    def scan_valid_plugins(self):
        """Step 2: Scan only the valid plugins with code"""

        valid_plugins = [c for c in self.classifications if c.should_scan]

        if not valid_plugins:
            print("No valid plugins to scan!")
            return

        print("=" * 80)
        print(f"STEP 2: SCANNING {len(valid_plugins)} VALID PLUGINS")
        print("=" * 80)
        print()

        # Initialize orchestrator
        orchestrator = IntelligentOrchestrator(
            patterns_file=str(self.patterns_file),
            max_memory_mb=500,
            enable_adaptive_routing=True
        )

        total_detections = 0
        high_conf = 0
        medium_conf = 0
        low_conf = 0
        conflicts = 0
        files_scanned = 0

        start_time = time.time()

        for i, classification in enumerate(valid_plugins, 1):
            repo = self.marketplace_dir / classification.name

            print(f"[{i}/{len(valid_plugins)}] Scanning: {classification.name}")
            print(f"  Files: {classification.code_files} ({classification.py_files} py, {classification.js_files} js, {classification.ts_files} ts)")

            # Get all code files
            py_files = list(repo.rglob('*.py'))
            js_files = list(repo.rglob('*.js'))
            ts_files = list(repo.rglob('*.ts'))
            all_files = py_files + js_files + ts_files

            files_scanned += len(all_files)
            plugin_detections = 0

            # Scan each file
            for code_file in all_files:
                try:
                    # Skip if it's actually a directory (edge case)
                    if not code_file.is_file():
                        continue

                    code = code_file.read_text(encoding='utf-8', errors='ignore')

                    # Skip empty files
                    if not code.strip():
                        continue

                    detections = orchestrator.scan_file(str(code_file), code)

                    plugin_detections += len(detections)
                    total_detections += len(detections)

                    for det in detections:
                        if det.confidence >= 0.90:
                            high_conf += 1
                        elif det.confidence >= 0.50:
                            medium_conf += 1
                        else:
                            low_conf += 1

                        if det.conflict_resolved:
                            conflicts += 1

                        self.scan_results.append({
                            'plugin': classification.name,
                            'file': str(code_file.relative_to(repo)),
                            'line': det.line_number,
                            'severity': det.severity,
                            'confidence': det.confidence,
                            'attack_id': det.primary_attack_id,
                            'agents': det.voting_agents,
                            'vote_count': det.vote_count
                        })

                except Exception as e:
                    print(f"    └─ Error scanning {code_file.name}: {str(e)[:50]}")

            if plugin_detections > 0:
                print(f"  └─ {plugin_detections} detections")
            else:
                print(f"  └─ ✓ Clean (no issues)")
            print()

        scan_time = time.time() - start_time

        # Get memory usage
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024

        # Create final results
        self.final_results = ScanResults(
            scan_date=time.strftime("%Y-%m-%d %H:%M:%S"),
            total_repos=len(self.classifications),
            valid_plugins_with_code=len([c for c in self.classifications if c.category == "VALID_PLUGIN_WITH_CODE"]),
            valid_plugins_no_code=len([c for c in self.classifications if c.category == "VALID_PLUGIN_NO_CODE"]),
            invalid_plugins=len([c for c in self.classifications if c.category == "INVALID_PLUGIN"]),
            non_plugins=len([c for c in self.classifications if c.category == "NON_PLUGIN"]),
            empty_repos=len([c for c in self.classifications if c.category == "EMPTY"]),
            repos_scanned=len(valid_plugins),
            files_scanned=files_scanned,
            detections_found=total_detections,
            high_confidence=high_conf,
            medium_confidence=medium_conf,
            low_confidence=low_conf,
            conflicts_resolved=conflicts,
            consensus_detections=len([d for d in self.scan_results if d['vote_count'] >= 2]),
            scan_time_seconds=scan_time,
            memory_mb=memory_mb,
            classifications=[asdict(c) for c in self.classifications],
            scanned_plugins=[asdict(c) for c in valid_plugins],
            skipped_summary={
                "valid_plugins_no_code": len([c for c in self.classifications if c.category == "VALID_PLUGIN_NO_CODE"]),
                "invalid_plugins": len([c for c in self.classifications if c.category == "INVALID_PLUGIN"]),
                "non_plugins": len([c for c in self.classifications if c.category == "NON_PLUGIN"]),
                "empty_repos": len([c for c in self.classifications if c.category == "EMPTY"])
            }
        )

        self.print_final_summary()
        self.save_results()

    def print_final_summary(self):
        """Print final clear summary"""

        r = self.final_results

        print("=" * 80)
        print("FINAL SCAN RESULTS")
        print("=" * 80)
        print()
        print(f"Scan Date: {r.scan_date}")
        print(f"Total repos in marketplace: {r.total_repos}")
        print()

        print("What we found:")
        print(f"  Valid plugins WITH code:    {r.valid_plugins_with_code:3d} → SCANNED")
        print(f"  Valid plugins WITHOUT code: {r.valid_plugins_no_code:3d} → SKIPPED (docs only)")
        print(f"  Invalid plugins:            {r.invalid_plugins:3d} → SKIPPED (no plugin.json)")
        print(f"  Non-plugin repos:           {r.non_plugins:3d} → SKIPPED (not Claude plugins)")
        print(f"  Empty repos:                {r.empty_repos:3d} → SKIPPED (no files)")
        print()

        print(f"Scanned:")
        print(f"  Plugins: {r.repos_scanned}")
        print(f"  Files:   {r.files_scanned}")
        print(f"  Time:    {r.scan_time_seconds:.1f}s")
        print(f"  Memory:  {r.memory_mb:.1f} MB")
        print()

        print(f"Detections: {r.detections_found}")
        print(f"  High confidence (≥90%):   {r.high_confidence:4d} ({r.high_confidence/max(1,r.detections_found)*100:.1f}%)")
        print(f"  Medium confidence (50-90%): {r.medium_confidence:4d} ({r.medium_confidence/max(1,r.detections_found)*100:.1f}%)")
        print(f"  Low confidence (<50%):    {r.low_confidence:4d} ({r.low_confidence/max(1,r.detections_found)*100:.1f}%)")
        print()

        print(f"Learning System:")
        print(f"  Consensus detections: {r.consensus_detections}")
        print(f"  Conflicts resolved:   {r.conflicts_resolved}")
        print()

    def save_results(self):
        """Save clear results to JSON"""

        output_dir = Path(__file__).parent.parent / "marketplace_scan_results"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "marketplace_scan_CLEAR_RESULTS.json"

        results = {
            "summary": asdict(self.final_results),
            "all_classifications": self.final_results.classifications,
            "scanned_plugins": self.final_results.scanned_plugins,
            "sample_detections": self.scan_results[:100],
            "skipped_summary": self.final_results.skipped_summary
        }

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✓ Results saved to: {output_file}")
        print()


if __name__ == "__main__":
    import sys

    marketplace_dir = Path(__file__).parent.parent / "marketplace-repos-2025"

    if len(sys.argv) > 1:
        marketplace_dir = Path(sys.argv[1])

    if not marketplace_dir.exists():
        print(f"Error: Marketplace directory not found: {marketplace_dir}")
        sys.exit(1)

    scanner = ClearMarketplaceScanner(str(marketplace_dir))

    # Step 1: Classify everything
    scanner.classify_repos()
    scanner.print_classification_summary()

    # Confirm before scanning
    print("Starting scan of valid plugins...")
    print()

    # Step 2: Scan only valid plugins
    scanner.scan_valid_plugins()

    print("\n✅ Scan complete!")
