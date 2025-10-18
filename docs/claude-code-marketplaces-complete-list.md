# Complete Claude Code Plugin Marketplaces List

Last Updated: 2025-10-18

## Official Anthropic Marketplaces

### 1. **anthropics/skills** ✅ INSTALLED
Core skills and agent capabilities from Anthropic.

```bash
/plugin marketplace add anthropics/skills
```

**Plugins:**
- Agent Skills (automatically activate based on context)
- Core development workflows

---

### 2. **anthropics/claude-code**
Official Claude Code repository with bundled plugins.

```bash
/plugin marketplace add anthropics/claude-code
```

**Included Plugins:**
- `agent-sdk-dev` - Claude Agent SDK development tools
- `pr-review-toolkit` - PR review automation
- `commit-commands` - Git commit helpers
- Meta-plugin for creating new plugins

---

## Large Community Marketplaces

### 3. **jeremylongshore/claude-code-plugins-plus** 🔥 227 PLUGINS
Largest marketplace with Skills Powerkit.

```bash
/plugin marketplace add jeremylongshore/claude-code-plugins-plus
```

**Categories (14 total):**
- DevOps Automation Pack
- Security Pro Pack
- Fullstack Starter Pack
- AI/ML Engineering Pack
- Database tools
- API debugging
- Testing suites
- Documentation generation

**Notable:** 164 plugins with intelligent Agent Skills that auto-activate based on context.

**Browse:** https://jeremylongshore.github.io/claude-code-plugins/

---

### 4. **ananddtyagi/claude-code-marketplace** 📦 115 PLUGINS
Community-driven marketplace with live database sync.

```bash
/plugin marketplace add ananddtyagi/claude-code-marketplace
```

**Featured Plugins:**
- Documentation Generator
- Lyra (AI prompt optimization specialist)
- Analyze Codebase
- Update Claude.md
- Ultrathink
- Security Audit

**Submit commands:** https://claudecodecommands.directory/submit

---

### 5. **obra/superpowers-marketplace** 💪 CORE SKILLS
Comprehensive skills library with proven techniques.

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**Skills Categories:**
- Testing Skills (TDD, async testing, anti-patterns)
- Debugging Skills (systematic debugging, root cause tracing)
- Collaboration Skills (brainstorming, planning, code review, parallel agents)
- Meta Skills (creating, testing, contributing skills)

**Commands:**
- `/brainstorm` - Interactive design refinement
- `/write-plan` - Create implementation plan
- `/execute-plan` - Execute plan in batches

**Version:** 3.0.1 by Jesse Vincent (MIT License)

**Skills repo:** https://github.com/obra/superpowers-skills

---

### 6. **ccplugins/marketplace** ⭐ CURATED
Curated collection of awesome plugins only.

```bash
/plugin marketplace add ccplugins/marketplace
```

**Focus:** Quality over quantity - only well-tested, production-ready plugins.

---

### 7. **dotclaude/marketplace** 🚀 14 PLUGINS, 70+ COMMANDS
Revolutionary AI interaction platform.

```bash
/plugin marketplace add dotclaude/marketplace
```

**Contents:**
- 14 specialized plugins
- 70+ commands
- 78 expert agents
- Full development lifecycle coverage

---

## Specialized Marketplaces

### 8. **EveryInc/every-marketplace** 🏢 ENTERPRISE
Official Every-Env marketplace for engineering workflows.

```bash
/plugin marketplace add EveryInc/every-marketplace
```

**Featured:**
- Compounding Engineering Philosophy plugin
- Code review with multiple expert perspectives
- Automated testing and bug reproduction
- PR management and parallel comment resolution
- Documentation generation and maintenance
- Security, performance, and architecture analysis

**Quick install:**
```bash
npx claude-plugins install @EveryInc/every-marketplace/compounding-engineering
```

---

### 9. **brennercruvinel/CCPlugins** ⚡ 24 PROFESSIONAL COMMANDS
Enterprise-grade development workflows framework.

```bash
/plugin marketplace add brennercruvinel/CCPlugins
```

**Quick Install (Mac/Linux):**
```bash
curl -sSL https://raw.githubusercontent.com/brennercruvinel/CCPlugins/main/install.sh | bash
```

**Features:**
- 24 curated professional commands
- First-person collaborative language
- Optimized for Opus 4 and Sonnet 4
- 1.5k+ stars on GitHub

**Note:** V2 in active development with complete architectural redesign.

---

### 10. **DustyWalker/claude-code-marketplace**
Production-ready AI agents marketplace.

```bash
/plugin marketplace add DustyWalker/claude-code-marketplace
```

**Focus:** Production-ready AI agents and workflows.

---

## How to Use

### Browse All Plugins
```bash
/plugin
```
Select "Browse Plugins" to see available options.

### Add Marketplace
```bash
/plugin marketplace add <user-or-org>/<repo-name>
```

### Install Plugin
```bash
/plugin install <plugin-name>@<marketplace-name>
```

### Remove Marketplace
```bash
/plugin marketplace remove <marketplace-name>
```

---

## Quick Start Recommendations

**For beginners:**
1. `anthropics/skills` - Core skills (already installed ✅)
2. `obra/superpowers-marketplace` - Proven workflows
3. `ccplugins/marketplace` - Curated quality plugins

**For comprehensive coverage:**
1. `jeremylongshore/claude-code-plugins-plus` - 227 plugins with auto-activation
2. `ananddtyagi/claude-code-marketplace` - 115 community plugins

**For enterprise/teams:**
1. `EveryInc/every-marketplace` - Enterprise workflows
2. `brennercruvinel/CCPlugins` - Professional command framework

---

## Creating Your Own Marketplace

To host a marketplace, you need:
1. Git repository (GitHub recommended)
2. `.claude-plugin/marketplace.json` file with proper format

**Resources:**
- Official docs: https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
- Reference: https://github.com/anthropics/claude-code/blob/main/.claude-plugin/marketplace.json

---

## Notes

- Plugin system launched October 2025 (in public beta)
- Works across terminal and VS Code
- Plugins can include: slash commands, agents, MCP servers, hooks
- Agent Skills auto-activate based on conversation context (no commands to remember)
- Most marketplaces are actively maintained and updated

---

**Total Marketplaces Listed:** 10
**Estimated Total Plugins Available:** 600+
**Categories Covered:** 20+
