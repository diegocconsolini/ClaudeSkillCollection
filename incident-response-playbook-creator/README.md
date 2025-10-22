# Incident Response Playbook Creator

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NIST SP 800-61r3](https://img.shields.io/badge/NIST-SP%20800--61r3-green.svg)](https://doi.org/10.6028/NIST.SP.800-61r3)

**Professional incident response playbooks from authoritative templates (NIST SP 800-61r3, CISA, NIST SP 800-161r1). Generate customized IR documentation for 11 comprehensive incident scenarios including ransomware, data breach, supply chain attacks, container/Kubernetes security, IoT/OT security, cloud breaches, API security, insider threats, and DDoS attacks with GDPR/HIPAA compliance.**

---

## 🚀 Quick Start

```bash
# Generate a ransomware playbook
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "Acme Corporation" \
  --industry "Technology"

# Browse available scenarios
python3 scripts/browse_scenarios.py --list

# View detailed scenario information
python3 scripts/browse_scenarios.py --detail ransomware
```

**Output**: Professional Markdown playbook ready for your security team

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Available Scenarios](#available-scenarios)
- [Playbook Contents](#playbook-contents)
- [Compliance](#compliance)
- [Examples](#examples)
- [Reference Data](#reference-data)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Capabilities

- ✅ **11 Comprehensive Incident Scenarios**: Ransomware, Data Breach, Phishing/BEC, AI/ML Attacks, Supply Chain, Container/Kubernetes, IoT/OT, Cloud Breach, API Security, Insider Threats, DDoS
- ✅ **NIST SP 800-61r3 Aligned**: Based on April 2025 revision with CSF 2.0 integration
- ✅ **Comprehensive NIST Coverage**: Incorporates SP 800-161r1 (Supply Chain), SP 800-190 (Container Security), SP 800-82r3 (OT Security), SP 800-218 (Secure SDLC)
- ✅ **GDPR & HIPAA Compliant**: Built-in breach notification requirements and timelines
- ✅ **Organization Customization**: Tailored playbooks with your company name, industry, contacts
- ✅ **100% Authoritative Content**: All data extracted from NIST, CISA, AWS, EUR-Lex official sources
- ✅ **Professional Format**: Ready-to-use Markdown playbooks for immediate deployment

### What's Included in Each Playbook

- 🔍 **Detection Indicators**: Technical and behavioral IOCs mapped to NIST CSF 2.0
- ⚡ **Response Procedures**: Step-by-step actions (Triage → Containment → Eradication)
- 🔄 **Recovery Actions**: System restoration with validation checklists
- 📞 **Communication Templates**: Internal, external, and regulatory notifications
- ⚖️ **Compliance Guidance**: GDPR Article 33/34 and HIPAA Breach Notification Rule
- 👥 **Roles & Responsibilities**: Clear team structure and escalation criteria
- 📊 **Post-Incident Activities**: Lessons learned and documentation requirements

---

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)

### Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

**Requirements**:
- `jinja2>=3.0.0` - Template engine for playbook generation
- `pyyaml>=6.0` - YAML parsing
- `pandas>=1.3.0` - Data manipulation (future use)
- `openpyxl>=3.0.0` - Excel generation (future use)

### Verify Installation

```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Test the browse script
python3 scripts/browse_scenarios.py --metadata

# Test the generator
python3 scripts/generate_playbook_markdown.py --list
```

---

## 🎯 Usage

### Method 1: Interactive (Recommended)

Ask Claude Code to create a playbook for you:

```
"Create an incident response playbook for ransomware attacks"
```

Claude will guide you through an interactive workflow using AskUserQuestion to collect:
- Incident scenario selection
- Organization name
- Industry sector
- Contact information (optional)

### Method 2: Command Line

#### Browse Available Scenarios

```bash
# List all scenarios with descriptions
python3 scripts/browse_scenarios.py --list

# View detailed information for a scenario
python3 scripts/browse_scenarios.py --detail ransomware

# Show dataset metadata
python3 scripts/browse_scenarios.py --metadata

# Search for scenarios
python3 scripts/browse_scenarios.py --search "data breach"
```

#### Generate a Playbook

**Basic Generation**:
```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "Acme Corporation"
```

**With Full Customization**:
```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario data_breach \
  --org "Healthcare Inc" \
  --industry "Healthcare" \
  --contact-email "security@healthcareinc.com" \
  --contact-phone "+1-555-MED-HELP" \
  --output output/healthcare-breach-playbook.md
```

**Parameters**:
- `--scenario` or `-s`: **Required**. Scenario ID (ransomware, data_breach, phishing)
- `--org` or `-o`: **Required**. Your organization name
- `--industry` or `-i`: Optional. Industry sector (default: "General")
- `--contact-email`: Optional. Security team email
- `--contact-phone`: Optional. Security team phone
- `--output`: Optional. Output file path (default: `output/[scenario]-playbook.md`)

---

## 📊 Available Scenarios

### Version 2.0.0 - 11 Comprehensive Scenarios

| Scenario ID | Name | Category | Severity | GDPR | HIPAA |
|-------------|------|----------|----------|------|-------|
| `ransomware` | Ransomware Attack | Malware | Critical | ✅ | ✅ |
| `data_breach` | Data Breach / Exfiltration | Data Breach | Critical | ✅ | ✅ |
| `phishing` | Phishing / Business Email Compromise | Social Engineering | High | ✅ | ✅ |
| `ai_ml_attack` | AI/ML Security Incident | Adversarial AI | High | ✅ | ⚠️ |
| `supply_chain_attack` | Supply Chain Attack | Supply Chain | Critical | ✅ | ✅ |
| `container_kubernetes_security` | Container/Kubernetes Security Incident | Container Orchestration | High | ✅ | ⚠️ |
| `iot_ot_security` | IoT/OT Security Incident | Operational Technology | Critical | ⚠️ | ⚠️ |
| `cloud_security_breach` | Cloud Security Breach | Cloud Infrastructure | Critical | ✅ | ✅ |
| `api_security_incident` | API Security Incident | Application Security | High | ✅ | ⚠️ |
| `insider_threat` | Insider Threat | Insider Risk | Critical | ✅ | ✅ |
| `ddos_attack` | DDoS Attack | Availability | High | ⚠️ | ⚠️ |

### Scenario Details

#### Traditional Attack Scenarios

**Ransomware Attack** (`ransomware`)
- Malware that encrypts files and demands payment for decryption
- Includes double extortion and data exfiltration tactics
- Based on NIST SP 800-61r3 and real-world incident patterns

**Data Breach / Exfiltration** (`data_breach`)
- Unauthorized access and theft of sensitive data
- Covers both external attacks and insider threats
- Comprehensive GDPR Article 33/34 and HIPAA breach notification guidance

**Phishing / Business Email Compromise** (`phishing`)
- Email-based social engineering attacks
- Credential harvesting, BEC fraud, and executive impersonation
- CEO fraud and wire transfer scam procedures

#### Modern Attack Vectors

**AI/ML Security Incident** (`ai_ml_attack`)
- Adversarial attacks on machine learning models
- Model poisoning, data poisoning, and inference attacks
- Based on OWASP Top 10 for LLMs v2025

**Supply Chain Attack** (`supply_chain_attack`)
- Compromise through third-party software or services
- Based on NIST SP 800-161r1 (Cybersecurity Supply Chain Risk Management)
- Covers SolarWinds-style attacks and dependency vulnerabilities

**Container/Kubernetes Security Incident** (`container_kubernetes_security`)
- Container escape, cluster compromise, and orchestration attacks
- Based on NIST SP 800-190 (Application Container Security Guide)
- Kubernetes-specific security controls and detection

#### Critical Infrastructure & Cloud

**IoT/OT Security Incident** (`iot_ot_security`)
- Industrial Control Systems (ICS) and SCADA security
- Based on NIST SP 800-82r3 (ICS Security)
- Safety-critical considerations for operational technology

**Cloud Security Breach** (`cloud_security_breach`)
- S3 bucket exposure, IAM compromise, and cloud misconfigurations
- Based on AWS Security Incident Response Guide
- Multi-cloud considerations (AWS, Azure, GCP)

**API Security Incident** (`api_security_incident`)
- API vulnerabilities, authentication bypass, and data exposure
- Based on OWASP API Security Top 10 and NIST SP 800-218 (Secure SDLC)
- REST, GraphQL, and microservices security

#### Insider & Availability Threats

**Insider Threat** (`insider_threat`)
- Malicious or negligent insider actions
- Data theft, sabotage, and privilege abuse
- Based on NIST guidelines for insider threat programs

**DDoS Attack** (`ddos_attack`)
- Distributed Denial of Service attacks
- Based on CISA Understanding and Responding to DDoS Attacks guide
- Application-layer and network-layer attack mitigation

---

## 📖 Playbook Contents

Each generated playbook contains:

### 1. Overview Section
- Incident type and severity classification
- NIST SP 800-61r3 reference example
- NIST CSF 2.0 function alignment

### 2. Detection & Indicators
- **Technical Indicators of Compromise**: File extensions, network patterns, system changes
- **Behavioral Indicators**: User reports, unusual activities
- **Detection Activities**: Mapped to NIST CSF DE.CM and DE.AE categories

### 3. Response Procedures
- **Phase 1 - Triage & Assessment** (0-15 minutes)
- **Phase 2 - Containment** (15 min - 2 hours)
- **Phase 3 - Eradication** (2-24 hours)

### 4. Recovery Actions
- System restoration procedures
- Validation checklists
- Enhanced monitoring requirements

### 5. Communication Requirements
- **Internal**: Executive leadership, IT team, Legal
- **External**: Law enforcement, regulators, customers
- **Public**: Media statements (if applicable)

### 6. Compliance Considerations
- **GDPR**: Article 33/34 notification timelines (72 hours)
- **HIPAA**: Breach notification requirements (60 days)
- Risk assessment factors and documentation requirements

### 7. Roles & Responsibilities
- Incident response team structure
- Role-based action items
- Escalation criteria and procedures

### 8. Contact Information
- Security team contacts
- External resources (FBI, CISA, etc.)
- Data protection authorities

### 9. Post-Incident Activities
- Lessons learned meeting agenda
- Documentation requirements
- Playbook update procedures

---

## ⚖️ Compliance

### GDPR (EU Regulation 2016/679)

**Breach Notification Requirements**:
- **Article 33**: Notify supervisory authority within **72 hours** of becoming aware
- **Article 34**: Notify data subjects **without undue delay** if high risk to rights/freedoms

**Playbook Coverage**:
- ✅ Risk assessment criteria
- ✅ Notification timelines and content requirements
- ✅ Data subject notification triggers
- ✅ Documentation obligations

### HIPAA (45 CFR §§ 164.400-414)

**Breach Notification Requirements**:
- **Individual Notification**: Within **60 days** of discovery
- **HHS Secretary**: Within **60 days** if ≥500 individuals affected
- **Media**: Within **60 days** if ≥500 residents of a state affected

**Playbook Coverage**:
- ✅ 4-factor risk assessment
- ✅ Notification timelines and methods
- ✅ Unsecured PHI determination
- ✅ Business Associate notification requirements

### Important Disclaimer

⚠️ **These playbooks are guidance tools** and do not replace professional legal, compliance, or security advice:

- Consult qualified legal counsel for compliance interpretation
- Work with certified privacy professionals for breach assessments
- Engage professional incident response firms for complex incidents
- Always verify requirements with authoritative sources and regulators

---

## 💼 Examples

### Example 1: Technology Startup

```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "TechStartup Inc" \
  --industry "Technology" \
  --contact-email "security@techstartup.io"
```

**Output**: `output/ransomware-playbook.md`
- Tailored for technology sector
- GDPR compliance (if handling EU customer data)
- Startup-appropriate team structure

### Example 2: Healthcare Organization

```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario data_breach \
  --org "HealthCare Medical Group" \
  --industry "Healthcare" \
  --contact-email "hipaa@healthcaregroup.com" \
  --contact-phone "+1-555-HIPAA-SEC"
```

**Output**: `output/data_breach-playbook.md`
- HIPAA Breach Notification Rule guidance
- PHI-specific considerations
- 60-day notification timelines

### Example 3: Financial Services

```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario phishing \
  --org "SecureBank Financial" \
  --industry "Finance" \
  --contact-email "soc@securebank.com"
```

**Output**: `output/phishing-playbook.md`
- BEC-specific procedures
- Financial fraud detection
- Customer notification requirements

---

## 📚 Reference Data

All playbook content is derived from authoritative sources:

### Primary Sources

| Source | Document | Version | Date |
|--------|----------|---------|------|
| **NIST** | SP 800-61r3 - IR Recommendations for Cybersecurity Risk Management | Revision 3 | April 2025 |
| **NIST** | Cybersecurity Framework | Version 2.0 | February 2024 |
| **NIST** | SP 800-161r1 - Cybersecurity Supply Chain Risk Management | Rev 1 Update 1 | May 2024 |
| **NIST** | SP 800-190 - Application Container Security Guide | Final | September 2017 |
| **NIST** | SP 800-82r3 - Guide to OT Security | Revision 3 | September 2023 |
| **NIST** | SP 800-218 - Secure Software Development Framework | Version 1.1 | February 2022 |
| **CISA** | Federal Incident Response Playbooks | Current | August 2024 |
| **AWS** | Security Incident Response Guide | Current | 2024 |
| **OWASP** | Top 10 for LLMs | Version 2025 | January 2025 |
| **EUR-Lex** | GDPR (Regulation 2016/679) | Official | April 2016 |
| **HHS** | HIPAA Breach Notification Rule | 45 CFR 164.400-414 | Current |

### Reference Files

Located in `references/` directory:

- `incident_scenarios_v2.json` (145KB) - 11 comprehensive incident scenarios with full NIST mappings
- `incident_scenarios_simplified.json` (9KB) - Original 3 scenarios (legacy)
- `framework_mappings.json` (36KB) - NIST CSF 2.0, GDPR, HIPAA mappings
- `communication_templates.json` (65KB) - Professional notification templates

### Data Quality Guarantee

- ✅ **No Mock Data**: All content extracted from official sources
- ✅ **No Hallucinations**: Verified against primary documents
- ✅ **Current Information**: Updated to April 2025 NIST revision
- ✅ **Compliance Accurate**: Reviewed against official legal text

---

## 🔧 Requirements

### System Requirements

- **Operating System**: macOS, Linux, Windows (with WSL)
- **Python**: 3.8 or higher
- **Disk Space**: ~5MB for plugin, ~100MB for dependencies

### Python Dependencies

```txt
jinja2>=3.0.0      # Template engine
pyyaml>=6.0        # YAML parsing
pandas>=1.3.0      # Data manipulation
openpyxl>=3.0.0    # Excel generation (future)
```

Install with:
```bash
pip install jinja2 pyyaml pandas openpyxl
```

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'jinja2'`
**Solution**: Install dependencies with `pip install -r requirements.txt`

**Problem**: `Error: Scenario 'xyz' not found`
**Solution**: Use `--list` to see all 11 available scenario IDs

**Problem**: `PermissionError` when writing output file
**Solution**: Check write permissions for output directory, or specify `--output` to a writable location

**Problem**: `Invalid JSON in scenarios file`
**Solution**: The scripts default to using `incident_scenarios_v2.json` (v2.0.0+) which contains 11 validated scenarios. If you specified a custom file, verify JSON syntax.

### Getting Help

1. Check this README first
2. Review `SKILL.md` for detailed usage instructions
3. Examine example outputs in `examples/` directory
4. Open an issue on GitHub with error details and steps to reproduce

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- **Report Bugs**: Open an issue with detailed reproduction steps
- **Suggest Scenarios**: Propose new incident types with authoritative source references
- **Improve Templates**: Enhance playbook formatting or content
- **Add Compliance**: Extend to other regulations (PCI DSS, SOC 2, etc.)
- **Documentation**: Fix typos, add examples, improve clarity

### Contribution Guidelines

1. **No Mock Data**: All contributions must use real, authoritative sources
2. **Cite Sources**: Include document references for all added content
3. **Test Thoroughly**: Verify JSON syntax and script functionality
4. **Follow Style**: Match existing code formatting and documentation style
5. **Update Changelog**: Document changes in CHANGELOG.md

---

## 📄 License

**MIT License**

Copyright (c) 2025 Diego Consolini

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🙏 Acknowledgments

### Data Sources

- **NIST** - National Institute of Standards and Technology for SP 800-61r3 and CSF 2.0
- **CISA** - Cybersecurity & Infrastructure Security Agency for federal playbooks
- **EUR-Lex** - Official Journal of the European Union for GDPR text
- **HHS** - U.S. Department of Health and Human Services for HIPAA Breach Notification Rule

### Inspiration

This plugin was created to provide high-quality, authoritative incident response guidance for the Claude Code ecosystem, helping organizations prepare for and respond to security incidents with confidence.

---

## 📞 Support

**Author**: Diego Consolini
**Email**: diego@diegocon.nl
**GitHub**: https://github.com/diegocconsolini/ClaudeSkillCollection

---

**Last Updated**: 2025-10-21
**Plugin Version**: 2.0.0
**Status**: ✅ Production Ready (11 scenarios)
