# Plugin Testing Checklist Template

**Plugin Name:** [Name]
**Version:** [Version]
**Tester:** Diego Consolini
**Date Started:** 2025-XX-XX
**Date Completed:** 2025-XX-XX

---

## Design Validation

- [ ] **Produces tangible deliverable** (report, document, config file, etc.)
- [ ] **Works with static files** (no live system access required)
- [ ] **Follows systematic workflow** (clear step-by-step process)
- [ ] **Based on objective criteria** (regulations, standards, best practices)
- [ ] **Includes reference materials** (authoritative sources, templates)

**Notes:**
[Any notes on design validation]

---

## Functional Testing

### Scripts
- [ ] Script 1: [name] works correctly
- [ ] Script 2: [name] works correctly
- [ ] Script 3: [name] works correctly
- [ ] All scripts have --help option
- [ ] All scripts handle errors gracefully
- [ ] All scripts produce expected output

### Claude Integration
- [ ] SKILL.md loads correctly
- [ ] Claude follows workflow as designed
- [ ] Generates expected deliverable format
- [ ] Includes specific references (file:line numbers)
- [ ] Cites authoritative sources correctly
- [ ] Output is actionable and clear

**Notes:**
[Any notes on functional testing]

---

## Documentation Testing

### SKILL.md
- [ ] Clear purpose statement
- [ ] "When to use" section complete
- [ ] "When NOT to use" section complete
- [ ] Complete workflow documented
- [ ] Reference materials listed
- [ ] Output format specified
- [ ] Defensive security note included
- [ ] Example usage shown
- [ ] Limitations documented

### plugin.json
- [ ] Correct plugin name
- [ ] Accurate version number
- [ ] Clear description
- [ ] Author info correct
- [ ] Keywords relevant
- [ ] Category appropriate
- [ ] Agent configured correctly
- [ ] Valid JSON format

### README.md
- [ ] Version number correct
- [ ] Feature list complete
- [ ] Installation instructions work
- [ ] Usage examples accurate
- [ ] Script documentation complete
- [ ] Limitations clearly stated
- [ ] Requirements listed
- [ ] Disclaimer included
- [ ] License mentioned (MIT)

### Reference Materials
- [ ] All sources cited with URLs
- [ ] URLs verified (not broken)
- [ ] Content accurate and verified
- [ ] Publication dates included
- [ ] Up-to-date information
- [ ] No placeholders or TODOs

**Notes:**
[Any documentation issues found]

---

## Quality Standards

### Code Quality
- [ ] No malicious code
- [ ] Defensive security only
- [ ] Error handling in all scripts
- [ ] Type hints in Python code
- [ ] Docstrings for functions
- [ ] Follows PEP 8 (Python) or relevant style guide
- [ ] No hardcoded credentials or secrets
- [ ] No external API dependencies (or minimal/optional)

### Content Quality
- [ ] Authoritative sources cited
- [ ] No hallucinated facts
- [ ] No fake examples
- [ ] Clear and professional writing
- [ ] Technical accuracy verified
- [ ] No broken links
- [ ] No placeholder text ("TODO", "Coming soon", etc.)

**Issues Found:**
[List any quality issues]

---

## Real-World Testing

### Test Codebase 1
- **Name:** [Codebase name]
- **Description:** [Brief description]
- **Size:** [Number of files, LOC]
- **Result:** [ ] Pass / [ ] Fail
- **Findings:** [Number of issues found]
- **Accuracy:** [ ] All accurate / [ ] Some false positives / [ ] Missed issues
- **Notes:**
  [Detailed notes on this test]

### Test Codebase 2
- **Name:** [Codebase name]
- **Description:** [Brief description]
- **Size:** [Number of files, LOC]
- **Result:** [ ] Pass / [ ] Fail
- **Findings:** [Number of issues found]
- **Accuracy:** [ ] All accurate / [ ] Some false positives / [ ] Missed issues
- **Notes:**
  [Detailed notes on this test]

### Test Codebase 3
- **Name:** [Codebase name]
- **Description:** [Brief description]
- **Size:** [Number of files, LOC]
- **Result:** [ ] Pass / [ ] Fail
- **Findings:** [Number of issues found]
- **Accuracy:** [ ] All accurate / [ ] Some false positives / [ ] Missed issues
- **Notes:**
  [Detailed notes on this test]

**Summary:**
- Total codebases tested: X
- Total issues found: X
- False positives: X
- Missed issues: X
- Overall accuracy: X%

---

## Edge Cases

- [ ] **Empty codebase** - Handles gracefully
- [ ] **Very large codebase** (10k+ files) - Completes in reasonable time
- [ ] **No issues found** - Generates appropriate report
- [ ] **Many issues found** (100+) - Doesn't crash, handles large output
- [ ] **Non-standard file structure** - Still works
- [ ] **Multiple languages** - Handles appropriately
- [ ] **Binary files** - Skips or handles correctly
- [ ] **Large files** (10k+ lines) - Doesn't crash
- [ ] **Special characters** in filenames - Handles correctly
- [ ] **Missing directories** - Error handling works

**Edge Case Notes:**
[Details on edge case handling]

---

## Performance

- [ ] **Small codebase** (<100 files) - Completes in <1 minute
- [ ] **Medium codebase** (100-1000 files) - Completes in <5 minutes
- [ ] **Large codebase** (1000-10k files) - Completes in <15 minutes
- [ ] **Memory usage** - Stays under 500MB for typical use
- [ ] **CPU usage** - Reasonable (doesn't peg CPU)
- [ ] **Progress indication** - User knows it's working

**Performance Metrics:**
- Small test: X seconds
- Medium test: X seconds
- Large test: X minutes
- Peak memory: X MB

**Notes:**
[Any performance issues or optimizations needed]

---

## Security

- [ ] No secrets or credentials in code
- [ ] No external network calls (or clearly documented)
- [ ] File operations are safe (no arbitrary file access)
- [ ] Input validation present
- [ ] No code execution of untrusted input
- [ ] Defensive security principles followed
- [ ] No offensive security capabilities

**Security Notes:**
[Any security concerns or validations]

---

## User Experience

- [ ] Clear output formatting
- [ ] Helpful error messages
- [ ] Actionable recommendations
- [ ] Easy to understand for non-experts
- [ ] Professional presentation
- [ ] Consistent terminology
- [ ] No jargon without explanation

**UX Notes:**
[Any user experience observations]

---

## Compatibility

- [ ] **Python 3.8** - Works
- [ ] **Python 3.9** - Works
- [ ] **Python 3.10** - Works
- [ ] **Python 3.11** - Works
- [ ] **Python 3.12** - Works
- [ ] **macOS** - Works
- [ ] **Linux** - Works
- [ ] **Windows** (WSL) - Works

**Compatibility Notes:**
[Any compatibility issues]

---

## Issues Found

### Critical Issues
[List any critical issues that must be fixed before release]

1. [Issue description]
   - Severity: Critical
   - Impact: [Description]
   - Fix required: [Yes/No]
   - Status: [Open/Fixed]

### High Priority Issues
[List high priority issues]

### Medium Priority Issues
[List medium priority issues]

### Low Priority Issues
[List low priority issues or nice-to-haves]

---

## Fixes Applied

1. [Date] - [Issue description] - [Solution]
2. [Date] - [Issue description] - [Solution]

---

## Final Sign-off

### Ready for Release?
- [ ] **YES** - All critical issues resolved
- [ ] **NO** - Outstanding issues (list below)

### Outstanding Issues
[List any remaining issues that need resolution]

### Release Recommendation
- [ ] **Recommend release** - Production ready
- [ ] **Recommend delay** - Needs more work
- [ ] **Recommend rejection** - Fundamental issues

### Tester Notes
[Final thoughts, recommendations, or observations]

---

### Sign-off
- **Tested by:** Diego Consolini
- **Date:** 2025-XX-XX
- **Version tested:** X.X.X
- **Status:** [ ] Approved / [ ] Needs work / [ ] Rejected
- **Signature:** ___________________

---

**Testing Checklist Version:** 1.0
**Last Updated:** 2025-10-19
