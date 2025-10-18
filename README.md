# Claude Skills Collection

A curated collection of professional, production-ready skills for Claude Code that extend its capabilities for specialized workflows and domain expertise.

## Overview

This repository provides high-quality, well-documented skills that you can install in Claude Code to unlock specialized capabilities. Each skill is designed following best practices with comprehensive reference materials, automated tools, and clear workflows.

## Available Skills

### 1. GDPR Auditor
**Status:** Production Ready
**Version:** 1.0.0
**Category:** Data Privacy & Compliance

Comprehensive GDPR compliance auditing skill that analyzes codebases, databases, and systems for EU data protection regulation compliance.

**Key Features:**
- Scans code for personal data collection patterns
- Analyzes database schemas for sensitive data
- Verifies data subject rights implementation
- Audits security measures and encryption
- Generates detailed compliance reports with specific code references
- 8 comprehensive reference documents covering GDPR articles
- 5 automated scanning tools

[→ Read GDPR Auditor Documentation](./gdpr-auditor/README.md)

---

## Quick Start

### Prerequisites

- **Claude Code** (latest version)
- **Python 3.8+** (for automated scanning tools)
- Basic understanding of Claude Code skills system

### Installation

#### Option 1: Install Individual Skill

```bash
# Navigate to your Claude skills directory
cd ~/.claude/skills/

# Clone specific skill
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git temp
cp -r temp/gdpr-auditor ./
rm -rf temp

# Restart Claude Code
```

#### Option 2: Install All Skills

```bash
# Clone entire repository
cd ~/.claude/skills/
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Symlink desired skills
ln -s claude-skills-collection/gdpr-auditor ./gdpr-auditor

# Restart Claude Code
```

### Verification

After installation and restart:

```
# In Claude Code, test that the skill loads:
"Can you help me audit my application for GDPR compliance?"

# You should see: "The gdpr-auditor skill is running"
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
- ✅ Follows Claude Skills best practices

### Accuracy
- ✅ Information verified against primary sources
- ✅ No hallucinated facts or fake examples
- ✅ Regular updates to reflect current standards
- ✅ Clear version tracking

---

## Repository Structure

```
claude-skills-collection/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
│
├── gdpr-auditor/               # GDPR Compliance Auditor Skill
│   ├── README.md               # Skill-specific documentation
│   ├── SKILL.md                # Claude skill prompt
│   ├── scripts/                # Automated scanning tools (5 scripts)
│   ├── references/             # GDPR reference materials (8 docs)
│   ├── examples/               # Usage examples and demos
│   └── tests/                  # Test files and validation
│
├── docs/                       # Global documentation
│   ├── installation.md         # Detailed installation guide
│   ├── skill-development.md    # Creating your own skills
│   └── troubleshooting.md      # Common issues and solutions
│
└── .github/                    # GitHub-specific files
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

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
