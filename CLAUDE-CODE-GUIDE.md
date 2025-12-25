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
8. [Troubleshooting](#troubleshooting)
9. [Quick Reference](#quick-reference)

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
src/
├── components/   # React components
├── services/     # Business logic
├── utils/        # Helpers
└── types/        # TypeScript types

## Coding Standards
- Use functional components with hooks
- Prefer async/await over promises
- All functions must have JSDoc comments

## Commands
npm run dev      # Development server
npm run test     # Run tests
npm run build    # Production build

## Important Files
- src/config.ts - Environment configuration
- src/api/index.ts - API routes
- .env.example - Required environment variables

## Don't
- Don't modify files in vendor/
- Don't commit .env files
- Don't use any type in TypeScript
```

### Best Practices

```
DO include:
- Build/test commands
- Project structure overview
- Critical patterns to follow
- Files to never modify

DON'T include:
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

### Transport Types

| Transport | Use Case | Example |
|-----------|----------|---------|
| **HTTP** | Cloud APIs, remote services | Sentry, GitHub, Notion |
| **Stdio** | Local tools, filesystem access | Database, custom scripts |
| **SSE** | Legacy (deprecated) | Migrate to HTTP |

### Quick Setup

```bash
# HTTP (cloud services)
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Stdio (local tools)
claude mcp add --transport stdio db -- npx -y pg-mcp-server

# With auth
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}"

# Multiple headers
claude mcp add --transport http secure https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "X-Custom: value"
```

### Stdio Server Examples

```bash
# NPM package
claude mcp add --transport stdio airtable -- npx -y airtable-mcp-server

# With environment variables
claude mcp add --transport stdio postgres \
  --env DATABASE_URL="${DB_URL}" \
  -- npx -y @modelcontextprotocol/server-postgres

# Python script
claude mcp add --transport stdio custom -- python /path/to/server.py

# Windows (requires cmd wrapper)
claude mcp add --transport stdio tool -- cmd /c npx -y @package/name
```

### Scope Levels

| Scope | Location | Shared | Command Flag |
|-------|----------|--------|--------------|
| **Local** | `~/.claude.json` (per-project) | No | (default) |
| **Project** | `.mcp.json` | Yes (git) | `--scope project` |
| **User** | `~/.claude.json` (global) | No | `--scope user` |
| **Enterprise** | `/etc/claude-code/managed-mcp.json` | Yes | (admin) |

**Scope Precedence:** Local → Project → User → Enterprise

```bash
# Personal dev tools → Local (default)
claude mcp add --transport http my-tool https://...

# Team tools → Project (creates .mcp.json)
claude mcp add --scope project --transport http shared https://...

# Global utilities → User
claude mcp add --scope user --transport http utility https://...
```

### .mcp.json Configuration

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "pg-mcp-server@2.1.0"],
      "env": {
        "DATABASE_URL": "${DB_URL}",
        "POOL_SIZE": "${DB_POOL:-10}"
      }
    }
  }
}
```

### Variable Expansion

```json
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "${API_BASE:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      },
      "env": {
        "TIMEOUT": "${TIMEOUT:-30000}"
      }
    }
  }
}
```

**Supported variables:**
- `${VAR}` - Environment variable
- `${VAR:-default}` - With fallback
- `${HOME}`, `${PWD}` - System paths
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory

### MCP Commands Reference

```bash
# Add servers
claude mcp add --transport http <name> <url> [--header "Key: Value"]
claude mcp add --transport stdio <name> [--env KEY=val] -- <command> [args]
claude mcp add --scope <local|project|user> ...

# List and inspect
claude mcp list                    # All servers
claude mcp get <name>              # Server details

# Remove
claude mcp remove <name>           # Remove server

# Advanced
claude mcp add-json <name> '<json>' [--scope scope]  # Add from JSON
claude mcp add-from-claude-desktop                    # Import from Desktop
claude mcp reset-project-choices                      # Reset approvals
claude mcp serve                                       # Run as MCP server

# In-session (within Claude Code)
/mcp                               # Manage, authenticate, view status
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MCP_TIMEOUT` | 5000 | Server startup timeout (ms) |
| `MCP_TOOL_TIMEOUT` | 30000 | Tool execution timeout (ms) |
| `MAX_MCP_OUTPUT_TOKENS` | 25000 | Max output per tool call |

```bash
# Slow-starting servers
MCP_TIMEOUT=15000 claude

# Long-running queries
MCP_TOOL_TIMEOUT=120000 claude

# Large data operations
MAX_MCP_OUTPUT_TOKENS=100000 claude

# Combined
MCP_TIMEOUT=15000 MCP_TOOL_TIMEOUT=120000 MAX_MCP_OUTPUT_TOKENS=50000 claude
```

### Authentication Methods

**OAuth 2.0 (Interactive):**
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
# Then in session: /mcp → Authenticate → Browser opens
```

**Bearer Token:**
```bash
export API_TOKEN="your-token"
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_TOKEN}"
```

**API Key:**
```bash
# Header-based
claude mcp add --transport http service https://api.example.com/mcp \
  --header "X-API-Key: ${SERVICE_API_KEY}"

# Environment-based (Stdio)
claude mcp add --transport stdio tool \
  --env API_KEY="${MY_API_KEY}" \
  -- npx -y tool-server
```

**Security Rules:**
```bash
# NEVER hardcode secrets
# BAD:
claude mcp add ... --header "Authorization: Bearer sk-secret-123"

# GOOD:
export TOKEN="sk-secret-123"
claude mcp add ... --header "Authorization: Bearer ${TOKEN}"
```

### MCP Best Practices

1. **Start minimal** - Add servers as needed
2. **Use appropriate scope** - Project for team, local for experiments
3. **Pin versions** - `pkg@1.2.3` in args
4. **Never hardcode secrets** - Use `${ENV_VAR}`
5. **Clean up regularly** - `claude mcp list` → remove unused

### Team Collaboration

```bash
# Use project scope for shared servers
claude mcp add --scope project --transport http github https://...

# Document in .mcp.json (commit to git)
git add .mcp.json
git commit -m "Add GitHub MCP integration"

# Team members approve on first use
/mcp  # Approve project servers
```

### Auto-Approval Settings

In `.claude/settings.json`:

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["github", "sentry"],
  "disabledMcpjsonServers": ["experimental"]
}
```

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

## Troubleshooting

### MCP Server Won't Start

```bash
# Increase timeout
MCP_TIMEOUT=15000 claude

# Test command manually
npx -y package-name

# Check dependencies
npm list -g package-name
```

### Authentication Fails

```bash
# Re-authenticate
/mcp → Clear authentication → Authenticate again

# Verify token is set
echo $API_TOKEN

# Check header format
claude mcp get server-name
```

### Tools Not Appearing

```bash
# Check server status
/mcp

# Verify server is running
claude mcp list

# Restart Claude Code
exit
claude
```

### Windows Stdio Issues

```bash
# WRONG
claude mcp add --transport stdio server -- npx -y @package

# CORRECT (use cmd /c wrapper)
claude mcp add --transport stdio server -- cmd /c npx -y @package
```

### Large Output Warnings

```bash
# Increase limit
MAX_MCP_OUTPUT_TOKENS=100000 claude

# Or request less data
> "Show only first 10 results"
```

### Context Full

```bash
# Signs: slow responses, forgotten context
# Solution:
1. Complete current task
2. Exit and restart Claude Code
3. Start fresh with minimal context
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
npm run dev
npm run test

## Structure
src/
├── ...
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
