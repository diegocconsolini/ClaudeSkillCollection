# Policy Categories Guide

This document describes the 15 policy categories available in the Cybersecurity Policy Generator, with 51 total policy templates.

## Category Overview

| Category | Policies | Description | Primary Use Case |
|----------|----------|-------------|------------------|
| **Governance** | 13 | High-level policies for security program management | Executive oversight, compliance framework |
| **Identity and Access** | 8 | User authentication and authorization controls | Access management, least privilege |
| **Application** | 7 | Application security and development practices | Secure SDLC, DevSecOps |
| **Compute** | 6 | Server and endpoint security | Infrastructure security |
| **Network** | 4 | Network security controls and segmentation | Perimeter defense, network monitoring |
| **Data Protection** | 2 | Data handling, classification, and protection | Data privacy, encryption |
| **Resilience** | 2 | Business continuity and disaster recovery | Operational continuity |
| **Configuration Management** | 2 | System configuration and change control | Baseline hardening |
| **Logging and Monitoring** | 1 | Security event logging and analysis | Threat detection, forensics |
| **Incident Management** | 1 | Incident response and handling | Security incident response |
| **Threat Protection** | 1 | Malware and threat defense | Endpoint protection |
| **Training and Awareness** | 1 | Security education programs | User awareness |
| **Third-Party Risk** | 1 | Vendor and supplier security | Supply chain security |
| **Asset Management** | 1 | Hardware and software inventory | Asset tracking |
| **Vulnerability Management** | 1 | Vulnerability scanning and patching | Risk remediation |

## Detailed Category Descriptions

### 1. Governance (13 policies)

**Purpose:** Establish the foundation for your cybersecurity program with executive-level policies that define security strategy, risk management, and compliance requirements.

**Policies Included:**
1. Acceptable Use Policy (CIS)
2. Artificial Intelligence Use Policy (SANS)
3. Cloud Security Policy (SANS)
4. Governance Policy (SANS)
5. Information Security Policy (SANS)
6. Pandemic Response Policy (SANS)
7. Privacy Management Policy (SANS)
8. Risk Assessment Policy (SANS)
9. Server Security Policy (SANS)
10. Social Media Policy (SANS)
11. Wireless Communication Policy (SANS)
12. *[Additional governance policies...]*

**When to Use:**
- Starting a new security program
- Preparing for compliance audits (ISO 27001, SOC 2)
- Establishing executive oversight
- Defining organizational security responsibilities

**Key Stakeholders:**
- C-suite executives (CEO, CIO, CISO)
- Board of directors
- Legal and compliance teams
- Risk management officers

**Frameworks:** ISO 27001, SOC 2, NIST

---

### 2. Identity and Access (8 policies)

**Purpose:** Control who has access to what resources through authentication, authorization, and account management policies.

**Policies Included:**
1. Account and Credential Management Policy (CIS)
2. Access Control Policy (SANS)
3. Password Policy (SANS)
4. Remote Access Policy (SANS)
5. Technology Equipment Disposal Policy (SANS)
6. User Account Policy (SANS)
7. Virtual Private Network (VPN) Policy (SANS)
8. *[Additional access policies...]*

**When to Use:**
- Implementing zero trust architecture
- Meeting compliance requirements for access controls
- Preventing unauthorized access
- Managing privileged accounts
- Supporting remote workforce

**Key Stakeholders:**
- Identity and Access Management (IAM) teams
- System administrators
- Security operations
- Help desk / IT support

**Frameworks:** ISO 27001 (A.9), SOC 2, NIST (AC family), CIS Controls 5-6

---

### 3. Application (7 policies)

**Purpose:** Secure the software development lifecycle and application deployment processes.

**Policies Included:**
1. Application Software Security Policy (CIS)
2. Email and Web Browser Protections Policy (CIS)
3. Secure Application Development Policy (SANS)
4. *[Additional application policies...]*

**When to Use:**
- Implementing DevSecOps practices
- Securing custom application development
- Managing third-party software
- Protecting web applications
- Email security controls

**Key Stakeholders:**
- Development teams
- DevOps engineers
- Application security teams
- QA/Testing teams

**Frameworks:** ISO 27001 (A.14), CIS Control 16, NIST (SA, SI families)

---

### 4. Compute (6 policies)

**Purpose:** Secure servers, workstations, endpoints, and computing infrastructure.

**Policies Included:**
1. Inventory and Control of Enterprise Assets Policy (CIS)
2. Inventory and Control of Software Assets Policy (CIS)
3. Secure Configuration Management Policy (CIS)
4. Server Security Policy (SANS)
5. Technology Equipment Disposal Policy (SANS)
6. *[Additional compute policies...]*

**When to Use:**
- Building asset inventory
- Hardening systems
- Implementing endpoint security
- Managing server infrastructure
- Decommissioning equipment securely

**Key Stakeholders:**
- System administrators
- Infrastructure teams
- Asset management
- Endpoint security teams

**Frameworks:** ISO 27001 (A.8, A.11), CIS Controls 1-2, 4, NIST (CM family)

---

### 5. Network (4 policies)

**Purpose:** Secure network infrastructure, connectivity, and communications.

**Policies Included:**
1. Network Infrastructure Management Policy (CIS)
2. Network Monitoring and Defense Policy (CIS)
3. Remote Access Policy (SANS)
4. Virtual Private Network (VPN) Policy (SANS)

**When to Use:**
- Network segmentation projects
- Perimeter defense
- Remote access enablement
- Network monitoring implementation
- Zero trust network architecture

**Key Stakeholders:**
- Network engineers
- Security operations center (SOC)
- Network security teams
- Infrastructure architects

**Frameworks:** ISO 27001 (A.13), CIS Controls 12-13, NIST (SC family)

---

### 6. Data Protection (2 policies)

**Purpose:** Protect sensitive data through classification, encryption, and handling procedures.

**Policies Included:**
1. Data Classification Policy (SANS)
2. Data Management Policy (CIS)

**When to Use:**
- GDPR compliance projects
- Implementing data loss prevention (DLP)
- Protecting intellectual property
- Handling customer data
- Encrypting sensitive information

**Key Stakeholders:**
- Data protection officers (DPO)
- Privacy teams
- Legal/compliance
- Database administrators

**Frameworks:** ISO 27001 (A.8), CIS Control 3, NIST (MP family), GDPR (Articles 5, 32)

---

### 7. Resilience (2 policies)

**Purpose:** Ensure business continuity and disaster recovery capabilities.

**Policies Included:**
1. Data Recovery Policy (CIS)
2. Disaster Recovery Plan Policy (SANS)

**When to Use:**
- Business continuity planning
- Disaster recovery testing
- Backup strategy development
- Ransomware protection
- High availability requirements

**Key Stakeholders:**
- Business continuity managers
- Backup administrators
- Disaster recovery teams
- Executive management

**Frameworks:** ISO 27001 (A.17), CIS Control 11, NIST (CP family)

---

### 8. Configuration Management (2 policies)

**Purpose:** Maintain secure system configurations and manage changes.

**Policies Included:**
1. Secure Configuration Management Policy (CIS)
2. *[Additional configuration policies...]*

**When to Use:**
- Implementing configuration baselines
- Change management processes
- System hardening initiatives
- Compliance with security benchmarks (CIS Benchmarks)

**Key Stakeholders:**
- Configuration management teams
- Change advisory boards (CAB)
- System administrators
- Security architects

**Frameworks:** ISO 27001 (A.12), CIS Control 4, NIST (CM family)

---

### 9. Logging and Monitoring (1 policy)

**Purpose:** Establish comprehensive logging and security monitoring capabilities.

**Policies Included:**
1. Audit Log Management Policy (CIS)

**When to Use:**
- Building security operations center (SOC)
- SIEM implementation
- Compliance logging requirements
- Forensic investigation preparation
- Threat detection programs

**Key Stakeholders:**
- Security operations teams
- SIEM administrators
- Compliance auditors
- Incident response teams

**Frameworks:** ISO 27001 (A.12.4), CIS Control 8, NIST (AU family), SOC 2 (Monitoring)

---

### 10. Incident Management (1 policy)

**Purpose:** Define incident response procedures and team responsibilities.

**Policies Included:**
1. Incident Response Management Policy (CIS)

**When to Use:**
- Establishing incident response team
- Preparing for security incidents
- Meeting regulatory notification requirements
- Coordinating breach response
- Post-incident reviews

**Key Stakeholders:**
- Incident response teams
- Security operations center (SOC)
- Legal/compliance
- Communications/PR teams

**Frameworks:** ISO 27001 (A.16), CIS Control 17, NIST (IR family), SOC 2

---

### 11. Threat Protection (1 policy)

**Purpose:** Protect against malware, ransomware, and other cyber threats.

**Policies Included:**
1. Malware Defenses Policy (CIS)

**When to Use:**
- Deploying antivirus/anti-malware solutions
- Ransomware protection programs
- Email security implementation
- Endpoint protection

**Key Stakeholders:**
- Endpoint security teams
- Security operations
- Email administrators
- End users

**Frameworks:** CIS Control 10, NIST (SI family)

---

### 12. Training and Awareness (1 policy)

**Purpose:** Educate employees on security best practices and threats.

**Policies Included:**
1. Security Awareness and Skills Training Policy (CIS)

**When to Use:**
- Onboarding new employees
- Annual security training programs
- Phishing awareness campaigns
- Role-based security training
- Compliance training requirements

**Key Stakeholders:**
- Human resources
- Security awareness teams
- Training coordinators
- All employees

**Frameworks:** ISO 27001 (A.7.2), CIS Control 14, NIST (AT family), SOC 2

---

### 13. Third-Party Risk (1 policy)

**Purpose:** Manage security risks from vendors, suppliers, and service providers.

**Policies Included:**
1. Service Provider Management Policy (CIS)

**When to Use:**
- Vendor onboarding processes
- Third-party risk assessments
- Cloud service provider evaluation
- Supply chain security
- Outsourcing arrangements

**Key Stakeholders:**
- Procurement teams
- Vendor management
- Legal/contracts
- Security teams

**Frameworks:** ISO 27001 (A.15), CIS Control 15, NIST (SA family), SOC 2

---

### 14. Asset Management (1 policy)

**Purpose:** Maintain accurate inventory of hardware and software assets.

**Policies Included:**
1. Inventory and Control of Enterprise Assets Policy (CIS)

**When to Use:**
- Building asset inventory
- Software license management
- Hardware lifecycle management
- Shadow IT discovery
- Decommissioning processes

**Key Stakeholders:**
- Asset management teams
- IT operations
- Procurement
- Finance (for asset tracking)

**Frameworks:** ISO 27001 (A.8.1), CIS Controls 1-2, NIST (CM family)

---

### 15. Vulnerability Management (1 policy)

**Purpose:** Identify, prioritize, and remediate security vulnerabilities.

**Policies Included:**
1. Continuous Vulnerability Management Policy (CIS)

**When to Use:**
- Vulnerability scanning programs
- Patch management processes
- Penetration testing
- Security assessment activities
- Risk-based prioritization

**Key Stakeholders:**
- Vulnerability management teams
- System administrators
- Security operations
- Risk management

**Frameworks:** ISO 27001 (A.12.6), CIS Control 7, NIST (RA, SI families)

---

## How to Choose the Right Policy

### By Use Case

**Starting a new security program?**
→ Begin with **Governance** policies (Information Security Policy, Risk Assessment)

**Need to protect data?**
→ Use **Data Protection** policies (Data Classification, Data Management)

**Building incident response capability?**
→ Focus on **Incident Management** and **Logging and Monitoring**

**Managing user access?**
→ Implement **Identity and Access** policies (Access Control, Password Policy)

**Securing infrastructure?**
→ Deploy **Compute** and **Network** policies

### By Compliance Framework

**ISO 27001 certification?**
→ All 51 policies support ISO 27001 (prioritize governance first)

**SOC 2 audit preparation?**
→ Focus on 36 SANS policies covering all Trust Service Criteria

**CIS Controls implementation?**
→ Use 15 CIS policies mapped directly to CIS Controls v8

**NIST Cybersecurity Framework?**
→ 15 CIS policies + 21 SANS policies cover all 5 functions

### By Organization Size

**Small Organization (<50 employees):**
- Acceptable Use Policy
- Password Policy
- Data Classification Policy
- Backup/Data Recovery Policy
- Incident Response Policy

**Medium Organization (50-500 employees):**
- Add: Access Control Policy
- Add: Remote Access Policy
- Add: Vulnerability Management Policy
- Add: Security Awareness Training Policy
- Add: Audit Log Management Policy

**Large Enterprise (500+ employees):**
- Comprehensive coverage across all 15 categories
- Role-specific policies for different departments
- Industry-specific additional policies

## Policy Implementation Priority

### Priority 1: Essential (Implement First)
1. Information Security Policy (Governance)
2. Acceptable Use Policy (Governance)
3. Password Policy (Identity and Access)
4. Data Classification Policy (Data Protection)
5. Data Recovery Policy (Resilience)

### Priority 2: Important (Implement Within 3 Months)
6. Access Control Policy (Identity and Access)
7. Incident Response Policy (Incident Management)
8. Remote Access Policy (Network)
9. Security Awareness Training (Training and Awareness)
10. Vulnerability Management (Vulnerability Management)

### Priority 3: Advanced (Implement Within 6 Months)
11. Audit Log Management (Logging and Monitoring)
12. Configuration Management (Configuration Management)
13. Asset Inventory (Asset Management)
14. Service Provider Management (Third-Party Risk)
15. Malware Defense (Threat Protection)

---

## Category Cross-References

Some policies span multiple categories:

- **Remote Access Policy** → Network + Identity and Access
- **Technology Equipment Disposal** → Compute + Data Protection
- **Server Security Policy** → Compute + Governance
- **Email and Web Browser Protections** → Application + Threat Protection

---

**Last Updated:** 2025-10-19
**Version:** 1.0
**Total Policies:** 51 (36 SANS + 15 CIS)
