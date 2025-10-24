#!/usr/bin/env python3
"""
Automated Detection Validation using Heuristics

Automatically classifies detections as TP/FP based on observable patterns:
- File paths (test/docs/examples = likely FP)
- Code context (test frameworks, pattern definitions = FP)
- Confidence levels (very low = likely FP)
- Production code paths (src/lib/app = likely TP)

This provides ground truth data for testing the learning system without
requiring manual human review of 100 detections.

Usage:
    python3 scripts/auto_validate_detections.py <results_file> [--limit N]
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import time


@dataclass
class AutoValidationResult:
    """Result of automated validation"""
    plugin: str
    file: str
    line: int
    severity: str
    confidence: float
    attack_id: str
    agents: List[str]
    vote_count: int

    # Validation data
    is_true_positive: bool
    classification_reason: str
    confidence_level: str  # "high", "medium", "low"
    reviewed_at: str


class AutomatedValidator:
    """Automated classifier using heuristics"""

    # File path patterns that indicate false positives
    FP_PATH_PATTERNS = [
        r'/tests?/',
        r'/__tests__/',
        r'\.test\.',
        r'\.spec\.',
        r'/examples?/',
        r'/docs?/',
        r'/documentation/',
        r'/fixtures?/',
        r'/mocks?/',
        r'/stubs?/',
        r'test_.*\.py$',
        r'.*_test\.py$',
    ]

    # Code patterns that indicate test/pattern code (FP)
    FP_CODE_PATTERNS = [
        r'describe\s*\(',  # Test frameworks
        r'\bit\s*\(',
        r'expect\s*\(',
        r'jest\.',
        r'mocha\.',
        r'chai\.',
        r'assert\.',
        r'@Test\b',
        r'@pytest\.',
        # Pattern definitions
        r'pattern\s*=\s*[rf]?["\']',
        r'regex\s*=\s*[rf]?["\']',
        r'detection_pattern',
        r'dangerous_pattern',
        # Security tool code
        r'def\s+detect_',
        r'def\s+scan_',
        r'class\s+\w*Scanner',
        r'class\s+\w*Detector',
    ]

    # Production code path patterns (likely TP)
    TP_PATH_PATTERNS = [
        r'/src/',
        r'/lib/',
        r'/app/',
        r'/api/',
        r'/server/',
        r'/backend/',
        r'/core/',
        r'/utils/',
        r'/services/',
        r'/routes/',
        r'/controllers/',
        r'/handlers/',
    ]

    def __init__(self, marketplace_dir: str):
        self.marketplace_dir = Path(marketplace_dir)
        self.validations: List[AutoValidationResult] = []

        # Statistics
        self.true_positives = 0
        self.false_positives = 0
        self.high_confidence_classifications = 0
        self.medium_confidence_classifications = 0
        self.low_confidence_classifications = 0

    def get_code_context(self, plugin: str, file_path: str, line_num: int, context_lines: int = 5) -> Optional[str]:
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

            return ''.join(lines[start:end])
        except Exception:
            return None

    def classify_detection(self, detection: Dict) -> Tuple[bool, str, str]:
        """
        Classify a detection as TP or FP using heuristics

        Returns:
            (is_true_positive, reason, confidence_level)
        """
        file_path = detection['file']
        confidence = detection['confidence']
        attack_id = detection['attack_id']

        # Get code context
        code_context = self.get_code_context(
            detection['plugin'],
            file_path,
            detection['line']
        )

        # --- STRONG FP INDICATORS ---

        # 1. File path indicates test/example/doc code
        for pattern in self.FP_PATH_PATTERNS:
            if re.search(pattern, file_path, re.IGNORECASE):
                return False, f"File path matches test/example pattern: {pattern}", "high"

        # 2. Very low confidence (<10%)
        if confidence < 0.10:
            return False, f"Very low confidence ({confidence:.1%}) suggests FP", "high"

        # 3. Conflict requiring review
        if attack_id == "CONFLICT:REQUIRES_HUMAN_REVIEW":
            return False, "Conflict detection - unclear case, assume FP", "medium"

        # 4. Code context shows test framework patterns
        if code_context:
            for pattern in self.FP_CODE_PATTERNS:
                if re.search(pattern, code_context, re.IGNORECASE):
                    return False, f"Code matches test/pattern definition: {pattern}", "high"

        # --- STRONG TP INDICATORS ---

        # 5. Production code path with high confidence
        for pattern in self.TP_PATH_PATTERNS:
            if re.search(pattern, file_path, re.IGNORECASE) and confidence >= 0.80:
                return True, f"Production code path with high confidence ({confidence:.1%})", "high"

        # 6. Very high confidence (≥95%) in non-test file
        if confidence >= 0.95:
            return True, f"Very high confidence ({confidence:.1%}) in non-test file", "high"

        # --- MEDIUM CONFIDENCE HEURISTICS ---

        # 7. Moderate confidence in production-looking path
        for pattern in self.TP_PATH_PATTERNS:
            if re.search(pattern, file_path, re.IGNORECASE) and confidence >= 0.50:
                return True, f"Production code path with moderate confidence ({confidence:.1%})", "medium"

        # 8. Moderate confidence (50-80%) - assume TP unless proven otherwise
        if 0.50 <= confidence < 0.80:
            return True, f"Moderate confidence ({confidence:.1%}), no clear FP indicators", "medium"

        # --- DEFAULT: LOW CONFIDENCE FP ---

        # If we get here, confidence is low and no clear indicators
        return False, f"Low confidence ({confidence:.1%}), no clear TP indicators", "low"

    def validate_detections(self, results_file: str, limit: Optional[int] = None):
        """Automatically validate detections"""

        print("=" * 80)
        print("AUTOMATED DETECTION VALIDATION")
        print("=" * 80)
        print()

        # Load detections
        with open(results_file) as f:
            data = json.load(f)

        detections = data.get('sample_detections', [])

        if limit:
            detections = detections[:limit]

        total = len(detections)

        print(f"Detections to validate: {total}")
        print(f"Results file: {results_file}")
        print(f"Marketplace: {self.marketplace_dir}")
        print()
        print("Using heuristics to classify as TP/FP...")
        print()

        # Classify each detection
        for i, detection in enumerate(detections, 1):
            is_tp, reason, conf_level = self.classify_detection(detection)

            # Record validation
            validation = AutoValidationResult(
                plugin=detection['plugin'],
                file=detection['file'],
                line=detection['line'],
                severity=detection['severity'],
                confidence=detection['confidence'],
                attack_id=detection['attack_id'],
                agents=detection['agents'],
                vote_count=detection['vote_count'],
                is_true_positive=is_tp,
                classification_reason=reason,
                confidence_level=conf_level,
                reviewed_at=time.strftime("%Y-%m-%d %H:%M:%S")
            )

            self.validations.append(validation)

            # Update stats
            if is_tp:
                self.true_positives += 1
            else:
                self.false_positives += 1

            if conf_level == "high":
                self.high_confidence_classifications += 1
            elif conf_level == "medium":
                self.medium_confidence_classifications += 1
            else:
                self.low_confidence_classifications += 1

            # Show progress
            if i % 10 == 0:
                print(f"  Classified {i}/{total} detections...")

        print(f"  ✓ Classified all {total} detections")
        print()

        # Show summary
        self.show_summary()

        # Save results
        self.save_results()

    def show_summary(self):
        """Show validation summary"""
        total = len(self.validations)

        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print()
        print(f"Total classified:    {total}")
        print(f"True Positives:      {self.true_positives} ({self.true_positives/total*100:.1f}%)")
        print(f"False Positives:     {self.false_positives} ({self.false_positives/total*100:.1f}%)")
        print()

        if total > 0:
            precision = self.true_positives / total if total > 0 else 0
            print(f"Precision: {precision:.1%}")
            print()

        print("Classification Confidence:")
        print(f"  High:   {self.high_confidence_classifications} ({self.high_confidence_classifications/total*100:.1f}%)")
        print(f"  Medium: {self.medium_confidence_classifications} ({self.medium_confidence_classifications/total*100:.1f}%)")
        print(f"  Low:    {self.low_confidence_classifications} ({self.low_confidence_classifications/total*100:.1f}%)")
        print()

        # Show example classifications
        print("Example Classifications:")
        print()

        # Show 5 TPs
        tps = [v for v in self.validations if v.is_true_positive][:5]
        if tps:
            print("True Positives (sample):")
            for i, v in enumerate(tps, 1):
                print(f"  {i}. {v.file}:{v.line}")
                print(f"     Reason: {v.classification_reason}")
                print()

        # Show 5 FPs
        fps = [v for v in self.validations if not v.is_true_positive][:5]
        if fps:
            print("False Positives (sample):")
            for i, v in enumerate(fps, 1):
                print(f"  {i}. {v.file}:{v.line}")
                print(f"     Reason: {v.classification_reason}")
                print()

    def save_results(self):
        """Save validation results"""
        output_dir = Path(__file__).parent.parent / "validation_results"
        output_dir.mkdir(exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"auto_validation_results_{timestamp}.json"

        data = {
            "validation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "validation_method": "automated_heuristics",
            "detections_classified": len(self.validations),
            "statistics": {
                "true_positives": self.true_positives,
                "false_positives": self.false_positives,
                "precision": self.true_positives / max(1, len(self.validations)),
                "high_confidence_classifications": self.high_confidence_classifications,
                "medium_confidence_classifications": self.medium_confidence_classifications,
                "low_confidence_classifications": self.low_confidence_classifications
            },
            "validations": [asdict(v) for v in self.validations]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Results saved to: {output_file}")
        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically validate security detections using heuristics"
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
        default=100,
        help="Limit number of detections to validate (default: 100)"
    )

    args = parser.parse_args()

    # Determine marketplace directory
    if args.marketplace:
        marketplace_dir = args.marketplace
    else:
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
    validator = AutomatedValidator(marketplace_dir=str(marketplace_dir))
    validator.validate_detections(args.results_file, args.limit)


if __name__ == "__main__":
    main()
