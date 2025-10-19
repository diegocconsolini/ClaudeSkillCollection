# Phishing / Business Email Compromise - Incident Response Playbook

**Organization**: Finance Inc
**Industry**: Finance
**Generated**: 2025-10-20
**Version**: 1.0
**Classification**: CONFIDENTIAL

---

## Table of Contents

1. [Overview](#overview)
2. [Incident Classification](#incident-classification)
3. [Detection & Indicators](#detection--indicators)
4. [Response Procedures](#response-procedures)
5. [Recovery Actions](#recovery-actions)
6. [Communication Requirements](#communication-requirements)
7. [Compliance Considerations](#compliance-considerations)
8. [Roles & Responsibilities](#roles--responsibilities)
9. [Contact Information](#contact-information)

---

## Overview

### Incident Type
**Phishing / Business Email Compromise**

### Description
Email-based attack to compromise credentials or conduct fraud

### NIST Reference

Attacker sending phishing emails to harvest credentials or conduct wire fraud


### Severity Level
**HIGH**

---

## Incident Classification

**Category**: social-engineering
**Severity**: HIGH

### NIST CSF 2.0 Alignment
This playbook aligns with the following NIST Cybersecurity Framework 2.0 Functions:
- **DETECT** (DE) - Finding and analyzing possible cybersecurity attacks
- **RESPOND** (RS) - Taking action regarding a detected incident
- **RECOVER** (RC) - Restoring impaired assets and operations

---

## Detection & Indicators

### Technical Indicators of Compromise


1. Emails from spoofed domains

2. Suspicious links or attachments

3. Multiple failed login attempts followed by success

4. Email forwarding rules created


### Behavioral Indicators


1. Users reporting suspicious emails

2. Unexpected password reset requests

3. Unusual wire transfer requests

4. Complaints of unauthorized email sends


### Detection Activities

#### Continuous Monitoring (NIST CSF DE.CM)

- DE.CM-03: Monitor email gateway for phishing indicators

- DE.CM-01: Monitor for credential harvesting attempts


#### Adverse Event Analysis (NIST CSF DE.AE)

- DE.AE-02: Analyze reported phishing emails

- DE.AE-03: Correlate with authentication logs


---

## Response Procedures

### Phase 1: Triage & Assessment

**Objective**: Validate the incident and determine initial scope.

**Actions**:

- Validate phishing report

- Identify number of recipients and clickers


**Timeframe**: 0-15 minutes from detection

---

### Phase 2: Containment

**Objective**: Prevent incident spread and limit damage.

**Actions**:

- Remove phishing emails from all mailboxes

- Block sender domains and malicious URLs

- Reset credentials for affected accounts


**Timeframe**: 15 minutes - 2 hours from detection

---

### Phase 3: Eradication

**Objective**: Remove the threat and eliminate vulnerabilities.

**Actions**:

- Remove email forwarding rules

- Revoke OAuth tokens if applicable

- Update email filtering rules


**Timeframe**: 2-24 hours from detection

---

## Recovery Actions

**Objective**: Restore normal operations while maintaining security.

### Recovery Procedures


1. Restore normal email operations

2. Conduct user awareness training

3. Implement MFA if not already in place


### Validation Steps

Before declaring incident resolved:
- [ ] Verify all malicious activity has ceased
- [ ] Confirm all affected systems are clean and operational
- [ ] Validate backup integrity (if used for recovery)
- [ ] Review logs for any remaining suspicious activity
- [ ] Implement enhanced monitoring for phishing / business email compromise indicators

---

## Communication Requirements

### Internal Communications

**Required Notifications**:

- All users - phishing warning

- IT team

- Management


**Communication Frequency**: Every 4 hours during active incident, daily during recovery

**Primary Contact**: security@organization.com
**Emergency Hotline**: (555) 123-4567

---

### External Communications


**Required Notifications**:

- Law enforcement if fraud occurred



---

### Public Communications


**May Be Required**:

- Customer notification if credentials exposed


**Approval Required**: Legal & Executive Leadership
**Coordinated By**: Communications/PR Team


---

## Compliance Considerations

### GDPR Requirements


**Notification Required**: If credentials compromised and personal data accessed


**Article 33 - Supervisory Authority Notification**:
Timeline: 72 hours if breach confirmed

**Article 34 - Data Subject Notification**:
Required: Depends on data accessed


**Risk Factors**:

- Email account contents

- Credential exposure



---

### HIPAA Requirements


**Breach Determination**: If PHI in compromised email accounts

**Notification Timeline**: 60 days if breach confirmed

**Risk Assessment Factors**:

- Email account purpose

- PHI volume in emails



---

## Roles & Responsibilities

### Incident Response Team Structure


- **IT Security**:  Email removal and account security

- **Identity Management**:  Credential resets

- **HR**:  User awareness training

- **Finance**:  Transaction verification if BEC


### Escalation Criteria

**Escalate to Executive Leadership if**:
- Incident severity is CRITICAL
- Data breach affects >500 individuals
- Regulatory notification required
- Media inquiries received
- Estimated recovery time >24 hours

---

## Contact Information

### Finance Inc Security Team

**Primary Contact**: security@organization.com
**Emergency Hotline**: (555) 123-4567
**Available**: 24/7 for critical incidents

### External Resources

**Law Enforcement**:
- FBI Cyber Division: https://www.fbi.gov/investigate/cyber
- IC3 (Internet Crime Complaint Center): https://www.ic3.gov

**Incident Reporting**:
- US-CERT: https://www.cisa.gov/report
- CERT/CC: cert@cert.org

**Data Protection Authorities** (if applicable):
- GDPR: [Your supervisory authority]
- State AG: [If US-based]

---

## Post-Incident Activities

### Lessons Learned Meeting

**Schedule**: Within 5 business days of incident resolution
**Attendees**: Incident response team, affected department leads, management
**Duration**: 90-120 minutes

**Agenda**:
1. Timeline review (detection to resolution)
2. What went well
3. What needs improvement
4. Root cause analysis
5. Action items with owners and deadlines

### Documentation Requirements

- [ ] Complete incident timeline
- [ ] Technical findings and forensic evidence
- [ ] Communication logs (internal and external)
- [ ] Regulatory notifications (if applicable)
- [ ] Post-incident report with lessons learned
- [ ] Updated playbook based on experience

---

## Appendix

### Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-20 | Auto-generated | Initial playbook creation |

### References

- NIST SP 800-61r3 - Computer Security Incident Handling Guide (April 2025)
- NIST Cybersecurity Framework 2.0
- GDPR Articles 33-34 (if applicable)
- HIPAA Breach Notification Rule (if applicable)

---

**END OF PLAYBOOK**

*This playbook is a living document and should be reviewed and updated regularly based on lessons learned, organizational changes, and evolving threats.*

*Generated by Incident Response Playbook Creator v1.0.0*
*2025-10-20 00:14:29*