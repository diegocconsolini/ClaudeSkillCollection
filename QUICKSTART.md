# Quick Start Guide

Get started with Security & Compliance Marketplace in 5 minutes.

## Prerequisites

- Claude Code installed and running
- GitHub account (for marketplace access)

## Installation (3 Steps)

### Step 1: Add Marketplace from GitHub

```bash
# Open Claude Code and run:
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
```

**⚠️ Important:** Always use the GitHub repository format (`owner/repo`), NOT a local path. Using local paths prevents remote updates.

❌ Don't use: `/plugin marketplace add /path/to/ClaudeSkillCollection`
✅ Use: `/plugin marketplace add diegocconsolini/ClaudeSkillCollection`

### Step 2: Install Plugins

```bash
# Install plugins from the marketplace
/plugin install gdpr-auditor@security-compliance-marketplace
/plugin install plugin-security-checker@security-compliance-marketplace
/plugin install pdf-smart-extractor@security-compliance-marketplace
```

**Browse available plugins:**
```bash
/plugin  # Interactive plugin browser
```

### Step 3: Enable Plugins and Restart

After installation:

1. Run `/plugin` to open the plugin manager
2. Navigate to each installed plugin
3. Select "Enable plugin"
4. **Restart Claude Code** for plugins to load

**Note:** Plugins are disabled by default after first installation. You must enable them manually.

---

## First Use (2 minutes)

### Test GDPR Auditor

```bash
# In Claude Code:
"Can you audit my application for GDPR compliance?"
```

Claude will automatically invoke the `gdpr-auditor` agent.

### Scan a Plugin for Security Issues

```bash
"Scan this plugin directory for security vulnerabilities: /path/to/plugin"
```

Claude will use `plugin-security-checker` to analyze the code.

### Extract a Large PDF

```bash
"Extract and analyze this PDF: /path/to/document.pdf"
```

Claude will use `pdf-smart-extractor` for efficient processing.

---

## Available Plugins

### Security & Compliance

1. **Plugin Security Checker** (v3.2.0)
   - Scan Claude Code plugins for vulnerabilities
   - 91 specialized detection agents
   - MITRE ATT&CK/ATLAS framework mapping

2. **GDPR Auditor** (v1.2.0)
   - Analyze code for EU data protection compliance
   - 8 reference documents from official sources
   - 5 automated scanning tools

3. **Cybersecurity Policy Generator** (v1.2.0)
   - Generate security policies from 51 templates
   - SANS Institute and CIS Controls
   - ISO 27001, SOC 2, NIST compliance

4. **Incident Response Playbook Creator** (v2.2.0)
   - Generate IR playbooks based on NIST SP 800-61r3
   - 11 comprehensive incident scenarios
   - GDPR/HIPAA notification guidance

### Productivity Tools

5. **PDF Smart Extractor** (v2.2.0)
   - Extract large PDFs (3MB-10MB+)
   - 12-103x token reduction
   - Persistent caching for instant reuse

6. **Excel Smart Extractor** (v2.2.0)
   - Analyze large workbooks (1MB-50MB+)
   - Formula and formatting preservation
   - 20-100x token reduction

7. **Word Smart Extractor** (v2.2.0)
   - Extract Word documents (1MB-50MB+)
   - Heading-based semantic chunking
   - 10-50x token reduction

---

## Updating Plugins

### Method 1: Via Plugin Manager (Recommended)

```bash
/plugin  # Open plugin manager
# Navigate to plugin details
# Select "Update now"
```

### Method 2: Update All Plugins

```bash
/plugin marketplace update security-compliance-marketplace
```

### If You Can't Update (Wrong Installation)

If you see "Local plugins cannot be updated remotely":

```bash
# Remove marketplace
/plugin marketplace remove security-compliance-marketplace

# Re-add using GitHub format
/plugin marketplace add diegocconsolini/ClaudeSkillCollection

# Reinstall plugins
/plugin install gdpr-auditor@security-compliance-marketplace
```

---

## Common Use Cases

### GDPR Compliance Audit

```
"Audit my FastAPI application at /path/to/app for GDPR compliance,
focusing on user data handling and security measures"
```

### Security Policy Generation

```
"Generate an Acceptable Use Policy for my organization with 500 employees
in the healthcare industry"
```

### Incident Response Planning

```
"Create a ransomware incident response playbook for my organization
with GDPR breach notification requirements"
```

### Large Document Analysis

```
"Analyze this 300-page NIST cybersecurity framework PDF and extract
all controls related to access management"
```

### Plugin Security Scanning

```
"Before I install this plugin from GitHub, can you scan it for
security vulnerabilities? Path: /path/to/plugin"
```

---

## Troubleshooting

### Plugins Don't Appear After Installation

**Solution:** Enable plugins and restart Claude Code

```bash
/plugin  # Enable each plugin
# Then restart Claude Code completely
```

### "Local plugins cannot be updated remotely"

**Cause:** Marketplace was added using local path instead of GitHub format

**Solution:**
```bash
/plugin marketplace remove security-compliance-marketplace
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
```

### Plugin Loading Errors

**Check plugin status:**
```bash
/plugin  # View plugin details and error messages
```

**Common issues:**
- Invalid plugin.json format
- Missing required fields
- Incorrect agents field format

### Updates Not Appearing

**Solution:**
1. Wait 2-5 minutes for GitHub CDN to update
2. Run `/plugin marketplace update security-compliance-marketplace`
3. Restart Claude Code
4. Check `/plugin` for new versions

---

## Best Practices

### 1. Always Use GitHub Repository Format

✅ **Correct:**
```bash
/plugin marketplace add owner/repository
```

❌ **Wrong:**
```bash
/plugin marketplace add /local/path/to/repo
```

### 2. Enable Plugins After Installation

Plugins are disabled by default. Always:
1. Install plugin
2. Enable via `/plugin`
3. Restart Claude Code

### 3. Keep Plugins Updated

Check for updates regularly:
```bash
/plugin marketplace update security-compliance-marketplace
```

### 4. Verify Plugin Security

Before installing third-party plugins:
```bash
"Scan this plugin for security issues: /path/to/plugin"
```

---

## Next Steps

### Explore Plugin Documentation

Each plugin has detailed documentation:
- [GDPR Auditor](./gdpr-auditor/README.md)
- [Plugin Security Checker](./plugin-security-checker/README.md)
- [PDF Smart Extractor](./pdf-smart-extractor/README.md)
- [All Plugins](./README.md)

### Join the Community

- **Report Issues:** [GitHub Issues](https://github.com/diegocconsolini/ClaudeSkillCollection/issues)
- **Suggest Features:** [Discussions](https://github.com/diegocconsolini/ClaudeSkillCollection/discussions)
- **Contribute:** [CONTRIBUTING.md](./CONTRIBUTING.md)

### Stay Updated

Star the repository on GitHub to get notified of new plugins and updates:
https://github.com/diegocconsolini/ClaudeSkillCollection

---

**Ready to get started?**

```bash
/plugin marketplace add diegocconsolini/ClaudeSkillCollection
```
