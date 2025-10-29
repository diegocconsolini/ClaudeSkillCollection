#!/usr/bin/env python3
"""
Calculate accurate risk scores with context awareness.
"""

import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskCalculator:
    """Calculate risk scores with context-aware weighting."""

    def __init__(self, severity_levels: Dict[str, Dict] = None):
        """
        Initialize risk calculator.

        Args:
            severity_levels: Severity level definitions with scores
        """
        self.severity_levels = severity_levels or self._default_severity_levels()

    def _default_severity_levels(self) -> Dict[str, Dict]:
        """Get default severity level configuration."""
        return {
            'CRITICAL': {'score': 100, 'cvss_range': [9.0, 10.0]},
            'HIGH': {'score': 50, 'cvss_range': [7.0, 8.9]},
            'MEDIUM': {'score': 25, 'cvss_range': [4.0, 6.9]},
            'LOW': {'score': 10, 'cvss_range': [0.1, 3.9]},
            'INFO': {'score': 0, 'cvss_range': [0.0, 0.0]},
            'UNKNOWN': {'score': 0, 'cvss_range': [0.0, 0.0]}
        }

    def calculate_finding_score(self, finding: Dict[str, Any]) -> float:
        """
        Calculate risk score for a single finding.

        Args:
            finding: Security finding with context analysis

        Returns:
            Risk score (0-100)
        """
        severity = finding.get('severity', 'UNKNOWN').upper()
        base_score = self.severity_levels.get(severity, {}).get('score', 0)

        # Apply context modifiers
        context = finding.get('context_analysis', {})

        # If identified as false positive, score is 0
        if context.get('is_likely_false_positive', False):
            return 0.0

        # Apply confidence multiplier
        confidence = context.get('confidence', 1.0)
        score = base_score * confidence

        # Boost score if user input is involved
        if self._has_user_input(finding):
            score *= 1.5

        # Reduce score for low-risk patterns
        if self._is_low_risk_pattern(finding):
            score *= 0.3

        # Cap at 100
        return min(score, 100.0)

    def calculate_plugin_score(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate aggregate risk score for a plugin.

        Args:
            findings: List of findings for the plugin

        Returns:
            Risk assessment dictionary
        """
        if not findings:
            return {
                'risk_score': 0.0,
                'risk_level': 'NONE',
                'finding_count': 0
            }

        # Calculate individual scores
        finding_scores = [self.calculate_finding_score(f) for f in findings]

        # Filter out false positives (score = 0)
        real_scores = [s for s in finding_scores if s > 0]

        if not real_scores:
            risk_score = 0.0
        else:
            # Use weighted average favoring higher scores
            # Formula: 0.5 * max + 0.3 * mean + 0.2 * sum_of_top_3
            max_score = max(real_scores)
            mean_score = sum(real_scores) / len(real_scores)
            top_3 = sorted(real_scores, reverse=True)[:3]
            top_3_sum = sum(top_3)

            risk_score = (0.5 * max_score +
                         0.3 * mean_score +
                         0.2 * top_3_sum)

            # Cap at 100
            risk_score = min(risk_score, 100.0)

        # Determine risk level
        risk_level = self._score_to_level(risk_score)

        # Calculate severity distribution
        severity_dist = {}
        for finding in findings:
            sev = finding.get('severity', 'UNKNOWN')
            severity_dist[sev] = severity_dist.get(sev, 0) + 1

        return {
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'finding_count': len(findings),
            'real_finding_count': len(real_scores),
            'false_positive_count': len(findings) - len(real_scores),
            'max_finding_score': round(max(real_scores), 2) if real_scores else 0.0,
            'mean_finding_score': round(sum(real_scores) / len(real_scores), 2) if real_scores else 0.0,
            'severity_distribution': severity_dist
        }

    def calculate_overall_risk(self, plugin_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall risk across all plugins.

        Args:
            plugin_scores: List of plugin risk assessments

        Returns:
            Overall risk assessment
        """
        if not plugin_scores:
            return {
                'overall_risk_score': 0.0,
                'overall_risk_level': 'NONE',
                'high_risk_count': 0,
                'medium_risk_count': 0,
                'low_risk_count': 0
            }

        # Extract scores
        scores = [p['risk_score'] for p in plugin_scores]

        # Calculate overall score (weighted average favoring high-risk plugins)
        high_risk = [s for s in scores if s >= 75]
        medium_risk = [s for s in scores if 50 <= s < 75]
        low_risk = [s for s in scores if 25 <= s < 50]

        if high_risk:
            overall_score = max(high_risk)
        elif medium_risk:
            overall_score = sum(medium_risk) / len(medium_risk)
        elif low_risk:
            overall_score = sum(low_risk) / len(low_risk)
        else:
            overall_score = sum(scores) / len(scores) if scores else 0.0

        return {
            'overall_risk_score': round(overall_score, 2),
            'overall_risk_level': self._score_to_level(overall_score),
            'total_plugins': len(plugin_scores),
            'critical_risk_count': len([s for s in scores if s >= 90]),
            'high_risk_count': len([s for s in scores if 75 <= s < 90]),
            'medium_risk_count': len([s for s in scores if 50 <= s < 75]),
            'low_risk_count': len([s for s in scores if 25 <= s < 50]),
            'minimal_risk_count': len([s for s in scores if s < 25]),
            'max_plugin_score': round(max(scores), 2) if scores else 0.0,
            'mean_plugin_score': round(sum(scores) / len(scores), 2) if scores else 0.0
        }

    def _score_to_level(self, score: float) -> str:
        """Convert numeric score to risk level."""
        if score >= 90:
            return 'CRITICAL'
        elif score >= 75:
            return 'HIGH'
        elif score >= 50:
            return 'MEDIUM'
        elif score >= 25:
            return 'LOW'
        elif score > 0:
            return 'MINIMAL'
        else:
            return 'NONE'

    def _has_user_input(self, finding: Dict[str, Any]) -> bool:
        """Check if finding involves user input."""
        code = finding.get('code_snippet', '').lower()
        description = finding.get('description', '').lower()

        user_input_indicators = [
            'user', 'input', 'req.', 'request', 'params',
            'query', 'body', 'form', 'post', 'get'
        ]

        return any(ind in code or ind in description for ind in user_input_indicators)

    def _is_low_risk_pattern(self, finding: Dict[str, Any]) -> bool:
        """Check if finding matches low-risk patterns."""
        context = finding.get('context_analysis', {})

        # Check if downgraded from original severity
        original = context.get('original_severity', '')
        current = finding.get('severity', '')

        severity_order = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'INFO': 1}
        original_score = severity_order.get(original, 0)
        current_score = severity_order.get(current, 0)

        # If downgraded, it's a low-risk pattern
        return original_score > current_score


def main():
    """CLI interface for testing the calculator."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Calculate risk scores')
    parser.add_argument('findings', help='Input JSON file with analyzed findings')

    args = parser.parse_args()

    # Load findings
    with open(args.findings, 'r') as f:
        data = json.load(f)

    calculator = RiskCalculator()

    # Group findings by plugin
    plugins = {}
    for finding in data.get('analyzed_findings', []):
        plugin = finding.get('plugin_name', 'unknown')
        if plugin not in plugins:
            plugins[plugin] = []
        plugins[plugin].append(finding)

    # Calculate per-plugin scores
    plugin_scores = []
    for plugin_name, findings in plugins.items():
        score = calculator.calculate_plugin_score(findings)
        score['plugin_name'] = plugin_name
        plugin_scores.append(score)

    # Calculate overall risk
    overall = calculator.calculate_overall_risk(plugin_scores)

    # Print results
    print(f"\n=== Risk Assessment ===")
    print(f"Overall Risk Score: {overall['overall_risk_score']}")
    print(f"Overall Risk Level: {overall['overall_risk_level']}")
    print(f"\nPlugins by Risk:")
    print(f"  CRITICAL: {overall['critical_risk_count']}")
    print(f"  HIGH: {overall['high_risk_count']}")
    print(f"  MEDIUM: {overall['medium_risk_count']}")
    print(f"  LOW: {overall['low_risk_count']}")
    print(f"  MINIMAL: {overall['minimal_risk_count']}")

    print(f"\n=== Top 10 Risky Plugins ===")
    for plugin in sorted(plugin_scores, key=lambda x: x['risk_score'], reverse=True)[:10]:
        print(f"{plugin['plugin_name']}: {plugin['risk_score']} ({plugin['risk_level']}) "
              f"- {plugin['real_finding_count']}/{plugin['finding_count']} real findings")

    return 0


if __name__ == '__main__':
    exit(main())
