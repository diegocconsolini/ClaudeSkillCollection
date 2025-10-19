# Testing Instructions - Incident Response Playbook Creator

**Version**: 1.0.0
**Date**: 2025-10-20
**Status**: Ready for Testing

---

## 🔧 Important: Fixes Applied

**Two critical issues were fixed on 2025-10-20**:

1. **Plugin Location**: Plugin was in wrong directory (`ClaudeSkillCollection-Private/wip-plugins/`)
   - **Fixed**: Moved to `ClaudeSkillCollection/private/wip-plugins/` where Claude Code scans for plugins

2. **Plugin Structure**: `plugin.json` was using incorrect field structure
   - **Fixed**: Changed to use `agents` array with `prompt: "./SKILL.md"` (matching gdpr-auditor structure)

---

## 🎯 Quick Test (2 minutes)

### Option 1: Fresh Claude Code Session

1. **Open a NEW Claude Code session** (not this one - the plugin needs to load fresh)
2. Type exactly:
   ```
   Create an incident response playbook for ransomware attacks
   ```
3. **Expected behavior**:
   - Plugin should auto-load
   - You should see AskUserQuestion prompts appear
   - Claude will ask for your organization name and industry
   - A playbook will be generated in the `output/` directory

### Option 2: Command Line Testing

```bash
cd /Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection/private/wip-plugins/incident-response-playbook-creator

# Test 1: List scenarios
python3 scripts/browse_scenarios.py --list

# Test 2: View ransomware details
python3 scripts/browse_scenarios.py --detail ransomware

# Test 3: Generate a playbook
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "Test Corp" \
  --industry "Technology"
```

---

## 📋 Full Testing Checklist

### 1. Plugin Auto-Loading Test

**In a FRESH Claude Code session**, try these prompts:

- ✅ "Create an incident response playbook for ransomware attacks"
- ✅ "I need IR documentation for data breaches"
- ✅ "Generate phishing incident response procedures"
- ✅ "Help me prepare for a DDoS attack" (should mention limited scenarios)

**Expected**: Plugin loads automatically and guides you through playbook creation

### 2. Interactive Workflow Test

When the plugin loads, verify:

- ✅ AskUserQuestion appears for scenario selection
- ✅ AskUserQuestion appears for organization name
- ✅ AskUserQuestion appears for industry sector
- ✅ Optional contact information prompt works
- ✅ Playbook generates successfully
- ✅ Output file location is shown

### 3. Script Functionality Tests

```bash
# Browse scenarios
python3 scripts/browse_scenarios.py --list
python3 scripts/browse_scenarios.py --detail ransomware
python3 scripts/browse_scenarios.py --detail data_breach
python3 scripts/browse_scenarios.py --detail phishing
python3 scripts/browse_scenarios.py --metadata

# Generate playbooks for all scenarios
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware --org "Test Org" --industry "Technology"

python3 scripts/generate_playbook_markdown.py \
  --scenario data_breach --org "Healthcare Inc" --industry "Healthcare"

python3 scripts/generate_playbook_markdown.py \
  --scenario phishing --org "Finance Corp" --industry "Finance"
```

### 4. Content Quality Tests

Open any generated playbook (`output/*.md`) and verify:

- ✅ Organization name appears correctly throughout
- ✅ Industry is mentioned
- ✅ All major sections are present:
  - Overview
  - Detection & Indicators
  - Response Procedures (Triage, Containment, Eradication)
  - Recovery Actions
  - Communication Requirements
  - Compliance Considerations (GDPR + HIPAA)
  - Roles & Responsibilities
  - Contact Information
  - Post-Incident Activities

- ✅ NIST SP 800-61r3 references are present
- ✅ NIST CSF 2.0 categories mentioned (DE.CM, DE.AE, RS, RC)
- ✅ GDPR Article 33/34 with 72-hour timeline
- ✅ HIPAA 60-day notification timeline
- ✅ No placeholder/mock data
- ✅ Professional formatting

### 5. Edge Case Tests

```bash
# Test with special characters in org name
python3 scripts/generate_playbook_markdown.py \
  --scenario ransomware \
  --org "Acme & Co., Inc." \
  --industry "Technology"

# Test with custom output path
python3 scripts/generate_playbook_markdown.py \
  --scenario data_breach \
  --org "Custom Corp" \
  --output /tmp/test-playbook.md

# Test with contact information
python3 scripts/generate_playbook_markdown.py \
  --scenario phishing \
  --org "Contact Test" \
  --contact-email "security@test.com" \
  --contact-phone "+1-555-TEST-SEC"

# Test error handling - invalid scenario
python3 scripts/generate_playbook_markdown.py \
  --scenario invalid_scenario \
  --org "Test"
# Expected: Error message listing valid scenario IDs
```

---

## 🐛 Troubleshooting

### Issue: Plugin doesn't load in fresh session

**Symptoms**: When you say "Create an incident response playbook for ransomware", Claude starts planning manually instead of using the plugin.

**Possible Causes**:
1. Plugin location - Check that it's in the correct directory
2. Session not fresh - Make sure you're in a NEW Claude Code session
3. Trigger phrase mismatch - Try exact phrases from SKILL.md

**Debugging Steps**:
```bash
# Verify plugin.json is valid
python3 -m json.tool plugin.json

# Check SKILL.md exists
ls -la SKILL.md

# Verify directory structure
tree -L 2
```

### Issue: Scripts fail with "ModuleNotFoundError"

**Solution**:
```bash
pip install jinja2 pyyaml pandas openpyxl
```

### Issue: "Scenario not found" error

**Solution**:
```bash
# List available scenarios
python3 scripts/generate_playbook_markdown.py --list

# Use one of: ransomware, data_breach, phishing
```

---

## 📊 Test Results Template

Use this template to report your test results:

```
## Test Results - [Your Name] - [Date]

### Plugin Auto-Loading
- [ ] Loaded automatically in fresh session: YES / NO
- [ ] Trigger phrase used: "_______________"
- [ ] AskUserQuestion appeared: YES / NO

### Playbook Generation
- [ ] Ransomware playbook generated: YES / NO / ERRORS
- [ ] Data breach playbook generated: YES / NO / ERRORS
- [ ] Phishing playbook generated: YES / NO / ERRORS

### Content Quality
- [ ] All sections present: YES / NO
- [ ] NIST references accurate: YES / NO
- [ ] GDPR compliance correct: YES / NO
- [ ] HIPAA compliance correct: YES / NO
- [ ] Organization customization works: YES / NO

### Issues Encountered
- Issue 1: [Description]
- Issue 2: [Description]

### Overall Rating
- [ ] Ready for production use
- [ ] Needs minor fixes
- [ ] Needs major fixes

### Comments
[Your feedback here]
```

---

## 📞 Support

If you encounter issues:

1. Check READY_FOR_TESTING.md for known issues
2. Review CORRECTIONS_APPLIED.md for error history
3. Check README.md for usage documentation
4. Examine SKILL.md for workflow details

---

## ✅ Success Criteria

The plugin passes testing if:

1. ✅ Loads automatically in fresh Claude Code sessions
2. ✅ Interactive workflow (AskUserQuestion) works smoothly
3. ✅ All 3 scenarios generate valid playbooks
4. ✅ Content is professional and authoritative (no mock data)
5. ✅ GDPR and HIPAA compliance information is accurate
6. ✅ Organization customization works correctly
7. ✅ No Python errors or crashes
8. ✅ Output is well-formatted Markdown

---

## 🚀 Next Steps After Testing

Once testing is complete:

1. **If successful**:
   - Move from `wip-plugins/` to production plugins directory
   - Update version to 1.0.0 (stable)
   - Add to ClaudeSkillCollection README
   - Create GitHub release

2. **If issues found**:
   - Document issues in GitHub issues
   - Prioritize fixes
   - Re-test after fixes

3. **Future enhancements** (v1.1+):
   - Add remaining 5 scenarios (DDoS, malware, cloud breach, supply chain, AI/ML)
   - Multi-format export (Word, PDF, HTML)
   - Additional compliance frameworks (PCI DSS, SOC 2)
   - Localization support

---

**Happy Testing!**

Start with a fresh Claude Code session and say:
```
Create an incident response playbook for ransomware attacks
```
