# Incident Response Playbook Creator

**Version**: 1.0.0
**Category**: Security
**Author**: Diego Consolini

---

## Overview

This skill generates comprehensive, customized incident response playbooks based on authoritative templates from **NIST SP 800-61r3** (April 2025) and **CISA** guidance. It creates professional, ready-to-use playbooks for 8 different incident scenarios with built-in GDPR and HIPAA compliance considerations.

### What This Skill Does

- ✅ Generates complete incident response playbooks in Markdown format
- ✅ Includes detection indicators, response procedures, recovery actions, and communication templates
- ✅ Incorporates NIST CSF 2.0 alignment and compliance requirements (GDPR, HIPAA)
- ✅ Customizes playbooks for specific organizations and industries
- ✅ Provides role-based responsibilities and escalation procedures
- ✅ Based on 100% real, authoritative content (no mock data)

### Available Incident Scenarios

1. **Ransomware Attack** (Critical)
2. **Data Breach / Exfiltration** (Critical)
3. **Phishing / Business Email Compromise** (High)

---

## When to Use This Skill

This skill should be activated when the user:

- Asks to create an incident response playbook
- Mentions they need IR documentation or procedures
- Asks about incident response for specific scenarios (ransomware, data breach, phishing, DDoS, etc.)
- Wants to prepare for security incidents
- Needs compliance-aligned incident response procedures
- Asks about NIST SP 800-61 or CISA incident response guidance

**Example Triggers**:
- "Create an incident response playbook for ransomware"
- "I need IR procedures for data breaches"
- "Generate incident response documentation"
- "Help me prepare for a phishing attack"

---

## How to Use This Skill

### Step 1: Browse Available Scenarios (Optional)

First, you can show the user what scenarios are available:

```bash
python3 scripts/browse_scenarios.py --list
```

This displays all available incident types with descriptions, severity levels, and compliance flags.

For detailed information about a specific scenario:

```bash
python3 scripts/browse_scenarios.py --detail ransomware
```

### Step 2: Collect Organization Information

Use the **AskUserQuestion** tool to collect the required information from the user. This provides a beautiful, user-friendly interface for gathering customization details.

**IMPORTANT**: Always use AskUserQuestion for gathering this information. Do NOT just ask in text.

#### Question 1: Incident Scenario Selection

```python
AskUserQuestion(questions=[
    {
        "question": "Which incident scenario do you need a playbook for?",
        "header": "Scenario",
        "multiSelect": false,
        "options": [
            {
                "label": "Ransomware Attack",
                "description": "Malware that encrypts files and demands payment for decryption. Critical severity."
            },
            {
                "label": "Data Breach / Exfiltration",
                "description": "Unauthorized access and theft of sensitive data. Critical severity with GDPR/HIPAA implications."
            },
            {
                "label": "Phishing / BEC",
                "description": "Email-based social engineering attacks to compromise credentials or conduct fraud. High severity."
            }
        ]
    }
])
```

#### Question 2: Organization Information

```python
AskUserQuestion(questions=[
    {
        "question": "What is your organization name?",
        "header": "Organization",
        "multiSelect": false,
        "options": [
            {
                "label": "Provide name",
                "description": "Enter your organization's name for the playbook"
            }
        ]
    },
    {
        "question": "What industry sector are you in?",
        "header": "Industry",
        "multiSelect": false,
        "options": [
            {
                "label": "Healthcare",
                "description": "Medical, hospitals, healthcare providers (HIPAA applicable)"
            },
            {
                "label": "Finance",
                "description": "Banks, financial services, payment processing"
            },
            {
                "label": "Technology",
                "description": "Software, SaaS, IT services"
            },
            {
                "label": "Retail/E-commerce",
                "description": "Online/offline retail, customer data"
            },
            {
                "label": "Government",
                "description": "Public sector, government agencies"
            },
            {
                "label": "Education",
                "description": "Schools, universities, educational institutions"
            }
        ]
    }
])
```

#### Question 3: Contact Information (Optional)

```python
AskUserQuestion(questions=[
    {
        "question": "Do you want to customize contact information in the playbook?",
        "header": "Contacts",
        "multiSelect": false,
        "options": [
            {
                "label": "Use defaults",
                "description": "Use placeholder contact information (you can edit later)"
            },
            {
                "label": "Provide custom",
                "description": "Enter your security team email and phone number"
            }
        ]
    }
])
```

### Step 3: Generate the Playbook

After collecting the information, use the generate_playbook_markdown.py script to create the playbook.

**Basic Command**:
```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario <scenario_id> \
  --org "<Organization Name>" \
  --industry "<Industry>"
```

**With Custom Contact Info**:
```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "Acme Corporation" \
  --industry "Technology" \
  --contact-email "security@acmecorp.com" \
  --contact-phone "+1-555-SEC-RITY" \
  --output output/acme-ransomware-playbook.md
```

**Scenario ID Mapping**:
- "Ransomware Attack" → `ransomware`
- "Data Breach / Exfiltration" → `data_breach`
- "Phishing / BEC" → `phishing`

### Step 4: Present the Results

After generation, you should:

1. **Confirm successful generation**: Show the user that the playbook was created successfully
2. **Show the file location**: Tell them where the file was saved
3. **Offer to display content**: Ask if they want to see the playbook content
4. **Suggest next steps**:
   - Review and customize the playbook for their specific environment
   - Share with their security team
   - Test the playbook with a tabletop exercise
   - Generate additional scenario playbooks

**Example Response**:
```
✅ Successfully generated Ransomware Attack playbook for Acme Corporation!

📄 **Output**: output/ransomware-playbook.md (7.2 KB)

The playbook includes:
- Detection indicators and monitoring guidance
- Step-by-step response procedures (Triage → Containment → Eradication)
- Recovery actions with validation checklist
- GDPR and HIPAA compliance considerations
- Communication requirements and templates
- Role-based responsibilities
- Contact information and escalation criteria

Would you like me to:
1. Display the playbook content
2. Generate a playbook for another incident type
3. Explain any section in detail
```

---

## Complete Workflow Example

Here's a complete interaction flow:

### 1. User Request
**User**: "I need an incident response playbook for ransomware attacks"

### 2. Scenario Browsing (Optional)
**You**: Let me show you the ransomware scenario details first.

```bash
python3 scripts/browse_scenarios.py --detail ransomware
```

**You**: This scenario includes [summarize key points from output]

### 3. Information Collection (Required)
**You**: I'll help you generate a custom playbook. Let me gather some information about your organization.

```python
# Use AskUserQuestion for organization name and industry
AskUserQuestion(questions=[...])
```

### 4. Playbook Generation
```bash
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "User's Organization" \
  --industry "User's Industry"
```

### 5. Results Presentation
**You**: ✅ Successfully generated your ransomware playbook!

[Show file location and summary of what's included]

### 6. Follow-up
**You**: Would you like me to:
- Generate playbooks for other incident types?
- Explain any section in detail?
- Show you how to use the playbook in a real incident?

---

## Important Notes

### Data Quality & Sources

All content in generated playbooks comes from authoritative sources:
- **NIST SP 800-61r3** (April 2025) - Primary incident response framework
- **NIST Cybersecurity Framework 2.0** - Function and category alignment
- **GDPR** (Articles 33-34) - EU data breach notification requirements
- **HIPAA** Breach Notification Rule - Healthcare breach requirements

**No mock or fake data** - Everything is extracted from real guidance documents.

### Compliance Disclaimers

Always remind users:
- ⚠️ These playbooks are templates and should be reviewed by legal counsel
- ⚠️ Compliance requirements vary by jurisdiction - verify with local regulations
- ⚠️ Playbooks should be customized for specific organizational needs
- ⚠️ Regular testing and updates are essential

### Limitations

- Currently supports 3 scenarios (simplified version for testing)
- Full version with 8 scenarios available but has JSON formatting issues (being fixed)
- Generated playbooks are in Markdown format only (not Word/PDF yet)
- Does not include automated translation or localization

---

## Script Reference

### browse_scenarios.py

**Purpose**: Explore available incident scenarios and view detailed information

**Usage**:
```bash
# List all scenarios
python3 scripts/browse_scenarios.py --list

# Show detailed view
python3 scripts/browse_scenarios.py --detail ransomware

# Display metadata
python3 scripts/browse_scenarios.py --metadata

# Search scenarios
python3 scripts/browse_scenarios.py --search "data breach"
```

### generate_playbook_markdown.py

**Purpose**: Generate customized incident response playbooks

**Usage**:
```bash
# Generate playbook with required parameters
python3 scripts/generate_playbook_markdown.py \
  --scenario <scenario_id> \
  --org "<Organization Name>" \
  [--industry "<Industry>"] \
  [--contact-email "<email>"] \
  [--contact-phone "<phone>"] \
  [--output "<path>"]

# List available scenarios
python3 scripts/generate_playbook_markdown.py --list
```

**Required Parameters**:
- `--scenario` or `-s`: Scenario ID (ransomware, data_breach, phishing)
- `--org` or `-o`: Organization name

**Optional Parameters**:
- `--industry` or `-i`: Industry sector (default: "General")
- `--contact-email`: Security team email (default: security@organization.com)
- `--contact-phone`: Security team phone (default: (555) 123-4567)
- `--output`: Output file path (default: output/[scenario]-playbook.md)

---

## Troubleshooting

### Common Issues

**Issue**: "Scenario not found"
**Solution**: Use `--list` to see available scenario IDs

**Issue**: "Required file not found"
**Solution**: Ensure you're running from the plugin directory, or use `--scenarios-file` to specify path

**Issue**: "Invalid JSON"
**Solution**: The script defaults to using `incident_scenarios_simplified.json` which is validated

---

## Future Enhancements

Planned features for future versions:
- All 8 incident scenarios (DDoS, Malware, Cloud Breach, Supply Chain, AI/ML)
- Multi-format export (Word .docx, PDF, HTML)
- Excel contact roster generation
- Playbook versioning and change tracking
- Tabletop exercise scenario generation
- Integration with ticketing systems

---

**END OF SKILL DOCUMENTATION**

*For questions or issues, refer to the README.md or contact the plugin author.*
