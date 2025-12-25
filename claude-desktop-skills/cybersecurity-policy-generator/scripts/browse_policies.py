#!/usr/bin/env python3
"""
Cybersecurity Policy Browser - Static File Analysis Tool

Browses, filters, and searches through 51 cybersecurity policy templates from
SANS and CIS Controls.

IMPORTANT - STATIC ANALYSIS ONLY:
This script analyzes static policy template files. It does NOT:
- Connect to live systems or networks
- Execute code or make network requests
- Access databases or servers
- Require credentials or system access
- Modify any files

Analyzes: Policy template JSON files
Purpose: Browse and filter cybersecurity policy templates for selection
"""

import json
import sys
import os
from typing import List, Dict, Any, Optional

def load_policies(policies_file: str) -> Dict[str, Any]:
    """Load policies from JSON file."""
    try:
        with open(policies_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Policies file '{policies_file}' not found")
        print(f"Expected location: {os.path.abspath(policies_file)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{policies_file}': {e}")
        sys.exit(1)

def filter_policies(
    policies: List[Dict[str, Any]],
    source: Optional[str] = None,
    category: Optional[str] = None,
    framework: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter policies by criteria.

    Args:
        policies: List of policy dictionaries
        source: Filter by source ("SANS" or "CIS")
        category: Filter by category (e.g., "Governance", "Identity and Access")
        framework: Filter by framework (e.g., "ISO 27001", "SOC 2")
        search: Search in title and category (case-insensitive)

    Returns:
        Filtered list of policies
    """
    filtered = policies

    if source:
        filtered = [p for p in filtered if p.get('source', '').upper() == source.upper()]

    if category:
        filtered = [p for p in filtered if p.get('category', '').lower() == category.lower()]

    if framework:
        filtered = [
            p for p in filtered
            if framework in p.get('frameworks', [])
        ]

    if search:
        search_lower = search.lower()
        filtered = [
            p for p in filtered
            if search_lower in p.get('title', '').lower() or
               search_lower in p.get('category', '').lower()
        ]

    return filtered

def format_policy_summary(policy: Dict[str, Any], index: int) -> str:
    """Format policy as summary string."""
    title = policy.get('title', 'Untitled')
    source = policy.get('source', 'Unknown')
    category = policy.get('category', 'Uncategorized')
    frameworks = policy.get('frameworks', [])
    policy_type = policy.get('type', 'policy')

    # Get word count from metadata
    word_count = policy.get('metadata', {}).get('wordCount', 'N/A')

    # Format frameworks
    frameworks_str = ', '.join(frameworks[:3])  # Show first 3
    if len(frameworks) > 3:
        frameworks_str += f" +{len(frameworks) - 3} more"

    return f"""
[{index}] {title}
    Source: {source} | Category: {category} | Type: {policy_type}
    Frameworks: {frameworks_str}
    Word Count: {word_count}
"""

def display_results(policies: List[Dict[str, Any]], total_available: int):
    """Display search/filter results."""
    print(f"\n{'='*80}")
    print(f"Found {len(policies)} policies (out of {total_available} total)")
    print(f"{'='*80}\n")

    if not policies:
        print("No policies match your criteria.")
        print("\nTry:")
        print("  - Removing some filters")
        print("  - Using different search terms")
        print("  - Run without filters to see all policies")
        return

    for idx, policy in enumerate(policies, 1):
        print(format_policy_summary(policy, idx))

    print(f"{'='*80}")
    print(f"Total: {len(policies)} policies")
    print(f"{'='*80}\n")

def display_statistics(data: Dict[str, Any]):
    """Display policy statistics from metadata."""
    metadata = data.get('metadata', {})

    print("\n" + "="*80)
    print("POLICY LIBRARY STATISTICS")
    print("="*80)

    print(f"\nTotal Policies: {metadata.get('totalPolicies', 0)}")
    print(f"Version: {metadata.get('version', 'Unknown')}")
    print(f"Generated: {metadata.get('generated', 'Unknown')}")

    # Source distribution
    print("\n--- Sources ---")
    source_dist = metadata.get('sourceDistribution', {})
    for source, count in source_dist.items():
        print(f"  {source}: {count} policies")

    # Category distribution
    print("\n--- Categories ---")
    category_dist = metadata.get('categoryDistribution', {})
    for category, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} policies")

    # Framework distribution
    print("\n--- Frameworks ---")
    framework_dist = metadata.get('frameworkDistribution', {})
    for framework, count in sorted(framework_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {framework}: {count} policies")

    print("\n" + "="*80 + "\n")

def list_categories(policies: List[Dict[str, Any]]) -> List[str]:
    """Extract unique categories from policies."""
    categories = set()
    for policy in policies:
        category = policy.get('category')
        if category:
            categories.add(category)
    return sorted(categories)

def list_frameworks(policies: List[Dict[str, Any]]) -> List[str]:
    """Extract unique frameworks from policies."""
    frameworks = set()
    for policy in policies:
        for framework in policy.get('frameworks', []):
            frameworks.add(framework)
    return sorted(frameworks)

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Browse cybersecurity policy templates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show all policies
  python browse_policies.py

  # Show statistics
  python browse_policies.py --stats

  # Filter by source
  python browse_policies.py --source SANS
  python browse_policies.py --source CIS

  # Filter by category
  python browse_policies.py --category "Governance"
  python browse_policies.py --category "Identity and Access"

  # Filter by framework
  python browse_policies.py --framework "ISO 27001"
  python browse_policies.py --framework "SOC 2"

  # Search in title/category
  python browse_policies.py --search "incident"
  python browse_policies.py --search "access"

  # Combine filters
  python browse_policies.py --source SANS --framework "SOC 2" --search "data"

  # List available categories
  python browse_policies.py --list-categories

  # List available frameworks
  python browse_policies.py --list-frameworks
        """
    )

    parser.add_argument(
        '--policies-file',
        default='../references/policies.json',
        help='Path to policies.json file (default: ../references/policies.json)'
    )

    parser.add_argument(
        '--source',
        choices=['SANS', 'CIS', 'sans', 'cis'],
        help='Filter by source (SANS or CIS)'
    )

    parser.add_argument(
        '--category',
        help='Filter by category (e.g., "Governance", "Identity and Access")'
    )

    parser.add_argument(
        '--framework',
        help='Filter by framework (e.g., "ISO 27001", "SOC 2", "NIST CSF")'
    )

    parser.add_argument(
        '--search',
        help='Search in policy title and category'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display policy library statistics'
    )

    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='List all available categories'
    )

    parser.add_argument(
        '--list-frameworks',
        action='store_true',
        help='List all available frameworks'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    # Resolve relative path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    policies_path = os.path.join(script_dir, args.policies_file)

    # Load policies
    data = load_policies(policies_path)
    policies = data.get('policies', [])

    # Handle statistics display
    if args.stats:
        display_statistics(data)
        return

    # Handle list categories
    if args.list_categories:
        categories = list_categories(policies)
        print("\nAvailable Categories:")
        print("=" * 50)
        for category in categories:
            count = sum(1 for p in policies if p.get('category') == category)
            print(f"  {category} ({count} policies)")
        print("=" * 50)
        print(f"\nTotal: {len(categories)} categories\n")
        return

    # Handle list frameworks
    if args.list_frameworks:
        frameworks = list_frameworks(policies)
        print("\nAvailable Frameworks:")
        print("=" * 50)
        for framework in frameworks:
            count = sum(1 for p in policies if framework in p.get('frameworks', []))
            print(f"  {framework} ({count} policies)")
        print("=" * 50)
        print(f"\nTotal: {len(frameworks)} frameworks\n")
        return

    # Filter policies
    filtered = filter_policies(
        policies,
        source=args.source,
        category=args.category,
        framework=args.framework,
        search=args.search
    )

    # Output results
    if args.json:
        # JSON output
        output = {
            "total_available": len(policies),
            "total_found": len(filtered),
            "filters": {
                "source": args.source,
                "category": args.category,
                "framework": args.framework,
                "search": args.search
            },
            "policies": filtered
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        display_results(filtered, len(policies))

        # Show filter summary
        if any([args.source, args.category, args.framework, args.search]):
            print("Active Filters:")
            if args.source:
                print(f"  Source: {args.source}")
            if args.category:
                print(f"  Category: {args.category}")
            if args.framework:
                print(f"  Framework: {args.framework}")
            if args.search:
                print(f"  Search: '{args.search}'")
            print()

if __name__ == "__main__":
    main()
