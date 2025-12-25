# Changelog

All notable changes to the Claude Desktop Skills Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-25

### Added - Initial Release

**Complete Claude Desktop skills pack with 9 professional skills**

#### Security & Compliance Skills

**gdpr-auditor** (v1.2.0)
- GDPR compliance auditing for codebases, databases, and configurations
- Analyzes data protection practices for EU regulation compliance
- Provides actionable compliance recommendations

**cybersecurity-policy-generator** (v1.2.0)
- Generates customized security policies based on industry best practices
- Supports multiple frameworks (NIST, ISO 27001, CIS)
- Creates ready-to-use policy documentation

**incident-response-playbook-creator** (v2.2.0)
- Creates comprehensive incident response playbooks
- Based on NIST SP 800-61r3 (April 2025) and CISA guidance
- Supports 11 incident scenarios (ransomware, data breach, phishing, etc.)
- Includes GDPR and HIPAA compliance considerations

**security-report-builder** (v1.0.1)
- Transforms plugin security scanner results into professional reports
- Multiple output formats (HTML, PDF, DOCX)
- Context-aware false positive filtering
- MITRE ATT&CK and OWASP Top 10 integration

**plugin-security-checker** (v3.2.0)
- Advanced security scanner with 91 specialized pattern agents
- Detects vulnerabilities, obfuscation, and security anti-patterns
- MITRE ATT&CK and ATLAS framework integration
- Consensus voting for accurate detection

#### Productivity & Optimization Skills

**pdf-smart-extractor** (v2.2.0)
- Extracts and analyzes large PDFs (1MB-50MB+) with minimal token usage
- Local extraction with semantic chunking
- 12-100x token reduction through intelligent querying
- Persistent caching for instant reuse

**xlsx-smart-extractor** (v2.2.0)
- Analyzes Excel workbooks (1MB-50MB+) efficiently
- Preserves formulas, formatting, and table structures
- Sheet-based semantic chunking
- 20-100x token reduction vs full workbook

**docx-smart-extractor** (v2.2.0)
- Processes Word documents (1MB-50MB+) with token optimization
- Preserves formatting, tables, and document structure
- Semantic chunking by headings
- 10-50x token reduction through targeted queries

**chrome-devtools-optimizer** (v1.0.1)
- Reduces token consumption by 70-80% with Chrome DevTools MCP
- Smart snapshot strategies and Gemini Flash vision processing
- Decision trees and pattern guides
- Automated optimization workflows

### Technical Details

#### File Format
- Entry file: `Skill.md` (capital S, lowercase kill)
- YAML frontmatter with `name`, `description`, `license`, `compatibility`, `metadata`
- Packaged as ZIP files with skill folder as root

#### Compatibility
- All skills compatible with Claude Desktop
- Python skills require Python 3.8+
- Node.js skills require Node.js 14+
- Platform support: macOS, Linux, Windows (WSL2)

#### Dependencies

**Python Skills:**
- pdf-smart-extractor: pymupdf
- xlsx-smart-extractor: openpyxl, pandas
- docx-smart-extractor: python-docx
- plugin-security-checker: stix2, taxii2-client, mitreattack-python
- gdpr-auditor, cybersecurity-policy-generator, incident-response-playbook-creator, security-report-builder: No external dependencies (stdlib only)

**Node.js Skills:**
- chrome-devtools-optimizer: No package.json (uses npx for dependencies)

#### Directory Structure
```
skill-name.zip
└── skill-name/
    ├── Skill.md (required)
    ├── scripts/ (optional)
    ├── references/ (optional)
    └── requirements.txt (Python skills only)
```

### Migration from Claude Code Plugins

All skills are derived from Claude Code plugins in the ClaudeSkillCollection repository:
- Original plugins remain unchanged
- Desktop skills are additional versions, not replacements
- Frontmatter transformed to Claude Desktop format
- All scripts and references copied

See MIGRATION_GUIDE.md for detailed comparison.

### Documentation

- README.md - Skills catalog and installation guide
- CHANGELOG.md - Version history (this file)
- MIGRATION_GUIDE.md - Claude Code vs Desktop comparison
- Each skill includes comprehensive Skill.md documentation

### Installation

**Install individual skills:**
1. Download skill ZIP file
2. Import into Claude Desktop via Skills menu

**Install all skills:**
1. Download all 9 ZIP files
2. Batch import into Claude Desktop

See README.md for detailed installation instructions.

### Known Issues

None reported for initial release.

### Breaking Changes

None (initial release).

---

## Version History

- **1.0.0** (2025-12-25) - Initial release with 9 skills

---

## Future Roadmap

Potential enhancements for future versions:

### Planned Features
- Additional skill categories (testing, deployment, monitoring)
- Multi-language support for policy templates
- Enhanced visual reporting for security tools
- Integration with CI/CD pipelines
- Cloud storage integration for cached extractions

### Under Consideration
- VSCode extension integration
- Slack/Discord notification support
- Automated skill updates
- Custom skill creation templates
- Community contribution guidelines

---

## Support

For issues, questions, or feature requests:
- Review individual skill documentation
- Check MIGRATION_GUIDE.md for Claude Code comparison
- Report issues to the ClaudeSkillCollection repository

## License

All skills are released under the MIT License.

## Credits

Created by Diego Consolini as part of the ClaudeSkillCollection project.

Based on:
- NIST security frameworks (SP 800-61r3, SP 800-161r1, SP 800-190, etc.)
- MITRE ATT&CK and ATLAS frameworks
- GDPR and HIPAA regulations
- Claude Code plugin ecosystem
- Community feedback and best practices
