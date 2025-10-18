# Data Protection Impact Assessment (DPIA) Guidelines

## Overview

Article 35 GDPR requires a Data Protection Impact Assessment (DPIA) when processing is "likely to result in a high risk to the rights and freedoms of natural persons." This is a key tool for demonstrating accountability and identifying privacy risks before they materialize.

## When is a DPIA Required?

### Article 35(3): Mandatory DPIA Scenarios

A DPIA is **required** when processing involves:

1. **Systematic and extensive evaluation/profiling**
   - Automated processing including profiling
   - Based on which decisions are made
   - That produce legal effects OR similarly significantly affect the person
   - Examples: Credit scoring, automated loan decisions, algorithmic hiring

2. **Large-scale processing of special categories**
   - Special category data (Article 9): health, race, religion, etc.
   - OR criminal conviction/offence data (Article 10)
   - On a large scale
   - Examples: Hospital patient database, genetic research database

3. **Systematic monitoring of publicly accessible areas**
   - On a large scale
   - Examples: Extensive CCTV networks, smart city monitoring

### Article 35(4): Supervisory Authority Lists

Each supervisory authority publishes:
- **Mandatory list** - Processing requiring DPIA
- **Optional list** - Processing exempt from DPIA

Check your relevant supervisory authority's guidance.

### Article 35(1): General Requirement

Even if not in the three categories above, conduct DPIA if processing "likely to result in high risk"

**High Risk Indicators:**

1. **Evaluation or scoring** - Including profiling and predicting behavior
2. **Automated decision-making with legal/significant effect**
3. **Systematic monitoring** - Tracking, observing, monitoring individuals
4. **Sensitive data** - Special categories or highly personal data
5. **Large scale** - Large numbers of people affected
6. **Matching/combining datasets** - From different sources
7. **Vulnerable data subjects** - Children, employees, patients, elderly
8. **Innovative technology** - New or novel processing methods
9. **Prevents individuals from exercising rights** - Or using a service
10. **Cross-border transfers** - Outside EU without adequacy decision

**WP29 Guidance:** If two or more criteria apply, DPIA is likely required.

## When DPIA is NOT Required

### Article 35(5): Exemptions

NOT required when:

1. **Legal basis established** - Processing has legal basis in EU/member state law that:
   - Regulates the specific processing operation
   - A DPIA has already been carried out as part of a general impact assessment

2. **Before May 2018** - Processing began before May 25, 2018, and:
   - Processing operations haven't changed
   - However, good practice to review

3. **Not high risk** - Processing unlikely to result in high risk

4. **Similar processing assessed** - Already conducted DPIA for similar processing operations

## DPIA Process

### Step 1: Screen for DPIA Necessity (Before starting)

**Questions to Ask:**

- Does this processing match Article 35(3) criteria?
- Does it appear on supervisory authority's mandatory list?
- Does it meet 2+ high-risk criteria from WP29 guidance?
- Is there an exemption that applies?

**Decision:**
- ✅ DPIA required → Proceed to Step 2
- ❌ DPIA not required → Document reasoning, but consider doing one anyway for complex processing

### Step 2: Describe the Processing (Initial Phase)

**2.1 Nature of Processing**

Document:
- **Purpose** - Why are you processing this data?
- **Legal basis** - What Article 6 (and 9 if applicable) basis?
- **Data categories** - What types of personal data?
- **Data sources** - Where does data come from?
- **Data subjects** - Who does it relate to?
- **Recipients** - Who receives the data?
- **Retention** - How long will you keep it?
- **Transfers** - Any international transfers?
- **Technology** - What systems/tools are used?
- **Processors** - Third parties involved?

**2.2 Scope of Processing**

- Geographic scope
- Number of data subjects
- Volume of data
- Duration of processing
- Context and background

**2.3 Data Flows**

Map how data moves:
- Collection points
- Storage locations
- Processing systems
- Third-party transfers
- Access points
- Deletion/archiving

### Step 3: Assess Necessity and Proportionality

**Article 35(7)(b) Requirement:**
"an assessment of the necessity and proportionality of the processing operations in relation to the purposes"

**Questions to Answer:**

1. **Necessity**
   - Is this processing necessary for the stated purpose?
   - Could you achieve the purpose with less/no personal data?
   - Are there less intrusive alternatives?
   - Have you applied data minimization?

2. **Proportionality**
   - Is the processing proportionate to the purpose?
   - Are the benefits worth the privacy impact?
   - Are safeguards proportionate to risks?

**Data Minimization Check:**
- Limit data to what's needed
- Limit retention to what's necessary
- Limit access to who needs it
- Limit processing to what's required

**Alternatives Analysis:**
- Could you use aggregated data?
- Could you use pseudonymized data?
- Could you use anonymized data?
- Could you collect less data?
- Could you process less frequently?

### Step 4: Identify and Assess Risks

**Article 35(7)(c) Requirement:**
"an assessment of the risks to the rights and freedoms of data subjects"

**4.1 Identify Threats**

**Confidentiality Threats:**
- Unauthorized access (hacking, insider threats)
- Unintended disclosure (misdirected emails, misconfigurations)
- Insufficient access controls
- Inadequate encryption

**Integrity Threats:**
- Unauthorized modification
- Data corruption
- Ransomware
- Human error

**Availability Threats:**
- System failures
- DDoS attacks
- Natural disasters
- Accidental deletion

**Rights and Freedoms Threats:**
- Discrimination
- Identity theft
- Financial loss
- Reputational damage
- Physical harm
- Loss of control over personal data
- Limitation of rights
- Denial of service

**4.2 Assess Likelihood**

For each threat, assess likelihood:
- **Low** - Unlikely to occur
- **Medium** - Could occur
- **High** - Likely to occur

Consider:
- Existing controls
- Historical incidents
- Threat landscape
- Vulnerabilities present

**4.3 Assess Impact (Severity)**

If the threat materializes, what's the impact on individuals?

- **Low** - Minor inconvenience
- **Medium** - Significant impact
- **High** - Severe impact (physical harm, significant financial loss, discrimination)

Consider:
- Type of data involved
- Vulnerability of data subjects
- Number affected
- Ease of identifying individuals
- Consequences for individuals

**4.4 Calculate Risk Level**

| Likelihood/Impact | Low Impact | Medium Impact | High Impact |
|-------------------|------------|---------------|-------------|
| **High Likelihood** | Medium | High | Critical |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Low | Low | Medium |

**Focus on high and critical risks for mitigation.**

### Step 5: Identify Mitigation Measures

**Article 35(7)(d) Requirement:**
"the measures envisaged to address the risks, including safeguards, security measures and mechanisms"

**5.1 Risk Treatment Options**

For each identified risk:

1. **Mitigate** - Reduce likelihood or impact
2. **Accept** - Document why risk is acceptable
3. **Avoid** - Don't do the processing
4. **Transfer** - Insurance, contractual terms

**5.2 Technical Measures**

- **Encryption** - At rest and in transit
- **Pseudonymization** - Separate identifiers from data
- **Access controls** - RBAC, least privilege
- **Authentication** - MFA, strong passwords
- **Logging and monitoring** - Audit trails
- **Backup and recovery** - Business continuity
- **Secure development** - Security by design
- **Penetration testing** - Regular security testing
- **Data minimization** - Collect/retain only what's needed
- **Anonymization** - Where possible, make data anonymous

**5.3 Organizational Measures**

- **Policies and procedures** - Written data protection policies
- **Staff training** - Regular GDPR and security training
- **Data processing agreements** - With processors
- **Access management** - Regular review of access rights
- **Incident response plan** - Breach procedures
- **Privacy by design** - Build-in privacy from start
- **Privacy by default** - Default to most protective settings
- **DPO involvement** - Seek DPO advice
- **Regular reviews** - Periodic reassessment
- **Vendor management** - Third-party oversight

**5.4 Safeguards for Data Subjects**

- **Transparency** - Clear privacy notices
- **Consent mechanisms** - Granular, withdrawable
- **Data subject rights** - Easy to exercise
- **Opt-outs** - For direct marketing, profiling
- **Human review** - For automated decisions
- **Explanation rights** - Logic of automated processing
- **Objection rights** - Right to object clearly stated

**5.5 Residual Risk**

After mitigation:
- Reassess risk levels
- Document remaining risks
- Determine if acceptable
- If high risk remains, consult supervisory authority (Article 36)

### Step 6: Consult Stakeholders

**DPO Consultation (Article 35(2)):**
- **Mandatory** - Must seek advice of DPO
- DPO should be involved throughout
- Document DPO's advice

**Data Subject Consultation (Article 35(9)):**
- **Where appropriate** - Seek views of data subjects or their representatives
- Not always required but recommended
- Methods: Surveys, focus groups, consultations

**Other Stakeholders:**
- IT/Security teams
- Business units
- Legal counsel
- Processors
- Relevant experts

### Step 7: Approve and Sign Off

**Approval Process:**

1. **Review** - Ensure DPIA is complete and accurate
2. **Senior Management Sign-off** - Executive approval
3. **DPO Opinion** - Documented DPO assessment
4. **Decision** - Approve, modify, or reject processing

**If High Residual Risk Remains:**
- **Article 36** - Consult supervisory authority before processing
- Authority will advise within 8 weeks (14 weeks if complex)

### Step 8: Integrate into Project

**Implementation:**
- Implement mitigation measures
- Assign responsibilities
- Set timelines
- Monitor compliance
- Train staff

**Documentation:**
- Keep DPIA with Records of Processing Activities
- Make available to supervisory authority on request
- Update privacy notices
- Update contracts with processors

### Step 9: Review and Update

**When to Review:**

- **Regularly** - At least annually
- **When processing changes** - New purposes, technologies, data
- **When risks change** - New threats, incidents
- **When required** - After supervisory authority feedback

**Review Questions:**
- Is processing still necessary?
- Have risks changed?
- Are mitigation measures still effective?
- Has technology or context changed?
- Are there new legal requirements?

## DPIA Template Structure

### Cover Page
- Processing operation name
- Date of DPIA
- Version number
- Owner/responsible person
- DPO contact
- Review date

### Section 1: Description of Processing
- Purpose and context
- Nature and scope
- Legal basis
- Data categories and subjects
- Recipients and transfers
- Retention periods
- Data flow diagram

### Section 2: Necessity and Proportionality
- Justification for processing
- Data minimization assessment
- Alternatives considered
- Proportionality analysis

### Section 3: Consultation
- DPO consultation and advice
- Data subject consultation (if any)
- Other stakeholder input

### Section 4: Risk Assessment
- Risk identification
- Likelihood and impact assessment
- Risk matrix/scoring

### Section 5: Risk Mitigation
- Technical measures
- Organizational measures
- Safeguards for data subjects
- Residual risk assessment

### Section 6: Sign-off
- DPO opinion
- Management approval
- Date approved
- Next review date

### Appendices
- Data flow diagrams
- Risk register
- Supporting documentation
- Consultation records

## Article 36: Prior Consultation

**When Required:**
If DPIA shows high residual risk that cannot be mitigated

**Process:**

1. **Submit to Supervisory Authority:**
   - DPIA results
   - Measures envisaged
   - Safeguards in place
   - Why risk remains high

2. **Authority Review (Article 36(2)):**
   - Within 8 weeks
   - Can extend to 14 weeks if complex
   - Must notify of extension within 1 month

3. **Authority Advice:**
   - Written advice on processing
   - May use investigative powers
   - May impose measures, limits, or ban

4. **Follow Advice:**
   - Implement authority's recommendations
   - Or do not proceed with processing

## Common DPIA Mistakes

❌ **Don't:**
- Conduct DPIA after processing has started
- Use generic templates without customization
- Skip stakeholder consultation
- Underestimate risks
- Fail to involve DPO
- Never review or update
- Focus only on compliance, ignore data subjects' perspective

✅ **Do:**
- Start DPIA at project inception
- Tailor to specific processing
- Genuinely assess necessity and proportionality
- Consult DPO and stakeholders
- Consider data subjects' perspective
- Document all decisions
- Review regularly
- Use DPIA as tool for improvement

## DPIA Benefits

Beyond compliance:

- **Risk management** - Identify and mitigate privacy risks early
- **Cost savings** - Avoid costly redesigns or breaches
- **Trust building** - Demonstrate accountability to customers
- **Better design** - Build privacy in from the start
- **Legal protection** - Evidence of due diligence
- **Innovation enabler** - Process complex/sensitive data responsibly

## Resources and Tools

**Official Guidance:**
- EDPB Guidelines 4/2017 on DPIA (most comprehensive)
- UK ICO DPIA guidance and tools
- CNIL's DPIA methodology (PIA software)
- National supervisory authority guidance

**DPIA Tools:**
- CNIL Privacy Impact Assessment (PIA) tool
- UK ICO DPIA template
- IAPP DPIA templates
- Custom organizational templates

## DPIA Checklist

- [ ] Screening completed to determine if DPIA needed
- [ ] DPIA started before processing begins
- [ ] DPO consulted and advice sought
- [ ] Processing described comprehensively
- [ ] Data flows mapped
- [ ] Necessity and proportionality assessed
- [ ] Alternatives considered
- [ ] Risks identified for each threat
- [ ] Likelihood and impact assessed
- [ ] Risk levels calculated
- [ ] Mitigation measures identified
- [ ] Residual risk evaluated
- [ ] Data subjects consulted (where appropriate)
- [ ] Other stakeholders consulted
- [ ] Sign-off obtained from management
- [ ] If high residual risk: supervisory authority consulted
- [ ] DPIA documented and filed
- [ ] Mitigation measures implemented
- [ ] Review date set
- [ ] Privacy notices updated
- [ ] Records of processing updated
