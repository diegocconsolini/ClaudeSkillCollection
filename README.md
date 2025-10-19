# Security & Compliance Marketplace

**A Community Claude Code Plugin Marketplace for Security, Privacy, and Compliance Auditing**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection/releases)
[![Plugins](https://img.shields.io/badge/plugins-2-green.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection)

A curated collection of professional, production-ready security and compliance plugins for Claude Code. This is the only marketplace dedicated exclusively to privacy regulations (GDPR, CCPA, HIPAA), security auditing, and compliance automation.

## 🚀 Quick Install

**Recommended: Install via Plugin Marketplace**

```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install gdpr-auditor@security-compliance-marketplace
```

**Alternative: Traditional Skills Installation** (see below)

---

## Overview

This repository provides high-quality, well-documented security and compliance tools that you can install in Claude Code to unlock specialized capabilities. Each plugin is designed following best practices with comprehensive reference materials, automated tools, and clear workflows.

**What Makes This Different:**
- ✅ **Community marketplace dedicated to security & compliance**
- ✅ **Production-tested** on real-world applications
- ✅ **Verified against authoritative sources** (EUR-Lex, ICO, OWASP)
- ✅ **Defensive security only** (ethical focus)
- ✅ **Professional documentation** and support

## Available Skills

### 1. GDPR Auditor
**Status:** Production Ready
**Version:** 1.0.0
**Category:** Data Privacy & Compliance

Comprehensive GDPR compliance auditing plugin that analyzes static code files, database schema files, and configuration files for EU data protection regulation compliance.

**Key Features:**
- Scans source code files for personal data collection patterns
- Analyzes database schema files (SQL DDL, migrations) for sensitive data
- Verifies data subject rights implementation in code
- Audits security measures and encryption configurations
- Generates detailed compliance audit reports with specific code references
- 8 comprehensive reference documents covering GDPR articles
- 5 automated scanning tools (work with static files only)

[→ Read GDPR Auditor Documentation](./gdpr-auditor/README.md)

### 2. Cybersecurity Policy Generator
**Status:** Work in Progress (Private Development)
**Version:** 0.9.0 (Beta)
**Category:** Security Governance & Compliance

Professional cybersecurity policy document generator using 51 industry-standard templates from SANS and CIS Controls. Creates complete, framework-compliant policy documents customized for your organization in multiple formats.

**Key Features:**
- 51 professional policy templates (36 SANS + 15 CIS Controls)
- Interactive workflow using AskUserQuestion for beautiful UX
- Compliance framework mappings (ISO 27001, SOC 2, NIST CSF, CIS Controls v8, GDPR)
- Multi-format generation (Markdown, Word, HTML, PDF)
- 15 security policy categories covering all aspects of InfoSec
- Organization customization with branding options
- Production-tested with real company policies generated

**Policy Categories:**
- Governance (13 policies) - Information Security, Acceptable Use, Password, etc.
- Identity & Access (8 policies) - Access Control, Authentication, Remote Access
- Application Security (7 policies) - Secure Development, API Security
- Compute & Network (10 policies) - Cloud Security, Network Security, Virtualization
- Data Protection (2 policies) - Data Classification, Data Recovery
- And 9 more categories covering all security domains

**Use Cases:**
- Starting a security program (foundational policies)
- Preparing for compliance audits (ISO 27001, SOC 2, NIST CSF)
- Updating outdated security policies
- Creating incident response, data protection, or access control policies
- Building policy documentation for framework compliance

**Note:** This plugin is currently in private development and will be released publicly once testing is complete. It has been production-tested with Guatemaltek generating 8 foundational policies across all formats.

---

## Quick Start

### Prerequisites

- **Claude Code** (latest version with plugin support)
- **Python 3.8+** (for automated scanning tools)
- **Git** (for installation)

### Installation Options

#### ⭐ Option 1: Plugin Marketplace (Recommended)

The easiest way to install plugins from this marketplace:

```bash
# Add the Security & Compliance Marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Browse available plugins
/plugin

# Install GDPR Auditor
/plugin install gdpr-auditor@security-compliance-marketplace
```

**Benefits:**
- ✅ One-command installation
- ✅ Automatic updates via `/plugin update`
- ✅ Easy plugin management
- ✅ Access to all marketplace plugins

#### Option 2: Traditional Skills Installation

For Claude Code versions without plugin marketplace support:

```bash
# Navigate to your Claude skills directory
cd ~/.claude/skills/

# Clone the repository
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Symlink desired skills
ln -s ClaudeSkillCollection/gdpr-auditor ./gdpr-auditor

# Restart Claude Code
```

#### Option 3: Individual Plugin Download

```bash
# Navigate to your Claude plugins/skills directory
cd ~/.claude/plugins/  # or ~/.claude/skills/

# Clone and extract specific plugin
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git temp
cp -r temp/gdpr-auditor ./
rm -rf temp

# Restart Claude Code
```

### Verification

After installation, verify the plugin is loaded:

```
"Can you help me audit my application for GDPR compliance?"
```

You should see: **"The gdpr-auditor plugin is running..."**

[→ Full Installation Guide](./docs/installation.md) | [→ Marketplace Guide](./MARKETPLACE.md)

---

## 📐 Skill Design Principles

**Core Philosophy:** Claude skills are designed to help Claude **generate deliverables**, not to perform live analysis or real-time monitoring.

### ✅ Claude Skills ARE:

- **Document Generators** - Create specific file types (reports, configs, documentation)
- **Workflow Guides** - Step-by-step instructions for systematic tasks
- **Template Systems** - Reusable patterns and boilerplates
- **Format Converters** - Transform data into structured deliverables
- **Code Libraries** - Manipulate file structures and generate code

**Examples:**
- ✅ GDPR Auditor: Guides Claude to generate compliance reports by analyzing code
- ✅ Privacy Policy Generator: Creates policy documents from data practices
- ✅ Security Checklist: Produces security assessment checklists

### ❌ Claude Skills are NOT:

- **Analysis Tools** - That scan live systems or running applications
- **External Services** - That require APIs or third-party integrations
- **Real-time Monitors** - That need continuous data streams
- **Subjective Assessors** - That make judgments without clear criteria
- **Simple Calculators** - That just return a single number

**Anti-patterns:**
- ❌ "Live vulnerability scanner" - Requires real-time system access
- ❌ "API health monitor" - Needs continuous external service calls
- ❌ "Performance analyzer" - Requires runtime metrics
- ❌ "Code quality scorer" - Too subjective without clear deliverable

### Design Guidelines

**When creating a skill, ask:**

1. **Does it produce a tangible deliverable?** (report, document, config file, etc.)
2. **Can it work with static code/files?** (no live system access required)
3. **Does it follow a systematic workflow?** (clear step-by-step process)
4. **Is it based on objective criteria?** (regulations, standards, best practices)
5. **Does it include reference materials?** (authoritative sources, templates)

**Good Skill Pattern:**
```
Input: Codebase files, configuration files, documentation
Process: Systematic analysis using reference materials
Output: Structured report/document/checklist with specific findings
```

---

## Skill Development Standards

All skills in this collection adhere to these quality standards:

### Documentation
- ✅ Comprehensive README with installation instructions
- ✅ Clear usage examples and workflows
- ✅ Technical specifications and requirements
- ✅ Troubleshooting guide
- ✅ Reference materials from authoritative sources

### Code Quality
- ✅ Production-ready Python scripts with error handling
- ✅ Type hints and docstrings
- ✅ Defensive security practices (no malicious code)
- ✅ Tested on real-world projects
- ✅ Follows Claude Code plugin best practices

### Accuracy
- ✅ Information verified against primary sources
- ✅ No hallucinated facts or fake examples
- ✅ Regular updates to reflect current standards
- ✅ Clear version tracking

### Design Compliance
- ✅ Produces tangible deliverables (reports, documents, configs)
- ✅ Works with static files (no live system scanning)
- ✅ Based on objective criteria (regulations, standards)
- ✅ Includes reference materials and templates
- ✅ Follows systematic workflows

---

## Repository Structure

```
ClaudeSkillCollection/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
├── MARKETPLACE.md                  # Marketplace documentation
├── CHANGELOG.md                    # Version history
│
├── .claude-plugin/                 # Marketplace configuration
│   └── marketplace.json            # Plugin marketplace manifest
│
├── gdpr-auditor/                   # GDPR Compliance Auditor Plugin
│   ├── README.md                   # Plugin documentation
│   ├── SKILL.md                    # Claude agent prompt
│   ├── plugin.json                 # Plugin manifest
│   ├── scripts/                    # Automated scanning tools (5 scripts)
│   ├── references/                 # GDPR reference materials (8 docs)
│   └── examples/                   # Usage examples and demos
│
├── private/                        # Private development workspace (submodule)
│   ├── wip-plugins/                # Work-in-progress plugins
│   │   └── cybersecurity-policy-generator/  # Policy generator (in development)
│   │       ├── SKILL.md            # Plugin workflow and instructions
│   │       ├── README.md           # Plugin documentation
│   │       ├── plugin.json         # Plugin manifest
│   │       ├── scripts/            # Policy generation scripts (4 tools)
│   │       ├── references/         # 320KB policy templates and frameworks
│   │       ├── output/             # Generated policies (production-tested)
│   │       └── examples/           # Customization examples
│   ├── drafts/                     # Draft documentation
│   ├── research/                   # Research materials
│   ├── test-data/                  # Test datasets
│   └── notes/                      # Development notes
│
│   ⚠️  This is a git submodule pointing to a PRIVATE repository
│       Only accessible to repository owner and collaborators
│       Public visitors see the reference but cannot access contents
│
├── docs/                           # Global documentation
│   └── installation.md             # Detailed installation guide
│
└── .github/                        # GitHub-specific files
    └── ISSUE_TEMPLATE/
```

---

## 🔒 Private Development Workspace

This repository includes a **private submodule** for work-in-progress plugins and development materials.

### What's in `private/`?

The `private/` directory is a **git submodule** pointing to a separate private repository:
- **Repository:** [ClaudeSkillCollection-Private](https://github.com/diegocconsolini/ClaudeSkillCollection-Private) (private)
- **Purpose:** Development workspace for unreleased plugins
- **Access:** Repository owner and invited collaborators only

**Contents:**
- `drafts/` - Draft documentation and ideas
- `research/` - Research materials and references
- `wip-plugins/` - Work-in-progress plugins (not ready for release)
- `test-data/` - Test datasets (sanitized)
- `notes/` - Development notes and planning

### How to Access (For Collaborators)

If you have access to the private repository:

```bash
# Clone with submodule
git clone --recurse-submodules https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Or if already cloned
git submodule init
git submodule update
```

### For Public Users

Public visitors will see the `private/` submodule reference in the repository, but **cannot access** the contents. This is intentional - it allows development work to happen privately before plugins are ready for public release.

---

## How Skills Work

Claude Code skills are specialized prompts with supporting materials that give Claude domain expertise. When you invoke a skill:

1. **Automatic Loading:** Mention the skill's domain (e.g., "GDPR compliance") or explicitly call it
2. **Context Injection:** Claude loads the skill's knowledge and workflow instructions
3. **Tool Access:** Claude can use skill-specific scripts and reference materials
4. **Guided Workflow:** Claude follows the skill's methodology for thorough analysis

### Example: GDPR Auditor Workflow

```
User: "Audit my app for GDPR compliance"
  ↓
Claude loads gdpr-auditor skill
  ↓
Skill guides Claude through:
  1. Identify scope and data types
  2. Run automated scanners
  3. Consult GDPR reference materials
  4. Analyze code and configurations
  5. Generate compliance report
  ↓
Professional audit report with specific findings
```

---

## Use Cases by Skill

### GDPR Auditor

**Best For:**
- Pre-launch compliance checks
- Regular compliance audits
- Privacy policy development
- Data protection impact assessments (DPIA)
- Security reviews
- Third-party vendor assessments

**Who Should Use:**
- Web application developers
- DevOps teams
- Privacy officers
- Security consultants
- Startup founders
- Legal/compliance teams

---

## Planned Skills (Roadmap)

### Data Privacy & Security
- [🔄] **Cybersecurity Policy Generator** - In development (private workspace)
- [ ] **CCPA Compliance Auditor** - California Consumer Privacy Act
- [ ] **Security Vulnerability Scanner** - OWASP Top 10 analysis
- [ ] **API Security Auditor** - REST/GraphQL security review

### Code Quality & Architecture
- [ ] **Accessibility Auditor** - WCAG 2.1 compliance
- [ ] **Performance Analyzer** - Bottleneck detection
- [ ] **Code Documentation Generator** - Auto-generate docs

### DevOps & Infrastructure
- [ ] **Infrastructure as Code Reviewer** - Terraform/CloudFormation
- [ ] **Container Security Scanner** - Docker/K8s security
- [ ] **CI/CD Pipeline Optimizer** - Build optimization

### Specialized Domains
- [ ] **Healthcare Compliance (HIPAA)** - US healthcare privacy
- [ ] **Financial Services (PCI DSS)** - Payment card security
- [ ] **AI Ethics Reviewer** - AI bias and fairness analysis

Vote for next skills or suggest new ones in [Issues](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)!

---

## Contributing

We welcome contributions! Whether you want to:
- Report a bug or issue
- Improve existing skills
- Create a new skill
- Fix documentation
- Share usage examples

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Skill Submission Checklist

To submit a new skill, ensure:
- [ ] Comprehensive SKILL.md with clear workflow
- [ ] Supporting scripts/tools are production-ready
- [ ] Reference materials from authoritative sources
- [ ] README with installation and usage instructions
- [ ] Working examples and test cases
- [ ] Follows repository standards
- [ ] No malicious code (defensive security only)

---

## Quality Assurance

### Testing
Each skill is tested on real-world projects before release. Test results are documented in the skill's `tests/` directory.

### Accuracy
All reference materials are verified against primary sources:
- **GDPR Auditor:** EUR-Lex official GDPR text, ICO guidance
- Future skills will cite their authoritative sources

### Maintenance
Skills are actively maintained with:
- Regular updates for new regulations/standards
- Bug fixes and improvements
- Community feedback integration
- Version tracking

---

## 📦 Plugin Marketplace

This repository is also a **Claude Code Plugin Marketplace**! You can add it to your Claude Code instance to browse and install plugins easily.

### Why Use the Marketplace?

**Easy Installation:**
- One-command plugin installation
- Automatic plugin discovery
- Centralized management

**Automatic Updates:**
- Keep plugins up-to-date with `/plugin update`
- Get notified of new releases
- Seamless version management

**Professional Quality:**
- Curated, production-ready plugins only
- Verified against authoritative sources
- Regular security audits
- Comprehensive documentation

### Marketplace Features

- **Specialization:** Community marketplace focused on security, privacy, and compliance
- **Quality Assurance:** All plugins production-tested
- **Ethical Focus:** Defensive security only (no offensive tools)
- **Professional Support:** Dedicated security expertise
- **Regular Updates:** Active maintenance and improvements

[→ Full Marketplace Documentation](./MARKETPLACE.md)

---

## Support & Community

### Getting Help
- **Documentation:** Check the skill's README and docs/
- **Issues:** Open a GitHub issue with details
- **Discussions:** Join GitHub Discussions for Q&A

### Reporting Issues
When reporting issues, include:
1. Claude Code version
2. Skill name and version
3. Steps to reproduce
4. Expected vs actual behavior
5. Relevant code snippets (if applicable)

---

## License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) file for details.

### What This Means
✅ Free to use commercially
✅ Modify and distribute
✅ Private use
❗ No warranty provided
❗ Include original license and copyright

---

## Disclaimer

### Scope of Skills
These skills are **tools to assist analysis** - they do not replace professional advice:
- **Legal Compliance:** Consult qualified legal counsel for compliance matters
- **Security Audits:** Professional security audits still recommended
- **Privacy Assessments:** Work with certified privacy professionals

### Accuracy
While we strive for accuracy:
- Skills provide guidance based on current information
- Regulations and standards change over time
- Always verify findings with authoritative sources
- No liability for errors or omissions

### Defensive Security Only
All tools are designed for **defensive security purposes**:
- Identifying vulnerabilities to fix them
- Improving compliance and security posture
- NOT for exploitation or malicious use

---

## Acknowledgments

### Inspiration
This collection was inspired by the Claude Code skills system and the need for high-quality, domain-specific analysis tools.

### Data Sources
- **GDPR:** EUR-Lex, ICO, EDPB guidelines
- **Security Standards:** OWASP, NIST, CIS Benchmarks
- **Best Practices:** Industry-standard frameworks and methodologies

### Community
Thanks to all contributors and users who help improve these skills!

---

## Changelog

### Version 1.1.0 (2025-10-19)
- Added Cybersecurity Policy Generator to private development workspace
  - 51 professional policy templates (SANS + CIS Controls)
  - 320KB reference data with compliance framework mappings
  - Interactive AskUserQuestion workflow
  - Multi-format generation (Markdown, Word, HTML, PDF)
  - Production-tested with Guatemaltek (8 foundational policies)
  - Improved SKILL.md with proper skill delegation architecture
- Updated repository structure documentation
- Enhanced marketplace capabilities

### Version 1.0.0 (2025-10-18)
- Initial release
- GDPR Auditor skill v1.0.0
  - 8 comprehensive reference documents
  - 5 automated scanning tools
  - Complete audit workflow
  - Tested on real-world applications

---

## Contact

- **Issues:** [GitHub Issues](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)
- **Discussions:** [GitHub Discussions](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)
- **Email:** your.email@example.com

---

**Claude Skills Collection** - Empowering Claude Code with specialized domain expertise.
