# Claude Desktop Skills Pack

**Version:** 1.0.0
**Release Date:** 2025-12-25
**Status:** 8 of 9 skills ready for distribution

## Overview

Professional skills pack for Claude Desktop featuring security, compliance, and productivity tools. All skills derived from the ClaudeSkillCollection plugin repository with proper Claude Desktop packaging.

## Available Skills

### Security & Compliance (5 skills)

**1. GDPR Auditor** (57 KB)
- Analyze codebases, databases, and systems for GDPR compliance
- Identify data protection issues and compliance gaps
- Generate actionable audit reports

**2. Cybersecurity Policy Generator** (168 KB)
- Generate enterprise security policies from 51 professional templates
- Support for ISO 27001, SOC 2, NIST, CIS Controls
- Multiple output formats: Markdown, Word, HTML, PDF

**3. Incident Response Playbook Creator** (85 KB)
- Create IR playbooks based on NIST SP 800-61r3 and CISA guidance
- 11 incident scenarios (ransomware, data breach, phishing, supply chain, etc.)
- GDPR and HIPAA compliance considerations included

**4. Security Report Builder** (35 KB)
- Transform security scan results into professional reports
- Intelligent false positive filtering (85-90% → <20%)
- MITRE ATT&CK and OWASP Top 10 integration

**5. Plugin Security Checker** (pending)
- ⏸️ **Size Issue:** 51MB uncompressed (exceeds 30MB limit)
- 91 specialized pattern agents for vulnerability detection
- MITRE ATT&CK/ATLAS framework integration
- **Status:** Waiting for size optimization (STIX data: 50MB)

### Productivity & Optimization (3 skills)

**6. PDF Smart Extractor** (17 KB)
- Extract and analyze large PDFs (1MB-50MB+) efficiently
- Semantic chunking with 12-100x token reduction
- Persistent caching for instant reuse

**7. Excel Smart Extractor** (16 KB)
- Analyze Excel workbooks (1MB-50MB+) with minimal tokens
- Preserve formulas, formatting, and table structures
- Sheet-based semantic chunking

**8. Word Smart Extractor** (14 KB)
- Process Word documents (1MB-50MB+) efficiently
- Preserve formatting, tables, and document structure
- Semantic chunking by headings

**9. Chrome DevTools Optimizer** (30 KB)
- Reduce token consumption by 70-80% with Chrome DevTools MCP
- Smart snapshot strategies and Gemini Flash integration
- Decision trees and automated optimization workflows

## Installation

### Individual Skill Installation

1. Download skill ZIP from `packages/` directory
2. Open Claude Desktop
3. Go to **Skills** menu
4. Click **Import Skill**
5. Select the ZIP file
6. Confirm import

### Batch Installation

Import all 8 ready skills at once:
1. Open Claude Desktop
2. Go to **Skills** menu
3. Click **Import Skill**
4. Select all ZIP files from `packages/` directory
5. Confirm batch import

## Package Format

All skills follow Claude Desktop format requirements:

```
skill-name.zip
└── skill-name/
    ├── Skill.md          # Entry file (REQUIRED)
    ├── scripts/          # Optional scripts
    ├── references/       # Optional reference data
    └── requirements.txt  # Python dependencies (if applicable)
```

**Critical Requirements:**
- Entry file MUST be named **exactly** `Skill.md` (capital S, lowercase kill)
- MUST start with YAML frontmatter (`---`)
- ZIP must have skill folder as root (not nested)
- Uncompressed size limit: 30MB

## Dependencies

### Python Skills
Most skills require Python 3.8+. Install dependencies:

```bash
pip install -r skill-name/requirements.txt
```

**Specific dependencies:**
- **pdf-smart-extractor:** pymupdf
- **xlsx-smart-extractor:** openpyxl, pandas
- **docx-smart-extractor:** python-docx
- **plugin-security-checker:** stix2, taxii2-client, mitreattack-python

### Node.js Skills
- **chrome-devtools-optimizer:** Node.js 14+ (uses npx for dependencies)

## Documentation

- **CHANGELOG.md** - Version history and release notes
- **MIGRATION_GUIDE.md** - Claude Code plugins vs Desktop skills comparison
- Each skill includes comprehensive documentation in its `Skill.md` file

## Known Issues

**1. Plugin Security Checker - Size Limit**
- **Issue:** 51MB uncompressed (30MB limit)
- **Cause:** 50MB STIX threat intelligence data
- **Status:** Pending decision on data removal or separate download
- **Original:** Preserved in `/plugin-security-checker/` directory

## Comparison: Claude Code vs Desktop

| Feature | Claude Code Plugin | Claude Desktop Skill |
|---------|-------------------|---------------------|
| Entry file | `agents/*.md` | `Skill.md` |
| Installation | `/plugin install` | Import ZIP via GUI |
| Packaging | Git repository | ZIP file |
| Frontmatter | `capabilities`, `tools`, `model` | `license`, `compatibility`, `metadata` |
| Size limit | No limit | 30MB uncompressed |

**Both versions available** - Choose based on your workflow preference.

## Support

- **Issues:** Original plugin repository
- **Documentation:** See individual Skill.md files
- **Migration Help:** See MIGRATION_GUIDE.md

## Version History

- **1.0.0** (2025-12-25) - Initial release with 8 distributable skills

## License

All skills: MIT License

## Credits

Created by Diego Consolini
Based on NIST frameworks, MITRE ATT&CK/ATLAS, GDPR, and HIPAA regulations

---

**Total Package Size:** 425 KB (8 distributable ZIP files)
**Ready for Claude Desktop:** 8 of 9 skills ✅
