# Security & Compliance Marketplace

**Professional Security, Compliance, and Productivity Plugins for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection/releases)
[![Plugins](https://img.shields.io/badge/plugins-7-green.svg)](https://github.com/diegocconsolini/ClaudeSkillCollection)

A curated collection of production-ready security, compliance, and productivity plugins for Claude Code. Built on authoritative sources and rigorously tested with real-world data.

## 🚀 Quick Start

### Step 1: Add Marketplace (GitHub Repository)

```bash
# IMPORTANT: Use GitHub repository format for remote updates
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
```

**⚠️ Critical:** Do NOT use local paths like `/path/to/ClaudeSkillCollection` as this prevents remote updates. Always use the GitHub format `owner/repo` for automatic updates.

### Step 2: Install Plugins

```bash
# Install desired plugins from the marketplace
/plugin install plugin-security-checker@security-compliance-marketplace
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install pdf-smart-extractor@security-compliance-marketplace
```

### Step 3: Enable Plugins and Restart

After installation:
1. **Enable plugins** via `/plugin` interface (plugins are disabled by default after first install)
2. **Restart Claude Code** to load the plugins properly

### Updating Plugins

```bash
# To get updates from GitHub:
/plugin  # Navigate to plugin details and select "Update now"

# If you installed with a local path and can't update:
/plugin marketplace remove security-compliance-marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection  # Re-add using GitHub format
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

**How caching works (v2.0.0 - Unified System):**
1. **First extraction:** Processes document locally (PyMuPDF for PDF, openpyxl for Excel, python-docx for Word)
2. **Persistent cache:** Stores extracted content in `~/.claude-cache/{doc_type}/` with SHAKE256 hash keys (SHA-3 family)
3. **Subsequent queries:** Instant - uses cached extraction, no re-processing needed
4. **Token optimization:** 10-100x reduction by loading only relevant chunks, not entire documents
5. **Automatic migration:** Old caches (SHA-256) automatically migrate to new format (SHAKE256)

All three extractors share unified caching: Local extraction → Semantic chunking → Persistent caching → Efficient querying

**What's new in v2.0.0:**
- Unified cache location: `~/.claude-cache/` (was `~/.claude-{type}-cache/`)
- Modern hashing: SHAKE256 (was SHA-256)
- Automatic migration from v1.x caches
- Shared caching library for consistency
- See `/shared/CACHE_STRATEGY.md` for details

**⚠️ IMPORTANT: Cache Location Behavior**

Extracted files are stored in **user cache directory**, NOT your working directory:

**Cache locations by platform:**
- **Linux/Mac:** `~/.claude-cache/{pdf,xlsx,docx}/{document_name}_{hash}/`
- **Windows:** `C:\Users\{username}\.claude-cache\{pdf,xlsx,docx}\{document_name}_{hash}\`

**Why cache directory instead of working directory?**
- **Cross-project reuse:** Same document analyzed from different projects uses the same cache
- **Persistent caching:** Extract once, query forever (even after closing Claude Code)
- **Performance:** Subsequent queries are instant (no re-extraction)
- **Disk space efficiency:** One extraction shared across all projects

**Accessing cached content:**
```bash
# List all cached documents
python scripts/query_{pdf,xlsx,docx}.py list

# Query specific document
python scripts/query_pdf.py search {cache_key} "your search"

# Copy cache to working directory (if needed)
cp -r ~/.claude-cache/pdf/{cache_key}/* ./extracted/
```

**Note:** Cache is local and not meant for version control. Keep original documents in your repo and let each developer extract locally (one-time operation).

---

## 🔒 Security & Compliance Plugins

### 1. Plugin Security Checker
**Production Ready** • **v3.0.0** • **Plugin Vulnerability Scanner**

Advanced security scanner for Claude Code plugins with 91 specialized pattern detection agents. Performs static code analysis to detect vulnerabilities, code obfuscation, hardcoded credentials, and security anti-patterns before you install untrusted plugins.

**Technical Foundation:**
- **IntelligentOrchestrator:** Consensus voting across 91 specialized agents
- **AccuracyCache:** Bloom filter + Trie hybrid with zero false positives
- **MITRE ATT&CK/ATLAS:** Framework mapping for attack technique identification
- **Adaptive Learning:** Auto-evolving rules from validated detections
- **Real-World Testing:** Successfully scanned 987 plugins from 15 marketplaces (100% scan success rate)

**Key Features:**
- **91 Specialized Agents** - 17 CRITICAL, 39 HIGH, 23 MEDIUM, 2 LOW severity patterns
- **Consensus Voting** - Multiple agents vote on each detection with conflict resolution
- **Dangerous Function Detection** - Python (eval, exec, os.system) and JavaScript (eval, innerHTML)
- **Code Obfuscation Detection** - Base64 encoding, hex encoding, character obfuscation
- **Credential Scanning** - Hardcoded API keys, passwords, cloud credentials, private keys
- **Schema Validation** - Validates plugin.json structure and configurations
- **CVE Mapping** - Links findings to CVE-2025-52882, CVE-2025-54794, CVE-2025-54795, CVE-2025-59828
- **OWASP API Top 10** - Mappings to API1 (BOLA), API2 (Auth), API7 (SSRF), API8 (Misconfig)
- **Comprehensive Reporting** - JSON, Markdown, and HTML report generation

**Real-World Results:**
- Scanned 987 plugins across 15 marketplace repositories
- CRITICAL Risk: 3 plugins (0.3%)
- HIGH Risk: 1 plugin (0.1%)
- LOW Risk: 982 plugins (99.5%)
- Test Results: 29/29 tests passed (100%)
- Memory Usage: ~17 MB (3.4% of 500MB budget)
- Cache Throughput: 11,111 ops/sec

**Use Cases:**
- Pre-installation security scanning of Claude Code plugins
- Vulnerability assessment of plugin code before running
- Security auditing of plugin repositories and marketplaces
- Identifying malicious or suspicious code patterns
- Validating plugin compliance with security best practices
- Research and analysis of plugin security landscape

**Who Should Use:**
- Anyone installing Claude Code plugins from third-party sources
- Plugin developers testing their own plugins for security issues
- Security researchers analyzing the plugin ecosystem
- Organizations with strict security policies for tooling
- Marketplace maintainers validating submitted plugins
- Security teams conducting defensive security assessments

**Commands:**
```bash
# Scan a single plugin
python3 scripts/scan_plugin.py /path/to/plugin

# Scan with JSON output
python3 scripts/scan_plugin.py /path/to/plugin --output scan.json --format json

# Generate Markdown report
python3 scripts/generate_report.py scan.json --format markdown --output report.md

# Using IntelligentOrchestrator (Python API)
from intelligent_orchestrator import IntelligentOrchestrator
orchestrator = IntelligentOrchestrator(
    patterns_file="references/dangerous_functions_expanded.json",
    max_memory_mb=500
)
detections = orchestrator.scan_file("plugin.py", code)
orchestrator.export_findings("findings.json")
```

**Important Disclaimer:**
This is a SUPPORTING TOOL for preliminary security checks only. It does NOT guarantee plugin safety. Always review source code manually before installing plugins. You are ultimately responsible for plugins you install.

[→ View Plugin Security Checker Documentation](./plugin-security-checker/README.md)

---

### 2. GDPR Auditor
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

### 3. Cybersecurity Policy Generator
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

### 4. Incident Response Playbook Creator
**Production Ready** • **v2.0.0** • **Incident Response & Security Operations**

Professional incident response playbook generator based on NIST SP 800-61r3 and authoritative sources. Creates comprehensive, customized IR documentation covering modern threat landscape with built-in GDPR and HIPAA compliance guidance.

**Authoritative Sources:**
- NIST SP 800-61r3: Computer Security Incident Handling Guide (April 2025 revision)
- NIST SP 800-218: Secure Software Development Framework (SSDF)
- NIST SP 800-161r1-upd1: Cybersecurity Supply Chain Risk Management (C-SCRM)
- NIST SP 800-190: Application Container Security Guide
- NIST SP 800-82r3: Guide to Operational Technology (OT) Security - ICS
- NIST IR 8228: IoT Device Cybersecurity Capability Core Baseline
- AWS Security Incident Response Guide
- CISA DDoS Attack Response Guide
- OWASP API Security Top 10 2023
- NIST Cybersecurity Framework 2.0: Function and category mappings (February 2024)
- GDPR (EU 2016/679): Article 33 (72-hour breach notification) and Article 34 (data subject notification)
- HIPAA Breach Notification Rule: 45 CFR §§164.400-414 (60-day timeline)
- 288KB total reference data (incident_scenarios_v2.json: 58KB, 11 scenarios)

**Key Features:**
- **11 comprehensive incident scenarios** covering traditional, modern, and emerging threats
- Based on 8 authoritative sources (NIST, AWS, CISA, OWASP)
- GDPR Article 33/34 breach notification requirements (72-hour timeline)
- HIPAA Breach Notification Rule guidance (60-day timeline)
- NIST Cybersecurity Framework 2.0 function mapping (DE, RS, RC)
- Interactive AskUserQuestion workflow for organization customization
- Professional Markdown playbook output ready for SOC/CSIRT teams
- 100% validation pass rate across all scenarios

**Available Scenarios:**

**Traditional Threats (3):**
1. **Ransomware Attack** (Critical) - File encryption, lateral movement, backup destruction
2. **Data Breach / Exfiltration** (Critical) - Unauthorized data access and theft
3. **Phishing / Business Email Compromise** (High) - Social engineering and credential theft

**Modern & Emerging Threats (3):**
4. **AI/ML Security Incident** (High) - Model poisoning, prompt injection, adversarial attacks
5. **Supply Chain Attack** (Critical) - Compromised dependencies, build pipeline injection
6. **API Security Incident** (High) - BOLA/IDOR, broken authentication, rate-limit bypass

**Critical Infrastructure & Cloud (3):**
7. **Container/Kubernetes Security** (High) - Pod escape, RBAC bypass, malicious images
8. **IoT/OT Security Incident** (Critical) - IoT botnets, SCADA exploitation, ICS disruption
9. **Cloud Security Breach** (Critical) - IAM compromise, misconfigured storage, metadata abuse

**Insider & Availability (2):**
10. **Insider Threat** (Critical) - Privileged user abuse, data exfiltration, sabotage
11. **DDoS Attack** (High) - Volumetric, protocol, and application-layer attacks

**Each Playbook Includes:**
- **Detection & Indicators** - Technical and behavioral IOCs mapped to NIST CSF 2.0 (8-9 indicators per scenario)
- **Response Procedures** - Step-by-step actions (Triage → Containment → Eradication) with 15-18 action steps
- **Recovery Actions** - System restoration with validation checklists
- **Communication Templates** - Internal, external, and regulatory notifications
- **Compliance Guidance** - GDPR Article 33/34 and HIPAA Breach Notification Rule
- **Roles & Responsibilities** - Clear team structure and escalation criteria
- **Post-Incident Activities** - Lessons learned and documentation requirements

**Quality Metrics (v2.0.0):**
- 8-9 technical indicators per scenario (industry-leading coverage)
- 5-7 behavioral indicators per scenario
- 8-9 NIST CSF 2.0 function mappings per scenario
- Average playbook size: 412 lines (400-422 range)
- 100% validation pass rate across all scenarios

**Use Cases:**
- Building your first incident response program
- Updating IR playbooks to NIST SP 800-61r3 (April 2025) and modern threats
- Preparing for compliance audits (GDPR, HIPAA)
- Creating scenario-specific response procedures
- Training security operations teams on modern threat landscape
- Meeting cyber insurance requirements
- Tabletop exercise preparation for diverse threat scenarios
- Covering modern threats: AI/ML, supply chain, cloud, API, containers, IoT/OT

**Who Should Use:**
- Security Operations Centers (SOC) and CSIRT teams
- Incident Response managers and coordinators
- CISOs establishing or modernizing IR programs
- Compliance officers (GDPR, HIPAA)
- MSPs and MSSPs serving clients
- IT managers preparing for security incidents
- Organizations in regulated industries (healthcare, finance)
- DevSecOps teams managing cloud and container infrastructure
- OT/ICS security teams in critical infrastructure sectors

[→ View Incident Response Playbook Creator Documentation](./incident-response-playbook-creator/README.md)

---

## 📊 Productivity Tools

### 5. PDF Smart Extractor
**Production Ready** • **v2.0.0** • **NEW: Unified Caching System**

Extract and analyze large PDF documents with 99%+ content preservation and 12-115x token reduction. Perfect for technical documentation, compliance frameworks, and research papers that exceed LLM context windows.

**October 2025 Updates:**
- ✅ **Password protection support** - Interactive prompts + CLI arguments for encrypted PDFs
- ✅ **Edge case documentation** - Shell escaping issues with special characters documented
- ✅ **Real-world testing** - Large encrypted PDFs (140 pages, 8.39MB) successfully extracted
- ✅ **Security considerations** - Passwords never cached, getpass.getpass() for hidden input

**Caching Architecture:**
- **Cache location:** `~/.claude-cache/pdf/{pdf_name}_{hash}/`
- **Cache key:** SHAKE256 hash (SHA-3 family, first 16 chars) ensures unique identification
- **Cache contents:** full_text.txt, pages.json, metadata.json, toc.json, manifest.json
- **Cache reuse:** Instant - no re-extraction needed (unless --force flag used)
- **Password handling:** Passwords NEVER stored in cache (security by design)
- **Migration:** Old SHA-256 caches automatically migrate to SHAKE256 format

**Key Features:**
- **Local Extraction** - Zero LLM involvement, complete privacy
- **Semantic Chunking** - Intelligent splitting at chapters, sections, paragraphs
- **12-115x Token Reduction** - Load only relevant chunks, not entire documents
- **Persistent Caching** - Extract once, query forever
- **Password Support** - Interactive prompts (recommended) or CLI arguments for encrypted PDFs
- **Content Preservation** - 99.76-99.81% preservation rate
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

### 6. Excel Smart Extractor
**Production Ready** • **v2.0.0** • **Large Workbook Analysis & Unified Caching**

Extract and analyze large Excel workbooks (1MB-50MB+) with comprehensive content preservation and 20-100x token reduction. Perfect for compliance matrices, financial models, security audit logs, and data tables that exceed LLM context windows.

**Caching Architecture:**
- **Cache location:** `~/.claude-cache/xlsx/{workbook_name}_{hash}/`
- **Cache key:** SHAKE256 hash (SHA-3 family, first 16 chars) ensures unique identification
- **Cache contents:** full_workbook.json, sheet_{name}.json, named_ranges.json, metadata.json, manifest.json
- **Cache reuse:** Instant - no re-extraction needed (unless --force flag used)
- **Comprehensive extraction:** Formulas, formatting, metadata, named ranges, merged cells
- **Migration:** Old SHA-256 caches automatically migrate to SHAKE256 format

**Key Features:**
- **Local Extraction** - Zero LLM involvement, complete privacy (openpyxl-powered)
- **Comprehensive Content Extraction** - Formulas, cell formatting, merged cells, hyperlinks, named ranges
- **20-100x Token Reduction** - Load only relevant sheets/columns, not entire workbooks
- **Persistent Caching** - Extract once, query forever
- **Semantic Chunking** - Intelligent splitting by sheets, columns, and row ranges
- **Fast Processing** - <5 seconds first extraction, <1 second subsequent queries
- **Read-Only Operations** - Never modifies source files

**Real Performance (Comprehensive Testing - October 2025):**
- **9 real-world files tested** (110KB - 1.5MB)
- **287,460 cells processed** across 85 sheets
- **15,409 formulas extracted** including array formulas
- **Comprehensive extraction** including formulas, formatting, and metadata
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

### 7. Word Smart Extractor
**Production Ready** • **v2.0.0** • **Large Document Analysis & Unified Caching**

Extract and analyze large Word documents (1MB-50MB+) with comprehensive content extraction and 10-50x token reduction. Perfect for policy documents, technical reports, contracts, and meeting notes with clear heading structure.

**Caching Architecture:**
- **Cache location:** `~/.claude-cache/docx/{document_name}_{hash}/`
- **Cache key:** SHAKE256 hash (SHA-3 family, first 16 chars) ensures unique identification
- **Cache contents:** full_text.txt, paragraphs.json, tables.json, metadata.json, headings.json, manifest.json
- **Cache reuse:** Instant - no re-extraction needed (unless --force flag used)
- **Content extraction:** Text, tables, formatting, comments, tracked changes, headers/footers
- **Migration:** Old SHA-256 caches automatically migrate to SHAKE256 format

**Key Features:**
- **Local Extraction** - Zero LLM involvement, complete privacy (python-docx powered)
- **Comprehensive Content Extraction** - Text, tables, formatting, comments, tracked changes
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
│ 2. Plugin generates SHAKE256 hash of document (SHA-3)       │
│ 3. Creates cache directory: ~/.claude-cache/{type}/{name}_{hash}/ │
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
- ✅ **Automatic invalidation** - Document changes detected via SHAKE256 hash (SHA-3 family)
- ✅ **Automatic migration** - Old SHA-256 caches automatically migrate to SHAKE256 format

**Cache Locations (v2.0.0 Unified):**
- PDF: `~/.claude-cache/pdf/{pdf_name}_{hash}/`
- Excel: `~/.claude-cache/xlsx/{workbook_name}_{hash}/`
- Word: `~/.claude-cache/docx/{document_name}_{hash}/`

**Cache Management:**
```bash
# Force re-extraction (bypass cache)
python scripts/extract_{pdf|xlsx|docx}.py document.{pdf|xlsx|docx} --force

# List all cached documents
python scripts/query_{pdf|xlsx|docx}.py list

# View cache statistics
python scripts/query_{pdf|xlsx|docx}.py stats {cache_key}

# Clear specific cache (v2.0.0 paths)
rm -rf ~/.claude-cache/{pdf|xlsx|docx}/{cache_key}/

# Clear all caches for one type
rm -rf ~/.claude-cache/{pdf|xlsx|docx}/

# Clear all caches (all three types)
rm -rf ~/.claude-cache/
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

### Plugin-Specific Dependencies

Some plugins require additional Python libraries. Each plugin includes a `requirements.txt` file for easy installation:

- **PDF Smart Extractor** - Requires `pymupdf` • [Installation Guide](./pdf-smart-extractor/README.md#installation)
- **Excel Smart Extractor** - Requires `openpyxl`, `pandas` • [Installation Guide](./xlsx-smart-extractor/README.md#installation)
- **Word Smart Extractor** - Requires `python-docx` • [Installation Guide](./docx-smart-extractor/README.md#installation)

**Installation methods:**
1. Virtual environment (recommended): Creates isolated Python environment
2. System-wide installation: Installs for all users

See individual plugin READMEs for detailed instructions and troubleshooting.

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
  2. Generate SHAKE256 cache key (SHA-3 family)
  3. Save to ~/.claude-cache/pdf/{name}_{hash}/
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
│   └── marketplace.json            # Plugin catalog (7 plugins)
│
├── plugin-security-checker/        # Plugin Security Checker v3.0.0
│   ├── README.md
│   ├── plugin.json
│   ├── agents/plugin-security-checker.md  # Agent with YAML frontmatter
│   ├── scripts/                    # 91 specialized pattern detection agents
│   │   ├── intelligent_orchestrator.py  # Consensus voting engine
│   │   ├── accuracy_cache.py       # Shared learning with Bloom+Trie
│   │   ├── pattern_agent.py        # Base agent class
│   │   ├── scan_plugin.py          # Main scanner
│   │   └── generate_report.py      # Report generation
│   ├── references/                 # Pattern databases and CVE mappings
│   │   └── dangerous_functions_expanded.json  # 91 patterns
│   └── examples/
│
├── gdpr-auditor/                   # GDPR Compliance Auditor
│   ├── README.md
│   ├── plugin.json
│   ├── agents/gdpr-auditor.md      # Agent with YAML frontmatter
│   ├── scripts/                    # 5 automated scanning tools
│   ├── references/                 # 8 GDPR reference documents (EUR-Lex, ICO, EDPB)
│   └── examples/
│
├── incident-response-playbook-creator/  # IR Playbook Generator v2.0.0
│   ├── README.md
│   ├── CHANGELOG.md                # v2.0.0 release notes
│   ├── plugin.json
│   ├── SKILL.md                    # Agent with YAML frontmatter
│   ├── scripts/                    # Playbook generation scripts
│   │   ├── browse_scenarios.py    # Browse 11 scenarios
│   │   └── generate_playbook_markdown.py  # Generate playbooks
│   ├── references/                 # 288KB NIST/AWS/CISA/OWASP data
│   │   ├── incident_scenarios_v2.json     # 11 scenarios (58KB, master file)
│   │   ├── incident_scenarios_simplified.json  # Legacy 4 scenarios
│   │   ├── framework_mappings.json
│   │   └── communication_templates.json
│   ├── output/                     # Generated playbooks
│   └── examples/
│
├── pdf-smart-extractor/            # PDF Smart Extractor (v2.0.0)
│   ├── README.md
│   ├── plugin.json
│   ├── agents/pdf-smart-extractor.md
│   ├── scripts/                    # extract, chunk, query scripts
│   ├── test-files/                 # Test PDFs
│   ├── TEST_RESULTS.md             # Comprehensive test report
│   ├── EDGE_CASES_PASSWORDS.md     # Password protection edge cases
│   └── PASSWORD_PROTECTION_TEST_LOG.md
│
├── xlsx-smart-extractor/           # Excel Smart Extractor (v2.0.0)
│   ├── README.md
│   ├── plugin.json
│   ├── agents/xlsx-smart-extractor.md
│   ├── scripts/                    # extract, chunk, query scripts
│   ├── test-files/                 # Test Excel files
│   └── TEST_RESULTS.md             # Comprehensive test report
│
├── docx-smart-extractor/           # Word Smart Extractor (v2.0.0)
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

### Version 2.0.0 (2025-10-24)
**New Plugin Release:**
- Released **Plugin Security Checker** v3.0.0
  - 91 specialized pattern detection agents (17 CRITICAL, 39 HIGH, 23 MEDIUM, 2 LOW)
  - IntelligentOrchestrator with consensus voting and conflict resolution
  - AccuracyCache with Bloom filter + Trie hybrid (zero false positives)
  - MITRE ATT&CK/ATLAS framework mapping for attack technique identification
  - Real-world testing: Scanned 987 plugins from 15 marketplaces (100% success rate)
  - Security results: 3 CRITICAL, 1 HIGH, 982 LOW risk plugins identified
  - Test coverage: 29/29 tests passed (100%)
  - Adaptive learning with auto-evolving rules from validated detections
  - CVE mapping: CVE-2025-52882, CVE-2025-54794, CVE-2025-54795, CVE-2025-59828
  - OWASP API Top 10 2023 mappings

**Marketplace Updates:**
- Updated marketplace to 7 total plugins
- Enhanced marketplace description with plugin security scanning capabilities

---

### Version 2.0.0-extractors (2025-10-21)
**Unified Caching System - Breaking Internal Changes, Zero User Impact:**
- **NEW:** Shared `smart_cache.py` library for all smart-extractors
  - SHAKE256 hashing (SHA-3 family) replaces SHA-256
  - Unified cache location: `~/.claude-cache/{doc_type}/` (was `~/.claude-{type}-cache/`)
  - Automatic SHA-256 → SHAKE256 cache migration (transparent to users)
  - Comprehensive documentation in `/shared/CACHE_STRATEGY.md` and `/shared/CHANGELOG.md`

**Extractor Updates:**
- **PDF Smart Extractor** v2.0.0 - Unified caching, tested with 316-page documents (8.2MB)
- **Excel Smart Extractor** v2.0.0 - Unified caching, tested with 19K cell workbooks
- **Word Smart Extractor** v2.0.0 - Unified caching, tested with policy documents

**Technical Improvements:**
- Zero external dependencies for caching (Python stdlib only)
- Bloom filter support for O(1) cache existence checks (optional)
- Future-ready for environment variable configuration (v2.1.0)
- LaTeX migration: Old caches automatically migrate on first access

**User Impact:**
- ✅ Zero breaking changes - everything works as before
- ✅ Automatic cache migration - no manual action needed
- ✅ Cleaner home directory - one `.claude-cache/` instead of three separate dirs

---

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

### Version 2.1.0 (2025-10-22)
**Major Plugin Update:**
- **Incident Response Playbook Creator** upgraded to v2.0.0
  - Expanded from 4 to 11 comprehensive incident scenarios (175% increase)
  - Added 7 new scenarios: Supply Chain, Container/K8s, IoT/OT, Cloud, API, Insider, DDoS
  - Enhanced original 4 scenarios with improved quality metrics
  - Based on 8 authoritative sources (NIST, AWS, CISA, OWASP)
  - 288KB total reference data (incident_scenarios_v2.json: 58KB, 11 scenarios)
  - All scenarios pass quality validation (100% success rate)
  - Critical bug fix: Added missing eradication field in data_breach scenario
  - Quality improvements: 8-9 technical indicators, 5-7 behavioral indicators, 8-9 NIST CSF IDs per scenario
  - Average playbook size: 412 lines (400-422 range)

### Version 1.3.0 (2025-10-19)
**New Plugin Release:**
- Released **Incident Response Playbook Creator** v1.0.0
  - Based on NIST SP 800-61r3 (April 2025)
  - 4 incident scenarios with GDPR/HIPAA compliance
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

## Acknowledgments

**Data Sources:**
- **GDPR Auditor:** EUR-Lex (Official EU Law), ICO Guidance, EDPB Guidelines
- **Policy Generator:** SANS Institute Policy Templates, CIS Controls v8, ISO 27001, NIST CSF, SOC 2 Trust Service Criteria
- **IR Playbook Creator:** NIST SP 800-61r3, NIST CSF 2.0, CISA Playbooks, GDPR Articles 33/34, HIPAA Breach Notification Rule
- **Smart Extractors:** PyMuPDF, openpyxl, python-docx (open-source libraries)

**Community:**
Thanks to all contributors, testers, and users who help improve these plugins!

---

**Security & Compliance Marketplace** - Professional plugins for Claude Code
