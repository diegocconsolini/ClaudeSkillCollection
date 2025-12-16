#!/usr/bin/env python3
"""
Generate unified HTML report from all plugin security scan results
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

RESULTS_DIR = Path("plugin-security-checker/archive_scan_results")
OUTPUT_FILE = Path("plugin-security-checker/archive_scan_results/security_report.html")

def load_all_results():
    """Load all JSON scan results"""
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

def generate_statistics(results):
    """Generate comprehensive statistics"""
    stats = {
        'total_plugins': len(results),
        'risk_levels': defaultdict(int),
        'verdicts': defaultdict(int),
        'total_findings': 0,
        'severity_counts': defaultdict(int),
        'category_counts': defaultdict(int),
        'critical_plugins': [],
        'high_risk_plugins': [],
        'medium_risk_plugins': [],
        'low_risk_plugins': [],
        'clean_plugins': []
    }

    for result in results:
        metadata = result.get('metadata', {})
        risk_level = metadata.get('risk_level', 'UNKNOWN')
        verdict = metadata.get('verdict', 'UNKNOWN')
        findings_count = metadata.get('total_findings', 0)

        stats['risk_levels'][risk_level] += 1
        stats['verdicts'][verdict] += 1
        stats['total_findings'] += findings_count

        # Count severities
        severity = metadata.get('summary', {}).get('severity_counts', {})
        for sev, count in severity.items():
            stats['severity_counts'][sev] += count

        # Categorize plugins
        plugin_info = {
            'name': result['plugin_name'],
            'findings': findings_count,
            'risk_score': metadata.get('risk_score', 0),
            'verdict': verdict
        }

        if risk_level == 'CRITICAL':
            stats['critical_plugins'].append(plugin_info)
        elif risk_level == 'HIGH':
            stats['high_risk_plugins'].append(plugin_info)
        elif risk_level == 'MEDIUM':
            stats['medium_risk_plugins'].append(plugin_info)
        elif risk_level == 'LOW':
            stats['low_risk_plugins'].append(plugin_info)
        else:
            stats['clean_plugins'].append(plugin_info)

    # Sort by risk score
    for key in ['critical_plugins', 'high_risk_plugins', 'medium_risk_plugins']:
        stats[key].sort(key=lambda x: x['risk_score'], reverse=True)

    return stats

def generate_html(results, stats):
    """Generate HTML report"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plugin Security Scan Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}

        .stat-card.critical {{
            border-left-color: #dc3545;
        }}

        .stat-card.high {{
            border-left-color: #fd7e14;
        }}

        .stat-card.medium {{
            border-left-color: #ffc107;
        }}

        .stat-card.low {{
            border-left-color: #28a745;
        }}

        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}

        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #667eea;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }}

        .plugin-list {{
            display: grid;
            gap: 15px;
        }}

        .plugin-item {{
            background: #f9f9f9;
            padding: 15px 20px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 4px solid #ddd;
        }}

        .plugin-item.critical {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}

        .plugin-item.high {{
            border-left-color: #fd7e14;
            background: #fff8f0;
        }}

        .plugin-item.medium {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}

        .plugin-name {{
            font-weight: 600;
            font-size: 1.1em;
            color: #333;
            font-family: 'Courier New', monospace;
        }}

        .plugin-meta {{
            display: flex;
            gap: 20px;
            align-items: center;
        }}

        .badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge.critical {{
            background: #dc3545;
            color: white;
        }}

        .badge.high {{
            background: #fd7e14;
            color: white;
        }}

        .badge.medium {{
            background: #ffc107;
            color: #333;
        }}

        .badge.low {{
            background: #28a745;
            color: white;
        }}

        .badge.pass {{
            background: #28a745;
            color: white;
        }}

        .badge.fail {{
            background: #dc3545;
            color: white;
        }}

        .badge.review {{
            background: #ffc107;
            color: #333;
        }}

        .findings-count {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}

        .chart-container {{
            margin: 20px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}

        .chart {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
        }}

        .chart h3 {{
            margin-bottom: 15px;
            color: #667eea;
        }}

        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .bar-label {{
            min-width: 100px;
            font-weight: 600;
            font-size: 0.9em;
        }}

        .bar {{
            flex: 1;
            height: 30px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-weight: 600;
        }}

        .bar.critical {{ background: linear-gradient(90deg, #dc3545 0%, #c82333 100%); }}
        .bar.high {{ background: linear-gradient(90deg, #fd7e14 0%, #e8590c 100%); }}
        .bar.medium {{ background: linear-gradient(90deg, #ffc107 0%, #e0a800 100%); }}
        .bar.low {{ background: linear-gradient(90deg, #28a745 0%, #218838 100%); }}

        footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            margin-top: 50px;
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
            margin-top: 10px;
        }}

        .collapsible-content.show {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 Plugin Security Scan Report</h1>
            <div class="subtitle">
                Comprehensive security analysis of {stats['total_plugins']} Claude Code plugins<br>
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_plugins']}</div>
                <div class="stat-label">Total Plugins Scanned</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['total_findings']}</div>
                <div class="stat-label">Total Security Findings</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value" style="color: #dc3545;">{len(stats['critical_plugins'])}</div>
                <div class="stat-label">Critical Risk</div>
            </div>
            <div class="stat-card high">
                <div class="stat-value" style="color: #fd7e14;">{len(stats['high_risk_plugins'])}</div>
                <div class="stat-label">High Risk</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-value" style="color: #ffc107;">{len(stats['medium_risk_plugins'])}</div>
                <div class="stat-label">Medium Risk</div>
            </div>
            <div class="stat-card low">
                <div class="stat-value" style="color: #28a745;">{len(stats['low_risk_plugins'])}</div>
                <div class="stat-label">Low/Clean</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 Distribution Analysis</h2>
            <div class="chart-container">
                <div class="chart">
                    <h3>Risk Levels</h3>
                    <div class="bar-chart">
"""

    # Risk level bars
    total = stats['total_plugins']
    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = stats['risk_levels'].get(level, 0)
        percentage = (count / total * 100) if total > 0 else 0
        width = percentage
        color_class = level.lower()
        html += f"""
                        <div class="bar-item">
                            <div class="bar-label">{level}</div>
                            <div class="bar {color_class}" style="width: {width}%;">{count}</div>
                        </div>
"""

    html += """
                    </div>
                </div>

                <div class="chart">
                    <h3>Severity Breakdown</h3>
                    <div class="bar-chart">
"""

    # Severity bars
    max_sev = max(stats['severity_counts'].values()) if stats['severity_counts'] else 1
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
        count = stats['severity_counts'].get(severity, 0)
        percentage = (count / max_sev * 100) if max_sev > 0 else 0
        color_class = severity.lower()
        html += f"""
                        <div class="bar-item">
                            <div class="bar-label">{severity}</div>
                            <div class="bar {color_class}" style="width: {percentage}%;">{count}</div>
                        </div>
"""

    html += """
                    </div>
                </div>
            </div>
        </div>
"""

    # Critical plugins section
    if stats['critical_plugins']:
        html += f"""
        <div class="section">
            <h2 class="expandable expanded" onclick="toggleSection(this)">🚨 Critical Risk Plugins ({len(stats['critical_plugins'])})</h2>
            <div class="collapsible-content show">
                <div class="plugin-list">
"""
        for plugin in stats['critical_plugins'][:50]:  # Show top 50
            html += f"""
                    <div class="plugin-item critical">
                        <span class="plugin-name">{plugin['name']}</span>
                        <div class="plugin-meta">
                            <span class="findings-count">{plugin['findings']} findings</span>
                            <span class="badge critical">{plugin['verdict']}</span>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
        </div>
"""

    # High risk plugins
    if stats['high_risk_plugins']:
        html += f"""
        <div class="section">
            <h2 class="expandable expanded" onclick="toggleSection(this)">⚠️ High Risk Plugins ({len(stats['high_risk_plugins'])})</h2>
            <div class="collapsible-content show">
                <div class="plugin-list">
"""
        for plugin in stats['high_risk_plugins'][:50]:
            html += f"""
                    <div class="plugin-item high">
                        <span class="plugin-name">{plugin['name']}</span>
                        <div class="plugin-meta">
                            <span class="findings-count">{plugin['findings']} findings</span>
                            <span class="badge high">{plugin['verdict']}</span>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
        </div>
"""

    # Medium risk plugins (collapsed by default)
    if stats['medium_risk_plugins']:
        html += f"""
        <div class="section">
            <h2 class="expandable" onclick="toggleSection(this)">⚡ Medium Risk Plugins ({len(stats['medium_risk_plugins'])})</h2>
            <div class="collapsible-content">
                <div class="plugin-list">
"""
        for plugin in stats['medium_risk_plugins'][:100]:
            html += f"""
                    <div class="plugin-item medium">
                        <span class="plugin-name">{plugin['name']}</span>
                        <div class="plugin-meta">
                            <span class="findings-count">{plugin['findings']} findings</span>
                            <span class="badge medium">{plugin['verdict']}</span>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
        </div>
"""

    # Low/Clean plugins (collapsed)
    clean_count = len(stats['low_risk_plugins']) + len(stats['clean_plugins'])
    if clean_count > 0:
        html += f"""
        <div class="section">
            <h2 class="expandable" onclick="toggleSection(this)">✅ Low Risk / Clean Plugins ({clean_count})</h2>
            <div class="collapsible-content">
                <p style="color: #666; margin-bottom: 15px;">These plugins passed security checks with no significant findings.</p>
                <div class="plugin-list">
"""
        all_clean = stats['low_risk_plugins'] + stats['clean_plugins']
        for plugin in sorted(all_clean, key=lambda x: x['name'])[:200]:
            html += f"""
                    <div class="plugin-item">
                        <span class="plugin-name">{plugin['name']}</span>
                        <div class="plugin-meta">
                            <span class="badge pass">{plugin['verdict']}</span>
                        </div>
                    </div>
"""
        html += """
                </div>
            </div>
        </div>
"""

    html += """
        <footer>
            <p>🔒 Plugin Security Checker v3.0 | Generated by ClaudeSkillCollection</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                ⚠️ This report provides preliminary security analysis. Always review plugin source code manually before installation.
            </p>
        </footer>
    </div>

    <script>
        function toggleSection(element) {
            element.classList.toggle('expanded');
            const content = element.nextElementSibling;
            content.classList.toggle('show');
        }
    </script>
</body>
</html>
"""

    return html

def main():
    print("🔍 Loading scan results...")
    results = load_all_results()
    print(f"✅ Loaded {len(results)} plugin scan results")

    print("📊 Generating statistics...")
    stats = generate_statistics(results)

    print("🎨 Creating HTML report...")
    html = generate_html(results, stats)

    print(f"💾 Saving to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"✅ HTML report generated successfully!")
    print(f"   File: {OUTPUT_FILE}")
    print(f"   Size: {file_size:.1f} KB")
    print(f"\n📊 Report Summary:")
    print(f"   Total Plugins: {stats['total_plugins']}")
    print(f"   Total Findings: {stats['total_findings']}")
    print(f"   Critical: {len(stats['critical_plugins'])}")
    print(f"   High: {len(stats['high_risk_plugins'])}")
    print(f"   Medium: {len(stats['medium_risk_plugins'])}")
    print(f"   Low/Clean: {len(stats['low_risk_plugins']) + len(stats['clean_plugins'])}")

if __name__ == "__main__":
    main()
