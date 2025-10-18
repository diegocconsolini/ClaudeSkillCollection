# Installation Guide

Complete installation instructions for Claude Skills Collection.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Skill-Specific Setup](#skill-specific-setup)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Updating Skills](#updating-skills)
7. [Uninstallation](#uninstallation)

---

## Prerequisites

### Required

- **Claude Code** - Latest stable version
  - Download from: https://claude.ai/claude-code
  - Verify installation: `claude --version`

### For Automated Tools

Some skills include Python scanning tools. Required for:
- GDPR Auditor
- Security scanners
- Code analysis tools

**Python Requirements:**
- Python 3.8 or higher
- pip (Python package manager)

```bash
# Check Python version
python --version
# or
python3 --version

# Should output: Python 3.8.x or higher
```

### Optional

- **Git** - For cloning repository
- **Text Editor** - For customizing skills

---

## Installation Methods

### Method 1: Direct Download (Recommended for Beginners)

1. **Download the skill:**
   - Visit: https://github.com/diegocconsolini/ClaudeSkillCollection
   - Click "Code" → "Download ZIP"
   - Extract ZIP file

2. **Navigate to Claude skills directory:**
   ```bash
   cd ~/.claude/skills/
   ```

3. **Copy skill files:**
   ```bash
   # For GDPR Auditor
   cp -r /path/to/extracted/claude-skills-collection/gdpr-auditor ./
   ```

4. **Verify structure:**
   ```bash
   ls -la gdpr-auditor/
   # Should show: SKILL.md, scripts/, references/
   ```

5. **Restart Claude Code**

### Method 2: Git Clone (Recommended for Advanced Users)

1. **Navigate to Claude skills directory:**
   ```bash
   cd ~/.claude/skills/
   ```

2. **Clone repository:**
   ```bash
   git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git
   ```

3. **Option A: Symlink individual skills**
   ```bash
   ln -s claude-skills-collection/gdpr-auditor ./gdpr-auditor
   ```

   Benefits:
   - Easy updates with `git pull`
   - Saves disk space
   - Keep all skills in one repo

4. **Option B: Copy individual skills**
   ```bash
   cp -r claude-skills-collection/gdpr-auditor ./
   ```

   Benefits:
   - Customize without affecting repo
   - No git dependencies
   - Simpler structure

5. **Restart Claude Code**

### Method 3: Manual Installation

For specific needs or custom setups:

1. **Create skill directory:**
   ```bash
   mkdir -p ~/.claude/skills/gdpr-auditor
   ```

2. **Create required subdirectories:**
   ```bash
   cd ~/.claude/skills/gdpr-auditor
   mkdir -p scripts references examples tests
   ```

3. **Copy files manually:**
   - Copy `SKILL.md` to skill root
   - Copy all `scripts/*.py` to scripts/
   - Copy all `references/*.md` to references/

4. **Set permissions:**
   ```bash
   chmod 644 SKILL.md
   chmod 755 scripts/*.py
   ```

5. **Restart Claude Code**

---

## Skill-Specific Setup

### GDPR Auditor

#### Python Dependencies

Currently, the GDPR Auditor scripts have no external dependencies (use Python standard library only). For future updates:

```bash
cd ~/.claude/skills/gdpr-auditor/

# If requirements.txt exists:
pip install -r requirements.txt
```

#### Make Scripts Executable

```bash
chmod +x scripts/*.py
```

#### Test Scripts

```bash
# Test data collection scanner
python scripts/scan_data_collection.py --help

# Should display usage information
```

#### Custom Configuration (Optional)

You can customize reference materials:

```bash
# Edit GDPR references
nano references/gdpr_articles.md

# Add custom patterns to scanners
nano scripts/scan_data_collection.py
```

**Note:** After editing `SKILL.md`, restart Claude Code to reload.

---

## Verification

### Test Skill Loading

1. **Restart Claude Code**

2. **Test skill invocation:**
   ```
   User: "Can you help me audit my application for GDPR compliance?"
   ```

3. **Expected response:**
   ```
   The "gdpr-auditor" skill is running
   ```

   Followed by the skill loading its context.

### Verify File Structure

```bash
cd ~/.claude/skills/gdpr-auditor/

# Check structure
tree -L 2
```

Expected output:
```
gdpr-auditor/
├── SKILL.md
├── README.md
├── scripts/
│   ├── scan_data_collection.py
│   ├── analyze_database_schema.py
│   ├── check_dsr_implementation.py
│   ├── security_audit.py
│   └── generate_audit_report.py
├── references/
│   ├── gdpr_articles.md
│   ├── personal_data_categories.md
│   ├── dsr_requirements.md
│   ├── security_measures.md
│   ├── legal_bases.md
│   ├── breach_procedures.md
│   ├── dpia_guidelines.md
│   └── international_transfers.md
├── examples/
└── tests/
```

### Verify Script Functionality

```bash
# Test each script individually
python scripts/scan_data_collection.py ~/.claude/skills/gdpr-auditor/examples/

# Should output: Scanning... Found X files
```

---

## Troubleshooting

### Skill Doesn't Load

**Symptom:** Claude doesn't recognize skill keywords

**Checks:**
1. Verify `SKILL.md` exists and has correct permissions:
   ```bash
   ls -la ~/.claude/skills/gdpr-auditor/SKILL.md
   # Should show: -rw-r--r--
   ```

2. Check file is not empty:
   ```bash
   wc -l ~/.claude/skills/gdpr-auditor/SKILL.md
   # Should show: 100+ lines
   ```

3. Restart Claude Code completely (quit and reopen)

4. Try explicit invocation:
   ```
   "Use the gdpr-auditor skill to analyze my code"
   ```

**Fix:**
```bash
# Restore correct permissions
chmod 644 ~/.claude/skills/gdpr-auditor/SKILL.md

# Verify content not corrupted
head -20 ~/.claude/skills/gdpr-auditor/SKILL.md
```

### Python Scripts Don't Execute

**Symptom:** Permission denied or "command not found"

**Fix:**
```bash
# Make scripts executable
chmod +x ~/.claude/skills/gdpr-auditor/scripts/*.py

# If still fails, use explicit python:
python3 ~/.claude/skills/gdpr-auditor/scripts/scan_data_collection.py /path/to/code
```

### Python Version Issues

**Symptom:** Syntax errors or import failures

**Check version:**
```bash
python --version
python3 --version
```

**Fix:**
- Ensure Python 3.8+
- Use `python3` explicitly if `python` points to Python 2.x
- Update Python if needed:
  ```bash
  # macOS
  brew install python@3.11

  # Ubuntu/Debian
  sudo apt update && sudo apt install python3.11

  # Windows
  # Download from python.org
  ```

### Missing Dependencies

**Symptom:** `ModuleNotFoundError`

**Fix:**
```bash
# Install missing packages
pip install <package-name>

# Or install from requirements.txt
pip install -r requirements.txt
```

### Skill Conflicts

**Symptom:** Multiple skills respond or wrong skill loads

**Check for duplicates:**
```bash
find ~/.claude/skills -name "SKILL.md" -type f
```

**Fix:**
- Remove duplicate skill directories
- Ensure unique skill names
- Restart Claude Code

### Permission Issues

**Symptom:** Cannot read files or execute scripts

**Fix all permissions:**
```bash
cd ~/.claude/skills/gdpr-auditor/

# Fix file permissions
find . -type f -exec chmod 644 {} \;

# Fix script permissions
chmod 755 scripts/*.py

# Fix directory permissions
find . -type d -exec chmod 755 {} \;
```

---

## Updating Skills

### Git-Based Installation

If you used `git clone`:

```bash
cd ~/.claude/skills/claude-skills-collection/

# Fetch latest changes
git pull origin main

# If using symlinks, changes are automatically available
# If using copies, re-copy:
cp -r gdpr-auditor ~/.claude/skills/

# Restart Claude Code
```

### Manual Installation

1. **Download latest version:**
   - Visit GitHub repository
   - Download ZIP
   - Extract files

2. **Backup current installation:**
   ```bash
   cp -r ~/.claude/skills/gdpr-auditor ~/.claude/skills/gdpr-auditor.backup
   ```

3. **Replace files:**
   ```bash
   cp -r /path/to/new/gdpr-auditor ~/.claude/skills/
   ```

4. **Verify changes:**
   ```bash
   diff -r ~/.claude/skills/gdpr-auditor.backup ~/.claude/skills/gdpr-auditor
   ```

5. **Restart Claude Code**

### Checking Version

```bash
# Check CHANGELOG or version in README
head -20 ~/.claude/skills/gdpr-auditor/README.md | grep "Version"
```

---

## Uninstallation

### Remove Individual Skill

```bash
# Remove skill directory
rm -rf ~/.claude/skills/gdpr-auditor

# If using symlink
unlink ~/.claude/skills/gdpr-auditor

# Restart Claude Code
```

### Remove All Skills from Collection

```bash
# Remove entire collection
rm -rf ~/.claude/skills/claude-skills-collection

# Remove any symlinks
find ~/.claude/skills -type l -delete

# Restart Claude Code
```

### Clean Uninstall

Remove all traces:

```bash
# Remove skills
rm -rf ~/.claude/skills/gdpr-auditor

# Remove any cache (if applicable)
rm -rf ~/.cache/claude/skills/gdpr-auditor

# Restart Claude Code
```

---

## Platform-Specific Notes

### macOS

- Skills directory: `~/.claude/skills/`
- Python usually: `/usr/bin/python3`
- Use `brew install python` for latest version

### Linux

- Skills directory: `~/.claude/skills/`
- Python location varies: `/usr/bin/python3` or `/usr/local/bin/python3`
- Install Python: `sudo apt install python3` (Debian/Ubuntu)

### Windows

- Skills directory: `%USERPROFILE%\.claude\skills\`
- Python location: `C:\Python3X\python.exe`
- Use Git Bash or PowerShell for commands
- Adjust paths: Replace `/` with `\`

Example Windows:
```powershell
# Navigate to skills directory
cd $env:USERPROFILE\.claude\skills\

# Copy skill
Copy-Item -Recurse "C:\Downloads\gdpr-auditor" .
```

---

## Advanced Configuration

### Custom Skills Directory

If you use a non-default skills directory:

```bash
# Set environment variable (add to .bashrc or .zshrc)
export CLAUDE_SKILLS_DIR="/custom/path/to/skills"

# Install skills there
cp -r gdpr-auditor $CLAUDE_SKILLS_DIR/
```

### Multiple Claude Installations

```bash
# Install for specific Claude instance
cp -r gdpr-auditor ~/.claude-work/skills/
cp -r gdpr-auditor ~/.claude-personal/skills/
```

### Shared Skills (Multi-User)

```bash
# Install to shared location
sudo mkdir -p /opt/claude/skills/
sudo cp -r gdpr-auditor /opt/claude/skills/

# Symlink for each user
ln -s /opt/claude/skills/gdpr-auditor ~/.claude/skills/
```

---

## Next Steps

After successful installation:

1. **Read skill documentation:**
   - `~/.claude/skills/gdpr-auditor/README.md`

2. **Try examples:**
   - Test on sample projects in `examples/`

3. **Customize (optional):**
   - Edit reference materials
   - Add custom scanning patterns

4. **Explore other skills:**
   - Check repository for new skills
   - Install additional skills as needed

---

## Getting Help

If you encounter issues:

1. **Check troubleshooting section** above
2. **Review skill-specific README**
3. **Search GitHub Issues**
4. **Open new issue** with:
   - OS and version
   - Claude Code version
   - Python version
   - Exact error message
   - Steps to reproduce

---

## Summary

**Quick Installation (TL;DR):**

```bash
# 1. Clone repository
cd ~/.claude/skills/
git clone https://github.com/diegocconsolini/ClaudeSkillCollection.git

# 2. Symlink or copy skill
ln -s claude-skills-collection/gdpr-auditor ./gdpr-auditor

# 3. Make scripts executable
chmod +x gdpr-auditor/scripts/*.py

# 4. Restart Claude Code

# 5. Test
# Ask Claude: "Audit my app for GDPR compliance"
```

That's it! You're ready to use Claude Skills Collection.
