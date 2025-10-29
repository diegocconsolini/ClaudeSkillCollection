#!/usr/bin/env python3
"""
Generate professional PDF security reports using WeasyPrint.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except Exception as e:
    logging.warning(f"weasyprint not available: {e}")
    HTML = None
    CSS = None
    FontConfiguration = None
    WEASYPRINT_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """Generate professional PDF reports."""

    def __init__(self):
        """Initialize PDF generator."""
        self.font_config = FontConfiguration() if HTML else None

    def generate_report(self,
                       findings: List[Dict[str, Any]],
                       statistics: Dict[str, Any],
                       framework_summary: Dict[str, Any],
                       plugin_scores: List[Dict[str, Any]],
                       overall_risk: Dict[str, Any],
                       config: Dict[str, Any],
                       branding: Dict[str, Any],
                       output_path: Path) -> None:
        """
        Generate PDF report from HTML.

        Args:
            findings: List of security findings
            statistics: Aggregate statistics
            framework_summary: Framework analysis
            plugin_scores: Plugin risk scores
            overall_risk: Overall risk assessment
            config: Report configuration
            branding: Branding configuration
            output_path: Output file path
        """
        if not HTML:
            logger.error("WeasyPrint not installed. Cannot generate PDF.")
            logger.info("Install with: pip install weasyprint")
            return

        # Generate print-optimized HTML
        html_content = self._generate_print_html(
            findings, statistics, framework_summary,
            plugin_scores, overall_risk, config, branding
        )

        # Generate PDF
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            HTML(string=html_content).write_pdf(
                str(output_path),
                font_config=self.font_config
            )

            logger.info(f"Generated PDF report: {output_path}")
            logger.info(f"Report size: {output_path.stat().st_size / 1024:.1f} KB")

        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise

    def _generate_print_html(self,
                            findings: List[Dict[str, Any]],
                            statistics: Dict[str, Any],
                            framework_summary: Dict[str, Any],
                            plugin_scores: List[Dict[str, Any]],
                            overall_risk: Dict[str, Any],
                            config: Dict[str, Any],
                            branding: Dict[str, Any]) -> str:
        """
        Generate print-optimized HTML for PDF conversion.

        Returns:
            HTML string optimized for printing
        """
        company = branding.get('company_name', 'Your Organization')
        primary = branding.get('primary_color', '#6366f1')
        secondary = branding.get('secondary_color', '#8b5cf6')
        generated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Severity counts
        critical_count = statistics.get('by_severity', {}).get('CRITICAL', 0)
        high_count = statistics.get('by_severity', {}).get('HIGH', 0)
        medium_count = statistics.get('by_severity', {}).get('MEDIUM', 0)
        low_count = statistics.get('by_severity', {}).get('LOW', 0)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Security Assessment Report - {company}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @top-center {{
                content: "Security Assessment Report - {company}";
                font-size: 10pt;
                color: #666;
            }}
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }}
        }}

        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}

        h1 {{
            color: {primary};
            font-size: 24pt;
            margin-bottom: 10px;
            page-break-after: avoid;
        }}

        h2 {{
            color: {primary};
            font-size: 18pt;
            margin-top: 20px;
            margin-bottom: 12px;
            border-bottom: 2px solid {primary};
            padding-bottom: 6px;
            page-break-after: avoid;
        }}

        h3 {{
            color: {secondary};
            font-size: 14pt;
            margin-top: 16px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}

        .cover-page {{
            text-align: center;
            padding-top: 100px;
            page-break-after: always;
        }}

        .cover-page h1 {{
            font-size: 32pt;
            margin-bottom: 20px;
        }}

        .cover-page .subtitle {{
            font-size: 16pt;
            color: #666;
            margin-bottom: 40px;
        }}

        .executive-summary {{
            background: #f8f9fa;
            border-left: 4px solid {primary};
            padding: 20px;
            margin: 20px 0;
            page-break-inside: avoid;
        }}

        .risk-level {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12pt;
        }}

        .risk-CRITICAL {{ background: #dc2626; color: white; }}
        .risk-HIGH {{ background: #ea580c; color: white; }}
        .risk-MEDIUM {{ background: #f59e0b; color: white; }}
        .risk-LOW {{ background: #10b981; color: white; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            page-break-inside: avoid;
        }}

        th {{
            background: {primary};
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            font-size: 10pt;
        }}

        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
            font-size: 10pt;
        }}

        tr:nth-child(even) {{
            background: #f8f9fa;
        }}

        .finding-card {{
            border-left: 4px solid;
            padding: 16px;
            margin: 16px 0;
            background: #f8f9fa;
            page-break-inside: avoid;
        }}

        .finding-card.CRITICAL {{ border-left-color: #dc2626; }}
        .finding-card.HIGH {{ border-left-color: #ea580c; }}
        .finding-card.MEDIUM {{ border-left-color: #f59e0b; }}
        .finding-card.LOW {{ border-left-color: #10b981; }}

        .severity-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 9pt;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .severity-badge.CRITICAL {{ background: #dc2626; color: white; }}
        .severity-badge.HIGH {{ background: #ea580c; color: white; }}
        .severity-badge.MEDIUM {{ background: #f59e0b; color: white; }}
        .severity-badge.LOW {{ background: #10b981; color: white; }}

        code {{
            background: #e5e7eb;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }}

        pre {{
            background: #e5e7eb;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 8pt;
            line-height: 1.4;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin: 20px 0;
        }}

        .stat-box {{
            text-align: center;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 4px;
        }}

        .stat-box .value {{
            font-size: 24pt;
            font-weight: bold;
            color: {primary};
        }}

        .stat-box .label {{
            font-size: 9pt;
            text-transform: uppercase;
            color: #666;
        }}

        .page-break {{
            page-break-before: always;
        }}

        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 9pt;
            color: #666;
        }}
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        <h1>Security Assessment Report</h1>
        <div class="subtitle">{company}</div>
        <p>Generated: {generated}</p>
        <p style="margin-top: 60px;">
            <span class="risk-level risk-{overall_risk['overall_risk_level']}">
                Risk Level: {overall_risk['overall_risk_level']}
            </span>
        </p>
    </div>

    <!-- Executive Summary -->
    <h2>Executive Summary</h2>
    <div class="executive-summary">
        <p><strong>Overall Risk Assessment:</strong></p>
        <ul>
            <li>Risk Score: <strong>{overall_risk['overall_risk_score']}/100</strong></li>
            <li>Risk Level: <strong>{overall_risk['overall_risk_level']}</strong></li>
            <li>Plugins Analyzed: <strong>{statistics['total_plugins']}</strong></li>
            <li>Total Findings: <strong>{statistics['total_findings']}</strong></li>
        </ul>
        <p style="margin-top: 16px;">
            This assessment identified <strong>{overall_risk['critical_risk_count'] + overall_risk['high_risk_count']}</strong>
            high-priority plugins requiring immediate remediation. Context-aware analysis has been applied to reduce
            false positives and focus on actionable security issues.
        </p>
    </div>

    <!-- Key Statistics -->
    <h2>Key Statistics</h2>
    <div class="stats-grid">
        <div class="stat-box">
            <div class="value">{critical_count}</div>
            <div class="label">Critical</div>
        </div>
        <div class="stat-box">
            <div class="value">{high_count}</div>
            <div class="label">High</div>
        </div>
        <div class="stat-box">
            <div class="value">{medium_count}</div>
            <div class="label">Medium</div>
        </div>
    </div>

    <!-- Top Risky Plugins -->
    <h2>Top 10 Risky Plugins</h2>
    <table>
        <thead>
            <tr>
                <th>Plugin Name</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Findings</th>
                <th>Critical</th>
                <th>High</th>
            </tr>
        </thead>
        <tbody>"""

        # Add top plugins
        for plugin in plugin_scores[:10]:
            sev_dist = plugin.get('severity_distribution', {})
            html += f"""
            <tr>
                <td>{plugin.get('plugin_name', 'unknown')}</td>
                <td><strong>{plugin['risk_score']}</strong></td>
                <td>{plugin['risk_level']}</td>
                <td>{plugin['real_finding_count']}/{plugin['finding_count']}</td>
                <td>{sev_dist.get('CRITICAL', 0)}</td>
                <td>{sev_dist.get('HIGH', 0)}</td>
            </tr>"""

        html += """
        </tbody>
    </table>

    <!-- Critical Findings -->
    <div class="page-break"></div>
    <h2>Critical Findings</h2>"""

        critical = [f for f in findings if f.get('severity') == 'CRITICAL'][:20]
        if critical:
            for idx, finding in enumerate(critical, 1):
                category = finding.get('category', 'Unknown')
                plugin = finding.get('plugin_name', 'unknown')
                desc = finding.get('description', 'No description')

                html += f"""
    <div class="finding-card CRITICAL">
        <h3>{idx}. {category} <span class="severity-badge CRITICAL">CRITICAL</span></h3>
        <p><strong>Plugin:</strong> <code>{plugin}</code></p>
        <p>{desc}</p>
    </div>"""
        else:
            html += '<p>No critical findings identified.</p>'

        html += f"""
    <!-- Framework Analysis -->
    <div class="page-break"></div>
    <h2>Framework Coverage</h2>
    <table>
        <thead>
            <tr>
                <th>Framework</th>
                <th>Techniques/Categories</th>
                <th>Coverage</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>MITRE ATT&CK</td>
                <td>{framework_summary.get('mitre_attack', {}).get('total_techniques', 0)}</td>
                <td>{framework_summary.get('mitre_attack', {}).get('coverage_percent', 0)}%</td>
            </tr>
            <tr>
                <td>MITRE ATLAS</td>
                <td>{framework_summary.get('mitre_atlas', {}).get('total_techniques', 0)}</td>
                <td>{framework_summary.get('mitre_atlas', {}).get('coverage_percent', 0)}%</td>
            </tr>
            <tr>
                <td>OWASP Top 10</td>
                <td>{framework_summary.get('owasp', {}).get('total_categories', 0)}</td>
                <td>N/A</td>
            </tr>
            <tr>
                <td>CWE</td>
                <td>{framework_summary.get('cwe', {}).get('total_weaknesses', 0)}</td>
                <td>N/A</td>
            </tr>
        </tbody>
    </table>

    <footer>
        <p>{branding.get('footer_text', 'Confidential')}</p>
        <p>Report generated by Security Report Builder v1.0.0</p>
    </footer>
</body>
</html>"""

        return html


def main():
    """CLI interface for testing the generator."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Generate PDF security report')
    parser.add_argument('findings', help='Input JSON file with analyzed findings')
    parser.add_argument('--output', required=True, help='Output PDF file')
    parser.add_argument('--config', help='Report config JSON')
    parser.add_argument('--branding', help='Branding config JSON')

    args = parser.parse_args()

    # Load data
    with open(args.findings, 'r') as f:
        data = json.load(f)

    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)

    branding = {}
    if args.branding:
        with open(args.branding, 'r') as f:
            branding = json.load(f)

    # Generate PDF
    generator = PDFReportGenerator()
    generator.generate_report(
        findings=data.get('analyzed_findings', []),
        statistics=data.get('statistics', {}),
        framework_summary=data.get('framework_summary', {}),
        plugin_scores=data.get('plugin_scores', []),
        overall_risk=data.get('overall_risk', {}),
        config=config,
        branding=branding,
        output_path=Path(args.output)
    )

    print(f"\n✓ PDF report generated: {args.output}")
    return 0


if __name__ == '__main__':
    exit(main())
