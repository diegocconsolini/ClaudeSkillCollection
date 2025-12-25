#!/usr/bin/env python3
"""
Interactive Validation Tool - Manual Review of Security Detections

Allows human reviewers to validate detections and provide feedback
to improve the learning system's accuracy.

Usage:
    python3 scripts/validate_detections.py <results_file> [--limit N]

Example:
    python3 scripts/validate_detections.py marketplace_scan_results/marketplace_scan_CLEAR_RESULTS.json --limit 100
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class ValidationResult:
    """Result of validating a detection"""
    plugin: str
    file: str
    line: int
    severity: str
    confidence: float
    attack_id: str
    agents: List[str]
    vote_count: int

    # Validation data
    is_true_positive: Optional[bool]  # True = TP, False = FP, None = Skipped
    reviewer_notes: str
    reviewed_at: str


class DetectionValidator:
    """Interactive CLI for validating security detections"""

    def __init__(self, results_file: str, marketplace_dir: str, limit: Optional[int] = None):
        self.results_file = Path(results_file)
        self.marketplace_dir = Path(marketplace_dir)
        self.limit = limit

        # Results
        self.validations: List[ValidationResult] = []
        self.current_index = 0

        # Statistics
        self.true_positives = 0
        self.false_positives = 0
        self.skipped = 0

    def load_detections(self) -> List[Dict]:
        """Load detections from scan results"""
        with open(self.results_file) as f:
            data = json.load(f)

        # Get sample detections (or all if available)
        detections = data.get('sample_detections', [])

        if self.limit:
            detections = detections[:self.limit]

        return detections

    def get_code_context(self, plugin: str, file_path: str, line_num: int, context_lines: int = 2) -> Optional[List[str]]:
        """Read code file and extract context around the detection line"""
        full_path = self.marketplace_dir / plugin / file_path

        if not full_path.exists():
            return None

        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Get context (line_num is 1-indexed)
            start = max(0, line_num - context_lines - 1)
            end = min(len(lines), line_num + context_lines)

            context = []
            for i in range(start, end):
                line_marker = " >>> " if i == line_num - 1 else "     "
                context.append(f"{line_marker}{i+1:4d} | {lines[i].rstrip()}")

            return context
        except Exception as e:
            return None

    def show_detection(self, detection: Dict, index: int, total: int):
        """Display a detection with context for review"""
        print("\n" + "=" * 80)
        print(f"DETECTION {index + 1} of {total}")
        print("=" * 80)
        print()

        # Basic info
        print(f"Plugin:     {detection['plugin']}")
        print(f"File:       {detection['file']}")
        print(f"Line:       {detection['line']}")
        print(f"Severity:   {detection['severity']}")
        print(f"Confidence: {detection['confidence']:.1%}")
        print(f"Attack ID:  {detection['attack_id']}")
        print(f"Agents:     {', '.join(set(detection['agents']))} ({detection['vote_count']} votes)")
        print()

        # Code context
        context = self.get_code_context(
            detection['plugin'],
            detection['file'],
            detection['line']
        )

        if context:
            print("Code Context:")
            print("-" * 80)
            for line in context:
                print(line)
            print("-" * 80)
        else:
            print("Code Context: [Unable to load file]")
        print()

    def get_user_input(self) -> tuple[Optional[bool], str]:
        """Get validation input from user

        Returns:
            (is_true_positive, notes)
            - is_true_positive: True (TP), False (FP), None (Skip)
            - notes: reviewer notes
        """
        while True:
            print("Is this a TRUE security issue?")
            print("  [T] True Positive  - Real security vulnerability")
            print("  [F] False Positive - Safe code or test/pattern code")
            print("  [S] Skip          - Unsure, need more context")
            print("  [Q] Quit          - Save progress and exit")
            print()

            choice = input("Your choice [T/F/S/Q]: ").strip().upper()

            if choice == 'Q':
                return None, "quit"
            elif choice == 'T':
                notes = input("Notes (optional, Enter to skip): ").strip()
                return True, notes or "Confirmed true positive"
            elif choice == 'F':
                notes = input("Why is this false positive? (optional): ").strip()
                return False, notes or "False positive"
            elif choice == 'S':
                notes = input("Why skipping? (optional): ").strip()
                return None, notes or "Skipped - needs review"
            else:
                print("Invalid choice. Please enter T, F, S, or Q.")

    def validate_detections(self):
        """Main validation loop"""
        detections = self.load_detections()
        total = len(detections)

        print(f"\n{'=' * 80}")
        print(f"DETECTION VALIDATION TOOL")
        print(f"{'=' * 80}")
        print(f"Total detections to review: {total}")
        print(f"Results file: {self.results_file}")
        print(f"Marketplace: {self.marketplace_dir}")
        print()
        print("Let's begin! Review each detection and mark as TP/FP.")
        print()

        for i, detection in enumerate(detections):
            self.current_index = i

            # Show detection
            self.show_detection(detection, i, total)

            # Get validation
            is_tp, notes = self.get_user_input()

            if notes == "quit":
                print("\nSaving progress and exiting...")
                break

            # Record validation
            validation = ValidationResult(
                plugin=detection['plugin'],
                file=detection['file'],
                line=detection['line'],
                severity=detection['severity'],
                confidence=detection['confidence'],
                attack_id=detection['attack_id'],
                agents=detection['agents'],
                vote_count=detection['vote_count'],
                is_true_positive=is_tp,
                reviewer_notes=notes,
                reviewed_at=time.strftime("%Y-%m-%d %H:%M:%S")
            )

            self.validations.append(validation)

            # Update stats
            if is_tp is True:
                self.true_positives += 1
            elif is_tp is False:
                self.false_positives += 1
            else:
                self.skipped += 1

            # Show progress
            print(f"\n✓ Validation recorded ({self.true_positives} TP, {self.false_positives} FP, {self.skipped} skipped)")

            # Save progress periodically (every 10 detections)
            if (i + 1) % 10 == 0:
                self.save_progress(f"validation_progress_{i+1}.json")
                print(f"  └─ Progress saved to validation_progress_{i+1}.json")

        # Final summary
        self.show_final_summary()

        # Save final results
        self.save_results()

    def show_final_summary(self):
        """Show validation summary"""
        total = len(self.validations)

        print(f"\n{'=' * 80}")
        print("VALIDATION SUMMARY")
        print(f"{'=' * 80}")
        print(f"Total reviewed:      {total}")
        print(f"True Positives:      {self.true_positives} ({self.true_positives/max(1,total)*100:.1f}%)")
        print(f"False Positives:     {self.false_positives} ({self.false_positives/max(1,total)*100:.1f}%)")
        print(f"Skipped:             {self.skipped} ({self.skipped/max(1,total)*100:.1f}%)")
        print()

        if total > 0:
            # Calculate precision (TP / (TP + FP))
            validated = self.true_positives + self.false_positives
            if validated > 0:
                precision = self.true_positives / validated
                print(f"Precision: {precision:.1%} (based on {validated} validated detections)")
                print()

    def save_progress(self, filename: str):
        """Save progress to file"""
        output_dir = Path(__file__).parent.parent / "validation_results"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / filename

        data = {
            "validation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results_file": str(self.results_file),
            "detections_reviewed": len(self.validations),
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "skipped": self.skipped,
            "validations": [asdict(v) for v in self.validations]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def save_results(self):
        """Save final validation results"""
        output_dir = Path(__file__).parent.parent / "validation_results"
        output_dir.mkdir(exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"validation_results_{timestamp}.json"

        data = {
            "validation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results_file": str(self.results_file),
            "detections_reviewed": len(self.validations),
            "statistics": {
                "true_positives": self.true_positives,
                "false_positives": self.false_positives,
                "skipped": self.skipped,
                "precision": self.true_positives / max(1, self.true_positives + self.false_positives)
            },
            "validations": [asdict(v) for v in self.validations]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n✓ Results saved to: {output_file}")
        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Interactive tool for validating security detections"
    )
    parser.add_argument(
        "results_file",
        help="Path to scan results JSON file"
    )
    parser.add_argument(
        "--marketplace",
        default=None,
        help="Path to marketplace repos directory (default: ../marketplace-repos-2025)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of detections to review (default: all)"
    )

    args = parser.parse_args()

    # Determine marketplace directory
    if args.marketplace:
        marketplace_dir = args.marketplace
    else:
        # Default to marketplace-repos-2025 in parent directory
        script_dir = Path(__file__).parent
        marketplace_dir = script_dir.parent / "marketplace-repos-2025"

    # Check files exist
    if not Path(args.results_file).exists():
        print(f"Error: Results file not found: {args.results_file}")
        sys.exit(1)

    if not Path(marketplace_dir).exists():
        print(f"Error: Marketplace directory not found: {marketplace_dir}")
        print(f"Use --marketplace to specify the correct path")
        sys.exit(1)

    # Create validator and run
    validator = DetectionValidator(
        results_file=args.results_file,
        marketplace_dir=str(marketplace_dir),
        limit=args.limit
    )

    try:
        validator.validate_detections()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Saving progress...")
        validator.show_final_summary()
        validator.save_results()
        print("Progress saved. You can resume later.")


if __name__ == "__main__":
    main()
