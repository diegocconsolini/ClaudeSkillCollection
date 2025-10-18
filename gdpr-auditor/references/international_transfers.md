# International Data Transfers Under GDPR

## Overview

GDPR Chapter V (Articles 44-50) regulates the transfer of personal data outside the European Economic Area (EEA). Transfers are only lawful when specific conditions are met to ensure continued protection of personal data.

## What Constitutes a Transfer?

**A transfer occurs when:**
- Personal data moves from EEA to a third country (non-EEA)
- Personal data is accessed from a third country
- Remote access to personal data by staff in third countries
- Cloud storage located outside EEA
- Processing by third-party processors in third countries

**EEA includes:**
- 27 EU member states
- Iceland, Liechtenstein, Norway
- Note: UK has adequacy decision (separate rules apply)

## Legal Bases for International Transfers

### Option 1: Adequacy Decision (Article 45)

**What it is:**
European Commission determines that a third country, territory, or sector provides an "adequate" level of data protection.

**How it works:**
- If adequacy decision exists, transfer is treated like intra-EEA transfer
- No further authorization or safeguards needed
- Simple and straightforward

**Current Adequacy Decisions (as of 2025):**

**Countries with Full Adequacy:**
- Andorra
- Argentina
- Canada (commercial organizations)
- Faroe Islands
- Guernsey
- Israel
- Isle of Man
- Japan
- Jersey
- New Zealand
- Republic of Korea (South Korea)
- Switzerland
- United Kingdom
- Uruguay

**US-Specific Framework:**
- **EU-U.S. Data Privacy Framework** (2023) - Replaced Privacy Shield
  - US companies must self-certify
  - Check certification status at https://www.dataprivacyframework.gov/
  - Not all US companies are certified
  - Must verify before relying on it

**Important:**
- Adequacy decisions can be revoked (see Schrems I & II)
- Monitor EDPB and Commission announcements
- May need backup transfer mechanisms

**Implementation:**
```python
# Check if country has adequacy
adequacy_countries = [
    'Andorra', 'Argentina', 'Canada', 'Guernsey', 'Israel',
    'Isle of Man', 'Japan', 'Jersey', 'New Zealand', 'South Korea',
    'Switzerland', 'United Kingdom', 'Uruguay'
]

def can_transfer_on_adequacy(country):
    if country in adequacy_countries:
        return True
    # Check for US-EU Data Privacy Framework certification
    if country == 'United States':
        return check_dpf_certification(recipient)
    return False
```

### Option 2: Appropriate Safeguards (Article 46)

**When to use:**
No adequacy decision exists, but you can implement appropriate safeguards.

**Article 46(2) Approved Safeguards:**

#### 2a. Standard Contractual Clauses (SCCs)

**What they are:**
EU Commission-approved contract templates that impose data protection obligations on the data importer.

**Current SCCs (June 2021):**
- Module 1: Controller to Controller
- Module 2: Controller to Processor
- Module 3: Processor to Processor
- Module 4: Processor to Controller

**How to implement:**
1. Select appropriate module(s)
2. Fill in Annexes (parties, data, processing details)
3. Conduct Transfer Impact Assessment (TIA)
4. Execute contract with importer
5. Keep signed copy for records

**Transfer Impact Assessment (TIA) Required:**

Following Schrems II ruling, must assess:

1. **Laws of third country:**
   - Can government access data?
   - Are there surveillance programs?
   - What legal protections exist?
   - Any conflicts with GDPR?

2. **Practical experience:**
   - Have there been government requests?
   - How were they handled?
   - Any transparency reports?

3. **Supplementary measures:**
   - Technical measures: Encryption, pseudonymization, key management
   - Organizational measures: Policies, data minimization, access controls
   - Contractual measures: Additional clauses beyond SCCs

**Decision:**
- If third country laws undermine SCCs → Need supplementary measures
- If supplementary measures insufficient → Cannot transfer
- Document assessment thoroughly

**SCC Implementation Checklist:**
- [ ] Identify correct SCC module(s)
- [ ] Complete all required Annexes
- [ ] Conduct Transfer Impact Assessment
- [ ] Implement supplementary measures if needed
- [ ] Obtain signatures from both parties
- [ ] Document in Records of Processing Activities
- [ ] Update privacy notices
- [ ] Review periodically

#### 2b. Binding Corporate Rules (BCRs)

**What they are:**
Internal data protection policies approved by supervisory authorities for multinational corporations.

**When to use:**
- Intra-group transfers within multinational
- Transfers to affiliates, subsidiaries, offices worldwide
- Frequent, ongoing transfers

**Requirements:**
- Legally binding on all group entities
- Enforceable data subject rights
- Approved by lead supervisory authority
- Published and easily accessible

**Content requirements (Article 47):**
- Structure and contact details of group
- Data transfers and processing
- Legally binding nature
- Data subject rights
- Cooperation with supervisory authorities
- Training requirements
- Data protection principles applied
- Complaint mechanisms
- Liability provisions

**Approval process:**
- Complex and lengthy (months to years)
- Coordination with multiple authorities
- Expensive to implement
- Best for large multinationals with ongoing transfers

**Advantages:**
- One-time approval for all group transfers
- Demonstrates accountability
- Competitive advantage

**Disadvantages:**
- Time-consuming approval
- Expensive
- Must be updated when group structure changes
- Requires cooperation from all group entities

#### 2c. Approved Codes of Conduct or Certification

**Codes of Conduct (Article 40 + 46(2)(e)):**
- Industry-specific codes approved by supervisory authority
- Binding commitments on adherence
- Monitoring mechanisms required

**Certification Mechanisms (Article 42 + 46(2)(f)):**
- GDPR certification schemes
- Binding contractual clauses required
- Periodic re-certification

**Current status:**
- Limited approved codes/certifications as of 2025
- Check EDPB registry for approved schemes

#### 2d. Approved Contractual Clauses

**Ad hoc contractual clauses:**
- Custom contracts not using SCC template
- Require supervisory authority approval
- Rarely used due to approval burden
- SCCs are preferred alternative

#### 2e. Administrative Arrangements (Public Authorities)

**For public authorities only:**
- Legally binding arrangements between authorities
- Enforceable rights for data subjects
- Subject to authorization by authorities

### Option 3: Derogations (Article 49)

**When to use:**
- No adequacy decision
- No appropriate safeguards
- Specific, non-repetitive transfer
- Limited data/individuals

**Article 49(1) Derogations (in order of preference):**

#### 1. Explicit Consent (Article 49(1)(a))

**Requirements:**
- Data subject explicitly consented
- After being informed of possible risks
- Cannot be used for regular/systematic transfers

**When valid:**
- One-off transfers
- Small number of people
- Genuinely voluntary
- Informed about risks (lack of adequacy/safeguards)

**Example use case:**
- Customer booking travel to non-adequate country
- Explicitly consents to transfer of booking data

**Implementation:**
```
I explicitly consent to the transfer of my personal data
(name, booking details) to [Country] for the purpose of
processing my travel booking. I understand that [Country]
does not provide the same level of data protection as the
European Union, and that my data may not be protected to
the same standards.

[ ] Yes, I consent to this transfer
```

#### 2. Contract Performance (Article 49(1)(b))

**Two scenarios:**

**a) Contract with data subject:**
- Transfer necessary to perform contract
- Example: Shipping product to data subject in third country

**b) Pre-contractual measures:**
- At request of data subject
- Example: Providing quote for services in third country

**Requirements:**
- Genuinely necessary for contract
- Cannot use for tangential processing
- Limited to what's needed

#### 3. Public Interest (Article 49(1)(c))

**Requirements:**
- Important reasons of public interest
- Recognized in EU or member state law

**Examples:**
- International cooperation for crime prevention
- Public health emergencies
- Regulatory reporting requirements

#### 4. Legal Claims (Article 49(1)(d))

**For:**
- Establishment, exercise, or defense of legal claims

**Examples:**
- Litigation in third country
- Arbitration proceedings
- Regulatory investigations

#### 5. Vital Interests (Article 49(1)(e))

**When:**
- Necessary to protect vital interests
- Data subject physically/legally incapable of consent

**Examples:**
- Medical emergency requiring transfer
- Life-threatening situation

**Rarely applicable:**
- Very narrow scope
- Last resort only

#### 6. Public Register (Article 49(1)(f))

**For transfers from:**
- Public registers
- Information intended for public consultation

**Conditions:**
- Register accessible to general public or those with legitimate interest
- Only information registry is intended to provide
- Respect conditions for consultation

#### 7. Compelling Legitimate Interests (Article 49(1), second subparagraph)

**Last resort derogation:**
- Compelling legitimate interests
- Not repetitive
- Limited number of data subjects
- Safeguards applied
- Data subject informed
- Notified to supervisory authority

**Requirements (all must apply):**
- No other legal basis available
- Occasional/non-repetitive transfer
- Limited set of data subjects
- Necessary for compelling legitimate interests
- Overriding rights of data subject assessed
- Appropriate safeguards applied
- Information provided to data subject
- Documented and notified to supervisory authority

**Very rarely valid:**
- High bar to meet
- Must document extensively
- Supervisory authority notification required

## Schrems II Impact and Transfer Impact Assessments

### Schrems II Ruling (July 2020)

**Key holdings:**
1. Invalidated EU-U.S. Privacy Shield
2. SCCs remain valid BUT
3. Must assess third country laws
4. Implement supplementary measures if needed
5. Cannot transfer if adequate protection impossible

### Transfer Impact Assessment (TIA) Process

**Step 1: Map transfers**
- Identify all international transfers
- Document recipients and countries
- Note transfer mechanisms used

**Step 2: Verify transfer tool**
- Confirm SCCs executed correctly
- Check adequacy decision still valid
- Verify BCR approval current

**Step 3: Assess third country law**

**Questions to research:**
- What are the surveillance laws?
- Can government access data without judicial oversight?
- Are there data localization requirements?
- What legal protections exist for data subjects?
- Any conflicts with GDPR requirements?

**Resources:**
- EDPB recommendations on supplementary measures
- Country-specific legal analysis
- Vendor transparency reports
- Government surveillance reports

**Step 4: Assess practical circumstances**

- Data importer's practical experience
- Previous government access requests
- How importer responded
- Industry practices
- Likelihood of access in practice

**Step 5: Identify supplementary measures**

**Technical measures:**
- **Encryption in transit:** TLS 1.3+
- **Encryption at rest:** AES-256, controller holds keys
- **End-to-end encryption:** Importer cannot access plaintext
- **Pseudonymization:** Separate identifiers from data
- **Anonymization:** If truly anonymous, not a transfer
- **Splitting data:** Technical split preventing reconstitution
- **Multi-party computation:** Process encrypted data
- **Secure enclaves:** Trusted execution environments

**Organizational measures:**
- Data minimization
- Strict access controls
- Regular audits
- Transparency reporting
- Incident notification
- Data subject rights mechanisms
- Staff training

**Contractual measures:**
- Additional clauses beyond SCCs
- Warrant canary provisions
- Notification obligations
- Right to terminate if laws change

**Step 6: Evaluate effectiveness**

- Can supplementary measures overcome third country risks?
- Do they prevent government access in practice?
- Are they feasible and sustainable?

**Step 7: Document and decide**

- Document TIA thoroughly
- If adequate: Proceed with transfer
- If inadequate: Find alternative or suspend transfer
- Review regularly

## Practical Implementation

### For US Transfers

**Best practices:**

1. **Check DPF certification:**
   - Verify at https://www.dataprivacyframework.gov/
   - Confirm current and active
   - Note: Not all US companies certified

2. **If no DPF:**
   - Use SCCs
   - Conduct TIA for US laws (FISA 702, EO 12333, CLOUD Act)
   - Implement strong encryption
   - Consider data residency in EEA

3. **Supplementary measures for US:**
   - Client-side encryption (controller holds keys)
   - Pseudonymization with keys in EEA
   - Data segregation (US entity cannot access EU data)
   - Contractual commitments to challenge requests

### For China Transfers

**Specific considerations:**
- National Security Law
- Data Security Law
- Personal Information Protection Law (PIPL)
- Cybersecurity Law
- Data localization requirements

**Approach:**
- Conduct detailed TIA
- Implement strong technical measures
- Consider avoiding if possible
- Monitor legal developments

### For Other Third Countries

**General approach:**
1. Research local laws
2. Consult legal counsel
3. Conduct TIA
4. Implement safeguards
5. Document extensively

## Documentation Requirements

### Records to Maintain

- [ ] List of all international transfers
- [ ] Transfer mechanisms used
- [ ] SCCs (signed copies)
- [ ] Transfer Impact Assessments
- [ ] Supplementary measures implemented
- [ ] Reviews and reassessments
- [ ] Communications with supervisory authorities
- [ ] DPF certification verification (if applicable)

### Privacy Notice Requirements

Must inform data subjects about:
- That transfer occurs
- To which country
- Transfer mechanism used (adequacy, SCCs, BCR, derogation)
- How to obtain copy of safeguards (or where accessed)

## Penalties for Non-Compliance

**Article 83(5):**
- Up to €20 million OR
- 4% of global annual turnover (whichever higher)

**For violations of:**
- Transfer rules (Articles 44-49)
- Unauthorized transfers

## Review and Monitoring

**Regular activities:**

- **Quarterly:** Monitor adequacy decisions and legal developments
- **Annually:** Review and update TIAs
- **When changes occur:** Reassess if countries, laws, or circumstances change
- **Ongoing:** Monitor vendor compliance with SCCs

## Common Mistakes

❌ **Don't:**
- Assume cloud provider handles compliance
- Rely on old Privacy Shield
- Skip Transfer Impact Assessment
- Use derogations for regular transfers
- Ignore Schrems II requirements
- Forget to update privacy notices
- Miss transfers via remote access

✅ **Do:**
- Map all transfers comprehensively
- Conduct TIAs for each country
- Implement robust supplementary measures
- Document everything thoroughly
- Review regularly
- Work with legal counsel
- Consider data minimization and localization

## Quick Decision Tree

1. **Is there an adequacy decision?**
   - Yes → Transfer allowed (but monitor for revocation)
   - No → Go to 2

2. **Can you use SCCs, BCRs, or other Article 46 safeguards?**
   - Yes → Conduct TIA and implement supplementary measures
   - No → Go to 3

3. **Does a derogation apply?**
   - Yes → Ensure conditions met and document
   - No → Cannot transfer (find alternative)

## Resources

**Official Guidance:**
- EDPB Recommendations 01/2020 on supplementary measures
- EDPB Recommendations 02/2020 on EEA-relevant cases (Schrems II)
- European Commission SCCs (2021)
- National supervisory authority guidance

**Tools:**
- EDPB TIA questionnaire
- ICO international transfers guidance
- CNIL transfer tools checklist
