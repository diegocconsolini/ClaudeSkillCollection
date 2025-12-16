# Supply Chain Attack - Incident Response Playbook

**Organization**: Test Corp
**Industry**: General
**Generated**: 2025-10-21
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
**Supply Chain Attack**

### Description
Compromise through software supply chain including malicious dependencies, build pipeline injection, vendor compromise, or SBOM manipulation

### NIST Reference

Attacker compromising software supply chain through malicious code injection in dependencies, build systems, or third-party components (NIST SP 800-218, SP 800-161r1)


### Severity Level
**CRITICAL**

---

## Incident Classification

**Category**: supply-chain
**Severity**: CRITICAL

### NIST CSF 2.0 Alignment
This playbook aligns with the following NIST Cybersecurity Framework 2.0 Functions:
- **DETECT** (DE) - Finding and analyzing possible cybersecurity attacks
- **RESPOND** (RS) - Taking action regarding a detected incident
- **RECOVER** (RC) - Restoring impaired assets and operations

---

## Detection & Indicators

### Technical Indicators of Compromise


1. Unexpected dependencies in package manifests (package.json, requirements.txt)

2. Unauthorized modifications to build pipelines or CI/CD configurations

3. Anomalous outbound connections from build servers

4. SBOM integrity violations or hash mismatches

5. Malicious code in npm, PyPI, or other package repositories

6. Unsigned or improperly signed software artifacts

7. Unusual git commits or repository access patterns

8. Modified compiler or build tool binaries


### Behavioral Indicators


1. Reports of compromised vendor systems (e.g., SolarWinds-style incidents)

2. Unexpected software behavior after dependency updates

3. Build process slowdowns or anomalies

4. Developers reporting unfamiliar package installation prompts

5. Third-party security researchers identifying malicious packages


### Detection Activities

#### Continuous Monitoring (NIST CSF DE.CM)

- DE.CM-07: Monitor software composition and dependency changes

- DE.CM-08: Monitor build pipeline integrity and artifact signing

- DE.CM-01: Monitor network traffic from development and build systems

- DE.CM-09: Monitor version control systems for unauthorized commits

- SR-03: Monitor supply chain elements for threats and vulnerabilities


#### Adverse Event Analysis (NIST CSF DE.AE)

- DE.AE-02: Analyze dependency trees for malicious or suspicious packages

- DE.AE-03: Correlate SBOM data with threat intelligence

- DE.AE-04: Assess impact scope across all systems using affected components

- RS.AN-03: Analyze root cause of supply chain compromise

- SR-06: Evaluate provenance and pedigree of software components


---

## Response Procedures

### Phase 1: Triage & Assessment

**Objective**: Validate the incident and determine initial scope.

**Actions**:

- Validate supply chain compromise indicators

- Identify affected software components and their dependencies

- Determine compromise vector (dependency, build system, vendor)

- Assess scope of deployment across production systems


**Timeframe**: 0-15 minutes from detection

---

### Phase 2: Containment

**Objective**: Prevent incident spread and limit damage.

**Actions**:

- Isolate compromised build and development systems

- Halt automated deployments and CI/CD pipelines

- Block network communications to attacker infrastructure

- Quarantine affected software versions and artifacts

- Revoke signing keys and certificates if compromised

- Implement emergency vendor communication protocols


**Timeframe**: 15 minutes - 2 hours from detection

---

### Phase 3: Eradication

**Objective**: Remove the threat and eliminate vulnerabilities.

**Actions**:

- Remove malicious dependencies from package manifests

- Rebuild software from clean, verified source code

- Restore build pipelines from known-good configurations

- Update SBOM with verified component versions

- Implement dependency pinning and hash verification

- Patch exploited vulnerabilities in build infrastructure


**Timeframe**: 2-24 hours from detection

---

## Recovery Actions

**Objective**: Restore normal operations while maintaining security.

### Recovery Procedures


1. Deploy verified, clean software versions to production

2. Implement enhanced dependency scanning and verification

3. Establish software provenance tracking (SSDF PS.3.1)

4. Conduct security review of all third-party components

5. Implement multi-party code review for critical changes

6. Deploy SBOM generation and verification tools


### Validation Steps

Before declaring incident resolved:
- [ ] Verify all malicious activity has ceased
- [ ] Confirm all affected systems are clean and operational
- [ ] Validate backup integrity (if used for recovery)
- [ ] Review logs for any remaining suspicious activity
- [ ] Implement enhanced monitoring for supply chain attack indicators

---

## Communication Requirements

### Internal Communications

**Required Notifications**:

- Development teams

- DevOps/SRE

- Security Operations

- Executive leadership

- Legal


**Communication Frequency**: Every 4 hours during active incident, daily during recovery

**Primary Contact**: security@organization.com
**Emergency Hotline**: (555) 123-4567

---

### External Communications


**Required Notifications**:

- Affected vendors and suppliers

- Open source maintainers

- CISA (if federal)

- Downstream customers



---

### Public Communications


**May Be Required**:

- Security advisory if customers affected

- CVE publication if applicable


**Approval Required**: Legal & Executive Leadership
**Coordinated By**: Communications/PR Team


---

## Compliance Considerations

### GDPR Requirements


**Notification Required**: If customer data compromised via supply chain


**Article 33 - Supervisory Authority Notification**:
Timeline: 72 hours if personal data breach confirmed

**Article 34 - Data Subject Notification**:
Required: If high risk to individuals from compromised software


**Risk Factors**:

- Scope of software deployment

- Data access by compromised components

- Potential for data exfiltration



---

### HIPAA Requirements


**Breach Determination**: If PHI accessible by compromised software components

**Notification Timeline**: 60 days if PHI exposure confirmed

**Risk Assessment Factors**:

- PHI processing by affected software

- Evidence of data access

- Duration of compromise



---

## Roles & Responsibilities

### Incident Response Team Structure


- **Incident Commander**:  Overall supply chain incident coordination

- **Software Engineering**:  Code review and rebuild from clean sources

- **DevSecOps**:  Pipeline security and artifact verification

- **Vendor Management**:  Third-party coordination and assessment

- **Legal/Compliance**:  Regulatory obligations and customer notifications


### Escalation Criteria

**Escalate to Executive Leadership if**:
- Incident severity is CRITICAL
- Data breach affects >500 individuals
- Regulatory notification required
- Media inquiries received
- Estimated recovery time >24 hours

---

## Contact Information

### Test Corp Security Team

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
| 1.0 | 2025-10-21 | Auto-generated | Initial playbook creation |

### References

- NIST SP 800-61r3 - Computer Security Incident Handling Guide (April 2025)
- NIST Cybersecurity Framework 2.0
- GDPR Articles 33-34 (if applicable)
- HIPAA Breach Notification Rule (if applicable)

---

**END OF PLAYBOOK**

*This playbook is a living document and should be reviewed and updated regularly based on lessons learned, organizational changes, and evolving threats.*

*Generated by Incident Response Playbook Creator v2.0.0*
*2025-10-21 23:22:46*