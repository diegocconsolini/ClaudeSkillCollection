# Incident Response Playbook Creator - Quick Start Guide

## 🎯 Executive Summary

Build a Claude skill that generates comprehensive, customized incident response playbooks from authoritative templates and best practices. This skill transforms complex compliance requirements into actionable, organization-specific documentation.

---

## 📌 Top 5 Essential Sources to Start With

### 1. **NIST SP 800-61 Rev 2** (Foundation)
- **Download**: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf
- **Extract**: Complete incident response lifecycle, team structures, communication flows
- **Pages to focus on**: 21-35 (Handling an Incident), Appendix A (Recommendations)

### 2. **CISA Ransomware Guide** (Scenario Template)
- **Access**: https://www.cisa.gov/stopransomware/ransomware-guide
- **Extract**: Detection indicators, containment steps, recovery procedures
- **Key sections**: Ransomware Response Checklist, Best Practices

### 3. **GDPR Breach Notification** (Regulatory Requirements)
- **Source**: European Data Protection Board Guidelines
- **Extract**: 72-hour timeline, risk assessment criteria, notification templates
- **Focus**: Articles 33-34, WP250 guidelines

### 4. **SANS Incident Forms** (Templates)
- **Access**: https://www.sans.org/information-security-policy/
- **Extract**: Incident report forms, chain of custody, communication templates
- **Download**: Incident Response Plan template

### 5. **GitHub IR Templates** (Ready-to-Use)
- **Repository**: https://github.com/counteractive/incident-response-plan-template
- **Extract**: Markdown-based templates, complete IR plan structure
- **Fork**: Use as base for your skill templates

---

## 🚀 7-Day Development Sprint

### Day 1-2: Extract Core Templates
```bash
# Create skill structure
mkdir incident-playbook-creator
cd incident-playbook-creator
mkdir -p templates/{scenarios,communications,escalation}
mkdir -p scripts examples tests

# Download and extract NIST templates
wget https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf
# Extract key sections into YAML templates

# Clone GitHub templates
git clone https://github.com/counteractive/incident-response-plan-template temp/
# Extract and adapt templates
```

### Day 3-4: Build Generator Engine
```python
# scripts/generator.py
class PlaybookGenerator:
    def __init__(self):
        self.templates = TemplateLoader()
        self.formatter = DocumentFormatter()
    
    def generate(self, config):
        playbook = self.build_playbook(config)
        return self.formatter.export(playbook, formats=['docx', 'pdf', 'md'])
```

### Day 5: Create Questionnaire System
```python
# scripts/questionnaire.py
def incident_response_questionnaire():
    return {
        'org_info': gather_organization_details(),
        'regulations': select_applicable_regulations(),
        'scenarios': choose_incident_scenarios(),
        'team': define_response_team(),
        'tools': list_available_tools()
    }
```

### Day 6: Build Output Formatters
```python
# scripts/formatter.py
class DocumentFormatter:
    def to_docx(self, playbook):
        # Generate professional Word document
    
    def to_pdf(self, playbook):
        # Create PDF with TOC and cross-references
    
    def to_xlsx(self, contacts):
        # Excel contact matrix
```

### Day 7: Test and Package
```bash
# Create example outputs
python scripts/generator.py --config examples/healthcare.yaml
python scripts/generator.py --config examples/financial.yaml

# Write documentation
echo "# Incident Response Playbook Creator" > SKILL.md
# Add complete skill documentation

# Package for distribution
tar -czf incident-playbook-creator.tar.gz .
```

---

## 📦 Minimal Viable Skill Structure

```yaml
incident-playbook-skill/
├── SKILL.md                      # Core skill definition
├── scripts/
│   └── generator.py              # Main generation script
├── templates/
│   ├── scenarios/
│   │   └── ransomware.yaml      # Start with one scenario
│   ├── communications/
│   │   └── breach_notice.md     # Basic notification
│   └── escalation/
│       └── matrix.yaml           # Simple escalation
└── examples/
    └── sample_playbook.docx      # One complete example
```

---

## 💡 Key Implementation Tips

### 1. Start Simple
- Begin with ONE scenario (ransomware)
- Create ONE regulation (GDPR)
- Build ONE output format (DOCX)
- Then expand incrementally

### 2. Use Existing Wheels
```python
# Don't build from scratch
from python_docx import Document  # Document generation
from jinja2 import Template       # Template engine
import yaml                       # Configuration
import pandas as pd              # Contact matrices
```

### 3. Template Variables Strategy
```yaml
# templates/scenarios/ransomware.yaml
detection:
  alert: "Ransomware detected on {{affected_systems}}"
  escalate_if: "{{critical_systems}} affected"
  notify: "{{incident_commander_name}} at {{incident_commander_phone}}"
```

### 4. Compliance Mapping
```python
REGULATORY_REQUIREMENTS = {
    'GDPR': {
        'breach_notification': '72 hours',
        'authority': 'Supervisory Authority',
        'template': 'gdpr_breach_notice.docx'
    },
    'CCPA': {
        'breach_notification': 'without unreasonable delay',
        'authority': 'California AG',
        'template': 'ccpa_breach_notice.docx'
    }
}
```

---

## 🎯 Quick Wins for MVP

### Phase 1 (MVP - Week 1)
✅ One scenario (Ransomware)
✅ Basic questionnaire (5 questions)
✅ Simple Word document output
✅ One communication template
✅ Basic escalation matrix

### Phase 2 (Enhanced - Week 2)
➕ Data breach scenario
➕ GDPR/CCPA compliance
➕ PDF quick reference
➕ Contact Excel sheet
➕ Multiple communications

### Phase 3 (Complete - Week 3)
➕ All major scenarios
➕ Industry customization
➕ Full regulatory coverage
➕ Tabletop exercises
➕ Metrics and reporting

---

## 📚 Additional Resources

### Free Template Sources
- **SANS Reading Room**: https://www.sans.org/white-papers/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **ENISA Publications**: https://www.enisa.europa.eu/publications
- **CISA Resources**: https://www.cisa.gov/resources-tools/resources

### Community Resources
- **r/blueteamsec**: Reddit community for defensive security
- **FIRST.org**: Forum of Incident Response Teams
- **ISACA Templates**: Available to members

### Commercial Resources (Free Sections)
- **Gartner**: Incident Response Planning Guide (exec summary free)
- **MITRE ATT&CK**: Attack patterns for playbooks
- **IBM X-Force**: Threat intelligence for scenarios

---

## ✅ Success Criteria

Your skill is ready when it can:
1. Generate a 50+ page customized playbook in < 2 minutes
2. Cover 5+ incident scenarios
3. Include regulatory compliance for 3+ frameworks
4. Provide templates in 3+ formats (DOCX, PDF, XLSX)
5. Pass review by a security professional

---

## 🚀 Get Started Now

```bash
# Quick start commands
mkdir incident-playbook-creator
cd incident-playbook-creator

# Download this guide and resources
curl -O [resource-urls]

# Create initial structure
python3 << EOF
import os
dirs = ['templates/scenarios', 'templates/communications', 
        'scripts', 'examples', 'tests']
for d in dirs:
    os.makedirs(d, exist_ok=True)
EOF

# Start with the simplest template
echo "# Ransomware Response" > templates/scenarios/ransomware.md

# Begin coding
touch scripts/generator.py
```

---

## 💬 Community Support

Share your progress and get help:
- **GitHub Issues**: Create issue on your repo for community input
- **Security Communities**: Share in relevant Slack/Discord servers
- **LinkedIn**: Connect with incident response professionals

Remember: This skill provides **massive value** by encoding expert knowledge into reusable templates. Every organization needs this, and you're making it accessible!