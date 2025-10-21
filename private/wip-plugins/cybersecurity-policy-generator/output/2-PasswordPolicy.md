# Password Policy

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

The purpose of this policy is to establish standards for creating secure passwords and protecting password information at Guatemaltek. Strong passwords are critical to maintaining the security of Guatemaltek's information systems and protecting against unauthorized access.

## Scope

This policy applies to all Guatemaltek employees, contractors, consultants, temporary workers, and other personnel who have access to Guatemaltek information systems. This includes:

- All user accounts and passwords
- System-level and administrative passwords
- Application passwords
- Passwords for third-party services used for business
- Passwords for remote access

## Policy

### Password Construction Requirements

All Guatemaltek passwords must meet the following minimum requirements:

1. **Minimum Length**: At least 12 characters (16 characters recommended for administrative accounts)

2. **Complexity**: Must contain characters from at least three of the following categories:
   - Uppercase letters (A-Z)
   - Lowercase letters (a-z)
   - Numbers (0-9)
   - Special characters (!@#$%^&*()_+-=[]{}|;:,.<>?)

3. **Prohibited Passwords**:
   - Dictionary words in any language
   - Your name, username, or company name
   - Common patterns (123456, qwerty, password)
   - Previous passwords with minor modifications
   - Personal information (birthdate, phone number, etc.)

4. **Passphrase Alternative**: Users may use passphrases of at least 4 random words (minimum 20 characters total) as an alternative to complex passwords

### Password Protection

1. **Confidentiality**: Passwords must not be:
   - Shared with any other person
   - Written down or stored in plain text
   - Sent via email or other unsecured channels
   - Included in automated login scripts

2. **Password Storage**: If password storage is necessary:
   - Use approved password management software
   - Password managers must be protected with a strong master password
   - Password managers must use encryption

3. **Multi-Factor Authentication (MFA)**: Where available, users must enable MFA for:
   - Email accounts
   - Remote access (VPN)
   - Cloud services
   - Administrative accounts
   - Financial systems

### Password Changes

1. **Regular Changes**:
   - Standard user passwords: Change every 90 days
   - Administrative passwords: Change every 60 days
   - Service account passwords: Change every 180 days (or as required)

2. **Immediate Change Required** when:
   - A password is suspected of being compromised
   - An account shows signs of unauthorized access
   - An employee with password knowledge leaves the company
   - A password has been shared (even unintentionally)
   - After a security incident

3. **Password History**: Systems must prevent reuse of the last 12 passwords

### Account Lockout

1. **Failed Login Attempts**: Accounts will be locked after 5 consecutive failed login attempts

2. **Lockout Duration**:
   - Accounts remain locked for 30 minutes OR
   - Until unlocked by IT Department/Help Desk

3. **Notification**: Failed login attempts should be reported to IT Department for investigation

### Administrative and Service Account Passwords

1. **Administrative Accounts**:
   - Minimum 16 characters
   - Must use MFA
   - Change every 60 days
   - Separate from standard user accounts
   - Used only for administrative tasks

2. **Service Accounts**:
   - Minimum 20 random characters
   - Stored in approved password vault
   - Access logged and monitored
   - Change every 180 days or when personnel change

3. **Shared Accounts**:
   - Avoided whenever possible
   - When necessary, password must be changed when any user with access leaves

### Default Passwords

1. All default passwords on systems, applications, and devices must be changed immediately upon installation or first use

2. Default passwords must never be used in production environments

3. IT Department will maintain a process for identifying and changing default passwords

### Password Recovery

1. **Self-Service Reset**: Where available, users should use self-service password reset tools

2. **Help Desk Reset**: Password resets by help desk require:
   - Verification of user identity
   - Documentation of the reset request
   - Temporary password valid for one use only

3. **Security Questions**: Security questions for password reset must:
   - Not contain publicly available information
   - Be unique and difficult to guess
   - Be changed periodically

## Compliance

This policy supports compliance with:

**Frameworks:**
- **ISO 27001:** A.9.2, A.9.3, A.9.4 (User access management, authentication, password management)
- **SOC 2:** CC6.1, CC6.2 (Logical access controls, authentication)
- **NIST CSF:** PR.AC-1, PR.AC-7 (Identity and credential management)

**Standards:**
- NIST SP 800-63B (Digital Identity Guidelines)
- CIS Controls v8: Control 6 (Access Control Management)

## Management Support

Guatemaltek's leadership recognizes that password security is a critical component of our overall security posture. The CISO and IT Department are authorized to implement technical controls and conduct audits to ensure compliance with this policy.

Management will provide:
- Password management tools
- Training on password best practices
- Support for MFA implementation
- Resources for password security awareness

## Review Schedule

This policy will be reviewed **annually** by the IT Department and CISO. Reviews will be conducted every January, with the next review scheduled for January 2027.

Updates may occur more frequently based on:
- New authentication technologies
- Security incidents related to passwords
- Changes in industry best practices
- Regulatory requirements

## Exceptions

Exceptions to this policy are rare and must be:
1. Documented with business justification
2. Approved by CISO
3. Include compensating controls
4. Reviewed quarterly

Exceptions may be considered for:
- Legacy systems that cannot meet requirements (must have migration plan)
- Specialized equipment with password limitations
- Third-party integrations (must use alternative authentication where possible)

## Responsibility

**All Users** are responsible for:
- Creating strong, unique passwords
- Protecting password confidentiality
- Changing passwords as required
- Reporting suspected password compromises
- Following password policy requirements

**IT Department** is responsible for:
- Implementing technical password controls
- Providing password management tools
- Monitoring password compliance
- Assisting with password resets
- Conducting password security training

**CISO** is responsible for:
- Policy oversight and enforcement
- Approving exceptions
- Reviewing password-related security incidents
- Ensuring compliance with regulatory requirements

**Managers** are responsible for:
- Ensuring team compliance
- Supporting password security awareness
- Reporting non-compliance
- Removing access for departed employees

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
*Frameworks: ISO 27001, SOC 2, NIST*
