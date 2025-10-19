# Security & Compliance Marketplace

**Professional Security and Compliance Plugins for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection/releases)
[![Plugins](https://img.shields.io/badge/plugins-2-green.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection)

A curated collection of production-ready security and compliance plugins for Claude Code. The only marketplace dedicated exclusively to privacy regulations, security auditing, and compliance automation.

## 🚀 Quick Start

```bash
# Add marketplace to Claude Code
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Install plugins
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install cybersecurity-policy-generator@security-compliance-marketplace
```

---

## Available Plugins

### 1. GDPR Auditor
**Production Ready** • **v1.0.0** • **Data Privacy & Compliance**

Comprehensive GDPR compliance auditing plugin that analyzes static code files, database schemas, and configurations for EU data protection regulation compliance.

**Key Features:**
- Scans source code for personal data collection patterns
- Analyzes database schema files (SQL DDL, migrations) for sensitive data
- Verifies data subject rights implementation
- Audits security measures and encryption configurations
- Generates detailed compliance audit reports
- 8 comprehensive reference documents covering GDPR articles
- 5 automated scanning tools (static file analysis only)

**Use Cases:**
- Pre-launch GDPR compliance checks
- Regular compliance audits and monitoring
- Privacy policy development and validation
- Data protection impact assessments (DPIA)
- Third-party vendor security assessments
- Security review preparation

**Who Should Use:**
- Web application developers
- DevOps and infrastructure teams
- Privacy officers and DPOs
- Security consultants and auditors
- Startup founders preparing for EU markets
- Legal and compliance teams

[→ View GDPR Auditor Documentation](./gdpr-auditor/README.md)

---

### 2. Cybersecurity Policy Generator
**Production Ready** • **v1.0.0** • **Security Governance & Compliance**

Professional cybersecurity policy document generator using 51 industry-standard templates from SANS and CIS Controls. Creates complete, framework-compliant policy documents customized for your organization.

**Key Features:**
- 51 professional policy templates (36 SANS + 15 CIS Controls)
- Interactive AskUserQuestion workflow with beautiful UI
- Compliance framework mappings (ISO 27001, SOC 2, NIST CSF, CIS Controls v8, GDPR)
- Multi-format generation (Markdown, Word, HTML, PDF)
- 15 security policy categories covering all InfoSec domains
- Organization customization with branding options
- 4 automated policy generation scripts
- 320KB reference data with compliance mappings

**Policy Categories:**
- **Governance** (13 policies) - Information Security, Acceptable Use, Password Management
- **Identity & Access** (8 policies) - Access Control, Authentication, Remote Access
- **Application Security** (7 policies) - Secure Development, API Security, Code Review
- **Compute & Network** (10 policies) - Cloud Security, Network Security, Virtualization
- **Data Protection** (2 policies) - Data Classification, Data Recovery & Backup
- **Operations, Resilience, Risk, and more** (11 policies)

**Use Cases:**
- Starting a new security program (foundational policies)
- Preparing for compliance audits (ISO 27001, SOC 2, NIST CSF, CIS Controls)
- Updating outdated or missing security policies
- Creating incident response, data protection, or access control policies
- Building comprehensive policy documentation for framework compliance
- Meeting insurance or vendor security requirements

**Who Should Use:**
- CISOs and security leaders starting or improving security programs
- Compliance officers preparing for audits
- Startups establishing security governance
- IT managers needing standardized policies
- Consultants creating client security documentation
- Organizations pursuing ISO 27001, SOC 2, or NIST compliance

[→ View Cybersecurity Policy Generator Documentation](./cybersecurity-policy-generator/README.md)

---

## Installation

### Prerequisites

- **Claude Code** (latest version recommended)
- **Python 3.8+** (for automated tools and scripts)
- **Git** (for repository cloning)

### Option 1: Plugin Marketplace (Recommended)

```bash
# Add the Security & Compliance Marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Browse available plugins
/plugin list

# Install specific plugins
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install cybersecurity-policy-generator@security-compliance-marketplace

# Update installed plugins
/plugin update
```

**Benefits:**
- ✅ One-command installation
- ✅ Automatic updates
- ✅ Easy plugin management
- ✅ Version tracking

### Option 2: Manual Installation

```bash
# Navigate to Claude skills directory
cd ~/.claude/skills/

# Clone repository
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Symlink desired plugins
ln -s ClaudeSkillCollection/gdpr-auditor ./gdpr-auditor
ln -s ClaudeSkillCollection/cybersecurity-policy-generator ./cybersecurity-policy-generator

# Restart Claude Code
```

### Option 3: Direct Download

```bash
# Clone and extract specific plugin
cd ~/.claude/plugins/
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git temp
cp -r temp/gdpr-auditor ./
cp -r temp/cybersecurity-policy-generator ./
rm -rf temp
```

### Verification

Test that plugins are loaded:

**For GDPR Auditor:**
```
"Can you help me audit my application for GDPR compliance?"
```

**For Policy Generator:**
```
"Generate cybersecurity policies for my organization"
```

[→ Full Installation Guide](./docs/installation.md)

---

## How Plugins Work

Claude Code plugins are specialized prompts with supporting materials that give Claude domain expertise:

1. **Automatic Loading** - Mention the plugin's domain or use explicit commands
2. **Context Injection** - Claude loads plugin knowledge and workflows
3. **Tool Access** - Claude uses plugin-specific scripts and reference materials
4. **Guided Workflow** - Claude follows systematic methodology for thorough analysis

### Example: GDPR Auditor Workflow

```
User: "Audit my app for GDPR compliance"
  ↓
Claude loads gdpr-auditor plugin
  ↓
Plugin guides Claude through:
  1. Identify scope and personal data types
  2. Run automated code scanners
  3. Consult GDPR reference materials
  4. Analyze code and configurations
  5. Generate compliance audit report
  ↓
Professional audit report with specific findings
```

### Example: Policy Generator Workflow

```
User: "Generate security policies for my startup"
  ↓
Claude loads cybersecurity-policy-generator plugin
  ↓
Plugin guides Claude through:
  1. Ask policy quantity and selection (AskUserQuestion UI)
  2. Collect organization information (interactive)
  3. Select compliance frameworks and branding
  4. Generate policies in requested formats
  5. Provide organized output with summaries
  ↓
Complete policy documents ready for review
```

---

## Repository Structure

```
ClaudeSkillCollection/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
├── MARKETPLACE.md                  # Marketplace documentation
├── CHANGELOG.md                    # Version history
├── QUICKSTART.md                   # Quick start guide
│
├── .claude-plugin/                 # Marketplace configuration
│   └── marketplace.json
│
├── gdpr-auditor/                   # GDPR Compliance Auditor Plugin
│   ├── README.md
│   ├── SKILL.md
│   ├── plugin.json
│   ├── scripts/                    # 5 automated scanning tools
│   ├── references/                 # 8 GDPR reference documents
│   └── examples/
│
├── cybersecurity-policy-generator/ # Cybersecurity Policy Generator Plugin
│   ├── README.md
│   ├── SKILL.md
│   ├── plugin.json
│   ├── scripts/                    # 4 policy generation scripts
│   ├── references/                 # 320KB policy templates & mappings
│   ├── output/                     # Generated policies directory
│   └── examples/
│
├── docs/                           # Documentation
│   └── installation.md
│
└── .github/                        # GitHub templates
    └── ISSUE_TEMPLATE/
```

---

## Quality Standards

All plugins in this marketplace meet professional quality standards:

### Documentation
- ✅ Comprehensive README with clear instructions
- ✅ Detailed usage examples and workflows
- ✅ Technical specifications and requirements
- ✅ Reference materials from authoritative sources

### Code Quality
- ✅ Production-ready Python scripts with error handling
- ✅ Type hints and comprehensive docstrings
- ✅ Defensive security practices only
- ✅ Tested on real-world projects
- ✅ Follows Claude Code plugin best practices

### Accuracy & Compliance
- ✅ Information verified against primary sources
  - **GDPR Auditor:** EUR-Lex official GDPR text, ICO guidance, EDPB guidelines
  - **Policy Generator:** SANS policy templates, CIS Controls v8, ISO 27001, NIST CSF
- ✅ No hallucinated facts or unverified claims
- ✅ Regular updates to reflect current standards
- ✅ Clear version tracking and changelog

### Plugin Design Principles
- ✅ Produces tangible deliverables (reports, documents, policies)
- ✅ Works with static files (no live system scanning)
- ✅ Based on objective criteria (regulations, standards, frameworks)
- ✅ Includes comprehensive reference materials
- ✅ Follows systematic, reproducible workflows

---

## Roadmap

### Upcoming Plugins

**Data Privacy & Security:**
- [ ] **CCPA Compliance Auditor** - California Consumer Privacy Act compliance
- [ ] **HIPAA Privacy Auditor** - Healthcare privacy and security compliance
- [ ] **PCI DSS Auditor** - Payment Card Industry security standards

**Security Assessment:**
- [ ] **OWASP Top 10 Scanner** - Web application security vulnerability analysis
- [ ] **API Security Auditor** - REST/GraphQL security assessment
- [ ] **Container Security Scanner** - Docker and Kubernetes security audit

**Governance & Documentation:**
- [ ] **Privacy Policy Generator** - GDPR, CCPA-compliant privacy policies
- [ ] **Security Documentation Generator** - Technical security documentation
- [ ] **Compliance Evidence Generator** - Audit evidence and attestations

**Code Quality:**
- [ ] **Accessibility Auditor** - WCAG 2.1 AA/AAA compliance checking
- [ ] **Infrastructure as Code Reviewer** - Terraform/CloudFormation security review

[Vote for next plugins](https://github.com/diegocconsolini/ClaudeSkillCollection/issues) or suggest new ones!

---

## Contributing

We welcome contributions from the security and compliance community!

**Ways to Contribute:**
- Report bugs or suggest improvements
- Enhance existing plugins
- Create new plugins
- Improve documentation
- Share usage examples

**Contribution Process:**
1. Review [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines
2. Check existing issues and pull requests
3. Follow plugin quality standards
4. Submit pull request with clear description

**Plugin Submission Checklist:**
- [ ] Comprehensive SKILL.md with clear workflow
- [ ] Production-ready scripts with error handling
- [ ] Reference materials from authoritative sources
- [ ] Complete README with installation and usage guide
- [ ] Working examples and test cases
- [ ] Follows defensive security principles
- [ ] No malicious code or unethical use cases

---

## Support

**Getting Help:**
- **Documentation:** Check plugin README files and docs/
- **Issues:** [Open a GitHub issue](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)
- **Discussions:** [Join GitHub Discussions](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)

**Reporting Issues:**

Please include:
1. Claude Code version
2. Plugin name and version
3. Steps to reproduce
4. Expected vs actual behavior
5. Relevant code snippets (sanitized)

---

## License

MIT License - See [LICENSE](./LICENSE) for details

**What this means:**
- ✅ Free for commercial use
- ✅ Modify and distribute freely
- ✅ Private use allowed
- ⚠️ No warranty provided
- ⚠️ Must include original license and copyright notice

---

## Disclaimer

**These plugins are analysis tools** - they do not replace professional advice:

- **Legal Compliance:** Consult qualified legal counsel for compliance matters
- **Security Audits:** Professional security assessments still recommended
- **Privacy Assessments:** Work with certified privacy professionals
- **Framework Certification:** Plugins support but don't guarantee certification

**Accuracy:**
- Plugins provide guidance based on current information
- Regulations and standards change over time
- Always verify findings with authoritative sources
- No liability for errors, omissions, or consequences of use

**Ethical Use Only:**
All plugins are designed for **defensive security purposes**:
- ✅ Identifying vulnerabilities to remediate them
- ✅ Improving compliance and security posture
- ✅ Protecting user privacy and data
- ❌ NOT for exploitation, malicious use, or unethical purposes

---

## Changelog

### Version 1.1.0 (2025-10-19)
**New Plugin Release:**
- Released **Cybersecurity Policy Generator** v1.0.0
  - 51 professional policy templates (SANS + CIS Controls)
  - 320KB reference data with compliance framework mappings
  - Interactive AskUserQuestion workflow
  - Multi-format generation (Markdown, Word, HTML, PDF)
  - 15 security policy categories
  - Production-tested with real organization

**Improvements:**
- Enhanced marketplace with security governance capabilities
- Updated repository structure and documentation
- Improved installation instructions

### Version 1.0.0 (2025-10-18)
**Initial Release:**
- Released **GDPR Auditor** v1.0.0
  - 8 comprehensive GDPR reference documents
  - 5 automated static code scanning tools
  - Complete compliance audit workflow
  - Production-tested on real applications

---

## Acknowledgments

**Inspiration:**
This marketplace was created to provide high-quality, domain-specific security and compliance tools for the Claude Code ecosystem.

**Data Sources:**
- **GDPR Auditor:** EUR-Lex (Official EU Law), ICO Guidance, EDPB Guidelines
- **Policy Generator:** SANS Institute Policy Templates, CIS Controls v8, ISO 27001, NIST Cybersecurity Framework, SOC 2 Trust Service Criteria
- **Best Practices:** OWASP, NIST, CIS Benchmarks, industry-standard frameworks

**Community:**
Thanks to all contributors, testers, and users who help improve these plugins!

---

**Security & Compliance Marketplace** - Professional plugins for Claude Code
