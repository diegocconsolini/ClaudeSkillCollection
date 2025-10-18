# Technical and Organizational Security Measures (Article 32)

## Overview

Article 32 requires implementing appropriate technical and organizational measures to ensure a level of security appropriate to the risk. This includes protecting against accidental or unlawful destruction, loss, alteration, unauthorized disclosure, or access.

## Risk Assessment Factors

When determining appropriate security measures, consider:

1. **State of the art** - Current best practices and technologies
2. **Implementation costs** - Cost-benefit analysis
3. **Nature of processing** - Type and sensitivity of data
4. **Scope of processing** - Volume and scale
5. **Context** - Circumstances and purposes
6. **Risks to rights and freedoms** - Potential harm to data subjects

## Technical Measures

### 1. Encryption

#### Encryption at Rest
**Purpose:** Protect data stored in databases, file systems, backups

**Implementation:**
- Full disk encryption (FDE)
- Database encryption (TDE - Transparent Data Encryption)
- File-level encryption for sensitive documents
- Encrypted backups
- Hardware Security Modules (HSM) for key management

**Technologies:**
- AES-256 for symmetric encryption
- RSA-2048+ for asymmetric encryption
- Encrypted filesystems (LUKS, BitLocker, FileVault)

**Code Example:**
```python
from cryptography.fernet import Fernet

# Encrypt sensitive data before storage
def encrypt_personal_data(data, key):
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted

# Decrypt when authorized access needed
def decrypt_personal_data(encrypted_data, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data)
    return decrypted.decode()
```

#### Encryption in Transit
**Purpose:** Protect data during transmission

**Implementation:**
- TLS 1.2+ for all communications
- HTTPS for web traffic
- Encrypted email (S/MIME, PGP)
- VPN for remote access
- SSH for server access

**Configuration:**
- Strong cipher suites only
- Disable weak protocols (SSLv3, TLS 1.0, TLS 1.1)
- Enable HSTS (HTTP Strict Transport Security)
- Implement certificate pinning for mobile apps

**Web Server Example:**
```nginx
# Nginx SSL/TLS configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### 2. Pseudonymization

**Purpose:** Reduce identifiability while maintaining data utility

**Techniques:**
- Replace identifiers with pseudonyms
- Hash personal identifiers
- Tokenization
- Key-coding

**Implementation:**
```python
import hashlib
import hmac

# Pseudonymize user ID with keyed hash
def pseudonymize_user_id(user_id, secret_key):
    return hmac.new(
        secret_key.encode(),
        user_id.encode(),
        hashlib.sha256
    ).hexdigest()

# Consistent pseudonym for same user
user_pseudo = pseudonymize_user_id("user123", "secret_key")
```

**Note:** Pseudonymization is reversible with the key, so data remains personal data under GDPR.

### 3. Access Controls

#### Authentication
**Requirements:**
- Strong password policies (length, complexity, rotation)
- Multi-factor authentication (MFA/2FA)
- Single Sign-On (SSO) with centralized management
- Biometric authentication where appropriate

**Implementation:**
- Minimum 12-character passwords
- Password complexity requirements
- Account lockout after failed attempts
- Password breach detection
- MFA for administrative access

#### Authorization
**Requirements:**
- Role-Based Access Control (RBAC)
- Principle of Least Privilege
- Need-to-know basis
- Separation of duties

**Implementation:**
```python
# Role-based access control example
def can_access_personal_data(user, data_type, operation):
    user_role = get_user_role(user)

    permissions = {
        'data_protection_officer': ['read', 'write', 'delete', 'export'],
        'customer_service': ['read', 'write'],
        'analyst': ['read'],  # Only aggregated/pseudonymized
        'developer': []  # No production access
    }

    allowed_operations = permissions.get(user_role, [])

    # Log access attempt
    log_access_attempt(user, data_type, operation, user_role)

    if operation in allowed_operations:
        # Additional check for sensitive data
        if is_sensitive_data(data_type) and operation != 'read':
            return requires_additional_approval(user, data_type, operation)
        return True

    return False
```

### 4. Data Minimization

**Technical Implementation:**
- Collect only necessary fields
- Remove unnecessary data fields from forms
- Auto-delete data after retention period
- Aggregate data for analytics instead of individual records

**Code Example:**
```python
# Automated data retention enforcement
def enforce_retention_policy():
    retention_periods = {
        'user_activity_logs': 90,  # days
        'marketing_data': 365,
        'customer_data': 730
    }

    for data_type, days in retention_periods.items():
        cutoff_date = datetime.now() - timedelta(days=days)
        delete_data_older_than(data_type, cutoff_date)
        log_retention_enforcement(data_type, cutoff_date)
```

### 5. Anonymization

**Purpose:** Irreversibly de-identify data so it's no longer personal data

**Techniques:**
- Data masking
- Aggregation
- Generalization
- Noise addition (differential privacy)
- K-anonymity

**Requirements:**
- Must be truly irreversible
- Consider singling out, linkability, inference risks
- Test re-identification resistance

**Example:**
```python
# K-anonymity implementation
def anonymize_dataset(df, quasi_identifiers, k=5):
    """
    Generalize quasi-identifiers to achieve k-anonymity
    """
    for qi in quasi_identifiers:
        if df[qi].dtype in ['int64', 'float64']:
            # Generalize numeric data into ranges
            df[qi] = pd.cut(df[qi], bins=10, labels=False)
        else:
            # Generalize categorical data
            df[qi] = generalize_categories(df[qi])

    # Verify k-anonymity
    group_sizes = df.groupby(quasi_identifiers).size()
    if group_sizes.min() < k:
        raise ValueError(f"K-anonymity not achieved (min group size: {group_sizes.min()})")

    return df
```

### 6. Audit Logging

**Purpose:** Track access and modifications to personal data

**What to Log:**
- Who accessed data (user ID, role)
- What data was accessed (type, record ID)
- When access occurred (timestamp)
- What operation (read, write, delete, export)
- From where (IP address, location)
- Result (success, failure, reason)

**Implementation:**
```python
# Comprehensive audit logging
def log_data_access(user_id, operation, data_type, record_id, result):
    audit_log = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'user_role': get_user_role(user_id),
        'operation': operation,
        'data_type': data_type,
        'record_id': record_id,
        'ip_address': get_user_ip(),
        'user_agent': get_user_agent(),
        'result': result,
        'session_id': get_session_id()
    }

    # Store in tamper-proof log
    write_to_audit_log(audit_log)

    # Alert on suspicious activity
    if is_suspicious_activity(audit_log):
        trigger_security_alert(audit_log)
```

**Log Protection:**
- Immutable logs (write-once)
- Encrypted storage
- Regular integrity checks
- Separate storage from operational data
- Retention: Typically 1-2 years

### 7. Security Testing

**Regular Testing:**
- Penetration testing (annually minimum)
- Vulnerability scanning (continuous)
- Security code reviews
- Dependency vulnerability checks
- Configuration audits

**Implementation:**
```bash
# Automated security scanning
# Static Application Security Testing (SAST)
bandit -r ./src -f json -o security-report.json

# Dependency vulnerability scanning
safety check --json

# Container security scanning
trivy image myapp:latest
```

### 8. Backup and Recovery

**Requirements:**
- Regular encrypted backups
- Offsite backup storage
- Tested restore procedures
- Backup retention policy
- Secure backup deletion

**Implementation:**
- Automated daily backups
- 3-2-1 rule: 3 copies, 2 media types, 1 offsite
- Encrypted backup transmission and storage
- Regular restore testing (quarterly)
- Document Recovery Time Objective (RTO) and Recovery Point Objective (RPO)

### 9. Network Security

**Measures:**
- Firewall configuration
- Network segmentation
- Intrusion Detection/Prevention Systems (IDS/IPS)
- DDoS protection
- VPN for remote access

**Implementation:**
- DMZ for public-facing services
- Separate networks for production, development, management
- Allowlist-based firewall rules
- Monitoring and alerting

## Organizational Measures

### 1. Policies and Procedures

**Required Policies:**
- Data protection policy
- Information security policy
- Incident response plan
- Data breach procedure
- Access control policy
- Data retention policy
- Acceptable use policy
- Third-party management policy

### 2. Staff Training

**Requirements:**
- GDPR awareness training (all staff)
- Data protection training (staff handling personal data)
- Security awareness training
- Phishing simulations
- Role-specific training

**Frequency:**
- Initial training for new hires
- Annual refresher training
- Additional training after incidents

### 3. Data Protection by Design and Default

**Principles:**
- Privacy considered from project inception
- Privacy-protective defaults
- Minimize data collection
- Limit data access
- Enable privacy controls

**Implementation Checklist:**
- [ ] Privacy impact assessment for new projects
- [ ] Data protection requirements in design phase
- [ ] Privacy-friendly default settings
- [ ] Built-in privacy controls
- [ ] Data minimization by default

### 4. Vendor Management

**Third-Party Processor Requirements:**
- Data Processing Agreements (DPA)
- Security assessment before onboarding
- Regular audits of processors
- Contract clauses covering security
- Sub-processor approval process

**Due Diligence:**
- Security certifications (ISO 27001, SOC 2)
- Data location and transfers
- Breach notification procedures
- Data return/deletion procedures
- Insurance coverage

### 5. Incident Response

**Incident Response Plan:**
1. **Detection** - Monitoring and detection systems
2. **Assessment** - Evaluate scope and impact
3. **Containment** - Stop the breach
4. **Investigation** - Root cause analysis
5. **Notification** - Supervisory authority (72 hours), data subjects if high risk
6. **Recovery** - Restore systems and data
7. **Lessons Learned** - Post-incident review

**Preparation:**
- Incident response team identified
- Contact lists maintained
- Escalation procedures documented
- Communication templates prepared
- Regular incident response drills

### 6. Physical Security

**Measures:**
- Access control to facilities (badges, biometrics)
- Visitor management
- CCTV surveillance
- Secure disposal of physical media
- Clean desk policy
- Locked storage for sensitive documents

### 7. Business Continuity

**Planning:**
- Business continuity plan (BCP)
- Disaster recovery plan (DRP)
- Redundant systems and data
- Regular testing of plans
- Alternative processing sites

## Risk-Based Approach

### Low Risk Processing
**Measures:**
- Basic encryption
- Password protection
- Standard access controls
- Basic logging

### Medium Risk Processing
**Measures:**
- Strong encryption
- MFA authentication
- RBAC
- Comprehensive logging
- Regular security testing
- Staff training

### High Risk Processing
**Measures:**
- Advanced encryption (HSM)
- Strict access controls
- Pseudonymization/anonymization
- Detailed audit trails
- Continuous monitoring
- Penetration testing
- DPIA required
- DPO involvement
- Enhanced vendor due diligence

## Security Certifications

**Relevant Certifications:**
- ISO 27001 (Information Security Management)
- ISO 27701 (Privacy Information Management)
- SOC 2 Type II (Security, Availability, Confidentiality)
- ISO 27017 (Cloud Security)
- ISO 27018 (Personal Data in Cloud)
- PCI DSS (Payment Card Industry - for payment data)

## Monitoring and Review

**Regular Activities:**
- Security metrics tracking
- Quarterly security reviews
- Annual security audits
- Penetration testing
- Vulnerability assessments
- Policy reviews and updates
- Incident trend analysis
- Training effectiveness assessment

**Key Metrics:**
- Number of security incidents
- Time to detect incidents
- Time to respond to incidents
- Number of access requests
- Failed login attempts
- Patch application time
- Training completion rates
- Audit findings
