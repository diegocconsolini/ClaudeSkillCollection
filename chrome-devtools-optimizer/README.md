# Chrome DevTools Optimizer

Reduce token consumption by **70-80%** when using Chrome DevTools MCP through smart snapshot strategies and optional Gemini Flash vision processing.

## The Problem

Chrome DevTools MCP screenshots consume **~1,600 tokens each** in Claude's context. For workflows involving multiple page checks, this quickly exhausts context and increases costs.

| Workflow | Without Optimizer | With Optimizer | Savings |
|----------|-------------------|----------------|---------|
| Single page check | 1,600 tokens | 500 tokens | 69% |
| Login flow (3 screens) | 4,800 tokens | 800 tokens | 83% |
| Form debugging (5 screens) | 8,000 tokens | 1,500 tokens | 81% |
| Full test session (10 ops) | 16,000 tokens | 3,000 tokens | 81% |

## How It Works

### 1. Snapshot Over Screenshot
Use text-based `take_snapshot` (accessibility tree) instead of images by default. Returns element structure, UIDs, and text content at 70% lower cost.

### 2. Gemini Flash Processing (Optional)
When visual analysis IS needed, process screenshots through Gemini Flash (~$0.001/image vs ~$0.005 direct to Claude) and return text summaries.

### 3. Smart Targeting
Capture only specific elements using UIDs. Smaller images = fewer tokens.

### 4. Batch Operations
Use `fill_form` for multiple fields instead of separate `fill` calls.

## Installation

### Prerequisites
- Chrome DevTools MCP configured in Claude Code
- Node.js 18+ (for Gemini integration)

### Install Plugin

```bash
# Clone or copy to your plugins directory
cp -r chrome-devtools-optimizer ~/.claude/plugins/
```

Or add to your Claude Code settings:

```json
{
  "plugins": [
    "path/to/chrome-devtools-optimizer"
  ]
}
```

### Setup Gemini Integration (Optional but Recommended)

```bash
# Interactive setup
node chrome-devtools-optimizer/scripts/setup.js
```

You'll need a Gemini API key:
- **Free tier:** 15 requests/min, 1M tokens/day
- **Get key:** https://aistudio.google.com/apikey

### Verify Setup

```bash
node chrome-devtools-optimizer/scripts/test-connection.js
```

## Usage

### Automatic Optimization
Once installed, the agent automatically applies optimization rules when you use Chrome DevTools MCP tools.

### Manual Screenshot Processing

```bash
# Process a screenshot file
node chrome-devtools-optimizer/scripts/process-screenshot.js screenshot.png

# Process base64 data
node chrome-devtools-optimizer/scripts/process-screenshot.js <base64_string>

# Custom analysis prompt
node chrome-devtools-optimizer/scripts/process-screenshot.js --prompt "Find all buttons" page.png

# JSON output
node chrome-devtools-optimizer/scripts/process-screenshot.js -j screenshot.png
```

## Quick Reference

### Decision Tree

| Need | Use | Tokens |
|------|-----|--------|
| Page structure/elements | `take_snapshot` | 300-1,500 |
| Visual appearance | Screenshot → Gemini | ~300 |
| Single element | `take_screenshot` with uid | 400-800 |
| Form values | `evaluate_script` | 50-100 |
| Console errors | `list_console_messages` (filtered) | 100-300 |
| Network calls | `list_network_requests` (filtered) | 200-500 |

### Anti-Patterns to Avoid

| Bad | Good |
|-----|------|
| Screenshot after every action | Snapshot or verify only when needed |
| Multiple `fill()` calls | Single `fill_form()` |
| Unfiltered console/network | Always filter and limit |
| Full page screenshot for one element | Use `uid` parameter |

## Documentation

- **Agent Rules:** `agents/chrome-devtools-optimizer.md`
- **Tool Reference:** `references/tool-reference.md`
- **Token Costs:** `references/token-costs.md`
- **Decision Tree:** `references/decision-tree.md`
- **Patterns:**
  - `patterns/navigation.md` - Navigate and verify patterns
  - `patterns/forms.md` - Form filling and validation
  - `patterns/debugging.md` - Console and network debugging
  - `patterns/visual-check.md` - When you need screenshots

## Examples

### Login Flow (Optimized)

```
1. navigate_page to login URL
2. take_snapshot → get form element UIDs
3. fill_form with all credentials at once
4. click submit button by uid
5. evaluate_script to check URL (verify redirect)
6. take_snapshot → confirm dashboard loaded
```

**Total: ~1,000 tokens** (vs ~6,000 with screenshots)

### Debug Console Error

```
1. list_console_messages({ types: ["error"], pageSize: 5 })
2. If error found, take_snapshot to see page state
3. evaluate_script to check specific element/variable
```

**Total: ~500 tokens** (vs ~3,000 with screenshots)

### Visual Verification (When Needed)

```
1. take_screenshot({ format: "jpeg", quality: 50 })
2. node scripts/process-screenshot.js screenshot.jpg
3. Gemini returns: "Page shows login form with email/password fields..."
```

**Total: ~300 tokens** (vs ~1,600 direct)

## Cost Comparison

### Per Session (50 operations)

| Approach | Tokens | Cost |
|----------|--------|------|
| Unoptimized | 80,000 | ~$1.20 |
| Snapshot-first | 25,000 | ~$0.38 |
| Full optimization | 15,000 | ~$0.28 |

### Monthly (10 sessions/day)

| Approach | Tokens | Cost |
|----------|--------|------|
| Unoptimized | 24M | ~$360 |
| Full optimization | 4.5M | ~$84 |

**Annual savings: ~$3,300**

## Troubleshooting

### "Config not found" Error

```bash
node chrome-devtools-optimizer/scripts/setup.js
```

### "API Error" from Gemini

1. Check API key is valid: https://aistudio.google.com/apikey
2. Check quota not exceeded (free tier: 15 RPM)
3. Run connection test: `node scripts/test-connection.js`

### Screenshots Still Large

Ensure you're using compression:
```json
{ "format": "jpeg", "quality": 50 }
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request

## License

MIT

## Credits

- Chrome DevTools MCP: https://github.com/anthropics/anthropic-tools
- Gemini API: https://ai.google.dev/
