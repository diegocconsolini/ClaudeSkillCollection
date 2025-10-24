# Security & Compliance Skills Catalog
## Prioritized by Value and Feasibility

**Version:** 2.0
**Last Updated:** 2025-10-18
**Based On:** Document generation paradigm analysis

---

## 🥇 TIER 1: Perfect Fit - Build First

These align perfectly with how Claude skills work: pure document generation from templates.

### 1. Privacy Policy Generator (`privacy_policy`)

**What It Generates:**
- privacy_policy.docx (comprehensive policy)
- cookie_policy.html (cookie consent text)
- privacy_notice.pdf (concise version)
- children_privacy.docx (COPPA/kids provisions)

**Value Proposition:**
- Saves 20+ hours of legal drafting
- Covers GDPR, CCPA, LGPD, PIPEDA, COPPA
- Multi-jurisdiction in single document
- Updates easily when regulations change

**How It Works:**
1. Questionnaire about company, data types, jurisdictions
2. Template selection based on answers
3. Clause assembly with jurisdiction-specific language
4. Format generation in multiple outputs

**Why It's Tier 1:**
- Every company needs this
- Highly templatable (proven clause libraries exist)
- Clear input/output workflow
- Massive time savings
- Universal demand

**Components Needed:**
- Template library for each jurisdiction
- Clause database with mappings
- HTML/DOCX/PDF formatters
- Questionnaire engine

**Estimated Development:** 3-4 weeks

---

### 2. Security Policy Suite Generator (`security_policies`)

**What It Generates:**
20+ policy documents including:
- Information Security Policy (main)
- Acceptable Use Policy
- Access Control Policy
- Incident Response Policy
- Data Classification Policy
- Business Continuity Policy
- Vendor Management Policy
- Change Management Policy
- Backup & Recovery Policy
- Physical Security Policy
- ... and 10 more

**Value Proposition:**
- Saves 40+ hours of policy writing
- Ensures consistency across all policies
- Maps to ISO 27001, NIST, SOC 2
- Professional formatting with approval workflows

**How It Works:**
1. Organization profile questionnaire (industry, size, controls)
2. Load appropriate templates for industry
3. Map controls to policies (ISO 27001 → policy sections)
4. Generate complete policy suite
5. Create approval tracking sheet

**Why It's Tier 1:**
- Highest time savings (40+ hours)
- Required for certifications
- Extremely templatable
- High demand from compliance teams

**Components Needed:**
- 20+ policy templates
- ISO 27001/NIST control mappings
- Industry-specific variations (healthcare, finance, tech)
- Approval workflow templates

**Estimated Development:** 4-5 weeks

---

### 3. Vendor Assessment Report Builder (`vendor_assessment`)

**What It Generates:**
- vendor_questionnaire.xlsx (SIG Lite, CAIQ, custom)
- assessment_report.docx (scoring and findings)
- risk_matrix.xlsx (risk ratings by category)
- executive_summary.pdf (for leadership)
- remediation_plan.docx (required actions)

**Value Proposition:**
- Saves 15+ hours per vendor assessment
- Standardizes vendor risk evaluation
- Creates audit-ready documentation
- Tracks remediation progress

**How It Works:**
1. Vendor type selection (cloud, SaaS, managed services, etc.)
2. Questionnaire generation (SIG, CAIQ, or custom)
3. User completes questionnaire (outside skill)
4. Import responses, calculate scores
5. Generate reports with findings and recommendations

**Why It's Tier 1:**
- Every company assesses vendors
- Highly structured and repeatable
- Clear scoring methodologies
- Professional report formats

**Components Needed:**
- SIG Lite/Full questionnaire templates
- CAIQ (Consensus Assessments) question bank
- Scoring algorithms by domain
- Risk matrix generators
- Report templates

**Estimated Development:** 3-4 weeks

---

## 🥈 TIER 2: Good Fit - Build Next

These work well as skills but need careful scoping to focus on document generation.

### 4. Data Processing Agreement Builder (`dpa_builder`)

**What It Generates:**
- dpa_main.docx (main agreement)
- schedule_processing_activities.xlsx (data inventory)
- schedule_technical_measures.docx (security controls)
- schedule_subprocessors.xlsx (subprocessor list)
- schedule_international_transfers.docx (transfer mechanisms)

**Value Proposition:**
- Saves 12+ hours per DPA
- Ensures GDPR Article 28 compliance
- Standard Contractual Clauses (SCCs) included
- Coordinates with privacy policies

**How It Works:**
1. Party details (controller, processor, subprocessors)
2. Processing details (purposes, data types, retention)
3. SCC selection (EU/UK/Swiss)
4. Technical measures from security assessment
5. Generate complete DPA package

**Why It's Tier 2:**
- Requires coordination of multiple documents
- Complex legal clauses need expert review
- Different SCCs for different transfers

**Estimated Development:** 3 weeks

---

### 5. PIA/DPIA Document Generator (`pia_generator`)

**What It Generates:**
- pia_document.docx (complete assessment)
- risk_register.xlsx (identified risks)
- mitigation_plan.docx (risk treatment)
- executive_summary.pdf (for leadership)

**Value Proposition:**
- Saves 10+ hours per assessment
- Required by GDPR Article 35
- Structures complex assessment process
- Documents compliance evidence

**How It Works:**
1. Processing activity description
2. Necessity and proportionality assessment
3. Risk identification questionnaire
4. Mitigation measure documentation
5. Generate complete DPIA

**Why It's Tier 2:**
- Requires significant user input/judgment
- Risk assessment is subjective
- Must be clear it's a template, not the actual assessment

**Estimated Development:** 2-3 weeks

---

### 6. Incident Response Playbook Creator (`incident_playbook`)

**What It Generates:**
- playbook_main.docx (complete runbook)
- quick_reference.pdf (laminated card format)
- contact_list.xlsx (escalation matrix)
- scenario_checklist.docx (per scenario)
- communication_templates.docx (notifications)

**Value Proposition:**
- Saves 15+ hours of procedure documentation
- Covers ransomware, breach, DDoS, insider threats
- Battle-tested procedures
- Ready for tabletop exercises

**How It Works:**
1. Organization structure (team roles, contacts)
2. Scenario selection (which incidents to cover)
3. Tool inventory (SIEM, ticketing, communication)
4. Regulatory requirements (notification timelines)
5. Generate complete playbook

**Why It's Tier 2:**
- Needs significant customization per org
- Procedures vary by industry
- Must integrate with existing tools

**Estimated Development:** 3 weeks

---

### 7. Breach Notification Letter Generator (`breach_letters`)

**What It Generates:**
- customer_notice.docx (individual notification)
- regulator_notice.docx (supervisory authority)
- media_statement.pdf (public communication)
- internal_communication.docx (employee notice)
- timeline.xlsx (notification tracking)

**Value Proposition:**
- Saves 5+ hours during crisis
- Time-critical compliance requirement
- Multiple audience templates
- Jurisdiction-specific requirements

**How It Works:**
1. Breach details (what, when, how many affected)
2. Jurisdiction (GDPR 72h, state laws vary)
3. Audience selection (individuals, regulators, media)
4. Generate appropriate letters
5. Track notification completion

**Why It's Tier 2:**
- Time-sensitive use case
- Requires crisis-time clarity
- Multiple jurisdictions with different rules

**Estimated Development:** 2 weeks

---

### 8. Cookie Banner Code Generator (`cookie_banner`)

**What It Generates:**
- cookie_banner.html (banner markup)
- cookie_banner.js (consent logic)
- cookie_banner.css (styling)
- cookie_policy.html (linked policy)
- implementation_guide.md (developer instructions)

**Value Proposition:**
- Saves 3-5 hours of implementation
- GDPR/ePrivacy compliant by default
- Multiple design options
- Integrates with analytics

**How It Works:**
1. Website details (URL, branding colors)
2. Cookie inventory (what cookies are used)
3. Design selection (modal, banner, corner)
4. Integration points (Google Analytics, Facebook Pixel, etc.)
5. Generate complete implementation

**Why It's Tier 2:**
- Technical implementation (code generation)
- Requires testing on actual site
- Integration complexity varies

**Estimated Development:** 2 weeks

---

### 9. Data Retention Schedule Creator (`retention_schedule`)

**What It Generates:**
- retention_policy.docx (policy document)
- retention_schedule.xlsx (data inventory with retention periods)
- deletion_procedures.docx (how to delete)
- legal_hold_process.docx (preservation procedures)

**Value Proposition:**
- Saves 8+ hours of research
- Maps regulations to retention periods
- Coordinates with backup policies
- Audit-ready documentation

**How It Works:**
1. Data inventory (what data exists)
2. Jurisdiction mapping (which laws apply)
3. Purpose mapping (why data is kept)
4. Generate retention matrix
5. Create deletion procedures

**Why It's Tier 2:**
- Complex regulatory landscape
- Must coordinate multiple requirements
- Industry-specific rules

**Estimated Development:** 2-3 weeks

---

### 10. Evidence Pack Builder (`evidence_pack`)

**What It Generates:**
- evidence_index.xlsx (inventory)
- cover_sheet.docx (per evidence item)
- audit_package.zip (complete package)
- gaps_report.docx (missing evidence)

**Value Proposition:**
- Saves 5+ hours of organization
- Audit-ready presentation
- Tracks evidence collection
- Professional formatting

**How It Works:**
1. Evidence inventory (what exists)
2. Requirement mapping (what's needed)
3. Gap identification (what's missing)
4. Organization and formatting
5. Generate complete package

**Why It's Tier 2:**
- Depends on existing evidence
- Organizational task more than generation
- Value is in organization, not creation

**Estimated Development:** 2 weeks

---

## ❌ NOT SUITABLE as Claude Skills

These require capabilities beyond document generation:

### Requires Live Scanning/Analysis:
- ❌ GDPR Compliance Auditor (needs to scan actual systems)
- ❌ Cookie Compliance Scanner (needs to analyze websites)
- ❌ Security Configuration Auditor (needs system access)
- ❌ Vulnerability Scanner (needs network access)
- ❌ Code Security Analyzer (needs to parse code)

### Requires External APIs/Services:
- ❌ Threat Intelligence Reporter (needs threat feeds)
- ❌ Dark Web Monitor (needs external data sources)
- ❌ Supply Chain Risk Analyzer (needs vendor databases)
- ❌ CVE Lookup Service (just API wrapper)

### Too Simple (Just Lookups):
- ❌ Encryption Standards Advisor (just a decision tree)
- ❌ Regulation Finder (just search)
- ❌ Compliance Calendar (just dates)
- ❌ Control Framework Mapper (simple mapping)

### Too Complex/Subjective:
- ❌ Risk Assessment Calculator (requires context-specific judgment)
- ❌ Security Maturity Scorer (needs organizational assessment)
- ❌ Zero Trust Planner (too organization-specific)
- ❌ Threat Model Generator (requires architecture analysis)

---

## Development Priority Roadmap

### Phase 1: Foundation (Q1 2026)
**Goal:** Establish core document generation capabilities

1. **Privacy Policy Generator** (4 weeks)
   - Universal need, highest demand
   - Clear templates from legal sources
   - Multiple jurisdictions

2. **Security Policy Suite** (5 weeks)
   - Highest time savings
   - Required for certifications
   - Template library exists

3. **Vendor Assessment Builder** (4 weeks)
   - Standardized questionnaires
   - Clear scoring methodology
   - High demand

**Total:** 13 weeks (Q1 2026)

### Phase 2: Compliance Essentials (Q2 2026)
**Goal:** Cover regulatory requirements

4. **DPA Builder** (3 weeks)
   - Coordinates with privacy policies
   - SCCs integration

5. **PIA/DPIA Generator** (3 weeks)
   - GDPR requirement
   - Assessment structure

6. **Incident Response Playbook** (3 weeks)
   - Crisis preparedness
   - Procedural templates

**Total:** 9 weeks (Q2 2026)

### Phase 3: Specialized Tools (Q3 2026)
**Goal:** Niche but valuable capabilities

7. **Breach Notification Letters** (2 weeks)
   - Crisis response
   - Multiple audiences

8. **Cookie Banner Generator** (2 weeks)
   - Technical implementation
   - Compliance by default

9. **Retention Schedule Creator** (3 weeks)
   - Regulatory complexity
   - Multi-jurisdiction

10. **Evidence Pack Builder** (2 weeks)
    - Audit preparation
    - Organization tool

**Total:** 9 weeks (Q3 2026)

---

## Skill Value Matrix

```
Time Savings (Hours)
    ^
 40 |  [Security Policy Suite]
    |
 30 |
    |
 20 |  [Privacy Policy]
    |
 15 |  [Vendor Assessment]  [Incident Playbook]
    |
 10 |  [DPA Builder]        [DPIA Generator]
    |  [Retention Schedule]
  5 |  [Breach Letters]     [Evidence Pack]
    |  [Cookie Banner]
    |
    +-------------------------------------------->
    Low                Complexity              High
    Templates          Custom Logic Required
```

---

## Success Metrics by Skill

### Privacy Policy Generator
- [ ] Covers 5+ jurisdictions (GDPR, CCPA, LGPD, PIPEDA, COPPA)
- [ ] Generates 3+ document formats
- [ ] < 10 minutes to complete questionnaire
- [ ] Professional legal review completed

### Security Policy Suite
- [ ] 20+ policy documents
- [ ] Maps to 3+ frameworks (ISO 27001, NIST, SOC 2)
- [ ] Industry variations (3+ industries)
- [ ] Consistent formatting across all docs

### Vendor Assessment Builder
- [ ] 3+ questionnaire types (SIG, CAIQ, custom)
- [ ] Automated scoring by domain
- [ ] Risk matrix generation
- [ ] Remediation tracking

### [Similar metrics for each skill...]

---

## Expansion Opportunities

Once core skills are established:

### International Versions
- Add more jurisdictions (APAC, LATAM, Middle East)
- Translate templates to local languages
- Local legal expert review

### Industry Specializations
- Healthcare (HIPAA, HITECH)
- Financial (PCI DSS, GLBA, SOX)
- Education (FERPA)
- Government (FedRAMP, FISMA)

### Framework Coverage
- Expand beyond ISO 27001
- Add NIST CSF, CIS Controls
- Include industry frameworks (HITRUST, PCI)

### Integration Skills
- Coordinate multiple skills
- Master document generator
- Policy/procedure linking

---

## Community Contribution Model

To scale beyond 10 skills:

1. **Template Marketplace**
   - Users contribute templates
   - Legal experts review
   - Community ratings

2. **Industry Packs**
   - Healthcare compliance suite
   - Financial services suite
   - SaaS company essentials

3. **Jurisdiction Packs**
   - EU compliance bundle
   - US state laws bundle
   - APAC compliance bundle

---

## Version History

- **v1.0** - Initial skill list
- **v2.0** - Prioritized based on document generation paradigm

---

## Next Steps

1. **Choose first skill:** Privacy Policy Generator
2. **Gather templates:** Collect legal-reviewed templates
3. **Build questionnaire:** Design comprehensive input system
4. **Develop generator:** Script following skill patterns
5. **Test thoroughly:** Multiple scenarios and jurisdictions
6. **Document completely:** SKILL.md, examples, tests
7. **Release:** v1.0.0 of first skill

---

**Current Status:** Planning complete, ready to build
**Recommended First Skill:** Privacy Policy Generator
**Estimated Time to First Release:** 4 weeks
