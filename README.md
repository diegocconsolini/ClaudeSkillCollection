# Security & Compliance Marketplace

**Professional Security, Compliance, and Productivity Plugins for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection/releases)
[![Plugins](https://img.shields.io/badge/plugins-6-green.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection)

A curated collection of production-ready security, compliance, and productivity plugins for Claude Code. Built on authoritative sources and rigorously tested with real-world data.

## 🚀 Quick Start

```bash
# Add marketplace to Claude Code
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Install plugins
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install pdf-smart-extractor@security-compliance-marketplace
```

---

## 📂 Plugin Categories

### 🔒 Security & Compliance (Authoritative Sources)

Professional security and compliance plugins built from official regulatory texts, industry frameworks, and authoritative guidance. No hallucinated content - every template, requirement, and guideline is traceable to its source.

**What makes these authoritative:**
- **GDPR Auditor:** EUR-Lex official EU regulation texts, ICO guidance, EDPB guidelines
- **Cybersecurity Policy Generator:** SANS Institute templates, CIS Controls v8 official framework
- **Incident Response Playbook Creator:** NIST SP 800-61r3 (April 2025), CISA federal playbooks, GDPR Article 33/34, HIPAA Breach Notification Rule

### 📊 Productivity Tools (Smart Extraction with Persistent Caching)

High-performance document extraction plugins that solve the "PDF/Excel/Word too large for LLM" problem through local extraction, semantic chunking, and intelligent caching.

**How caching works:**
1. **First extraction:** Processes document locally (PyMuPDF for PDF, openpyxl for Excel, python-docx for Word)
2. **Persistent cache:** Stores extracted content in `~/.claude-{pdf|xlsx|docx}-cache/` with SHA-256 hash keys
3. **Subsequent queries:** Instant - uses cached extraction, no re-processing needed
4. **Token optimization:** 10-100x reduction by loading only relevant chunks, not entire documents

All three extractors share the same architecture: Local extraction → Semantic chunking → Persistent caching → Efficient querying

---

## 🔒 Security & Compliance Plugins

### 1. GDPR Auditor
**Production Ready** • **v1.0.0** • **Data Privacy & Compliance**

Comprehensive GDPR compliance auditing plugin that analyzes static code files, database schemas, and configurations for EU data protection regulation compliance.

**Authoritative Sources:**
- EUR-Lex: Official GDPR regulation text (EU 2016/679)
- ICO (UK Information Commissioner's Office): Implementation guidance
- EDPB (European Data Protection Board): Official interpretations and guidelines
- 8 reference documents totaling 2.1MB of official compliance materials

**Key Features:**
- Scans source code for personal data collection patterns
- Analyzes database schema files (SQL DDL, migrations) for sensitive data
- Verifies data subject rights implementation (access, rectification, erasure)
- Audits security measures and encryption configurations
- Generates detailed compliance audit reports with specific article references
- 5 automated scanning tools (static file analysis only - no live system access)

**Use Cases:**
- Pre-launch GDPR compliance checks for EU market entry
- Regular compliance audits and monitoring
- Privacy policy development and validation
- Data protection impact assessments (DPIA)
- Third-party vendor security assessments
- Audit preparation (ISO 27001, SOC 2, GDPR)

**Who Should Use:**
- Web application developers handling EU user data
- DevOps and infrastructure teams
- Privacy officers and DPOs (Data Protection Officers)
- Security consultants and auditors
- Startup founders preparing for EU markets
- Legal and compliance teams

[→ View GDPR Auditor Documentation](./gdpr-auditor/README.md)

---

### 2. Cybersecurity Policy Generator
**Production Ready** • **v1.0.0** • **Security Governance & Compliance**

Professional cybersecurity policy document generator using 51 industry-standard templates from SANS Institute and CIS Controls. Creates complete, framework-compliant policy documents customized for your organization.

**Authoritative Sources:**
- SANS Institute: 36 policy templates from the industry-leading security training organization
- CIS Controls v8: 15 additional templates from the Center for Internet Security
- ISO 27001: Compliance mappings to information security management standard
- NIST CSF: Cybersecurity Framework function and category mappings
- SOC 2: Trust Service Criteria alignment (Security, Availability, Confidentiality)
- 320KB of reference data with verified compliance framework mappings

**Key Features:**
- 51 professional policy templates (36 SANS + 15 CIS Controls)
- Interactive AskUserQuestion workflow with Claude Code's native UI
- Multi-framework compliance mappings (ISO 27001, SOC 2, NIST CSF, CIS Controls v8, GDPR)
- Multi-format generation (Markdown, Word, HTML, PDF)
- 15 security policy categories covering all InfoSec domains
- Organization customization with branding options
- 4 automated policy generation scripts

**Policy Categories:**
- **Governance** (13 policies) - Information Security, Acceptable Use, Password Management
- **Identity & Access** (8 policies) - Access Control, Authentication, Remote Access
- **Application Security** (7 policies) - Secure Development, API Security, Code Review
- **Compute & Network** (10 policies) - Cloud Security, Network Security, Virtualization
- **Data Protection** (2 policies) - Data Classification, Data Recovery & Backup
- **Operations, Resilience, Risk** (11 policies) - Incident Response, Change Management, Risk Assessment

**Real-World Testing:**
- Production deployment: Guatemaltek (October 2025)
- Generated: 8 foundational security policies
- Formats: Markdown + Word (.docx)
- Result: Production-ready policies deployed to internal security program

**Use Cases:**
- Starting a new security program (foundational policies)
- Preparing for compliance audits (ISO 27001, SOC 2, NIST CSF)
- Updating outdated or missing security policies
- Meeting cyber insurance or vendor security requirements
- Building comprehensive policy documentation for framework compliance

**Who Should Use:**
- CISOs and security leaders starting or improving security programs
- Compliance officers preparing for audits
- Startups establishing security governance
- IT managers needing standardized policies
- Consultants creating client security documentation
- Organizations pursuing ISO 27001, SOC 2, or NIST compliance

[→ View Cybersecurity Policy Generator Documentation](./private/wip-plugins/cybersecurity-policy-generator/README.md)

---

### 3. Incident Response Playbook Creator
**Production Ready** • **v1.0.0** • **Incident Response & Security Operations**

Professional incident response playbook generator based on NIST SP 800-61r3 (April 2025 revision). Creates comprehensive, customized IR documentation for multiple incident scenarios with built-in GDPR and HIPAA compliance guidance.

**Authoritative Sources:**
- NIST SP 800-61r3: Computer Security Incident Handling Guide (April 2025 revision)
- NIST Cybersecurity Framework 2.0: Function and category mappings (February 2024)
- CISA: Federal Incident Response Playbooks (August 2024)
- GDPR (EU 2016/679): Article 33 (72-hour breach notification) and Article 34 (data subject notification)
- HIPAA Breach Notification Rule: 45 CFR §§164.400-414 (60-day timeline)
- 110KB of authoritative reference data (no mock content)

**Key Features:**
- 3 incident scenarios: Ransomware Attack, Data Breach/Exfiltration, Phishing/BEC
- Based on NIST SP 800-61r3 (April 2025) with CSF 2.0 integration
- GDPR Article 33/34 breach notification requirements (72-hour timeline)
- HIPAA Breach Notification Rule guidance (60-day timeline)
- NIST Cybersecurity Framework 2.0 function mapping (DE, RS, RC)
- Interactive AskUserQuestion workflow for organization customization
- Professional Markdown playbook output ready for SOC/CSIRT teams

**Each Playbook Includes:**
- **Detection & Indicators** - Technical and behavioral IOCs mapped to NIST CSF 2.0
- **Response Procedures** - Step-by-step actions (Triage → Containment → Eradication)
- **Recovery Actions** - System restoration with validation checklists
- **Communication Templates** - Internal, external, and regulatory notifications
- **Compliance Guidance** - GDPR Article 33/34 and HIPAA Breach Notification Rule
- **Roles & Responsibilities** - Clear team structure and escalation criteria
- **Post-Incident Activities** - Lessons learned and documentation requirements

**Use Cases:**
- Building your first incident response program
- Updating IR playbooks to NIST SP 800-61r3 (April 2025)
- Preparing for compliance audits (GDPR, HIPAA)
- Creating scenario-specific response procedures
- Training security operations teams
- Meeting cyber insurance requirements
- Tabletop exercise preparation

**Who Should Use:**
- Security Operations Centers (SOC) and CSIRT teams
- Incident Response managers and coordinators
- CISOs establishing IR programs
- Compliance officers (GDPR, HIPAA)
- MSPs and MSSPs serving clients
- IT managers preparing for security incidents
- Organizations in regulated industries (healthcare, finance)

[→ View Incident Response Playbook Creator Documentation](./incident-response-playbook-creator/README.md)

---

## 📊 Productivity Tools

### 4. PDF Smart Extractor
**Production Ready** • **v1.1.0** • **NEW: Password Protection Support**

Extract and analyze large PDF documents (3MB-35MB+) with 100% content preservation and 12-115x token reduction. Perfect for technical documentation, compliance frameworks, and research papers that exceed LLM context windows.

**October 2025 Updates:**
- ✅ **Password protection support** - Interactive prompts + CLI arguments for encrypted PDFs
- ✅ **Edge case documentation** - Shell escaping issues with special characters documented
- ✅ **Real-world testing** - Large encrypted PDFs (140 pages, 8.39MB) successfully extracted
- ✅ **Security considerations** - Passwords never cached, getpass.getpass() for hidden input

**Caching Architecture:**
- **Cache location:** `~/.claude-pdf-cache/{pdf_name}_{hash}/`
- **Cache key:** SHA-256 hash (first 16 chars) ensures unique identification
- **Cache contents:** full_text.txt, pages.json, metadata.json, toc.json, manifest.json
- **Cache reuse:** Instant - no re-extraction needed (unless --force flag used)
- **Password handling:** Passwords NEVER stored in cache (security by design)

**Key Features:**
- **100% Local Extraction** - Zero LLM involvement, complete privacy
- **Semantic Chunking** - Intelligent splitting at chapters, sections, paragraphs
- **12-115x Token Reduction** - Load only relevant chunks, not entire documents
- **Persistent Caching** - Extract once, query forever
- **Password Support** - Interactive prompts (recommended) or CLI arguments for encrypted PDFs
- **Content Preservation** - 99.76-99.81% preservation rate (mathematical verification)
- **Fast Processing** - <2 minutes first extraction, <1 second subsequent queries
- **PyMuPDF-Powered** - Lightweight, reliable PDF parsing with encryption support

**Real Performance (Comprehensive Testing - October 2025):**
- NIST SP 800-161r1 (3.3MB, 325 pages): 215,907 tokens → 1,864 tokens = **115.8x reduction**, 99.81% preservation
- NIST SP 800-82r3 (8.2MB, 316 pages): 186,348 tokens → 3,085 tokens = **60.2x reduction**, 99.76% preservation
- Large Technical Book (35.46MB, 414 pages): 110,235 tokens, 400 chunks, **99.81% preservation**
- Encrypted Document (8.39MB, 140 pages): 260K characters, 65K tokens extracted via Python API

**Password Protection Workflow:**
```bash
# Interactive password prompt (recommended for complex passwords)
python scripts/extract_pdf.py encrypted_document.pdf
# Script prompts: Enter password: [hidden input]

# CLI password argument (for simple passwords or automation)
python scripts/extract_pdf.py encrypted_document.pdf --password YourPassword123

# Python API (for automation with complex passwords)
from extract_pdf import PDFExtractor
extractor = PDFExtractor()
result = extractor.extract_full_pdf('file.pdf', password='complex_P@ssw0rd!')
```

**Workflow:**
1. **Extract PDF** - One-time local extraction with PyMuPDF (handles encryption)
2. **Semantic Chunk** - Split at intelligent boundaries (chapters, sections)
3. **Query Efficiently** - Search and load only relevant chunks
4. **Reuse Forever** - Cached for instant subsequent queries

**Use Cases:**
- Analyzing NIST, ISO, AWS, Azure, GCP technical documentation
- Building knowledge bases from compliance frameworks
- Researching academic papers and technical reports
- Extracting specific sections from encrypted legal documents
- Processing large PDF datasets without token waste
- Expanding incident response playbooks (solved "PDF too large" problem)

**Who Should Use:**
- Security researchers analyzing NIST/ISO/CIS frameworks
- Compliance officers reviewing regulatory documentation
- Developers building RAG systems from PDF sources
- Data scientists processing research paper collections
- Legal teams working with encrypted contracts and agreements
- Anyone working with large technical PDFs (>1MB)

**Commands:**
```bash
# Extract PDF
python scripts/extract_pdf.py document.pdf

# Extract encrypted PDF (interactive)
python scripts/extract_pdf.py encrypted.pdf
# Prompts for password securely

# Extract encrypted PDF (CLI)
python scripts/extract_pdf.py encrypted.pdf --password YourPassword

# Force re-extraction (ignores cache)
python scripts/extract_pdf.py document.pdf --force

# Chunk content
python scripts/semantic_chunker.py {cache_key}

# Search chunks
python scripts/query_pdf.py search {cache_key} "your query"

# List cached PDFs
python scripts/query_pdf.py list
```

**Security Notes:**
- ⚠️ CLI `--password` stores password in command history - use interactive prompt for complex passwords
- ✅ Passwords never stored in cache - only decrypted content
- ✅ Cache contains extracted text only - same security model as Adobe, Ghostscript
- 📄 See [EDGE_CASES_PASSWORDS.md](./pdf-smart-extractor/EDGE_CASES_PASSWORDS.md) for shell escaping edge cases

[→ View PDF Smart Extractor Documentation](./pdf-smart-extractor/README.md)

---

### 5. Excel Smart Extractor
**Production Ready** • **v1.0.0** • **Large Workbook Analysis & Token Optimization**

Extract and analyze large Excel workbooks (1MB-50MB+) with 100% content preservation and 20-100x token reduction. Perfect for compliance matrices, financial models, security audit logs, and data tables that exceed LLM context windows.

**Caching Architecture:**
- **Cache location:** `~/.claude-xlsx-cache/{workbook_name}_{hash}/`
- **Cache key:** SHA-256 hash (first 16 chars) ensures unique identification
- **Cache contents:** full_workbook.json, sheet_{name}.json, named_ranges.json, metadata.json, manifest.json
- **Cache reuse:** Instant - no re-extraction needed (unless --force flag used)
- **Content preservation:** 100.04-100.59% (formulas, formatting, metadata all extracted)

**Key Features:**
- **100% Local Extraction** - Zero LLM involvement, complete privacy (openpyxl-powered)
- **100%+ Content Preservation** - Formulas, cell formatting, merged cells, hyperlinks, named ranges
- **20-100x Token Reduction** - Load only relevant sheets/columns, not entire workbooks
- **Persistent Caching** - Extract once, query forever
- **Semantic Chunking** - Intelligent splitting by sheets, columns, and row ranges
- **Fast Processing** - <5 seconds first extraction, <1 second subsequent queries
- **Read-Only Operations** - Never modifies source files

**Real Performance (Comprehensive Testing - October 2025):**
- **9 real-world files tested** (110KB - 1.5MB)
- **287,460 cells processed** across 85 sheets
- **15,409 formulas extracted** including array formulas
- **Content preservation:** 100.04% - 100.59% (includes formulas + formatting)
- **Token reduction:** 4x - 58x (average 27.6x)

**Example (Compliance Matrix):**
- CCM v4.0.12 (Cloud Controls Matrix): 1.41MB, 25 sheets
- **287K cells** → **15K tokens** (56.6x reduction)
- 100% formula preservation including HYPERLINK functions
- All control mappings, compliance domains, and audit criteria preserved

**Workflow:**
1. **Extract Workbook** - One-time local extraction with openpyxl
2. **Semantic Chunk** - Split by sheets, columns, and semantic row ranges
3. **Query Efficiently** - Search and load only relevant sheets/columns
4. **Reuse Forever** - Cached for instant subsequent queries

**Use Cases:**
- Analyzing compliance matrices (ISO 27001, SOC 2, CCM, CAIQ)
- Processing financial models and pricing sheets
- Extracting security audit logs and analysis reports
- Building knowledge bases from Excel data tables
- Querying large datasets with complex formulas

**Who Should Use:**
- Compliance officers analyzing security control matrices
- Financial analysts working with large pricing models
- Security teams processing audit logs in Excel format
- Data analysts querying large Excel datasets
- Anyone working with Excel files >1MB that exceed LLM context

**Commands:**
```bash
# Extract Excel workbook
python scripts/extract_xlsx.py workbook.xlsx

# Force re-extraction (ignores cache)
python scripts/extract_xlsx.py workbook.xlsx --force

# Chunk content
python scripts/chunk_sheets.py {cache_key}

# Search chunks
python scripts/query_xlsx.py search {cache_key} "your query"

# List cached workbooks
python scripts/query_xlsx.py list
```

**Supported Formats:**
- ✅ .xlsx (Excel 2007+ XML format)
- ✅ .xlsm (Macro-enabled workbooks - VBA macros disabled for security)
- ❌ .xls (Legacy Excel 97-2003 - convert to .xlsx first)

[→ View Excel Smart Extractor Documentation](./xlsx-smart-extractor/README.md)

---

### 6. Word Smart Extractor
**Production Ready** • **v1.0.0** • **Large Document Analysis & Token Optimization**

Extract and analyze large Word documents (1MB-50MB+) with complete content extraction and 10-50x token reduction. Perfect for policy documents, technical reports, contracts, and meeting notes with clear heading structure.

**Caching Architecture:**
- **Cache location:** `~/.claude-docx-cache/{document_name}_{hash}/`
- **Cache key:** SHA-256 hash (first 16 chars) ensures unique identification
- **Cache contents:** full_text.txt, paragraphs.json, tables.json, metadata.json, headings.json, manifest.json
- **Cache reuse:** Instant - no re-extraction needed (unless --force flag used)
- **Content extraction:** Text, tables, formatting, comments, tracked changes, headers/footers

**Key Features:**
- **100% Local Extraction** - Zero LLM involvement, complete privacy (python-docx powered)
- **Complete Content Extraction** - Text, tables, formatting, comments, tracked changes
- **10-50x Token Reduction** - Load only relevant sections, not entire documents
- **Persistent Caching** - Extract once, query forever
- **Semantic Chunking** - Intelligent splitting by heading hierarchy (H1, H2, H3)
- **Fast Processing** - 1-5 seconds first extraction, <1 second subsequent queries
- **Read-Only Operations** - Never modifies source files

**Real Performance (Tested October 2025):**
- Small documents (< 50 paragraphs): 5-10x reduction
- Medium documents (50-200 paragraphs): 10-30x reduction
- Large documents (200+ paragraphs): 30-50x reduction

**Example (Security Policy Document):**
- Acceptable Use Policy: 245 paragraphs, 12 tables
- Chunked into 13 semantic sections by heading structure
- Each chunk 500-2000 tokens (optimized for LLM context)
- Total token reduction: ~25x

**Workflow:**
1. **Extract Document** - One-time local extraction with python-docx
2. **Semantic Chunk** - Split by heading hierarchy (H1, H2, H3 boundaries)
3. **Query Efficiently** - Search and load only relevant sections
4. **Reuse Forever** - Cached for instant subsequent queries

**Use Cases:**
- Analyzing policy documents (security, privacy, compliance)
- Processing technical reports and specifications
- Contract review and analysis
- Meeting notes and project documentation
- Building knowledge bases from Word documents

**Who Should Use:**
- Security teams analyzing policy documents
- Compliance officers reviewing contract terms
- Technical writers working with large specifications
- Legal teams processing contracts and agreements
- Anyone working with Word documents >1MB

**Commands:**
```bash
# Extract Word document
python scripts/extract_docx.py document.docx

# Force re-extraction (ignores cache)
python scripts/extract_docx.py document.docx --force

# Chunk content by headings
python scripts/semantic_chunker.py {cache_key}

# Search chunks
python scripts/query_docx.py search {cache_key} "your query"

# Get specific heading section
python scripts/query_docx.py heading {cache_key} "Section Title"

# List cached documents
python scripts/query_docx.py list
```

**Supported Formats:**
- ✅ .docx (Word 2007+ XML format)
- ✅ .docm (Macro-enabled Word documents - VBA macros not extracted by design)
- ❌ .doc (Legacy Word 97-2003 - convert to .docx first)
- ❌ Password-protected files (cannot be opened)

[→ View Word Smart Extractor Documentation](./docx-smart-extractor/README.md)

---

## 📐 Caching Architecture

All three Smart Extractor plugins share the same efficient caching architecture:

```
First Extraction (One-Time Process):
┌─────────────────────────────────────────────────────────────┐
│ 1. User runs extract script with document path              │
│ 2. Plugin generates SHA-256 hash of document                │
│ 3. Creates cache directory: ~/.claude-{type}-cache/{name}_{hash}/ │
│ 4. Extracts content locally (PyMuPDF/openpyxl/python-docx) │
│ 5. Saves structured JSON + full text to cache               │
│ 6. Returns cache key for future queries                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
Subsequent Queries (Instant):
┌─────────────────────────────────────────────────────────────┐
│ 1. User queries with cache key                              │
│ 2. Plugin reads cached JSON (no re-extraction)              │
│ 3. Chunks content semantically (chapters/sheets/headings)   │
│ 4. Loads only relevant chunks (10-100x token reduction)     │
│ 5. Returns precise results in <1 second                     │
└─────────────────────────────────────────────────────────────┘
```

**Cache Benefits:**
- ✅ **Extract once, query forever** - No re-processing needed
- ✅ **Instant queries** - <1 second for cached documents
- ✅ **Token optimization** - 10-100x reduction by loading only relevant chunks
- ✅ **Complete privacy** - All processing happens locally, no external API calls
- ✅ **Persistent storage** - Cache survives Claude Code restarts
- ✅ **Automatic invalidation** - Document changes detected via SHA-256 hash

**Cache Locations:**
- PDF: `~/.claude-pdf-cache/{pdf_name}_{hash}/`
- Excel: `~/.claude-xlsx-cache/{workbook_name}_{hash}/`
- Word: `~/.claude-docx-cache/{document_name}_{hash}/`

**Cache Management:**
```bash
# Force re-extraction (bypass cache)
python scripts/extract_{pdf|xlsx|docx}.py document.{pdf|xlsx|docx} --force

# List all cached documents
python scripts/query_{pdf|xlsx|docx}.py list

# View cache statistics
python scripts/query_{pdf|xlsx|docx}.py stats {cache_key}

# Clear specific cache
rm -rf ~/.claude-{pdf|xlsx|docx}-cache/{cache_key}/

# Clear all caches
rm -rf ~/.claude-{pdf,xlsx,docx}-cache/
```

---

## 💡 Request New Plugins or Report Issues

We welcome community feedback, bug reports, and plugin ideas!

### 🆕 Request a New Plugin

Have an idea for a security, compliance, or productivity plugin?

**[→ Open a Feature Request](https://github.com/diegocconsolini/ClaudeSkillCollection/issues/new?labels=enhancement&template=feature_request.md)**

**Good plugin ideas:**
- Based on authoritative sources (regulations, frameworks, standards)
- Produces tangible deliverables (reports, documents, policies)
- Solves a specific security/compliance/productivity problem
- Can work with static files (no live system access required)

**Examples of plugins we'd love to see:**
- CCPA Compliance Auditor (California privacy law)
- HIPAA Privacy Auditor (Healthcare compliance)
- OWASP Top 10 Scanner (Web security)
- Privacy Policy Generator (GDPR/CCPA-compliant)
- Container Security Scanner (Docker/Kubernetes)

### 🐛 Report Bugs

Found a bug in an existing plugin?

**[→ Open a Bug Report](https://github.com/diegocconsolini/ClaudeSkillCollection/issues/new?labels=bug&template=bug_report.md)**

**Please include:**
1. Plugin name and version
2. Claude Code version
3. Steps to reproduce
4. Expected vs actual behavior
5. Relevant code snippets (sanitized - no sensitive data)

### 💬 Suggest Improvements

Have ideas for improving existing plugins?

**[→ Start a Discussion](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)**

**Examples:**
- Additional policy templates for Policy Generator
- New incident scenarios for IR Playbook Creator
- Performance improvements for Smart Extractors
- Additional compliance framework mappings

---

## 📦 Installation

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
/plugin install pdf-smart-extractor@security-compliance-marketplace

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
# Navigate to Claude plugins directory
cd ~/.claude/plugins/

# Clone repository
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# Symlink desired plugins
ln -s ClaudeSkillCollection/gdpr-auditor ./gdpr-auditor
ln -s ClaudeSkillCollection/pdf-smart-extractor ./pdf-smart-extractor

# Restart Claude Code
```

### Verification

Test that plugins are loaded:

**For GDPR Auditor:**
```
"Can you help me audit my application for GDPR compliance?"
```

**For PDF Smart Extractor:**
```
"Extract this large PDF: /path/to/technical_doc.pdf"
```

---

## 📖 How Plugins Work

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
  3. Consult GDPR reference materials (EUR-Lex, ICO, EDPB)
  4. Analyze code and configurations
  5. Generate compliance audit report with article references
  ↓
Professional audit report with specific findings
```

### Example: PDF Smart Extractor Workflow

```
User: "Extract this 10MB PDF: nist_sp_800-161.pdf"
  ↓
Claude loads pdf-smart-extractor plugin
  ↓
Plugin guides Claude through:
  1. Run extract_pdf.py script (local PyMuPDF extraction)
  2. Generate SHA-256 cache key
  3. Save to ~/.claude-pdf-cache/{name}_{hash}/
  4. Run semantic_chunker.py (chapter/section splitting)
  5. Return cache key for future queries
  ↓
User can now query: "Search for 'supply chain risk' in cached PDF"
  ↓
Plugin uses query_pdf.py to search chunks (instant, <1 second)
```

---

## 🗂️ Repository Structure

```
ClaudeSkillCollection/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
├── PLUGIN_STRUCTURE_GUIDE.md       # Official plugin development guide
├── CHANGELOG.md                    # Version history
│
├── .claude-plugin/                 # Marketplace configuration
│   └── marketplace.json            # Plugin catalog (6 plugins)
│
├── gdpr-auditor/                   # GDPR Compliance Auditor
│   ├── README.md
│   ├── plugin.json
│   ├── agents/gdpr-auditor.md      # Agent with YAML frontmatter
│   ├── scripts/                    # 5 automated scanning tools
│   ├── references/                 # 8 GDPR reference documents (EUR-Lex, ICO, EDPB)
│   └── examples/
│
├── incident-response-playbook-creator/  # IR Playbook Generator
│   ├── README.md
│   ├── plugin.json
│   ├── agents/incident-response-playbook-creator.md
│   ├── scripts/                    # Playbook generation scripts
│   ├── references/                 # 110KB NIST/CISA/GDPR/HIPAA data
│   └── output/
│
├── pdf-smart-extractor/            # PDF Smart Extractor (v1.1.0)
│   ├── README.md
│   ├── plugin.json
│   ├── agents/pdf-smart-extractor.md
│   ├── scripts/                    # extract, chunk, query scripts
│   ├── test-files/                 # Test PDFs
│   ├── TEST_RESULTS.md             # Comprehensive test report
│   ├── EDGE_CASES_PASSWORDS.md     # Password protection edge cases
│   └── PASSWORD_PROTECTION_TEST_LOG.md
│
├── xlsx-smart-extractor/           # Excel Smart Extractor (v1.0.0)
│   ├── README.md
│   ├── plugin.json
│   ├── agents/xlsx-smart-extractor.md
│   ├── scripts/                    # extract, chunk, query scripts
│   ├── test-files/                 # Test Excel files
│   └── TEST_RESULTS.md             # Comprehensive test report
│
├── docx-smart-extractor/           # Word Smart Extractor (v1.0.0)
│   ├── README.md
│   ├── plugin.json
│   ├── agents/docx-smart-extractor.md
│   ├── scripts/                    # extract, chunk, query scripts
│   └── examples/
│
├── private/wip-plugins/            # Private development workspace
│   └── cybersecurity-policy-generator/  # Policy Generator (in beta)
│       ├── README.md
│       ├── plugin.json
│       ├── agents/cybersecurity-policy-generator.md
│       ├── scripts/                # 4 policy generation scripts
│       ├── references/             # 320KB SANS/CIS templates
│       └── output/                 # Generated policies
│
└── .github/                        # GitHub templates
    └── ISSUE_TEMPLATE/
        ├── feature_request.md
        └── bug_report.md
```

---

## ⭐ Quality Standards

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
- ✅ Tested on real-world projects (October 2025: 35MB PDFs, 1.5MB Excel files, complex Word documents)
- ✅ Follows Claude Code plugin best practices (PLUGIN_STRUCTURE_GUIDE.md)
- ✅ Comprehensive test suites with edge case coverage
- ✅ YAML frontmatter in all agent files (required for marketplace loading)

### Accuracy & Compliance
- ✅ Information verified against primary sources
  - **GDPR Auditor:** EUR-Lex official GDPR text, ICO guidance, EDPB guidelines
  - **Policy Generator:** SANS policy templates, CIS Controls v8, ISO 27001, NIST CSF
  - **IR Playbook Creator:** NIST SP 800-61r3 (April 2025), CISA playbooks, GDPR/HIPAA official texts
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

## 🗺️ Roadmap

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

**[→ Vote for next plugins](https://github.com/diegocconsolini/ClaudeSkillCollection/issues) or suggest new ones!**

---

## 🤝 Contributing

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
- [ ] Agent file with YAML frontmatter (description + capabilities)
- [ ] Production-ready scripts with error handling
- [ ] Reference materials from authoritative sources
- [ ] Complete README with installation and usage guide
- [ ] Working examples and test cases
- [ ] Follows defensive security principles
- [ ] No malicious code or unethical use cases

---

## 📞 Support

**Getting Help:**
- **Documentation:** Check plugin README files and PLUGIN_STRUCTURE_GUIDE.md
- **Issues:** [Open a GitHub issue](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)
- **Discussions:** [Join GitHub Discussions](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)

**Reporting Issues:**

Please include:
1. Claude Code version
2. Plugin name and version
3. Steps to reproduce
4. Expected vs actual behavior
5. Relevant code snippets (sanitized - no sensitive data)

---

## 📜 License

MIT License - See [LICENSE](./LICENSE) for details

**What this means:**
- ✅ Free for commercial use
- ✅ Modify and distribute freely
- ✅ Private use allowed
- ⚠️ No warranty provided
- ⚠️ Must include original license and copyright notice

---

## ⚠️ Disclaimer

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

## 📋 Changelog

### Version 1.5.0 (2025-10-20)
**New Plugins:**
- Released **Excel Smart Extractor** v1.0.0
  - 100%+ content preservation (formulas, formatting, metadata)
  - 20-100x token reduction through semantic chunking
  - Tested with 9 real-world files (287K cells, 15K formulas)
  - Persistent caching in ~/.claude-xlsx-cache/
- Released **Word Smart Extractor** v1.0.0
  - Complete content extraction (text, tables, formatting, comments)
  - 10-50x token reduction through heading-based chunking
  - Tested with security policy documents
  - Persistent caching in ~/.claude-docx-cache/

**Updates:**
- **PDF Smart Extractor** upgraded to v1.1.0
  - Added password protection support (interactive + CLI)
  - Edge case documentation for shell escaping
  - Real-world testing with large encrypted PDFs (8.39MB, 140 pages)
- Updated marketplace to 6 total plugins
- Enhanced README with categorization, caching architecture, GitHub issues invitation

### Version 1.3.0 (2025-10-19)
**New Plugin Release:**
- Released **Incident Response Playbook Creator** v1.0.0
  - Based on NIST SP 800-61r3 (April 2025)
  - 3 incident scenarios with GDPR/HIPAA compliance
  - 110KB authoritative reference data
- Updated repository documentation

### Version 1.1.0 (2025-10-19)
**New Plugin Release:**
- Released **Cybersecurity Policy Generator** v1.0.0
  - 51 professional policy templates (SANS + CIS Controls)
  - 320KB reference data with compliance framework mappings
  - Interactive AskUserQuestion workflow
  - Multi-format generation (Markdown, Word, HTML, PDF)
  - Production-tested with real organization (Guatemaltek)

### Version 1.0.0 (2025-10-18)
**Initial Release:**
- Released **GDPR Auditor** v1.0.0
  - 8 comprehensive GDPR reference documents
  - 5 automated static code scanning tools
  - Complete compliance audit workflow
- Released **PDF Smart Extractor** v1.0.0
  - 100% content preservation with PyMuPDF
  - 12-115x token reduction
  - Persistent caching architecture
  - Tested with NIST documents up to 35MB

---

## 🙏 Acknowledgments

**Data Sources:**
- **GDPR Auditor:** EUR-Lex (Official EU Law), ICO Guidance, EDPB Guidelines
- **Policy Generator:** SANS Institute Policy Templates, CIS Controls v8, ISO 27001, NIST CSF, SOC 2 Trust Service Criteria
- **IR Playbook Creator:** NIST SP 800-61r3, NIST CSF 2.0, CISA Playbooks, GDPR Articles 33/34, HIPAA Breach Notification Rule
- **Smart Extractors:** PyMuPDF, openpyxl, python-docx (open-source libraries)

**Community:**
Thanks to all contributors, testers, and users who help improve these plugins!

---

**Security & Compliance Marketplace** - Professional plugins for Claude Code
