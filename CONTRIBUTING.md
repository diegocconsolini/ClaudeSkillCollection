# Contributing to Claude Skills Collection

Thank you for your interest in contributing! This document provides guidelines for contributing to the Claude Skills Collection.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Skill Submission Guidelines](#skill-submission-guidelines)
4. [Development Workflow](#development-workflow)
5. [Quality Standards](#quality-standards)
6. [Review Process](#review-process)

---

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving the skills
- Accept criticism gracefully
- Prioritize community benefit

### Not Acceptable

- Malicious code or exploits
- Plagiarized content
- Harassment or discrimination
- Fake examples or documentation
- Unverified claims

---

## How to Contribute

### Reporting Issues

Found a bug or inaccuracy?

1. **Search existing issues** - Check if already reported
2. **Create detailed issue:**
   - Skill name and version
   - Claude Code version
   - Steps to reproduce
   - Expected vs actual behavior
   - Code snippets (anonymized)
   - Screenshots if relevant

### Suggesting Enhancements

Have an idea for improvement?

1. **Open GitHub Discussion** for major changes
2. **Create issue** for specific enhancements
3. **Include:**
   - Clear description of enhancement
   - Use cases and benefits
   - Potential implementation approach
   - Breaking changes (if any)

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or grammar
- Clarify instructions
- Add examples
- Update outdated information
- Translate to other languages

**Process:**
1. Fork repository
2. Make changes
3. Submit pull request
4. Reference related issues

---

## Skill Submission Guidelines

### Before You Start

1. **Check existing skills** - Avoid duplicates
2. **Discuss your idea** - Open GitHub Discussion
3. **Review quality standards** - Ensure you can meet them
4. **Gather authoritative sources** - For reference materials

### Skill Requirements

#### Required Files

```
your-skill-name/
├── SKILL.md              # Claude skill prompt (required)
├── README.md             # Comprehensive documentation (required)
├── scripts/              # Automated tools (if applicable)
├── references/           # Reference materials (required)
├── examples/             # Usage examples (recommended)
└── tests/                # Test cases (recommended)
```

#### SKILL.md Requirements

- Clear skill purpose and scope
- Structured workflow methodology
- When to use skill vs when not to
- Reference to supporting materials
- Defensive security only

**Template:**
```markdown
# Your Skill Name

## Purpose
[Clear 2-3 sentence description]

## When to Use This Skill
- Use case 1
- Use case 2

## Workflow
1. Phase 1: [Description]
2. Phase 2: [Description]

## Reference Materials
- reference1.md - Description
- reference2.md - Description

## Note on Defensive Security
[If applicable]
```

#### README.md Requirements

Must include:
- Version number
- Overview and features
- Installation instructions
- Usage examples
- Limitations and disclaimers
- Authoritative source citations
- Support information

See `gdpr-auditor/README.md` as template.

#### Scripts Requirements (if applicable)

- Python 3.8+ compatible
- Type hints and docstrings
- Error handling
- Standard library preferred (minimal dependencies)
- Defensive security practices
- Tested on real-world examples

**Example script header:**
```python
#!/usr/bin/env python3
"""
Skill Script Name

Description of what this script does.
"""

import os
from typing import List, Dict, Any
from pathlib import Path

def main():
    """Main entry point."""
    pass

if __name__ == "__main__":
    main()
```

#### Reference Materials Requirements

- **Authoritative sources only** - Official docs, standards, regulations
- **Citations required** - Link to original sources
- **Verification date** - When information was verified
- **No hallucinations** - All facts must be verifiable
- **Clear structure** - Use markdown headers, lists, examples

**Example reference header:**
```markdown
# Topic Name

## Overview
[Brief introduction]

## Primary Sources
- [Official Source Name](URL) - Description

## Verified: 2025-10-18

## Content
[Detailed, verified information]
```

### Submission Checklist

Before submitting, verify:

- [ ] SKILL.md follows template and best practices
- [ ] README.md is comprehensive and clear
- [ ] All references cite authoritative sources
- [ ] Scripts are tested and documented
- [ ] Examples are realistic (not fake)
- [ ] No malicious code
- [ ] Follows defensive security principles
- [ ] Quality standards met
- [ ] GitHub Actions tests pass (if added)

---

## Development Workflow

### 1. Fork and Clone

```bash
# Fork repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ClaudeSkillCollection.git
cd ClaudeSkillCollection
git remote add upstream https://github.com/diegocconsolini/ClaudeSkillCollection.git
```

### 2. Create Branch

```bash
# Create feature branch
git checkout -b feature/your-skill-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 3. Develop Skill

```bash
# Create skill directory
mkdir -p your-skill-name/{scripts,references,examples,tests}

# Create required files
touch your-skill-name/SKILL.md
touch your-skill-name/README.md

# Develop and test your skill
```

### 4. Test Locally

```bash
# Copy to Claude skills directory
cp -r your-skill-name ~/.claude/skills/

# Restart Claude Code

# Test skill functionality
# Document test results in tests/ directory
```

### 5. Commit Changes

```bash
# Stage changes
git add your-skill-name/

# Commit with clear message
git commit -m "Add [Skill Name] - [Brief description]

- Feature 1
- Feature 2
- Reference materials from [source]
- Tested on [examples]"
```

### 6. Submit Pull Request

```bash
# Push to your fork
git push origin feature/your-skill-name

# Create pull request on GitHub
# Fill out PR template completely
```

---

## Quality Standards

### Documentation Quality

- **Clarity** - Instructions are easy to follow
- **Completeness** - All necessary information included
- **Accuracy** - No errors or outdated information
- **Examples** - Real-world, tested examples
- **Citations** - All claims backed by sources

### Code Quality

- **Functionality** - Works as documented
- **Reliability** - Handles errors gracefully
- **Security** - No vulnerabilities or malicious code
- **Maintainability** - Clean, documented code
- **Compatibility** - Works on major platforms

### Reference Quality

- **Authoritative** - From official/trusted sources
- **Current** - Up-to-date information
- **Verified** - Facts checked against sources
- **Comprehensive** - Covers topic thoroughly
- **Structured** - Easy to navigate and reference

### Testing Requirements

Skills should be tested on:
- Real-world projects (anonymized)
- Multiple platforms (Windows, macOS, Linux)
- Different Claude Code versions
- Various use cases

Document test results in `tests/` directory.

---

## Review Process

### Timeline

1. **Initial Review** - Within 1 week
   - Completeness check
   - Quality standards verification
   - Security scan

2. **Detailed Review** - 1-2 weeks
   - Code review
   - Documentation review
   - Testing by maintainers

3. **Revisions** - As needed
   - Address feedback
   - Make requested changes

4. **Approval** - After all checks pass
   - Merge to main branch
   - Add to skill catalog
   - Announcement in discussions

### Review Criteria

Reviewers check:

- [ ] Follows submission guidelines
- [ ] Quality standards met
- [ ] No security issues
- [ ] References are authoritative
- [ ] Examples are realistic
- [ ] Documentation is comprehensive
- [ ] Scripts are tested
- [ ] No plagiarism
- [ ] Defensive security principles followed

### Feedback

- Constructive and specific
- References to guidelines
- Suggestions for improvement
- Recognition of good work

---

## Skill Categories

When submitting, choose category:

### Data Privacy & Security
- GDPR, CCPA, HIPAA compliance
- Security audits and vulnerability scanning
- Encryption and access control reviews

### Code Quality & Architecture
- Code review and refactoring
- Architecture analysis
- Performance optimization

### DevOps & Infrastructure
- CI/CD pipeline optimization
- Infrastructure as Code review
- Container and cloud security

### Specialized Domains
- Healthcare, finance, legal tech
- AI/ML ethics and bias detection
- Industry-specific compliance

---

## Style Guide

### Markdown

- Use headers consistently (# for title, ## for sections)
- Code blocks with language specification
- Links to related documents
- Tables for structured data
- Lists for sequential items

### Code

- Follow PEP 8 (Python)
- Use type hints
- Document with docstrings
- Handle errors explicitly
- Avoid external dependencies when possible

### Naming

- Skills: `lowercase-with-hyphens`
- Files: `lowercase_with_underscores.py`
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`

---

## Getting Help

### Questions?

- **GitHub Discussions** - General questions
- **GitHub Issues** - Specific problems
- **Email** - diegocc@example.com (update this)

### Resources

- [Claude Skills Documentation](https://docs.claude.com/claude-code)
- [Existing Skills](./gdpr-auditor/) - Use as templates
- [Installation Guide](./docs/installation.md)

---

## Recognition

Contributors will be:
- Listed in skill README.md
- Mentioned in CHANGELOG
- Credited in repository README

Significant contributions earn:
- Maintainer status
- Decision-making input
- Community recognition

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

All contributed skills must:
- Be your original work or properly attributed
- Not infringe on copyrights or licenses
- Be compatible with MIT License
- Include proper attribution for references

---

## Security

### Reporting Security Issues

**Do not open public issues for security vulnerabilities.**

Email: security@example.com (update this)

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Standards

All skills must:
- Use defensive security practices only
- Not contain exploit code
- Validate all inputs
- Handle sensitive data securely
- Follow principle of least privilege

---

## Contact

- **Maintainer:** Diego Consolini
- **GitHub:** [@diegocconsolini](https://github.com/diegocconsolini)
- **Repository:** https://github.com/diegocconsolini/ClaudeSkillCollection

---

Thank you for contributing to Claude Skills Collection! Your work helps the entire Claude Code community.
