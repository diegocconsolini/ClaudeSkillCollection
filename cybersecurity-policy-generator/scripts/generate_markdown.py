#!/usr/bin/env python3
"""
Markdown Policy Generator - Static File Processing Tool

Generates professional Markdown policy documents from customized policy JSON.

IMPORTANT - STATIC ANALYSIS ONLY:
This script processes static policy data files. It does NOT:
- Connect to live systems or networks
- Execute code or make network requests
- Access databases or servers
- Require credentials or system access

Analyzes: Customized policy JSON files
Purpose: Generate formatted Markdown policy documents
"""

import json
import sys
import os
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


def format_metadata_header(policy: Dict[str, Any]) -> str:
    """Format policy metadata header."""
    customization = policy.get('customization', {})
    metadata = policy.get('metadata', {})

    header = f"""# {policy.get('title', 'Untitled Policy')}

**Company:** {customization.get('organization', 'N/A')}
**Version:** {customization.get('version', '1.0')}
**Effective Date:** {customization.get('effective_date', 'TBD')}
**Review Schedule:** {customization.get('review_schedule', 'Annually')}
**Responsible Officer:** {customization.get('responsible_officer', 'N/A')}
**Contact:** {customization.get('organization', 'N/A')} Security Team

---

"""
    return header


def format_section(section: Dict[str, Any], level: int = 2) -> str:
    """Format a policy section as Markdown."""
    markdown = ""

    # Section title
    title = section.get('title', '')
    if title:
        markdown += f"{'#' * level} {title}\n\n"

    # Section content
    content = section.get('content', '')
    if content:
        markdown += f"{content}\n\n"

    # Subsections
    subsections = section.get('subsections', [])
    for subsection in subsections:
        markdown += format_section(subsection, level + 1)

    return markdown


def format_compliance_frameworks(policy: Dict[str, Any]) -> str:
    """Format compliance framework information."""
    customization = policy.get('customization', {})
    frameworks = customization.get('frameworks', [])
    regulations = customization.get('regulations', [])

    if not frameworks and not regulations:
        return ""

    markdown = "## Compliance Frameworks\n\n"
    markdown += "This policy supports the following compliance frameworks and regulations:\n\n"

    if frameworks:
        markdown += "**Frameworks:**\n"
        for framework in frameworks:
            markdown += f"- {framework}\n"
        markdown += "\n"

    if regulations and regulations != ["None"]:
        markdown += "**Regulatory Requirements:**\n"
        for regulation in regulations:
            if regulation != "None":
                markdown += f"- {regulation}\n"
        markdown += "\n"

    return markdown


def format_approval_footer(policy: Dict[str, Any]) -> str:
    """Format approval and signature footer."""
    customization = policy.get('customization', {})

    footer = f"""---

## Approval and Review

**Approved by:** {customization.get('responsible_officer', 'N/A')}
**Approval Date:** {customization.get('effective_date', 'TBD')}
**Next Review Date:** {_calculate_next_review(customization)}

## Document Control

**Version:** {customization.get('version', '1.0')}
**Last Updated:** {customization.get('customized_at', datetime.now().isoformat())}
**Document Owner:** {customization.get('organization', 'N/A')} Information Security Department

---

*This policy was generated using the Cybersecurity Policy Generator.*
*Template Source: {policy.get('source', 'Unknown')}*
"""
    return footer


def _calculate_next_review(customization: Dict[str, Any]) -> str:
    """Calculate next review date based on review schedule."""
    effective_date = customization.get('effective_date', '')
    review_schedule = customization.get('review_schedule', 'Annually')

    if not effective_date:
        return "TBD"

    try:
        from dateutil.relativedelta import relativedelta
        eff_date = datetime.fromisoformat(effective_date)

        if review_schedule == "Quarterly":
            next_review = eff_date + relativedelta(months=3)
        elif review_schedule == "Semi-annually":
            next_review = eff_date + relativedelta(months=6)
        elif review_schedule == "Annually":
            next_review = eff_date + relativedelta(years=1)
        elif review_schedule == "Bi-annually":
            next_review = eff_date + relativedelta(years=2)
        else:
            return "As needed"

        return next_review.strftime('%Y-%m-%d')

    except (ImportError, ValueError):
        # Fallback if dateutil not available or date invalid
        return f"{review_schedule} from {effective_date}"


def generate_table_of_contents(sections: List[Dict[str, Any]]) -> str:
    """Generate table of contents from sections."""
    toc = "## Table of Contents\n\n"

    for i, section in enumerate(sections, 1):
        title = section.get('title', 'Untitled')
        # Create anchor link (lowercase, replace spaces with hyphens)
        anchor = title.lower().replace(' ', '-').replace('/', '-')
        toc += f"{i}. [{title}](#{anchor})\n"

        # Add subsections
        subsections = section.get('subsections', [])
        for j, subsection in enumerate(subsections, 1):
            subtitle = subsection.get('title', 'Untitled')
            sub_anchor = subtitle.lower().replace(' ', '-').replace('/', '-')
            toc += f"   {i}.{j}. [{subtitle}](#{sub_anchor})\n"

    toc += "\n---\n\n"
    return toc


def generate_markdown(policy: Dict[str, Any], include_toc: bool = True) -> str:
    """Generate complete Markdown document from policy."""
    markdown = ""

    # Metadata header
    markdown += format_metadata_header(policy)

    # Table of contents
    if include_toc:
        sections = policy.get('sections', [])
        if len(sections) > 3:  # Only add TOC if more than 3 sections
            markdown += generate_table_of_contents(sections)

    # Policy description
    description = policy.get('description', '')
    if description:
        markdown += f"{description}\n\n---\n\n"

    # Sections
    sections = policy.get('sections', [])
    for section in sections:
        markdown += format_section(section)

    # Compliance frameworks (if not already in sections)
    has_compliance = any(s.get('type') == 'compliance' for s in sections)
    if not has_compliance:
        markdown += format_compliance_frameworks(policy)

    # Approval footer
    markdown += format_approval_footer(policy)

    return markdown


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate Markdown policy document from customized policy JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Markdown from customized policy
  python generate_markdown.py \\
    --input customized_policy.json \\
    --output AcceptableUsePolicy.md

  # Generate without table of contents
  python generate_markdown.py \\
    --input customized_policy.json \\
    --output policy.md \\
    --no-toc

  # Preview to stdout
  python generate_markdown.py \\
    --input customized_policy.json \\
    --preview
        """
    )

    parser.add_argument(
        '--input',
        required=True,
        help='Path to customized policy JSON file'
    )

    parser.add_argument(
        '--output',
        help='Output Markdown file path (default: policy.md)',
        default='policy.md'
    )

    parser.add_argument(
        '--no-toc',
        action='store_true',
        help='Do not include table of contents'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview output to stdout instead of writing to file'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )

    args = parser.parse_args()

    # Load customized policy
    if args.verbose:
        print(f"Loading policy from: {args.input}")

    policy = load_json(args.input)

    # Generate Markdown
    if args.verbose:
        print("Generating Markdown...")

    include_toc = not args.no_toc
    markdown = generate_markdown(policy, include_toc=include_toc)

    # Output
    if args.preview:
        print("\n" + "="*80)
        print("MARKDOWN PREVIEW")
        print("="*80 + "\n")
        print(markdown)
        print("="*80 + "\n")
    else:
        # Write to file
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"\n{'='*80}")
        print(f"Markdown Policy Generated")
        print(f"{'='*80}\n")
        print(f"✓ Output file: {os.path.abspath(args.output)}")
        print(f"  Policy: {policy.get('title', 'Unknown')}")
        print(f"  Organization: {policy.get('customization', {}).get('organization', 'N/A')}")
        print(f"  File size: {len(markdown)} bytes")

        # Count sections
        sections = policy.get('sections', [])
        print(f"  Sections: {len(sections)}")

        if include_toc:
            print(f"  Table of Contents: Included")

        print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
