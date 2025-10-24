#!/usr/bin/env python3
"""
Plugin Security Checker - Report Generator
Version: 1.0.0

Generates human-readable security reports in Markdown and HTML formats.
"""

import json
from typing import Dict, Any, List
from datetime import datetime


class ReportGenerator:
    """Generates formatted security reports"""

    def __init__(self, report_data: Dict[str, Any]):
        self.data = report_data

    def generate_markdown(self) -> str:
        """Generate Markdown format report"""
        md = []

        # Header
        md.append("# Plugin Security Scan Report\n")
        md.append(f"**Generated:** {self._format_datetime(self.data['metadata']['scan_date'])}\n")
        md.append(f"**Plugin:** `{self.data['metadata']['plugin_path']}`\n")
        md.append(f"**Scanner Version:** {self.data['metadata']['scanner_version']}\n")
        md.append("\n---\n")

        # Executive Summary
        md.append("## Executive Summary\n")
        md.append(f"- **Overall Risk Level:** {self._format_risk_badge(self.data['metadata']['risk_level'])}\n")
        md.append(f"- **Risk Score:** {self.data['metadata']['risk_score']}\n")
        md.append(f"- **Verdict:** {self._format_verdict(self.data['metadata']['verdict'])}\n")
        md.append(f"- **Total Findings:** {self.data['metadata']['total_findings']}\n")
        md.append("\n")

        # Severity Breakdown
        md.append("### Findings by Severity\n")
        md.append("| Severity | Count |\n")
        md.append("|----------|-------|\n")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            count = self.data['summary']['severity_counts'].get(severity, 0)
            badge = self._format_severity_badge(severity)
            md.append(f"| {badge} | {count} |\n")
        md.append("\n")

        # Category Breakdown
        md.append("### Findings by Category\n")
        md.append("| Category | Count |\n")
        md.append("|----------|-------|\n")
        for category, count in sorted(self.data['summary']['categories'].items(), key=lambda x: -x[1]):
            md.append(f"| {category} | {count} |\n")
        md.append("\n")

        md.append("---\n\n")

        # Critical Findings
        critical_findings = [f for f in self.data['findings'] if f['severity'] == 'CRITICAL']
        if critical_findings:
            md.append("## ⚠️ Critical Findings\n")
            md.append("**Immediate action required!**\n\n")
            for finding in critical_findings:
                md.append(self._format_finding_markdown(finding, detailed=True))
            md.append("\n---\n\n")

        # High Priority Findings
        high_findings = [f for f in self.data['findings'] if f['severity'] == 'HIGH']
        if high_findings:
            md.append("## 🔴 High Priority Findings\n")
            md.append("**Review recommended**\n\n")
            for finding in high_findings:
                md.append(self._format_finding_markdown(finding, detailed=True))
            md.append("\n---\n\n")

        # Medium Priority Findings
        medium_findings = [f for f in self.data['findings'] if f['severity'] == 'MEDIUM']
        if medium_findings:
            md.append("## 🟡 Medium Priority Findings\n")
            for finding in medium_findings:
                md.append(self._format_finding_markdown(finding, detailed=False))
            md.append("\n---\n\n")

        # Low/Info Findings
        low_findings = [f for f in self.data['findings'] if f['severity'] in ['LOW', 'INFO']]
        if low_findings:
            md.append("## 🔵 Low Priority & Informational\n")
            md.append("<details>\n<summary>Click to expand low priority findings</summary>\n\n")
            for finding in low_findings:
                md.append(self._format_finding_markdown(finding, detailed=False))
            md.append("</details>\n\n")
            md.append("---\n\n")

        # Disclaimer
        md.append("## ⚠️ Security Disclaimer\n")
        md.append("```\n")
        md.append(self.data['disclaimer'])
        md.append("```\n")

        return "".join(md)

    def generate_html(self) -> str:
        """Generate HTML format report"""
        html = []

        # HTML Header
        html.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plugin Security Scan Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a1a1a;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h2 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e0e0e0;
        }
        h3 {
            color: #34495e;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .metadata {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .metadata p {
            margin: 5px 0;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .summary-card {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 20px;
            text-align: center;
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
        }
        .summary-card .value {
            font-size: 36px;
            font-weight: bold;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .badge-critical {
            background: #dc3545;
            color: white;
        }
        .badge-high {
            background: #fd7e14;
            color: white;
        }
        .badge-medium {
            background: #ffc107;
            color: #000;
        }
        .badge-low {
            background: #17a2b8;
            color: white;
        }
        .badge-info {
            background: #6c757d;
            color: white;
        }
        .badge-pass {
            background: #28a745;
            color: white;
        }
        .badge-review {
            background: #ffc107;
            color: #000;
        }
        .badge-fail {
            background: #dc3545;
            color: white;
        }
        .finding {
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .finding.critical {
            border-left-color: #dc3545;
            background: #fff5f5;
        }
        .finding.high {
            border-left-color: #fd7e14;
            background: #fff8f0;
        }
        .finding.medium {
            border-left-color: #ffc107;
        }
        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .finding-id {
            font-family: 'Courier New', monospace;
            color: #666;
            font-size: 14px;
        }
        .finding-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .finding-location {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }
        .code-snippet {
            background: #272822;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin: 10px 0;
        }
        .finding-details {
            margin-top: 15px;
        }
        .finding-details dt {
            font-weight: 600;
            margin-top: 10px;
            color: #555;
        }
        .finding-details dd {
            margin-left: 20px;
            margin-top: 5px;
        }
        .disclaimer {
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 20px;
            border-radius: 5px;
            margin-top: 30px;
        }
        .disclaimer h2 {
            color: #856404;
            border: none;
            margin-top: 0;
        }
        .disclaimer pre {
            background: #fff;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
        }
        tr:hover {
            background: #f8f9fa;
        }
        details {
            margin: 20px 0;
        }
        summary {
            cursor: pointer;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
            font-weight: 600;
        }
        summary:hover {
            background: #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
""")

        # Title and Metadata
        html.append(f"        <h1>🔒 Plugin Security Scan Report</h1>\n")
        html.append(f"        <div class='metadata'>\n")
        html.append(f"            <p><strong>Generated:</strong> {self._format_datetime(self.data['metadata']['scan_date'])}</p>\n")
        html.append(f"            <p><strong>Plugin:</strong> <code>{self._escape_html(self.data['metadata']['plugin_path'])}</code></p>\n")
        html.append(f"            <p><strong>Scanner Version:</strong> {self.data['metadata']['scanner_version']}</p>\n")
        html.append(f"        </div>\n")

        # Summary Cards
        html.append(f"        <div class='summary'>\n")
        html.append(f"            <div class='summary-card'>\n")
        html.append(f"                <h3>Risk Level</h3>\n")
        html.append(f"                <div class='value'>{self._format_risk_badge_html(self.data['metadata']['risk_level'])}</div>\n")
        html.append(f"            </div>\n")
        html.append(f"            <div class='summary-card'>\n")
        html.append(f"                <h3>Verdict</h3>\n")
        html.append(f"                <div class='value'>{self._format_verdict_html(self.data['metadata']['verdict'])}</div>\n")
        html.append(f"            </div>\n")
        html.append(f"            <div class='summary-card'>\n")
        html.append(f"                <h3>Risk Score</h3>\n")
        html.append(f"                <div class='value'>{self.data['metadata']['risk_score']}</div>\n")
        html.append(f"            </div>\n")
        html.append(f"            <div class='summary-card'>\n")
        html.append(f"                <h3>Total Findings</h3>\n")
        html.append(f"                <div class='value'>{self.data['metadata']['total_findings']}</div>\n")
        html.append(f"            </div>\n")
        html.append(f"        </div>\n")

        # Severity Breakdown Table
        html.append(f"        <h2>Findings by Severity</h2>\n")
        html.append(f"        <table>\n")
        html.append(f"            <thead><tr><th>Severity</th><th>Count</th></tr></thead>\n")
        html.append(f"            <tbody>\n")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            count = self.data['summary']['severity_counts'].get(severity, 0)
            badge = self._format_severity_badge_html(severity)
            html.append(f"                <tr><td>{badge}</td><td>{count}</td></tr>\n")
        html.append(f"            </tbody>\n")
        html.append(f"        </table>\n")

        # Category Breakdown
        html.append(f"        <h2>Findings by Category</h2>\n")
        html.append(f"        <table>\n")
        html.append(f"            <thead><tr><th>Category</th><th>Count</th></tr></thead>\n")
        html.append(f"            <tbody>\n")
        for category, count in sorted(self.data['summary']['categories'].items(), key=lambda x: -x[1]):
            html.append(f"                <tr><td>{self._escape_html(category)}</td><td>{count}</td></tr>\n")
        html.append(f"            </tbody>\n")
        html.append(f"        </table>\n")

        # Critical Findings
        critical_findings = [f for f in self.data['findings'] if f['severity'] == 'CRITICAL']
        if critical_findings:
            html.append(f"        <h2>⚠️ Critical Findings</h2>\n")
            html.append(f"        <p><strong>Immediate action required!</strong></p>\n")
            for finding in critical_findings:
                html.append(self._format_finding_html(finding, detailed=True))

        # High Priority Findings
        high_findings = [f for f in self.data['findings'] if f['severity'] == 'HIGH']
        if high_findings:
            html.append(f"        <h2>🔴 High Priority Findings</h2>\n")
            html.append(f"        <p><strong>Review recommended</strong></p>\n")
            for finding in high_findings:
                html.append(self._format_finding_html(finding, detailed=True))

        # Medium Priority Findings
        medium_findings = [f for f in self.data['findings'] if f['severity'] == 'MEDIUM']
        if medium_findings:
            html.append(f"        <h2>🟡 Medium Priority Findings</h2>\n")
            for finding in medium_findings:
                html.append(self._format_finding_html(finding, detailed=False))

        # Low/Info Findings
        low_findings = [f for f in self.data['findings'] if f['severity'] in ['LOW', 'INFO']]
        if low_findings:
            html.append(f"        <h2>🔵 Low Priority & Informational</h2>\n")
            html.append(f"        <details>\n")
            html.append(f"            <summary>Click to expand low priority findings ({len(low_findings)} total)</summary>\n")
            for finding in low_findings:
                html.append(self._format_finding_html(finding, detailed=False))
            html.append(f"        </details>\n")

        # Disclaimer
        html.append(f"        <div class='disclaimer'>\n")
        html.append(f"            <h2>⚠️ Security Disclaimer</h2>\n")
        html.append(f"            <pre>{self._escape_html(self.data['disclaimer'])}</pre>\n")
        html.append(f"        </div>\n")

        # HTML Footer
        html.append("""    </div>
</body>
</html>
""")

        return "".join(html)

    def _format_finding_markdown(self, finding: Dict, detailed: bool = False) -> str:
        """Format a single finding in Markdown"""
        md = []

        md.append(f"### {finding['id']} - {finding['description']}\n\n")
        md.append(f"**Severity:** {self._format_severity_badge(finding['severity'])}\n")
        md.append(f"**Category:** {finding['category']} / {finding['subcategory']}\n")
        md.append(f"**Location:** `{finding['file']}:{finding['line']}:{finding['column']}`\n\n")

        if finding['code_snippet']:
            md.append("**Code Snippet:**\n```\n")
            md.append(finding['code_snippet'])
            md.append("\n```\n\n")

        if detailed:
            md.append(f"**Explanation:** {finding['explanation']}\n\n")
            md.append(f"**Impact:** {finding['impact']}\n\n")
            md.append(f"**Recommendation:** {finding['recommendation']}\n\n")

            if finding.get('cvss_score', 0) > 0:
                md.append(f"**CVSS Score:** {finding['cvss_score']}\n\n")

            if finding.get('cve_reference'):
                md.append(f"**CVE Reference:** {finding['cve_reference']}\n\n")

            if finding.get('owasp_reference'):
                md.append(f"**OWASP Reference:** {finding['owasp_reference']}\n\n")

            md.append(f"**Remediation Effort:** {finding['remediation_effort']}\n\n")

        md.append("---\n\n")

        return "".join(md)

    def _format_finding_html(self, finding: Dict, detailed: bool = False) -> str:
        """Format a single finding in HTML"""
        severity_class = finding['severity'].lower()

        html = []
        html.append(f"        <div class='finding {severity_class}'>\n")
        html.append(f"            <div class='finding-header'>\n")
        html.append(f"                <span class='finding-id'>{finding['id']}</span>\n")
        html.append(f"                {self._format_severity_badge_html(finding['severity'])}\n")
        html.append(f"            </div>\n")
        html.append(f"            <div class='finding-title'>{self._escape_html(finding['description'])}</div>\n")
        html.append(f"            <div class='finding-location'>{self._escape_html(finding['file'])}:{finding['line']}:{finding['column']}</div>\n")

        if finding['code_snippet']:
            html.append(f"            <div class='code-snippet'>{self._escape_html(finding['code_snippet'])}</div>\n")

        if detailed:
            html.append(f"            <dl class='finding-details'>\n")
            html.append(f"                <dt>Explanation</dt>\n")
            html.append(f"                <dd>{self._escape_html(finding['explanation'])}</dd>\n")
            html.append(f"                <dt>Impact</dt>\n")
            html.append(f"                <dd>{self._escape_html(finding['impact'])}</dd>\n")
            html.append(f"                <dt>Recommendation</dt>\n")
            html.append(f"                <dd>{self._escape_html(finding['recommendation'])}</dd>\n")

            if finding.get('cvss_score', 0) > 0:
                html.append(f"                <dt>CVSS Score</dt>\n")
                html.append(f"                <dd>{finding['cvss_score']}</dd>\n")

            if finding.get('cve_reference'):
                html.append(f"                <dt>CVE Reference</dt>\n")
                html.append(f"                <dd>{finding['cve_reference']}</dd>\n")

            if finding.get('owasp_reference'):
                html.append(f"                <dt>OWASP Reference</dt>\n")
                html.append(f"                <dd>{finding['owasp_reference']}</dd>\n")

            html.append(f"                <dt>Remediation Effort</dt>\n")
            html.append(f"                <dd>{finding['remediation_effort']}</dd>\n")
            html.append(f"            </dl>\n")

        html.append(f"        </div>\n")

        return "".join(html)

    def _format_risk_badge(self, risk: str) -> str:
        """Format risk level as Markdown badge"""
        emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(risk, "⚪")
        return f"{emoji} **{risk}**"

    def _format_risk_badge_html(self, risk: str) -> str:
        """Format risk level as HTML badge"""
        badge_class = risk.lower()
        return f"<span class='badge badge-{badge_class}'>{risk}</span>"

    def _format_verdict(self, verdict: str) -> str:
        """Format verdict as Markdown"""
        emoji = {"PASS": "✅", "REVIEW": "⚠️", "FAIL": "❌"}.get(verdict, "⚪")
        return f"{emoji} **{verdict}**"

    def _format_verdict_html(self, verdict: str) -> str:
        """Format verdict as HTML badge"""
        badge_class = verdict.lower()
        return f"<span class='badge badge-{badge_class}'>{verdict}</span>"

    def _format_severity_badge(self, severity: str) -> str:
        """Format severity as Markdown badge"""
        emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🔵",
            "INFO": "⚪"
        }.get(severity, "⚪")
        return f"{emoji} {severity}"

    def _format_severity_badge_html(self, severity: str) -> str:
        """Format severity as HTML badge"""
        badge_class = severity.lower()
        return f"<span class='badge badge-{badge_class}'>{severity}</span>"

    def _format_datetime(self, iso_datetime: str) -> str:
        """Format datetime for display"""
        try:
            dt = datetime.fromisoformat(iso_datetime)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return iso_datetime

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))


def main():
    """Standalone report generator"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Generate formatted security reports")
    parser.add_argument('input', help='Input JSON report file')
    parser.add_argument('--format', '-f', choices=['markdown', 'html'], default='markdown',
                        help='Output format')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')

    args = parser.parse_args()

    # Load JSON report
    try:
        with open(args.input, 'r') as f:
            report_data = json.load(f)
    except Exception as e:
        print(f"Error loading report: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate report
    generator = ReportGenerator(report_data)

    if args.format == 'markdown':
        output = generator.generate_markdown()
    elif args.format == 'html':
        output = generator.generate_html()

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
