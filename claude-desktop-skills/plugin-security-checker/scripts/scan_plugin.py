#!/usr/bin/env python3
"""
Plugin Security Checker - Main Scanner
Version: 1.0.0

A SUPPORTING TOOL for preliminary security checks of Claude Code plugins.

IMPORTANT DISCLAIMER:
This tool provides basic security checks but does NOT guarantee plugin safety.
Users are ultimately responsible for reviewing and approving plugins they install.
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Finding:
    """Represents a security finding"""
    id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str
    subcategory: str
    file: str
    line: int
    column: int
    code_snippet: str
    description: str
    explanation: str
    impact: str
    recommendation: str
    cvss_score: float
    cve_reference: Optional[str] = None
    owasp_reference: Optional[str] = None
    remediation_effort: str = "MEDIUM"
    false_positive_likelihood: str = "LOW"


class PluginScanner:
    """Main scanner class for analyzing Claude Code plugins"""

    def __init__(self, plugin_path: str, references_path: str):
        self.plugin_path = Path(plugin_path)
        self.references_path = Path(references_path)
        self.findings: List[Finding] = []
        self.finding_counter = 0

        # Load reference databases
        self.dangerous_functions = self._load_json(
            self.references_path / "dangerous_functions.json"
        )
        self.obfuscation_patterns = self._load_json(
            self.references_path / "obfuscation_patterns.json"
        )

    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON reference file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}", file=sys.stderr)
            sys.exit(1)

    def _generate_finding_id(self) -> str:
        """Generate unique finding ID"""
        self.finding_counter += 1
        return f"FINDING-{self.finding_counter:03d}"

    def scan(self) -> Dict[str, Any]:
        """Main scan orchestration"""
        print(f"[*] Scanning plugin: {self.plugin_path}")

        # Step 1: Validate plugin structure
        print("[*] Step 1/5: Validating plugin.json schema...")
        self._validate_plugin_json()

        # Step 2: Scan Python files
        print("[*] Step 2/5: Scanning Python files...")
        self._scan_python_files()

        # Step 3: Scan JavaScript files
        print("[*] Step 3/5: Scanning JavaScript files...")
        self._scan_javascript_files()

        # Step 4: Analyze dependencies
        print("[*] Step 4/5: Analyzing dependencies...")
        self._analyze_dependencies()

        # Step 5: Check permissions
        print("[*] Step 5/5: Checking permissions and hooks...")
        self._check_permissions()

        # Generate report
        return self._generate_report()

    def _validate_plugin_json(self):
        """Validate plugin.json structure"""
        plugin_json_path = self.plugin_path / ".claude-plugin" / "plugin.json"

        if not plugin_json_path.exists():
            self.findings.append(Finding(
                id=self._generate_finding_id(),
                severity="CRITICAL",
                category="Schema Validation",
                subcategory="Missing File",
                file=".claude-plugin/plugin.json",
                line=0,
                column=0,
                code_snippet="",
                description="Missing required plugin.json file",
                explanation="Claude Code plugins MUST have a .claude-plugin/plugin.json file at the plugin root.",
                impact="Plugin will not be recognized by Claude Code",
                recommendation="Create .claude-plugin/plugin.json with required fields",
                cvss_score=0.0,
                remediation_effort="LOW"
            ))
            return

        try:
            with open(plugin_json_path, 'r') as f:
                plugin_data = json.load(f)

            # Check required fields
            required_fields = ["name", "version", "description"]
            for field in required_fields:
                if field not in plugin_data:
                    self.findings.append(Finding(
                        id=self._generate_finding_id(),
                        severity="HIGH",
                        category="Schema Validation",
                        subcategory="Missing Field",
                        file=".claude-plugin/plugin.json",
                        line=0,
                        column=0,
                        code_snippet=json.dumps(plugin_data, indent=2)[:200],
                        description=f"Missing required field: {field}",
                        explanation=f"Plugin must specify '{field}' in plugin.json",
                        impact="Plugin may not load correctly",
                        recommendation=f"Add '{field}' field to plugin.json",
                        cvss_score=0.0,
                        remediation_effort="LOW"
                    ))

            # Check for hardcoded credentials
            plugin_str = json.dumps(plugin_data)
            credential_patterns = [
                (r'(?i)(api[_-]?key|apikey)\s*["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', "API Key"),
                (r'(?i)(secret[_-]?key|secretkey)\s*["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', "Secret Key"),
                (r'(?i)(password|passwd)\s*["\']?\s*[:=]\s*["\']([^"\']{6,})["\']', "Password"),
            ]

            for pattern, cred_type in credential_patterns:
                if re.search(pattern, plugin_str):
                    self.findings.append(Finding(
                        id=self._generate_finding_id(),
                        severity="CRITICAL",
                        category="Credentials",
                        subcategory="Hardcoded Secrets",
                        file=".claude-plugin/plugin.json",
                        line=0,
                        column=0,
                        code_snippet="[REDACTED]",
                        description=f"Hardcoded {cred_type} detected in plugin.json",
                        explanation="Credentials should never be hardcoded. Use environment variables instead.",
                        impact="Credential exposure, unauthorized access",
                        recommendation="Use environment variables via ${env:VAR_NAME} syntax",
                        cvss_score=9.0,
                        cve_reference="CVE-2025-54795",
                        owasp_reference="API8: Security Misconfiguration",
                        remediation_effort="LOW"
                    ))

        except json.JSONDecodeError as e:
            self.findings.append(Finding(
                id=self._generate_finding_id(),
                severity="CRITICAL",
                category="Schema Validation",
                subcategory="Invalid JSON",
                file=".claude-plugin/plugin.json",
                line=e.lineno if hasattr(e, 'lineno') else 0,
                column=e.colno if hasattr(e, 'colno') else 0,
                code_snippet="",
                description=f"Invalid JSON syntax: {e.msg}",
                explanation="plugin.json must be valid JSON",
                impact="Plugin will not load",
                recommendation="Fix JSON syntax errors",
                cvss_score=0.0,
                remediation_effort="LOW"
            ))

    def _scan_python_files(self):
        """Scan all Python files in plugin"""
        python_files = list(self.plugin_path.rglob("*.py"))

        if not python_files:
            return

        for py_file in python_files:
            # Skip virtual environments and common excluded directories
            if any(x in py_file.parts for x in ['venv', 'env', '.venv', 'node_modules', '__pycache__']):
                continue

            self._scan_python_file(py_file)

    def _scan_python_file(self, filepath: Path):
        """Scan individual Python file using AST analysis"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            # Parse AST
            tree = ast.parse(source, filename=str(filepath))

            # Visit nodes for dangerous functions
            visitor = DangerousFunctionVisitor(
                filepath=filepath,
                source=source,
                scanner=self,
                dangerous_functions=self.dangerous_functions['python']
            )
            visitor.visit(tree)

            # Pattern-based detection
            self._scan_python_patterns(filepath, source)

        except SyntaxError as e:
            self.findings.append(Finding(
                id=self._generate_finding_id(),
                severity="MEDIUM",
                category="Code Quality",
                subcategory="Syntax Error",
                file=str(filepath.relative_to(self.plugin_path)),
                line=e.lineno or 0,
                column=e.offset or 0,
                code_snippet=e.text or "",
                description=f"Python syntax error: {e.msg}",
                explanation="Code contains syntax errors",
                impact="Code will not execute",
                recommendation="Fix syntax errors",
                cvss_score=0.0,
                remediation_effort="LOW"
            ))
        except Exception as e:
            print(f"[!] Error scanning {filepath}: {e}", file=sys.stderr)

    def _scan_python_patterns(self, filepath: Path, source: str):
        """Pattern-based scanning for Python code"""
        lines = source.split('\n')

        # Check for obfuscation patterns
        python_obf = self.obfuscation_patterns.get('python', {})

        # Count occurrences for threshold-based detection
        pattern_counts = {}

        for category, patterns in python_obf.items():
            if category in ['detection_tools', 'packing']:
                continue

            for pattern_name, pattern_data in patterns.items():
                if 'pattern' not in pattern_data:
                    continue

                pattern = pattern_data['pattern']
                matches = list(re.finditer(pattern, source, re.MULTILINE))

                if matches:
                    pattern_counts[pattern_name] = len(matches)
                    threshold = pattern_data.get('threshold', 1)

                    if len(matches) >= threshold:
                        # Find first match for reporting
                        first_match = matches[0]
                        line_num = source[:first_match.start()].count('\n') + 1

                        # Get line content
                        line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                        severity = pattern_data.get('severity', 'MEDIUM')

                        self.findings.append(Finding(
                            id=self._generate_finding_id(),
                            severity=severity,
                            category="Code Obfuscation",
                            subcategory=category.replace('_', ' ').title(),
                            file=str(filepath.relative_to(self.plugin_path)),
                            line=line_num,
                            column=first_match.start() - source.rfind('\n', 0, first_match.start()),
                            code_snippet=line_content.strip(),
                            description=f"{pattern_data.get('description', pattern_name)} (found {len(matches)} times, threshold: {threshold})",
                            explanation=pattern_data.get('example', 'Obfuscation pattern detected'),
                            impact="Code obfuscation hides true intent, may indicate malicious behavior",
                            recommendation="Review code for legitimate use case or remove obfuscation",
                            cvss_score=7.5 if severity == "HIGH" else 5.0,
                            remediation_effort="MEDIUM",
                            false_positive_likelihood="MEDIUM" if threshold > 1 else "LOW"
                        ))

    def _scan_javascript_files(self):
        """Scan JavaScript/TypeScript files"""
        js_files = list(self.plugin_path.rglob("*.js")) + \
                   list(self.plugin_path.rglob("*.ts")) + \
                   list(self.plugin_path.rglob("*.jsx")) + \
                   list(self.plugin_path.rglob("*.tsx"))

        for js_file in js_files:
            # Skip node_modules and build directories
            if any(x in js_file.parts for x in ['node_modules', 'dist', 'build', '.next']):
                continue

            self._scan_javascript_file(js_file)

    def _scan_javascript_file(self, filepath: Path):
        """Scan individual JavaScript file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            lines = source.split('\n')

            # Pattern-based detection for JavaScript dangerous functions
            js_dangerous = self.dangerous_functions.get('javascript', {})

            for severity_level, functions in js_dangerous.items():
                if severity_level == 'detection_strategies':
                    continue

                for func_name, func_data in functions.items():
                    pattern = func_data.get('detection_pattern', '')
                    if not pattern:
                        continue

                    matches = list(re.finditer(pattern, source, re.MULTILINE))

                    for match in matches:
                        line_num = source[:match.start()].count('\n') + 1
                        col_num = match.start() - source.rfind('\n', 0, match.start())
                        line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                        self.findings.append(Finding(
                            id=self._generate_finding_id(),
                            severity=func_data.get('severity', 'MEDIUM'),
                            category="Dangerous Function",
                            subcategory="Code Execution",
                            file=str(filepath.relative_to(self.plugin_path)),
                            line=line_num,
                            column=col_num,
                            code_snippet=line_content.strip(),
                            description=func_data.get('description', f"Use of {func_name}"),
                            explanation=f"{func_data.get('risk', 'Security risk')}. {func_data.get('safe_alternative', 'Avoid this function.')}",
                            impact=func_data.get('risk', 'Potential security vulnerability'),
                            recommendation=func_data.get('safe_alternative', 'Refactor code'),
                            cvss_score=func_data.get('cvss', 5.0),
                            cve_reference=func_data.get('cve_reference'),
                            remediation_effort="MEDIUM"
                        ))

            # Obfuscation pattern detection
            self._scan_javascript_patterns(filepath, source)

        except Exception as e:
            print(f"[!] Error scanning {filepath}: {e}", file=sys.stderr)

    def _scan_javascript_patterns(self, filepath: Path, source: str):
        """Pattern-based obfuscation detection for JavaScript"""
        lines = source.split('\n')
        js_obf = self.obfuscation_patterns.get('javascript', {})

        for category, patterns in js_obf.items():
            if category in ['detection_tools', 'webpack_indicators']:
                continue

            for pattern_name, pattern_data in patterns.items():
                if 'pattern' not in pattern_data:
                    continue

                pattern = pattern_data['pattern']
                matches = list(re.finditer(pattern, source, re.MULTILINE))

                if matches:
                    threshold = pattern_data.get('threshold', 1)

                    if len(matches) >= threshold:
                        first_match = matches[0]
                        line_num = source[:first_match.start()].count('\n') + 1
                        col_num = first_match.start() - source.rfind('\n', 0, first_match.start())
                        line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                        severity = pattern_data.get('severity', 'MEDIUM')

                        self.findings.append(Finding(
                            id=self._generate_finding_id(),
                            severity=severity,
                            category="Code Obfuscation",
                            subcategory=category.replace('_', ' ').title(),
                            file=str(filepath.relative_to(self.plugin_path)),
                            line=line_num,
                            column=col_num,
                            code_snippet=line_content.strip()[:100],
                            description=f"{pattern_data.get('description', pattern_name)} (found {len(matches)} times)",
                            explanation=pattern_data.get('example', 'Obfuscation detected'),
                            impact="Code obfuscation may hide malicious intent",
                            recommendation="Review code for legitimate obfuscation need",
                            cvss_score=7.5 if severity == "HIGH" else 5.0,
                            remediation_effort="MEDIUM",
                            false_positive_likelihood="MEDIUM"
                        ))

    def _analyze_dependencies(self):
        """Analyze package dependencies for security issues"""
        # Check Python requirements.txt
        requirements_txt = self.plugin_path / "requirements.txt"
        if requirements_txt.exists():
            self._check_python_dependencies(requirements_txt)

        # Check Node.js package.json
        package_json = self.plugin_path / "package.json"
        if package_json.exists():
            self._check_node_dependencies(package_json)

    def _check_python_dependencies(self, filepath: Path):
        """Check Python dependencies for known issues"""
        try:
            with open(filepath, 'r') as f:
                requirements = f.readlines()

            # Basic checks for now - could integrate with vulnerability databases later
            for line_num, line in enumerate(requirements, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Check for unpinned versions (security best practice)
                if '==' not in line and '>=' not in line and '~=' not in line:
                    self.findings.append(Finding(
                        id=self._generate_finding_id(),
                        severity="LOW",
                        category="Dependency Management",
                        subcategory="Unpinned Version",
                        file="requirements.txt",
                        line=line_num,
                        column=0,
                        code_snippet=line,
                        description="Unpinned dependency version",
                        explanation="Unpinned versions can lead to unexpected behavior from dependency updates",
                        impact="Potential compatibility issues or unexpected behavior",
                        recommendation="Pin dependency versions using == or ~=",
                        cvss_score=3.0,
                        remediation_effort="LOW"
                    ))

        except Exception as e:
            print(f"[!] Error analyzing Python dependencies: {e}", file=sys.stderr)

    def _check_node_dependencies(self, filepath: Path):
        """Check Node.js dependencies"""
        try:
            with open(filepath, 'r') as f:
                package_data = json.load(f)

            # Check for install scripts (CVE-2025-59828)
            scripts = package_data.get('scripts', {})
            dangerous_script_patterns = ['postinstall', 'preinstall', 'install']

            for script_name in dangerous_script_patterns:
                if script_name in scripts:
                    self.findings.append(Finding(
                        id=self._generate_finding_id(),
                        severity="HIGH",
                        category="Dependency Management",
                        subcategory="Install Script",
                        file="package.json",
                        line=0,
                        column=0,
                        code_snippet=f'"{script_name}": "{scripts[script_name]}"',
                        description=f"Dangerous install script: {script_name}",
                        explanation="Install scripts execute automatically during npm/yarn install and can run malicious code",
                        impact="Arbitrary code execution during package installation",
                        recommendation="Review install script necessity, consider removing",
                        cvss_score=7.7,
                        cve_reference="CVE-2025-59828",
                        remediation_effort="MEDIUM"
                    ))

        except Exception as e:
            print(f"[!] Error analyzing Node dependencies: {e}", file=sys.stderr)

    def _check_permissions(self):
        """Check permission configurations and hooks"""
        # Check hooks.json if exists
        hooks_json = self.plugin_path / ".claude-plugin" / "hooks.json"
        if hooks_json.exists():
            try:
                with open(hooks_json, 'r') as f:
                    hooks_data = json.load(f)

                # Check for auto-accept suggestions
                hooks_str = json.dumps(hooks_data).lower()
                if 'auto-accept' in hooks_str or 'autoaccept' in hooks_str:
                    self.findings.append(Finding(
                        id=self._generate_finding_id(),
                        severity="CRITICAL",
                        category="Permissions",
                        subcategory="Auto-Accept Mode",
                        file=".claude-plugin/hooks.json",
                        line=0,
                        column=0,
                        code_snippet="[auto-accept reference detected]",
                        description="Plugin suggests or enables auto-accept mode",
                        explanation="Auto-accept mode bypasses all security prompts and is extremely dangerous",
                        impact="Complete bypass of Claude Code security model",
                        recommendation="Remove auto-accept suggestions entirely",
                        cvss_score=9.0,
                        owasp_reference="API8: Security Misconfiguration",
                        remediation_effort="LOW"
                    ))

            except Exception as e:
                print(f"[!] Error analyzing hooks.json: {e}", file=sys.stderr)

        # Check MCP server configurations
        mcp_servers_dir = self.plugin_path / "mcp-servers"
        if mcp_servers_dir.exists():
            for mcp_file in mcp_servers_dir.rglob("*.json"):
                self._check_mcp_server(mcp_file)

    def _check_mcp_server(self, filepath: Path):
        """Check MCP server configuration for security issues"""
        try:
            with open(filepath, 'r') as f:
                mcp_data = json.load(f)

            # Check for WebSocket usage (CVE-2025-52882)
            if 'transport' in mcp_data:
                transport = mcp_data['transport']
                if isinstance(transport, dict) and transport.get('type') == 'websocket':
                    if not transport.get('auth'):
                        self.findings.append(Finding(
                            id=self._generate_finding_id(),
                            severity="HIGH",
                            category="MCP Security",
                            subcategory="WebSocket Authentication",
                            file=str(filepath.relative_to(self.plugin_path)),
                            line=0,
                            column=0,
                            code_snippet=json.dumps(transport, indent=2),
                            description="WebSocket transport without authentication",
                            explanation="WebSocket MCP servers without proper authentication are vulnerable to bypass attacks",
                            impact="Authentication bypass, unauthorized access",
                            recommendation="Implement proper authentication for WebSocket transport",
                            cvss_score=8.8,
                            cve_reference="CVE-2025-52882",
                            remediation_effort="MEDIUM"
                        ))

        except Exception as e:
            print(f"[!] Error analyzing MCP server {filepath}: {e}", file=sys.stderr)

    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        # Calculate risk scores
        severity_weights = {
            "CRITICAL": 100,
            "HIGH": 75,
            "MEDIUM": 50,
            "LOW": 25,
            "INFO": 0
        }

        total_score = sum(severity_weights.get(f.severity, 0) for f in self.findings)

        # Determine overall risk level
        if total_score >= 200:
            risk_level = "CRITICAL"
            verdict = "FAIL"
        elif total_score >= 100:
            risk_level = "HIGH"
            verdict = "REVIEW"
        elif total_score >= 50:
            risk_level = "MEDIUM"
            verdict = "REVIEW"
        else:
            risk_level = "LOW"
            verdict = "PASS"

        # Count findings by severity
        severity_counts = {}
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            severity_counts[severity] = len([f for f in self.findings if f.severity == severity])

        # Generate report
        report = {
            "metadata": {
                "plugin_path": str(self.plugin_path),
                "scan_date": datetime.now().isoformat(),
                "scanner_version": "1.0.0",
                "total_findings": len(self.findings),
                "risk_level": risk_level,
                "risk_score": total_score,
                "verdict": verdict
            },
            "summary": {
                "severity_counts": severity_counts,
                "categories": self._categorize_findings()
            },
            "findings": [asdict(f) for f in sorted(
                self.findings,
                key=lambda x: (severity_weights.get(x.severity, 0), x.id),
                reverse=True
            )],
            "disclaimer": self._get_disclaimer()
        }

        return report

    def _categorize_findings(self) -> Dict[str, int]:
        """Categorize findings by category"""
        categories = {}
        for finding in self.findings:
            categories[finding.category] = categories.get(finding.category, 0) + 1
        return categories

    def _get_disclaimer(self) -> str:
        """Get security disclaimer text"""
        return """
⚠️ IMPORTANT SECURITY DISCLAIMER

This is a SUPPORTING TOOL for preliminary security checks.

What this tool DOES:
✓ Detects common code obfuscation patterns
✓ Identifies dangerous function usage
✓ Validates plugin.json structure
✓ Flags suspicious code patterns
✓ Provides security recommendations

What this tool does NOT do:
✗ Guarantee plugin safety or security
✗ Detect all possible vulnerabilities
✗ Replace manual security code review
✗ Provide legal or compliance advice
✗ Detect zero-day vulnerabilities
✗ Analyze runtime behavior

YOUR RESPONSIBILITY:
🔒 YOU are ultimately responsible for plugins you install and use
📖 ALWAYS review plugin source code manually before installation
🛡️ ONLY install plugins from sources you trust
🔍 VERIFY the plugin author's identity and reputation
💻 RUN untrusted plugins in sandboxed environments only
⚠️ USE this tool at your own risk

LIMITATIONS:
- Static analysis only (no runtime analysis)
- May produce false positives
- May miss sophisticated attacks
- Obfuscation detection is heuristic-based
- Cannot detect social engineering
- Cannot verify external MCP server safety

LEGAL:
This tool is provided "AS IS" without warranty of any kind, express or
implied. The authors assume no liability for damages resulting from the
use of this tool or from installing plugins scanned by this tool.
"""


class DangerousFunctionVisitor(ast.NodeVisitor):
    """AST visitor to detect dangerous Python function calls"""

    def __init__(self, filepath: Path, source: str, scanner: PluginScanner, dangerous_functions: Dict):
        self.filepath = filepath
        self.source = source
        self.scanner = scanner
        self.dangerous_functions = dangerous_functions
        self.lines = source.split('\n')

    def visit_Call(self, node: ast.Call):
        """Visit function call nodes"""
        func_name = self._get_function_name(node.func)

        if func_name:
            # Check all severity levels
            for severity_level, functions in self.dangerous_functions.items():
                if severity_level == 'detection_strategies':
                    continue

                if func_name in functions:
                    func_data = functions[func_name]

                    # Special handling for subprocess with shell=True
                    if 'subprocess' in func_name:
                        if not self._has_shell_true(node):
                            self.generic_visit(node)
                            return

                    # Get line content
                    line_content = self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else ""

                    self.scanner.findings.append(Finding(
                        id=self.scanner._generate_finding_id(),
                        severity=func_data.get('severity', 'MEDIUM'),
                        category="Dangerous Function",
                        subcategory="Code Execution" if 'eval' in func_name or 'exec' in func_name else "Command Injection",
                        file=str(self.filepath.relative_to(self.scanner.plugin_path)),
                        line=node.lineno,
                        column=node.col_offset,
                        code_snippet=line_content.strip(),
                        description=func_data.get('description', f"Use of {func_name}"),
                        explanation=f"{func_data.get('risk', 'Security risk')}",
                        impact=func_data.get('risk', 'Potential security vulnerability'),
                        recommendation=func_data.get('safe_alternative', 'Refactor code to avoid this function'),
                        cvss_score=func_data.get('cvss', 5.0),
                        cve_reference=func_data.get('cve_reference'),
                        remediation_effort="MEDIUM"
                    ))

        self.generic_visit(node)

    def _get_function_name(self, node) -> Optional[str]:
        """Extract function name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            # Handle os.system, subprocess.run, etc.
            if isinstance(node.value, ast.Name):
                return f"{node.value.id}.{node.attr}"
        return None

    def _has_shell_true(self, node: ast.Call) -> bool:
        """Check if subprocess call has shell=True"""
        for keyword in node.keywords:
            if keyword.arg == 'shell':
                if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    return True
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Plugin Security Checker - Scan Claude Code plugins for security issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/plugin
  %(prog)s /path/to/plugin --output report.json
  %(prog)s /path/to/plugin --format markdown --output report.md

IMPORTANT: This tool is for preliminary checks only. Users are responsible
for reviewing plugins before installation. See --disclaimer for details.
        """
    )

    parser.add_argument(
        'plugin_path',
        help='Path to Claude Code plugin directory'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)',
        default=None
    )

    parser.add_argument(
        '--format', '-f',
        choices=['json', 'markdown', 'html'],
        default='json',
        help='Output format (default: json)'
    )

    parser.add_argument(
        '--references',
        help='Path to references directory (default: ../references)',
        default=None
    )

    parser.add_argument(
        '--disclaimer',
        action='store_true',
        help='Show security disclaimer and exit'
    )

    args = parser.parse_args()

    # Show disclaimer if requested
    if args.disclaimer:
        scanner = PluginScanner(".", ".")
        print(scanner._get_disclaimer())
        sys.exit(0)

    # Determine references path
    if args.references:
        references_path = Path(args.references)
    else:
        script_dir = Path(__file__).parent
        references_path = script_dir.parent / "references"

    if not references_path.exists():
        print(f"Error: References directory not found: {references_path}", file=sys.stderr)
        sys.exit(1)

    # Validate plugin path
    plugin_path = Path(args.plugin_path)
    if not plugin_path.exists():
        print(f"Error: Plugin path not found: {plugin_path}", file=sys.stderr)
        sys.exit(1)

    # Run scanner
    scanner = PluginScanner(plugin_path, references_path)
    report = scanner.scan()

    # Output report
    if args.format == 'json':
        output = json.dumps(report, indent=2)
    elif args.format == 'markdown':
        # Import report generator for markdown
        try:
            script_dir = Path(__file__).parent
            sys.path.insert(0, str(script_dir))
            from generate_report import ReportGenerator
            generator = ReportGenerator(report)
            output = generator.generate_markdown()
        except ImportError as e:
            print(f"Error importing report generator: {e}", file=sys.stderr)
            print("Falling back to JSON format", file=sys.stderr)
            output = json.dumps(report, indent=2)
    elif args.format == 'html':
        # Import report generator for HTML
        try:
            script_dir = Path(__file__).parent
            sys.path.insert(0, str(script_dir))
            from generate_report import ReportGenerator
            generator = ReportGenerator(report)
            output = generator.generate_html()
        except ImportError as e:
            print(f"Error importing report generator: {e}", file=sys.stderr)
            print("Falling back to JSON format", file=sys.stderr)
            output = json.dumps(report, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"[+] Report written to: {args.output}")
        print(f"[+] Risk Level: {report['metadata']['risk_level']}")
        print(f"[+] Verdict: {report['metadata']['verdict']}")
        print(f"[+] Total Findings: {report['metadata']['total_findings']}")
    else:
        print(output)


if __name__ == '__main__':
    main()
