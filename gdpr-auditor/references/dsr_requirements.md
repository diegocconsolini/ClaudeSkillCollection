# Data Subject Rights (DSR) Implementation Requirements

## Overview

GDPR grants data subjects eight key rights regarding their personal data. Organizations must implement mechanisms to fulfill these rights within specified timeframes.

## Right of Access (Article 15)

### What Data Subjects Can Request

- Confirmation of whether personal data is being processed
- Access to their personal data
- The following information:
  - Purposes of processing
  - Categories of personal data
  - Recipients or categories of recipients
  - Retention period (or criteria for determining it)
  - Rights to rectification, erasure, restriction, objection
  - Right to lodge complaint with supervisory authority
  - Source of data (if not collected from data subject)
  - Existence of automated decision-making including profiling
  - Safeguards for international transfers

### Implementation Requirements

**Technical:**
- Build data export functionality
- Aggregate data from all systems/databases
- Format data in readable form (not raw database dumps)
- Include metadata about processing

**Process:**
- Verify data subject identity before providing access
- Respond within one month (extendable by two months)
- First copy must be provided free of charge
- Additional copies may incur reasonable fee

**Code Implementation Examples:**

```python
# Python example
def export_user_data(user_id):
    """Export all personal data for a user"""
    data = {
        'personal_info': get_user_profile(user_id),
        'contact_info': get_user_contacts(user_id),
        'account_history': get_user_history(user_id),
        'transactions': get_user_transactions(user_id),
        'preferences': get_user_preferences(user_id),
        'activity_logs': get_user_activity(user_id),
        'metadata': {
            'export_date': datetime.now(),
            'data_retention_period': '2 years',
            'processing_purposes': ['Service provision', 'Analytics']
        }
    }
    return json.dumps(data, indent=2)
```

## Right to Rectification (Article 16)

### What Data Subjects Can Request

- Correction of inaccurate personal data
- Completion of incomplete personal data

### Implementation Requirements

**Technical:**
- Provide edit functionality for all personal data fields
- Validate data accuracy when possible
- Propagate updates to all systems where data exists
- Log rectification requests and actions

**Process:**
- Verify identity before allowing changes
- Respond within one month
- Notify recipients of data about rectifications (if feasible)
- Allow addition of supplementary statements

**Code Implementation Examples:**

```python
# Python example
def update_user_data(user_id, field, new_value):
    """Update user personal data and log the change"""
    old_value = get_user_field(user_id, field)

    # Update main database
    update_database(user_id, field, new_value)

    # Log the rectification
    log_data_change(user_id, field, old_value, new_value,
                    reason='User rectification request')

    # Notify third parties if applicable
    notify_data_recipients(user_id, field, new_value)

    return {'status': 'success', 'field': field, 'updated': new_value}
```

## Right to Erasure / "Right to be Forgotten" (Article 17)

### When Erasure Required

- Data no longer necessary for original purpose
- Consent withdrawn and no other legal basis
- Data subject objects and no overriding legitimate grounds
- Data processed unlawfully
- Legal obligation requires deletion
- Data collected from children for information society services

### Exceptions (When Erasure Not Required)

- Freedom of expression and information
- Legal obligation or public interest
- Public health reasons
- Archiving/research/statistical purposes
- Legal claims establishment, exercise or defense

### Implementation Requirements

**Technical:**
- Hard delete or irreversible anonymization
- Delete from all systems including backups (or flag for deletion)
- Delete from third-party systems
- Remove all derived/inferred data
- Retain only minimal data for legal compliance

**Process:**
- Verify identity and eligibility for erasure
- Respond within one month
- Notify recipients about erasure
- Document reason if request denied
- Implement automated deletion schedules

**Code Implementation Examples:**

```python
# Python example
def delete_user_account(user_id, reason):
    """Permanently delete user account and personal data"""

    # Check if erasure is allowed
    if has_legal_obligation_to_retain(user_id):
        return {'status': 'denied', 'reason': 'Legal retention requirement'}

    # Delete from all tables
    delete_user_profile(user_id)
    delete_user_transactions(user_id)
    delete_user_preferences(user_id)
    delete_user_activity_logs(user_id)

    # Anonymize retained data (for legal compliance)
    anonymize_financial_records(user_id)

    # Notify third parties
    notify_data_processors_of_deletion(user_id)

    # Log deletion (without retaining personal data)
    log_account_deletion(user_id, reason, timestamp=datetime.now())

    # Schedule backup deletion
    schedule_backup_deletion(user_id)

    return {'status': 'success', 'deleted': True}
```

## Right to Restriction of Processing (Article 18)

### When Restriction Required

- Accuracy contested (during verification)
- Processing unlawful but erasure not wanted
- Data no longer needed but subject needs for legal claims
- Objection raised (pending verification of legitimate grounds)

### Implementation Requirements

**Technical:**
- Flag data as "restricted"
- Prevent processing except storage
- Allow processing only with consent or for legal claims
- Implement access controls to prevent unauthorized processing

**Process:**
- Verify identity
- Respond within one month
- Notify recipients about restriction
- Inform data subject before lifting restriction

**Code Implementation Examples:**

```python
# Python example
def restrict_data_processing(user_id, reason):
    """Restrict processing of user data"""

    # Set restriction flag
    set_user_restriction(user_id,
                        restricted=True,
                        reason=reason,
                        timestamp=datetime.now())

    # Disable automated processing
    disable_marketing(user_id)
    disable_analytics(user_id)
    disable_profiling(user_id)

    # Log restriction
    log_restriction_request(user_id, reason)

    # Notify systems
    notify_processors_of_restriction(user_id)

    return {'status': 'restricted', 'reason': reason}
```

## Right to Data Portability (Article 20)

### Scope

- Applies when:
  - Processing based on consent or contract
  - Processing carried out by automated means
- Does not apply to paper records or manual processing

### What Data Subjects Can Request

- Receive personal data in structured, commonly used, machine-readable format
- Transmit data to another controller
- Direct transmission between controllers (where technically feasible)

### Implementation Requirements

**Technical:**
- Export in standard format (JSON, CSV, XML)
- Include all personal data provided by data subject
- Include data generated by their use of service
- Provide API for direct transmission (optional but recommended)
- Ensure format is interoperable

**Process:**
- Verify identity
- Respond within one month
- Provide first export free of charge
- Should not adversely affect others' rights

**Code Implementation Examples:**

```python
# Python example
def export_portable_data(user_id, format='json'):
    """Export user data in machine-readable format"""

    data = {
        'user_provided_data': {
            'profile': get_user_profile(user_id),
            'contacts': get_user_contacts(user_id),
            'content': get_user_generated_content(user_id)
        },
        'usage_data': {
            'preferences': get_user_preferences(user_id),
            'history': get_user_history(user_id),
            'settings': get_user_settings(user_id)
        },
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'format_version': '1.0',
            'data_schema': get_schema_definition()
        }
    }

    if format == 'json':
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif format == 'csv':
        return convert_to_csv(data)
    elif format == 'xml':
        return convert_to_xml(data)
```

## Right to Object (Article 21)

### What Data Subjects Can Object To

- Processing based on legitimate interests
- Processing based on public interest
- Direct marketing (absolute right)
- Profiling related to direct marketing
- Scientific/historical research or statistics (unless public interest)

### Implementation Requirements

**Technical:**
- Provide clear opt-out mechanisms
- Implement preference center
- Honor "Do Not Track" signals (best practice)
- Stop processing immediately for marketing objections

**Process:**
- Respond within one month
- For marketing: stop immediately upon objection
- For other processing: stop unless compelling legitimate grounds
- Clearly inform about right to object

**Code Implementation Examples:**

```python
# Python example
def process_objection(user_id, objection_type):
    """Process user objection to data processing"""

    if objection_type == 'marketing':
        # Stop immediately - absolute right
        disable_all_marketing(user_id)
        unsubscribe_from_lists(user_id)
        log_marketing_objection(user_id)
        return {'status': 'stopped', 'type': 'marketing'}

    elif objection_type == 'profiling':
        disable_profiling(user_id)
        delete_user_segments(user_id)
        log_profiling_objection(user_id)
        return {'status': 'stopped', 'type': 'profiling'}

    elif objection_type == 'legitimate_interest':
        # Assess if compelling legitimate grounds exist
        if has_compelling_grounds(user_id):
            return {'status': 'denied', 'reason': 'Compelling legitimate grounds'}
        else:
            stop_legitimate_interest_processing(user_id)
            return {'status': 'stopped', 'type': 'legitimate_interest'}
```

## Right Not to be Subject to Automated Decision-Making (Article 22)

### Scope

Applies to decisions that:
- Are based solely on automated processing
- Have legal or similarly significant effects
- Include profiling

### Exceptions

- Necessary for contract
- Authorized by EU or member state law
- Based on explicit consent

### Implementation Requirements

**Technical:**
- Implement human review process for significant decisions
- Provide explanation of automated logic
- Allow data subject to express point of view
- Allow data subject to contest decision

**Process:**
- Clearly inform about automated decision-making
- Provide meaningful information about logic involved
- Explain significance and envisaged consequences
- Implement human intervention option

## Consent Management (Article 7)

### Valid Consent Requirements

- Freely given (no coercion, no bundling)
- Specific (granular, per purpose)
- Informed (clear information provided)
- Unambiguous (clear affirmative action)
- Easy to withdraw

### Implementation Requirements

**Technical:**
- Separate consent requests per purpose
- Pre-ticked boxes not allowed
- Clear consent interface
- Easy withdrawal mechanism (as easy as giving consent)
- Consent logging and audit trail

**Code Implementation Examples:**

```python
# Python example
def record_consent(user_id, purposes, method='explicit'):
    """Record user consent with audit trail"""

    consent_record = {
        'user_id': user_id,
        'timestamp': datetime.now().isoformat(),
        'purposes': purposes,  # List of specific purposes
        'method': method,  # 'explicit', 'opt_in'
        'consent_text': get_consent_text_version(),
        'ip_address': get_user_ip(),
        'user_agent': get_user_agent()
    }

    # Store consent record
    store_consent_record(consent_record)

    # Enable processing for consented purposes
    for purpose in purposes:
        enable_processing(user_id, purpose)

    return {'status': 'recorded', 'purposes': purposes}

def withdraw_consent(user_id, purposes):
    """Allow user to withdraw consent"""

    for purpose in purposes:
        disable_processing(user_id, purpose)
        log_consent_withdrawal(user_id, purpose, datetime.now())

    # Should be as easy as giving consent
    return {'status': 'withdrawn', 'purposes': purposes}
```

## Response Timeframes

All DSR requests must be responded to:
- **Within 1 month** of receiving the request
- **Extendable by 2 months** if complex (must inform data subject of extension within 1 month)
- **Free of charge** (unless manifestly unfounded or excessive)

## Identity Verification

Before fulfilling any DSR:
- Verify the identity of the data subject
- Request additional information if necessary
- Do not disclose data to wrong person
- Balance security with accessibility

## Denial of Requests

If denying a request:
- Provide reasons for refusal
- Inform about right to lodge complaint with supervisory authority
- Inform about right to judicial remedy
- Document the decision and reasoning
