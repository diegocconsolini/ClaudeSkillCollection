# GDPR Auditor Skill

A comprehensive Claude Code skill for auditing applications, codebases, and systems for GDPR (General Data Protection Regulation) compliance.

## Version

**1.0.0** - Production Ready

## Overview

The GDPR Auditor skill equips Claude Code with specialized knowledge to conduct professional-grade GDPR compliance audits. It combines:
- 8 comprehensive reference documents covering all key GDPR articles
- 5 automated Python scanning tools
- Structured audit workflow
- Professional report generation

### What It Does

This skill enables Claude to:
1. **Identify Personal Data** - Scan code for data collection, storage, and processing
2. **Assess Compliance** - Evaluate against GDPR principles and articles
3. **Review Security** - Audit encryption, access controls, and data protection measures
4. **Verify Rights** - Check implementation of data subject rights (access, erasure, portability, etc.)
5. **Generate Reports** - Create detailed audit reports with specific code references and recommendations

### What It Doesn't Do

This skill is a **tool to assist analysis** - it does NOT:
- Replace qualified legal counsel
- Provide legal advice
- Guarantee compliance
- Certify GDPR compliance
- Access live databases or running systems
- Monitor runtime behavior or execute code
- Test third-party APIs or external services
- Exploit vulnerabilities (defensive security only)

---

## Features

### Automated Scanning Tools

Five production-ready Python scripts for automated analysis:

1. **scan_data_collection.py** - Identifies data collection patterns
   - Form fields and inputs
   - API endpoints
   - Cookies and local storage
   - Analytics tracking
   - Personal data fields

2. **analyze_database_schema.py** - Analyzes database structures
   - Personal data in schemas
   - Sensitive field detection
   - Encryption verification
   - Retention policies

3. **check_dsr_implementation.py** - Verifies data subject rights
   - Right of access endpoints
   - Data export functionality
   - Deletion mechanisms
   - Rectification capabilities

4. **security_audit.py** - Security compliance checks
   - Authentication/authorization
   - Encryption (transit and rest)
   - Access controls
   - Audit logging

5. **generate_audit_report.py** - Creates comprehensive reports
   - Finding aggregation
   - Risk prioritization
   - Actionable recommendations
   - Professional formatting

### Reference Materials

Eight comprehensive reference documents verified against official GDPR sources:

1. **gdpr_articles.md** - Key GDPR articles (5, 6, 7, 9, 12-22, 32-35)
2. **personal_data_categories.md** - Complete taxonomy of personal data
3. **dsr_requirements.md** - Data subject rights implementation guide
4. **security_measures.md** - Technical and organizational measures
5. **legal_bases.md** - Article 6 legal bases for processing
6. **breach_procedures.md** - Articles 33-34 breach notification
7. **dpia_guidelines.md** - Article 35 DPIA requirements
8. **international_transfers.md** - Chapter V transfer mechanisms

All references verified against:
- EUR-Lex official GDPR text
- ICO (UK) guidance documents
- EDPB guidelines

---

## Installation

### Prerequisites

- **Claude Code** (latest version)
- **Python 3.8+** (for scanning tools)
- **pip** (Python package manager)

### Step 1: Install the Skill

```bash
# Navigate to Claude skills directory
cd ~/.claude/skills/

# Create gdpr-auditor directory
mkdir -p gdpr-auditor

# Copy skill files (from this repository)
cp -r /path/to/claude-skills-collection/gdpr-auditor/* ./gdpr-auditor/

# Verify structure
ls -la gdpr-auditor/
# Should show: SKILL.md, scripts/, references/
```

### Step 2: Install Python Dependencies

```bash
# Navigate to skill directory
cd ~/.claude/skills/gdpr-auditor/

# Install required packages (none currently, but for future scripts)
# pip install -r requirements.txt
```

### Step 3: Set Permissions

```bash
# Make scripts executable
chmod +x scripts/*.py
```

### Step 4: Restart Claude Code

Restart Claude Code to load the new skill.

### Step 5: Verify Installation

In Claude Code, try:
```
"Can you help me audit my application for GDPR compliance?"
```

You should see:
```
The "gdpr-auditor" skill is running
```

---

## Usage

### Basic Audit

```
"Audit the application at /path/to/my/app for GDPR compliance"
```

Claude will:
1. Load the gdpr-auditor skill
2. Analyze codebase structure
3. Run automated scans (with your permission)
4. Reference GDPR articles as needed
5. Generate a comprehensive compliance report

### Targeted Analysis

```
# Focus on specific areas:
"Check if my app implements all data subject rights"
"Analyze database schema for personal data handling"
"Review security measures for GDPR compliance"
"Evaluate privacy policy against GDPR requirements"
```

### Report Generation

```
"Generate a GDPR compliance audit report for this project"
```

Includes:
- Executive summary
- Critical issues with GDPR article references
- High/medium/low priority findings
- Specific code references (file:line)
- Actionable recommendations
- Compliance roadmap

---

## Example Output

### Audit Report Structure

```markdown
# GDPR Compliance Audit Report

## Executive Summary
- Overall Status: PARTIALLY COMPLIANT
- Critical Issues: 3
- High Priority: 5
- Risk Level: HIGH

## Critical Issues
1. Missing Privacy Policy
   - GDPR Articles: 12, 13, 14
   - Code References: None found
   - Recommendation: Create comprehensive privacy policy...

2. No Consent Mechanism
   - GDPR Articles: 6, 7
   - Code References: api/routes.py:45-67
   - Recommendation: Implement consent before processing...

## High-Priority Recommendations
1. Implement Data Subject Rights
   - Article 15-22 requirements
   - Missing: Data portability, rectification
   - Code changes required: Add export endpoint...

## Compliance Roadmap
Phase 1 (Immediate): Privacy policy, consent, auth
Phase 2 (1-3 months): Encryption, logging, DPIAs
Phase 3 (3-6 months): Data minimization, automation
```

---

## Workflow

The skill follows a structured audit methodology:

### Phase 1: Discovery
1. Identify application type and scope
2. Determine data subjects (users, customers, employees)
3. Map data flows and processing activities
4. Catalog personal data categories

### Phase 2: Analysis
1. **Data Collection** - Scan for collection points
2. **Data Storage** - Analyze databases and file systems
3. **Data Processing** - Review processing logic
4. **Data Security** - Audit security measures
5. **Data Subject Rights** - Verify rights implementation
6. **Policies & Documentation** - Review legal requirements

### Phase 3: Reporting
1. Aggregate findings by severity
2. Map to GDPR articles
3. Prioritize by risk to data subjects
4. Generate actionable recommendations
5. Create compliance roadmap

---

## Automated Scans

### Running Scans Manually

You can run the scanning tools independently:

```bash
# Scan for data collection patterns
python scripts/scan_data_collection.py /path/to/codebase

# Analyze database schema
python scripts/analyze_database_schema.py /path/to/schema.sql

# Check data subject rights implementation
python scripts/check_dsr_implementation.py /path/to/api

# Security audit
python scripts/security_audit.py /path/to/app

# Generate report from findings
python scripts/generate_audit_report.py findings.json
```

### Scan Output

Scans produce JSON output with:
- File paths and line numbers
- Issue categories
- Matched patterns
- Context snippets

Example:
```json
{
  "file": "api/routes.py",
  "issues": [
    {
      "category": "personal_data_fields",
      "line": 45,
      "pattern": "\\b(email)\\b",
      "matched_text": "user.email",
      "context": "data = {'email': user.email, 'name': user.name}"
    }
  ]
}
```

---

## Reference Materials

### When Claude Uses References

Claude loads reference documents progressively as needed:

- **Initial Assessment** → gdpr_articles.md, personal_data_categories.md
- **Security Review** → security_measures.md
- **Rights Verification** → dsr_requirements.md
- **Legal Basis Analysis** → legal_bases.md
- **Breach Response** → breach_procedures.md
- **High-Risk Processing** → dpia_guidelines.md
- **Cross-Border Data** → international_transfers.md

### Customizing References

You can update reference materials:
1. Edit markdown files in `references/`
2. Add new sections or examples
3. Cite authoritative sources
4. Restart Claude Code to reload

---

## Tested Applications

This skill has been tested on:

### Real-World Projects
- ✅ **Web Applications** - FastAPI, Express.js, Django
- ✅ **Mobile Backends** - REST APIs with authentication
- ✅ **SaaS Platforms** - Multi-tenant applications
- ✅ **Document Processing** - PDF analyzers, file uploads
- ✅ **E-commerce** - Payment processing, user accounts

### Database Systems
- ✅ PostgreSQL schemas
- ✅ MySQL/MariaDB
- ✅ MongoDB collections
- ✅ Redis configurations
- ✅ File-based storage (JSON registries)

### Technology Stacks
- ✅ Python (FastAPI, Django, Flask)
- ✅ JavaScript/TypeScript (Node.js, React)
- ✅ Java (Spring Boot)
- ✅ PHP (Laravel)

---

## Limitations

### What This Skill Cannot Do

1. **Legal Advice** - This is a technical tool, not legal counsel
2. **Guarantee Compliance** - Only professional auditors can certify
3. **Runtime Analysis** - Works with static code only; cannot execute applications, simulate user flows, or observe runtime behavior
4. **Live Database Access** - Analyzes schema files only; does not connect to running databases
5. **Third-Party API Testing** - Cannot call or audit external services directly
6. **Cloud Infrastructure** - Limited visibility into cloud provider internals
7. **Network Monitoring** - No real-time traffic analysis capability

### Known Limitations

- **Code Coverage** - May miss obfuscated or dynamic code
- **False Positives** - Some findings may require manual verification
- **Language Support** - Scanning tools optimized for common languages
- **Context Understanding** - Cannot understand all business logic nuances

### When to Seek Professional Help

Consult qualified professionals for:
- Legal interpretation of GDPR requirements
- Official compliance certification
- Data Protection Impact Assessments (DPIAs)
- Supervisory authority communications
- Cross-border transfer mechanisms
- Binding Corporate Rules (BCRs)

---

## Troubleshooting

### Skill Doesn't Load

**Problem:** Claude doesn't recognize GDPR-related queries

**Solutions:**
1. Verify file structure: `~/.claude/skills/gdpr-auditor/SKILL.md` exists
2. Restart Claude Code completely
3. Check permissions: `chmod 644 SKILL.md`
4. Explicitly invoke: "Use the gdpr-auditor skill to..."

### Scripts Don't Run

**Problem:** Python scripts fail with permission or module errors

**Solutions:**
```bash
# Fix permissions
chmod +x scripts/*.py

# Verify Python version
python --version  # Should be 3.8+

# Run with explicit python
python3 scripts/scan_data_collection.py /path/to/code
```

### Incomplete Analysis

**Problem:** Audit seems superficial or misses obvious issues

**Solutions:**
1. Be specific about what to audit
2. Provide full codebase path
3. Mention specific concerns: "Check for missing encryption"
4. Request re-analysis with more detail

### Reference Material Not Used

**Problem:** Claude doesn't cite GDPR articles

**Solutions:**
1. Explicitly ask: "What GDPR articles apply?"
2. Request: "Reference specific GDPR requirements"
3. Verify reference files exist in `references/` directory

---

## Contributing

### Reporting Issues

Found a bug or inaccuracy? Please report:
1. Go to GitHub Issues
2. Describe the problem with examples
3. Include Claude Code version
4. Share relevant code snippet (anonymized)

### Improving References

To update GDPR references:
1. Verify information against official sources
2. Edit markdown files in `references/`
3. Cite authoritative sources (EUR-Lex, ICO, EDPB)
4. Submit pull request with changes

### Adding Scripts

To add new scanning tools:
1. Create script in `scripts/`
2. Follow existing script structure
3. Add comprehensive docstrings
4. Test on real codebases
5. Update this README

---

## Version History

### 1.0.0 (2025-10-18)
- Initial production release
- 8 comprehensive reference documents
- 5 automated scanning tools
- Complete audit workflow
- Tested on real-world applications

---

## License

MIT License - See repository LICENSE file

---

## Disclaimer

This skill is provided as a **technical tool to assist compliance analysis**. It does not constitute legal advice and cannot guarantee GDPR compliance. Always consult qualified legal counsel and certified data protection professionals for compliance matters.

The scanning tools are designed for **defensive security purposes only** - to identify issues for remediation, not for exploitation.

---

## References & Citations

### Primary Sources
- **GDPR Text:** [EUR-Lex - Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **ICO Guidance:** [UK Information Commissioner's Office](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- **EDPB Guidelines:** [European Data Protection Board](https://edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en)

### Verification
All reference materials in this skill have been verified against official sources as of October 2025. GDPR requirements are current as of publication date.

---

## Support

- **Documentation:** This README and repository wiki
- **Issues:** GitHub Issues for bugs/improvements
- **Discussions:** GitHub Discussions for Q&A
- **Updates:** Watch repository for new versions

---

**GDPR Auditor Skill** - Professional GDPR compliance auditing for Claude Code
