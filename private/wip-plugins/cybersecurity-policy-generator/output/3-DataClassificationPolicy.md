# Data Classification Policy

**Company:** Guatemaltek
**Version:** 1.0
**Effective Date:** 2026-01-01
**Review Schedule:** Annually
**Responsible Officer:** Chief Information Security Officer (CISO)
**Department:** IT Department
**Contact:** test@guatemaltek.com

---

## Table of Contents

1. [Purpose](#purpose)
2. [Scope](#scope)
3. [Policy](#policy)
4. [Compliance](#compliance)
5. [Management Support](#management-support)
6. [Exceptions](#exceptions)
7. [Responsibility](#responsibility)

---

## Purpose

The purpose of this policy is to establish a framework for classifying Guatemaltek's data based on its level of sensitivity, value, and criticality to the organization. Proper data classification ensures that appropriate security controls are applied to protect information assets according to their importance and sensitivity.

## Scope

This policy applies to:
- All Guatemaltek employees, contractors, consultants, and temporary workers
- All data created, processed, stored, or transmitted by Guatemaltek
- All information systems and storage media containing Guatemaltek data
- Data in any format: electronic, paper, or other media
- Data throughout its entire lifecycle (creation to destruction)

## Policy

### Data Classification Levels

Guatemaltek uses a four-tier data classification system:

#### 1. Public Data
**Definition:** Information that can be freely shared with the public without risk to Guatemaltek.

**Examples:**
- Marketing materials
- Published website content
- Press releases
- Product documentation (public-facing)
- Job postings

**Handling Requirements:**
- No special protection required
- May be freely distributed
- Should still maintain accuracy and quality

---

#### 2. Internal Use Data
**Definition:** Information intended for use within Guatemaltek that could cause minor inconvenience if disclosed but would not significantly harm the organization.

**Examples:**
- Internal policies and procedures (non-sensitive)
- Organization charts
- Internal newsletters
- Meeting minutes (non-confidential)
- Training materials

**Handling Requirements:**
- Limit distribution to Guatemaltek personnel
- Store on approved company systems
- Do not share on public platforms
- Use email encryption when sending externally
- Dispose of securely (shredding for paper)

---

#### 3. Confidential Data
**Definition:** Sensitive business information that could cause significant harm to Guatemaltek if disclosed to unauthorized parties.

**Examples:**
- Employee personal information (PII)
- Financial records
- Customer data
- Contracts and agreements
- Strategic plans
- Source code (proprietary)
- Security configurations
- Vendor information

**Handling Requirements:**
- Access limited to authorized personnel only
- Encrypt when stored electronically
- Encrypt when transmitted (email, file transfer)
- Multi-factor authentication for access
- Logged and audited access
- Secure disposal required (shredding, secure deletion)
- Non-disclosure agreements may be required
- Watermark or label as "Confidential"

---

#### 4. Restricted Data
**Definition:** Highly sensitive information that could cause severe damage to Guatemaltek if disclosed. Requires the highest level of protection.

**Examples:**
- Authentication credentials (passwords, API keys)
- Encryption keys
- Trade secrets
- M&A information (pre-announcement)
- Security incident details
- Regulated data (if applicable)
- Executive communications (sensitive)

**Handling Requirements:**
- Access strictly limited to specific individuals
- Strong encryption required (at rest and in transit)
- Multi-factor authentication mandatory
- All access logged and reviewed regularly
- No electronic transmission without encryption
- Physical documents kept in locked storage
- Secure destruction required (cross-cut shredding, certified deletion)
- Data loss prevention (DLP) tools applied
- Label as "Restricted" with handling instructions

### Data Classification Process

1. **Data Creation**:
   - Creator/owner must classify data upon creation
   - Apply appropriate classification label
   - Document classification decision if non-obvious

2. **Classification Review**:
   - Review classification when data changes significantly
   - Annual review of Confidential and Restricted data
   - Reclassify if sensitivity changes

3. **Labeling**:
   - Electronic documents: Include classification in header/footer or metadata
   - Email: Include classification in subject line for Confidential/Restricted
   - Physical documents: Mark on each page
   - Storage media: Label clearly

4. **Declassification**:
   - Data may be declassified when sensitivity decreases
   - Requires approval from data owner
   - Document declassification decision

### Handling Requirements by Classification

| Requirement | Public | Internal | Confidential | Restricted |
|-------------|--------|----------|--------------|------------|
| **Access Control** | None | Guatemaltek personnel | Authorized only | Strictly limited |
| **Encryption (Storage)** | No | Recommended | Required | Required (strong) |
| **Encryption (Transit)** | No | Recommended | Required | Required (strong) |
| **MFA Required** | No | No | Recommended | Required |
| **Access Logging** | No | No | Required | Required |
| **Labeling** | Optional | Optional | Required | Required |
| **Secure Disposal** | No | Recommended | Required | Required (certified) |
| **DLP Monitoring** | No | No | Recommended | Required |

### Data Storage

1. **Approved Storage**:
   - Public: Any location
   - Internal: Guatemaltek-approved systems only
   - Confidential: Encrypted Guatemaltek systems
   - Restricted: Encrypted systems with strict access controls

2. **Prohibited Storage**:
   - Personal email accounts (for Internal and above)
   - Personal cloud storage (for Confidential and above)
   - Unencrypted portable media (for Confidential and above)
   - Public file sharing sites (for Confidential and above)

3. **Backup**:
   - Backups must maintain same classification and protections
   - Encrypted backups required for Confidential and Restricted

### Data Transmission

1. **Email**:
   - Public/Internal: Standard email acceptable
   - Confidential: Encrypt or use secure file sharing
   - Restricted: Must encrypt, consider secure portal

2. **File Sharing**:
   - Public/Internal: Approved collaboration tools
   - Confidential: Encrypted file sharing with access controls
   - Restricted: Encrypted sharing with MFA and access logging

3. **Physical Transport**:
   - Confidential/Restricted: Encrypted storage media
   - Use tracked shipping methods
   - Document chain of custody

### Data Destruction

1. **Electronic Data**:
   - Public/Internal: Standard deletion
   - Confidential: Secure deletion (overwrite)
   - Restricted: Certified secure deletion or physical destruction

2. **Physical Media**:
   - Public/Internal: Standard disposal
   - Confidential: Cross-cut shredding
   - Restricted: Certified destruction with certificate

3. **Storage Media**:
   - Confidential/Restricted hard drives: Physical destruction
   - Document destruction with serial numbers

## Compliance

This policy supports compliance with:

**Frameworks:**
- **ISO 27001:** A.8.2 (Information classification), A.8.3 (Media handling)
- **SOC 2:** CC6.1, CC6.6 (Logical access, data protection)
- **NIST CSF:** PR.DS-1, PR.DS-2, PR.DS-5, PR.IP-2 (Data-at-rest protection, data-in-transit protection)

**Data Protection:**
- Supports GDPR Article 32 (Security of processing)
- Supports data minimization principles
- Enables appropriate technical and organizational measures

## Management Support

Guatemaltek's leadership recognizes that proper data classification is fundamental to protecting our information assets and meeting our obligations to customers, partners, and employees.

The CISO and IT Department are authorized to:
- Implement technical controls for data protection
- Conduct audits of data handling practices
- Enforce this policy
- Provide classification guidance

## Review Schedule

This policy will be reviewed **annually** by the IT Department and CISO. Reviews will be conducted every January, with the next review scheduled for January 2027.

Classification levels and requirements will be reviewed in response to:
- Changes in business operations
- New regulatory requirements
- Security incidents involving data
- Technology changes

## Exceptions

Exceptions to handling requirements may be granted when:
1. Technical limitations prevent compliance
2. Business justification exists
3. Compensating controls are implemented
4. CISO approves in writing
5. Exception is reviewed quarterly

Common exceptions:
- Legacy systems unable to encrypt (must have migration plan)
- Specific business processes requiring alternate handling

## Responsibility

**Data Owners** are responsible for:
- Classifying data they create or manage
- Ensuring appropriate protections are applied
- Reviewing classification periodically
- Authorizing access to classified data
- Approving declassification

**All Users** are responsible for:
- Understanding data classification levels
- Handling data according to its classification
- Reporting misclassified data
- Reporting data security incidents
- Applying proper labels to data they create

**IT Department** is responsible for:
- Implementing technical controls by classification level
- Providing tools for data protection (encryption, DLP, etc.)
- Monitoring compliance
- Providing classification training
- Assisting with proper data disposal

**CISO** is responsible for:
- Policy oversight and enforcement
- Approving exceptions
- Reviewing classification incidents
- Ensuring regulatory compliance
- Updating classification framework as needed

**Managers** are responsible for:
- Ensuring their teams understand and follow this policy
- Identifying data owners in their area
- Supporting data classification efforts
- Reporting policy violations

---

## Approval and Review

**Approved by:** Chief Information Security Officer (CISO)
**Approval Date:** 2026-01-01
**Next Review Date:** 2027-01-01

## Document Control

**Version:** 1.0
**Last Updated:** 2025-10-19
**Document Owner:** Guatemaltek IT Department

---

*This policy was generated using the Cybersecurity Policy Generator.*
*Template Source: SANS Security Policy Templates*
*Frameworks: ISO 27001, SOC 2, NIST CSF*
