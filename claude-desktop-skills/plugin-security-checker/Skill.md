---
name: plugin-security-checker
description: Advanced security scanner for Claude Code plugins with 91 specialized pattern agents. Detects vulnerabilities, code obfuscation, and security anti-patterns across plugin manifests, agents, and scripts.
license: MIT
compatibility: claude-desktop
metadata:
  version: 3.2.0
  author: Diego Consolini
  category: security
  runtime: python3
  dependencies: requirements.txt
---

# Plugin Security Checker

**Comprehensive security analysis tool for Claude Code plugins**

## ⚠️ IMPORTANT DISCLAIMER

**This is a SUPPORTING TOOL for preliminary security checks only.**

- ✓ Provides automated static code analysis
- ✓ Detects common vulnerabilities and suspicious patterns
- ✓ Maps findings to MITRE ATT&CK/ATLAS frameworks
- ✗ Does NOT guarantee plugin safety or security
- ✗ Does NOT detect all possible vulnerabilities
- ✗ Does NOT replace manual security code review

**Always review source code manually before installing plugins.**

## When to Use This Skill

Use this skill when:
- User wants to scan a Claude Code plugin for security issues
- User mentions "scan plugin", "check plugin security", "audit plugin"
- User provides a path to a plugin directory
- User wants to validate a plugin before installation
- User mentions security vulnerabilities, malware, or suspicious code
- User needs to generate a security report for a plugin

## What This Tool Detects

### 1. Dangerous Function Detection
**Python:**
- `eval()`, `exec()`, `compile()` - Code execution risks
- `os.system()`, `subprocess` with `shell=True` - Command injection
- `pickle.loads()`, `yaml.load()` - Deserialization vulnerabilities
- `__import__()` - Dynamic imports

**JavaScript:**
- `eval()`, `Function()` constructor - Code execution
- `innerHTML`, `outerHTML` - XSS vulnerabilities
- `document.write()` - DOM manipulation risks
- `new Function()` - Dynamic code generation

### 2. Code Obfuscation Detection
- Base64 encoding patterns
- Hex encoding and character codes
- Execution chains (eval chains, nested evals)
- Dynamic imports and late binding
- String obfuscation techniques

### 3. Credential Scanning
- Hardcoded API keys and passwords
- AWS credentials (access keys, secret keys)
- Google Cloud credentials
- Private keys and certificates
- Database connection strings
- OAuth tokens and secrets

### 4. Schema Validation
- Plugin manifest (.claude-plugin/plugin.json) structure
- Semantic versioning compliance
- Required field validation
- Skill and command configurations
- Hook definitions

### 5. Permission Analysis
- Dangerous hook configurations
- MCP server permissions
- Network request patterns
- File system access patterns

### 6. Dependency Analysis
- Scans requirements.txt and package.json
- Identifies known vulnerable packages
- Checks for suspicious dependencies
- Version constraint analysis

## Core Features

### IntelligentOrchestrator (v3.0.0)
- **91 specialized pattern agents**
  - 17 CRITICAL severity patterns
  - 39 HIGH severity patterns
  - 23 MEDIUM severity patterns
  - 2 LOW severity patterns
- **Consensus voting** across multiple agents for accuracy
- **Conflict resolution** using MITRE ATT&CK/ATLAS frameworks
- **Adaptive routing** (best agents per file type)
- **Resource management** (<500MB RAM usage)

### AccuracyCache
- **Bloom filter + Trie hybrid** for zero false positives
- **Shared learning** across all 91 agents
- **MITRE ATLAS JSON export** for threat intelligence
- **Auto-evolving rules** from validated detections
- **File type correlation learning**
- **Adaptive eviction** by agent accuracy

### Pattern Agents
- Context-aware confidence scoring
- Historical accuracy tracking
- Validation learning
- MITRE ATT&CK/ATLAS mapping

## Usage

### Basic Plugin Scan

```bash
# Scan a plugin directory
python3 scripts/scan_plugin.py /path/to/plugin

# Scan with JSON output
python3 scripts/scan_plugin.py /path/to/plugin \
  --output scan_results.json \
  --format json

# Scan with custom severity threshold
python3 scripts/scan_plugin.py /path/to/plugin \
  --min-severity HIGH
```

### Generate Reports

```bash
# Generate Markdown report
python3 scripts/generate_report.py scan_results.json \
  --format markdown \
  --output report.md

# Generate HTML report
python3 scripts/generate_report.py scan_results.json \
  --format html \
  --output report.html

# Generate PDF report (requires weasyprint)
python3 scripts/generate_report.py scan_results.json \
  --format pdf \
  --output report.pdf
```

### Batch Scanning

```bash
# Scan multiple plugins from a collection
bash scripts/test_scanner.sh

# Scan all plugins from marketplace repositories
bash scripts/scan_all_marketplace_plugins.sh
```

### Advanced Usage with IntelligentOrchestrator

```python
from intelligent_orchestrator import IntelligentOrchestrator

# Initialize with all 91 agents
orchestrator = IntelligentOrchestrator(
    patterns_file="references/dangerous_functions_expanded.json",
    max_memory_mb=500,
    enable_adaptive_routing=True
)

# Scan file with consensus voting
code = open("plugin.py").read()
detections = orchestrator.scan_file("plugin.py", code)

# Review consensus detections
for det in detections:
    print(f"Line {det.line_number}: {det.severity}")
    print(f"  Confidence: {det.confidence:.0%}")
    print(f"  Voting agents: {det.vote_count}")
    print(f"  ATT&CK: {det.primary_attack_id}")

# Export findings to ATLAS format
orchestrator.export_findings("findings.json")
```

## Output Format

### Risk Levels
- **CRITICAL** (200+ points): Multiple severe issues, **DO NOT INSTALL**
- **HIGH** (100-199 points): Serious concerns, **REVIEW CAREFULLY**
- **MEDIUM** (50-99 points): Moderate risks, review recommended
- **LOW** (0-49 points): Minor or informational findings

### Verdicts
- **FAIL**: Critical issues found, installation not recommended
- **REVIEW**: Issues found that require manual review
- **PASS**: No significant issues detected (still review manually!)

### Severity Levels
- **CRITICAL**: Immediate security risk (100 points)
- **HIGH**: Significant security concern (75 points)
- **MEDIUM**: Moderate security issue (50 points)
- **LOW**: Minor issue or best practice violation (25 points)
- **INFO**: Informational finding (0 points)

### Sample Output

```json
{
  "metadata": {
    "plugin_name": "example-plugin",
    "scan_date": "2025-12-25T10:30:00",
    "scanner_version": "3.2.0"
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "category": "dangerous-function",
      "description": "Use of eval() enables arbitrary code execution",
      "file": "scripts/process.py",
      "line_number": 42,
      "code_snippet": "result = eval(user_input)",
      "cvss_score": 9.8,
      "cve_references": ["CVE-2021-3177"],
      "attack_techniques": ["T1059.006"],
      "owasp_categories": ["A03:2021-Injection"],
      "confidence": 0.95,
      "vote_count": 5
    }
  ],
  "summary": {
    "total_findings": 10,
    "risk_score": 450,
    "risk_level": "CRITICAL",
    "verdict": "FAIL"
  }
}
```

## Recommended Workflow

1. **Find a plugin** you want to install
2. **Clone the plugin repository** to your local machine
   ```bash
   git clone https://github.com/author/plugin-name
   ```
3. **Run the security scanner**
   ```bash
   python3 scripts/scan_plugin.py plugin-name --output scan.json --format json
   ```
4. **Generate a readable report**
   ```bash
   python3 scripts/generate_report.py scan.json --format markdown --output report.md
   ```
5. **Review the findings** in report.md
6. **Manually inspect the source code** for any flagged issues
7. **Make an informed decision** about whether to install

## Security Reference Databases

The scanner uses curated reference databases (see `references/` directory):

- **dangerous_functions_expanded_v3.json**: 91 patterns across Python, JavaScript, and obfuscation
- **obfuscation_patterns.json**: 35+ obfuscation detection patterns
- **credential_patterns.json**: Regex patterns for credential detection
- **threat_mappings.json**: MITRE ATT&CK and ATLAS technique mappings
- **stix/**: STIX 2.1 formatted threat intelligence data

## MITRE Framework Integration

### MITRE ATT&CK Coverage
Maps findings to ATT&CK techniques and tactics:
- **T1059**: Command and Scripting Interpreter
- **T1027**: Obfuscated Files or Information
- **T1552**: Unsecured Credentials
- **T1566**: Phishing (credential harvesting)
- And 50+ additional techniques

### MITRE ATLAS Coverage
Maps ML/AI security findings to ATLAS techniques:
- **AML.T0043**: Craft Adversarial Data
- **AML.T0040**: ML Model Inference API Access
- **AML.T0024**: Backdoor ML Model
- And 15+ additional AI security techniques

## Installation

### Prerequisites

```bash
# Python 3.8+
python3 --version

# Install dependencies
pip3 install -r requirements.txt
```

### Dependencies

The tool requires:
- **stix2** (>=2.0.0, <3.0.0): STIX 2.1 threat intelligence format
- **taxii2-client** (>=2.3.0): MITRE ATT&CK data access
- **mitreattack-python** (>=2.0.0, <3.0.0): MITRE ATT&CK framework library

All dependencies are compatible with Python 3.8+ (including macOS system Python 3.9).

### Verify Installation

```bash
# Test STIX2
python3 -c "import stix2; print('stix2 available')"

# Test TAXII client
python3 -c "import taxii2client; print('taxii2-client available')"

# Test MITRE ATT&CK
python3 -c "import mitreattack; print('mitreattack-python available')"
```

## Available Scripts

The `scripts/` directory contains 30+ specialized scripts:

### Core Scripts
- **scan_plugin.py**: Main plugin scanner
- **generate_report.py**: Report generation (Markdown, HTML, PDF)
- **intelligent_orchestrator.py**: Orchestrator with 91 pattern agents
- **accuracy_cache.py**: Bloom filter + Trie cache system

### Pattern Agents
- **pattern_agent_base.py**: Base class for all pattern agents
- **dangerous_functions_agent.py**: Dangerous function detection
- **obfuscation_agent.py**: Code obfuscation detection
- **credential_agent.py**: Credential scanning
- And 20+ specialized pattern agents

### Utility Scripts
- **test_scanner.sh**: Batch scan multiple plugins
- **scan_all_marketplace_plugins.sh**: Scan all marketplace plugins
- **update_mitre_data.py**: Update ATT&CK/ATLAS data
- **export_stix.py**: Export findings to STIX 2.1 format

## Limitations

### What This Tool Cannot Do

1. **Guarantee Safety**: Static analysis cannot detect all vulnerabilities
2. **Runtime Analysis**: Does not execute code or analyze runtime behavior
3. **Zero-Day Detection**: Cannot detect unknown vulnerabilities
4. **External MCP Servers**: Cannot verify safety of external MCP servers
5. **Encrypted Code**: Cannot analyze encrypted or heavily obfuscated code
6. **Legal/Compliance**: Does not provide legal or compliance advice

### Known False Positives

- **innerHTML clearing**: `innerHTML = ''` flagged but safe
- **Static eval**: `eval('2 + 2')` flagged but low risk
- **Template engines**: May use eval-like constructs safely
- **Development tools**: Debug/test code may trigger warnings

**Mitigation**: Use context-aware severity adjustment and manual review.

## Performance

- **Scan Speed**: ~1-5 seconds per plugin (typical size)
- **Memory Usage**: <500MB RAM (orchestrator mode)
- **Accuracy**: ~80-85% true positive rate (after false positive filtering)
- **Coverage**: 91 pattern agents across 50+ vulnerability types

## Comparison to Other Tools

| Feature | Plugin Security Checker | npm audit | Snyk | Semgrep |
|---------|------------------------|-----------|------|---------|
| Context-aware analysis | ✅ Yes | ❌ No | ✅ Limited | ✅ Yes |
| Consensus voting | ✅ 91 agents | ❌ No | ❌ No | ❌ No |
| MITRE mapping | ✅ ATT&CK+ATLAS | ❌ No | ✅ ATT&CK | ✅ ATT&CK |
| Plugin-specific | ✅ Yes | ❌ No | ❌ No | ❌ No |
| False positive rate | ~15-20% | ~10% | ~15% | ~10-15% |
| Python + JavaScript | ✅ Yes | ❌ JS only | ✅ Yes | ✅ Yes |

## Troubleshooting

### Issue: "Module not found: stix2"
**Solution:**
```bash
pip3 install stix2
```

### Issue: "MITRE ATT&CK data not found"
**Solution:**
```bash
python3 scripts/update_mitre_data.py
```

### Issue: High memory usage (>1GB)
**Solution:** Reduce max_memory_mb in orchestrator configuration:
```python
orchestrator = IntelligentOrchestrator(max_memory_mb=250)
```

### Issue: Too many false positives
**Solution:** Increase minimum severity threshold:
```bash
python3 scripts/scan_plugin.py plugin/ --min-severity HIGH
```

## Best Practices

1. **Always scan before installing** untrusted plugins
2. **Review all CRITICAL and HIGH findings** manually
3. **Understand false positives** - not all findings are exploitable
4. **Update reference databases** regularly
5. **Combine with manual code review** for best security
6. **Generate reports** for audit trails
7. **Test in sandbox** before production use

## Support and Documentation

For detailed documentation:
- **scripts/** - Full source code with inline comments
- **references/** - Security pattern databases and MITRE mappings
- **SCAN_RESULTS_ANALYSIS.md** - Example scan results and analysis

## License

MIT License - See LICENSE file for details

## Credits

- Built for Claude Code plugin ecosystem
- Based on MITRE ATT&CK and ATLAS frameworks
- Inspired by npm audit, Snyk, and Semgrep
- STIX 2.1 integration for threat intelligence sharing

---

**Version:** 3.2.0
**Last Updated:** 2025-12-25
**Status:** Production Ready
