"""
Auto-generate 63 specialized agents from dangerous_functions_expanded.json

Each agent is an expert in ONE specific dangerous pattern
"""

import json
from pathlib import Path
from typing import Dict, List
from pattern_agent import PatternAgent
from accuracy_cache import AccuracyCache


def load_patterns(patterns_file: str) -> Dict:
    """Load dangerous patterns from JSON"""
    with open(patterns_file, 'r') as f:
        return json.load(f)


def generate_agents(patterns_data: Dict, cache: AccuracyCache) -> List[PatternAgent]:
    """
    Generate specialized agents from pattern database

    Returns: List of PatternAgent instances (63 total)
    """
    agents = []

    for language, severity_levels in patterns_data.items():
        if language == "metadata":
            continue

        for severity, patterns in severity_levels.items():
            for func_name, func_info in patterns.items():
                # Create agent ID
                agent_id = f"{func_name}-agent".lower().replace('.', '-').replace('_', '-')

                # Extract pattern info
                pattern = func_info.get('detection_pattern', f"\\b{func_name}\\s*\\(")
                description = func_info.get('description', f"Detects {func_name}")
                attack_id = func_info.get('attack_id')
                atlas_id = func_info.get('atlas_id')
                cwe = func_info.get('cwe')
                cvss = func_info.get('cvss', 5.0)

                # Context checks (if specified)
                context_check = func_info.get('context_check')
                context_checks = []
                if context_check and "user_input" in context_check:
                    context_checks = [
                        r"user_input",
                        r"request\.",
                        r"input\(",
                        r"sys\.argv",
                        r"params\[",
                        r"query\."
                    ]

                # Create specialized agent
                agent = PatternAgent(
                    agent_id=agent_id,
                    pattern=pattern,
                    severity=severity.upper(),
                    description=description,
                    attack_id=attack_id,
                    atlas_id=atlas_id,
                    cwe=cwe,
                    cvss=cvss,
                    context_checks=context_checks,
                    cache=cache
                )

                agents.append(agent)

    return agents


def print_agent_manifest(agents: List[PatternAgent]):
    """Print manifest of all generated agents"""
    print("=" * 80)
    print(f"AGENT MANIFEST: {len(agents)} Specialized Pattern Detection Agents")
    print("=" * 80)

    # Group by severity
    by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
    for agent in agents:
        by_severity.get(agent.severity, []).append(agent)

    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        agents_in_severity = by_severity[severity]
        if agents_in_severity:
            print(f"\n{severity}: {len(agents_in_severity)} agents")
            for agent in agents_in_severity:
                attack_info = f" [{agent.attack_id}]" if agent.attack_id else ""
                atlas_info = f" [{agent.atlas_id}]" if agent.atlas_id else ""
                print(f"  - {agent.agent_id:30s} {attack_info}{atlas_info}")


if __name__ == "__main__":
    # Load patterns
    patterns_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded.json"

    print(f"Loading patterns from: {patterns_file}")
    patterns = load_patterns(str(patterns_file))

    # Create shared cache
    cache = AccuracyCache(max_detections=100000)

    # Generate all agents
    agents = generate_agents(patterns, cache)

    # Print manifest
    print_agent_manifest(agents)

    # Test a few agents
    print("\n" + "=" * 80)
    print("TESTING SAMPLE AGENTS")
    print("=" * 80)

    test_code = """
import os
import subprocess

# Critical: eval with user input
result = eval(user_data)

# Critical: exec
exec(malicious_code)

# High: os.system
os.system("rm -rf /")

# High: subprocess with shell=True
subprocess.run(cmd, shell=True)

# Medium: requests.get
requests.get(untrusted_url)
"""

    # Test first 5 agents
    for agent in agents[:5]:
        detections = agent.detect(test_code, "test.py", "py")
        if detections:
            print(f"\n{agent.agent_id}:")
            for det in detections:
                print(f"  Line {det.line_number}: {det.severity} (confidence: {det.confidence:.0%})")

    print(f"\n✓ Generated {len(agents)} agents successfully")
