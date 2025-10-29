#!/usr/bin/env python3
"""
Parse security scanner JSON results and aggregate findings.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Union
from collections import defaultdict, Counter
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScanResultParser:
    """Parse and aggregate security scan results from JSON files."""

    def __init__(self):
        self.results = []
        self.stats = {
            'total_plugins': 0,
            'total_findings': 0,
            'by_severity': Counter(),
            'by_category': Counter(),
            'by_plugin': defaultdict(dict),
            'scan_dates': []
        }

    def parse_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Parse a single JSON scan result file.

        Args:
            file_path: Path to JSON file

        Returns:
            Parsed result dictionary
        """
        file_path = Path(file_path)

        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate required fields
            if 'metadata' not in data or 'findings' not in data:
                logger.warning(f"Invalid format in {file_path}: missing required fields")
                return None

            # Normalize data structure
            result = {
                'plugin_name': data['metadata'].get('plugin_name', file_path.stem),
                'scan_date': data['metadata'].get('scan_date', datetime.now().isoformat()),
                'scanner_version': data['metadata'].get('scanner_version', 'unknown'),
                'findings': data.get('findings', []),
                'summary': data.get('summary', {}),
                'file_path': str(file_path)
            }

            # Update statistics
            self._update_stats(result)

            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return None

    def parse_directory(self, dir_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Parse all JSON files in a directory.

        Args:
            dir_path: Path to directory containing JSON files

        Returns:
            List of parsed results
        """
        dir_path = Path(dir_path)

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory not found: {dir_path}")
            return []

        json_files = list(dir_path.glob('*.json'))
        logger.info(f"Found {len(json_files)} JSON files in {dir_path}")

        results = []
        for json_file in json_files:
            result = self.parse_file(json_file)
            if result:
                results.append(result)
                self.results.append(result)

        logger.info(f"Successfully parsed {len(results)} files")
        return results

    def _update_stats(self, result: Dict[str, Any]) -> None:
        """Update aggregate statistics with new result."""
        self.stats['total_plugins'] += 1

        findings = result.get('findings', [])
        self.stats['total_findings'] += len(findings)

        # Track by severity
        for finding in findings:
            severity = finding.get('severity', 'UNKNOWN')
            self.stats['by_severity'][severity] += 1

            # Track by category
            category = finding.get('category', 'UNKNOWN')
            self.stats['by_category'][category] += 1

        # Track per-plugin stats
        plugin_name = result['plugin_name']
        self.stats['by_plugin'][plugin_name] = {
            'total_findings': len(findings),
            'by_severity': Counter(f.get('severity', 'UNKNOWN') for f in findings),
            'risk_score': result.get('summary', {}).get('risk_score', 0),
            'risk_level': result.get('summary', {}).get('risk_level', 'UNKNOWN')
        }

        # Track scan dates
        if result.get('scan_date'):
            self.stats['scan_dates'].append(result['scan_date'])

    def get_all_findings(self) -> List[Dict[str, Any]]:
        """
        Get flattened list of all findings across all plugins.

        Returns:
            List of findings with plugin context
        """
        all_findings = []

        for result in self.results:
            plugin_name = result['plugin_name']
            for finding in result.get('findings', []):
                finding_with_context = finding.copy()
                finding_with_context['plugin_name'] = plugin_name
                finding_with_context['scan_date'] = result['scan_date']
                all_findings.append(finding_with_context)

        return all_findings

    def get_findings_by_severity(self, min_severity: str = 'INFO') -> List[Dict[str, Any]]:
        """
        Get findings filtered by minimum severity level.

        Args:
            min_severity: Minimum severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)

        Returns:
            Filtered list of findings
        """
        severity_order = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'INFO': 1, 'UNKNOWN': 0}
        min_level = severity_order.get(min_severity.upper(), 0)

        all_findings = self.get_all_findings()
        return [
            f for f in all_findings
            if severity_order.get(f.get('severity', 'UNKNOWN'), 0) >= min_level
        ]

    def get_top_plugins_by_risk(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get plugins with highest risk scores.

        Args:
            limit: Maximum number of plugins to return

        Returns:
            List of plugin statistics sorted by risk score
        """
        plugins = []
        for plugin_name, stats in self.stats['by_plugin'].items():
            plugins.append({
                'plugin_name': plugin_name,
                'risk_score': stats['risk_score'],
                'risk_level': stats['risk_level'],
                'total_findings': stats['total_findings'],
                'critical_count': stats['by_severity'].get('CRITICAL', 0),
                'high_count': stats['by_severity'].get('HIGH', 0)
            })

        # Sort by risk score descending
        plugins.sort(key=lambda x: x['risk_score'], reverse=True)
        return plugins[:limit]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get aggregate statistics across all scans.

        Returns:
            Dictionary of statistics
        """
        return {
            'total_plugins': self.stats['total_plugins'],
            'total_findings': self.stats['total_findings'],
            'by_severity': dict(self.stats['by_severity']),
            'by_category': dict(self.stats['by_category']),
            'scan_date_range': {
                'earliest': min(self.stats['scan_dates']) if self.stats['scan_dates'] else None,
                'latest': max(self.stats['scan_dates']) if self.stats['scan_dates'] else None
            }
        }

    def export_aggregated_json(self, output_path: Union[str, Path]) -> None:
        """
        Export aggregated results to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        output_path = Path(output_path)

        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'parser_version': '1.0.0',
                'total_plugins_scanned': self.stats['total_plugins']
            },
            'statistics': self.get_statistics(),
            'top_risky_plugins': self.get_top_plugins_by_risk(20),
            'all_findings': self.get_all_findings()
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported aggregated results to {output_path}")


def main():
    """CLI interface for testing the parser."""
    import argparse

    parser = argparse.ArgumentParser(description='Parse security scan results')
    parser.add_argument('input', help='Input JSON file or directory')
    parser.add_argument('--output', help='Output JSON file for aggregated results')
    parser.add_argument('--min-severity', default='INFO',
                       help='Minimum severity level to include')

    args = parser.parse_args()

    # Parse results
    result_parser = ScanResultParser()
    input_path = Path(args.input)

    if input_path.is_file():
        result_parser.parse_file(input_path)
    elif input_path.is_dir():
        result_parser.parse_directory(input_path)
    else:
        logger.error(f"Invalid input path: {input_path}")
        return 1

    # Print statistics
    stats = result_parser.get_statistics()
    print(f"\n=== Scan Results Summary ===")
    print(f"Total Plugins: {stats['total_plugins']}")
    print(f"Total Findings: {stats['total_findings']}")
    print(f"\nBy Severity:")
    for severity, count in sorted(stats['by_severity'].items(),
                                  key=lambda x: {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3,
                                                'LOW': 2, 'INFO': 1}.get(x[0], 0),
                                  reverse=True):
        print(f"  {severity}: {count}")

    # Top risky plugins
    print(f"\n=== Top 10 Risky Plugins ===")
    for plugin in result_parser.get_top_plugins_by_risk(10):
        print(f"{plugin['plugin_name']}: Risk Score {plugin['risk_score']} "
              f"({plugin['critical_count']} CRITICAL, {plugin['high_count']} HIGH)")

    # Export if requested
    if args.output:
        result_parser.export_aggregated_json(args.output)

    return 0


if __name__ == '__main__':
    exit(main())
