#!/usr/bin/env python3
"""
Context-aware analysis to reduce false positives in security findings.
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContextAnalyzer:
    """Analyze security findings with context to reduce false positives."""

    def __init__(self, rules_file: Optional[Path] = None):
        """
        Initialize context analyzer.

        Args:
            rules_file: Path to severity rules JSON
        """
        self.rules = {}
        self.severity_levels = {}
        self.false_positive_indicators = []

        if rules_file:
            self.load_rules(rules_file)

    def load_rules(self, rules_file: Path) -> None:
        """
        Load context-aware severity adjustment rules.

        Args:
            rules_file: Path to rules JSON
        """
        if not rules_file.exists():
            logger.warning(f"Rules file not found: {rules_file}")
            return

        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.rules = data.get('rules', {})
            self.severity_levels = data.get('severity_levels', {})
            self.false_positive_indicators = data.get('false_positive_indicators', [])

            logger.info(f"Loaded {len(self.rules)} rule categories")

        except Exception as e:
            logger.error(f"Error loading rules: {e}")

    def analyze_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a finding and adjust severity based on context.

        Args:
            finding: Security finding dictionary

        Returns:
            Finding with adjusted severity and context notes
        """
        analyzed = finding.copy()

        # Store original severity
        original_severity = finding.get('severity', 'UNKNOWN')
        analyzed['original_severity'] = original_severity

        # Get category and code snippet
        category = finding.get('category', '').lower()
        code_snippet = finding.get('code_snippet', '')
        description = finding.get('description', '')

        # Check if we have rules for this category
        if category not in self.rules:
            # No specific rules, return as-is
            analyzed['context_analysis'] = {
                'adjusted': False,
                'reason': f'No context rules for category: {category}'
            }
            return analyzed

        rule_set = self.rules[category]

        # Try pattern-based matching
        adjusted_severity = None
        match_reason = None
        confidence = 0.0

        for pattern_rule in rule_set.get('patterns', []):
            pattern = pattern_rule['pattern']

            # Check if pattern matches code snippet
            if re.search(pattern, code_snippet, re.IGNORECASE | re.MULTILINE):
                adjusted_severity = pattern_rule['adjusted_severity']
                match_reason = pattern_rule['reason']
                confidence = pattern_rule.get('confidence', 0.8)
                break

        # If pattern matched, apply adjustment
        if adjusted_severity:
            analyzed['severity'] = adjusted_severity
            analyzed['context_analysis'] = {
                'adjusted': True,
                'original_severity': original_severity,
                'adjusted_severity': adjusted_severity,
                'reason': match_reason,
                'confidence': confidence,
                'is_likely_false_positive': self._is_false_positive(
                    original_severity, adjusted_severity
                )
            }
        else:
            # No pattern match, keep original
            analyzed['context_analysis'] = {
                'adjusted': False,
                'reason': 'No matching context pattern'
            }

        # Check for plugin type context
        plugin_name = finding.get('plugin_name', '')
        plugin_type = self._infer_plugin_type(plugin_name, code_snippet)

        if plugin_type:
            analyzed['plugin_type'] = plugin_type
            analyzed['context_analysis']['plugin_type'] = plugin_type

            # Apply plugin type modifiers
            if 'plugin_type_context' in rule_set:
                self._apply_plugin_context(analyzed, rule_set['plugin_type_context'], plugin_type)

        return analyzed

    def _infer_plugin_type(self, plugin_name: str, code_snippet: str) -> Optional[str]:
        """
        Infer plugin type from name and code.

        Args:
            plugin_name: Plugin name
            code_snippet: Code snippet from finding

        Returns:
            Plugin type or None
        """
        # Check for web UI indicators
        web_ui_patterns = [
            r'<html',
            r'<div',
            r'<script',
            r'document\.',
            r'window\.',
            r'getElementById',
            r'querySelector'
        ]

        for pattern in web_ui_patterns:
            if re.search(pattern, code_snippet, re.IGNORECASE):
                return 'web_ui_plugin'

        # Check plugin name for CLI indicators
        cli_indicators = ['cli', 'command', 'terminal', 'bash', 'shell']
        if any(ind in plugin_name.lower() for ind in cli_indicators):
            return 'cli_only_plugin'

        return None

    def _apply_plugin_context(self, finding: Dict[str, Any],
                             context_rules: Dict[str, Any],
                             plugin_type: str) -> None:
        """
        Apply plugin type context modifiers.

        Args:
            finding: Finding to modify (modified in-place)
            context_rules: Plugin context rules
            plugin_type: Inferred plugin type
        """
        if plugin_type not in context_rules:
            return

        modifier_rule = context_rules[plugin_type]
        severity_modifier = modifier_rule.get('severity_modifier', 0)
        reason = modifier_rule.get('reason', '')

        if severity_modifier != 0:
            # Adjust severity level
            current_severity = finding['severity']
            new_severity = self._adjust_severity_level(current_severity, severity_modifier)

            if new_severity != current_severity:
                finding['severity'] = new_severity
                finding['context_analysis']['adjusted'] = True
                finding['context_analysis']['plugin_context_applied'] = True
                finding['context_analysis']['plugin_context_reason'] = reason

    def _adjust_severity_level(self, current: str, modifier: int) -> str:
        """
        Adjust severity level by modifier.

        Args:
            current: Current severity
            modifier: +/- adjustment (e.g., -1 to downgrade)

        Returns:
            Adjusted severity
        """
        levels = ['INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        try:
            current_index = levels.index(current.upper())
            new_index = max(0, min(len(levels) - 1, current_index + modifier))
            return levels[new_index]
        except ValueError:
            return current

    def _is_false_positive(self, original: str, adjusted: str) -> bool:
        """
        Determine if adjustment indicates a false positive.

        Args:
            original: Original severity
            adjusted: Adjusted severity

        Returns:
            True if likely false positive
        """
        severity_scores = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'INFO': 1, 'UNKNOWN': 0}

        original_score = severity_scores.get(original.upper(), 0)
        adjusted_score = severity_scores.get(adjusted.upper(), 0)

        # If downgraded by 2+ levels, likely false positive
        return (original_score - adjusted_score) >= 2

    def analyze_batch(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze batch of findings and provide statistics.

        Args:
            findings: List of findings

        Returns:
            Analysis results with statistics
        """
        analyzed_findings = []
        stats = {
            'total_findings': len(findings),
            'adjusted_count': 0,
            'false_positive_count': 0,
            'severity_changes': {
                'CRITICAL_to_HIGH': 0,
                'CRITICAL_to_MEDIUM': 0,
                'CRITICAL_to_LOW': 0,
                'CRITICAL_to_INFO': 0,
                'HIGH_to_MEDIUM': 0,
                'HIGH_to_LOW': 0,
                'HIGH_to_INFO': 0,
                'MEDIUM_to_LOW': 0,
                'MEDIUM_to_INFO': 0
            },
            'original_distribution': {},
            'adjusted_distribution': {}
        }

        for finding in findings:
            analyzed = self.analyze_finding(finding)
            analyzed_findings.append(analyzed)

            # Track statistics
            original = analyzed.get('original_severity', 'UNKNOWN')
            current = analyzed.get('severity', 'UNKNOWN')

            # Count by original severity
            stats['original_distribution'][original] = \
                stats['original_distribution'].get(original, 0) + 1

            # Count by adjusted severity
            stats['adjusted_distribution'][current] = \
                stats['adjusted_distribution'].get(current, 0) + 1

            # Track adjustments
            if analyzed.get('context_analysis', {}).get('adjusted', False):
                stats['adjusted_count'] += 1

                # Track severity changes
                change_key = f"{original}_to_{current}"
                if change_key in stats['severity_changes']:
                    stats['severity_changes'][change_key] += 1

                # Check for false positives
                if analyzed['context_analysis'].get('is_likely_false_positive', False):
                    stats['false_positive_count'] += 1

        # Calculate false positive rate
        stats['false_positive_rate'] = round(
            (stats['false_positive_count'] / stats['total_findings'] * 100), 2
        ) if stats['total_findings'] > 0 else 0.0

        return {
            'analyzed_findings': analyzed_findings,
            'statistics': stats
        }


def main():
    """CLI interface for testing the analyzer."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze findings with context')
    parser.add_argument('findings', help='Input JSON file with findings')
    parser.add_argument('--rules', help='Severity rules file',
                       default='../../config/severity_rules.json')
    parser.add_argument('--output', help='Output file for analyzed findings')

    args = parser.parse_args()

    # Load analyzer
    analyzer = ContextAnalyzer(Path(args.rules))

    # Load findings
    with open(args.findings, 'r') as f:
        data = json.load(f)
        findings = data.get('all_findings', [])

    # Analyze batch
    result = analyzer.analyze_batch(findings)

    # Print statistics
    stats = result['statistics']
    print(f"\n=== Context Analysis Results ===")
    print(f"Total Findings: {stats['total_findings']}")
    print(f"Adjusted: {stats['adjusted_count']} ({stats['adjusted_count']/stats['total_findings']*100:.1f}%)")
    print(f"False Positives: {stats['false_positive_count']} ({stats['false_positive_rate']}%)")

    print(f"\nOriginal Distribution:")
    for sev, count in sorted(stats['original_distribution'].items()):
        print(f"  {sev}: {count}")

    print(f"\nAdjusted Distribution:")
    for sev, count in sorted(stats['adjusted_distribution'].items()):
        print(f"  {sev}: {count}")

    # Export if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nExported to {args.output}")

    return 0


if __name__ == '__main__':
    exit(main())
