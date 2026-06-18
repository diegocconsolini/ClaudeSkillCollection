---
name: org-compliance-context
description: Organization-specific compliance rules and constraints for this project (fill in)
metadata:
  type: project
---

Fill in the org-specific compliance context that Claude should respect in this project.
Delete the placeholders that don't apply.

**Frameworks in scope:** _(e.g. GDPR, SOC 2 Type II, ISO 27001, HIPAA)_

**Data handling constraints:**
- Personal data categories present: _(...)_
- Data residency / region: _(...)_
- Retention rules: _(...)_

**Reporting / notification clocks:**
- GDPR Art. 33: 72h breach notification to the supervisory authority.
- HIPAA Breach Notification Rule: 60 days.

**Hard don'ts:** _(e.g. never commit customer data; never disable encryption-at-rest config)_

**How to apply:** treat these as constraints on any code change, audit, or report in this
project; surface a conflict rather than silently violating one.
