#!/usr/bin/env python3
"""
Incident Response Playbook Generator

Generates comprehensive incident response playbooks in Markdown format from
scenario templates and organizational information.

Usage:
    python3 generate_playbook_markdown.py --scenario ransomware --org "Acme Corp"
    python3 generate_playbook_markdown.py --scenario data_breach --org "Healthcare Inc" --output custom.md

Author: Diego Consolini
License: MIT
Version: 1.0.0
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from jinja2 import Template


class PlaybookGenerator:
    """Generator for incident response playbooks."""

    def __init__(self, scenarios_file: Path, frameworks_file: Path, templates_file: Path):
        """
        Initialize the playbook generator.

        Args:
            scenarios_file: Path to incident_scenarios.json
            frameworks_file: Path to framework_mappings.json
            templates_file: Path to communication_templates.json
        """
        self.scenarios_file = scenarios_file
        self.frameworks_file = frameworks_file
        self.templates_file = templates_file

        self.scenarios_data = None
        self.frameworks_data = None
        self.templates_data = None

        self._load_data()

    def _load_data(self) -> None:
        """Load all reference data from JSON files."""
        try:
            with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                self.scenarios_data = json.load(f)

            with open(self.frameworks_file, 'r', encoding='utf-8') as f:
                self.frameworks_data = json.load(f)

            with open(self.templates_file, 'r', encoding='utf-8') as f:
                self.templates_data = json.load(f)

        except FileNotFoundError as e:
            print(f"❌ Error: Required file not found: {e.filename}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in file: {e}")
            sys.exit(1)

    def get_scenario(self, scenario_id: str) -> Optional[Dict]:
        """
        Get scenario data by ID.

        Args:
            scenario_id: ID of the scenario (e.g., 'ransomware')

        Returns:
            Scenario dictionary or None if not found
        """
        scenarios = self.scenarios_data.get('scenarios', [])
        return next((s for s in scenarios if s.get('id') == scenario_id), None)

    def list_scenarios(self) -> None:
        """List all available scenarios."""
        scenarios = self.scenarios_data.get('scenarios', [])

        print("\n📋 Available Incident Scenarios:")
        print("=" * 80)
        for scenario in scenarios:
            print(f"\nID: {scenario.get('id')}")
            print(f"Name: {scenario.get('name')}")
            print(f"Category: {scenario.get('category')} | Severity: {scenario.get('severity', '').upper()}")
            print(f"Description: {scenario.get('description')}")
            print("-" * 80)

    def generate_playbook(
        self,
        scenario_id: str,
        organization_name: str,
        industry: str = "General",
        contact_email: str = "security@organization.com",
        contact_phone: str = "(555) 123-4567"
    ) -> str:
        """
        Generate a complete incident response playbook in Markdown.

        Args:
            scenario_id: ID of the incident scenario
            organization_name: Name of the organization
            industry: Industry sector
            contact_email: Security team contact email
            contact_phone: Security team contact phone

        Returns:
            Generated playbook as Markdown string
        """
        scenario = self.get_scenario(scenario_id)

        if not scenario:
            print(f"❌ Error: Scenario '{scenario_id}' not found")
            return ""

        # Prepare template variables
        context = {
            'scenario': scenario,
            'organization': {
                'name': organization_name,
                'industry': industry,
                'contact_email': contact_email,
                'contact_phone': contact_phone
            },
            'generated_date': datetime.now().strftime("%Y-%m-%d"),
            'generated_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'frameworks': self.frameworks_data,
            'templates': self.templates_data
        }

        # Generate playbook using Jinja2 template
        template_str = self._get_playbook_template()
        template = Template(template_str)

        return template.render(**context)

    def _get_playbook_template(self) -> str:
        """
        Get the Jinja2 template for playbook generation.

        Returns:
            Jinja2 template string
        """
        return """# {{ scenario.name }} - Incident Response Playbook

**Organization**: {{ organization.name }}
**Industry**: {{ organization.industry }}
**Generated**: {{ generated_date }}
**Version**: 1.0
**Classification**: CONFIDENTIAL

---

## Table of Contents

1. [Overview](#overview)
2. [Incident Classification](#incident-classification)
3. [Detection & Indicators](#detection--indicators)
4. [Response Procedures](#response-procedures)
5. [Recovery Actions](#recovery-actions)
6. [Communication Requirements](#communication-requirements)
7. [Compliance Considerations](#compliance-considerations)
8. [Roles & Responsibilities](#roles--responsibilities)
9. [Contact Information](#contact-information)

---

## Overview

### Incident Type
**{{ scenario.name }}**

### Description
{{ scenario.description }}

### NIST Reference
{% if scenario.nist_example %}
{{ scenario.nist_example }}
{% endif %}

### Severity Level
**{{ scenario.severity | upper }}**

---

## Incident Classification

**Category**: {{ scenario.category }}
**Severity**: {{ scenario.severity | upper }}

### NIST CSF 2.0 Alignment
This playbook aligns with the following NIST Cybersecurity Framework 2.0 Functions:
- **DETECT** (DE) - Finding and analyzing possible cybersecurity attacks
- **RESPOND** (RS) - Taking action regarding a detected incident
- **RECOVER** (RC) - Restoring impaired assets and operations

---

## Detection & Indicators

### Technical Indicators of Compromise

{% for indicator in scenario.indicators.technical %}
{{ loop.index }}. {{ indicator }}
{% endfor %}

### Behavioral Indicators

{% for indicator in scenario.indicators.behavioral %}
{{ loop.index }}. {{ indicator }}
{% endfor %}

### Detection Activities

#### Continuous Monitoring (NIST CSF DE.CM)
{% for activity in scenario.detection_activities.continuous_monitoring %}
- {{ activity }}
{% endfor %}

#### Adverse Event Analysis (NIST CSF DE.AE)
{% for activity in scenario.detection_activities.analysis %}
- {{ activity }}
{% endfor %}

---

## Response Procedures

### Phase 1: Triage & Assessment

**Objective**: Validate the incident and determine initial scope.

**Actions**:
{% for action in scenario.response_actions.triage %}
- {{ action }}
{% endfor %}

**Timeframe**: 0-15 minutes from detection

---

### Phase 2: Containment

**Objective**: Prevent incident spread and limit damage.

**Actions**:
{% for action in scenario.response_actions.containment %}
- {{ action }}
{% endfor %}

**Timeframe**: 15 minutes - 2 hours from detection

---

### Phase 3: Eradication

**Objective**: Remove the threat and eliminate vulnerabilities.

**Actions**:
{% for action in scenario.response_actions.eradication %}
- {{ action }}
{% endfor %}

**Timeframe**: 2-24 hours from detection

---

## Recovery Actions

**Objective**: Restore normal operations while maintaining security.

### Recovery Procedures

{% for action in scenario.recovery_actions %}
{{ loop.index }}. {{ action }}
{% endfor %}

### Validation Steps

Before declaring incident resolved:
- [ ] Verify all malicious activity has ceased
- [ ] Confirm all affected systems are clean and operational
- [ ] Validate backup integrity (if used for recovery)
- [ ] Review logs for any remaining suspicious activity
- [ ] Implement enhanced monitoring for {{ scenario.name | lower }} indicators

---

## Communication Requirements

### Internal Communications

**Required Notifications**:
{% for stakeholder in scenario.communication_requirements.internal %}
- {{ stakeholder }}
{% endfor %}

**Communication Frequency**: Every 4 hours during active incident, daily during recovery

**Primary Contact**: {{ organization.contact_email }}
**Emergency Hotline**: {{ organization.contact_phone }}

---

### External Communications

{% if scenario.communication_requirements.external %}
**Required Notifications**:
{% for stakeholder in scenario.communication_requirements.external %}
- {{ stakeholder }}
{% endfor %}
{% endif %}

---

### Public Communications

{% if scenario.communication_requirements.public %}
**May Be Required**:
{% for requirement in scenario.communication_requirements.public %}
- {{ requirement }}
{% endfor %}

**Approval Required**: Legal & Executive Leadership
**Coordinated By**: Communications/PR Team
{% endif %}

---

## Compliance Considerations

### GDPR Requirements

{% if scenario.gdpr_considerations %}
**Notification Required**: {{ scenario.gdpr_considerations.notification_required }}

{% if scenario.gdpr_considerations.article_33_timeline %}
**Article 33 - Supervisory Authority Notification**:
Timeline: {{ scenario.gdpr_considerations.article_33_timeline }}

**Article 34 - Data Subject Notification**:
Required: {{ scenario.gdpr_considerations.article_34_required }}
{% endif %}

**Risk Factors**:
{% for factor in scenario.gdpr_considerations.risk_factors %}
- {{ factor }}
{% endfor %}
{% endif %}

---

### HIPAA Requirements

{% if scenario.hipaa_considerations %}
**Breach Determination**: {{ scenario.hipaa_considerations.breach_determination }}

**Notification Timeline**: {{ scenario.hipaa_considerations.notification_timeline }}

**Risk Assessment Factors**:
{% for factor in scenario.hipaa_considerations.risk_assessment_factors %}
- {{ factor }}
{% endfor %}
{% endif %}

---

## Roles & Responsibilities

### Incident Response Team Structure

{% for role in scenario.roles_responsibilities %}
- **{{ role.split(':')[0] }}**: {{ role.split(':')[1] if ':' in role else role }}
{% endfor %}

### Escalation Criteria

**Escalate to Executive Leadership if**:
- Incident severity is CRITICAL
- Data breach affects >500 individuals
- Regulatory notification required
- Media inquiries received
- Estimated recovery time >24 hours

---

## Contact Information

### {{ organization.name }} Security Team

**Primary Contact**: {{ organization.contact_email }}
**Emergency Hotline**: {{ organization.contact_phone }}
**Available**: 24/7 for critical incidents

### External Resources

**Law Enforcement**:
- FBI Cyber Division: https://www.fbi.gov/investigate/cyber
- IC3 (Internet Crime Complaint Center): https://www.ic3.gov

**Incident Reporting**:
- US-CERT: https://www.cisa.gov/report
- CERT/CC: cert@cert.org

**Data Protection Authorities** (if applicable):
- GDPR: [Your supervisory authority]
- State AG: [If US-based]

---

## Post-Incident Activities

### Lessons Learned Meeting

**Schedule**: Within 5 business days of incident resolution
**Attendees**: Incident response team, affected department leads, management
**Duration**: 90-120 minutes

**Agenda**:
1. Timeline review (detection to resolution)
2. What went well
3. What needs improvement
4. Root cause analysis
5. Action items with owners and deadlines

### Documentation Requirements

- [ ] Complete incident timeline
- [ ] Technical findings and forensic evidence
- [ ] Communication logs (internal and external)
- [ ] Regulatory notifications (if applicable)
- [ ] Post-incident report with lessons learned
- [ ] Updated playbook based on experience

---

## Appendix

### Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {{ generated_date }} | Auto-generated | Initial playbook creation |

### References

- NIST SP 800-61r3 - Computer Security Incident Handling Guide (April 2025)
- NIST Cybersecurity Framework 2.0
- GDPR Articles 33-34 (if applicable)
- HIPAA Breach Notification Rule (if applicable)

---

**END OF PLAYBOOK**

*This playbook is a living document and should be reviewed and updated regularly based on lessons learned, organizational changes, and evolving threats.*

*Generated by Incident Response Playbook Creator v1.0.0*
*{{ generated_datetime }}*
"""

    def save_playbook(self, playbook_content: str, output_file: Path) -> None:
        """
        Save generated playbook to a file.

        Args:
            playbook_content: Playbook markdown content
            output_file: Path to output file
        """
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(playbook_content)

            print(f"\n✅ Playbook generated successfully!")
            print(f"📄 Output: {output_file}")
            print(f"📏 Size: {len(playbook_content)} characters")

        except Exception as e:
            print(f"❌ Error saving playbook: {e}")
            sys.exit(1)


def main():
    """Main entry point for the playbook generator."""
    parser = argparse.ArgumentParser(
        description="Generate incident response playbooks from authoritative templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate ransomware playbook:
    python3 generate_playbook_markdown.py --scenario ransomware --org "Acme Corp"

  Generate data breach playbook with custom output:
    python3 generate_playbook_markdown.py --scenario data_breach --org "Healthcare Inc" \\
      --industry Healthcare --output output/healthcare-breach-playbook.md

  List available scenarios:
    python3 generate_playbook_markdown.py --list
        """
    )

    parser.add_argument('--scenario', '-s', type=str,
                        help='Incident scenario ID (e.g., ransomware, data_breach, phishing)')
    parser.add_argument('--org', '-o', type=str,
                        help='Organization name')
    parser.add_argument('--industry', '-i', type=str, default='General',
                        help='Industry sector (default: General)')
    parser.add_argument('--contact-email', type=str, default='security@organization.com',
                        help='Security team contact email')
    parser.add_argument('--contact-phone', type=str, default='(555) 123-4567',
                        help='Security team contact phone')
    parser.add_argument('--output', type=str,
                        help='Output file path (default: output/[scenario]-playbook.md)')
    parser.add_argument('--list', '-l', action='store_true',
                        help='List all available scenarios')
    parser.add_argument('--scenarios-file', type=str,
                        help='Path to scenarios JSON file (default: ../references/incident_scenarios_simplified.json)')
    parser.add_argument('--frameworks-file', type=str,
                        help='Path to frameworks JSON file (default: ../references/framework_mappings.json)')
    parser.add_argument('--templates-file', type=str,
                        help='Path to templates JSON file (default: ../references/communication_templates.json)')

    args = parser.parse_args()

    # Determine file paths
    script_dir = Path(__file__).parent

    scenarios_file = Path(args.scenarios_file) if args.scenarios_file else \
                     script_dir.parent / 'references' / 'incident_scenarios_simplified.json'

    frameworks_file = Path(args.frameworks_file) if args.frameworks_file else \
                      script_dir.parent / 'references' / 'framework_mappings.json'

    templates_file = Path(args.templates_file) if args.templates_file else \
                     script_dir.parent / 'references' / 'communication_templates.json'

    # Create generator
    generator = PlaybookGenerator(scenarios_file, frameworks_file, templates_file)

    # List scenarios if requested
    if args.list:
        generator.list_scenarios()
        return

    # Validate required arguments
    if not args.scenario:
        parser.error("--scenario is required (use --list to see available scenarios)")

    if not args.org:
        parser.error("--org (organization name) is required")

    # Generate playbook
    playbook_content = generator.generate_playbook(
        scenario_id=args.scenario,
        organization_name=args.org,
        industry=args.industry,
        contact_email=args.contact_email,
        contact_phone=args.contact_phone
    )

    if not playbook_content:
        sys.exit(1)

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_dir = script_dir.parent / 'output'
        output_file = output_dir / f"{args.scenario}-playbook.md"

    # Save playbook
    generator.save_playbook(playbook_content, output_file)


if __name__ == '__main__':
    main()
