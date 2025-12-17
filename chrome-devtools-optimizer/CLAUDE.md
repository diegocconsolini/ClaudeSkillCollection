# Chrome DevTools Optimizer

## WSL2 Quick Setup

```bash
# Check Chrome → install if missing
which google-chrome || (wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && sudo apt update && sudo apt install -y google-chrome-stable)

# Check alias → add if missing
grep -q "chrome-debug" ~/.bashrc || echo "alias chrome-debug='mkdir -p /tmp/chrome-debug-profile && google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug-profile --no-sandbox > /tmp/chrome.log 2>&1 &'" >> ~/.bashrc && source ~/.bashrc

# Check MCP config → add if missing (restart Claude Code after)
jq -e '.mcpServers["chrome-devtools"]' ~/.claude/settings.json >/dev/null 2>&1 || (jq '.mcpServers["chrome-devtools"] = {"command":"npx","args":["-y","chrome-devtools-mcp@latest","--browserUrl","http://localhost:9222"],"env":{}}' ~/.claude/settings.json > /tmp/s.tmp && mv /tmp/s.tmp ~/.claude/settings.json && echo "Restart Claude Code")
```

## Usage

1. Start Chrome: `chrome-debug`
2. Use optimized MCP tools (see decision tree below)

## Token Optimization Decision Tree

| Need | Use | Tokens |
|------|-----|--------|
| Page structure/elements | `take_snapshot` | 300-1,500 |
| Visual appearance | `take_screenshot` → Gemini | ~300 |
| Single element visual | `take_screenshot` with `uid` | 400-800 |
| Form values/state | `evaluate_script` | 50-100 |
| Console errors | `list_console_messages` (filtered) | 100-300 |
| Network calls | `list_network_requests` (filtered) | 200-500 |

## Anti-Patterns (Avoid)

- Screenshot after every action → Use snapshot or verify only when needed
- Multiple `fill()` calls → Use single `fill_form()`
- Unfiltered console/network → Always use `types`/`resourceTypes` + `pageSize`
- Full page screenshot for one element → Use `uid` parameter

## Example: Optimized Login Flow

```
1. navigate_page → login URL
2. take_snapshot → get form UIDs
3. fill_form → all credentials at once
4. click → submit button by uid
5. evaluate_script → check URL (verify redirect)
6. take_snapshot → confirm dashboard
```

**~1,000 tokens** (vs ~6,000 with screenshots)

## Troubleshooting

```bash
# Chrome logs
cat /tmp/chrome.log

# Verify Chrome running
ps aux | grep chrome

# Test connection
curl http://localhost:9222/json
```
