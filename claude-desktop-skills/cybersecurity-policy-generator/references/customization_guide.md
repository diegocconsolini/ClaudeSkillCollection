# Policy Customization Guide

This guide explains how to customize the 51 policy templates for your organization using the Cybersecurity Policy Generator.

## Overview

All policy templates contain **placeholders** that must be replaced with your organization's specific information. This guide shows you what customizations are needed and how to apply them effectively.

## Common Placeholders

These placeholders appear across multiple policies:

| Placeholder | Replace With | Example |
|-------------|--------------|---------|
| `<Company Name>` | Your organization's legal name | "Acme Corporation" |
| `<YourCompanyName>` | Your organization's name | "Acme Corp" |
| `<ResponsibleCorporateOfficer>` | Title of responsible executive | "Chief Information Security Officer (CISO)" |
| `<Department>` | Responsible department | "Information Security Department" |
| `<Contact>` | Contact information | "security@acme.com" |
| `<Review Date>` | Policy review schedule | "Annually on January 1st" |
| `<Effective Date>` | When policy takes effect | "2025-11-01" |
| `<Version>` | Policy version number | "1.0" |

## Customization Questionnaire

The interactive questionnaire will ask you these questions:

### 1. Organization Information

**Company Name**
- **Question:** "What is your organization's legal name?"
- **Purpose:** Replaces `<Company Name>` and `<YourCompanyName>`
- **Example:** "Acme Corporation Inc."

**Industry Sector**
- **Question:** "What industry does your organization operate in?"
- **Options:** Technology, Finance, Healthcare, Government, Manufacturing, Retail, Other
- **Purpose:** May influence policy language and compliance requirements

**Organization Size**
- **Question:** "How many employees does your organization have?"
- **Options:** <50, 50-500, 500-1000, 1000+
- **Purpose:** Determines policy complexity and scope

### 2. Governance & Responsibility

**Responsible Officer**
- **Question:** "Who is the executive responsible for this policy?"
- **Purpose:** Replaces `<ResponsibleCorporateOfficer>`
- **Examples:**
  - "Chief Information Security Officer (CISO)"
  - "Chief Technology Officer (CTO)"
  - "Chief Risk Officer (CRO)"
  - "VP of Information Security"

**Responsible Department**
- **Question:** "Which department owns this policy?"
- **Purpose:** Replaces `<Department>`
- **Examples:**
  - "Information Security Department"
  - "IT Security Team"
  - "Risk Management Office"

**Contact Information**
- **Question:** "What is the contact email for policy questions?"
- **Purpose:** Replaces `<Contact>`
- **Example:** "security@acme.com" or "infosec@acme.com"

### 3. Policy Lifecycle

**Effective Date**
- **Question:** "When does this policy take effect?"
- **Purpose:** Replaces `<Effective Date>`
- **Format:** YYYY-MM-DD
- **Example:** "2025-11-01"

**Review Schedule**
- **Question:** "How often will this policy be reviewed?"
- **Options:**
  - Quarterly
  - Semi-annually
  - Annually
  - Bi-annually
  - As needed
- **Purpose:** Replaces `<Review Date>`
- **Example:** "Annually every January"

**Version Number**
- **Question:** "What version number is this policy?"
- **Purpose:** Replaces `<Version>`
- **Default:** "1.0" (for new policies)
- **Format:** Major.Minor (e.g., "1.0", "2.1", "3.0")

### 4. Compliance & Frameworks

**Required Frameworks**
- **Question:** "Which compliance frameworks must you meet?"
- **Options:** ISO 27001, SOC 2, NIST CSF, CIS Controls, GDPR, HIPAA, PCI-DSS
- **Purpose:** Ensures policy includes necessary controls
- **Multi-select:** Yes (can choose multiple)

**Regulatory Requirements**
- **Question:** "Are you subject to specific regulations?"
- **Options:** GDPR, HIPAA, PCI-DSS, SOX, GLBA, FERPA, None
- **Purpose:** Adds compliance-specific language

### 5. Policy-Specific Questions

Some policies require additional customization:

#### Access Control Policy
- **MFA Requirement:** "Is multi-factor authentication required?" (Yes/No)
- **Password Complexity:** "What are your password requirements?" (Standard/Strong/Custom)
- **Access Review Frequency:** "How often are access rights reviewed?" (Monthly/Quarterly/Annually)

#### Data Classification Policy
- **Classification Levels:** "How many data classification levels?" (3/4/5)
- **Retention Periods:** "Data retention requirements?" (Custom/Standard)

#### Incident Response Policy
- **Incident Response Team:** "Who is on your IR team?" (Names/roles)
- **Escalation Contacts:** "24/7 emergency contacts?" (Phone numbers)

#### Remote Access Policy
- **VPN Required:** "Is VPN mandatory for remote access?" (Yes/No)
- **Approved Devices:** "Personal devices allowed?" (Yes/No/BYOD policy)

## Step-by-Step Customization Process

### Step 1: Browse and Select Template

1. Run `browse_policies.py` to see available templates
2. Filter by category, framework, or search keyword
3. Select the policy that matches your needs
4. Review policy description and requirements

### Step 2: Answer Questionnaire

1. Run `questionnaire.py` with selected policy
2. Answer general questions (company name, officer, etc.)
3. Answer policy-specific questions
4. Review and confirm your answers

### Step 3: Customize Policy

1. Run `customize_policy.py` to apply customizations
2. Script replaces all placeholders with your answers
3. Review customized policy content
4. Make manual adjustments if needed

### Step 4: Generate Outputs

1. Run `generate_markdown.py` for .md file
2. Run `generate_docx_html_pdf.py` for other formats
3. Policies generated in all 4 formats

## Advanced Customization

### Adding Custom Sections

Some policies allow custom sections beyond the standard 8:

**Standard 8 Sections:**
1. Purpose
2. Scope
3. Policy Content
4. Compliance
5. Management Support
6. Review Schedule
7. Exceptions
8. Responsibility

**How to Add Custom Sections:**
- Edit `customized_policy.json` manually
- Add your section under `sections: { "customSection": "content" }`
- Regenerate outputs

### Industry-Specific Language

Adjust policy language for your industry:

**Healthcare (HIPAA):**
- Replace "data" with "protected health information (PHI)"
- Add HIPAA-specific requirements
- Reference HITECH Act provisions

**Finance (PCI-DSS, SOX):**
- Emphasize cardholder data protection
- Add financial controls language
- Reference regulatory examination requirements

**Government:**
- Add FedRAMP/FISMA language
- Reference NIST SP 800-53 controls
- Include clearance/classification requirements

### Multi-Location Organizations

For global organizations:

1. **Specify Jurisdictions:**
   - Add applicable laws (GDPR for EU, CCPA for California, etc.)
   - Include data residency requirements
   - Reference local data protection authorities

2. **Language Variations:**
   - Create policy versions in multiple languages
   - Ensure legal review in each jurisdiction
   - Maintain consistent meaning across translations

3. **Regional Customizations:**
   - Adjust for regional regulatory differences
   - Include region-specific contact information
   - Note jurisdictional exceptions

## Customization Examples

### Example 1: Small Tech Startup

**Organization:** ByteStart Inc. (30 employees, San Francisco)

**Customizations:**
- Company Name: "ByteStart Inc."
- Responsible Officer: "CTO"
- Industry: Technology
- Size: <50 employees
- Frameworks: SOC 2, ISO 27001 (for customers)
- Review: Annually
- Tone: Practical, implementation-focused

**Result:** Lightweight policies suitable for small team, focused on customer trust

### Example 2: Healthcare Provider

**Organization:** MedHealth Systems (500 employees, multi-state)

**Customizations:**
- Company Name: "MedHealth Systems LLC"
- Responsible Officer: "Chief Privacy Officer (CPO)"
- Industry: Healthcare
- Size: 500-1000 employees
- Frameworks: HIPAA, ISO 27001
- Regulations: HIPAA, HITECH Act
- Review: Annually (or when regulations change)
- Tone: Formal, compliance-focused

**Result:** HIPAA-compliant policies with PHI protections

### Example 3: Financial Institution

**Organization:** SecureBank (2000 employees, global)

**Customizations:**
- Company Name: "SecureBank International"
- Responsible Officer: "Chief Information Security Officer (CISO)"
- Industry: Finance
- Size: 1000+
- Frameworks: ISO 27001, SOC 2, PCI-DSS
- Regulations: GLBA, SOX, PCI-DSS, GDPR (EU operations)
- Review: Quarterly
- Tone: Formal, risk-focused

**Result:** Comprehensive policies meeting financial regulations

## Policy Approval Workflow

After customization, follow this approval process:

### 1. Internal Review
- Legal department review
- HR review (for employee policies)
- IT/Security review
- Business unit review (for operational impact)

### 2. Revisions
- Incorporate feedback
- Address legal concerns
- Adjust for operational feasibility
- Clarify ambiguous language

### 3. Management Approval
- Present to responsible officer
- Executive sign-off
- Board approval (if required)
- Document approval date

### 4. Communication
- Announce new/updated policy
- Provide training if needed
- Make policy accessible (intranet)
- Obtain employee acknowledgment

### 5. Enforcement
- Set effective date
- Monitor compliance
- Handle exceptions process
- Review violations

## Maintenance & Updates

### When to Update Policies

**Regulatory Changes:**
- New laws or regulations
- Updated compliance frameworks
- Industry standard revisions

**Organizational Changes:**
- Mergers/acquisitions
- New business lines
- Technology changes
- Organizational restructuring

**Security Events:**
- After major incidents
- Lessons learned implementation
- New threat landscapes
- Vulnerability discoveries

**Scheduled Reviews:**
- Follow review schedule (quarterly/annually)
- Stakeholder feedback
- Audit findings
- Best practice updates

### Version Control

**Versioning Scheme:**
- **Major version** (1.0 → 2.0): Significant policy changes, re-approval needed
- **Minor version** (1.0 → 1.1): Small updates, clarifications
- **Patch** (1.1 → 1.1.1): Typos, formatting only

**Change Log:**
- Document all changes
- Note reason for update
- Track approval dates
- Maintain old versions (for audit trail)

## Best Practices

### DO:
✓ Involve stakeholders early
✓ Use clear, unambiguous language
✓ Make policies actionable
✓ Include examples where helpful
✓ Keep policies current
✓ Document exceptions process
✓ Provide training on policies
✓ Make policies easily accessible
✓ Use consistent formatting

### DON'T:
✗ Copy policies without customization
✗ Create overly complex policies
✗ Ignore operational feasibility
✗ Skip legal review
✗ Set unrealistic requirements
✗ Use jargon without definitions
✗ Forget to communicate changes
✗ Neglect regular reviews

## Getting Help

### Common Issues

**Issue:** "Policy too technical for non-IT staff"
**Solution:** Add glossary, simplify language, provide examples

**Issue:** "Policy conflicts with business processes"
**Solution:** Involve business units in review, adjust for operations

**Issue:** "Too many policies to maintain"
**Solution:** Prioritize critical policies, consolidate where possible

**Issue:** "Policy not followed by employees"
**Solution:** Training, awareness, enforcement, leadership support

### Resources

- **Framework Documentation:**
  - ISO 27001: https://www.iso.org/standard/54534.html
  - CIS Controls: https://www.cisecurity.org/controls
  - NIST CSF: https://www.nist.gov/cyberframework

- **Compliance Resources:**
  - GDPR: https://gdpr-info.eu
  - HIPAA: https://www.hhs.gov/hipaa
  - PCI-DSS: https://www.pcisecuritystandards.org

- **Policy Templates:**
  - SANS: https://www.sans.org/security-resources/policies
  - CIS: https://www.cisecurity.org/insights/white-papers/cis-controls-policy-templates

---

**Last Updated:** 2025-10-19
**Version:** 1.0
**For:** Cybersecurity Policy Generator v1.0
