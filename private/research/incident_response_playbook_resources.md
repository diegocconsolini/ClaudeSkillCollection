# Incident Response Playbook Creator - Resource Guide

## 📚 Authoritative Sources & Templates

---

## 🏛️ Government & Standards Organizations

### NIST (National Institute of Standards and Technology)
**Primary Resource: NIST SP 800-61 Rev 2**
- **URL**: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf
- **What it provides**:
  - Complete incident response lifecycle
  - Incident categorization and prioritization
  - Communication guidelines
  - Escalation procedures
  - Post-incident activities
- **Templates you can extract**:
  - Incident classification matrix
  - Response team structure
  - Communication flow charts
  - Evidence collection procedures

### CISA (Cybersecurity & Infrastructure Security Agency)
**Federal Government Cybersecurity Incident Response Playbooks**
- **URL**: https://www.cisa.gov/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks
- **What it provides**:
  - Federal incident response playbook
  - Vulnerability response playbook
  - Coordination procedures
- **Templates you can extract**:
  - Severity classification
  - Role definitions
  - Decision trees
  - Notification timelines

### ENISA (European Union Agency for Cybersecurity)
**Good Practice Guide for Incident Management**
- **URL**: https://www.enisa.europa.eu/publications/good-practice-guide-for-incident-management
- **What it provides**:
  - European perspective on incident response
  - GDPR-aligned breach notification
  - Cross-border incident handling
- **Templates you can extract**:
  - GDPR breach notification templates
  - EU-specific escalation procedures
  - Data breach assessment forms

### ISO/IEC Standards
**ISO/IEC 27035 - Information Security Incident Management**
- **What it provides**:
  - International standard for incident management
  - Structured approach to planning and operations
  - Incident response team organization
- **Templates you can extract**:
  - Incident response policy template
  - Incident classification scheme
  - Response procedures

---

## 🔒 Industry-Specific Frameworks

### SANS Institute
**Incident Handler's Handbook**
- **URL**: https://www.sans.org/white-papers/33901/
- **What it provides**:
  - 6-step incident response process
  - Detailed technical procedures
  - Tool recommendations
- **Templates you can extract**:
  - Technical investigation checklists
  - Evidence collection forms
  - Chain of custody templates

**SANS Incident Response Plan Template**
- **URL**: https://www.sans.org/information-security-policy/
- **What it provides**:
  - Customizable IR plan template
  - Policy templates
  - Communication templates

### Carnegie Mellon - CERT
**CERT Resilience Management Model**
- **URL**: https://resources.sei.cmu.edu/library/
- **What it provides**:
  - Incident management capability model
  - Process improvement guidance
  - Metrics and measurements
- **Templates you can extract**:
  - Capability assessment templates
  - Process documentation
  - Performance metrics

---

## 📋 Scenario-Specific Playbook Sources

### Ransomware Response
**CISA Ransomware Guide**
- **URL**: https://www.cisa.gov/stopransomware/ransomware-guide
- **Components**:
  - Prevention checklist
  - Response checklist
  - Recovery procedures
  - Communication templates

**Microsoft Ransomware Response Playbook**
- **Documentation**: Microsoft Security Documentation
- **Components**:
  - Detection procedures
  - Containment strategies
  - Recovery steps
  - Decision tree for payment

### Data Breach Response
**Privacy Rights Clearinghouse**
- **URL**: https://privacyrights.org/data-breaches
- **Components**:
  - Breach notification templates
  - State-specific requirements (US)
  - Timeline requirements
  - Sample notification letters

**ICO (UK) Personal Data Breach Guidance**
- **URL**: https://ico.org.uk/for-organisations/guide-to-data-protection/
- **Components**:
  - GDPR breach assessment
  - 72-hour notification templates
  - Risk assessment framework
  - Communication templates

### DDoS Response
**Cloudflare DDoS Response Guide**
- **Documentation**: Cloudflare Learning Center
- **Components**:
  - Attack identification
  - Mitigation strategies
  - Communication during attacks
  - Post-attack analysis

**AWS DDoS Resiliency Playbook**
- **Documentation**: AWS Best Practices for DDoS Resiliency
- **Components**:
  - Architecture patterns
  - Response procedures
  - AWS-specific tools
  - Escalation to AWS

### Insider Threat Response
**CISA Insider Threat Mitigation Guide**
- **URL**: https://www.cisa.gov/insider-threat-mitigation
- **Components**:
  - Detection indicators
  - Investigation procedures
  - HR coordination
  - Legal considerations

---

## 📞 Communication Template Sources

### Breach Notification Templates
**State Attorney General Offices** (US)
- Many states provide template breach notification letters
- Examples: California, New York, Massachusetts AGs

**IAPP (International Association of Privacy Professionals)**
- **Resources**: Template library for members
- **Components**:
  - Multi-jurisdiction templates
  - Regulatory notification forms
  - Customer notification letters
  - Media statements

### Internal Communication Templates
**NIST SP 800-61 Appendices**
- Incident reporting forms
- Status update templates
- Executive briefing formats
- Technical report templates

### Stakeholder Communication
**SEC Cybersecurity Disclosure Guidelines**
- **For public companies**:
  - 8-K filing templates
  - Material incident disclosure
  - Board communication templates

---

## 📊 Escalation Matrix Sources

### Severity Classification
**Common Vulnerability Scoring System (CVSS)**
- **URL**: https://www.first.org/cvss/
- **Use for**: Technical severity ratings
- **Mapping**: CVSS scores to response levels

**Business Impact Analysis Templates**
- **Source**: BCI (Business Continuity Institute)
- **Components**:
  - Impact categories
  - Time-based escalation
  - Business function priorities

### Escalation Procedures
**ITIL Service Management**
- **Framework**: ITIL 4
- **Components**:
  - Hierarchical escalation
  - Functional escalation
  - Escalation timelines
  - RACI matrices

---

## 🛠️ Ready-to-Use Template Collections

### GitHub Repositories
**Awesome Incident Response**
- **URL**: https://github.com/meirwah/awesome-incident-response
- **Contains**: Curated list of IR tools and resources

**IR Playbook Collection**
- **URL**: https://github.com/certsocietegenerale/IRM
- **Contains**: Multiple scenario playbooks

**Incident Response Plan Template**
- **URL**: https://github.com/counteractive/incident-response-plan-template
- **Contains**: Markdown-based IR plan template

### Commercial Sources (Free Resources)
**CrowdStrike Services Cyber Front Lines**
- Incident response best practices
- Real-world playbooks
- Tabletop exercise scenarios

**Mandiant (Google Cloud) Resources**
- M-Trends reports with IR statistics
- Playbook examples
- APT response procedures

---

## 📐 Template Structure for Your Skill

### Base Playbook Structure
```yaml
playbook:
  metadata:
    name: "Incident Type"
    severity_levels: [Critical, High, Medium, Low]
    regulatory_requirements: [GDPR, CCPA, HIPAA]
    
  phases:
    detection:
      - indicators
      - alert_sources
      - initial_assessment
      
    containment:
      - immediate_actions
      - short_term_containment
      - system_isolation
      
    eradication:
      - root_cause_analysis
      - removal_procedures
      - system_hardening
      
    recovery:
      - system_restoration
      - monitoring_enhanced
      - normal_operations
      
    post_incident:
      - lessons_learned
      - documentation
      - process_improvements
      
  communications:
    internal:
      - incident_team
      - management
      - affected_departments
      
    external:
      - customers
      - regulators
      - media
      - law_enforcement
      
  escalation:
    triggers:
      - time_based
      - impact_based
      - regulatory_required
    
    levels:
      - L1_response_team
      - L2_management
      - L3_executive
      - L4_board
```

---

## 🔄 Maintenance & Updates

### Regular Update Sources
1. **US-CERT/CISA Alerts** - New threat playbooks
2. **ENISA Publications** - European guidelines
3. **FIRST.org** - Global incident response community
4. **SANS Internet Storm Center** - Current threat intelligence
5. **Verizon DBIR** - Annual incident statistics

### Regulatory Update Sources
1. **Privacy law databases** (IAPP)
2. **State AG offices** (breach notification changes)
3. **EU data protection authorities**
4. **Industry regulators** (HIPAA, PCI DSS, etc.)

---

## 💡 Implementation Tips for Your Skill

### Document Generation Approach
1. **Create modular templates** - Mix and match sections
2. **Use decision trees** - Guide playbook customization
3. **Include placeholders** - Company-specific information
4. **Version control** - Track template updates
5. **Format flexibility** - DOCX, PDF, Markdown, HTML

### Key Components to Include
```python
# Core template library structure
templates/
├── scenarios/
│   ├── ransomware/
│   │   ├── detection.yaml
│   │   ├── containment.yaml
│   │   ├── recovery.yaml
│   │   └── communications.yaml
│   ├── data_breach/
│   ├── ddos/
│   ├── malware/
│   ├── insider_threat/
│   └── supply_chain/
├── communications/
│   ├── internal/
│   │   ├── initial_alert.md
│   │   ├── status_update.md
│   │   └── all_clear.md
│   ├── customer/
│   ├── regulatory/
│   └── media/
├── escalation/
│   ├── matrices/
│   ├── contact_lists/
│   └── decision_trees/
└── tools/
    ├── checklists/
    ├── forms/
    └── logs/
```

### Customization Parameters
```python
playbook_config = {
    "organization": {
        "size": ["small", "medium", "large", "enterprise"],
        "industry": ["finance", "healthcare", "retail", "technology"],
        "geography": ["US", "EU", "global"],
        "regulations": ["GDPR", "CCPA", "HIPAA", "PCI-DSS"]
    },
    "capabilities": {
        "soc": ["none", "basic", "24x7", "advanced"],
        "forensics": ["none", "basic", "advanced"],
        "legal": ["none", "on-call", "in-house"],
        "pr": ["none", "on-call", "in-house"]
    },
    "scenarios": {
        "priority": ["ransomware", "data_breach", "ddos"],
        "likelihood": ["high", "medium", "low"],
        "impact": ["critical", "high", "medium", "low"]
    }
}
```

---

## 📚 Additional Reading

### Books
- "Incident Response & Computer Forensics" - Luttgens, Pepe, Mandia
- "Applied Incident Response" - Steve Anson
- "Intelligence-Driven Incident Response" - Bianco & Ouellette
- "Crafting the InfoSec Playbook" - Bollinger, Enright, Valites

### Industry Reports
- Verizon Data Breach Investigations Report (Annual)
- IBM Cost of a Data Breach Report (Annual)
- Mandiant M-Trends (Annual)
- CrowdStrike Global Threat Report (Annual)

### Training & Certifications
- SANS FOR508: Advanced Incident Response
- GIAC Certified Incident Handler (GCIH)
- Certified Computer Security Incident Handler (CSIH)
- ISACA Cybersecurity Incident Response

---

## ✅ Validation Checklist

When building your playbook templates, ensure they include:
- [ ] Clear role definitions (RACI matrix)
- [ ] Time-based escalation triggers
- [ ] Regulatory notification requirements
- [ ] Evidence collection procedures
- [ ] Communication templates for all stakeholders
- [ ] Technical containment procedures
- [ ] Business continuity considerations
- [ ] Legal and HR coordination points
- [ ] Post-incident review process
- [ ] Metrics and success criteria