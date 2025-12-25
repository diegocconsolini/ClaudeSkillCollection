# MCP (Model Context Protocol) Guide for Claude Code

A practical reference for configuring and managing MCP servers across projects.

---

## Quick Start

```bash
# Add HTTP server (cloud services)
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Add Stdio server (local tools)
claude mcp add --transport stdio db -- npx -y @modelcontextprotocol/server-postgres

# List all servers
claude mcp list

# Authenticate (within Claude Code session)
/mcp
```

---

## Session Strategy: When to Use MCP

### Enable MCP For
- Data retrieval (database queries, API calls)
- External integrations (GitHub, Sentry, Notion)
- Real-time information needs
- Team collaboration features

### Disable/Skip MCP For
- Pure code writing/refactoring
- Security-sensitive work
- Offline development
- Context-limited sessions

### Task-Based Configuration

```bash
# Data analysis session (high limits)
MAX_MCP_OUTPUT_TOKENS=100000 claude

# Secure coding session (minimal MCP)
claude  # Don't add sensitive MCP servers

# Local development (fast startup)
MCP_TIMEOUT=3000 claude
```

---

## Transport Types

| Transport | Use Case | Example |
|-----------|----------|---------|
| **HTTP** | Cloud APIs, remote services | Sentry, GitHub, Notion |
| **Stdio** | Local tools, filesystem access | Database, custom scripts |
| **SSE** | Legacy (deprecated) | Migrate to HTTP |

### HTTP Server

```bash
# Basic
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# With authentication
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_TOKEN}"

# Multiple headers
claude mcp add --transport http secure https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "X-Custom: value"
```

### Stdio Server

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

---

## Scope Levels

| Scope | Location | Shared | Command Flag |
|-------|----------|--------|--------------|
| **Local** | `~/.claude.json` (per-project) | No | (default) |
| **Project** | `.mcp.json` | Yes (git) | `--scope project` |
| **User** | `~/.claude.json` (global) | No | `--scope user` |
| **Enterprise** | `/etc/claude-code/managed-mcp.json` | Yes | (admin) |

### Choosing the Right Scope

```bash
# Personal dev tools → Local (default)
claude mcp add --transport http my-tool https://...

# Team-shared tools → Project
claude mcp add --scope project --transport http shared-api https://...

# Cross-project utilities → User
claude mcp add --scope user --transport http global-tool https://...
```

### Scope Precedence (highest to lowest)
1. Local → 2. Project → 3. User → 4. Enterprise

---

## Configuration Files

### .mcp.json (Project Scope)

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

---

## Commands Reference

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

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MCP_TIMEOUT` | 5000 | Server startup timeout (ms) |
| `MCP_TOOL_TIMEOUT` | 30000 | Tool execution timeout (ms) |
| `MAX_MCP_OUTPUT_TOKENS` | 25000 | Max output per tool call |

### Usage

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

### Persistent Settings

In `.claude/settings.json`:

```json
{
  "env": {
    "MCP_TIMEOUT": "15000",
    "MAX_MCP_OUTPUT_TOKENS": "50000"
  }
}
```

---

## Authentication

### OAuth 2.0 (Interactive)

```bash
# Add server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Authenticate in session
/mcp
# Select "Authenticate" → Browser opens → Login
```

### Bearer Token

```bash
# Set environment variable
export API_TOKEN="your-token"

# Add with header
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_TOKEN}"
```

### API Key

```bash
# Header-based
claude mcp add --transport http service https://api.example.com/mcp \
  --header "X-API-Key: ${SERVICE_API_KEY}"

# Environment-based (Stdio)
claude mcp add --transport stdio tool \
  --env API_KEY="${MY_API_KEY}" \
  -- npx -y tool-server
```

### Security Rules

```bash
# NEVER hardcode secrets
# BAD:
claude mcp add ... --header "Authorization: Bearer sk-secret-123"

# GOOD:
export TOKEN="sk-secret-123"
claude mcp add ... --header "Authorization: Bearer ${TOKEN}"
```

---

## Context Management

### How MCP Affects Context

- Each tool output consumes context tokens
- Default limit: 25,000 tokens per output
- Warning threshold: 10,000 tokens
- Large outputs reduce space for conversation

### Optimization Strategies

```bash
# 1. Limit output tokens
MAX_MCP_OUTPUT_TOKENS=50000 claude

# 2. Request filtered data
> "Query database but only return first 10 rows"
> "Show only id and name fields"

# 3. Use pagination
> "Get first page of results (10 items)"

# 4. Delegate to subagents (isolated context)
> Use the Explore agent to search the codebase
```

### Token-Efficient Workflow

```
Start session
├── Enable only needed MCP servers
├── Use specific queries (not "get everything")
├── Paginate large results
├── Delegate exploration to subagents
└── Clear session if context fills up
```

---

## Best Practices

### Lifecycle Management

```bash
# 1. Add minimal config first
claude mcp add --transport http api https://api.example.com/mcp

# 2. Test it works
/mcp  # Check status

# 3. Add authentication if needed
claude mcp remove api
claude mcp add --transport http api https://... --header "Auth: ${TOKEN}"

# 4. Move to appropriate scope
claude mcp remove api
claude mcp add --scope project ...  # For team sharing
```

### Version Pinning

```json
{
  "mcpServers": {
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "db-server@2.1.0"]
    }
  }
}
```

### Regular Cleanup

```bash
# Review servers
claude mcp list

# Remove unused
claude mcp remove old-server

# Check project .mcp.json
cat .mcp.json | jq .
```

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

## Troubleshooting

### Server Won't Start

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

---

## MCP vs Plugins

| Feature | MCP Servers | Plugins |
|---------|-------------|---------|
| **Purpose** | External data/APIs | Reusable commands |
| **Distribution** | Config files | ZIP packages |
| **Includes** | Tools only | Commands + Agents + MCP |
| **Best For** | Integrations | Workflows |

### Combined Usage

```
Plugin (distributable package)
├── Slash Commands (user interface)
├── Agents (logic)
├── Bundled MCP Servers (auto-start with plugin)
└── Hooks (automation)
```

---

## Quick Reference Card

```bash
# === ADDING SERVERS ===
claude mcp add --transport http name url
claude mcp add --transport stdio name -- command args
claude mcp add --scope project ...  # Team-shared

# === MANAGEMENT ===
claude mcp list                     # View all
claude mcp get name                 # Details
claude mcp remove name              # Delete
/mcp                                # In-session auth

# === ENVIRONMENT ===
MCP_TIMEOUT=15000                   # Startup timeout
MCP_TOOL_TIMEOUT=120000             # Execution timeout
MAX_MCP_OUTPUT_TOKENS=50000         # Output limit

# === FILES ===
.mcp.json                           # Project config (git)
~/.claude.json                      # User/local config
.claude/settings.json               # Preferences
```

---

## Resources

- Official docs: https://docs.anthropic.com/en/docs/claude-code/mcp
- MCP servers: https://github.com/modelcontextprotocol/servers
- Protocol spec: https://modelcontextprotocol.io
