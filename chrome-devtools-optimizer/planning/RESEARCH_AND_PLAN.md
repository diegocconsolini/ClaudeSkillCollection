# Chrome DevTools Optimizer Skill - Research & Plan

> Created: 2025-12-14
> Status: Planning Phase
> Branch: feature/chrome-devtools-optimizer

---

## Problem Statement

Screenshots from Chrome DevTools MCP consume ~1,600 tokens each in Claude's context. For workflows involving multiple page checks, this quickly exhausts context and increases costs.

**Goal:** Reduce token consumption by 70-80% while maintaining functionality.

---

## Research Findings

### Chrome DevTools MCP Tools (v0.12.1)

**26 tools in 6 categories:**

| Category | Tools | Token Impact |
|----------|-------|--------------|
| **Debugging** | take_screenshot, take_snapshot, evaluate_script, console messages | HIGH |
| **Input** | click, fill, fill_form, hover, press_key, drag | Low |
| **Navigation** | navigate_page, list_pages, select_page, new_page, close_page | Low |
| **Network** | list_network_requests, get_network_request | Medium |
| **Performance** | trace tools | Medium-High |
| **Emulation** | emulate, resize_page | Low |

### Token Cost Analysis

| Tool | Output Type | Est. Tokens | Notes |
|------|-------------|-------------|-------|
| `take_screenshot` | Base64 image | 1,500-4,000 | **Biggest consumer** |
| `take_snapshot` | Text (a11y tree) | 300-1,500 | Depends on page complexity |
| `list_network_requests` | JSON list | 200-2,000 | Grows with requests |
| `list_console_messages` | Text | 100-1,000 | Grows with logs |
| `evaluate_script` | JSON result | 50-500 | Depends on return value |
| Navigation/Input tools | Confirmation | 20-50 | Minimal |

### Vision API Cost Comparison (per image)

| Service | Tokens/Image | Cost | Speed | Accuracy |
|---------|--------------|------|-------|----------|
| **Gemini 2.5 Flash** | 560 | ~$0.001 | Very fast | 95%+ OCR |
| **Claude (direct)** | 1,600 | ~$0.005 | Fast | Excellent |
| **GPT-4o mini** | 2,833 | ~$0.004 | Fast | Good |
| **GPT-4o** | 85-700 | ~$0.005 | Fast | Excellent |

**Winner: Gemini Flash** - 25x cheaper than Claude vision, excellent for OCR/screenshots.

### Sources

- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Claude Vision Docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- [Chrome DevTools MCP GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Gemini Flash Image API Guide](https://blog.laozhang.ai/api-guides/gemini-flash-image-api/)

---

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌──────────────────┐               │
│  │   Chrome    │───▶│  take_snapshot   │──▶ Text       │
│  │  DevTools   │    │  (default)       │   (300-1500t) │
│  │    MCP      │    └──────────────────┘               │
│  │             │                                        │
│  │             │    ┌──────────────────┐               │
│  │             │───▶│ take_screenshot  │               │
│  └─────────────┘    │  (when needed)   │               │
│                     └────────┬─────────┘               │
│                              │                          │
│                              ▼                          │
│                     ┌──────────────────┐               │
│                     │  Gemini Flash    │               │
│                     │  Vision Script   │               │
│                     │  (~$0.001/img)   │               │
│                     └────────┬─────────┘               │
│                              │                          │
│                              ▼                          │
│                     ┌──────────────────┐               │
│                     │  Text Summary    │──▶ ~200-500t  │
│                     │  (returned)      │               │
│                     └──────────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Decision Flow

```
WHEN user needs page info:
├── Structure/elements needed?
│   └── YES → take_snapshot (text, ~500 tokens)
├── Visual appearance needed?
│   └── YES → screenshot → Gemini Flash → text summary (~300 tokens)
├── Specific element only?
│   └── YES → element screenshot with uid (smaller image)
└── Complex visual reasoning needed?
    └── YES → direct Claude vision (rare, last resort)
```

---

## Optimization Strategies

### 1. Snapshot Over Screenshot (Primary)
- Default to `take_snapshot` for page structure
- Returns accessibility tree as text
- 70% token reduction vs screenshot

### 2. Gemini Flash Processing (Secondary)
- When visual analysis needed, use Gemini Flash
- Process screenshot externally, return text summary
- 80% token reduction + lower cost

### 3. Element-Targeted Screenshots
- Use `uid` parameter to capture only specific elements
- Smaller image = fewer tokens
- 50-70% reduction for focused captures

### 4. Compressed Screenshots
- Use `format: "jpeg"`, `quality: 50` for full-page
- Reduces image size significantly
- 30-40% reduction

### 5. Conditional Re-Snapshot
- Don't re-snapshot if page unchanged
- Reference previous snapshot in conversation
- 100% reduction for repeated checks

### 6. Filtered Network/Console
- Use type filters (`resourceTypes`, `types` params)
- Use `pageSize` for pagination
- 50-80% reduction for large lists

### 7. Batch Operations
- Use `fill_form` instead of multiple `fill` calls
- Single operation vs multiple round-trips

---

## Token Savings Estimate

| Scenario | Without Skill | With Skill | Savings |
|----------|---------------|------------|---------|
| Single page check | 1,600 tokens | 500 tokens | 69% |
| Form debugging (3 screens) | 4,800 tokens | 800 tokens | 83% |
| Visual verification | 1,600 tokens | 300 tokens | 81% |
| Full workflow (10 ops) | 16,000 tokens | 3,000 tokens | 81% |

---

## Skill Structure (Proposed)

```
chrome-devtools-optimizer/
├── .claude-plugin/
│   └── plugin.json                    # Plugin manifest
├── agents/
│   └── chrome-devtools-optimizer.md   # Main agent with rules
├── scripts/
│   ├── process-screenshot.js          # Gemini Flash processor
│   ├── setup-gemini.sh               # API key setup helper
│   └── test-connection.js            # Verify setup
├── references/
│   ├── tool-reference.md             # All 26 tools documented
│   ├── token-costs.md                # Token cost estimates
│   └── decision-tree.md              # When to use what
├── patterns/
│   ├── navigation.md                 # Navigate + verify patterns
│   ├── forms.md                      # Efficient form filling
│   ├── debugging.md                  # Console/network patterns
│   └── visual-check.md               # Screenshot optimization
├── README.md                         # User documentation
├── SKILL.md                          # Quick reference
└── CHANGELOG.md                      # Version history
```

---

## Requirements

### For Basic Optimization
- Chrome DevTools MCP configured
- Skill installed in Claude Code

### For Gemini Integration (Optional but Recommended)
- Gemini API Key (free tier: 15 RPM, 1M tokens/day)
- Node.js 18+
- `@google/generative-ai` npm package

---

## Open Questions

### 1. Gemini Integration Approach
- **A) Standalone script** - Called via Bash tool, simple
- **B) MCP server wrapper** - More integrated, complex
- **C) Instructions only** - Manual, no automation

### 2. Skill Scope
- **A) Full automation** - Script handles everything
- **B) Guided workflow** - Skill teaches patterns, user decides
- **C) Hybrid** - Automation + education

### 3. Repository Location
- **A) ClaudeSkillCollection** - Part of existing marketplace
- **B) ChromeDevToolsMCPSetup** - Extend existing repo
- **C) New standalone repo**

### 4. Gemini API Key Management
- **A) Environment variable** - User sets GEMINI_API_KEY
- **B) Config file** - Store in ~/.config/
- **C) Prompt on first use** - Interactive setup

---

## Next Steps

1. [ ] Decide on open questions above
2. [ ] Create Gemini Flash processor script prototype
3. [ ] Test token savings in real scenarios
4. [ ] Write agent instructions
5. [ ] Create reference documentation
6. [ ] Test with various websites
7. [ ] Package as skill
8. [ ] Update marketplace.json

---

## References

- [Chrome DevTools MCP npm](https://www.npmjs.com/package/chrome-devtools-mcp)
- [Chrome DevTools MCP GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Chrome Developers Blog](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
- [Gemini Vision Node.js Example](https://github.com/elfvingralf/gemini-vision-node-example)
- [Claude Vision Documentation](https://platform.claude.com/docs/en/build-with-claude/vision)
