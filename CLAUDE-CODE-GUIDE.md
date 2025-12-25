# Claude Code Project Guide

A universal reference for optimizing Claude Code across any project. Copy this to your projects or reference it globally.

---

## Table of Contents

1. [CLAUDE.md Configuration](#claudemd-configuration)
2. [Session Strategy](#session-strategy)
3. [Plugins Management](#plugins-management)
4. [MCP Servers](#mcp-servers)
5. [Context Optimization](#context-optimization)
6. [Subagents & Delegation](#subagents--delegation)
7. [Settings & Permissions](#settings--permissions)
8. [Quick Reference](#quick-reference)

---

## CLAUDE.md Configuration

### Purpose

CLAUDE.md provides project-specific instructions that Claude Code reads automatically. Use it to:
- Define coding standards and patterns
- Document project structure
- Set behavioral guidelines
- Provide context Claude needs

### File Locations (Priority Order)

| Location | Scope | Use Case |
|----------|-------|----------|
| `./CLAUDE.md` | Project root | Main project instructions |
| `./CLAUDE.local.md` | Personal | Your overrides (gitignored) |
| `~/.claude/CLAUDE.md` | Global | Cross-project defaults |
| `./dir/CLAUDE.md` | Directory | Submodule-specific rules |

### Effective CLAUDE.md Structure

```markdown
# Project Name

Brief description of what this project does.

## Tech Stack
- Language: TypeScript/Python/etc
- Framework: React/FastAPI/etc
- Database: PostgreSQL/MongoDB/etc

## Project Structure
```
src/
├── components/   # React components
├── services/     # Business logic
├── utils/        # Helpers
└── types/        # TypeScript types
```

## Coding Standards
- Use functional components with hooks
- Prefer async/await over promises
- All functions must have JSDoc comments

## Commands
```bash
npm run dev      # Development server
npm run test     # Run tests
npm run build    # Production build
```

## Important Files
- `src/config.ts` - Environment configuration
- `src/api/index.ts` - API routes
- `.env.example` - Required environment variables

## Don't
- Don't modify files in `vendor/`
- Don't commit `.env` files
- Don't use `any` type in TypeScript
```

### Best Practices

```markdown
# Keep it concise - Claude reads this every session
# Focus on what Claude needs to know, not documentation

## DO include:
- Build/test commands
- Project structure overview
- Critical patterns to follow
- Files to never modify

## DON'T include:
- Lengthy documentation
- Historical context
- Marketing content
- Redundant info from README
```

### Local Overrides

Create `CLAUDE.local.md` for personal preferences (add to `.gitignore`):

```markdown
# My Local Preferences

## Environment
- My API key: Use $DEV_API_KEY
- Local DB: postgresql://localhost/mydb

## Preferences
- I prefer verbose explanations
- Always run tests before committing
```

---

## Session Strategy

### Starting a Session

```bash
# Minimal session (pure coding)
claude

# With increased MCP limits (data work)
MAX_MCP_OUTPUT_TOKENS=100000 claude

# Fast local development
MCP_TIMEOUT=3000 claude
```

### Task-Based Configuration

| Task Type | Plugins | MCP | Context Strategy |
|-----------|---------|-----|------------------|
| **Code writing** | Minimal | None/Local | Full context for code |
| **Data analysis** | None | Database, APIs | High output limits |
| **Research** | None | Web, Search | Delegate to subagents |
| **Security work** | Security only | None | Isolated, no network |
| **Debugging** | Debugger | Logs, Monitoring | Focused on error |

### Context-Efficient Workflow

```
Session Start
├── Load only needed plugins/MCP
├── Use CLAUDE.md for project context
├── Delegate exploration to subagents
├── Request specific data (not "everything")
└── Clear session if context fills
```

### When to Start Fresh

- Context feels "stale" or confused
- Major task switch (coding → data analysis)
- After long debugging sessions
- When responses become slower

---

## Plugins Management

### Plugin vs MCP Decision

| Need | Use Plugin | Use MCP |
|------|------------|---------|
| Reusable commands | Yes | - |
| Team distribution | Yes | - |
| External API access | - | Yes |
| Real-time data | - | Yes |
| Packaged workflows | Yes | - |
| Database queries | - | Yes |

### Plugin Lifecycle

```bash
# Install when needed
/plugin install gdpr-auditor

# Use the plugin
/gdpr-auditor analyze ./src

# Uninstall when done (saves context)
/plugin uninstall gdpr-auditor
```

### Context Impact

- Installed plugins consume context
- Each plugin adds tool definitions
- Uninstall unused plugins between tasks
- Keep 3-5 most-used plugins installed

### Plugin Best Practices

```bash
# Start session with minimal plugins
claude

# Install for specific task
/plugin install security-auditor
# ... do security work ...
/plugin uninstall security-auditor

# Keep core plugins only
/plugin list  # Review regularly
```

---

## MCP Servers

### Quick Setup

```bash
# HTTP (cloud services)
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Stdio (local tools)
claude mcp add --transport stdio db -- npx -y pg-mcp-server

# With auth
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}"
```

### Scope Selection

```bash
# Personal dev tools → Local (default)
claude mcp add --transport http my-tool https://...

# Team tools → Project (creates .mcp.json)
claude mcp add --scope project --transport http shared https://...

# Global utilities → User
claude mcp add --scope user --transport http utility https://...
```

### .mcp.json Template

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "pg-mcp@2.0.0"],
      "env": {
        "DATABASE_URL": "${DB_URL}"
      }
    }
  }
}
```

### Environment Variables

```bash
MCP_TIMEOUT=15000           # Startup timeout (ms)
MCP_TOOL_TIMEOUT=120000     # Execution timeout (ms)
MAX_MCP_OUTPUT_TOKENS=50000 # Output limit (default: 25000)
```

### MCP Best Practices

1. **Start minimal** - Add servers as needed
2. **Use appropriate scope** - Project for team, local for experiments
3. **Pin versions** - `pkg@1.2.3` in args
4. **Never hardcode secrets** - Use `${ENV_VAR}`
5. **Clean up regularly** - `claude mcp list` → remove unused

---

## Context Optimization

### What Consumes Context

| Source | Impact | Optimization |
|--------|--------|--------------|
| CLAUDE.md | Low | Keep concise |
| Conversation | Medium | Start fresh sessions |
| File reads | Medium | Read specific lines |
| MCP outputs | High | Limit/paginate results |
| Plugin tools | Medium | Uninstall unused |

### Reducing Context Usage

```bash
# 1. Use subagents for exploration
> "Use Explore agent to find authentication handlers"
# Results stay in subagent context

# 2. Request specific data
> "Show first 10 rows from users table"
# Not: "Show all users"

# 3. Read specific file sections
> "Read lines 50-100 of src/auth.ts"
# Not: "Read src/auth.ts"

# 4. Paginate MCP results
> "Get page 1 of issues (10 per page)"
```

### Subagent Delegation

```bash
# Exploration (isolated context)
> "Use Explore agent to understand the codebase structure"

# Research (doesn't pollute main context)
> "Use search-specialist to find React form validation patterns"

# Analysis (separate context window)
> "Use code-analyzer to review security of auth module"
```

### Context Recovery

```bash
# When context gets full:
1. Complete current task
2. Exit Claude Code
3. Start fresh session
4. Reference previous work: "Continue from where we left off on X"
```

---

## Subagents & Delegation

### Built-in Agents

| Agent | Use For |
|-------|---------|
| `Explore` | Codebase exploration, finding files |
| `Plan` | Implementation planning |
| `code-reviewer` | Code quality review |
| `security-auditor` | Security analysis |
| `debugger` | Error investigation |
| `test-runner` | Test execution and analysis |

### When to Use Subagents

```bash
# Exploration (saves context)
> "Use Explore to find all API endpoints"

# Complex analysis (isolated processing)
> "Use code-analyzer to check for vulnerabilities in src/"

# Parallel work (concurrent execution)
> "Run these agents in parallel:
   - code-reviewer on src/auth/
   - test-runner for auth tests"
```

### Custom Agent Definition

In `.claude/agents.json`:

```json
{
  "my-agent": {
    "description": "Custom agent for my workflow",
    "tools": ["Read", "Write", "Bash", "Grep"],
    "systemPrompt": "You are a specialist in..."
  }
}
```

---

## Settings & Permissions

### Settings File Location

```
~/.claude/settings.json       # Global settings
.claude/settings.json         # Project settings
.claude/settings.local.json   # Personal (gitignored)
```

### Common Settings

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Read(*)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Write(.env*)",
      "Read(~/.ssh/*)"
    ]
  },
  "env": {
    "MCP_TIMEOUT": "15000",
    "MAX_MCP_OUTPUT_TOKENS": "50000"
  },
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": ["github", "sentry"]
}
```

### Permission Patterns

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",        // NPM scripts
      "Bash(git *)",            // Git commands
      "Bash(docker-compose *)", // Docker
      "Read(**)",               // All files
      "Write(src/**)",          // Source only
      "Edit(src/**)"            // Edit source
    ],
    "deny": [
      "Bash(rm -rf *)",         // Destructive
      "Write(.env*)",           // Secrets
      "Read(~/.ssh/*)"          // SSH keys
    ]
  }
}
```

---

## Quick Reference

### Essential Commands

```bash
# MCP
claude mcp add --transport http name url
claude mcp add --transport stdio name -- command
claude mcp list
claude mcp remove name
/mcp                          # In-session management

# Plugins
/plugin install name
/plugin uninstall name
/plugin list

# Session
/clear                        # Clear conversation
/cost                         # Token usage
/help                         # Help
```

### File Locations

```
Project:
├── CLAUDE.md                 # Project instructions
├── CLAUDE.local.md           # Personal overrides (gitignored)
├── .mcp.json                 # Project MCP servers
└── .claude/
    ├── settings.json         # Project settings
    └── settings.local.json   # Personal settings (gitignored)

Global:
├── ~/.claude.json            # User MCP servers
└── ~/.claude/
    ├── CLAUDE.md             # Global instructions
    └── settings.json         # Global settings
```

### Environment Variables

```bash
# MCP Control
MCP_TIMEOUT=15000             # Server startup (ms)
MCP_TOOL_TIMEOUT=120000       # Tool execution (ms)
MAX_MCP_OUTPUT_TOKENS=50000   # Output limit

# Session
CLAUDE_DEBUG=1                # Debug logging
```

### Workflow Checklist

```
Before Session:
[ ] Set needed environment variables
[ ] Review installed plugins
[ ] Check MCP servers needed

During Session:
[ ] Use subagents for exploration
[ ] Request specific data (not "all")
[ ] Uninstall plugins when done

After Session:
[ ] Clean up temporary MCP servers
[ ] Note any CLAUDE.md updates needed
```

---

## Project Setup Template

### New Project Checklist

```bash
# 1. Create CLAUDE.md
cat > CLAUDE.md << 'EOF'
# Project Name

## Stack
- Language:
- Framework:
- Database:

## Commands
```bash
npm run dev
npm run test
```

## Structure
```
src/
├── ...
```
EOF

# 2. Create .mcp.json (if needed)
cat > .mcp.json << 'EOF'
{
  "mcpServers": {}
}
EOF

# 3. Create .claude/settings.json
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "allow": ["Bash(npm run *)"]
  }
}
EOF

# 4. Update .gitignore
echo "CLAUDE.local.md" >> .gitignore
echo ".claude/settings.local.json" >> .gitignore
```

---

## Resources

- Claude Code docs: https://docs.anthropic.com/en/docs/claude-code
- MCP protocol: https://modelcontextprotocol.io
- MCP servers: https://github.com/modelcontextprotocol/servers
