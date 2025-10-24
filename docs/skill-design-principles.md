# Claude Skills Design Principles

**Version:** 2.0
**Last Updated:** 2025-10-18
**Based On:** Research of existing skills (docx, pptx, xlsx, pdf)

---

## What Claude Skills Actually Are

Based on extensive research of production skills:

### ✅ Claude Skills ARE:

1. **Document Generators**
   - Create specific file types (DOCX, XLSX, PDF, HTML)
   - Transform data into formatted deliverables
   - Use templates extensively

2. **Workflow Guides**
   - Step-by-step instructions
   - Decision trees for different scenarios
   - Clear input → process → output paths

3. **Template Systems**
   - Reusable patterns and clauses
   - Modular components
   - Jurisdiction/industry variations

4. **Format Converters**
   - Transform between file types
   - Maintain structure and styling
   - Preserve metadata

5. **Code Libraries**
   - Manipulate file structures
   - Generate implementation code
   - Provide working examples

### ❌ Claude Skills ARE NOT:

1. **Analysis Tools**
   - Cannot scan live systems
   - Cannot access databases
   - Cannot evaluate running code

2. **External Services**
   - No API calls to external services
   - No real-time data fetching
   - Self-contained only

3. **Monitoring Systems**
   - No continuous observation
   - No change detection
   - No alerting mechanisms

4. **Assessment Tools**
   - No subjective judgments
   - No risk calculations
   - No compliance certifications

5. **Simple Calculators**
   - Must produce documents, not just answers
   - Must involve significant logic/templates
   - Must save substantial time

---

## The Document Generation Paradigm

### Core Pattern

```
User Input → Template Selection → Data Assembly → Format Generation → Output File(s)
```

### What This Means

**Good Skill Design:**
- "Generate privacy policy from questionnaire"
- "Create incident response playbook from scenarios"
- "Build vendor assessment report from completed questionnaire"

**Bad Skill Design:**
- "Scan code for GDPR violations"
- "Analyze security posture"
- "Calculate compliance score"

---

## Success Metrics for Skills

### A Successful Skill:

1. **Generates Tangible Files**
   - Actual DOCX/XLSX/PDF/HTML files
   - Not just advice or recommendations
   - Ready to use without additional work

2. **Uses Templates Extensively**
   - Pre-built structures
   - Modular components
   - Proven patterns

3. **Follows Clear Workflows**
   - Questionnaire-based input
   - Step-by-step generation
   - Predictable outputs

4. **Includes Working Code**
   - Actual implementation scripts
   - Tested generation logic
   - Complete examples

5. **Provides Multiple Formats**
   - DOCX for editing
   - PDF for sharing
   - HTML for web
   - JSON for integration

6. **Is Deterministic**
   - Same inputs = same outputs
   - No random variations
   - Reproducible results

7. **Avoids Subjective Decisions**
   - Templates encode expertise
   - Rules-based logic
   - User makes judgment calls

---

## Skill Architecture Template

### Directory Structure

```
/skill_name/
├── SKILL.md              # Main skill documentation
├── LICENSE.txt           # License information
├── templates/            # Document templates
│   ├── base/            # Base templates
│   ├── jurisdictions/   # Region-specific
│   └── industries/      # Industry-specific
├── generators/          # Generation scripts
│   ├── generator.py     # Main generator
│   ├── formatter.py     # Output formatting
│   └── utilities.py     # Helper functions
├── questionnaires/      # Input templates
│   ├── basic.yaml       # Basic questionnaire
│   └── advanced.yaml    # Detailed questionnaire
├── examples/            # Example outputs
│   ├── sample.docx
│   ├── sample.pdf
│   └── sample.html
└── tests/              # Test suite
    ├── test_generator.py
    └── test_templates.py
```

### SKILL.md Structure

```markdown
---
name: skill_name
description: "What documents it creates and when to use it"
license: MIT
---

# Skill Name

## Overview
[Brief description of document generation capabilities]

## Workflow Decision Tree
[When to use different generation paths]

## Document Generation

### Workflow
1. **READ DOCUMENTATION**: [Required reading]
2. **GATHER INFORMATION**: [Questionnaire/inputs]
3. **GENERATE**: [Generation process]
4. **FORMAT**: [Output options]

## Templates
[Template library organization]

## Code Guidelines
[Generation script patterns]

## Dependencies
[Required packages]

## Examples
[Sample outputs and use cases]
```

---

## Value Proposition Framework

### High-Value Skills:

**Characteristics:**
- Save 10+ hours of manual work
- Required by regulations/standards
- Complex enough to need automation
- Frequently needed

**Examples:**
- Privacy policy generation (20+ hours saved)
- Security policy suite (40+ hours saved)
- Incident response playbooks (15+ hours saved)

### Medium-Value Skills:

**Characteristics:**
- Save 3-10 hours
- Standardized but not complex
- Periodic need

**Examples:**
- Breach notification letters (5 hours saved)
- Cookie policies (3 hours saved)
- Data retention schedules (8 hours saved)

### Low-Value Skills:

**Characteristics:**
- Save < 3 hours
- Too simple (just lookups)
- Rare need

**Examples:**
- Standards reference lookup
- Compliance calendar
- Simple checklists

---

## Common Pitfalls to Avoid

### 1. The Analysis Trap

**Bad:** "This skill scans your codebase for vulnerabilities"
**Good:** "This skill generates security assessment questionnaires"

**Why:** Skills can't actually scan systems; they can create templates for humans to use.

### 2. The API Dependency Trap

**Bad:** "This skill fetches threat intelligence from VirusTotal"
**Good:** "This skill generates threat intelligence report templates"

**Why:** Skills are self-contained; they can't call external APIs.

### 3. The Judgment Trap

**Bad:** "This skill calculates your security maturity score"
**Good:** "This skill generates maturity assessment frameworks"

**Why:** Skills shouldn't make subjective assessments; they provide structures for humans to complete.

### 4. The Simplicity Trap

**Bad:** "This skill tells you which encryption algorithm to use"
**Good:** "This skill generates encryption implementation guides with code"

**Why:** Skills must generate documents, not just provide simple answers.

### 5. The Scope Creep Trap

**Bad:** "This skill does GDPR compliance, privacy policies, security audits, and threat modeling"
**Good:** "This skill generates GDPR compliance documentation"

**Why:** Each skill should have a focused purpose with clear deliverables.

---

## Testing Your Skill Concept

### The Document Test

**Question:** "Does this skill generate actual document files?"

- ✅ Yes → Good candidate
- ❌ No → Reconsider

### The Template Test

**Question:** "Can most of the output come from pre-built templates?"

- ✅ Yes → Good candidate
- ❌ No → May be too custom/complex

### The Value Test

**Question:** "Does this save users 5+ hours of manual work?"

- ✅ Yes → Good candidate
- ❌ No → May not be worth building

### The Self-Contained Test

**Question:** "Can this work without external APIs or live system access?"

- ✅ Yes → Good candidate
- ❌ No → Not suitable as skill

### The Determinism Test

**Question:** "Will the same inputs always produce similar outputs?"

- ✅ Yes → Good candidate
- ❌ No → Too subjective/variable

---

## Best Practices

### 1. Start with Templates

- Collect comprehensive template library BEFORE coding
- Get legal/expert review of templates
- Version templates separately from code

### 2. Build Robust Questionnaires

- Cover all scenarios with branching logic
- Provide clear examples for each question
- Validate inputs before generation

### 3. Generate Multiple Formats

- Always provide DOCX for editing
- Include PDF for distribution
- Add HTML for web integration
- Consider JSON for data integration

### 4. Include Complete Examples

- Show what good output looks like
- Provide multiple scenarios
- Include edge cases

### 5. Document Limitations Clearly

- State what skill CAN'T do
- Explain when to seek professional help
- Clarify disclaimers upfront

### 6. Design for Extensibility

- Make templates easy to update
- Allow custom template additions
- Support multiple jurisdictions/industries

### 7. Test Thoroughly

- Test all questionnaire paths
- Verify output formatting
- Check multiple scenarios
- Validate against regulations

---

## Skill Quality Checklist

Before releasing a skill, verify:

### Functionality
- [ ] Generates actual files (not just advice)
- [ ] Uses comprehensive templates
- [ ] Follows clear workflow
- [ ] Includes working code examples
- [ ] Produces multiple formats

### Documentation
- [ ] Clear SKILL.md with workflow
- [ ] Comprehensive README
- [ ] Example outputs included
- [ ] Limitations clearly stated
- [ ] Installation instructions complete

### Code Quality
- [ ] Scripts are tested
- [ ] Error handling implemented
- [ ] Type hints included
- [ ] Docstrings complete
- [ ] Dependencies minimal

### Legal/Compliance
- [ ] Disclaimers included
- [ ] Sources cited
- [ ] License clear
- [ ] No false claims
- [ ] Professional review (if applicable)

### User Experience
- [ ] < 5 minutes to complete questionnaire
- [ ] < 2 minutes to generate documents
- [ ] Output is professional quality
- [ ] Works on multiple platforms
- [ ] Clear error messages

---

## Version History

- **v1.0** - Initial principles based on assumptions
- **v2.0** - Complete refinement based on research of production skills (docx, pptx, xlsx, pdf)

---

## References

- Claude Code Skills Documentation
- Existing skills: docx, pptx, xlsx, pdf
- Real-world skill usage patterns
- User feedback and adoption data
