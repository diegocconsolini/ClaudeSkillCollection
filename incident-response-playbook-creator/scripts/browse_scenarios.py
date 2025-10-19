#!/usr/bin/env python3
"""
Incident Response Scenario Browser

This script allows browsing of available incident response scenarios from the
incident_scenarios.json reference file. It provides filtering, search, and
detailed view capabilities.

Usage:
    python3 browse_scenarios.py [--list] [--category CATEGORY] [--severity SEVERITY]
                                 [--detail SCENARIO_ID] [--search TERM]

Examples:
    python3 browse_scenarios.py --list
    python3 browse_scenarios.py --category malware --severity critical
    python3 browse_scenarios.py --detail ransomware
    python3 browse_scenarios.py --search "data breach"

Author: Diego Consolini
License: MIT
Version: 1.0.0
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import textwrap


class ScenarioBrowser:
    """Browser for incident response scenarios."""

    def __init__(self, scenarios_file: Path):
        """
        Initialize the scenario browser.

        Args:
            scenarios_file: Path to incident_scenarios.json
        """
        self.scenarios_file = scenarios_file
        self.scenarios_data = None
        self._load_scenarios()

    def _load_scenarios(self) -> None:
        """Load scenarios from JSON file."""
        try:
            with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                self.scenarios_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Scenarios file not found: {self.scenarios_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in scenarios file: {e}")
            sys.exit(1)

    def list_scenarios(self, category: Optional[str] = None,
                       severity: Optional[str] = None) -> None:
        """
        List all scenarios or filter by category/severity.

        Args:
            category: Filter by category (e.g., 'malware', 'data-breach')
            severity: Filter by severity (e.g., 'critical', 'high')
        """
        scenarios = self.scenarios_data.get('scenarios', [])

        # Apply filters
        if category:
            scenarios = [s for s in scenarios if s.get('category', '').lower() == category.lower()]
        if severity:
            scenarios = [s for s in scenarios if s.get('severity', '').lower() == severity.lower()]

        if not scenarios:
            print("No scenarios found matching the specified criteria.")
            return

        # Print header
        print("\n" + "=" * 80)
        print(f"INCIDENT RESPONSE SCENARIOS")
        if category or severity:
            filters = []
            if category:
                filters.append(f"Category: {category}")
            if severity:
                filters.append(f"Severity: {severity}")
            print(f"Filtered by: {', '.join(filters)}")
        print("=" * 80 + "\n")

        # Print scenarios
        for scenario in scenarios:
            self._print_scenario_summary(scenario)
            print("-" * 80)

        print(f"\nTotal scenarios: {len(scenarios)}")
        print("\nUse --detail <scenario_id> to view full details of a specific scenario.")

    def _print_scenario_summary(self, scenario: Dict) -> None:
        """
        Print a summary of a scenario.

        Args:
            scenario: Scenario dictionary
        """
        # Header with ID and name
        scenario_id = scenario.get('id', 'unknown')
        name = scenario.get('name', 'Unknown Scenario')
        category = scenario.get('category', 'unknown')
        severity = scenario.get('severity', 'unknown')

        # Severity color coding (for terminal)
        severity_display = severity.upper()
        if severity.lower() == 'critical':
            severity_display = f"🔴 {severity_display}"
        elif severity.lower() == 'high':
            severity_display = f"🟠 {severity_display}"
        elif severity.lower() == 'medium':
            severity_display = f"🟡 {severity_display}"
        else:
            severity_display = f"🟢 {severity_display}"

        print(f"ID: {scenario_id}")
        print(f"Name: {name}")
        print(f"Category: {category} | Severity: {severity_display}")

        # Description
        description = scenario.get('description', 'No description available')
        wrapped_desc = textwrap.fill(description, width=76,
                                     initial_indent="Description: ",
                                     subsequent_indent="             ")
        print(wrapped_desc)

        # Key indicators count
        indicators = scenario.get('indicators', {})
        technical_count = len(indicators.get('technical', []))
        behavioral_count = len(indicators.get('behavioral', []))
        print(f"Indicators: {technical_count} technical, {behavioral_count} behavioral")

        # Response actions count
        response_actions = scenario.get('response_actions', {})
        total_actions = sum(len(v) for v in response_actions.values() if isinstance(v, list))
        print(f"Response Actions: {total_actions} total")

        # Compliance flags
        compliance_flags = []
        if scenario.get('gdpr_considerations'):
            compliance_flags.append("GDPR")
        if scenario.get('hipaa_considerations'):
            compliance_flags.append("HIPAA")
        if compliance_flags:
            print(f"Compliance: {', '.join(compliance_flags)}")

    def show_scenario_detail(self, scenario_id: str) -> None:
        """
        Show detailed information about a specific scenario.

        Args:
            scenario_id: ID of the scenario to display
        """
        scenarios = self.scenarios_data.get('scenarios', [])
        scenario = next((s for s in scenarios if s.get('id') == scenario_id), None)

        if not scenario:
            print(f"❌ Error: Scenario '{scenario_id}' not found.")
            print(f"\nAvailable scenario IDs:")
            for s in scenarios:
                print(f"  - {s.get('id')}")
            return

        # Print detailed view
        print("\n" + "=" * 80)
        print(f"SCENARIO DETAILS: {scenario.get('name', 'Unknown')}")
        print("=" * 80 + "\n")

        # Basic info
        print(f"ID: {scenario.get('id')}")
        print(f"Name: {scenario.get('name')}")
        print(f"Category: {scenario.get('category')}")
        print(f"Severity: {scenario.get('severity', '').upper()}")
        print(f"\nDescription:")
        print(textwrap.fill(scenario.get('description', ''), width=76, initial_indent="  ", subsequent_indent="  "))

        # NIST example if present
        if 'nist_example' in scenario:
            print(f"\nNIST SP 800-61r3 Example:")
            print(textwrap.fill(scenario['nist_example'], width=76, initial_indent="  ", subsequent_indent="  "))

        # Indicators
        print(f"\n{'-' * 80}")
        print("INDICATORS OF COMPROMISE")
        print(f"{'-' * 80}")

        indicators = scenario.get('indicators', {})

        technical = indicators.get('technical', [])
        if technical:
            print(f"\nTechnical Indicators ({len(technical)}):")
            for idx, indicator in enumerate(technical, 1):
                print(f"  {idx}. {indicator}")

        behavioral = indicators.get('behavioral', [])
        if behavioral:
            print(f"\nBehavioral Indicators ({len(behavioral)}):")
            for idx, indicator in enumerate(behavioral, 1):
                print(f"  {idx}. {indicator}")

        # Detection activities
        print(f"\n{'-' * 80}")
        print("DETECTION ACTIVITIES")
        print(f"{'-' * 80}")

        detection = scenario.get('detection_activities', {})

        if 'continuous_monitoring' in detection:
            print(f"\nContinuous Monitoring (NIST CSF DE.CM):")
            for activity in detection['continuous_monitoring']:
                print(f"  • {activity}")

        if 'analysis' in detection:
            print(f"\nAdverse Event Analysis (NIST CSF DE.AE):")
            for activity in detection['analysis']:
                print(f"  • {activity}")

        # Response actions
        print(f"\n{'-' * 80}")
        print("RESPONSE ACTIONS")
        print(f"{'-' * 80}")

        response_actions = scenario.get('response_actions', {})

        for phase, actions in response_actions.items():
            if isinstance(actions, list) and actions:
                print(f"\n{phase.replace('_', ' ').title()}:")
                for idx, action in enumerate(actions, 1):
                    wrapped = textwrap.fill(action, width=72, initial_indent=f"  {idx}. ",
                                           subsequent_indent="     ")
                    print(wrapped)

        # Recovery actions
        recovery = scenario.get('recovery_actions', [])
        if recovery:
            print(f"\n{'-' * 80}")
            print("RECOVERY ACTIONS")
            print(f"{'-' * 80}\n")
            for idx, action in enumerate(recovery, 1):
                wrapped = textwrap.fill(action, width=72, initial_indent=f"  {idx}. ",
                                       subsequent_indent="     ")
                print(wrapped)

        # Communication requirements
        print(f"\n{'-' * 80}")
        print("COMMUNICATION REQUIREMENTS")
        print(f"{'-' * 80}")

        comm_req = scenario.get('communication_requirements', {})

        for comm_type in ['internal', 'external', 'public']:
            if comm_type in comm_req and comm_req[comm_type]:
                print(f"\n{comm_type.title()} Communications:")
                for item in comm_req[comm_type]:
                    print(f"  • {item}")

        # Roles and responsibilities
        roles = scenario.get('roles_responsibilities', [])
        if roles:
            print(f"\n{'-' * 80}")
            print("ROLES & RESPONSIBILITIES")
            print(f"{'-' * 80}\n")
            for role in roles:
                print(f"  • {role}")

        # GDPR considerations
        gdpr = scenario.get('gdpr_considerations', {})
        if gdpr:
            print(f"\n{'-' * 80}")
            print("GDPR COMPLIANCE CONSIDERATIONS")
            print(f"{'-' * 80}")

            if 'notification_required' in gdpr:
                print(f"\nNotification Required: {gdpr['notification_required']}")

            if 'article_33_timeline' in gdpr:
                print(f"Article 33 Timeline: {gdpr['article_33_timeline']}")

            if 'article_34_required' in gdpr:
                print(f"Article 34 Required: {gdpr['article_34_required']}")

            if 'risk_factors' in gdpr and gdpr['risk_factors']:
                print(f"\nRisk Factors:")
                for factor in gdpr['risk_factors']:
                    print(f"  • {factor}")

            if 'considerations' in gdpr and gdpr['considerations']:
                print(f"\nKey Considerations:")
                for consideration in gdpr['considerations']:
                    wrapped = textwrap.fill(consideration, width=72, initial_indent="  • ",
                                           subsequent_indent="    ")
                    print(wrapped)

        # HIPAA considerations
        hipaa = scenario.get('hipaa_considerations', {})
        if hipaa:
            print(f"\n{'-' * 80}")
            print("HIPAA COMPLIANCE CONSIDERATIONS")
            print(f"{'-' * 80}")

            if 'breach_determination' in hipaa:
                print(f"\nBreach Determination: {hipaa['breach_determination']}")

            if 'notification_timeline' in hipaa:
                print(f"Notification Timeline: {hipaa['notification_timeline']}")

            if 'risk_assessment_factors' in hipaa and hipaa['risk_assessment_factors']:
                print(f"\nRisk Assessment Factors:")
                for factor in hipaa['risk_assessment_factors']:
                    print(f"  • {factor}")

            if 'considerations' in hipaa and hipaa['considerations']:
                print(f"\nKey Considerations:")
                for consideration in hipaa['considerations']:
                    wrapped = textwrap.fill(consideration, width=72, initial_indent="  • ",
                                           subsequent_indent="    ")
                    print(wrapped)

        print("\n" + "=" * 80 + "\n")

    def search_scenarios(self, search_term: str) -> None:
        """
        Search scenarios by keyword in name, description, or content.

        Args:
            search_term: Search term to look for
        """
        scenarios = self.scenarios_data.get('scenarios', [])
        matches = []

        search_lower = search_term.lower()

        for scenario in scenarios:
            # Convert scenario to string and search
            scenario_str = json.dumps(scenario).lower()
            if search_lower in scenario_str:
                matches.append(scenario)

        if not matches:
            print(f"No scenarios found matching '{search_term}'")
            return

        print("\n" + "=" * 80)
        print(f"SEARCH RESULTS FOR: '{search_term}'")
        print("=" * 80 + "\n")

        for scenario in matches:
            self._print_scenario_summary(scenario)
            print("-" * 80)

        print(f"\nTotal matches: {len(matches)}")

    def show_metadata(self) -> None:
        """Display metadata about the scenarios dataset."""
        metadata = self.scenarios_data.get('metadata', {})

        print("\n" + "=" * 80)
        print("SCENARIOS DATASET METADATA")
        print("=" * 80 + "\n")

        print(f"Title: {metadata.get('title', 'Unknown')}")
        print(f"Version: {metadata.get('version', 'Unknown')}")
        print(f"Last Updated: {metadata.get('last_updated', 'Unknown')}")

        sources = metadata.get('sources', [])
        if sources:
            print(f"\nAuthoritative Sources:")
            for idx, source in enumerate(sources, 1):
                print(f"  {idx}. {source.get('name', 'Unknown')}")
                if 'version' in source:
                    print(f"     Version: {source['version']}")
                if 'publication_date' in source:
                    print(f"     Published: {source['publication_date']}")

        scenarios = self.scenarios_data.get('scenarios', [])
        print(f"\nTotal Scenarios: {len(scenarios)}")

        # Count by category
        categories = {}
        severities = {}
        for scenario in scenarios:
            cat = scenario.get('category', 'unknown')
            sev = scenario.get('severity', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            severities[sev] = severities.get(sev, 0) + 1

        print(f"\nBy Category:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        print(f"\nBy Severity:")
        for sev, count in sorted(severities.items(),
                                  key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}.get(x[0], 99)):
            print(f"  {sev}: {count}")

        print("\n" + "=" * 80 + "\n")


def main():
    """Main entry point for the scenario browser."""
    parser = argparse.ArgumentParser(
        description="Browse incident response scenarios from NIST SP 800-61r3 and other authoritative sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              List all scenarios:
                python3 browse_scenarios.py --list

              Filter by category:
                python3 browse_scenarios.py --list --category malware

              Filter by severity:
                python3 browse_scenarios.py --list --severity critical

              View detailed information:
                python3 browse_scenarios.py --detail ransomware

              Search scenarios:
                python3 browse_scenarios.py --search "data breach"

              Show metadata:
                python3 browse_scenarios.py --metadata
        """)
    )

    parser.add_argument('--list', '-l', action='store_true',
                        help='List all scenarios (or filtered scenarios)')
    parser.add_argument('--category', '-c', type=str,
                        help='Filter scenarios by category (e.g., malware, data-breach)')
    parser.add_argument('--severity', '-s', type=str,
                        help='Filter scenarios by severity (e.g., critical, high, medium)')
    parser.add_argument('--detail', '-d', type=str, metavar='SCENARIO_ID',
                        help='Show detailed information for a specific scenario ID')
    parser.add_argument('--search', type=str, metavar='TERM',
                        help='Search scenarios by keyword')
    parser.add_argument('--metadata', '-m', action='store_true',
                        help='Show metadata about scenarios dataset')
    parser.add_argument('--scenarios-file', type=str,
                        help='Path to incident_scenarios.json (default: ../references/incident_scenarios.json)')

    args = parser.parse_args()

    # Determine scenarios file path
    if args.scenarios_file:
        scenarios_file = Path(args.scenarios_file)
    else:
        # Default: assume script is in scripts/ directory
        # Use simplified version by default (full version has JSON syntax errors to be fixed)
        script_dir = Path(__file__).parent
        scenarios_file = script_dir.parent / 'references' / 'incident_scenarios_simplified.json'

    # Create browser
    browser = ScenarioBrowser(scenarios_file)

    # Execute requested action
    if args.metadata:
        browser.show_metadata()
    elif args.detail:
        browser.show_scenario_detail(args.detail)
    elif args.search:
        browser.search_scenarios(args.search)
    elif args.list or args.category or args.severity:
        browser.list_scenarios(category=args.category, severity=args.severity)
    else:
        # No arguments - show help and list all scenarios
        parser.print_help()
        print("\n")
        browser.list_scenarios()


if __name__ == '__main__':
    main()
