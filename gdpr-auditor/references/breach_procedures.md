# Data Breach Notification Procedures

## Overview

Articles 33 and 34 of GDPR mandate specific procedures for responding to personal data breaches. Failure to comply can result in significant fines (up to €10 million or 2% of global turnover for notification failures).

## What is a Personal Data Breach?

**Definition (Article 4.12):**
"A breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed."

### Types of Breaches

1. **Confidentiality breach** - Unauthorized or accidental disclosure or access
2. **Integrity breach** - Unauthorized or accidental alteration of personal data
3. **Availability breach** - Accidental or unauthorized loss of access or destruction

### Examples

**Confidentiality Breaches:**
- Hacking/cyber attack exposing data
- Sending email to wrong recipient
- Lost/stolen unencrypted devices
- Insider unauthorized access
- Misconfigured cloud storage

**Integrity Breaches:**
- Ransomware encrypting data
- Unauthorized modification of records
- Database corruption
- Malicious data alteration

**Availability Breaches:**
- Denial of service attacks
- Accidental deletion
- Hardware failure
- Natural disaster destroying data centers

## Breach Response Timeline

### Phase 1: Detection and Initial Response (0-24 hours)

**Immediate Actions:**

1. **Contain the breach**
   - Isolate affected systems
   - Stop ongoing unauthorized access
   - Preserve evidence
   - Document timeline of events

2. **Assess the situation**
   - What data was affected?
   - How many individuals?
   - How did it happen?
   - Is it still ongoing?

3. **Assemble response team**
   - Data Protection Officer (DPO)
   - IT/Security team
   - Legal counsel
   - Management
   - Communications/PR (if needed)

**Documentation to Begin:**
- Time of detection
- Nature of breach
- Affected systems/data
- Immediate actions taken
- Who was notified

### Phase 2: Investigation and Risk Assessment (24-48 hours)

**Detailed Assessment:**

1. **Scope of breach**
   - Categories of data affected
   - Number of data subjects
   - Systems/databases compromised
   - Geographic scope

2. **Risk evaluation**
   - Likelihood of harm to individuals
   - Severity of potential consequences
   - Types of data involved (special categories = higher risk)
   - Safeguards in place (encryption, pseudonymization)

3. **Root cause analysis**
   - How did breach occur?
   - What vulnerabilities exist?
   - Who was responsible?
   - Could it happen again?

**Risk Factors to Consider:**

**High Risk Indicators:**
- Special category data (health, race, etc.)
- Financial data or credentials
- Children's data
- Large volume of individuals
- No encryption or other safeguards
- Potential for identity theft or fraud
- Risk of physical harm
- Significant damage to reputation or financial loss

**Lower Risk Indicators:**
- Encrypted data (key not compromised)
- Limited number of individuals
- Non-sensitive data
- Quick containment
- Minimal likelihood of harm

### Phase 3: Notification Decision (Within 72 hours)

**Article 33: Notification to Supervisory Authority**

**When Required:**
Notify unless "unlikely to result in a risk to the rights and freedoms of natural persons"

**Timeline:**
- Within 72 hours of becoming aware
- Clock starts when organization has reasonable certainty a breach occurred
- Not when breach originally happened

**What to Report:**

1. **Nature of the breach**
   - Description of what happened
   - Categories of data subjects
   - Approximate number of data subjects affected
   - Categories of personal data records
   - Approximate number of records

2. **Contact information**
   - Name and contact details of DPO or contact point

3. **Likely consequences**
   - Describe likely consequences of the breach
   - Potential impact on individuals

4. **Measures taken**
   - Measures taken or proposed to address breach
   - Measures to mitigate possible adverse effects

**If Information Not Available:**
- Provide in phases as it becomes available
- Explain delay in final report

**Notification Methods:**
- Online form (most supervisory authorities)
- Email to designated address
- Follow specific authority procedures
- Keep confirmation of notification

**Article 34: Notification to Data Subjects**

**When Required:**
If breach "likely to result in high risk to the rights and freedoms" of individuals

**When NOT Required:**

1. **Technical protection** - Data was encrypted/pseudonymized and key not compromised
2. **Subsequent measures** - Controller took measures ensuring high risk no longer likely
3. **Disproportionate effort** - Would require disproportionate effort (must use public communication instead)

**Timeline:**
- Without undue delay
- No specific timeline, but should be as soon as possible
- Must allow individuals to take precautions

**What to Communicate:**

Must use "clear and plain language" including:

1. **Nature of breach**
   - Describe what happened in understandable terms

2. **Contact point**
   - Name and contact of DPO or information point

3. **Likely consequences**
   - Explain potential impact on them

4. **Measures taken**
   - What you've done to address it
   - What they should do (if anything)

**Communication Methods:**
- Direct communication (email, letter, SMS)
- Individual notification preferred
- Public communication if disproportionate effort
- Clear, not buried in other communications

### Phase 4: Containment and Remediation (Ongoing)

**Technical Measures:**

1. **Immediate containment**
   - Disable compromised accounts
   - Patch vulnerabilities
   - Change passwords/credentials
   - Isolate affected systems
   - Block unauthorized access

2. **Evidence preservation**
   - Preserve logs
   - Document system state
   - Keep backup of evidence
   - Maintain chain of custody

3. **Long-term fixes**
   - Address root causes
   - Implement additional security
   - Update systems and software
   - Review access controls

**Support for Affected Individuals:**

- Credit monitoring (if financial data involved)
- Identity theft protection
- Password reset assistance
- Dedicated helpline/support
- Regular updates on situation

### Phase 5: Documentation (Required)

**Article 33(5) Requirement:**
Document all breaches (even if not notified to authority)

**Must Record:**
- Facts of the breach
- Effects of the breach
- Remedial action taken
- Reasoning if not notified

**Purpose:**
- Demonstrate compliance
- Learn from incidents
- Enable supervisory authority verification

**Documentation Format:**

```
Breach ID: [Unique identifier]
Date Detected: [Date/time]
Date Occurred: [Estimated date/time]
Discovery Method: [How was it detected?]

Affected Data:
- Categories: [Personal data types]
- Number of records: [Approximate count]
- Number of individuals: [Approximate count]
- Special categories: [Yes/No - specify]

Breach Type: [Confidentiality/Integrity/Availability]
Cause: [How did it happen?]

Risk Assessment:
- Risk level: [Low/Medium/High]
- Rationale: [Why this level?]

Notifications:
- Supervisory Authority: [Yes/No - Date/Time]
- Data Subjects: [Yes/No - Date/Time]
- Reasoning: [Why or why not?]

Containment Measures:
- [List actions taken with dates]

Remediation:
- [Short-term fixes]
- [Long-term fixes]
- [Preventive measures]

Lessons Learned:
- [What went wrong?]
- [What worked well?]
- [Changes to implement]
```

### Phase 6: Post-Incident Review (After resolution)

**Conduct Review Meeting:**

1. **What happened?**
   - Timeline of events
   - How was it detected?
   - Response effectiveness

2. **Why did it happen?**
   - Root causes
   - Contributing factors
   - Warning signs missed

3. **What worked well?**
   - Effective response elements
   - Good practices to maintain

4. **What needs improvement?**
   - Response gaps
   - Process weaknesses
   - Technical vulnerabilities

5. **Action items**
   - Security improvements
   - Process changes
   - Training needs
   - Technology upgrades

**Update Plans and Procedures:**
- Incident response plan
- Business continuity plan
- Security policies
- Staff training

## Breach Register Template

Maintain a register of all breaches:

| Breach ID | Date | Type | Affected Data | # Individuals | Risk Level | Authority Notified | Subjects Notified | Status |
|-----------|------|------|---------------|---------------|------------|-------------------|-------------------|--------|
| BR-001 | 2025-10-15 | Confidentiality | Email addresses | ~500 | Low | No | No | Closed |
| BR-002 | 2025-10-17 | Availability | Customer records | ~10,000 | High | Yes (Oct 18) | Yes (Oct 19) | Remediation |

## Common Mistakes to Avoid

❌ **Don't:**
- Wait to notify while gathering all information
- Minimize or hide the breach
- Delay notifying to avoid bad publicity
- Fail to document even small breaches
- Ignore breaches that seem minor
- Notify too broadly without assessing risk

✅ **Do:**
- Start 72-hour clock from awareness
- Notify in phases if needed
- Be transparent with authority
- Document everything
- Learn from incidents
- Test incident response plan

## Penalties for Non-Compliance

**Article 83(4):**
- Up to €10 million OR
- 2% of global annual turnover (whichever higher)

**For:**
- Failure to notify supervisory authority (Article 33)
- Failure to notify data subjects (Article 34)
- Failure to document breaches (Article 33.5)

## Supervisory Authority Contacts

Each EU member state has a supervisory authority. Examples:

- **Germany:** Various state authorities (Landesdatenschutzbeauftragten)
- **France:** CNIL (Commission Nationale de l'Informatique et des Libertés)
- **UK:** ICO (Information Commissioner's Office)
- **Ireland:** DPC (Data Protection Commission)
- **Spain:** AEPD (Agencia Española de Protección de Datos)

Find yours: https://edpb.europa.eu/about-edpb/board/members_en

## Testing and Preparedness

**Regular Activities:**

1. **Tabletop exercises** - Quarterly
   - Simulate breach scenarios
   - Test response procedures
   - Identify gaps

2. **Incident response plan review** - Annually
   - Update contact lists
   - Review procedures
   - Incorporate lessons learned

3. **Staff training** - Ongoing
   - How to recognize breaches
   - Reporting procedures
   - Individual responsibilities

4. **Technical testing**
   - Penetration testing
   - Vulnerability scanning
   - Security audits
   - Backup restoration tests

## Breach Prevention Checklist

- [ ] Encryption at rest and in transit
- [ ] Access controls and authentication
- [ ] Regular security updates and patches
- [ ] Employee security training
- [ ] Vendor security assessments
- [ ] Network monitoring and logging
- [ ] Incident response plan in place
- [ ] Data minimization practices
- [ ] Regular backups
- [ ] Business continuity plan
- [ ] Cyber insurance coverage
- [ ] DPO or responsible person designated
