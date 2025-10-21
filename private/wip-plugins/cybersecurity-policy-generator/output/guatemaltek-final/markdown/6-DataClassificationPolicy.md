# Data Classification Policy

**Company:** Guatemaltek | **V:** 1.0 | **Effective:** 2026-01-01 | **Review:** Annually | **Officer:** CISO | **Dept:** IT

## Purpose
Establishes data classification framework to ensure appropriate protection based on sensitivity and business value.

## Scope
All Guatemaltek data in any format: electronic, paper, verbal communication.

## Policy

### Classification Levels

**PUBLIC** - Can be freely shared
- Marketing materials, public website content, job postings
- **Handling**: No restrictions
- **Storage**: Any location
- **Transmission**: Any method
- **Disposal**: Standard deletion/recycling

**INTERNAL** - For company use only
- Internal procedures, org charts, internal communications
- **Handling**: Guatemaltek personnel only
- **Storage**: Company approved systems
- **Transmission**: Encrypted for external transmission
- **Disposal**: Secure deletion/shredding

**CONFIDENTIAL** - Sensitive business information
- Customer data, employee PII, financial records, contracts, source code
- **Handling**: Authorized personnel only, need-to-know
- **Storage**: Encrypted company systems only
- **Transmission**: Encryption required
- **Access**: MFA required, logged and audited
- **Labeling**: Mark as "CONFIDENTIAL"
- **Disposal**: Certified secure destruction

**RESTRICTED** - Highly sensitive information
- Passwords/credentials, encryption keys, trade secrets, M&A information
- **Handling**: Strictly limited access, specific authorization
- **Storage**: Encrypted with strong controls
- **Transmission**: Encrypted only, secure channels
- **Access**: MFA mandatory, all access logged and reviewed
- **Labeling**: Mark as "RESTRICTED - DO NOT DISTRIBUTE"
- **Disposal**: Certified secure destruction with certificate

### Handling Requirements Matrix

| Requirement | PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED |
|-------------|--------|----------|--------------|------------|
| **Encryption (at rest)** | No | Recommended | Required | Required (strong) |
| **Encryption (in transit)** | No | For external | Required | Required |
| **MFA** | No | No | Recommended | Required |
| **Access Logging** | No | No | Required | Required + Review |
| **Labeling** | No | No | Required | Required |
| **DLP Monitoring** | No | No | Recommended | Required |
| **Secure Disposal** | No | Yes | Certified | Certified + Log |

### Classification Process
1. **Data Owner** classifies data upon creation
2. Apply appropriate labels/markings
3. Review classification when data changes significantly
4. Annual review of CONFIDENTIAL/RESTRICTED data
5. Declassify when sensitivity decreases (with approval)

### Responsibilities

**Data Owners:** Classify data, authorize access, enforce handling
**All Users:** Handle data per classification, report misclassification
**IT Department:** Implement technical controls, monitor compliance

## Compliance
**ISO 27001:** A.8.2 (Data classification) | **NIST CSF:** PR.DS (Data Security)

---
**Approved:** CISO | 2026-01-01 | **Next Review:** 2027-01-01
