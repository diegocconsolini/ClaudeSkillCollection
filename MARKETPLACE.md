# Security & Compliance Marketplace

**A Community Claude Code Plugin Marketplace for Security, Privacy, and Compliance Auditing**

Version: 1.0.0
Category: Security & Compliance
Repository: [diegocconsolini/ClaudeSkillCollection](https://github.com/diegocconsolini/ClaudeSkillCollection)

---

## Overview

The **Security & Compliance Marketplace** is a community-driven Claude Code plugin marketplace dedicated exclusively to privacy regulations, security auditing, and compliance automation. Our plugins are production-ready, professionally maintained, and verified against authoritative sources.

### Why This Marketplace?

**Unique Focus:**
- Community marketplace specializing in security and compliance
- Production-tested on real-world applications
- Verified against authoritative sources (EUR-Lex, ICO, OWASP, NIST)
- Defensive security only (ethical focus)
- Professional documentation and support

**Target Audience:**
- Privacy Officers & Data Protection Officers (DPOs)
- Security Consultants & Auditors
- Compliance Teams
- Startup Founders (pre-launch compliance checks)
- DevOps & Security Engineers
- Enterprise Development Teams
- Legal & Regulatory Affairs

---

## Quick Start

### Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
```

### Browse Plugins

```bash
/plugin
```

Select "Browse Plugins" and choose from the Security & Compliance Marketplace.

### Install a Plugin

```bash
/plugin install gdpr-auditor@security-compliance-marketplace
```

---

## Available Plugins

### 1. GDPR Auditor ✅ Production Ready

**Version:** 1.0.0
**Category:** Data Privacy & Compliance
**Status:** Production Ready

Comprehensive GDPR compliance auditing skill that analyzes codebases, databases, and systems for EU data protection regulation compliance.

**Features:**
- Scans code for personal data collection patterns
- Analyzes database schemas for sensitive data
- Verifies data subject rights implementation (access, deletion, portability)
- Audits security measures and encryption
- Generates detailed compliance reports with specific code references
- 8 comprehensive reference documents covering GDPR articles
- 5 automated scanning tools (Python)

**Verified Against:**
- EUR-Lex Official GDPR Text
- ICO (UK Information Commissioner's Office) Guidance
- EDPB (European Data Protection Board) Guidelines

**Quick Install:**
```bash
/plugin install gdpr-auditor@security-compliance-marketplace
```

**Usage:**
```
"Audit my application for GDPR compliance"
"Check if my database schema complies with GDPR"
"Generate a GDPR compliance report for my codebase"
```

[→ Full GDPR Auditor Documentation](./gdpr-auditor/README.md)

---

## Roadmap

### Coming Soon (Q1-Q2 2026)

#### Data Privacy & Compliance
- **CCPA Auditor** - California Consumer Privacy Act compliance
- **HIPAA Compliance Checker** - US healthcare privacy regulations
- **PCI DSS Security Auditor** - Payment card industry standards
- **Privacy Policy Generator** - Automated privacy policy creation

#### Security Auditing
- **Security Vulnerability Scanner** - OWASP Top 10 analysis
- **API Security Auditor** - REST/GraphQL security review
- **Container Security Scanner** - Docker/K8s security checks
- **Secrets Detection Tool** - Find exposed credentials and API keys

#### Code Quality & Accessibility
- **Accessibility Auditor** - WCAG 2.1/2.2 compliance
- **Performance Analyzer** - Bottleneck detection and optimization
- **Code Documentation Generator** - Auto-generate professional docs

#### DevOps & Infrastructure
- **Infrastructure as Code Reviewer** - Terraform/CloudFormation security
- **CI/CD Pipeline Security** - Build pipeline vulnerability scanning
- **Cloud Security Posture** - AWS/Azure/GCP security configuration

**Vote for next plugins:** [GitHub Issues](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)

---

## Plugin Categories

All plugins are organized into clear categories:

### 🔒 Security
- Vulnerability scanning
- Penetration testing assistance (defensive only)
- Security configuration auditing
- Secrets detection

### 📋 Compliance
- GDPR, CCPA, HIPAA auditing
- PCI DSS compliance
- SOC 2 preparation
- ISO 27001 assessment

### 🔐 Privacy
- Privacy policy analysis
- Data protection impact assessments (DPIA)
- Consent mechanism reviews
- Data subject rights automation

### 🛡️ Defensive Security
- Threat modeling
- Security best practices
- Secure coding patterns
- Incident response planning

---

## Quality Standards

Every plugin in this marketplace adheres to strict quality standards:

### Documentation ✅
- Comprehensive README with installation instructions
- Clear usage examples and workflows
- Technical specifications and requirements
- Troubleshooting guide
- Reference materials from authoritative sources

### Code Quality ✅
- Production-ready scripts with error handling
- Type hints and comprehensive docstrings
- Defensive security practices (no malicious code)
- Tested on real-world projects
- Follows Claude Code plugin best practices

### Accuracy ✅
- Information verified against primary sources
- No hallucinated facts or fake examples
- Regular updates to reflect current standards
- Clear version tracking and changelogs

### Security ✅
- Defensive security only (no offensive tools)
- No credential harvesting or exploitation tools
- Ethical use guidelines
- Regular security audits

---

## Use Cases

### Pre-Launch Compliance Checks
Run comprehensive audits before launching your application to ensure compliance with privacy regulations and security standards.

```bash
/plugin install gdpr-auditor@security-compliance-marketplace
# "Audit my application for GDPR compliance before launch"
```

### Regular Security Audits
Periodically scan your codebase for security vulnerabilities, compliance issues, and privacy risks.

### Third-Party Vendor Assessment
Evaluate third-party services and APIs for compliance and security risks.

### Privacy Policy Development
Generate and validate privacy policies based on actual data handling practices in your codebase.

### Data Protection Impact Assessments (DPIA)
Conduct DPIAs for high-risk processing activities as required by GDPR Article 35.

### Security Reviews
Perform comprehensive security reviews of authentication, authorization, encryption, and data handling.

---

## Installation Methods

### Method 1: Plugin Marketplace (Recommended)

```bash
# Add marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Install specific plugin
/plugin install gdpr-auditor@security-compliance-marketplace
```

### Method 2: Direct Repository Clone

```bash
# Navigate to Claude plugins directory
cd ~/.claude/plugins/

# Clone marketplace
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Restart Claude Code
```

### Method 3: Individual Plugin Installation

```bash
# Navigate to Claude plugins directory
cd ~/.claude/plugins/

# Clone and copy specific plugin
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git temp
cp -r temp/gdpr-auditor ./
rm -rf temp

# Restart Claude Code
```

---

## Verification

After installation, verify the plugin is loaded:

```
"Can you help me audit my application for GDPR compliance?"
```

You should see: `The gdpr-auditor plugin is running...`

---

## Requirements

### Minimum Requirements
- Claude Code (any version supporting plugins)
- Python 3.8+ (for automated scanning tools)
- Git (for installation)

### Recommended
- Claude Code (latest version)
- Python 3.10+
- 50 MB disk space per plugin

### Platform Support
- ✅ Linux (Ubuntu 20.04+, Debian, Fedora, Arch)
- ✅ macOS (12+)
- ✅ Windows 10/11 (WSL recommended for Python tools)

---

## Community & Support

### Getting Help

**Documentation:**
- Main README: [README.md](./README.md)
- Plugin-specific docs: See each plugin's directory
- Quick Start Guide: [QUICKSTART.md](./QUICKSTART.md)

**Issues & Bugs:**
- GitHub Issues: [Report Issues](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)
- Include: Claude version, plugin version, error messages, steps to reproduce

**Discussions:**
- GitHub Discussions: [Join Discussions](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)
- Feature requests, Q&A, community support

### Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Ways to Contribute:**
- Report bugs or issues
- Suggest new plugins
- Improve existing plugins
- Add documentation
- Share usage examples
- Submit test cases

---

## Marketplace Management

### Update Marketplace

```bash
# Pull latest changes
cd ~/.claude/plugins/ClaudeSkillCollection
git pull

# Or remove and re-add
/plugin marketplace remove security-compliance-marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
```

### Remove Marketplace

```bash
/plugin marketplace remove security-compliance-marketplace
```

### Check Installed Plugins

```bash
/plugin
# Select "Manage Installed Plugins"
```

---

## Comparison with Other Marketplaces

| Feature | Security & Compliance | General Marketplaces |
|---------|----------------------|---------------------|
| **Specialization** | Security, Privacy, Compliance focus | General purpose |
| **Verification** | Verified against legal/regulatory sources | Varies |
| **Production Ready** | All plugins production-tested | Mixed quality |
| **Ethical Focus** | Defensive security only | No specific focus |
| **Target Audience** | Security/Compliance professionals | General developers |
| **Documentation** | Comprehensive, professional | Varies |
| **Support** | Dedicated security expertise | General |

---

## Legal & Disclaimer

### Scope of Tools

These plugins are **tools to assist analysis** - they do not replace professional advice:

- **Legal Compliance:** Consult qualified legal counsel for compliance matters
- **Security Audits:** Professional security audits still recommended
- **Privacy Assessments:** Work with certified privacy professionals

### Accuracy

While we strive for accuracy:
- Plugins provide guidance based on current information
- Regulations and standards change over time
- Always verify findings with authoritative sources
- No liability for errors or omissions

### Defensive Security Only

All tools are designed for **defensive security purposes only**:
- ✅ Identifying vulnerabilities to fix them
- ✅ Improving compliance and security posture
- ✅ Security research and education
- ❌ NOT for exploitation or malicious use
- ❌ NOT for credential harvesting
- ❌ NOT for unauthorized access

---

## License

All plugins in this marketplace are licensed under the **MIT License** - see [LICENSE](./LICENSE) file for details.

**What This Means:**
- ✅ Free to use commercially
- ✅ Modify and distribute
- ✅ Private use
- ❗ No warranty provided
- ❗ Include original license and copyright

---

## Statistics

**Marketplace Statistics:**
- Total Plugins: 1 (production) + 12 (roadmap)
- Lines of Code: 6,000+
- Reference Documents: 8+
- Automated Tools: 5+
- Supported Regulations: GDPR, CCPA (coming), HIPAA (coming)
- GitHub Stars: Building community
- Contributors: Open to contributions

---

## Changelog

### Version 1.0.0 (2025-10-19)
- ✅ Initial marketplace launch
- ✅ GDPR Auditor plugin v1.0.0
  - 8 comprehensive reference documents
  - 5 automated scanning tools
  - Complete audit workflow
  - Tested on real-world applications
- ✅ Marketplace infrastructure
- ✅ Professional documentation
- ✅ GitHub integration

---

## Contact

- **Repository:** https://github.com/diegocconsolini/ClaudeSkillCollection
- **Issues:** https://github.com/diegocconsolini/ClaudeSkillCollection/issues
- **Discussions:** https://github.com/diegocconsolini/ClaudeSkillCollection/discussions

---

**Security & Compliance Marketplace** - A community Claude Code marketplace dedicated to professional security, privacy, and compliance auditing.

*Empowering developers and security professionals with production-ready compliance tools.*
