# Legal Bases for Processing Personal Data

## Overview

Under GDPR Article 6, processing personal data is lawful only if at least one of six legal bases applies. The controller must determine the appropriate legal basis **before** processing begins and document this decision.

## The Six Legal Bases (Article 6.1)

### 1. Consent (Article 6.1(a))

**Definition:** The data subject has given consent to the processing of their personal data for one or more specific purposes.

**When to Use:**
- Optional processing activities
- Marketing and promotional communications
- Non-essential cookies and tracking
- Sharing data with third parties for their purposes
- Any processing where other legal bases don't apply

**Requirements:**
- Freely given (no coercion, imbalance of power considered)
- Specific (separate consent for different purposes)
- Informed (clear information about what they're consenting to)
- Unambiguous (clear affirmative action required)
- Easy to withdraw (as easy as giving consent)
- Documented (proof of consent must be kept)

**Advantages:**
- Gives individuals control
- Demonstrates transparency
- Appropriate for optional activities

**Disadvantages:**
- Can be withdrawn at any time
- Cannot be used if there's imbalance of power (e.g., employer-employee)
- Cannot be bundled with other terms and conditions
- Requires ongoing management

**Examples:**
- Newsletter subscriptions
- Marketing emails
- Analytics cookies
- Social media integrations
- Data sharing with partners

**Implementation:**
```python
# Consent must be granular and documented
consent_record = {
    'purpose': 'marketing_emails',
    'timestamp': '2025-10-17T10:30:00Z',
    'method': 'opt_in_checkbox',
    'consent_text': 'I agree to receive marketing emails',
    'ip_address': '192.0.2.1',
    'can_withdraw': True
}
```

### 2. Contract (Article 6.1(b))

**Definition:** Processing is necessary for the performance of a contract to which the data subject is party, or to take steps at the request of the data subject prior to entering into a contract.

**When to Use:**
- Delivering products or services the individual has requested
- Processing payments
- Managing customer accounts
- Pre-contractual steps (e.g., providing quotes)

**Requirements:**
- Genuine contractual necessity
- Processing must be objectively necessary
- Cannot use this basis for optional extras
- Must be processing to fulfill your obligations or their requests

**Advantages:**
- Does not require consent
- Cannot be withdrawn while contract is active
- Straightforward to explain

**Disadvantages:**
- Limited to contract performance only
- Cannot use for secondary purposes
- Must be genuinely necessary

**Examples:**
- Processing customer name and address to deliver purchased goods
- Processing payment information to complete transactions
- Creating user accounts for online services
- Processing booking information for reservations

**Not Valid For:**
- Marketing (even to existing customers)
- Analytics beyond service improvement
- Sharing data with partners for their purposes

### 3. Legal Obligation (Article 6.1(c))

**Definition:** Processing is necessary for compliance with a legal obligation to which the controller is subject.

**When to Use:**
- Complying with legal requirements under EU or member state law
- Responding to lawful requests from authorities
- Meeting statutory obligations

**Requirements:**
- Must be a clear legal obligation
- Obligation must be in EU or member state law
- Must be necessary to comply

**Advantages:**
- Clear basis for processing
- Cannot be objected to by data subject
- Straightforward to justify

**Disadvantages:**
- Very limited scope
- Cannot use for voluntary compliance
- Must be able to cite specific legal provision

**Examples:**
- Tax record keeping
- Employment law compliance (e.g., payroll records)
- Health and safety reporting
- Anti-money laundering checks
- Responding to court orders

### 4. Vital Interests (Article 6.1(d))

**Definition:** Processing is necessary to protect the vital interests of the data subject or another natural person.

**When to Use:**
- Life or death situations
- Protecting someone from serious harm
- Emergency situations where consent cannot be obtained

**Requirements:**
- Must be genuinely necessary to protect vital interests
- Usually life or death situations
- Should be used as last resort
- Other legal bases don't apply

**Advantages:**
- Allows processing in emergencies
- Protects life and health

**Disadvantages:**
- Very narrow scope
- Rarely applicable
- Cannot be used for routine processing

**Examples:**
- Emergency medical treatment without consent
- Sharing medical data during medical emergency
- Natural disaster response
- Preventing harm to vulnerable individuals

**Not Valid For:**
- Routine health data processing (use consent or legal obligation)
- General safety measures
- Non-emergency situations

### 5. Public Task (Article 6.1(e))

**Definition:** Processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller.

**When to Use:**
- Public authorities performing statutory functions
- Bodies exercising official authority
- Tasks carried out in the public interest

**Requirements:**
- Must have a basis in EU or member state law
- Must be performing public task or exercising official authority
- Processing must be necessary for the task

**Advantages:**
- Appropriate for public sector
- Clear legal basis
- Cannot be objected to in most cases

**Disadvantages:**
- Limited to public authorities or official tasks
- Must have clear legal basis
- Private sector rarely can use this

**Examples:**
- Government service delivery
- Law enforcement activities
- Public health monitoring
- Educational institutions (in some cases)
- Regulatory functions

### 6. Legitimate Interests (Article 6.1(f))

**Definition:** Processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject.

**When to Use:**
- Processing in the interests of the controller or third party
- Where there's a good reason and minimal privacy impact
- After balancing against individual's rights

**Requirements:**
- **Three-part test:**
  1. **Purpose test:** Is there a legitimate interest?
  2. **Necessity test:** Is the processing necessary?
  3. **Balancing test:** Do individual's interests override yours?
- Must document the balancing assessment (Legitimate Interest Assessment - LIA)
- Individuals have right to object

**Advantages:**
- Flexible
- Doesn't require consent
- Appropriate for many business activities

**Disadvantages:**
- Requires careful balancing assessment
- Can be objected to
- More complex to justify
- Not available for public authorities in performance of tasks

**Examples:**
- Fraud prevention and detection
- Network and information security
- Internal administrative purposes
- Direct marketing to existing customers (with easy opt-out)
- CCTV for security purposes
- Sharing data within corporate group

**Not Valid For:**
- Children's data (usually)
- Special category data (Article 9)
- Processing that's intrusive or unexpected
- Where individual's interests clearly override

**Balancing Assessment Factors:**

Consider:
- Nature of the personal data
- Reasonable expectations of data subjects
- Likely impact on data subjects
- Safeguards in place
- Transparency of processing
- Status of controller (e.g., public authority vs private company)

## Special Categories (Article 9)

For **special category data** (race, health, biometric, etc.), Article 6 legal basis is **not sufficient**. Must also have an Article 9(2) condition:

- Explicit consent (Article 9.2(a))
- Employment/social security law (Article 9.2(b))
- Vital interests when consent impossible (Article 9.2(c))
- Legitimate activities of foundations/associations (Article 9.2(d))
- Made public by data subject (Article 9.2(e))
- Legal claims or judicial acts (Article 9.2(f))
- Substantial public interest (Article 9.2(g))
- Health/social care (Article 9.2(h))
- Public health (Article 9.2(i))
- Research/statistics (Article 9.2(j))

## Children's Data

For children's data (information society services):
- Consent from parent/guardian required if under 16 (member states can lower to 13)
- Legitimate interests less likely to apply
- Higher bar for demonstrating lawfulness

## Switching Legal Bases

- Generally should not switch legal bases
- If circumstances genuinely change, may switch with proper documentation
- Must inform data subjects of change
- Cannot switch to avoid individual's rights (e.g., from consent to legitimate interests to avoid withdrawal)

## Documenting Legal Basis

For each processing activity, document:
- What legal basis applies
- Why it's appropriate
- How you determined it was necessary
- Balancing assessment (if legitimate interests)
- How you keep this under review

## Common Mistakes

❌ **Wrong:**
- Using consent when there's imbalance of power
- Using contract for non-essential processing
- Using legitimate interests without balancing assessment
- Trying to switch from consent to another basis to avoid withdrawal
- Not documenting legal basis decision

✅ **Right:**
- Choose most appropriate legal basis before processing
- Document decision-making process
- Be transparent with data subjects
- Review legal basis regularly
- Respect individual rights associated with each basis

## Decision Tree

1. **Is it required by law?** → Legal obligation
2. **Is it necessary for a contract with the individual?** → Contract
3. **Is it a life or death emergency?** → Vital interests
4. **Are you a public authority performing a statutory function?** → Public task
5. **Do you have a legitimate interest that outweighs individual's rights?** → Legitimate interests
6. **Is it optional or none of the above apply?** → Consent

## Compliance Checklist

- [ ] Legal basis identified before processing begins
- [ ] Legal basis documented in records of processing activities (Article 30)
- [ ] Legal basis communicated to data subjects (Article 13/14)
- [ ] Balancing assessment completed (if legitimate interests)
- [ ] Consent mechanisms comply with Article 7 (if consent)
- [ ] Special category conditions checked (if applicable)
- [ ] Children's data requirements met (if applicable)
- [ ] Legal basis reviewed regularly
- [ ] Staff trained on applying legal bases correctly
