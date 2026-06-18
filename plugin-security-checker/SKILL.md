---
name: plugin-security-checker
description: Use this skill to scan a Claude Code plugin (or any npm/PyPI package tree) for security issues before installation. Detects dangerous functions, code obfuscation, hardcoded credentials, schema problems, and known 2024-2026 supply-chain attack IOCs (Shai-Hulud, Nx s1ngularity, chalk/debug clipper, Axios RAT, litellm/.pth), mapped to MITRE ATT&CK/ATLAS, CVE, and OWASP.
license: MIT
---

# Plugin Security Checker Skill

Static security analysis for Claude Code plugins and package trees. This is a
**supporting tool for preliminary checks** — it does not guarantee safety; always review
source manually before installing untrusted plugins.

## Usage

```bash
# Scan a single plugin (the documented entry point)
python3 scripts/scan_plugin.py /path/to/plugin

# JSON output
python3 scripts/scan_plugin.py /path/to/plugin --output scan.json --format json

# Generate a report from results
python3 scripts/generate_report.py scan.json --format markdown --output report.md
```

## What it checks

- **Dangerous functions** — Python (`eval`/`exec`/`os.system`/`subprocess shell=True`) and
  JavaScript (`eval`/Function/`innerHTML`), from the canonical
  `references/dangerous_functions_expanded.json` (63 Python + 18 JS patterns).
- **Obfuscation & credentials** — base64/hex/char-code chains; hardcoded API keys/tokens.
- **Schema & permissions** — `plugin.json` structure, hooks, MCP server config.
- **Supply-chain IOCs** — named 2024-2026 npm/PyPI campaigns from
  `references/supply_chain_iocs.json` (verified against primary sources).

See [`agents/plugin-security-checker.md`](agents/plugin-security-checker.md) for the full
workflow and the IntelligentOrchestrator (consensus-voting) entry points.
