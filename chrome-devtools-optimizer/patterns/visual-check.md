# Visual Check Patterns

Efficient patterns for visual verification and UI testing.

## When to Use Visual Checks

Visual checks (screenshots) should be **last resort**. Use them only when:
- Layout/positioning issues suspected
- Color/styling verification needed
- Visual regression testing
- Screenshot evidence required

## Basic Visual Check

### With Gemini Flash (Recommended)

```bash
# 1. Take screenshot
take_screenshot({ format: "jpeg", quality: 70 })

# 2. Process with Gemini
node chrome-devtools-optimizer/scripts/process-screenshot.js screenshot.jpg
```

**Returns text description:** ~300 tokens
**Direct to Claude:** ~1,600 tokens
**Savings:** 81%

### Element-Only Screenshot

```
# 1. Get element UID from snapshot
take_snapshot()

# 2. Screenshot just that element
take_screenshot({ uid: "target-element-uid" })

# 3. Process if needed
node scripts/process-screenshot.js element.png
```

**Cost:** ~400-600 tokens (vs full page ~1,600)

## Layout Verification

### Check Alignment (Optimized)

```javascript
// Get element positions programmatically
evaluate_script({
  expression: `
    const elements = ['header', 'sidebar', 'main', 'footer']
      .map(id => document.getElementById(id))
      .filter(Boolean)
      .map(el => ({
        id: el.id,
        rect: el.getBoundingClientRect(),
        computed: {
          display: getComputedStyle(el).display,
          position: getComputedStyle(el).position
        }
      }));
    JSON.stringify(elements, null, 2)
  `
})
```

**Cost:** ~200 tokens

### Check Responsiveness

```
// 1. Resize to mobile
resize_page({ width: 375, height: 667 })

// 2. Check layout with snapshot (not screenshot)
take_snapshot()

// 3. Only screenshot if issues found
// take_screenshot() → Gemini if needed
```

### Detect Overflow

```javascript
evaluate_script({
  expression: `
    Array.from(document.querySelectorAll('*'))
      .filter(el => el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight)
      .slice(0, 10)
      .map(el => ({
        selector: el.id || el.className || el.tagName,
        overflow: {
          horizontal: el.scrollWidth - el.clientWidth,
          vertical: el.scrollHeight - el.clientHeight
        }
      }))
  `
})
```

## Color/Style Verification

### Check Specific Colors

```javascript
evaluate_script({
  expression: `
    const el = document.querySelector('.error-message');
    el ? {
      color: getComputedStyle(el).color,
      backgroundColor: getComputedStyle(el).backgroundColor,
      fontSize: getComputedStyle(el).fontSize
    } : null
  `
})
```

**Cost:** ~50 tokens

### Compare to Expected Styles

```javascript
evaluate_script({
  expression: `
    const expected = { color: 'rgb(255, 0, 0)', fontSize: '14px' };
    const el = document.querySelector('.warning');
    const actual = getComputedStyle(el);
    {
      colorMatch: actual.color === expected.color,
      fontMatch: actual.fontSize === expected.fontSize,
      actual: { color: actual.color, fontSize: actual.fontSize }
    }
  `
})
```

## Visual Regression

### Quick Comparison (Without Screenshots)

```javascript
// Hash the visible content for comparison
evaluate_script({
  expression: `
    // Simple content hash for regression
    const content = document.body.innerText.trim();
    const hash = content.split('').reduce((a, b) => {
      a = ((a << 5) - a) + b.charCodeAt(0);
      return a & a;
    }, 0);
    { hash, length: content.length }
  `
})
```

### Structure Comparison

```
// Compare snapshots between versions
// Snapshot 1: Before change
take_snapshot()  // Save output

// Snapshot 2: After change
take_snapshot()  // Compare UIDs and structure
```

### When Screenshot Needed

```bash
# Only when visual diff is essential
take_screenshot({ format: "jpeg", quality: 50 })

# Use Gemini with comparison prompt
node scripts/process-screenshot.js --prompt "Compare to baseline: [describe expected state]. List any differences." screenshot.jpg
```

## Custom Gemini Prompts

### For Layout Issues

```bash
node scripts/process-screenshot.js --prompt "
Analyze this layout for issues:
1. Element alignment (centered, left/right aligned as expected?)
2. Spacing consistency (margins, padding uniform?)
3. Overflow or clipping issues
4. Mobile responsiveness problems
Be specific about coordinates/positions.
" screenshot.jpg
```

### For Form UI

```bash
node scripts/process-screenshot.js --prompt "
Analyze this form:
1. Are all labels properly aligned with inputs?
2. Is error state visible? What color?
3. Is submit button clearly visible and styled?
4. Any accessibility concerns visible?
" form.jpg
```

### For Dashboard/Data Display

```bash
node scripts/process-screenshot.js --prompt "
Analyze this dashboard:
1. Are charts/graphs rendering correctly?
2. Is data visible and readable?
3. Any loading states or empty states showing?
4. Navigation elements accessible?
" dashboard.jpg
```

## Complete Example: UI Bug Investigation

```
// User reports: "The submit button looks wrong on mobile"

// 1. Switch to mobile viewport
resize_page({ width: 375, height: 667 })

// 2. First, check DOM state (cheap)
take_snapshot()
// Found button UID: "b1"

// 3. Check computed styles (still cheap)
evaluate_script({
  expression: `
    const btn = document.querySelector('[data-uid="b1"]');
    {
      width: btn.offsetWidth,
      height: btn.offsetHeight,
      visible: btn.offsetParent !== null,
      styles: {
        display: getComputedStyle(btn).display,
        position: getComputedStyle(btn).position,
        padding: getComputedStyle(btn).padding
      }
    }
  `
})
// Found: width is 0 due to display:none in mobile CSS

// 4. Only if still unclear, screenshot the specific area
take_screenshot({ uid: "form-container" })
node scripts/process-screenshot.js --prompt "Is submit button visible? Describe its appearance." element.png
```

**Diagnosis cost:** ~500 tokens
**With screenshots every step:** ~4,000+ tokens

## Best Practices

1. **Start with code inspection** - evaluate_script for styles/positions
2. **Use snapshots for structure** - cheaper than screenshots
3. **Target specific elements** - never full-page unless necessary
4. **Use JPEG for full-page** - 30-40% smaller
5. **Process via Gemini** - 80%+ token reduction
6. **Custom prompts** - tell Gemini exactly what to look for
