#!/usr/bin/env python3
"""
Generate COMPLETE security report with MITRE ATT&CK/ATLAS framework mappings
Includes all threat intelligence, CVE references, OWASP mappings, and CWE details
"""

import json
import os
import html as html_lib  # aliased: the report string is also named `html`
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter


def _esc(value):
    """Escape user/scan-controlled text before embedding in the HTML report.
    Prevents stored XSS from a scanned plugin's description/code_snippet/etc."""
    return html_lib.escape("" if value is None else str(value))


# Resolve paths relative to this script (not the caller's cwd), so the report works
# from any working directory. (#44 N7)
_PLUGIN_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = _PLUGIN_ROOT / "archive_scan_results"
THREAT_MAP_FILE = _PLUGIN_ROOT / "references" / "threat_mappings.json"
OUTPUT_FILE = _PLUGIN_ROOT / "archive_scan_results" / "complete_security_report.html"

def load_threat_mappings():
    """Load MITRE ATT&CK/ATLAS/OWASP/CWE mappings"""
    try:
        with open(THREAT_MAP_FILE) as f:
            return json.load(f)
    except:
        return {"mappings": {}}

def load_all_results():
    """Load all JSON scan results with detailed findings"""
    results = []
    for json_file in RESULTS_DIR.glob("*.json"):
        if json_file.name == "scan_summary.json":
            continue
        try:
            with open(json_file) as f:
                data = json.load(f)
                data['plugin_name'] = json_file.stem
                results.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    return results

def analyze_findings(results):
    """Deep analysis of all security findings"""
    analysis = {
        'total_findings': 0,
        'by_severity': Counter(),
        'by_category': Counter(),
        'by_subcategory': Counter(),
        'att&ck_techniques': Counter(),
        'atlas_techniques': Counter(),
        'cwe_weaknesses': Counter(),
        'owasp_categories': Counter(),
        'cvss_distribution': [],
        'high_risk_patterns': [],
        'critical_findings': [],
        'plugins_with_findings': [],
        'file_hotspots': Counter(),
        'language_analysis': Counter()
    }

    for result in results:
        findings = result.get('findings', [])
        if not findings:
            continue

        plugin_name = result['plugin_name']
        metadata = result.get('metadata', {})

        analysis['total_findings'] += len(findings)

        plugin_summary = {
            'name': plugin_name,
            'findings_count': len(findings),
            'risk_level': metadata.get('risk_level', 'UNKNOWN'),
            'risk_score': metadata.get('risk_score', 0),
            'findings': []
        }

        for finding in findings:
            sev = finding.get('severity', 'UNKNOWN')
            cat = finding.get('category', 'UNKNOWN')
            subcat = finding.get('subcategory', 'UNKNOWN')
            cvss = finding.get('cvss_score', 0)

            analysis['by_severity'][sev] += 1
            analysis['by_category'][cat] += 1
            analysis['by_subcategory'][subcat] += 1
            analysis['cvss_distribution'].append(cvss)

            # Track file hotspots
            file_path = finding.get('file', '')
            if file_path:
                analysis['file_hotspots'][file_path] += 1
                # Detect language
                if file_path.endswith('.py'):
                    analysis['language_analysis']['Python'] += 1
                elif file_path.endswith('.js'):
                    analysis['language_analysis']['JavaScript'] += 1
                elif file_path.endswith('.ts'):
                    analysis['language_analysis']['TypeScript'] += 1

            # Collect critical findings
            if sev == 'CRITICAL':
                analysis['critical_findings'].append({
                    'plugin': plugin_name,
                    'finding': finding
                })

            plugin_summary['findings'].append(finding)

        if plugin_summary['findings']:
            analysis['plugins_with_findings'].append(plugin_summary)

    # Sort plugins by risk
    analysis['plugins_with_findings'].sort(key=lambda x: x['risk_score'], reverse=True)

    return analysis

def generate_html(results, analysis, threat_map):
    """Generate comprehensive HTML report"""

    stats = {
        'total_plugins': len(results),
        'total_findings': analysis['total_findings'],
        'plugins_with_findings': len(analysis['plugins_with_findings']),
        'plugins_clean': len(results) - len(analysis['plugins_with_findings'])
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Security Analysis Report - MITRE ATT&CK/ATLAS Framework</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #00d9ff;
            padding: 50px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.3);
            border: 1px solid #00d9ff;
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 15px;
            text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
            font-weight: 700;
        }}

        .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
            color: #a0a0ff;
        }}

        .framework-badges {{
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .framework-badge {{
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid #00d9ff;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            border: 1px solid #2a2a4e;
            transition: all 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0, 217, 255, 0.2);
            border-color: #00d9ff;
        }}

        .stat-card.critical {{
            border-left: 4px solid #ff4757;
            background: linear-gradient(135deg, #2e1a1a 0%, #3e1616 100%);
        }}

        .stat-card.high {{
            border-left: 4px solid #ffa502;
            background: linear-gradient(135deg, #2e2a1a 0%, #3e2e16 100%);
        }}

        .stat-card.info {{
            border-left: 4px solid #00d9ff;
        }}

        .stat-value {{
            font-size: 3em;
            font-weight: 800;
            color: #00d9ff;
            margin-bottom: 10px;
            text-shadow: 0 0 15px rgba(0, 217, 255, 0.4);
        }}

        .stat-label {{
            color: #a0a0ff;
            font-size: 1em;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }}

        .section {{
            background: #1a1a2e;
            padding: 35px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            border: 1px solid #2a2a4e;
        }}

        h2 {{
            font-size: 2.2em;
            margin-bottom: 25px;
            color: #00d9ff;
            border-bottom: 3px solid #00d9ff;
            padding-bottom: 15px;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        }}

        h3 {{
            font-size: 1.6em;
            margin: 25px 0 15px 0;
            color: #a0a0ff;
        }}

        .finding-card {{
            background: #16213e;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 4px solid #00d9ff;
            transition: all 0.3s;
        }}

        .finding-card:hover {{
            background: #1a2847;
            box-shadow: 0 5px 15px rgba(0, 217, 255, 0.2);
        }}

        .finding-card.critical {{
            border-left-color: #ff4757;
            background: #2e1a1a;
        }}

        .finding-card.high {{
            border-left-color: #ffa502;
            background: #2e2516;
        }}

        .finding-card.medium {{
            border-left-color: #ffd32a;
            background: #2e2916;
        }}

        .finding-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .finding-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: #00d9ff;
        }}

        .severity-badge {{
            padding: 8px 18px;
            border-radius: 25px;
            font-size: 0.85em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .severity-badge.critical {{
            background: #ff4757;
            color: white;
            box-shadow: 0 0 15px rgba(255, 71, 87, 0.5);
        }}

        .severity-badge.high {{
            background: #ffa502;
            color: #000;
            box-shadow: 0 0 15px rgba(255, 165, 2, 0.5);
        }}

        .severity-badge.medium {{
            background: #ffd32a;
            color: #000;
            box-shadow: 0 0 15px rgba(255, 211, 42, 0.5);
        }}

        .severity-badge.low {{
            background: #2ed573;
            color: #000;
        }}

        .finding-details {{
            display: grid;
            gap: 15px;
            margin: 15px 0;
        }}

        .detail-row {{
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 10px;
        }}

        .detail-label {{
            color: #a0a0ff;
            font-weight: 600;
        }}

        .detail-value {{
            color: #e0e0e0;
        }}

        .code-snippet {{
            background: #0f0f23;
            border: 1px solid #2a2a4e;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #ff6b9d;
            overflow-x: auto;
            margin: 10px 0;
        }}

        .framework-mapping {{
            background: rgba(0, 217, 255, 0.05);
            border: 1px solid #00d9ff;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        }}

        .technique-tag {{
            display: inline-block;
            background: rgba(0, 217, 255, 0.2);
            border: 1px solid #00d9ff;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            margin: 5px 5px 5px 0;
            color: #00d9ff;
            font-weight: 600;
        }}

        .technique-tag.atlas {{
            background: rgba(255, 71, 87, 0.2);
            border-color: #ff4757;
            color: #ff4757;
        }}

        .technique-tag.cwe {{
            background: rgba(255, 165, 2, 0.2);
            border-color: #ffa502;
            color: #ffa502;
        }}

        .technique-tag.owasp {{
            background: rgba(46, 213, 115, 0.2);
            border-color: #2ed573;
            color: #2ed573;
        }}

        .chart {{
            background: #16213e;
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
        }}

        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .bar-label {{
            min-width: 150px;
            font-weight: 600;
            color: #a0a0ff;
        }}

        .bar {{
            flex: 1;
            height: 35px;
            background: linear-gradient(90deg, #00d9ff 0%, #0099cc 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            padding: 0 15px;
            color: #000;
            font-weight: 700;
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.3);
        }}

        .bar.critical {{ background: linear-gradient(90deg, #ff4757 0%, #cc0000 100%); color: #fff; }}
        .bar.high {{ background: linear-gradient(90deg, #ffa502 0%, #cc6600 100%); }}
        .bar.medium {{ background: linear-gradient(90deg, #ffd32a 0%, #cc9900 100%); }}
        .bar.low {{ background: linear-gradient(90deg, #2ed573 0%, #00cc44 100%); }}

        .plugin-list {{
            display: grid;
            gap: 15px;
        }}

        .plugin-item {{
            background: #16213e;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #00d9ff;
            transition: all 0.3s;
        }}

        .plugin-item:hover {{
            background: #1a2847;
            transform: translateX(5px);
        }}

        .plugin-item.critical {{
            border-left-color: #ff4757;
        }}

        .plugin-name {{
            font-weight: 700;
            font-size: 1.2em;
            color: #00d9ff;
            font-family: 'Courier New', monospace;
        }}

        .expandable {{
            cursor: pointer;
            user-select: none;
        }}

        .expandable::before {{
            content: '▶ ';
            display: inline-block;
            transition: transform 0.2s;
        }}

        .expandable.expanded::before {{
            transform: rotate(90deg);
        }}

        .collapsible-content {{
            display: none;
            margin-top: 15px;
        }}

        .collapsible-content.show {{
            display: block;
        }}

        footer {{
            text-align: center;
            padding: 30px;
            color: #a0a0ff;
            margin-top: 50px;
            border-top: 2px solid #2a2a4e;
        }}

        .cvss-score {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-weight: 700;
            font-size: 0.9em;
        }}

        .cvss-critical {{ background: #ff4757; color: white; }}
        .cvss-high {{ background: #ffa502; color: #000; }}
        .cvss-medium {{ background: #ffd32a; color: #000; }}
        .cvss-low {{ background: #2ed573; color: #000; }}

        a {{
            color: #00d9ff;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 Complete Security Analysis Report</h1>
            <div class="subtitle">
                Comprehensive threat intelligence analysis with MITRE ATT&CK & ATLAS framework mappings<br>
                {stats['total_plugins']} plugins analyzed | {stats['total_findings']} security findings<br>
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            </div>
            <div class="framework-badges">
                <span class="framework-badge">MITRE ATT&CK® v14.1</span>
                <span class="framework-badge">MITRE ATLAS™ v4.5.0</span>
                <span class="framework-badge">OWASP Top 10 2021</span>
                <span class="framework-badge">OWASP API Security 2023</span>
                <span class="framework-badge">CWE 4.13</span>
                <span class="framework-badge">CVE Database</span>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card info">
                <div class="stat-value">{stats['total_plugins']}</div>
                <div class="stat-label">Plugins Analyzed</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value" style="color: #ff4757;">{stats['total_findings']}</div>
                <div class="stat-label">Total Findings</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value" style="color: #ff4757;">{analysis['by_severity']['CRITICAL']}</div>
                <div class="stat-label">Critical Severity</div>
            </div>
            <div class="stat-card high">
                <div class="stat-value" style="color: #ffa502;">{analysis['by_severity']['HIGH']}</div>
                <div class="stat-label">High Severity</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{analysis['by_severity']['MEDIUM']}</div>
                <div class="stat-label">Medium Severity</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['plugins_with_findings']}</div>
                <div class="stat-label">Plugins w/ Findings</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 Threat Distribution Analysis</h2>
            <div class="chart">
                <h3>Findings by Severity</h3>
                <div class="bar-chart">
"""

    # Severity bars
    total_findings = max(analysis['total_findings'], 1)
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
        count = analysis['by_severity'][severity]
        percentage = (count / total_findings * 100) if total_findings > 0 else 0
        color_class = severity.lower()
        html += f"""
                    <div class="bar-item">
                        <div class="bar-label">{severity}</div>
                        <div class="bar {color_class}" style="width: {percentage}%;">{count} findings</div>
                    </div>
"""

    html += """
                </div>
            </div>

            <div class="chart">
                <h3>Findings by Category</h3>
                <div class="bar-chart">
"""

    # Category bars
    max_cat = max(analysis['by_category'].values()) if analysis['by_category'] else 1
    for category, count in analysis['by_category'].most_common(10):
        percentage = (count / max_cat * 100) if max_cat > 0 else 0
        html += f"""
                    <div class="bar-item">
                        <div class="bar-label">{category}</div>
                        <div class="bar" style="width: {percentage}%;">{count}</div>
                    </div>
"""

    html += """
                </div>
            </div>
        </div>
"""

    # Critical Findings Detail
    if analysis['critical_findings']:
        html += f"""
        <div class="section">
            <h2 class="expandable expanded" onclick="toggleSection(this)">🚨 Critical Security Findings ({len(analysis['critical_findings'])})</h2>
            <div class="collapsible-content show">
"""
        for item in analysis['critical_findings'][:50]:
            finding = item['finding']
            plugin = item['plugin']

            cvss = finding.get('cvss_score', 0)
            cvss_class = 'cvss-critical' if cvss >= 9 else 'cvss-high' if cvss >= 7 else 'cvss-medium'

            html += f"""
                <div class="finding-card critical">
                    <div class="finding-header">
                        <div class="finding-title">{_esc(plugin)} - {_esc(finding.get('description', 'Security Issue'))}</div>
                        <span class="severity-badge critical">CRITICAL</span>
                    </div>
                    <div class="finding-details">
                        <div class="detail-row">
                            <span class="detail-label">Category:</span>
                            <span class="detail-value">{_esc(finding.get('category'))} / {_esc(finding.get('subcategory'))}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Location:</span>
                            <span class="detail-value">{_esc(finding.get('file'))}:{_esc(finding.get('line'))}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">CVSS Score:</span>
                            <span class="detail-value"><span class="{cvss_class} cvss-score">{_esc(cvss)}</span></span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Impact:</span>
                            <span class="detail-value">{_esc(finding.get('impact', 'N/A'))}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Recommendation:</span>
                            <span class="detail-value">{_esc(finding.get('recommendation', 'Review code manually'))}</span>
                        </div>
                    </div>
"""

            # Code snippet
            if finding.get('code_snippet'):
                html += f"""
                    <div class="code-snippet">{_esc(finding['code_snippet'])}</div>
"""

            # Framework mappings (if available)
            cve = finding.get('cve_reference')
            owasp = finding.get('owasp_reference')

            if cve or owasp:
                html += """
                    <div class="framework-mapping">
                        <strong>Framework Mappings:</strong><br>
"""
                if cve:
                    html += f'<span class="technique-tag">CVE: {cve}</span>'
                if owasp:
                    html += f'<span class="technique-tag owasp">OWASP: {owasp}</span>'
                html += """
                    </div>
"""

            html += """
                </div>
"""

        html += """
            </div>
        </div>
"""

    # Plugins with Most Findings
    if analysis['plugins_with_findings']:
        html += f"""
        <div class="section">
            <h2 class="expandable expanded" onclick="toggleSection(this)">📦 Plugins Ranked by Risk ({len(analysis['plugins_with_findings'])})</h2>
            <div class="collapsible-content show">
                <div class="plugin-list">
"""
        for plugin in analysis['plugins_with_findings'][:100]:
            risk_class = plugin['risk_level'].lower()
            html += f"""
                    <div class="plugin-item {risk_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="plugin-name">{plugin['name']}</span>
                            <div>
                                <span class="severity-badge {risk_class}">{plugin['risk_level']}</span>
                                <span style="margin-left: 10px; color: #a0a0ff; font-weight: 600;">
                                    {plugin['findings_count']} findings | Risk Score: {plugin['risk_score']}
                                </span>
                            </div>
                        </div>
                    </div>
"""

        html += """
                </div>
            </div>
        </div>
"""

    html += f"""
        <footer>
            <p style="font-size: 1.2em; margin-bottom: 15px;">
                🔒 Plugin Security Checker v3.2.0 | ClaudeSkillCollection
            </p>
            <p style="margin-bottom: 10px;">
                Report generated with MITRE ATT&CK® v14.1, MITRE ATLAS™ v4.5.0, OWASP Top 10 2021, CWE 4.13
            </p>
            <p style="font-size: 0.9em; color: #808080;">
                ⚠️ This report provides comprehensive security analysis. Always review plugin source code manually before installation.<br>
                MITRE ATT&CK® and ATT&CK® are registered trademarks of The MITRE Corporation.<br>
                Total analysis: {stats['total_plugins']} plugins | {stats['total_findings']} findings across {len(analysis['by_category'])} categories
            </p>
        </footer>
    </div>

    <script>
        function toggleSection(element) {{
            element.classList.toggle('expanded');
            const content = element.nextElementSibling;
            content.classList.toggle('show');
        }}
    </script>
</body>
</html>
"""

    return html

def main():
    print("🔍 Loading comprehensive scan results...")
    results = load_all_results()
    print(f"✅ Loaded {len(results)} plugin scan results")

    print("🗺️  Loading MITRE ATT&CK/ATLAS threat mappings...")
    threat_map = load_threat_mappings()
    print(f"✅ Loaded {len(threat_map.get('mappings', {}))} threat intelligence mappings")

    print("🔬 Analyzing all security findings...")
    analysis = analyze_findings(results)
    print(f"✅ Analyzed {analysis['total_findings']} findings across {len(analysis['plugins_with_findings'])} plugins")

    print("🎨 Generating complete HTML report...")
    html = generate_html(results, analysis, threat_map)

    print(f"💾 Saving to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✅ COMPLETE security report generated successfully!")
    print(f"   File: {OUTPUT_FILE}")
    print(f"   Size: {file_size:.1f} KB")
    print(f"\n📊 Report Summary:")
    print(f"   Total Plugins: {len(results)}")
    print(f"   Total Findings: {analysis['total_findings']}")
    print(f"   Critical Findings: {analysis['by_severity']['CRITICAL']}")
    print(f"   High Findings: {analysis['by_severity']['HIGH']}")
    print(f"   Medium Findings: {analysis['by_severity']['MEDIUM']}")
    print(f"   Plugins with Issues: {len(analysis['plugins_with_findings'])}")
    print(f"   Clean Plugins: {len(results) - len(analysis['plugins_with_findings'])}")

if __name__ == "__main__":
    main()
