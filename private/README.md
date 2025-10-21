# ClaudeSkillCollection - Private Development Repository

**Private repository for work-in-progress plugins and development materials**

This repository contains non-public development files, research, drafts, and work-in-progress plugins for the [ClaudeSkillCollection](https://github.com/diegocconsolini/ClaudeSkillCollection) marketplace.

---

## Purpose

This private repository stores:
- Work-in-progress plugins (not ready for public release)
- Research and reference materials
- Draft documentation
- Test data and examples
- Development notes
- Experimental features

---

## Folder Structure

```
ClaudeSkillCollection-Private/
├── README.md                  # This file
├── drafts/                    # Draft documentation and ideas
├── research/                  # Research materials and references
├── wip-plugins/              # Work-in-progress plugins
├── test-data/                # Test datasets (non-sensitive)
└── notes/                    # Development notes and planning
```

---

## Usage

### Accessing This Repository

This repository is a **git submodule** within the main ClaudeSkillCollection repository.

**From the main repository:**
```bash
cd ClaudeSkillCollection
cd private/    # This is the submodule
```

**Clone with submodule:**
```bash
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git
cd ClaudeSkillCollection
git submodule init
git submodule update
```

---

## Workflow

### Working on a New Plugin

1. **Create in `wip-plugins/`:**
   ```bash
   cd private/wip-plugins/
   mkdir ccpa-auditor
   cd ccpa-auditor
   # Develop the plugin
   ```

2. **Test and refine privately**

3. **When ready, move to public repo:**
   ```bash
   cd /path/to/ClaudeSkillCollection
   cp -r private/wip-plugins/ccpa-auditor ./ccpa-auditor
   # Update marketplace.json
   # Commit to public repo
   ```

### Research and Notes

```bash
cd private/research/
# Add research materials, legal references, etc.
git add .
git commit -m "Add CCPA research materials"
git push
```

---

## Security

**This repository should contain:**
- ✅ Non-sensitive development materials
- ✅ Work-in-progress code
- ✅ Research and drafts
- ✅ Test data (sanitized)

**This repository should NOT contain:**
- ❌ API keys or credentials
- ❌ Sensitive user data
- ❌ Production secrets
- ❌ Personally identifiable information (PII)

For sensitive credentials, use environment variables or a password manager.

---

## Folder Guidelines

### `/drafts`
Draft documentation, blog posts, announcements, and ideas before they're ready for publication.

### `/research`
Research materials, legal references, compliance documentation, technical specifications, and reference implementations.

### `/wip-plugins`
Complete plugin directories that are being developed but not ready for public release. Each should follow the same structure as public plugins:
```
wip-plugins/
└── ccpa-auditor/
    ├── README.md
    ├── SKILL.md
    ├── plugin.json
    ├── scripts/
    └── references/
```

### `/test-data`
Sample test data, example codebases, and testing scenarios. **Ensure all data is sanitized and contains no sensitive information.**

### `/notes`
Development notes, planning documents, roadmaps, meeting notes, and ideas.

---

## Git Workflow

**Commit regularly:**
```bash
cd private/
git add .
git commit -m "Descriptive commit message"
git push
```

**The main repository only tracks the submodule reference, not the contents.**

---

## Syncing with Main Repository

When you update this private repository, you need to update the submodule reference in the main repository:

```bash
# In the main repository
cd ClaudeSkillCollection
git add private/
git commit -m "Update private submodule reference"
git push
```

---

## Access Control

**Who can see this:**
- Only you (repository owner)
- Collaborators you explicitly invite

**Public repository visitors:**
- Can see that a `private/` submodule exists
- Cannot access the contents
- Cannot clone the submodule without permissions

---

## Maintenance

### Regular Cleanup
- Archive completed research
- Move completed plugins to public repository
- Remove obsolete notes
- Update this README as needed

### Version Control
- Commit early and often
- Use descriptive commit messages
- Tag major milestones
- Keep a changelog (optional)

---

## Related Repositories

**Public Marketplace:**
- [ClaudeSkillCollection](https://github.com/diegocconsolini/ClaudeSkillCollection) - Public plugin marketplace

**This Repository:**
- Private development workspace
- Linked as submodule in main repository

---

## Contact

**Owner:** Diego Consolini
**Email:** diego@diegocon.nl
**Main Repository:** https://github.com/diegocconsolini/ClaudeSkillCollection

---

**Last Updated:** 2025-10-19
**Repository Type:** Private Development
**Submodule Path:** `private/` in main repository
