#!/usr/bin/env python3
"""
Generate interactive HTML security reports with modern styling.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

try:
    from jinja2 import Template, Environment, FileSystemLoader
except ImportError:
    logging.warning("jinja2 not installed. Install with: pip install jinja2")
    Template = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTMLReportGenerator:
    """Generate interactive HTML reports."""

    def __init__(self, template_dir: Path = None):
        """
        Initialize HTML generator.

        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = template_dir or Path(__file__).parent.parent / 'templates'
        self.env = None

        if Template:
            try:
                self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
            except Exception as e:
                logger.warning(f"Could not load templates: {e}")

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
        Generate complete HTML report.

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
        # Prepare template data
        template_data = {
            'report_title': 'Security Assessment Report',
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'company_name': branding.get('company_name', 'Your Organization'),
            'primary_color': branding.get('primary_color', '#6366f1'),
            'secondary_color': branding.get('secondary_color', '#8b5cf6'),
            'accent_color': branding.get('accent_color', '#ec4899'),
            'footer_text': branding.get('footer_text', 'Confidential'),

            # Data
            'findings': findings,
            'statistics': statistics,
            'framework_summary': framework_summary,
            'plugin_scores': sorted(plugin_scores, key=lambda x: x['risk_score'], reverse=True)[:20],
            'overall_risk': overall_risk,

            # Top findings
            'top_critical': [f for f in findings if f.get('severity') == 'CRITICAL'][:10],
            'top_high': [f for f in findings if f.get('severity') == 'HIGH'][:10],

            # Utilities
            'len': len,
            'enumerate': enumerate,
            'round': round
        }

        # Generate HTML
        html = self._generate_html(template_data)

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"Generated HTML report: {output_path}")
        logger.info(f"Report size: {output_path.stat().st_size / 1024:.1f} KB")

    def _generate_html(self, data: Dict[str, Any]) -> str:
        """
        Generate HTML from template or inline.

        Args:
            data: Template data

        Returns:
            HTML string
        """
        if self.env:
            try:
                template = self.env.get_template('report_template.html')
                return template.render(**data)
            except Exception as e:
                logger.warning(f"Could not render template: {e}, using inline HTML")

        # Fallback to inline HTML generation
        return self._generate_inline_html(data)

    def _generate_inline_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML without external templates."""

        # Extract data
        findings = data['findings']
        stats = data['statistics']
        overall = data['overall_risk']
        plugins = data['plugin_scores']
        frameworks = data['framework_summary']

        # Severity counts
        critical_count = stats.get('by_severity', {}).get('CRITICAL', 0)
        high_count = stats.get('by_severity', {}).get('HIGH', 0)
        medium_count = stats.get('by_severity', {}).get('MEDIUM', 0)
        low_count = stats.get('by_severity', {}).get('LOW', 0)

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['report_title']} - {data['company_name']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: #1a1a2e;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, {data['primary_color']} 0%, {data['secondary_color']} 100%);
            padding: 40px;
            text-align: center;
            color: white;
        }}

        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .executive-summary {{
            background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(139,92,246,0.1) 100%);
            border-left: 4px solid {data['primary_color']};
            padding: 30px;
            margin-bottom: 40px;
            border-radius: 8px;
        }}

        .executive-summary h2 {{
            color: {data['primary_color']};
            margin-bottom: 20px;
            font-size: 1.8rem;
        }}

        .risk-level {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 24px;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 10px 0;
        }}

        .risk-CRITICAL {{ background: #dc2626; color: white; }}
        .risk-HIGH {{ background: #ea580c; color: white; }}
        .risk-MEDIUM {{ background: #f59e0b; color: white; }}
        .risk-LOW {{ background: #10b981; color: white; }}
        .risk-MINIMAL {{ background: #3b82f6; color: white; }}
        .risk-NONE {{ background: #6b7280; color: white; }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .stat-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}

        .stat-card .value {{
            font-size: 3rem;
            font-weight: 700;
            margin: 10px 0;
            background: linear-gradient(135deg, {data['primary_color']}, {data['accent_color']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-card .label {{
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.7;
        }}

        .severity-CRITICAL {{ color: #dc2626; }}
        .severity-HIGH {{ color: #ea580c; }}
        .severity-MEDIUM {{ color: #f59e0b; }}
        .severity-LOW {{ color: #10b981; }}

        .section {{
            margin: 40px 0;
        }}

        .section h2 {{
            font-size: 1.8rem;
            margin-bottom: 24px;
            color: {data['primary_color']};
            border-bottom: 2px solid {data['primary_color']};
            padding-bottom: 10px;
        }}

        .finding-card {{
            background: rgba(255,255,255,0.03);
            border-left: 4px solid;
            margin: 20px 0;
            padding: 20px;
            border-radius: 8px;
        }}

        .finding-card.CRITICAL {{ border-left-color: #dc2626; }}
        .finding-card.HIGH {{ border-left-color: #ea580c; }}
        .finding-card.MEDIUM {{ border-left-color: #f59e0b; }}
        .finding-card.LOW {{ border-left-color: #10b981; }}

        .finding-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .finding-title {{
            font-size: 1.2rem;
            font-weight: 600;
        }}

        .severity-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .severity-badge.CRITICAL {{ background: #dc2626; color: white; }}
        .severity-badge.HIGH {{ background: #ea580c; color: white; }}
        .severity-badge.MEDIUM {{ background: #f59e0b; color: white; }}
        .severity-badge.LOW {{ background: #10b981; color: white; }}

        .plugin-name {{
            font-family: 'Courier New', monospace;
            color: {data['accent_color']};
            font-size: 0.9rem;
        }}

        code {{
            background: rgba(0,0,0,0.4);
            padding: 12px;
            border-radius: 4px;
            display: block;
            margin: 10px 0;
            overflow-x: auto;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.85rem;
            line-height: 1.4;
        }}

        .framework-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }}

        .framework-tag {{
            background: rgba(99,102,241,0.2);
            color: {data['primary_color']};
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            overflow: hidden;
        }}

        th {{
            background: rgba(99,102,241,0.2);
            padding: 12px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}

        tr:hover {{
            background: rgba(255,255,255,0.05);
        }}

        footer {{
            background: #0f0f1a;
            padding: 24px;
            text-align: center;
            color: #888;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}

        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid {data['primary_color']};
            background: transparent;
            color: {data['primary_color']};
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .filter-btn:hover {{
            background: {data['primary_color']};
            color: white;
        }}

        .filter-btn.active {{
            background: {data['primary_color']};
            color: white;
        }}

        @media print {{
            body {{ background: white; color: black; }}
            .container {{ box-shadow: none; }}
            .filter-buttons {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{data['report_title']}</h1>
            <div class="subtitle">{data['company_name']} | Generated: {data['generated_at']}</div>
        </header>

        <div class="content">
            <!-- Executive Summary -->
            <div class="executive-summary">
                <h2>Executive Summary</h2>
                <p><strong>Overall Risk Level:</strong>
                    <span class="risk-level risk-{overall['overall_risk_level']}">
                        {overall['overall_risk_level']}
                    </span>
                </p>
                <p><strong>Risk Score:</strong> {overall['overall_risk_score']}/100</p>
                <p style="margin-top: 16px; font-size: 1.05rem;">
                    Analyzed <strong>{stats['total_plugins']}</strong> plugins and identified
                    <strong>{stats['total_findings']}</strong> findings after context-aware filtering.
                    The assessment identified <strong>{overall['critical_risk_count'] + overall['high_risk_count']}</strong>
                    high-priority plugins requiring immediate attention.
                </p>
            </div>

            <!-- Key Statistics -->
            <div class="section">
                <h2>Key Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">Total Plugins</div>
                        <div class="value">{stats['total_plugins']}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Total Findings</div>
                        <div class="value">{stats['total_findings']}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label severity-CRITICAL">Critical</div>
                        <div class="value severity-CRITICAL">{critical_count}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label severity-HIGH">High</div>
                        <div class="value severity-HIGH">{high_count}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label severity-MEDIUM">Medium</div>
                        <div class="value severity-MEDIUM">{medium_count}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label severity-LOW">Low</div>
                        <div class="value severity-LOW">{low_count}</div>
                    </div>
                </div>
            </div>

            <!-- Top Risky Plugins -->
            <div class="section">
                <h2>Top 10 Risky Plugins</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Plugin Name</th>
                            <th>Risk Score</th>
                            <th>Risk Level</th>
                            <th>Findings</th>
                            <th>CRITICAL</th>
                            <th>HIGH</th>
                        </tr>
                    </thead>
                    <tbody>"""

        # Add top 10 risky plugins
        for plugin in plugins[:10]:
            severity_dist = plugin.get('severity_distribution', {})
            crit = severity_dist.get('CRITICAL', 0)
            high = severity_dist.get('HIGH', 0)

            html += f"""
                        <tr>
                            <td><span class="plugin-name">{plugin.get('plugin_name', 'unknown')}</span></td>
                            <td><strong>{plugin['risk_score']}</strong></td>
                            <td><span class="risk-level risk-{plugin['risk_level']}">{plugin['risk_level']}</span></td>
                            <td>{plugin['real_finding_count']}/{plugin['finding_count']}</td>
                            <td class="severity-CRITICAL"><strong>{crit}</strong></td>
                            <td class="severity-HIGH"><strong>{high}</strong></td>
                        </tr>"""

        html += """
                    </tbody>
                </table>
            </div>

            <!-- Critical Findings -->
            <div class="section">
                <h2>Critical Findings</h2>"""

        critical_findings = [f for f in findings if f.get('severity') == 'CRITICAL'][:10]
        if critical_findings:
            for finding in critical_findings:
                category = finding.get('category', 'Unknown')
                plugin = finding.get('plugin_name', 'unknown')
                description = finding.get('description', 'No description')
                code = finding.get('code_snippet', '')

                # Framework tags
                attack_techs = finding.get('att&ck_techniques', [])
                owasp = finding.get('owasp_categories', [])

                html += f"""
                <div class="finding-card CRITICAL">
                    <div class="finding-header">
                        <div class="finding-title">{category}</div>
                        <span class="severity-badge CRITICAL">CRITICAL</span>
                    </div>
                    <div class="plugin-name">Plugin: {plugin}</div>
                    <p style="margin: 12px 0;">{description}</p>"""

                if code:
                    html += f"""<code>{code[:500]}</code>"""

                if attack_techs or owasp:
                    html += '<div class="framework-tags">'
                    for tech in attack_techs[:3]:
                        html += f'<span class="framework-tag">ATT&CK: {tech}</span>'
                    for cat in owasp[:2]:
                        html += f'<span class="framework-tag">OWASP: {cat}</span>'
                    html += '</div>'

                html += """
                </div>"""
        else:
            html += '<p>No critical findings identified.</p>'

        html += f"""
            </div>

            <!-- Framework Analysis -->
            <div class="section">
                <h2>Framework Coverage</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">MITRE ATT&CK Techniques</div>
                        <div class="value">{frameworks.get('mitre_attack', {}).get('total_techniques', 0)}</div>
                        <div style="margin-top: 8px; opacity: 0.7;">
                            {frameworks.get('mitre_attack', {}).get('coverage_percent', 0)}% coverage
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="label">MITRE ATLAS Techniques</div>
                        <div class="value">{frameworks.get('mitre_atlas', {}).get('total_techniques', 0)}</div>
                        <div style="margin-top: 8px; opacity: 0.7;">
                            {frameworks.get('mitre_atlas', {}).get('coverage_percent', 0)}% coverage
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="label">OWASP Categories</div>
                        <div class="value">{frameworks.get('owasp', {}).get('total_categories', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">CWE Weaknesses</div>
                        <div class="value">{frameworks.get('cwe', {}).get('total_weaknesses', 0)}</div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>{data['footer_text']}</p>
            <p style="margin-top: 8px; font-size: 0.85rem;">
                Report generated by Security Report Builder v1.0.0
            </p>
        </footer>
    </div>

    <script>
        // Simple filtering logic (can be enhanced)
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Security Report loaded successfully');
        }});
    </script>
</body>
</html>"""

        return html


def main():
    """CLI interface for testing the generator."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate HTML security report')
    parser.add_argument('findings', help='Input JSON file with analyzed findings')
    parser.add_argument('--output', required=True, help='Output HTML file')
    parser.add_argument('--config', help='Report config JSON')
    parser.add_argument('--branding', help='Branding config JSON')

    args = parser.parse_args()

    # Load findings
    with open(args.findings, 'r') as f:
        data = json.load(f)

    # Load configs
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)

    branding = {}
    if args.branding:
        with open(args.branding, 'r') as f:
            branding = json.load(f)

    # Generate report
    generator = HTMLReportGenerator()
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

    print(f"\n✓ HTML report generated: {args.output}")
    return 0


if __name__ == '__main__':
    exit(main())
