---
name: chrome-devtools-optimizer
description: Reduce token consumption by 70-80% when using Chrome DevTools MCP through smart snapshot strategies and optional Gemini Flash vision processing
trigger: When using Chrome DevTools MCP for web testing, screenshots, page inspection, or form automation
tools: [Bash, Read, Write]
---

# Chrome DevTools Optimizer

You are an expert at efficiently using Chrome DevTools MCP while minimizing token consumption. Apply these optimization strategies automatically.

## Core Principle

**Default to text over images.** Screenshots cost 1,600+ tokens. Text snapshots cost 300-500 tokens.

## Decision Tree

When the user needs page information:

1. **Need page structure/elements?** → Use `take_snapshot` (text, ~500 tokens)
2. **Need visual appearance?** → Screenshot → Gemini Flash → text summary (~300 tokens)
3. **Need specific element only?** → Use `take_screenshot` with `uid` parameter (smaller image)
4. **Need complex visual reasoning?** → Direct screenshot to Claude (last resort, ~1,600 tokens)

## Optimization Rules

### Rule 1: Snapshot First
ALWAYS try `take_snapshot` before `take_screenshot`. The accessibility tree provides:
- All interactive elements with unique IDs
- Text content
- Element hierarchy
- Form field states

```
GOOD: take_snapshot → analyze structure → targeted action
BAD:  take_screenshot → analyze image → action
```

### Rule 2: Gemini Flash for Visual Analysis
When visual analysis IS needed, use the processor script:

```bash
node chrome-devtools-optimizer/scripts/process-screenshot.js <base64_image_or_file>
```

This returns a text summary (~200-500 tokens) instead of embedding the image (~1,600 tokens).

### Rule 3: Element-Targeted Screenshots
If you must screenshot, capture only what's needed:

```
GOOD: take_screenshot with uid="element-id" (element only)
BAD:  take_screenshot full page then describe one button
```

### Rule 4: Compress Full-Page Shots
When full-page screenshot is unavoidable:

```json
{
  "format": "jpeg",
  "quality": 50
}
```

This reduces image size by 30-40%.

### Rule 5: Don't Re-Snapshot Unchanged Pages
If the page hasn't changed since last snapshot, reference the previous one:

```
"Based on the previous snapshot, the login form has fields for..."
```

### Rule 6: Filter Network/Console Output
Use filters to reduce output size:

```json
// Network - filter by type
{ "resourceTypes": ["Document", "XHR", "Fetch"] }

// Console - filter by type
{ "types": ["error", "warning"] }

// Both - use pagination
{ "pageSize": 20 }
```

### Rule 7: Batch Form Operations
Use `fill_form` instead of multiple `fill` calls:

```
GOOD: fill_form with all fields at once
BAD:  fill("email", "...") → fill("password", "...") → fill("name", "...")
```

## Token Cost Reference

| Operation | Tokens | When to Use |
|-----------|--------|-------------|
| `take_snapshot` | 300-1,500 | Structure, elements, text content |
| Screenshot → Gemini | 200-500 | Visual appearance, layout, colors |
| Element screenshot | 400-800 | Single component analysis |
| Full screenshot (JPEG 50%) | 800-1,200 | Complex visual debugging |
| Full screenshot (PNG) | 1,600-4,000 | Last resort, precise pixels needed |

## Setup Check

Before using Gemini integration, verify setup:

```bash
node chrome-devtools-optimizer/scripts/test-connection.js
```

If not configured, run interactive setup:

```bash
node chrome-devtools-optimizer/scripts/setup.js
```

## Example Workflows

### Verify Login Page (Optimized)
```
1. navigate_page to login URL
2. take_snapshot → confirm form elements present
3. fill_form with credentials
4. click submit button by uid
5. take_snapshot → confirm success/error state
```
Total: ~1,500 tokens (vs ~6,400 with screenshots)

### Debug Visual Layout Issue
```
1. take_snapshot → identify element uid
2. take_screenshot with uid → Gemini Flash
3. Gemini returns: "Button is misaligned, positioned 20px left of container"
4. Fix CSS based on text description
```
Total: ~800 tokens (vs ~3,200 with full screenshots)

### Check Responsive Design
```
1. resize_page to mobile dimensions
2. take_snapshot → verify elements reflow
3. Only if visual issues: screenshot → Gemini for layout analysis
```
Total: ~600-1,000 tokens (vs ~3,200 minimum with screenshots)

## References

- Read `references/tool-reference.md` for all 26 Chrome DevTools MCP tools
- Read `references/token-costs.md` for detailed cost analysis
- Read `references/decision-tree.md` for flowchart decision logic
- Read `patterns/*.md` for specific workflow patterns
