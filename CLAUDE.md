# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

**Type:** Claude Code Plugin Marketplace
**Specialization:** Security, Privacy, and Compliance Auditing
**Marketplace Name:** `security-compliance-marketplace`
**Public Repository:** https://github.com/diegocconsolini/ClaudeSkillCollection
**Private Submodule:** https://github.com/diegocconsolini/ClaudeSkillCollection-Private (private)

This is a community-driven Claude Code plugin marketplace focused exclusively on security, privacy regulations (GDPR, CCPA, HIPAA), and compliance automation. All plugins are production-ready, verified against authoritative sources, and follow defensive security principles.

---

## Core Design Philosophy

**Critical:** All plugins in this marketplace MUST adhere to these design principles (see SKILL_DESIGN_PRINCIPLES.md for full details).

### What Plugins ARE:
1. **Document Generators** - Create reports, configs, documentation
2. **Workflow Guides** - Step-by-step systematic instructions
3. **Template Systems** - Reusable patterns and boilerplates
4. **Format Converters** - Transform data into deliverables
5. **Code Libraries** - Manipulate file structures, generate code

### What Plugins are NOT:
1. **Analysis Tools** - That scan live systems or running applications
2. **External Services** - That require APIs or third-party integrations
3. **Real-time Monitors** - That need continuous data streams
4. **Subjective Assessors** - That make judgments without clear criteria
5. **Simple Calculators** - That just return a single number

### Design Validation (All 5 Must Be True):
1. ✅ Produces tangible deliverable (report, document, config file)
2. ✅ Works with static files (no live system access required)
3. ✅ Follows systematic workflow (clear step-by-step process)
4. ✅ Based on objective criteria (regulations, standards, best practices)
5. ✅ Includes reference materials (authoritative sources, templates)

**Reference:** SKILL_DESIGN_PRINCIPLES.md contains comprehensive guidelines with examples.

---

## Repository Structure

### Public Repository (Main)
```
ClaudeSkillCollection/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace configuration
│
├── gdpr-auditor/                  # Production plugin
│   ├── SKILL.md                   # Claude agent prompt
│   ├── plugin.json                # Plugin manifest
│   ├── README.md                  # User documentation
│   ├── scripts/                   # Automation tools (5 scripts)
│   └── references/                # GDPR reference materials (8 docs)
│
├── private/                       # Git submodule (PRIVATE repository)
│   ├── notes/                     # Development notes
│   │   ├── PLUGIN_DEVELOPMENT_WORKFLOW.md  # Complete workflow guide
│   │   └── TESTING_CHECKLIST_TEMPLATE.md   # Testing checklist
│   ├── research/                  # Research materials
│   ├── wip-plugins/               # Work-in-progress plugins
│   │   └── _TEMPLATE/             # Plugin template structure
│   ├── drafts/                    # Draft documentation
│   └── test-data/                 # Test datasets
│
├── SKILL_DESIGN_PRINCIPLES.md    # Design guidelines (600+ lines)
├── CONTRIBUTING.md                # Contribution guidelines
├── MARKETPLACE.md                 # Marketplace documentation
└── README.md                      # Main documentation
```

### Private Submodule (Development Workspace)
- **Purpose:** Work-in-progress plugins and development materials
- **Access:** Owner and invited collaborators only
- **Location:** `private/` directory (git submodule)
- **Public visibility:** Reference visible, contents not accessible

---

## Plugin Development Workflow

**Complete guide:** `private/notes/PLUGIN_DEVELOPMENT_WORKFLOW.md` (9,000+ lines)

### 7-Phase Development Cycle:

1. **Planning & Design**
   - Validate idea against 5 design questions
   - Gather research from authoritative sources
   - Design systematic workflow
   - Location: `private/notes/`, `private/research/`

2. **Development**
   - Copy template: `private/wip-plugins/_TEMPLATE/`
   - Create plugin structure in `private/wip-plugins/{plugin-name}/`
   - Write SKILL.md (agent prompt)
   - Create plugin.json (manifest)
   - Develop automation scripts
   - Write reference materials
   - Location: `private/wip-plugins/{plugin-name}/`

3. **Testing**
   - Use checklist: `private/notes/TESTING_CHECKLIST_TEMPLATE.md`
   - Test on minimum 3 real codebases
   - Verify all scripts work
   - Check against design principles
   - Location: `private/test-data/`

4. **Documentation Review**
   - Complete SKILL.md, plugin.json, README.md
   - Verify all reference materials cited
   - Check for placeholders or broken links

5. **Pre-Release**
   - Finalize version numbers
   - Create release notes
   - Complete testing sign-off

6. **Publication**
   - Copy from `private/wip-plugins/{plugin-name}/` to `./{plugin-name}/`
   - Update `.claude-plugin/marketplace.json`
   - Update README.md, CHANGELOG.md, MARKETPLACE.md
   - Commit and push to public repository
   - Create GitHub release

7. **Post-Release**
   - Announce in community
   - Monitor issues and feedback
   - Plan updates in private workspace

### Key Commands:

**Start new plugin:**
```bash
cd private/wip-plugins/
cp -r _TEMPLATE {plugin-name}
cd {plugin-name}
# Edit SKILL.md, plugin.json, README.md
```

**Test plugin with Claude:**
```bash
# Copy to temp location
cp -r private/wip-plugins/{plugin-name} /tmp/
# In Claude Code:
"Using the skill at /tmp/{plugin-name}, audit [target]"
```

**Publish plugin:**
```bash
cp -r private/wip-plugins/{plugin-name} ./{plugin-name}/
# Edit .claude-plugin/marketplace.json to add plugin entry
git add .
git commit -m "Add {Plugin Name} v1.0.0"
git push
```

---

## Marketplace Management

### Adding Plugin to Marketplace

Edit `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "plugin-name",
      "description": "One-sentence description of deliverable",
      "source": "./plugin-name",
      "version": "1.0.0",
      "author": {
        "name": "Diego Consolini",
        "email": "diego@diegocon.nl"
      },
      "category": "security",
      "keywords": ["keyword1", "keyword2"],
      "homepage": "https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/plugin-name",
      "repository": "https://github.com/diegocconsolini/ClaudeSkillCollection",
      "license": "MIT"
    }
  ]
}
```

### Installing from Marketplace

**End users:**
```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
/plugin install gdpr-auditor@security-compliance-marketplace
```

**Traditional installation:**
```bash
cd ~/.claude/skills/
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git
ln -s ClaudeSkillCollection/gdpr-auditor ./gdpr-auditor
```

---

## Plugin Structure Requirements

Each plugin MUST contain:

```
plugin-name/
├── SKILL.md              # Claude agent prompt (REQUIRED)
│   ├── Frontmatter: name, description, license
│   ├── Purpose and capabilities
│   ├── When to use / when NOT to use
│   ├── Systematic workflow (phases and steps)
│   ├── Reference materials list
│   ├── Output format specification
│   ├── Defensive security note
│   └── Example usage and limitations
│
├── plugin.json           # Plugin manifest (REQUIRED)
│   ├── Schema, name, version, description
│   ├── Author info (diego@diegocon.nl)
│   ├── Keywords and category
│   └── Agent configuration pointing to SKILL.md
│
├── README.md             # User documentation (REQUIRED)
│   ├── Version, features, installation
│   ├── Usage examples
│   ├── Script documentation
│   └── Limitations and disclaimers
│
├── references/           # Reference materials (REQUIRED)
│   ├── Authoritative sources cited
│   ├── Official regulations/standards
│   └── Implementation guidelines
│
├── scripts/              # Automation tools (optional)
│   ├── Python 3.8+ scripts
│   ├── Error handling
│   └── Work with static files only
│
└── examples/             # Sample outputs (recommended)
    └── Example deliverables
```

---

## Testing Requirements

**Checklist:** `private/notes/TESTING_CHECKLIST_TEMPLATE.md`

### Mandatory Tests:
1. **Design Validation** - Pass all 5 design criteria
2. **Functional Testing** - All scripts work, Claude follows workflow
3. **Real-World Testing** - Minimum 3 actual codebases
4. **Documentation** - Complete, accurate, no placeholders
5. **Security** - Defensive only, no malicious code
6. **Performance** - Completes in reasonable time (<5 min for medium codebase)

### Testing on Real Codebases:
- Small codebase (<100 files)
- Medium codebase (100-1000 files)
- Large codebase (1000-10k files)

Must verify:
- Findings are accurate (no false positives)
- Output is actionable
- Cites specific locations (file:line)
- References authoritative sources correctly

---

## Quality Standards

### Code Quality (Python Scripts):
- Python 3.8+ compatible
- Type hints and docstrings
- Error handling (never crash)
- No external API calls (unless essential and documented)
- No hardcoded credentials
- Executable permissions (`chmod +x`)

### Reference Materials:
- Cite authoritative sources (EUR-Lex, NIST, OWASP, ISO, etc.)
- Include URLs to official documentation
- Add publication/retrieval dates
- Verify accuracy against primary sources
- No hallucinated facts

### Documentation:
- No placeholder text ("TODO", "Coming soon")
- No broken links
- Professional tone
- Clear for non-experts
- Includes limitations and disclaimers

---

## Private Workspace Usage

The `private/` submodule is for development work before public release.

### Common Operations:

**Work in private workspace:**
```bash
cd private/wip-plugins/{plugin-name}/
# Make changes
git add .
git commit -m "Progress on {plugin-name}"
git push
```

**Update main repo to track private changes:**
```bash
cd /path/to/ClaudeSkillCollection
git add private/
git commit -m "Update private submodule reference"
git push
```

**Clone with submodule:**
```bash
git clone --recurse-submodules https://github.com/diegocconsolini/ClaudeSkillCollection.git
```

**Public users cannot access private submodule contents** - only see the reference.

---

## Contribution Guidelines

**Review CONTRIBUTING.md before submitting.**

### Submission Checklist:
- [ ] Passes all 5 design validation criteria
- [ ] Tested on 3+ real codebases
- [ ] All reference materials from authoritative sources
- [ ] Complete documentation (SKILL.md, plugin.json, README.md)
- [ ] No malicious code, defensive security only
- [ ] MIT License
- [ ] Production-ready (not a proof-of-concept)

### Grounds for Rejection:
- Requires live system access or real-time monitoring
- Depends on external APIs or third-party services
- Makes subjective judgments without objective criteria
- No tangible deliverable produced
- Contains malicious code or offensive security tools
- Unverified claims or fake examples
- Plagiarized content

---

## Version Management

**Semantic Versioning (SemVer):** `MAJOR.MINOR.PATCH`

- **MAJOR** - Breaking changes or incompatible API changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

### Version Locations:
- `plugin.json`: `"version": "1.0.0"`
- `README.md`: `**Version:** 1.0.0`
- `.claude-plugin/marketplace.json`: Update plugin entry version

### CHANGELOG.md:
Update with each release following Keep a Changelog format.

---

## Available Plugins

### 1. GDPR Auditor (v1.0.0)
**Status:** Production Ready
**Description:** GDPR compliance auditing for EU data protection (static file analysis only)
**Features:** 8 reference docs, 5 automation scripts (analyze code/schema files), comprehensive audit reports
**Install:** `/plugin install gdpr-auditor@security-compliance-marketplace`

### Roadmap (12+ Planned):
- CCPA Auditor (California Consumer Privacy Act)
- HIPAA Compliance Checker (US healthcare)
- PCI DSS Security Auditor (Payment card industry)
- Security Vulnerability Scanner (OWASP Top 10)
- API Security Auditor
- Accessibility Auditor (WCAG 2.1)
- And more...

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `SKILL_DESIGN_PRINCIPLES.md` | Core design philosophy (600+ lines) |
| `CONTRIBUTING.md` | Contribution guidelines |
| `MARKETPLACE.md` | Marketplace documentation |
| `.claude-plugin/marketplace.json` | Marketplace configuration |
| `private/notes/PLUGIN_DEVELOPMENT_WORKFLOW.md` | Complete development guide (9,000+ lines) |
| `private/notes/TESTING_CHECKLIST_TEMPLATE.md` | Testing checklist (500+ lines) |
| `private/wip-plugins/_TEMPLATE/` | Plugin template structure |

---

## Defensive Security Policy

**All tools MUST be defensive security only:**

✅ **Allowed:**
- Identifying vulnerabilities to fix them
- Analyzing code for compliance issues
- Generating remediation recommendations
- Security education and awareness
- Vulnerability research (responsible disclosure)

❌ **NOT Allowed:**
- Live system exploitation
- Credential harvesting or dumping
- Offensive penetration testing tools
- Unauthorized access attempts
- Malicious code or backdoors

---

## Support and Contact

- **Issues:** https://github.com/diegocconsolini/ClaudeSkillCollection/issues
- **Discussions:** https://github.com/diegocconsolini/ClaudeSkillCollection/discussions
- **Maintainer:** Diego Consolini <diego@diegocon.nl>
- **License:** MIT

---

## Working with This Repository

When contributing or developing plugins:

1. **Always validate against design principles first** - Read SKILL_DESIGN_PRINCIPLES.md
2. **Develop in private workspace** - Use `private/wip-plugins/`
3. **Follow the 7-phase workflow** - See `private/notes/PLUGIN_DEVELOPMENT_WORKFLOW.md`
4. **Test thoroughly** - Use `private/notes/TESTING_CHECKLIST_TEMPLATE.md`
5. **Cite authoritative sources** - No hallucinated facts
6. **Focus on deliverables** - What tangible output does it produce?
7. **Defensive security only** - No offensive tools

When in doubt about whether a plugin idea fits this marketplace, ask:
- Does it produce a deliverable?
- Does it work with static files?
- Is it based on objective criteria?
- Does it follow a systematic workflow?
- Can we provide authoritative references?

If all YES → proceed. If any NO → reconsider or redesign.

---

**Last Updated:** 2025-10-19
**Repository Version:** 1.1.0 (with marketplace and private workspace)
**Marketplace Name:** `security-compliance-marketplace`
