# Cybersecurity Policy Generator

**Version:** 1.0.0
**Category:** Security & Compliance
**Status:** Production Ready

Generate professional, framework-compliant cybersecurity policies from 51 industry-standard templates (SANS, CIS Controls) for ISO 27001, SOC 2, NIST, and CIS Controls compliance.

## Features

- 51 professional policy templates (36 SANS + 15 CIS Controls)
- Interactive customization using AskUserQuestion UI
- Framework compliance mapping (ISO 27001, SOC 2, NIST CSF, CIS Controls v8, GDPR)
- 4 output formats (Markdown, Word, HTML, PDF)
- 15 policy categories covering all security domains
- 5 comprehensive reference documents
- 4 automated Python tools

## Installation

### Via Marketplace (Recommended)

```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install cybersecurity-policy-generator@security-compliance-marketplace
```

### Traditional Method

```bash
cd ~/.claude/plugins/
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git
ln -s ClaudeSkillCollection/cybersecurity-policy-generator ./cybersecurity-policy-generator
```

### Python Dependencies

```bash
pip install python-docx markdown2 weasyprint
```

## Usage

### Basic Usage

```
"Create an Acceptable Use Policy for my organization"
"Generate a Password Policy for ISO 27001 compliance"
"I need an Incident Response Policy for SOC 2"
```

Claude will:
1. Show you available policy templates
2. Ask questions to customize for your organization (via beautiful AskUserQuestion UI)
3. Generate policy in all 4 formats (MD, DOCX, HTML, PDF)

### Advanced Usage

Browse specific policy categories:
```
"Show me all Identity and Access policies"
"What policies do I need for ISO 27001?"
"Find policies related to incident response"
```

Generate multiple policies:
```
"Generate the 5 foundational policies for a startup"
"Create all CIS Controls policies for my organization"
```

## What It Does

This plugin follows a systematic 4-phase workflow:

**Phase 1: Browse Templates**
- Browse 51 policy templates by category, framework, or keyword
- View policy descriptions and framework mappings
- Select the most appropriate policy for your needs

**Phase 2: Customize**
- Interactive questionnaire collects organization information
- Uses AskUserQuestion for beautiful multiple-choice UI
- Gathers company name, industry, size, governance, compliance requirements

**Phase 3: Apply**
- Replaces all placeholders with organization-specific values
- Adds compliance framework references
- Creates customized policy JSON

**Phase 4: Generate**
- Creates professional policy documents in 4 formats
- Markdown for documentation systems
- Word for legal review
- HTML for intranet publishing
- PDF for distribution

**Deliverables:** Complete, customized policy documents ready for legal review and approval.

## Scripts

### 1. `scripts/browse_policies.py`

**Purpose:** Browse, filter, and search through 51 policy templates

**Usage:**
```bash
# Show all policies
python scripts/browse_policies.py

# Filter by category
python scripts/browse_policies.py --category "Governance"

# Filter by framework
python scripts/browse_policies.py --framework "ISO 27001"

# Search by keyword
python scripts/browse_policies.py --search "incident"

# Show statistics
python scripts/browse_policies.py --stats

# List categories
python scripts/browse_policies.py --list-categories
```

### 2. `scripts/apply_customizations.py`

**Purpose:** Apply organization-specific customizations to policy templates

**Usage:**
```bash
python scripts/apply_customizations.py \
  --policy-id "acceptable-use-policy-template-04-25-2023" \
  --customizations customizations.json \
  --output customized_policy.json
```

### 3. `scripts/generate_markdown.py`

**Purpose:** Generate professional Markdown policy documents

**Usage:**
```bash
python scripts/generate_markdown.py \
  --input customized_policy.json \
  --output AcceptableUsePolicy.md
```

### 4. `scripts/generate_docx_html_pdf.py`

**Purpose:** Generate Word, HTML, and PDF policy documents

**Usage:**
```bash
python scripts/generate_docx_html_pdf.py \
  --input customized_policy.json \
  --output-dir ./output \
  --formats docx html pdf
```

## Reference Materials

This plugin includes comprehensive reference materials:

- `references/policies.json` - 51 complete policy templates (320KB, SANS + CIS)
- `references/buildingBlocks.json` - 169 reusable policy clauses (316KB)
- `references/framework_mappings.md` - Complete guide to ISO 27001, SOC 2, NIST, CIS, GDPR mappings
- `references/policy_categories.md` - Descriptions of all 15 policy categories
- `references/customization_guide.md` - Advanced customization techniques and best practices

All references are verified against authoritative sources (SANS Institute, CIS).

## Compliance Framework Coverage

| Framework | Policies | Coverage | Description |
|-----------|----------|----------|-------------|
| **ISO 27001** | 51 | 100% | All policies support ISO 27001 Annex A controls |
| **SOC 2** | 36 | 71% | SANS policies cover Trust Service Criteria |
| **NIST CSF** | 36 | 71% | Policies map to all 5 CSF functions |
| **CIS Controls v8** | 15 | 29% | Direct mapping to CIS Critical Security Controls |
| **GDPR** | 3 | 6% | Privacy-specific policies for data protection |

## Policy Categories (51 Policies)

- Governance (13) | Identity and Access (8) | Application (7)
- Compute (6) | Network (4) | Data Protection (2)
- Resilience (2) | Configuration Management (2)
- Logging and Monitoring (1) | Incident Management (1)
- Threat Protection (1) | Training and Awareness (1)
- Third-Party Risk (1) | Asset Management (1)
- Vulnerability Management (1)

## Limitations

- **Not legal advice:** Templates require review by qualified legal counsel
- **No compliance guarantee:** Policies support but don't certify compliance
- **Template-based only:** Uses existing templates, not custom authoring
- **No policy enforcement:** Generates documents only, doesn't implement controls
- **Static templates:** Based on SANS/CIS templates current as of 2023-2025
- **Professional review required:** Legal, compliance, and executive approval needed

## Requirements

- Claude Code (latest version recommended)
- Python 3.8+ (for automated tools)
- Python packages: `python-docx`, `markdown2`, `weasyprint`
- Git (for installation)

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Disclaimer

This tool generates policy documentation based on industry-standard templates. It does NOT replace professional legal or compliance advice. All generated policies must be reviewed by qualified legal counsel and approved by appropriate executives before implementation.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Support

- Issues: [GitHub Issues](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)
- Discussions: [GitHub Discussions](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)

## Data Sources

- **SANS Institute:** https://www.sans.org/security-resources/policies
- **CIS Controls:** https://www.cisecurity.org/insights/white-papers/cis-controls-policy-templates

---

**Last Updated:** 2025-10-19
**Author:** Diego Consolini <diego@diegocon.nl>
