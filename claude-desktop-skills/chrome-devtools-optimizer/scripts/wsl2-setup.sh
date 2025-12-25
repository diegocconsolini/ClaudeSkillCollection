#!/bin/bash
# Chrome DevTools MCP Setup for WSL2
# Installs Chrome, adds bash alias, and configures MCP server

set -e

echo "🔧 Chrome DevTools MCP Setup for WSL2"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running in WSL
if ! grep -qi microsoft /proc/version 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Warning: This script is designed for WSL2. Continuing anyway...${NC}"
fi

# Step 1: Check/Install Chrome
echo "📦 Step 1: Checking Google Chrome..."
if command -v google-chrome &> /dev/null; then
    echo -e "${GREEN}✓ Chrome already installed${NC}"
else
    echo "Installing Google Chrome..."
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    sudo apt update
    sudo apt install -y google-chrome-stable
    echo -e "${GREEN}✓ Chrome installed${NC}"
fi

# Step 2: Add bash alias
echo ""
echo "📝 Step 2: Checking bash alias..."
if grep -q "chrome-debug" ~/.bashrc 2>/dev/null; then
    echo -e "${GREEN}✓ Alias already exists${NC}"
else
    echo "Adding chrome-debug alias to ~/.bashrc..."
    cat >> ~/.bashrc << 'EOF'

# Chrome DevTools MCP - launch Chrome with remote debugging
alias chrome-debug='mkdir -p /tmp/chrome-debug-profile && google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug-profile --no-sandbox > /tmp/chrome.log 2>&1 &'
EOF
    echo -e "${GREEN}✓ Alias added${NC}"
fi

# Step 3: Configure MCP Server
echo ""
echo "⚙️  Step 3: Checking MCP configuration..."
CLAUDE_SETTINGS="$HOME/.claude/settings.json"

if [ ! -f "$CLAUDE_SETTINGS" ]; then
    echo -e "${YELLOW}Creating Claude settings file...${NC}"
    mkdir -p "$HOME/.claude"
    echo '{"mcpServers":{}}' > "$CLAUDE_SETTINGS"
fi

if jq -e '.mcpServers["chrome-devtools"]' "$CLAUDE_SETTINGS" >/dev/null 2>&1; then
    echo -e "${GREEN}✓ MCP server already configured${NC}"
else
    echo "Adding chrome-devtools MCP server..."
    if command -v jq &> /dev/null; then
        jq '.mcpServers["chrome-devtools"] = {
            "command": "npx",
            "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://localhost:9222"],
            "env": {}
        }' "$CLAUDE_SETTINGS" > /tmp/claude-settings.tmp && mv /tmp/claude-settings.tmp "$CLAUDE_SETTINGS"
        echo -e "${GREEN}✓ MCP server configured${NC}"
        echo -e "${YELLOW}⚠️  Restart Claude Code to apply MCP changes${NC}"
    else
        echo -e "${RED}✗ jq not installed. Install with: sudo apt install jq${NC}"
        echo "Then manually add to $CLAUDE_SETTINGS:"
        echo '  "chrome-devtools": {'
        echo '    "command": "npx",'
        echo '    "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://localhost:9222"],'
        echo '    "env": {}'
        echo '  }'
    fi
fi

# Step 4: Check Gemini API Setup
echo ""
echo "🔑 Step 4: Checking Gemini API configuration..."
GEMINI_CONFIG="$HOME/.config/chrome-devtools-optimizer/config.json"

if [ -f "$GEMINI_CONFIG" ] && jq -e '.geminiApiKey' "$GEMINI_CONFIG" >/dev/null 2>&1; then
    MASKED_KEY=$(jq -r '.geminiApiKey' "$GEMINI_CONFIG" | sed 's/\(.\{8\}\).*\(.\{4\}\)$/\1...\2/')
    echo -e "${GREEN}✓ Gemini API configured: $MASKED_KEY${NC}"
else
    echo -e "${YELLOW}⚠️  Gemini API not configured${NC}"
    echo ""
    echo "Gemini Flash provides 80% token savings on visual analysis."
    echo "Free tier: 15 requests/min, 1M tokens/day"
    echo "Get your API key at: https://aistudio.google.com/apikey"
    echo ""
    read -p "Do you want to configure Gemini now? (Y/n): " SETUP_GEMINI
    if [ "$SETUP_GEMINI" != "n" ] && [ "$SETUP_GEMINI" != "N" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        node "$SCRIPT_DIR/setup.js"
    else
        echo -e "${YELLOW}Skipped. Run later: node scripts/setup.js${NC}"
    fi
fi

# Summary
echo ""
echo "======================================"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Usage:"
echo "  1. Start Chrome:  chrome-debug"
echo "  2. Open new terminal or run: source ~/.bashrc"
echo "  3. In Claude Code, use: list_pages, take_snapshot, click, fill, etc."
echo ""
echo "Gemini Integration (for visual analysis):"
echo "  - Test: node scripts/test-connection.js"
echo "  - Setup: node scripts/setup.js"
echo ""
echo "Troubleshooting:"
echo "  - Check Chrome logs: cat /tmp/chrome.log"
echo "  - Verify Chrome running: ps aux | grep chrome"
echo "  - Test connection: curl http://localhost:9222/json"
echo ""
