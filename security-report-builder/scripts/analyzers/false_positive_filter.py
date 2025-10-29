#!/usr/bin/env python3
"""
Filter out false positives from security findings.
"""

import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FalsePositiveFilter:
    """Filter false positives from security findings."""

    def __init__(self):
        """Initialize false positive filter."""
        self.filtered_count = 0
        self.retained_count = 0

    def filter_findings(self, findings: List[Dict[str, Any]],
                       exclude_info: bool = True,
                       exclude_low: bool = False,
                       min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """
        Filter findings to remove false positives.

        Args:
            findings: List of analyzed findings
            exclude_info: Exclude INFO-level findings
            exclude_low: Exclude LOW-level findings
            min_confidence: Minimum confidence threshold (0-1)

        Returns:
            Filtered list of findings
        """
        filtered = []

        for finding in findings:
            if self._should_exclude(finding, exclude_info, exclude_low, min_confidence):
                self.filtered_count += 1
            else:
                filtered.append(finding)
                self.retained_count += 1

        logger.info(f"Filtered {self.filtered_count} findings, retained {self.retained_count}")

        return filtered

    def _should_exclude(self, finding: Dict[str, Any],
                       exclude_info: bool,
                       exclude_low: bool,
                       min_confidence: float) -> bool:
        """
        Determine if finding should be excluded.

        Args:
            finding: Finding to check
            exclude_info: Exclude INFO findings
            exclude_low: Exclude LOW findings
            min_confidence: Minimum confidence threshold

        Returns:
            True if should be excluded
        """
        severity = finding.get('severity', '').upper()
        context = finding.get('context_analysis', {})

        # Exclude if marked as false positive
        if context.get('is_likely_false_positive', False):
            return True

        # Exclude if confidence too low
        confidence = context.get('confidence', 1.0)
        if confidence < min_confidence:
            return True

        # Exclude INFO if requested
        if exclude_info and severity == 'INFO':
            return True

        # Exclude LOW if requested
        if exclude_low and severity == 'LOW':
            return True

        return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get filtering statistics."""
        total = self.filtered_count + self.retained_count
        return {
            'total_processed': total,
            'filtered_out': self.filtered_count,
            'retained': self.retained_count,
            'filter_rate': round((self.filtered_count / total * 100), 2) if total > 0 else 0.0
        }


def main():
    """CLI interface for testing the filter."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Filter false positives')
    parser.add_argument('findings', help='Input JSON file with analyzed findings')
    parser.add_argument('--exclude-info', action='store_true',
                       help='Exclude INFO-level findings')
    parser.add_argument('--exclude-low', action='store_true',
                       help='Exclude LOW-level findings')
    parser.add_argument('--min-confidence', type=float, default=0.7,
                       help='Minimum confidence threshold (0-1)')
    parser.add_argument('--output', help='Output file for filtered findings')

    args = parser.parse_args()

    # Load findings
    with open(args.findings, 'r') as f:
        data = json.load(f)
        findings = data.get('analyzed_findings', [])

    # Filter
    fp_filter = FalsePositiveFilter()
    filtered = fp_filter.filter_findings(
        findings,
        exclude_info=args.exclude_info,
        exclude_low=args.exclude_low,
        min_confidence=args.min_confidence
    )

    # Print statistics
    stats = fp_filter.get_statistics()
    print(f"\n=== False Positive Filtering ===")
    print(f"Total Processed: {stats['total_processed']}")
    print(f"Filtered Out: {stats['filtered_out']} ({stats['filter_rate']}%)")
    print(f"Retained: {stats['retained']}")

    # Export if requested
    if args.output:
        output_data = {
            'filtered_findings': filtered,
            'filter_statistics': stats
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nExported to {args.output}")

    return 0


if __name__ == '__main__':
    exit(main())
