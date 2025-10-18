# Claude Skill Design Principles

**Version:** 1.0
**Last Updated:** 2025-10-19
**Status:** Official Guidelines for ClaudeSkillCollection Marketplace

---

## Core Philosophy

Claude Code skills and plugins are designed to help Claude **generate tangible deliverables**, not to perform live system analysis, real-time monitoring, or subjective assessments.

**Key Principle:**
> Skills provide Claude with systematic workflows, reference materials, and templates to produce structured outputs (reports, documents, configurations, code) based on analyzing static files and following objective criteria.

---

## ✅ What Claude Skills ARE

### 1. Document Generators
**Definition:** Tools that create specific file types and structured outputs.

**Examples:**
- ✅ GDPR Compliance Report Generator
- ✅ Privacy Policy Document Creator
- ✅ Security Audit Report Builder
- ✅ API Documentation Generator
- ✅ Configuration File Creator

**Pattern:**
```
Input: Codebase files, schemas, existing docs
Process: Analyze against templates and standards
Output: Formatted document (MD, PDF, HTML, JSON, etc.)
```

### 2. Workflow Guides
**Definition:** Step-by-step instructions for systematic, repeatable tasks.

**Examples:**
- ✅ GDPR Compliance Audit Workflow
- ✅ Security Review Checklist Process
- ✅ Code Migration Step-by-Step Guide
- ✅ Deployment Preparation Workflow
- ✅ Incident Response Procedure

**Pattern:**
```
Input: User request + codebase context
Process: Follow systematic multi-step workflow
Output: Completed checklist + findings + recommendations
```

### 3. Template Systems
**Definition:** Reusable patterns and boilerplates that can be customized.

**Examples:**
- ✅ Privacy Policy Templates
- ✅ Security Configuration Templates
- ✅ API Endpoint Boilerplates
- ✅ Test Case Templates
- ✅ Documentation Scaffolds

**Pattern:**
```
Input: Project specifications and requirements
Process: Select and customize appropriate template
Output: Tailored code/config/document from template
```

### 4. Format Converters
**Definition:** Tools that transform data from one format to another.

**Examples:**
- ✅ Database Schema → Documentation
- ✅ API Spec → Client Code
- ✅ Config Files → Human-Readable Reports
- ✅ Code Comments → API Docs
- ✅ CSV Data → Compliance Reports

**Pattern:**
```
Input: Data in format A (JSON, YAML, SQL, etc.)
Process: Transform according to rules and templates
Output: Data in format B (MD, HTML, PDF, etc.)
```

### 5. Code Libraries
**Definition:** Utilities that manipulate file structures and generate code.

**Examples:**
- ✅ Scaffolding Generators
- ✅ Boilerplate Code Creators
- ✅ Configuration Builders
- ✅ Test File Generators
- ✅ Migration Script Creators

**Pattern:**
```
Input: Project structure and requirements
Process: Generate code following patterns and standards
Output: Code files, configs, or file structure changes
```

---

## ❌ What Claude Skills are NOT

### 1. Live Analysis Tools
**Why NOT:** Require real-time system access or running applications.

**Anti-patterns (Do NOT create):**
- ❌ Live Vulnerability Scanner - Scans running systems
- ❌ Active Port Scanner - Probes network in real-time
- ❌ Runtime Debugger - Requires live process access
- ❌ Memory Analyzer - Needs running application
- ❌ Database Query Executor - Runs live queries

**The Problem:**
- Requires external system access
- Can't work with static files alone
- May have security/ethical implications
- Not reproducible or auditable

**Alternative Approach:**
Instead of "Live Vulnerability Scanner," create:
- ✅ **Vulnerability Assessment Report Generator** - Analyzes code for known patterns and generates findings report

### 2. External Services
**Why NOT:** Depend on APIs or third-party integrations that may fail, change, or have availability issues.

**Anti-patterns (Do NOT create):**
- ❌ API Health Monitor - Calls external APIs continuously
- ❌ Cloud Resource Checker - Requires cloud provider API access
- ❌ Third-party Service Status - Depends on external services
- ❌ Payment Gateway Tester - Calls payment APIs
- ❌ Email Deliverability Checker - Sends actual emails

**The Problem:**
- Dependencies on external services
- Requires API keys/credentials
- May incur costs
- Unreliable (network, rate limits, downtime)

**Alternative Approach:**
Instead of "API Health Monitor," create:
- ✅ **API Integration Checklist Generator** - Creates checklist for manual API testing based on OpenAPI spec

### 3. Real-time Monitors
**Why NOT:** Need continuous data streams or ongoing observation.

**Anti-patterns (Do NOT create):**
- ❌ Performance Monitor - Watches metrics continuously
- ❌ Log Stream Analyzer - Requires live log access
- ❌ Traffic Monitor - Observes network traffic in real-time
- ❌ Resource Usage Tracker - Monitors CPU/memory continuously
- ❌ Error Rate Dashboard - Displays live error counts

**The Problem:**
- Requires continuous operation
- Can't produce finite deliverable
- Not suitable for one-time skill execution

**Alternative Approach:**
Instead of "Performance Monitor," create:
- ✅ **Performance Audit Report Generator** - Analyzes code for performance anti-patterns and generates recommendations

### 4. Subjective Assessors
**Why NOT:** Make judgments without clear, objective criteria.

**Anti-patterns (Do NOT create):**
- ❌ Code Quality Scorer - Gives arbitrary quality score
- ❌ Design Beauty Rater - Subjective aesthetic judgment
- ❌ "Best Practices" Checker - Without specific standards
- ❌ Priority Assigner - Arbitrary importance ratings
- ❌ Complexity Estimator - Vague complexity metrics

**The Problem:**
- No objective, verifiable criteria
- Results not reproducible
- Can't cite authoritative sources
- May conflict with team standards

**Alternative Approach:**
Instead of "Code Quality Scorer," create:
- ✅ **Code Standards Compliance Checker** - Checks against specific style guide (PEP 8, ESLint, etc.) and generates report

### 5. Simple Calculators
**Why NOT:** Just return a single number without context or actionable output.

**Anti-patterns (Do NOT create):**
- ❌ Lines of Code Counter - Returns single number
- ❌ File Count Calculator - Just counts files
- ❌ Average Calculator - Simple math operation
- ❌ Percentage Calculator - Basic arithmetic
- ❌ Time Estimator - Single duration output

**The Problem:**
- Too trivial for a skill
- No systematic workflow
- No structured deliverable
- Better as simple script/function

**Alternative Approach:**
Instead of "Lines of Code Counter," create:
- ✅ **Codebase Metrics Report Generator** - Comprehensive report with LOC, complexity, test coverage, trends, and recommendations

---

## Design Validation Checklist

Before creating or submitting a skill, verify it passes ALL these criteria:

### Required Criteria (Must Pass All)

1. **✅ Produces Tangible Deliverable**
   - Generates a file (report, config, code, document)
   - Creates structured output (checklist, table, diagram)
   - Builds reusable artifact (template, boilerplate)

   ❌ **Fails if:** Just returns a number, status, or yes/no answer

2. **✅ Works with Static Files**
   - Analyzes existing code/configuration/documentation
   - Processes files in the repository
   - Uses provided inputs (no live system access)

   ❌ **Fails if:** Requires running application, API calls, or network access

3. **✅ Follows Systematic Workflow**
   - Clear step-by-step process
   - Documented methodology
   - Repeatable and deterministic

   ❌ **Fails if:** Adhoc process, random exploration, or unclear steps

4. **✅ Based on Objective Criteria**
   - Cites regulations (GDPR, CCPA, HIPAA, etc.)
   - References standards (OWASP, NIST, PCI DSS, etc.)
   - Uses best practices (style guides, industry frameworks)

   ❌ **Fails if:** Makes subjective judgments without clear criteria

5. **✅ Includes Reference Materials**
   - Authoritative sources (official regulations, standards bodies)
   - Templates and examples
   - Implementation guidelines

   ❌ **Fails if:** No supporting materials or unverified sources

---

## Good Skill Patterns

### Pattern 1: Compliance Audit
```
Skill: GDPR Compliance Auditor

Input:
- Codebase files (Python, JS, etc.)
- Database schemas
- Configuration files
- Privacy policy (if exists)

Process:
1. Scan code for personal data collection patterns
2. Analyze database for PII storage
3. Check data subject rights implementation
4. Review security measures
5. Consult GDPR reference materials

Output:
- Comprehensive compliance report (Markdown)
- Risk-prioritized findings
- Specific code references (file:line)
- GDPR article citations
- Actionable recommendations

Why It Works:
✅ Tangible deliverable (report)
✅ Works with static files
✅ Systematic workflow
✅ Objective criteria (GDPR articles)
✅ Reference materials included
```

### Pattern 2: Document Generator
```
Skill: Privacy Policy Generator

Input:
- Application description
- Data practices (collected, processed, shared)
- Legal jurisdiction
- Data retention policies

Process:
1. Identify data categories
2. Map to legal bases
3. Select privacy policy template
4. Customize sections
5. Add jurisdiction-specific clauses

Output:
- Complete privacy policy (Markdown/HTML)
- GDPR/CCPA compliance annotations
- Customization checklist
- Review guidelines

Why It Works:
✅ Tangible deliverable (document)
✅ Template-based generation
✅ Systematic workflow
✅ Objective criteria (regulations)
✅ Templates and references included
```

### Pattern 3: Code Generator
```
Skill: API Security Configuration Generator

Input:
- API specification (OpenAPI/Swagger)
- Security requirements
- Authentication method
- Deployment environment

Process:
1. Analyze API endpoints
2. Identify security needs (auth, CORS, rate limiting)
3. Select configuration template
4. Generate security configs
5. Add inline documentation

Output:
- Security configuration files
- Implementation checklist
- Testing guidelines
- Documentation

Why It Works:
✅ Tangible deliverable (config files)
✅ Template-based approach
✅ Systematic workflow
✅ Security best practices (OWASP)
✅ References and examples included
```

---

## Bad Skill Patterns (Will Be Rejected)

### Anti-pattern 1: Live System Scanner
```
❌ Skill: Live Vulnerability Scanner

Description:
"Scans running applications for security vulnerabilities"

Why It's Bad:
- Requires live system access
- Needs network connectivity
- May trigger security alerts
- Can't work with static files
- Ethical concerns (scanning without permission)

Better Alternative:
✅ Vulnerability Assessment Report Generator
- Analyzes code for known vulnerability patterns
- Checks dependencies against CVE databases (offline)
- Generates remediation recommendations
- Creates security audit report
```

### Anti-pattern 2: External API Monitor
```
❌ Skill: Third-party API Health Monitor

Description:
"Continuously monitors external API availability and response times"

Why It's Bad:
- Requires API keys and credentials
- Depends on external services
- Continuous operation (not one-time)
- May incur API costs
- Network dependent

Better Alternative:
✅ API Integration Checklist Generator
- Analyzes API specifications
- Creates testing checklist
- Generates integration documentation
- Provides error handling templates
```

### Anti-pattern 3: Subjective Code Scorer
```
❌ Skill: Code Quality Scorer

Description:
"Rates code quality from 1-10 based on 'best practices'"

Why It's Bad:
- No objective criteria
- Arbitrary scoring system
- Not based on specific standards
- Results not actionable
- Can't cite authoritative sources

Better Alternative:
✅ Code Standards Compliance Reporter
- Checks against specific style guide (PEP 8, Airbnb JS, etc.)
- Identifies violations with line numbers
- Generates compliance report
- Provides auto-fix suggestions
- Cites official style guide sections
```

---

## Implementation Guidelines

### Skill Structure

Every skill should include:

```
skill-name/
├── SKILL.md                 # Claude agent prompt
├── plugin.json              # Plugin manifest
├── README.md                # User documentation
├── references/              # Authoritative sources
│   ├── regulations.md       # Legal/compliance sources
│   ├── standards.md         # Technical standards
│   └── best-practices.md    # Industry guidelines
├── templates/               # Reusable patterns
│   ├── report-template.md
│   └── checklist-template.md
├── scripts/                 # Automation tools (optional)
│   └── analyzer.py
└── examples/                # Usage examples
    └── sample-output.md
```

### SKILL.md Template

```markdown
---
name: skill-name
description: Clear one-sentence description focusing on deliverable
license: MIT
---

# Skill Name

## Purpose
[2-3 sentences describing what deliverable this skill produces]

## When to Use This Skill
- Use case 1 (specific scenario)
- Use case 2 (specific scenario)
- Use case 3 (specific scenario)

## When NOT to Use This Skill
- Anti-use case 1
- Anti-use case 2

## Workflow

### Phase 1: [Name]
1. Step 1
2. Step 2
3. Step 3

### Phase 2: [Name]
1. Step 1
2. Step 2

### Phase 3: Generate Deliverable
[Description of output format and contents]

## Reference Materials
- `references/regulations.md` - [Description]
- `references/standards.md` - [Description]
- `templates/report.md` - [Description]

## Output Format
[Detailed description of deliverable structure]

## Defensive Security Note
[If applicable: How this skill follows defensive security principles]
```

---

## Quality Standards

### Reference Materials Must:
- ✅ Cite authoritative sources (EUR-Lex, NIST, OWASP, ISO, etc.)
- ✅ Include publication dates
- ✅ Link to official documentation
- ✅ Be verifiable and accurate
- ❌ NOT contain hallucinated facts
- ❌ NOT use unverified claims
- ❌ NOT rely on outdated information

### Templates Must:
- ✅ Be production-ready
- ✅ Include inline documentation
- ✅ Provide customization guidance
- ✅ Show example usage
- ❌ NOT be placeholder-heavy
- ❌ NOT require external tools
- ❌ NOT have hard-coded values

### Scripts Must:
- ✅ Have error handling
- ✅ Include type hints (Python)
- ✅ Provide help/usage info
- ✅ Work offline when possible
- ❌ NOT make network calls (unless essential)
- ❌ NOT require API keys
- ❌ NOT have security vulnerabilities

---

## Examples from This Marketplace

### ✅ Good Example: GDPR Auditor

**What it does:**
- Analyzes code for GDPR compliance issues
- Generates comprehensive audit report
- Provides specific findings with code references

**Why it's good:**
- ✅ Produces tangible deliverable (audit report)
- ✅ Works with static code files
- ✅ Systematic audit workflow
- ✅ Based on GDPR regulations (objective criteria)
- ✅ 8 reference documents with official sources
- ✅ 5 automation scripts
- ✅ Production-tested

**Deliverable Example:**
```markdown
# GDPR Compliance Audit Report
Generated: 2025-10-19

## Executive Summary
[Risk level, key findings, compliance score]

## Findings
### Critical Issues (3)
1. Unencrypted PII in database
   - File: models.py:45
   - GDPR Article: 32 (Security)
   - Recommendation: Implement encryption at rest

[... more findings ...]

## Compliance Checklist
- [x] Data inventory complete
- [ ] Consent mechanisms implemented
- [ ] Data retention policies defined

[... full report ...]
```

---

## Review Criteria

Skills submitted to this marketplace will be reviewed against these criteria:

### Mandatory Requirements (Must Pass)
1. ✅ Follows core design principles (document generator, workflow guide, etc.)
2. ✅ Produces tangible deliverable
3. ✅ Works with static files only
4. ✅ Based on objective, verifiable criteria
5. ✅ Includes authoritative reference materials
6. ✅ MIT License
7. ✅ Production-ready (tested on real projects)
8. ✅ Defensive security only (no offensive tools)

### Quality Standards (Should Meet Most)
- Comprehensive documentation
- Clear usage examples
- Error handling in scripts
- Professional code quality
- Contribution guidelines
- Changelog and versioning

### Grounds for Rejection
- ❌ Requires live system access
- ❌ Depends on external APIs
- ❌ Makes subjective judgments without criteria
- ❌ No tangible deliverable
- ❌ Contains malicious code
- ❌ Plagiarized content
- ❌ Unverified claims
- ❌ Offensive security tools

---

## FAQ

### Q: Can skills use external Python libraries?
**A:** Yes, if they're standard libraries (requests, pandas, etc.) and clearly documented as requirements. Avoid obscure dependencies.

### Q: Can skills make HTTP requests?
**A:** Only if essential for the deliverable (e.g., fetching public CVE data). Must work offline when possible. Never require API keys for core functionality.

### Q: Can skills analyze log files?
**A:** Yes! Analyzing static log files is fine. Creating reports from logs is a perfect use case. Just don't require live log streams.

### Q: Can skills run tests?
**A:** Yes, if the output is a test report. "Test Result Report Generator" that runs tests and formats results is valid.

### Q: What about database analysis?
**A:** Analyzing database schemas (DDL/migrations) is great. Connecting to live databases to query data is not allowed.

### Q: Can skills use AI/LLM APIs?
**A:** Generally no, as it creates external dependencies. Skills should leverage Claude's native capabilities through well-structured prompts and reference materials.

---

## Summary

**Core Principle:**
> Skills help Claude generate deliverables through systematic workflows, not perform live analysis or real-time monitoring.

**Before Creating a Skill, Ask:**
1. What tangible deliverable does it produce?
2. Can it work with static files only?
3. Does it follow a clear, systematic workflow?
4. Is it based on objective, verifiable criteria?
5. Have I included authoritative reference materials?

**If you answered YES to all 5, you have a valid skill!**

---

**Document Version:** 1.0
**Last Updated:** 2025-10-19
**Maintained By:** Diego Consolini <diego@diegocon.nl>
**Repository:** https://github.com/diegocconsolini/ClaudeSkillCollection
