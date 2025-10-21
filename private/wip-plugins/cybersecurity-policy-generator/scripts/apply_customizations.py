#!/usr/bin/env python3
"""
Policy Customization Application Script - Static File Processing Tool

Applies organization-specific customizations to policy templates by replacing
placeholders with actual values.

IMPORTANT - STATIC ANALYSIS ONLY:
This script processes static policy template files. It does NOT:
- Connect to live systems or networks
- Execute code or make network requests
- Access databases or servers
- Require credentials or system access
- Modify original template files

Analyzes: Policy template JSON files and customization data
Purpose: Replace placeholders with organization-specific values
"""

import json
import sys
import os
import re
from typing import Dict, Any, List
from datetime import datetime


def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        print(f"Expected location: {os.path.abspath(filepath)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}")
        sys.exit(1)


def find_policy_by_id(policies: List[Dict[str, Any]], policy_id: str) -> Dict[str, Any]:
    """Find policy by ID."""
    for policy in policies:
        if policy.get('id') == policy_id:
            return policy

    print(f"Error: Policy with ID '{policy_id}' not found")
    print(f"\nAvailable policy IDs:")
    for p in policies[:10]:  # Show first 10
        print(f"  - {p.get('id', 'Unknown')}")
    print(f"  ... and {len(policies) - 10} more")
    sys.exit(1)


def replace_placeholders(text: str, customizations: Dict[str, Any]) -> str:
    """
    Replace placeholders in text with customization values.

    Placeholders can be in formats:
    - <PlaceholderName>
    - [PlaceholderName]
    - {PlaceholderName}
    """
    if not text:
        return text

    # Define placeholder mappings
    placeholder_map = {
        # Company information
        '<Company Name>': customizations.get('company_name', '<Company Name>'),
        '<YourCompanyName>': customizations.get('company_name', '<YourCompanyName>'),
        '[Company Name]': customizations.get('company_name', '[Company Name]'),

        # Responsible parties
        '<ResponsibleCorporateOfficer>': customizations.get('responsible_officer', '<ResponsibleCorporateOfficer>'),
        '<Department>': customizations.get('responsible_department', '<Department>'),
        '[Department]': customizations.get('responsible_department', '[Department]'),

        # Contact information
        '<Contact>': customizations.get('contact_email', '<Contact>'),
        '<ContactEmail>': customizations.get('contact_email', '<ContactEmail>'),

        # Dates and versions
        '<Effective Date>': customizations.get('effective_date', '<Effective Date>'),
        '<EffectiveDate>': customizations.get('effective_date', '<EffectiveDate>'),
        '[Effective Date]': customizations.get('effective_date', '[Effective Date]'),

        '<Review Date>': customizations.get('review_schedule', '<Review Date>'),
        '<ReviewSchedule>': customizations.get('review_schedule', '<ReviewSchedule>'),

        '<Version>': customizations.get('version', '1.0'),

        # Industry and size
        '<Industry>': customizations.get('industry', '<Industry>'),
        '<OrganizationSize>': customizations.get('organization_size', '<OrganizationSize>'),
    }

    # Apply replacements
    result = text
    for placeholder, value in placeholder_map.items():
        result = result.replace(placeholder, value)

    return result


def customize_section(section: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Customize a policy section."""
    customized = section.copy()

    # Replace placeholders in title
    if 'title' in customized:
        customized['title'] = replace_placeholders(customized['title'], customizations)

    # Replace placeholders in content
    if 'content' in customized:
        customized['content'] = replace_placeholders(customized['content'], customizations)

    # Replace placeholders in subsections
    if 'subsections' in customized:
        customized['subsections'] = [
            customize_section(subsection, customizations)
            for subsection in customized['subsections']
        ]

    return customized


def add_compliance_section(policy: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Add or enhance compliance section based on selected frameworks."""
    frameworks = customizations.get('frameworks', [])
    regulations = customizations.get('regulations', [])

    if not frameworks and not regulations:
        return policy

    # Build compliance text
    compliance_text = "This policy supports compliance with:\n\n"

    if frameworks:
        compliance_text += "**Frameworks:**\n"
        for framework in frameworks:
            if framework == "ISO 27001":
                # Extract ISO controls from policy metadata
                iso_controls = policy.get('frameworks', {}).get('iso27001', {}).get('controls', [])
                controls_str = ', '.join(iso_controls) if iso_controls else "Multiple controls"
                compliance_text += f"- **ISO 27001:** {controls_str}\n"
            elif framework == "SOC 2":
                compliance_text += f"- **SOC 2:** Trust Service Criteria (Security, Availability)\n"
            elif framework == "NIST CSF":
                compliance_text += f"- **NIST Cybersecurity Framework:** Identify, Protect, Detect, Respond, Recover\n"
            elif framework == "CIS Controls v8":
                # Extract CIS control from policy metadata
                cis_control = policy.get('frameworks', {}).get('cisControls', {}).get('control', 'N/A')
                compliance_text += f"- **CIS Controls v8:** Control {cis_control}\n"
            elif framework == "GDPR":
                compliance_text += f"- **GDPR:** Articles 5, 24, 25, 32 (Data Protection)\n"
            else:
                compliance_text += f"- **{framework}**\n"
        compliance_text += "\n"

    if regulations and regulations != ["None"]:
        compliance_text += "**Regulatory Requirements:**\n"
        for regulation in regulations:
            if regulation != "None":
                compliance_text += f"- {regulation}\n"

    # Add compliance section to policy
    sections = policy.get('sections', [])

    # Check if compliance section exists
    compliance_exists = any(s.get('type') == 'compliance' for s in sections)

    if not compliance_exists:
        sections.append({
            "type": "compliance",
            "title": "Compliance",
            "content": compliance_text
        })
        policy['sections'] = sections
    else:
        # Enhance existing compliance section
        for section in sections:
            if section.get('type') == 'compliance':
                existing_content = section.get('content', '')
                section['content'] = existing_content + "\n\n" + compliance_text

    return policy


def add_metadata(policy: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Add customization metadata to policy."""
    policy['customization'] = {
        'customized_at': datetime.now().isoformat(),
        'organization': customizations.get('company_name', 'Unknown'),
        'version': customizations.get('version', '1.0'),
        'effective_date': customizations.get('effective_date', ''),
        'review_schedule': customizations.get('review_schedule', ''),
        'responsible_officer': customizations.get('responsible_officer', ''),
        'frameworks': customizations.get('frameworks', []),
        'regulations': customizations.get('regulations', [])
    }
    return policy


def validate_customizations(customizations: Dict[str, Any]) -> List[str]:
    """Validate required customization fields."""
    required_fields = [
        'company_name',
        'industry',
        'organization_size',
        'responsible_officer',
        'responsible_department',
        'contact_email',
        'effective_date',
        'review_schedule',
        'version'
    ]

    missing = []
    for field in required_fields:
        if field not in customizations or not customizations[field]:
            missing.append(field)

    return missing


def apply_customizations(policy: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Apply customizations to policy template."""
    # Validate customizations
    missing = validate_customizations(customizations)
    if missing:
        print(f"Warning: Missing customization fields: {', '.join(missing)}")
        print("These placeholders may not be replaced in the output.\n")

    # Deep copy policy
    customized_policy = json.loads(json.dumps(policy))

    # Customize title
    if 'title' in customized_policy:
        customized_policy['title'] = replace_placeholders(customized_policy['title'], customizations)

    # Customize description
    if 'description' in customized_policy:
        customized_policy['description'] = replace_placeholders(customized_policy['description'], customizations)

    # Customize sections
    if 'sections' in customized_policy:
        customized_policy['sections'] = [
            customize_section(section, customizations)
            for section in customized_policy['sections']
        ]

    # Add compliance information
    customized_policy = add_compliance_section(customized_policy, customizations)

    # Add metadata
    customized_policy = add_metadata(customized_policy, customizations)

    return customized_policy


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Apply customizations to policy template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply customizations to a policy
  python apply_customizations.py \\
    --policy-id "acceptable-use-policy-template-04-25-2023" \\
    --customizations customizations.json \\
    --output customized_policy.json

  # Specify custom policies file
  python apply_customizations.py \\
    --policies-file ../references/policies.json \\
    --policy-id "password-policy-template-04-25-2023" \\
    --customizations my_customizations.json \\
    --output output/password_policy.json

  # Validate customizations only
  python apply_customizations.py \\
    --customizations customizations.json \\
    --validate-only
        """
    )

    parser.add_argument(
        '--policies-file',
        default='../references/policies.json',
        help='Path to policies.json file (default: ../references/policies.json)'
    )

    parser.add_argument(
        '--policy-id',
        help='Policy ID to customize (e.g., "acceptable-use-policy-template-04-25-2023")'
    )

    parser.add_argument(
        '--customizations',
        required=True,
        help='Path to customizations.json file with organization data'
    )

    parser.add_argument(
        '--output',
        help='Output file path for customized policy (default: customized_policy.json)',
        default='customized_policy.json'
    )

    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate customizations, do not apply'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )

    args = parser.parse_args()

    # Load customizations
    customizations = load_json(args.customizations)

    # Validate customizations
    missing = validate_customizations(customizations)
    if missing:
        print("⚠️  Customization Validation Warnings:")
        for field in missing:
            print(f"  - Missing field: {field}")
        print()

    if args.validate_only:
        if missing:
            print("Validation failed: Missing required fields")
            sys.exit(1)
        else:
            print("✓ Validation passed: All required fields present")
            sys.exit(0)

    # Require policy ID for customization
    if not args.policy_id:
        print("Error: --policy-id is required (unless using --validate-only)")
        sys.exit(1)

    # Resolve relative path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    policies_path = os.path.join(script_dir, args.policies_file)

    # Load policies
    if args.verbose:
        print(f"Loading policies from: {policies_path}")

    data = load_json(policies_path)
    policies = data.get('policies', [])

    if args.verbose:
        print(f"Loaded {len(policies)} policies")

    # Find target policy
    if args.verbose:
        print(f"Finding policy: {args.policy_id}")

    policy = find_policy_by_id(policies, args.policy_id)

    print(f"\n{'='*80}")
    print(f"Customizing Policy: {policy.get('title', 'Unknown')}")
    print(f"{'='*80}\n")

    # Apply customizations
    if args.verbose:
        print("Applying customizations...")

    customized_policy = apply_customizations(policy, customizations)

    # Save output
    output_path = args.output
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(customized_policy, f, indent=2, ensure_ascii=False)

    print(f"✓ Customized policy saved to: {os.path.abspath(output_path)}")
    print(f"\nCustomization Summary:")
    print(f"  Organization: {customizations.get('company_name', 'N/A')}")
    print(f"  Industry: {customizations.get('industry', 'N/A')}")
    print(f"  Effective Date: {customizations.get('effective_date', 'N/A')}")
    print(f"  Responsible Officer: {customizations.get('responsible_officer', 'N/A')}")

    frameworks = customizations.get('frameworks', [])
    if frameworks:
        print(f"  Compliance Frameworks: {', '.join(frameworks)}")

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
