#!/usr/bin/env python3
"""
Apply Validation Feedback to Cache

Takes validation results (TP/FP labels from human review) and feeds them
back into the AccuracyCache to improve the learning system.

Usage:
    python3 scripts/apply_validations_to_cache.py <validation_results.json>

Example:
    python3 scripts/apply_validations_to_cache.py validation_results/validation_results_20251024_123456.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from accuracy_cache import AccuracyCache


def apply_validations(validation_file: str, cache_file: str = ".cache/accuracy_cache.json"):
    """Apply validation results to the cache"""

    print("=" * 80)
    print("APPLYING VALIDATION FEEDBACK TO CACHE")
    print("=" * 80)
    print()

    # Load validation results
    print(f"Loading validation results from: {validation_file}")
    with open(validation_file) as f:
        data = json.load(f)

    validations = data.get('validations', [])
    total = len(validations)

    print(f"  ✓ Loaded {total} validations")
    print()

    # Load or create cache
    cache = AccuracyCache()
    cache_path = Path(cache_file)

    if cache_path.exists():
        print(f"Loading existing cache: {cache_file}")
        if cache.load_from_disk(cache_file):
            print("  ✓ Cache loaded successfully")
        else:
            print("  ⚠ Failed to load cache, starting fresh")
    else:
        print(f"Creating new cache: {cache_file}")

    print()

    # Apply each validation
    print("Applying validations...")
    print()

    tp_count = 0
    fp_count = 0
    skipped_count = 0

    for i, validation in enumerate(validations, 1):
        is_tp = validation.get('is_true_positive')

        # Skip if validation was skipped
        if is_tp is None:
            skipped_count += 1
            continue

        # Extract detection info
        plugin = validation['plugin']
        file_path = validation['file']
        line = validation['line']
        severity = validation['severity']
        confidence = validation['confidence']
        attack_id = validation['attack_id']
        agents = validation['agents']

        # Determine file type
        file_type = Path(file_path).suffix or '.unknown'

        # Record the detection with ground truth
        import hashlib
        file_hash = hashlib.md5(f"{plugin}/{file_path}".encode()).hexdigest()
        agent_id = agents[0] if agents else "unknown"

        cache.store_detection(
            agent_id=agent_id,
            pattern=agent_id,  # Use agent as pattern
            file_hash=file_hash,
            file_type=file_type,
            confidence=confidence,
            severity=severity,
            context="",  # No context available from validation data
            attack_id=attack_id,
            atlas_id=None,
            is_true_positive=is_tp,
            validated_by="automated_heuristics"
        )

        if is_tp:
            tp_count += 1
        else:
            fp_count += 1

        # Show progress
        if i % 10 == 0:
            print(f"  Processed {i}/{total} validations...")

    print(f"  ✓ Processed all {total} validations")
    print()

    # Show statistics
    print("Validation Statistics:")
    print(f"  True Positives:  {tp_count}")
    print(f"  False Positives: {fp_count}")
    print(f"  Skipped:         {skipped_count}")
    print()

    if tp_count + fp_count > 0:
        precision = tp_count / (tp_count + fp_count)
        print(f"  Overall Precision: {precision:.1%}")
        print()

    # Save updated cache
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache.save_to_disk(cache_file)

    print(f"✓ Updated cache saved to: {cache_file}")
    print()

    # Show cache statistics
    print("Cache Statistics:")
    print(f"  Agent statistics:        {len(cache.agent_stats)}")
    print(f"  File type correlations:  {len(cache.file_type_correlations)}")
    print(f"  Total detections:        {len(cache.detections)}")
    print()

    # Show top patterns by accuracy
    print("Top Patterns by Precision:")
    print()

    # Calculate precision for each agent
    agent_precision = {}
    for agent_id, stats in cache.agent_stats.items():
        total_detected = stats.true_positives + stats.false_positives
        if total_detected > 0:
            precision = stats.true_positives / total_detected
            agent_precision[agent_id] = (precision, stats.true_positives, stats.false_positives)

    # Sort by precision
    sorted_agents = sorted(agent_precision.items(), key=lambda x: x[1][0], reverse=True)

    for i, (agent_id, (precision, tp, fp)) in enumerate(sorted_agents[:10], 1):
        print(f"  {i:2d}. {agent_id:30s} {precision:6.1%} ({tp} TP, {fp} FP)")

    print()
    print("=" * 80)
    print("VALIDATION FEEDBACK APPLIED SUCCESSFULLY")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Re-run the marketplace scan:")
    print("     python3 scripts/scan_marketplace_clear.py")
    print()
    print("  2. The scanner will now use the validated accuracy data to:")
    print("     - Adjust confidence scores using Bayesian updating")
    print("     - Better distinguish TP from FP patterns")
    print("     - Improve overall precision")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply validation feedback to the learning cache"
    )
    parser.add_argument(
        "validation_file",
        help="Path to validation results JSON file"
    )
    parser.add_argument(
        "--cache-file",
        default=".cache/accuracy_cache.json",
        help="Path to cache file (default: .cache/accuracy_cache.json)"
    )

    args = parser.parse_args()

    # Check file exists
    if not Path(args.validation_file).exists():
        print(f"Error: Validation file not found: {args.validation_file}")
        sys.exit(1)

    apply_validations(args.validation_file, args.cache_file)


if __name__ == "__main__":
    main()
