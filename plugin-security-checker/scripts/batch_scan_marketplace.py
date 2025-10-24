#!/usr/bin/env python3
"""
Batch Marketplace Scanner with Learning System Testing

Scans 300+ repos in blocks to:
1. Test learning system performance
2. Track consensus accuracy
3. Monitor memory usage
4. Identify patterns across marketplace
5. Generate comprehensive threat intelligence
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict

from intelligent_orchestrator import IntelligentOrchestrator


@dataclass
class BlockScanResults:
    """Results from scanning a block of repos"""
    block_number: int
    repos_scanned: int
    total_files: int
    total_detections: int
    high_confidence: int      # ≥90%
    medium_confidence: int    # 50-90%
    low_confidence: int       # <50%
    conflicts: int
    memory_mb: float
    scan_time_seconds: float
    top_patterns: List[Dict]  # Most common dangerous patterns


class MarketplaceBatchScanner:
    """Batch scanner with learning progress tracking"""

    def __init__(self, marketplace_dir: str, block_size: int = 25):
        self.marketplace_dir = Path(marketplace_dir)
        self.block_size = block_size
        self.patterns_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded.json"

        # Results tracking
        self.blocks_results: List[BlockScanResults] = []
        self.all_detections: List[Dict] = []

        # Learning metrics
        self.pattern_frequency: Dict[str, int] = {}
        self.attack_technique_frequency: Dict[str, int] = {}

    def scan_marketplace(self):
        """Scan all repos in blocks"""

        # Get all repo directories
        repos = sorted([d for d in self.marketplace_dir.iterdir() if d.is_dir()])
        total_repos = len(repos)

        print("=" * 80)
        print(f"MARKETPLACE BATCH SCAN")
        print("=" * 80)
        print(f"Total repos: {total_repos}")
        print(f"Block size: {self.block_size}")
        print(f"Total blocks: {(total_repos + self.block_size - 1) // self.block_size}")
        print()

        # Scan in blocks
        for block_num, i in enumerate(range(0, total_repos, self.block_size), 1):
            block_repos = repos[i:i + self.block_size]

            print(f"\n{'=' * 80}")
            print(f"BLOCK {block_num}: Repos {i+1}-{min(i+self.block_size, total_repos)} of {total_repos}")
            print(f"{'=' * 80}\n")

            block_result = self.scan_block(block_num, block_repos)
            self.blocks_results.append(block_result)

            # Show block summary
            self.print_block_summary(block_result)

            # Pause after each block for review
            if block_num < ((total_repos + self.block_size - 1) // self.block_size):
                print(f"\n{'─' * 80}")
                print(f"Block {block_num} complete. Press Enter to continue to next block...")
                print(f"Or type 'stop' to pause and review results so far.")
                print(f"{'─' * 80}")

                # Save results so far
                self.save_results(f"marketplace_scan_blocks_1-{block_num}.json")

                user_input = input("Continue? [Enter/stop]: ").strip().lower()
                if user_input == 'stop':
                    print("\nScan paused. Results saved.")
                    break

        # Final summary
        print(f"\n{'=' * 80}")
        print("FINAL SUMMARY")
        print(f"{'=' * 80}\n")
        self.print_final_summary()

        # Save complete results
        self.save_results("marketplace_scan_complete.json")

    def scan_block(self, block_num: int, repos: List[Path]) -> BlockScanResults:
        """Scan a block of repos"""

        start_time = time.time()
        total_files = 0
        total_detections = 0
        high_conf = 0
        medium_conf = 0
        low_conf = 0
        conflicts = 0

        # Initialize orchestrator for this block
        orchestrator = IntelligentOrchestrator(
            patterns_file=str(self.patterns_file),
            max_memory_mb=500,
            enable_adaptive_routing=True
        )

        for repo in repos:
            repo_name = repo.name
            print(f"  Scanning: {repo_name}...")

            # Find all code files
            py_files = list(repo.rglob('*.py'))
            js_files = list(repo.rglob('*.js'))
            ts_files = list(repo.rglob('*.ts'))

            all_files = py_files + js_files + ts_files
            total_files += len(all_files)

            if len(all_files) == 0:
                print(f"    └─ No code files")
                continue

            print(f"    └─ {len(all_files)} files ({len(py_files)} py, {len(js_files)} js, {len(ts_files)} ts)")

            # Scan each file
            repo_detections = 0
            for code_file in all_files:
                try:
                    code = code_file.read_text(encoding='utf-8', errors='ignore')
                    detections = orchestrator.scan_file(str(code_file), code)

                    repo_detections += len(detections)
                    total_detections += len(detections)

                    # Track confidence distribution
                    for det in detections:
                        if det.confidence >= 0.90:
                            high_conf += 1
                        elif det.confidence >= 0.50:
                            medium_conf += 1
                        else:
                            low_conf += 1

                        if det.conflict_resolved:
                            conflicts += 1

                        # Track patterns
                        pattern_key = f"{det.severity}:{det.primary_attack_id}"
                        self.pattern_frequency[pattern_key] = self.pattern_frequency.get(pattern_key, 0) + 1

                        if det.primary_attack_id:
                            self.attack_technique_frequency[det.primary_attack_id] = \
                                self.attack_technique_frequency.get(det.primary_attack_id, 0) + 1

                        # Store detection
                        self.all_detections.append({
                            'repo': repo_name,
                            'file': str(code_file.relative_to(repo)),
                            'line': det.line_number,
                            'severity': det.severity,
                            'confidence': det.confidence,
                            'attack_id': det.primary_attack_id,
                            'agents': det.voting_agents,
                            'vote_count': det.vote_count
                        })

                except Exception as e:
                    print(f"      └─ Error scanning {code_file.name}: {str(e)[:50]}")

            if repo_detections > 0:
                print(f"      └─ {repo_detections} detections")

        # Get top patterns
        top_patterns = sorted(
            self.pattern_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_patterns_list = [
            {"pattern": k, "count": v} for k, v in top_patterns
        ]

        # Get memory usage
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024

        scan_time = time.time() - start_time

        return BlockScanResults(
            block_number=block_num,
            repos_scanned=len(repos),
            total_files=total_files,
            total_detections=total_detections,
            high_confidence=high_conf,
            medium_confidence=medium_conf,
            low_confidence=low_conf,
            conflicts=conflicts,
            memory_mb=memory_mb,
            scan_time_seconds=scan_time,
            top_patterns=top_patterns_list
        )

    def print_block_summary(self, result: BlockScanResults):
        """Print summary for a block"""
        print(f"\nBlock {result.block_number} Summary:")
        print(f"  Repos scanned: {result.repos_scanned}")
        print(f"  Files scanned: {result.total_files}")
        print(f"  Total detections: {result.total_detections}")
        print(f"  ")
        print(f"  Confidence Distribution:")
        print(f"    High (≥90%):   {result.high_confidence:4d} ({result.high_confidence/max(1,result.total_detections)*100:.1f}%)")
        print(f"    Medium (50-90%): {result.medium_confidence:4d} ({result.medium_confidence/max(1,result.total_detections)*100:.1f}%)")
        print(f"    Low (<50%):    {result.low_confidence:4d} ({result.low_confidence/max(1,result.total_detections)*100:.1f}%)")
        print(f"  ")
        print(f"  Conflicts resolved: {result.conflicts}")
        print(f"  Memory usage: {result.memory_mb:.1f} MB")
        print(f"  Scan time: {result.scan_time_seconds:.1f}s")
        print(f"  ")
        print(f"  Top Patterns:")
        for i, pattern in enumerate(result.top_patterns, 1):
            print(f"    {i}. {pattern['pattern']}: {pattern['count']} detections")

    def print_final_summary(self):
        """Print final summary across all blocks"""
        total_repos = sum(b.repos_scanned for b in self.blocks_results)
        total_files = sum(b.total_files for b in self.blocks_results)
        total_detections = sum(b.total_detections for b in self.blocks_results)
        total_high = sum(b.high_confidence for b in self.blocks_results)
        total_medium = sum(b.medium_confidence for b in self.blocks_results)
        total_low = sum(b.low_confidence for b in self.blocks_results)
        total_conflicts = sum(b.conflicts for b in self.blocks_results)
        avg_memory = sum(b.memory_mb for b in self.blocks_results) / len(self.blocks_results)
        total_time = sum(b.scan_time_seconds for b in self.blocks_results)

        print(f"Blocks scanned: {len(self.blocks_results)}")
        print(f"Total repos: {total_repos}")
        print(f"Total files: {total_files}")
        print(f"Total detections: {total_detections}")
        print()
        print("Confidence Distribution:")
        print(f"  High (≥90%):     {total_high:5d} ({total_high/max(1,total_detections)*100:.1f}%)")
        print(f"  Medium (50-90%): {total_medium:5d} ({total_medium/max(1,total_detections)*100:.1f}%)")
        print(f"  Low (<50%):      {total_low:5d} ({total_low/max(1,total_detections)*100:.1f}%)")
        print()
        print(f"Conflicts resolved: {total_conflicts}")
        print(f"Average memory: {avg_memory:.1f} MB")
        print(f"Total scan time: {total_time/60:.1f} minutes")
        print()

        # Top attack techniques
        print("Top 10 Attack Techniques Found:")
        top_attacks = sorted(
            self.attack_technique_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        for i, (attack_id, count) in enumerate(top_attacks, 1):
            print(f"  {i:2d}. {attack_id}: {count} detections")

    def save_results(self, filename: str):
        """Save results to JSON"""
        output_dir = Path(__file__).parent.parent / "marketplace_scan_results"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / filename

        results = {
            "scan_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_blocks": len(self.blocks_results),
            "blocks": [asdict(b) for b in self.blocks_results],
            "pattern_frequency": self.pattern_frequency,
            "attack_technique_frequency": self.attack_technique_frequency,
            "sample_detections": self.all_detections[:100]  # First 100 for review
        }

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n✓ Results saved to: {output_file}")


if __name__ == "__main__":
    import sys

    # Default marketplace directory
    marketplace_dir = Path(__file__).parent.parent / "marketplace-repos-2025"

    if len(sys.argv) > 1:
        marketplace_dir = Path(sys.argv[1])

    if not marketplace_dir.exists():
        print(f"Error: Marketplace directory not found: {marketplace_dir}")
        sys.exit(1)

    # Create scanner with 25 repos per block
    scanner = MarketplaceBatchScanner(str(marketplace_dir), block_size=25)

    print("Starting marketplace batch scan...")
    print("You will be prompted after each block to review results.")
    print("Press Enter to continue or type 'stop' to pause.\n")

    scanner.scan_marketplace()

    print("\nScan complete!")
