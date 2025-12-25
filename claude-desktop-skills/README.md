# Claude Desktop Skills - ClaudeSkillCollection

This directory contains Claude Desktop skill versions of the 9 ClaudeSkillCollection plugins. These are optimized for Claude Desktop's skill system while maintaining the original Claude Code plugins unchanged.

## Available Skills

### Security & Compliance (4 skills)
1. **GDPR Auditor** (v1.2.0) - GDPR compliance auditing for codebases and databases
2. **Plugin Security Checker** (v3.2.0) - Security scanner for Claude Code plugins with 91 pattern agents
3. **Cybersecurity Policy Generator** (v1.2.0) - Generate policies from 51 SANS/CIS templates
4. **Incident Response Playbook Creator** (v2.2.0) - IR playbooks for 11 incident scenarios

### Productivity & Optimization (2 skills)
5. **Chrome DevTools Optimizer** (v1.0.1) - 70-80% token reduction for Chrome DevTools MCP
6. **Security Report Builder** (v1.0.1) - Generate HTML/PDF/DOCX security reports

### Document Processing (3 skills)
7. **PDF Smart Extractor** (v2.2.0) - Extract large PDFs (3MB-10MB+) with minimal tokens
8. **XLSX Smart Extractor** (v2.2.0) - Analyze Excel workbooks (1MB-50MB+) efficiently
9. **DOCX Smart Extractor** (v2.2.0) - Process Word documents with token optimization

## Quick Start

### Installation

1. **Copy skill to Claude Desktop:**
   ```bash
   cp -r gdpr-auditor ~/.claude/skills/
   ```

2. **Install dependencies (if required):**
   ```bash
   cd ~/.claude/skills/gdpr-auditor
   pip install -r requirements.txt  # For Python skills
   ```

3. **Follow skill-specific setup:**
   - See each skill's SKILL.md for detailed instructions
   - Some skills require API keys or MCP servers

### Validation

```bash
# Install validator
npm install -g @anthropic/skills-ref

# Validate a skill
skills-ref validate ./gdpr-auditor
```

## Skill Categories

### No Dependencies (Ready to Use)
- GDPR Auditor
- Cybersecurity Policy Generator
- Incident Response Playbook Creator

### Python Dependencies
- PDF Smart Extractor (`pip install pymupdf>=1.23.0`)
- XLSX Smart Extractor (`pip install openpyxl`)
- DOCX Smart Extractor (`pip install python-docx`)
- Plugin Security Checker (`pip install -r requirements.txt`)

### External APIs (Optional)
- Chrome DevTools Optimizer (Gemini Flash API for 50% additional token savings)

### MCP Server Requirements
- Chrome DevTools Optimizer (requires chrome-devtools MCP server)

## Differences from Claude Code Plugins

These Desktop skills are **additional versions**, not replacements:

| Aspect | Claude Code Plugin | Desktop Skill |
|--------|-------------------|---------------|
| Entry file | `agents/*.md` | `SKILL.md` |
| Manifest | `.claude-plugin/plugin.json` | Frontmatter in SKILL.md |
| Frontmatter | `capabilities`, `tools`, `model` | `name`, `description`, `license` |
| Loading | Plugin system | Skill system |
| Location | Plugin directory | `~/.claude/skills/` |

## Contributing

These skills are derived from ClaudeSkillCollection plugins. To contribute:

1. Report issues in the main repository
2. Suggest improvements to skill packaging
3. Test skills on different platforms (macOS/Linux/Windows)

## License

All skills are licensed under MIT License (see individual skill directories).

## Resources

- **Original Plugins:** https://github.com/diegocconsolini/ClaudeSkillCollection
- **Claude Desktop Docs:** https://docs.anthropic.com/claude/docs/desktop
- **Skill Spec:** https://agentskills.io/specification
