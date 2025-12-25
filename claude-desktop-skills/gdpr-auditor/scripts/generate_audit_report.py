#!/usr/bin/env python3
"""
GDPR Audit Report Generator - Static File Analysis Tool

Generates comprehensive GDPR compliance audit reports in Markdown format from
JSON findings collected by other analysis scripts.

IMPORTANT - STATIC ANALYSIS ONLY:
This script processes JSON files and generates Markdown reports. It does NOT:
- Connect to any external systems or services
- Execute code or make network requests
- Access databases or live applications
- Require credentials or system access
- Monitor or analyze runtime behavior
- Modify any files except the output report

Analyzes: JSON files containing audit findings from other scanning tools
Purpose: Format findings into professional GDPR compliance audit reports
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any
import os

def load_findings(findings_file: str) -> Dict[str, Any]:
    """Load findings from JSON file."""
    try:
        with open(findings_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Findings file '{findings_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{findings_file}'")
        sys.exit(1)

def categorize_findings(findings: Dict[str, Any]) -> Dict[str, List]:
    """Categorize findings by risk level."""
    categorized = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': [],
        'compliant': []
    }

    for category, items in findings.items():
        if isinstance(items, list):
            for item in items:
                risk = item.get('risk_level', 'medium').lower()
                if risk in categorized:
                    categorized[risk].append({
                        'category': category,
                        'item': item
                    })

    return categorized

def generate_executive_summary(categorized: Dict[str, List], metadata: Dict[str, Any]) -> str:
    """Generate executive summary section."""
    total_issues = sum(len(categorized[level]) for level in ['critical', 'high', 'medium', 'low'])

    summary = f"""# GDPR Compliance Audit Report

## Executive Summary

**Audit Date:** {metadata.get('audit_date', datetime.now().strftime('%Y-%m-%d'))}
**Auditor:** {metadata.get('auditor', 'GDPR Auditor')}
**System/Application:** {metadata.get('system_name', 'N/A')}
**Scope:** {metadata.get('scope', 'Full GDPR compliance audit')}

### Overall Assessment

This audit identified **{total_issues} compliance issues** requiring attention:

- **Critical Issues:** {len(categorized['critical'])} - Immediate action required
- **High-Priority Issues:** {len(categorized['high'])} - Action needed within 30 days
- **Medium-Priority Issues:** {len(categorized['medium'])} - Action needed within 90 days
- **Low-Priority Issues:** {len(categorized['low'])} - Recommended improvements

**Compliance Rating:** {calculate_compliance_rating(categorized)}

### Key Findings

"""

    # Add top 3 critical/high issues
    top_issues = categorized['critical'][:3] if categorized['critical'] else categorized['high'][:3]

    if top_issues:
        summary += "**Most Critical Issues:**\n\n"
        for idx, finding in enumerate(top_issues, 1):
            item = finding['item']
            summary += f"{idx}. {item.get('description', 'Issue identified')}\n"
            summary += f"   - **GDPR Article:** {item.get('gdpr_article', 'N/A')}\n"
            summary += f"   - **Risk:** {item.get('risk_level', 'N/A')}\n\n"

    summary += "\n---\n\n"
    return summary

def calculate_compliance_rating(categorized: Dict[str, List]) -> str:
    """Calculate overall compliance rating."""
    critical = len(categorized['critical'])
    high = len(categorized['high'])
    medium = len(categorized['medium'])
    low = len(categorized['low'])

    if critical > 0:
        return "⚠️ **Non-Compliant** - Critical issues present"
    elif high > 5:
        return "⚠️ **Partially Compliant** - Multiple high-priority issues"
    elif high > 0 or medium > 10:
        return "⚡ **Mostly Compliant** - Some improvements needed"
    elif medium > 0 or low > 0:
        return "✓ **Compliant** - Minor improvements recommended"
    else:
        return "✓ **Fully Compliant** - No issues identified"

def generate_findings_section(categorized: Dict[str, List]) -> str:
    """Generate detailed findings sections."""
    output = "## Detailed Findings\n\n"

    risk_levels = [
        ('critical', 'Critical Issues', '🔴'),
        ('high', 'High-Priority Issues', '🟠'),
        ('medium', 'Medium-Priority Issues', '🟡'),
        ('low', 'Low-Priority Issues', '🔵')
    ]

    for level, title, emoji in risk_levels:
        findings = categorized[level]
        if not findings:
            continue

        output += f"### {emoji} {title} ({len(findings)})\n\n"

        for idx, finding in enumerate(findings, 1):
            item = finding['item']
            category = finding['category']

            output += f"#### {idx}. {item.get('title', item.get('description', 'Finding'))}\n\n"
            output += f"**Category:** {category}\n\n"

            if 'gdpr_article' in item:
                output += f"**GDPR Article(s):** {item['gdpr_article']}\n\n"

            if 'description' in item:
                output += f"**Description:**\n{item['description']}\n\n"

            if 'current_implementation' in item:
                output += f"**Current Implementation:**\n{item['current_implementation']}\n\n"

            if 'risk_description' in item:
                output += f"**Risk:**\n{item['risk_description']}\n\n"

            if 'recommendation' in item:
                output += f"**Recommendation:**\n{item['recommendation']}\n\n"

            if 'code_reference' in item:
                output += f"**Code Reference:**\n```\n{item['code_reference']}\n```\n\n"

            if 'priority' in item:
                output += f"**Priority:** {item['priority']}\n\n"

            output += "---\n\n"

    return output

def generate_compliant_areas(categorized: Dict[str, List]) -> str:
    """Generate section on compliant areas."""
    output = "## ✅ Compliant Areas\n\n"

    if categorized['compliant']:
        output += "The following areas were found to be compliant with GDPR requirements:\n\n"
        for finding in categorized['compliant']:
            item = finding['item']
            output += f"- **{item.get('area', 'Area')}:** {item.get('description', 'Compliant')}\n"
    else:
        output += "*No specifically compliant areas were documented in this audit.*\n"

    output += "\n---\n\n"
    return output

def generate_recommendations(categorized: Dict[str, List]) -> str:
    """Generate prioritized recommendations section."""
    output = "## Recommendations & Next Steps\n\n"

    output += "### Immediate Actions (0-7 days)\n\n"
    immediate = [f for f in categorized['critical']]
    if immediate:
        for idx, finding in enumerate(immediate, 1):
            item = finding['item']
            output += f"{idx}. {item.get('recommendation', item.get('description', 'Address critical issue'))}\n"
    else:
        output += "*No immediate actions required.*\n"

    output += "\n### Short-term Actions (30 days)\n\n"
    short_term = [f for f in categorized['high']]
    if short_term:
        for idx, finding in enumerate(short_term, 1):
            item = finding['item']
            output += f"{idx}. {item.get('recommendation', item.get('description', 'Address high-priority issue'))}\n"
    else:
        output += "*No short-term actions required.*\n"

    output += "\n### Medium-term Actions (90 days)\n\n"
    medium_term = [f for f in categorized['medium'][:5]]  # Top 5
    if medium_term:
        for idx, finding in enumerate(medium_term, 1):
            item = finding['item']
            output += f"{idx}. {item.get('recommendation', item.get('description', 'Address medium-priority issue'))}\n"
        if len(categorized['medium']) > 5:
            output += f"\n*Plus {len(categorized['medium']) - 5} additional medium-priority items...*\n"
    else:
        output += "*No medium-term actions required.*\n"

    output += "\n### Ongoing Improvements\n\n"
    output += """
- Implement regular GDPR compliance reviews (quarterly)
- Conduct staff training on data protection
- Review and update privacy policies
- Monitor data subject rights requests
- Maintain Records of Processing Activities (Article 30)
- Review third-party processor agreements
- Test incident response procedures
- Stay updated on GDPR guidance and case law
"""

    output += "\n---\n\n"
    return output

def generate_appendix(findings: Dict[str, Any]) -> str:
    """Generate appendix with technical details."""
    output = "## Appendix\n\n"

    output += "### A. Audit Methodology\n\n"
    output += """
This audit was conducted using automated scanning tools and manual review:

1. **Code Scanning** - Analyzed source code for data collection patterns
2. **Database Analysis** - Reviewed database schemas for personal data
3. **DSR Implementation** - Verified data subject rights mechanisms
4. **Security Assessment** - Evaluated technical and organizational measures
5. **Documentation Review** - Examined privacy policies and procedures

"""

    output += "### B. GDPR Compliance Checklist\n\n"
    output += """
| Requirement | Status | Notes |
|-------------|--------|-------|
| Article 5 - Principles | ⚠️ | See findings |
| Article 6 - Legal Basis | ⚠️ | Verify documentation |
| Article 7 - Consent | ⚠️ | Review mechanisms |
| Article 13-14 - Transparency | ⚠️ | Update privacy notices |
| Article 15-22 - Data Subject Rights | ⚠️ | Implement all rights |
| Article 25 - Data Protection by Design | ⚠️ | Review architecture |
| Article 30 - Records of Processing | ⚠️ | Maintain records |
| Article 32 - Security | ⚠️ | See security findings |
| Article 33-34 - Breach Notification | ⚠️ | Establish procedures |
| Article 35 - DPIA | ⚠️ | Conduct where needed |
| Article 44-49 - International Transfers | ⚠️ | Verify safeguards |

"""

    output += "### C. Resources\n\n"
    output += """
**Official GDPR Resources:**
- Official GDPR Text: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- EDPB Guidelines: https://edpb.europa.eu/our-work-tools/general-guidance/gdpr-guidelines-recommendations-best-practices_en
- GDPR-Info.eu: https://gdpr-info.eu/

**Supervisory Authorities:**
- Find your supervisory authority: https://edpb.europa.eu/about-edpb/board/members_en

**Implementation Tools:**
- CNIL DPIA Tool: https://www.cnil.fr/en/privacy-impact-assessment-pia
- ICO Resources: https://ico.org.uk/for-organisations/guide-to-data-protection/
"""

    return output

def generate_report(findings: Dict[str, Any], output_file: str, metadata: Dict[str, Any]) -> None:
    """Generate complete audit report."""

    # Categorize findings by risk level
    categorized = categorize_findings(findings)

    # Generate report sections
    report = generate_executive_summary(categorized, metadata)
    report += generate_findings_section(categorized)
    report += generate_compliant_areas(categorized)
    report += generate_recommendations(categorized)
    report += generate_appendix(findings)

    # Add footer
    report += f"\n\n---\n\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    report += "*This report was generated using the GDPR Auditor skill for Claude Code*\n"

    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ GDPR Audit Report generated: {output_file}")
    print(f"\nSummary:")
    print(f"  Critical issues: {len(categorized['critical'])}")
    print(f"  High-priority issues: {len(categorized['high'])}")
    print(f"  Medium-priority issues: {len(categorized['medium'])}")
    print(f"  Low-priority issues: {len(categorized['low'])}")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_audit_report.py <findings.json> [output.md]")
        print("\nfindings.json should contain:")
        print('{')
        print('  "metadata": {')
        print('    "audit_date": "2025-10-17",')
        print('    "system_name": "My Application",')
        print('    "auditor": "John Doe",')
        print('    "scope": "Full compliance audit"')
        print('  },')
        print('  "findings": {')
        print('    "category_name": [')
        print('      {')
        print('        "title": "Issue title",')
        print('        "description": "Issue description",')
        print('        "gdpr_article": "Article 32",')
        print('        "risk_level": "high",')
        print('        "recommendation": "Fix this...",')
        print('        "code_reference": "file.py:123"')
        print('      }')
        print('    ]')
        print('  }')
        print('}')
        sys.exit(1)

    findings_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'gdpr_audit_report.md'

    # Load findings
    data = load_findings(findings_file)

    # Extract metadata and findings
    metadata = data.get('metadata', {})
    findings = data.get('findings', data)  # Support both formats

    # Generate report
    generate_report(findings, output_file, metadata)

if __name__ == "__main__":
    main()
