# Cybersecurity Framework Mappings

This document maps the 51 policy templates to major cybersecurity and compliance frameworks.

## Framework Coverage Overview

| Framework | Policies Covered | Description |
|-----------|-----------------|-------------|
| **ISO 27001** | 51 (100%) | International standard for information security management |
| **SOC 2** | 36 (71%) | Service Organization Control - Trust Service Criteria |
| **NIST** | 36 (71%) | NIST Cybersecurity Framework and SP 800-53 |
| **CIS Controls v8** | 15 (29%) | Center for Internet Security Critical Security Controls |
| **NIST CSF** | 15 (29%) | NIST Cybersecurity Framework |
| **GDPR** | 3 (6%) | EU General Data Protection Regulation |

## Framework Descriptions

### ISO 27001
**Full Name:** ISO/IEC 27001:2013 - Information Security Management Systems

**Purpose:** International standard that specifies requirements for establishing, implementing, maintaining and continually improving an information security management system (ISMS).

**Applicability:** All 51 policy templates support ISO 27001 compliance. This framework is globally recognized and suitable for organizations of all sizes and industries.

**Key Controls Covered:**
- A.5: Information Security Policies
- A.6: Organization of Information Security
- A.7: Human Resource Security
- A.8: Asset Management
- A.9: Access Control
- A.10: Cryptography
- A.11: Physical and Environmental Security
- A.12: Operations Security
- A.13: Communications Security
- A.14: System Acquisition, Development and Maintenance
- A.15: Supplier Relationships
- A.16: Information Security Incident Management
- A.17: Information Security Aspects of Business Continuity Management
- A.18: Compliance

### SOC 2
**Full Name:** Service Organization Control 2 - Trust Service Criteria

**Purpose:** Audit framework for service providers storing customer data in the cloud, focused on security, availability, processing integrity, confidentiality, and privacy.

**Applicability:** 36 policies (primarily SANS templates) map to SOC 2 requirements. Critical for SaaS companies and cloud service providers.

**Trust Service Criteria:**
- **Security** (Common Criteria) - All 36 policies
- **Availability** - Data Recovery, Business Continuity policies
- **Processing Integrity** - Change Management, Configuration Management policies
- **Confidentiality** - Data Classification, Encryption policies
- **Privacy** - Privacy Management, Data Protection policies

### NIST Cybersecurity Framework (CSF)
**Full Name:** Framework for Improving Critical Infrastructure Cybersecurity

**Purpose:** Risk-based approach to managing cybersecurity risk, organized into five core functions: Identify, Protect, Detect, Respond, Recover.

**Applicability:** 15 policies (CIS templates) specifically map to NIST CSF. Additional 21 SANS policies support NIST SP 800-53 controls.

**Five Functions Mapping:**
- **Identify:** Asset Management, Risk Assessment policies
- **Protect:** Access Control, Data Protection, Training policies
- **Detect:** Logging and Monitoring, Audit policies
- **Respond:** Incident Response Management policy
- **Recover:** Data Recovery, Business Continuity policies

### CIS Controls v8
**Full Name:** Center for Internet Security Critical Security Controls Version 8

**Purpose:** Prioritized set of actions to protect organizations from cyber attacks, organized into 18 critical security controls.

**Applicability:** 15 policies (all CIS templates) directly implement CIS Controls. Suitable for organizations following CIS Implementation Groups (IG1, IG2, IG3).

**18 CIS Controls Covered:**
1. Inventory and Control of Enterprise Assets
2. Inventory and Control of Software Assets
3. Data Protection
4. Secure Configuration of Enterprise Assets and Software
5. Account Management
6. Access Control Management
7. Continuous Vulnerability Management
8. Audit Log Management
9. Email and Web Browser Protections
10. Malware Defenses
11. Data Recovery
12. Network Infrastructure Management
13. Network Monitoring and Defense
14. Security Awareness and Skills Training
15. Service Provider Management
16. Application Software Security
17. Incident Response Management
18. Penetration Testing

### NIST (General)
**Full Name:** National Institute of Standards and Technology - Various Publications

**Purpose:** U.S. federal standards and guidelines for information security, including SP 800-53 (Security and Privacy Controls).

**Applicability:** 36 policies (SANS templates) support NIST SP 800-53 control families.

**Control Families Covered:**
- AC: Access Control
- AT: Awareness and Training
- AU: Audit and Accountability
- CA: Assessment, Authorization, and Monitoring
- CM: Configuration Management
- CP: Contingency Planning
- IA: Identification and Authentication
- IR: Incident Response
- MA: Maintenance
- MP: Media Protection
- PE: Physical and Environmental Protection
- PL: Planning
- PS: Personnel Security
- RA: Risk Assessment
- SA: System and Services Acquisition
- SC: System and Communications Protection
- SI: System and Information Integrity

### GDPR
**Full Name:** General Data Protection Regulation (EU) 2016/679

**Purpose:** EU regulation on data protection and privacy for individuals within the European Union and European Economic Area.

**Applicability:** 3 policies specifically address GDPR requirements (Privacy Management, Data Protection, Data Classification).

**Key GDPR Principles Covered:**
- Lawfulness, fairness and transparency (Article 5)
- Purpose limitation (Article 5)
- Data minimization (Article 5)
- Accuracy (Article 5)
- Storage limitation (Article 5)
- Integrity and confidentiality (Article 5, 32)
- Accountability (Article 5, 24)
- Data subject rights (Articles 12-22)
- Data protection by design and by default (Article 25)
- Records of processing activities (Article 30)
- Security of processing (Article 32)

## Policy-to-Framework Matrix

### Governance Policies (13)

| Policy | ISO 27001 | SOC 2 | NIST | CIS v8 | NIST CSF | GDPR |
|--------|-----------|-------|------|--------|----------|------|
| Acceptable Use Policy | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Information Security Policy | ✓ | ✓ | ✓ | | | |
| Privacy Management Policy | ✓ | ✓ | ✓ | | | ✓ |
| Risk Assessment Policy | ✓ | ✓ | ✓ | | | |
| ... | | | | | | |

### Identity and Access (8)

| Policy | ISO 27001 | SOC 2 | NIST | CIS v8 | NIST CSF | GDPR |
|--------|-----------|-------|------|--------|----------|------|
| Account & Credential Management | ✓ | | | ✓ | ✓ | |
| Access Control Policy | ✓ | ✓ | ✓ | | | |
| Password Policy | ✓ | ✓ | ✓ | | | |
| Remote Access Policy | ✓ | ✓ | ✓ | | | |
| ... | | | | | | |

### Data Protection (2)

| Policy | ISO 27001 | SOC 2 | NIST | CIS v8 | NIST CSF | GDPR |
|--------|-----------|-------|------|--------|----------|------|
| Data Classification Policy | ✓ | ✓ | ✓ | | | ✓ |
| Data Management Policy | ✓ | | | ✓ | ✓ | |

### Incident Management (1)

| Policy | ISO 27001 | SOC 2 | NIST | CIS v8 | NIST CSF | GDPR |
|--------|-----------|-------|------|--------|----------|------|
| Incident Response Management | ✓ | | | ✓ | ✓ | |

## How to Use This Mapping

### For Compliance Projects

1. **Identify Required Framework:** Determine which frameworks your organization must comply with (e.g., ISO 27001, SOC 2)
2. **Filter Policies:** Use the matrix above to identify which policies are required for your framework
3. **Prioritize Implementation:** Start with policies that cover multiple frameworks
4. **Customize:** Adapt policies to your organization's specific context

### For Audit Preparation

1. **Review Coverage:** Check which framework controls are addressed by existing policies
2. **Identify Gaps:** Find framework requirements not covered by current policies
3. **Generate Missing Policies:** Use this plugin to create policies for gaps
4. **Cross-Reference:** Map your policies to specific framework control numbers

### For Multi-Framework Compliance

Organizations complying with multiple frameworks can use policies that satisfy multiple requirements:

**High-Value Policies** (cover 4+ frameworks):
- Acceptable Use Policy (ISO 27001, SOC 2, NIST, CIS v8, NIST CSF)
- Access Control Policy (ISO 27001, SOC 2, NIST, CIS v8)
- Data Classification Policy (ISO 27001, SOC 2, NIST, GDPR)
- Incident Response Policy (ISO 27001, CIS v8, NIST CSF)

## Framework Selection Guide

### Choose ISO 27001 if:
- You need international recognition
- You're in any industry (universally applicable)
- You want a comprehensive ISMS
- You plan to get certified

### Choose SOC 2 if:
- You're a SaaS company or cloud service provider
- You handle customer data
- Customers require SOC 2 reports
- You're in the technology sector

### Choose NIST CSF if:
- You're a U.S. organization
- You're in critical infrastructure sectors
- You want a risk-based approach
- You need flexibility in implementation

### Choose CIS Controls if:
- You want prescriptive, prioritized controls
- You're implementing cybersecurity from scratch
- You want implementation group guidance (IG1/IG2/IG3)
- You prefer technical, actionable controls

### Choose GDPR if:
- You process EU resident data
- You need privacy-specific policies
- You must comply with EU data protection law
- You want privacy by design principles

## References

- **ISO 27001:** https://www.iso.org/standard/54534.html
- **SOC 2:** https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html
- **NIST CSF:** https://www.nist.gov/cyberframework
- **CIS Controls:** https://www.cisecurity.org/controls
- **NIST SP 800-53:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- **GDPR:** https://gdpr-info.eu/

---

**Last Updated:** 2025-10-19
**Version:** 1.0
**Source:** PolicyFrameworkGuide v2.0.0
