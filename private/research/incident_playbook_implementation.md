# Incident Response Playbook Creator - Implementation Guide

## 🚀 From Resources to Working Skill

---

## Step 1: Extract Core Templates from Sources

### A. NIST-Based Foundation Structure
```python
# Extract from NIST SP 800-61 Rev 2
base_playbook_structure = {
    "1_preparation": {
        "team_contacts": [],
        "tools_required": [],
        "access_credentials": [],
        "communication_channels": []
    },
    "2_detection_analysis": {
        "indicators": [],
        "triage_questions": [],
        "initial_assessment": [],
        "severity_determination": []
    },
    "3_containment_eradication_recovery": {
        "short_term_containment": [],
        "evidence_gathering": [],
        "long_term_containment": [],
        "eradication_steps": [],
        "recovery_procedures": []
    },
    "4_post_incident": {
        "lessons_learned_meeting": [],
        "report_template": [],
        "improvement_actions": []
    }
}
```

### B. Scenario-Specific Templates

#### Ransomware Playbook (from CISA Guide)
```yaml
ransomware_playbook:
  detection_indicators:
    - "Files with unusual extensions (.locked, .encrypted)"
    - "Ransom notes in directories"
    - "Inability to open files"
    - "System performance degradation"
    
  immediate_actions:
    - "Isolate affected systems from network"
    - "Disable automated maintenance tasks"
    - "Photograph ransom message"
    - "Preserve logs and memory dumps"
    
  decision_points:
    backup_availability:
      yes: "Proceed to recovery from backup"
      no: "Evaluate decryption options"
    
    critical_systems:
      yes: "Escalate to Crisis Management Team"
      no: "Standard incident response"
    
  communications:
    internal:
      t+0: "Alert incident response team"
      t+15min: "Notify IT management"
      t+1hr: "Brief executive team if critical"
      
    external:
      law_enforcement: "FBI IC3 or local FBI field office"
      cyber_insurance: "Within 24 hours"
      customers: "If service disruption > 4 hours"
```

#### Data Breach Playbook (from GDPR/CCPA requirements)
```yaml
data_breach_playbook:
  initial_assessment:
    questions:
      - "What type of data was exposed?"
      - "How many records affected?"
      - "When did the breach occur?"
      - "How was it discovered?"
      - "Is the breach ongoing?"
    
  regulatory_timelines:
    GDPR:
      supervisory_authority: "72 hours"
      data_subjects: "Without undue delay"
      documentation: "Mandatory regardless of notification"
      
    CCPA:
      attorney_general: "Without unreasonable delay"
      consumers: "Without unreasonable delay"
      threshold: "> 500 California residents"
    
  risk_assessment:
    high_risk_factors:
      - "Sensitive data categories"
      - "Large volume of records"
      - "Vulnerable individuals affected"
      - "Data not encrypted"
```

---

## Step 2: Build the Document Generation Engine

### Core Generator Script Structure
```python
class IncidentPlaybookGenerator:
    def __init__(self):
        self.templates = self.load_templates()
        self.scenarios = ['ransomware', 'data_breach', 'ddos', 
                         'insider_threat', 'supply_chain', 'malware']
        
    def generate_playbook(self, config):
        """
        config = {
            'organization': 'ACME Corp',
            'industry': 'healthcare',
            'size': 'medium',
            'scenarios': ['ransomware', 'data_breach'],
            'regulations': ['HIPAA', 'GDPR'],
            'contact_info': {...},
            'tools_available': [...]
        }
        """
        playbook = Document()
        
        # Add title page
        playbook.add_title_page(config['organization'])
        
        # Add table of contents
        playbook.add_table_of_contents()
        
        # Generate scenario-specific playbooks
        for scenario in config['scenarios']:
            section = self.generate_scenario_section(scenario, config)
            playbook.add_section(section)
        
        # Add communication templates
        comms = self.generate_communication_section(config)
        playbook.add_section(comms)
        
        # Add escalation matrix
        escalation = self.generate_escalation_matrix(config)
        playbook.add_section(escalation)
        
        # Add appendices
        appendices = self.generate_appendices(config)
        playbook.add_section(appendices)
        
        return playbook
```

---

## Step 3: Create the Questionnaire System

### Interactive Configuration Builder
```python
def run_playbook_questionnaire():
    """Guides user through playbook customization"""
    
    config = {}
    
    # Organization Details
    print("=== ORGANIZATION DETAILS ===")
    config['org_name'] = input("Organization name: ")
    config['industry'] = select_from_list([
        'Healthcare', 'Financial', 'Retail', 'Technology', 
        'Government', 'Education', 'Manufacturing', 'Other'
    ])
    config['size'] = select_from_list([
        'Small (1-50)', 'Medium (51-500)', 
        'Large (501-5000)', 'Enterprise (5000+)'
    ])
    
    # Regulatory Requirements
    print("\n=== REGULATORY REQUIREMENTS ===")
    config['regulations'] = select_multiple([
        'GDPR', 'CCPA/CPRA', 'HIPAA', 'PCI-DSS', 
        'SOX', 'FERPA', 'GLBA', 'None'
    ])
    
    # Incident Scenarios
    print("\n=== INCIDENT SCENARIOS TO INCLUDE ===")
    config['scenarios'] = select_multiple([
        'Ransomware Attack',
        'Data Breach',
        'DDoS Attack',
        'Insider Threat',
        'Supply Chain Compromise',
        'Malware Infection',
        'Physical Security Breach',
        'Cloud Security Incident'
    ])
    
    # Team Structure
    print("\n=== INCIDENT RESPONSE TEAM ===")
    config['has_soc'] = yes_no("Do you have a Security Operations Center?")
    config['has_legal'] = yes_no("Do you have in-house legal counsel?")
    config['has_pr'] = yes_no("Do you have a PR/Communications team?")
    
    # Contact Information
    print("\n=== KEY CONTACTS ===")
    config['contacts'] = gather_contacts()
    
    # Tools and Resources
    print("\n=== AVAILABLE TOOLS ===")
    config['tools'] = select_multiple([
        'SIEM (Splunk/QRadar/etc)',
        'EDR (CrowdStrike/SentinelOne/etc)',
        'Forensics Tools',
        'Backup Systems',
        'Ticketing System',
        'Communication Platform'
    ])
    
    return config
```

---

## Step 4: Template Library Structure

### File Organization
```
incident_playbook_skill/
├── SKILL.md
├── templates/
│   ├── base/
│   │   ├── title_page.docx
│   │   ├── table_of_contents.docx
│   │   └── revision_history.docx
│   │
│   ├── scenarios/
│   │   ├── ransomware/
│   │   │   ├── playbook.yaml
│   │   │   ├── flowchart.xml
│   │   │   └── checklist.md
│   │   ├── data_breach/
│   │   │   ├── playbook.yaml
│   │   │   ├── assessment_form.docx
│   │   │   └── timeline.xlsx
│   │   └── [other scenarios]/
│   │
│   ├── communications/
│   │   ├── internal/
│   │   │   ├── initial_alert.md
│   │   │   ├── status_update.md
│   │   │   └── post_incident.md
│   │   ├── customer/
│   │   │   ├── breach_notification_gdpr.md
│   │   │   ├── breach_notification_ccpa.md
│   │   │   └── service_disruption.md
│   │   ├── regulatory/
│   │   │   ├── gdpr_72hr.docx
│   │   │   ├── hipaa_breach.docx
│   │   │   └── state_ag_notice.docx
│   │   └── media/
│   │       ├── press_release.md
│   │       └── holding_statement.md
│   │
│   ├── escalation/
│   │   ├── severity_matrix.yaml
│   │   ├── escalation_triggers.yaml
│   │   └── contact_tree.yaml
│   │
│   └── appendices/
│       ├── evidence_log.xlsx
│       ├── chain_of_custody.docx
│       ├── lessons_learned.docx
│       └── regulatory_requirements.xlsx
│
├── scripts/
│   ├── generator.py
│   ├── questionnaire.py
│   ├── formatter.py
│   └── validator.py
│
└── examples/
    ├── healthcare_playbook.docx
    ├── financial_playbook.docx
    └── tech_startup_playbook.docx
```

---

## Step 5: Sample Generated Output

### Example: Ransomware Playbook Section
```markdown
# 3. RANSOMWARE INCIDENT RESPONSE PLAYBOOK

## 3.1 Activation Criteria
This playbook is activated when any of the following indicators are observed:
- Files encrypted with unusual extensions
- Ransom notes appearing on systems
- Multiple users reporting inability to access files
- Detection of known ransomware signatures by security tools

## 3.2 Initial Response (0-15 minutes)
**Incident Commander**: [Name from config]
**Primary Contact**: [Phone from config]

### Immediate Actions Checklist:
- [ ] Isolate affected systems from network
- [ ] Take photographs of ransom messages
- [ ] Disable automated maintenance tasks
- [ ] Begin documentation in incident log
- [ ] Notify incident response team via [Slack/Teams]

## 3.3 Containment (15-60 minutes)
### Short-term Containment:
1. Disconnect affected systems from network
2. Disable wireless/Bluetooth on affected systems
3. Block identified malicious IPs/domains at firewall
4. Reset credentials for potentially compromised accounts

### Evidence Collection:
- [ ] Capture memory dump
- [ ] Export system/security logs
- [ ] Document ransom note details
- [ ] Screenshot encrypted file examples

## 3.4 Escalation Matrix
| Time | Impact | Escalate To | Contact |
|------|--------|-------------|---------|
| T+0 | Any | Security Team Lead | [Contact] |
| T+15min | >10 systems | IT Director | [Contact] |
| T+30min | Critical systems | CISO | [Contact] |
| T+1hr | Customer impact | CEO | [Contact] |

## 3.5 Communication Templates

### Internal Alert (T+0):
Subject: [URGENT] Potential Ransomware Incident Detected

Team,
We have detected indicators of ransomware on [system/network segment].
Immediate response team is investigating. 

DO NOT:
- Restart affected computers
- Connect USB drives to any systems
- Open suspicious emails

Updates will follow every 30 minutes.

### Customer Notification (If Required):
[Template customized based on impact and regulations]
```

---

## Step 6: Quick Reference Generator

### Generate One-Page Quick Reference
```python
def generate_quick_reference(config):
    """Creates a one-page PDF with critical information"""
    
    quick_ref = {
        "INCIDENT HOTLINE": config['hotline'],
        
        "IMMEDIATE ACTIONS": [
            "1. Assess severity",
            "2. Contain the incident", 
            "3. Preserve evidence",
            "4. Notify incident commander"
        ],
        
        "KEY CONTACTS": {
            "Incident Commander": config['contacts']['commander'],
            "Legal Counsel": config['contacts']['legal'],
            "PR Team": config['contacts']['pr'],
            "Cyber Insurance": config['contacts']['insurance']
        },
        
        "ESCALATION TRIGGERS": [
            "Customer data exposed → Legal + PR",
            "Service down >1hr → Executive team",
            "Ransomware detected → Law enforcement",
            "Media inquiry → PR team only responds"
        ],
        
        "REGULATORY DEADLINES": {
            "GDPR": "72 hours to supervisory authority",
            "CCPA": "Without unreasonable delay",
            "HIPAA": "60 days to affected individuals"
        },
        
        "EVIDENCE PRESERVATION": [
            "DO: Photograph screens, Save logs, Document timeline",
            "DON'T: Shutdown systems, Delete files, Share on social"
        ]
    }
    
    return create_pdf_quickref(quick_ref)
```

---

## Step 7: Contact List Generator

### Generate Excel Contact Matrix
```python
def generate_contact_matrix(config):
    """Creates structured contact list in Excel"""
    
    workbook = create_workbook()
    
    # Internal Contacts Sheet
    internal = workbook.add_sheet('Internal Contacts')
    internal.add_headers(['Role', 'Name', 'Primary Phone', 
                          'After Hours', 'Email', 'Escalation Level'])
    
    for contact in config['internal_contacts']:
        internal.add_row(contact)
    
    # External Contacts Sheet  
    external = workbook.add_sheet('External Contacts')
    external.add_headers(['Organization', 'Purpose', 'Phone', 
                          'Email', 'Account #', 'Notes'])
    
    external.add_rows([
        ['FBI IC3', 'Ransomware', '1-800-CALL-FBI', 'ic3.gov', '', ''],
        ['Cyber Insurance', 'Claims', config['insurance_phone'], '', '', ''],
        ['Outside Counsel', 'Legal', config['legal_phone'], '', '', ''],
        # ... more contacts
    ])
    
    # Vendor Contacts Sheet
    vendors = workbook.add_sheet('Critical Vendors')
    # ... add vendor contacts
    
    return workbook
```

---

## Step 8: Implementation Checklist

### For Building This Skill:
- [ ] Extract templates from NIST, CISA, ENISA sources
- [ ] Create YAML scenario definitions for each incident type  
- [ ] Build questionnaire flow for gathering requirements
- [ ] Develop document assembly engine
- [ ] Create communication template library
- [ ] Build escalation matrix generator
- [ ] Add regulatory timeline calculator
- [ ] Generate quick reference cards
- [ ] Create contact list manager
- [ ] Test with multiple organization profiles
- [ ] Include example outputs
- [ ] Write comprehensive SKILL.md documentation

---

## 🎯 Final Deliverables

When complete, your skill will generate:

1. **Comprehensive Playbook (DOCX)**
   - 50-150 pages depending on scenarios
   - Fully customized to organization
   - Professional formatting
   - Table of contents and cross-references

2. **Quick Reference Card (PDF)**
   - 1-2 page emergency response guide
   - Laminate-ready format
   - Critical contacts and actions

3. **Contact Matrix (XLSX)**
   - Internal response team
   - External resources
   - Vendor contacts
   - Regulatory authorities

4. **Communication Templates (DOCX/HTML)**
   - Pre-drafted notifications
   - Variable placeholders
   - Multiple formats

5. **Supporting Documents**
   - Evidence collection forms
   - Chain of custody templates
   - Lessons learned templates
   - Tabletop exercise scenarios