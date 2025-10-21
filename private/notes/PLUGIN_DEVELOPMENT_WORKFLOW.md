# Plugin Development Workflow

**Your Complete Guide to Creating, Testing, and Publishing Plugins**

**Last Updated:** 2025-10-19
**For:** ClaudeSkillCollection Security & Compliance Marketplace

---

## Overview

This guide walks you through the complete lifecycle of creating a new plugin from idea to public release.

**Workflow Summary:**
```
Idea → Design → Develop (Private) → Test → Document → Review → Publish (Public) → Maintain
```

**Timeline:** Typically 1-2 weeks per plugin depending on complexity

---

## Phase 1: Planning & Design

### Step 1.1: Validate Your Idea

Before starting development, ensure your plugin idea follows our design principles.

**Ask yourself:**

1. **What deliverable does it produce?**
   - Example: "CCPA Compliance Audit Report"
   - NOT: "CCPA Compliance Score" (too simple)

2. **Can it work with static files?**
   - ✅ YES: Analyzes code, configs, docs
   - ❌ NO: Requires live database connection

3. **Does it follow a systematic workflow?**
   - ✅ YES: Clear 5-step audit process
   - ❌ NO: Arbitrary exploration

4. **Is it based on objective criteria?**
   - ✅ YES: CCPA regulations (authoritative source)
   - ❌ NO: "Best practices" (too vague)

5. **Do reference materials exist?**
   - ✅ YES: Official CCPA text, AG guidelines
   - ❌ NO: Would need to create everything

**If you answered YES to all 5, proceed!**

**Document in:** `private/notes/plugin-ideas.md`

```markdown
# Plugin Ideas

## CCPA Auditor
- **Status:** Planning
- **Deliverable:** CCPA compliance audit report
- **Works with:** Static code files, database schemas
- **Workflow:** 5-step audit process
- **Criteria:** CCPA regulations (California AG guidelines)
- **References:** Official CCPA text, AG enforcement guidelines
- **Validation:** ✅ Passed all 5 design questions
- **Started:** 2025-10-19
```

### Step 1.2: Research & Gather References

**Create research directory:**
```bash
cd private/research/
mkdir ccpa-auditor
cd ccpa-auditor/
```

**Gather authoritative sources:**
1. Official regulations (CCPA text)
2. Government guidelines (California AG)
3. Industry standards (if applicable)
4. Best practices from authoritative bodies

**Example structure:**
```
private/research/ccpa-auditor/
├── ccpa-official-text.pdf
├── california-ag-guidelines.md
├── data-categories.md
├── consumer-rights.md
└── enforcement-actions.md
```

**Document sources:**
```markdown
# CCPA Research Sources

## Official Regulations
- CCPA (California Civil Code 1798.100-1798.199)
  - Source: California Legislative Information
  - URL: https://leginfo.legislature.ca.gov/...
  - Retrieved: 2025-10-19

## Government Guidelines
- California AG Enforcement Guidelines
  - Source: California Department of Justice
  - URL: https://oag.ca.gov/...
  - Retrieved: 2025-10-19

## Notes
- Focus on consumer rights (access, deletion, opt-out)
- Similar to GDPR but California-specific
- Applies to businesses with $25M+ revenue or 50k+ consumers
```

### Step 1.3: Design the Workflow

**Create workflow document:**
```bash
cd private/drafts/
touch ccpa-auditor-workflow.md
```

**Define systematic process:**

```markdown
# CCPA Auditor Workflow

## Phase 1: Scope Identification
1. Identify business type (B2C, B2B)
2. Determine CCPA applicability
3. List data categories collected
4. Map data flows

## Phase 2: Consumer Rights Analysis
1. Scan for "Right to Know" implementation
2. Check "Right to Delete" functionality
3. Verify "Right to Opt-Out" mechanism
4. Review "Do Not Sell My Info" link

## Phase 3: Data Practice Review
1. Analyze data collection points
2. Review third-party sharing
3. Check sale of personal information
4. Verify disclosure practices

## Phase 4: Security & Retention
1. Review security measures
2. Check data retention policies
3. Verify deletion procedures
4. Assess breach notification readiness

## Phase 5: Generate Report
1. Compile findings by risk level
2. Map to CCPA sections
3. Provide code references
4. Generate recommendations
5. Create compliance checklist

## Deliverable
Markdown report with:
- Executive summary
- Risk-prioritized findings
- CCPA section citations
- Specific code references (file:line)
- Actionable remediation steps
```

---

## Phase 2: Development (Private Repository)

### Step 2.1: Create Plugin Structure

**In private workspace:**
```bash
cd /path/to/ClaudeSkillCollection/private/wip-plugins/
mkdir ccpa-auditor
cd ccpa-auditor/
```

**Create directory structure:**
```bash
mkdir -p scripts references examples

# Create core files
touch SKILL.md
touch plugin.json
touch README.md
touch .gitkeep
```

**Your structure:**
```
private/wip-plugins/ccpa-auditor/
├── SKILL.md              # Claude agent prompt
├── plugin.json           # Plugin manifest
├── README.md             # User documentation
├── scripts/              # Automation tools
│   ├── scan_data_collection.py
│   ├── check_consumer_rights.py
│   └── generate_report.py
├── references/           # CCPA reference materials
│   ├── ccpa_sections.md
│   ├── consumer_rights.md
│   ├── data_categories.md
│   └── disclosure_requirements.md
└── examples/             # Sample outputs
    └── sample-audit.md
```

### Step 2.2: Write SKILL.md (Agent Prompt)

This is the most important file - it guides Claude's behavior.

**Template:**
```markdown
---
name: ccpa-auditor
description: Comprehensive CCPA compliance auditing skill that analyzes codebases and systems for California Consumer Privacy Act compliance. Generates detailed audit reports with consumer rights verification and data practice analysis.
license: MIT
---

# CCPA Auditor Skill

## Purpose

This skill equips Claude with specialized knowledge to audit systems for CCPA compliance and generate comprehensive audit reports.

**Key capabilities:**
1. Identify personal information collection and processing
2. Verify consumer rights implementation (access, deletion, opt-out)
3. Assess data sale and sharing practices
4. Review disclosure and transparency requirements
5. Generate structured compliance reports

## When to Use This Skill

Use this skill when:
- Auditing California-focused applications
- Preparing for CCPA compliance certification
- Reviewing consumer rights implementation
- Assessing third-party data sharing practices
- Generating CCPA compliance documentation

**Do NOT use for:**
- Live system monitoring
- Real-time data processing analysis
- Non-California jurisdictions (use GDPR for EU)

## Workflow

### Phase 1: Scope Assessment

Determine CCPA applicability:
1. Identify business revenue ($25M+ threshold)
2. Check consumer data volume (50k+ consumers)
3. Verify California consumer presence
4. List categories of personal information collected

### Phase 2: Consumer Rights Review

Audit the four primary consumer rights:

**Right to Know:**
- Scan for data access request handling
- Check 12-month lookback capability
- Verify response timeline (45 days)

**Right to Delete:**
- Identify deletion endpoints/functionality
- Review deletion exceptions (legal hold, etc.)
- Check deletion confirmation mechanisms

**Right to Opt-Out:**
- Find "Do Not Sell My Personal Information" links
- Verify opt-out mechanism functionality
- Check opt-out honoring in code

**Right to Non-Discrimination:**
- Review pricing/service parity
- Check for discrimination prevention
- Verify incentive programs compliance

### Phase 3: Data Practice Analysis

Examine data handling:

**Collection:**
- Identify collection points (forms, APIs, tracking)
- Map personal information categories
- Review collection notices

**Sale/Sharing:**
- Scan for third-party data transfers
- Check "sale" definition compliance
- Review service provider agreements

**Disclosure:**
- Verify privacy policy completeness
- Check disclosure at collection
- Review category-specific disclosures

### Phase 4: Security & Retention

Assess data protection:
- Review security measures (encryption, access controls)
- Check retention policies and schedules
- Verify data minimization practices
- Assess breach notification readiness

### Phase 5: Generate Audit Report

Produce comprehensive deliverable:

1. **Executive Summary**
   - Overall compliance status
   - Risk level assessment
   - Priority recommendations

2. **Detailed Findings**
   - Organized by CCPA section
   - Risk-prioritized (Critical, High, Medium, Low)
   - Specific code references (file:line)
   - Remediation guidance

3. **Consumer Rights Matrix**
   - Implementation status for each right
   - Gap analysis
   - Implementation recommendations

4. **Compliance Checklist**
   - Completed requirements
   - Missing requirements
   - In-progress items

5. **Action Plan**
   - Prioritized remediation steps
   - Estimated effort
   - Recommended timeline

## Reference Materials

**Primary References:**
- `references/ccpa_sections.md` - Key CCPA sections (1798.100-1798.199)
- `references/consumer_rights.md` - Four primary consumer rights
- `references/data_categories.md` - Personal information taxonomy

**Supporting Materials:**
- `references/disclosure_requirements.md` - Privacy policy requirements
- `references/exemptions.md` - CCPA exemptions and exceptions
- `references/enforcement.md` - California AG enforcement priorities

## Output Format

**Markdown Report Structure:**

```markdown
# CCPA Compliance Audit Report
Generated: [Date]
Audited System: [Name]

## Executive Summary
- Compliance Status: [Compliant/Non-Compliant/Partial]
- Risk Level: [Low/Medium/High/Critical]
- Total Findings: [Number]
- Priority Actions: [Number]

## Findings Summary

### Critical Issues (0)
[None found / List]

### High Priority (3)
1. Missing "Do Not Sell" Link
   - CCPA Section: 1798.135
   - Location: All pages
   - Risk: Enforcement action
   - Remediation: Add prominent link to homepage and data collection pages

[... more findings ...]

## Consumer Rights Assessment

### Right to Know - ❌ Not Implemented
- Missing: Data access request endpoint
- Missing: 12-month data retrieval capability
- Required: Implement /api/ccpa/access endpoint

[... other rights ...]

## Detailed Analysis

[By CCPA section with code references]

## Compliance Checklist

- [ ] Privacy Policy includes CCPA disclosures
- [x] Security measures implemented
- [ ] "Do Not Sell" link present
- [ ] Consumer request handling implemented

## Recommendations

1. **Immediate (Critical):**
   - Add "Do Not Sell My Personal Information" link
   - Implement consumer data access endpoint

2. **Short-term (30 days):**
   - Update privacy policy
   - Create deletion workflow

3. **Medium-term (90 days):**
   - Implement service provider agreements
   - Enhance security measures

## Resources
- California AG CCPA Guidelines: [URL]
- Implementation Guide: [URL]
```

## Defensive Security Note

This skill performs **defensive security analysis only**:
- ✅ Identifies compliance gaps to fix them
- ✅ Reviews code for consumer privacy protections
- ✅ Generates remediation recommendations
- ❌ Does NOT scan live systems without permission
- ❌ Does NOT access consumer data
- ❌ Does NOT perform penetration testing

## Tools Available

**Scripts (optional, manual execution):**
- `scripts/scan_data_collection.py` - Identifies data collection patterns
- `scripts/check_consumer_rights.py` - Verifies rights implementation
- `scripts/generate_report.py` - Formats audit output

**These scripts analyze static code only and do not require system access.**

## Example Usage

```
User: "Audit my e-commerce site for CCPA compliance"

Claude (using this skill):
1. Examines codebase for data collection
2. Checks for consumer rights implementation
3. Reviews privacy policy and disclosures
4. Analyzes third-party integrations
5. Generates comprehensive audit report with findings
```

## Limitations

- Works with static code analysis only
- Cannot verify runtime behavior
- Requires access to codebase and documentation
- Legal review recommended for official compliance
- California law subject to updates and court interpretations
```

### Step 2.3: Create plugin.json

**Manifest file:**
```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "ccpa-auditor",
  "version": "1.0.0",
  "description": "Comprehensive CCPA compliance auditing skill that analyzes codebases and systems for California Consumer Privacy Act compliance. Generates detailed audit reports with consumer rights verification and data practice analysis.",
  "author": {
    "name": "Diego Consolini",
    "email": "diego@diegocon.nl"
  },
  "license": "MIT",
  "homepage": "https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/ccpa-auditor",
  "repository": "https://github.com/diegocconsolini/ClaudeSkillCollection",
  "keywords": [
    "ccpa",
    "compliance",
    "privacy",
    "california",
    "consumer-rights",
    "audit",
    "security",
    "personal-information"
  ],
  "category": "security",
  "agents": [
    {
      "name": "ccpa-auditor",
      "description": "CCPA compliance auditor agent that analyzes systems for California Consumer Privacy Act compliance",
      "prompt": "./SKILL.md"
    }
  ]
}
```

### Step 2.4: Create Reference Materials

**Example: references/ccpa_sections.md**

```markdown
# Key CCPA Sections

## Section 1798.100 - Consumer's Right to Know

Consumers have the right to request:
1. Categories of personal information collected
2. Categories of sources from which collected
3. Business purpose for collecting/selling
4. Categories of third parties shared with
5. Specific pieces of personal information collected

**Requirements:**
- Must respond within 45 days (extendable to 90)
- Must provide information covering prior 12 months
- Must provide information free of charge

[... more sections ...]
```

Create all reference documents based on your research.

### Step 2.5: Write Automation Scripts

**Example: scripts/scan_data_collection.py**

```python
#!/usr/bin/env python3
"""
Scan codebase for CCPA-relevant data collection patterns.

This script analyzes code to identify where personal information
is collected, processed, or shared.
"""

import sys
import re
from pathlib import Path
from typing import List, Dict

def scan_for_data_collection(directory: str) -> List[Dict]:
    """
    Scan directory for data collection patterns.

    Args:
        directory: Path to codebase

    Returns:
        List of findings with file, line, pattern
    """
    findings = []

    # Patterns that indicate data collection
    patterns = {
        'email': r'email\s*=|@\w+\.\w+',
        'phone': r'phone|telephone|\d{3}-\d{3}-\d{4}',
        'ssn': r'ssn|social.security|\d{3}-\d{2}-\d{4}',
        'address': r'address|street|city|state|zip',
        'location': r'location|geolocation|lat.*lon',
        'ip_address': r'ip.?address|remote.?addr',
        'cookies': r'setcookie|cookie\s*=',
        'tracking': r'tracking|analytics|pixel'
    }

    path = Path(directory)

    for file_path in path.rglob('*'):
        if file_path.suffix in ['.py', '.js', '.java', '.php', '.rb']:
            try:
                content = file_path.read_text()
                for line_num, line in enumerate(content.split('\n'), 1):
                    for category, pattern in patterns.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            findings.append({
                                'file': str(file_path),
                                'line': line_num,
                                'category': category,
                                'code': line.strip()
                            })
            except Exception as e:
                print(f"Error reading {file_path}: {e}", file=sys.stderr)

    return findings

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python scan_data_collection.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    findings = scan_for_data_collection(directory)

    print(f"\\nFound {len(findings)} data collection patterns:\\n")

    # Group by category
    by_category = {}
    for finding in findings:
        category = finding['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(finding)

    for category, items in sorted(by_category.items()):
        print(f"\\n{category.upper()} ({len(items)} instances):")
        for item in items[:5]:  # Show first 5
            print(f"  {item['file']}:{item['line']}")
            print(f"    {item['code'][:80]}")

if __name__ == '__main__':
    main()
```

**Make executable:**
```bash
chmod +x scripts/scan_data_collection.py
```

### Step 2.6: Create README.md

**User-facing documentation:**

```markdown
# CCPA Auditor

**Version:** 1.0.0
**Category:** Data Privacy & Compliance
**Status:** Production Ready

Comprehensive CCPA (California Consumer Privacy Act) compliance auditing plugin that analyzes codebases and systems for California privacy law compliance.

## Features

- Scans code for personal information collection
- Verifies consumer rights implementation (access, deletion, opt-out)
- Analyzes data sale and sharing practices
- Reviews disclosure and transparency requirements
- Generates detailed compliance reports with specific code references
- 4 comprehensive reference documents covering CCPA sections
- 3 automated scanning tools (Python)

[... rest of README similar to GDPR Auditor ...]
```

### Step 2.7: Create Example Output

**examples/sample-audit.md:**

Show users what the deliverable looks like.

```markdown
# CCPA Compliance Audit Report
Generated: 2025-10-20
Audited System: Example E-commerce Platform

## Executive Summary

- **Compliance Status:** Non-Compliant
- **Risk Level:** High
- **Total Findings:** 12 (2 Critical, 4 High, 4 Medium, 2 Low)
- **Priority Actions:** 6

[... full example report ...]
```

---

## Phase 3: Testing

### Step 3.1: Internal Testing

**Test on a sample codebase:**

```bash
# Create test directory
cd private/test-data/
mkdir ccpa-auditor-test
cd ccpa-auditor-test/

# Create sample files with CCPA-relevant code
# ... create test files ...
```

**Run your scripts:**
```bash
cd private/wip-plugins/ccpa-auditor/
python scripts/scan_data_collection.py ../../test-data/ccpa-auditor-test/
```

**Test with Claude:**

1. Temporarily copy to main repo for testing:
```bash
cp -r private/wip-plugins/ccpa-auditor /tmp/ccpa-auditor-test
```

2. In Claude Code, load the skill and test:
```
"Using the CCPA auditor skill at /tmp/ccpa-auditor-test, audit this sample application"
```

3. Verify output matches expected format

### Step 3.2: Create Testing Checklist

**In private/notes/ccpa-auditor-testing.md:**

```markdown
# CCPA Auditor Testing Checklist

## Design Validation
- [x] Produces tangible deliverable (audit report)
- [x] Works with static files only
- [x] Follows systematic workflow
- [x] Based on objective criteria (CCPA regulations)
- [x] Includes reference materials

## Functional Testing
- [ ] Script 1: Data collection scanner works
- [ ] Script 2: Consumer rights checker works
- [ ] Script 3: Report generator works
- [ ] SKILL.md guides Claude correctly
- [ ] Generates expected report format
- [ ] Includes specific code references (file:line)
- [ ] Cites CCPA sections correctly

## Documentation Testing
- [ ] README is clear and complete
- [ ] Installation instructions work
- [ ] Examples are accurate
- [ ] Reference materials are correct
- [ ] No broken links
- [ ] No placeholder text

## Quality Standards
- [ ] No malicious code
- [ ] Defensive security only
- [ ] Error handling in scripts
- [ ] Type hints in Python code
- [ ] Authoritative sources cited
- [ ] MIT License included

## Real-World Testing
- [ ] Tested on actual codebase (specify which)
- [ ] Identified real issues
- [ ] Generated actionable report
- [ ] Findings were accurate
- [ ] No false positives

## Edge Cases
- [ ] Empty codebase
- [ ] Non-Python/JS codebase
- [ ] Large codebase (10k+ files)
- [ ] Codebase without CCPA issues
- [ ] Codebase with many CCPA issues

## Performance
- [ ] Runs in reasonable time (<5 min for medium codebase)
- [ ] Doesn't crash on large files
- [ ] Memory usage acceptable

## Issues Found
[Document any issues encountered during testing]

## Sign-off
- [ ] Ready for public release
- [ ] Tested by: Diego Consolini
- [ ] Date: 2025-10-XX
```

### Step 3.3: Fix Issues

As you find problems, fix them in the private version:

```bash
cd private/wip-plugins/ccpa-auditor/
# Make fixes
git add .
git commit -m "Fix data collection scanner false positives"
git push
```

---

## Phase 4: Documentation Review

### Step 4.1: Final Documentation Check

**Create checklist:**

```markdown
# CCPA Auditor Documentation Review

## SKILL.md
- [x] Clear purpose statement
- [x] When to use / when NOT to use
- [x] Complete workflow (5 phases)
- [x] Reference materials listed
- [x] Output format specified
- [x] Defensive security note
- [x] Example usage
- [x] Limitations documented

## plugin.json
- [x] Correct version number
- [x] Accurate description
- [x] Author info correct (diego@diegocon.nl)
- [x] Keywords relevant
- [x] Category: security
- [x] Agent configured correctly

## README.md
- [x] Version number
- [x] Feature list
- [x] Installation instructions
- [x] Usage examples
- [x] Script documentation
- [x] Limitations
- [x] Disclaimer
- [x] License (MIT)

## Reference Materials
- [x] All sources cited
- [x] URLs verified (not broken)
- [x] Content accurate
- [x] Up-to-date (check dates)

## Scripts
- [x] Help/usage info
- [x] Error handling
- [x] Type hints
- [x] Docstrings
- [x] Executable permissions

## Examples
- [x] Sample output realistic
- [x] Shows key features
- [x] Demonstrates format
```

### Step 4.2: Peer Review (Optional)

If you have collaborators:

```bash
# Give collaborator access to private repo
# They can review: private/wip-plugins/ccpa-auditor/

# Incorporate feedback
git add .
git commit -m "Address peer review feedback"
git push
```

---

## Phase 5: Pre-Release Preparation

### Step 5.1: Version Bump

**Ensure version is correct:**
- `plugin.json`: `"version": "1.0.0"`
- `README.md`: `**Version:** 1.0.0`

### Step 5.2: Create Pre-Release Notes

**In private/notes/ccpa-auditor-release-notes.md:**

```markdown
# CCPA Auditor v1.0.0 Release Notes

## Release Date
2025-10-25 (planned)

## Summary
First public release of CCPA Auditor plugin for California Consumer Privacy Act compliance auditing.

## Features
- Consumer rights verification (access, delete, opt-out, non-discrimination)
- Data collection and sale analysis
- Privacy disclosure review
- Comprehensive audit report generation
- 4 CCPA reference documents
- 3 automation scripts

## Testing
- Tested on 3 real codebases
- Identified 47 compliance issues
- 100% accurate findings
- No false positives in final testing

## Known Limitations
- Static code analysis only
- Requires manual legal review
- California jurisdiction only

## Documentation
- Complete SKILL.md (300 lines)
- Comprehensive README (150 lines)
- 4 reference documents (500+ lines)
- Example audit report

## Marketing
- Will announce in Claude Code discussions
- Blog post (optional): TBD
- Tweet (optional): TBD
```

---

## Phase 6: Publication

### Step 6.1: Copy to Public Repository

**Move from private to public:**

```bash
# In main repository
cd /path/to/ClaudeSkillCollection

# Copy plugin from private
cp -r private/wip-plugins/ccpa-auditor ./ccpa-auditor

# Verify structure
ls -la ccpa-auditor/
```

### Step 6.2: Update Marketplace Configuration

**Edit `.claude-plugin/marketplace.json`:**

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "security-compliance-marketplace",
  "version": "1.0.0",
  "description": "...",
  "owner": {...},
  "plugins": [
    {
      "name": "gdpr-auditor",
      ...
    },
    {
      "name": "ccpa-auditor",
      "description": "Comprehensive CCPA compliance auditing skill that analyzes codebases and systems for California Consumer Privacy Act compliance. Generates detailed audit reports with consumer rights verification.",
      "source": "./ccpa-auditor",
      "version": "1.0.0",
      "author": {
        "name": "Diego Consolini",
        "email": "diego@diegocon.nl"
      },
      "category": "security",
      "keywords": [
        "ccpa",
        "compliance",
        "privacy",
        "california",
        "consumer-rights",
        "audit",
        "security",
        "personal-information"
      ],
      "homepage": "https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/ccpa-auditor",
      "repository": "https://github.com/diegocconsolini/ClaudeSkillCollection",
      "license": "MIT"
    }
  ]
}
```

### Step 6.3: Update Documentation

**Update README.md:**

```markdown
## Available Skills

### 1. GDPR Auditor
[existing content]

### 2. CCPA Auditor ✅ NEW
**Status:** Production Ready
**Version:** 1.0.0
**Category:** Data Privacy & Compliance

Comprehensive CCPA (California Consumer Privacy Act) compliance auditing plugin...

[feature list]

[→ Read CCPA Auditor Documentation](./ccpa-auditor/README.md)
```

**Update CHANGELOG.md:**

```markdown
## [1.2.0] - 2025-10-25

### Added - CCPA Auditor Plugin

#### CCPA Auditor Plugin v1.0.0
- Complete CCPA compliance auditing plugin
- SKILL.md with structured audit workflow
- Comprehensive README with installation and usage
- 4 reference documents covering CCPA:
  - ccpa_sections.md - Key CCPA sections
  - consumer_rights.md - Four consumer rights
  - data_categories.md - Personal information taxonomy
  - disclosure_requirements.md - Privacy policy requirements
- 3 automated scanning tools:
  - scan_data_collection.py - Data collection patterns
  - check_consumer_rights.py - Rights verification
  - generate_report.py - Report generation
- Example audit output
- Verified against official CCPA sources
- Tested on real-world e-commerce applications

[... rest of changelog entry ...]
```

**Update MARKETPLACE.md:**

Add to roadmap or available plugins section.

### Step 6.4: Commit to Public Repository

```bash
# Stage changes
git add ccpa-auditor/
git add .claude-plugin/marketplace.json
git add README.md
git add CHANGELOG.md
git add MARKETPLACE.md

# Commit
git commit -m "$(cat <<'EOF'
Add CCPA Auditor Plugin v1.0.0

New Plugin: California Consumer Privacy Act Compliance Auditor

Features:
- Consumer rights verification (access, delete, opt-out, non-discrimination)
- Data collection and sale analysis
- Privacy disclosure review
- Comprehensive audit report generation
- 4 CCPA reference documents
- 3 automation scripts (Python)

Plugin Structure:
- SKILL.md - Claude agent prompt (300 lines)
- plugin.json - Plugin manifest
- README.md - User documentation (150 lines)
- scripts/ - 3 automation tools
- references/ - 4 CCPA reference documents (500+ lines)
- examples/ - Sample audit report

Testing:
- Tested on 3 real e-commerce codebases
- Identified 47 compliance issues
- 100% accurate findings
- Production-ready

Documentation:
- Complete workflow guide
- Consumer rights matrix
- CCPA section citations
- Example outputs

Marketplace Update:
- Added to marketplace.json
- Updated README with new plugin
- Updated CHANGELOG for v1.2.0
- Available via: /plugin install ccpa-auditor@security-compliance-marketplace

🤖 Generated with Claude Code
https://claude.com/claude-code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to GitHub
git push
```

### Step 6.5: Create GitHub Release

1. Go to: https://github.com/diegocconsolini/ClaudeSkillCollection/releases
2. Click "Draft a new release"
3. Tag: `v1.2.0`
4. Title: "CCPA Auditor Plugin - v1.2.0"
5. Description: Copy from CHANGELOG.md
6. Publish release

### Step 6.6: Archive in Private Repo

**Mark as released in private:**

```bash
cd private/wip-plugins/ccpa-auditor/

# Add release note
echo "Released to public: v1.0.0 on 2025-10-25" > RELEASED.txt

git add RELEASED.txt
git commit -m "Mark CCPA Auditor as released (v1.0.0)"
git push

# Optionally move to archive
cd ..
mkdir -p ../archive/
mv ccpa-auditor/ ../archive/ccpa-auditor-v1.0.0/
git add ../archive/
git commit -m "Archive released CCPA Auditor v1.0.0"
git push
```

---

## Phase 7: Post-Release

### Step 7.1: Announce

**Where to announce:**
1. GitHub Discussions (your repo)
2. Claude Code community
3. Social media (optional)
4. LinkedIn (professional network)

**Sample announcement:**

```markdown
# 🎉 New Plugin: CCPA Auditor v1.0.0

We've just released the CCPA Auditor plugin for California Consumer Privacy Act compliance!

**Features:**
✅ Consumer rights verification
✅ Data sale & sharing analysis
✅ Privacy disclosure review
✅ Comprehensive audit reports

**Install:**
```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install ccpa-auditor@security-compliance-marketplace
```

Perfect for California-focused businesses and e-commerce platforms.

GitHub: https://github.com/diegocconsolini/ClaudeSkillCollection
```

### Step 7.2: Monitor Feedback

**Track:**
- GitHub issues
- GitHub discussions
- User questions

**Respond to:**
- Bug reports (create issues in private for fixes)
- Feature requests (document in private/notes/)
- Questions (update README/docs if needed)

### Step 7.3: Plan Updates

**If bugs are found:**

1. Create issue in private repo
2. Fix in `private/wip-plugins/ccpa-auditor-v1.0.1/`
3. Test thoroughly
4. Release patch version (v1.0.1)
5. Update public repo

**If features are requested:**

1. Evaluate against design principles
2. Document in `private/notes/ccpa-auditor-roadmap.md`
3. Plan for minor version (v1.1.0)
4. Develop in private
5. Release when ready

---

## Quick Reference

### File Locations

**Development:**
- Plugin code: `private/wip-plugins/{plugin-name}/`
- Research: `private/research/{plugin-name}/`
- Design docs: `private/drafts/{plugin-name}-*.md`
- Notes: `private/notes/{plugin-name}-*.md`
- Test data: `private/test-data/{plugin-name}-test/`

**Public Release:**
- Plugin: `{plugin-name}/` (main repo root)
- Marketplace: `.claude-plugin/marketplace.json`
- Docs: `README.md`, `CHANGELOG.md`, `MARKETPLACE.md`

### Common Commands

**Start new plugin:**
```bash
cd private/wip-plugins/
mkdir {plugin-name} && cd {plugin-name}
mkdir -p scripts references examples
touch SKILL.md plugin.json README.md
```

**Test plugin:**
```bash
# Copy to temp location
cp -r private/wip-plugins/{plugin-name} /tmp/

# In Claude Code
"Using the skill at /tmp/{plugin-name}, audit [target]"
```

**Release plugin:**
```bash
cp -r private/wip-plugins/{plugin-name} ./
# Edit marketplace.json, README.md, CHANGELOG.md
git add .
git commit -m "Add {Plugin Name} v1.0.0"
git push
```

**Update plugin:**
```bash
# Work in private
cd private/wip-plugins/{plugin-name}-v1.0.1/
# Make changes, test
# When ready:
cp -r private/wip-plugins/{plugin-name}-v1.0.1/* ./{plugin-name}/
git add .
git commit -m "Update {Plugin Name} to v1.0.1"
git push
```

---

## Checklist Template

Copy this for each new plugin:

```markdown
# {Plugin Name} Development Checklist

## Planning
- [ ] Idea validated against 5 design questions
- [ ] Research gathered from authoritative sources
- [ ] Workflow designed (documented)
- [ ] Deliverable format defined

## Development
- [ ] Directory structure created in private/wip-plugins/
- [ ] SKILL.md written (agent prompt)
- [ ] plugin.json created (manifest)
- [ ] README.md written (user docs)
- [ ] Reference materials created (4+ documents)
- [ ] Scripts developed (if applicable)
- [ ] Examples created (sample output)

## Testing
- [ ] Passes design validation (5 criteria)
- [ ] Scripts work correctly
- [ ] Tested with Claude
- [ ] Tested on real codebase
- [ ] Edge cases tested
- [ ] Documentation accurate
- [ ] No malicious code
- [ ] Performance acceptable

## Documentation
- [ ] SKILL.md complete
- [ ] README.md complete
- [ ] Reference materials cited
- [ ] Examples realistic
- [ ] No placeholders
- [ ] No broken links

## Pre-Release
- [ ] Version number correct
- [ ] Release notes drafted
- [ ] Testing checklist completed
- [ ] Peer review done (if applicable)

## Publication
- [ ] Copied to public repo
- [ ] marketplace.json updated
- [ ] README.md updated
- [ ] CHANGELOG.md updated
- [ ] MARKETPLACE.md updated
- [ ] Committed and pushed
- [ ] GitHub release created

## Post-Release
- [ ] Announced in discussions
- [ ] Monitoring issues/feedback
- [ ] Archived in private repo

## Sign-off
- [ ] Ready for release
- [ ] Created by: Diego Consolini
- [ ] Date: 2025-XX-XX
```

---

## Workflow Diagram

```
┌─────────────────┐
│   IDEA          │
│   (Private)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   VALIDATE      │ ← Check 5 design questions
│   (Private)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RESEARCH      │ ← Gather authoritative sources
│   (Private)     │   private/research/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DESIGN        │ ← Create workflow document
│   (Private)     │   private/drafts/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DEVELOP       │ ← Build in private/wip-plugins/
│   (Private)     │   • SKILL.md
│                 │   • plugin.json
│                 │   • README.md
│                 │   • scripts/
│                 │   • references/
│                 │   • examples/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TEST          │ ← Test with Claude + scripts
│   (Private)     │   private/test-data/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DOCUMENT      │ ← Complete all docs
│   (Private)     │   Check against standards
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   REVIEW        │ ← Peer review (optional)
│   (Private)     │   Testing checklist
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PUBLISH       │ ← Copy to public repo
│   (Public)      │   Update marketplace.json
│                 │   Update README, CHANGELOG
│                 │   git commit + push
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RELEASE       │ ← Create GitHub release
│   (Public)      │   Tag version
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ANNOUNCE      │ ← Share with community
│   (Public)      │   Monitor feedback
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MAINTAIN      │ ← Bug fixes, updates
│   (Ongoing)     │   Version increments
└─────────────────┘
```

---

## Tips & Best Practices

### Development
1. **Commit often** in private repo - version control is your friend
2. **Test early** - don't wait until plugin is "done"
3. **Real codebases** - test on actual projects, not toy examples
4. **Reference quality** - spend time on authoritative sources
5. **Workflow clarity** - if you can't explain it simply, it's not clear

### Documentation
1. **Show, don't tell** - include real examples
2. **User perspective** - write for someone who doesn't know CCPA
3. **Code references** - always include file:line in examples
4. **Limitations** - be honest about what it can't do
5. **Sources** - cite everything, link to originals

### Testing
1. **Edge cases** - test with empty, huge, and weird codebases
2. **False positives** - minimize these, they erode trust
3. **Performance** - script should run in reasonable time
4. **Error handling** - never crash, always fail gracefully
5. **Reproducibility** - same input should give same output

### Publishing
1. **Version carefully** - semantic versioning (major.minor.patch)
2. **Changelog detailed** - users need to know what changed
3. **Release notes** - summarize value, not just features
4. **Timing** - don't rush, but don't wait for perfection
5. **Communication** - tell users about new plugins!

### Maintenance
1. **Monitor issues** - respond within 48 hours
2. **Bug fixes fast** - patch versions for bugs
3. **Features deliberate** - minor/major versions for features
4. **Breaking changes** - only in major versions
5. **Deprecation** - give users time to migrate

---

## Troubleshooting

### Issue: Plugin doesn't load in Claude
**Solution:**
- Check SKILL.md syntax (YAML front matter)
- Verify plugin.json format (valid JSON)
- Ensure files are in correct locations
- Check file permissions (readable)

### Issue: Scripts don't work
**Solution:**
- Verify shebang line (#!/usr/bin/env python3)
- Check executable permissions (chmod +x)
- Test standalone (python script.py --help)
- Check dependencies (import errors)

### Issue: Generated reports are inconsistent
**Solution:**
- Make workflow more explicit in SKILL.md
- Add more examples in references/
- Include report template
- Add validation step to workflow

### Issue: Testing takes too long
**Solution:**
- Create smaller test datasets
- Add early exit for large files
- Implement progress indicators
- Consider performance optimizations

---

## Summary

**Your Development Cycle:**

1. **Idea** → Validate against 5 design questions (private/notes/)
2. **Research** → Gather authoritative sources (private/research/)
3. **Design** → Create workflow document (private/drafts/)
4. **Develop** → Build plugin (private/wip-plugins/)
5. **Test** → Verify functionality (private/test-data/)
6. **Document** → Complete all docs
7. **Publish** → Copy to public, update marketplace
8. **Release** → GitHub release, announce
9. **Maintain** → Monitor, fix, enhance

**Time Estimates:**
- Simple plugin: 3-5 days
- Medium plugin (like GDPR/CCPA): 1-2 weeks
- Complex plugin: 2-4 weeks

**Success Criteria:**
- ✅ Passes 5 design questions
- ✅ Tested on real codebase
- ✅ Documentation complete
- ✅ No critical bugs
- ✅ User value clear

---

**Last Updated:** 2025-10-19
**Your Workflow Version:** 1.0
**For Questions:** diego@diegocon.nl
