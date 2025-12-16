# Debugging Patterns

Efficient patterns for debugging web applications.

## Console Error Debugging

### Get Errors Only (Optimized)

```
list_console_messages({
  types: ["error"],
  pageSize: 10
})
```

**Cost:** ~150 tokens

### Get All Console (Unoptimized - Avoid)

```
list_console_messages({})
// Returns everything including verbose logs
```

**Cost:** ~1,000+ tokens

### Tiered Console Investigation

```
// Step 1: Errors only
list_console_messages({ types: ["error"], pageSize: 5 })

// Step 2: If errors found, get warnings too
list_console_messages({ types: ["error", "warning"], pageSize: 10 })

// Step 3: Only if needed, get info/log
list_console_messages({ types: ["error", "warning", "log"], pageSize: 20 })
```

## Network Debugging

### API Calls Only (Optimized)

```
list_network_requests({
  resourceTypes: ["XHR", "Fetch"],
  pageSize: 10
})
```

**Cost:** ~300 tokens

### Failed Requests

```
list_network_requests({
  resourceTypes: ["XHR", "Fetch"],
  pageSize: 20
})
// Filter results for status >= 400
```

### Specific Request Details

```
// After finding request ID from list
get_network_request({
  requestId: "req-123",
  includeBody: false  // Start without body
})

// Only if needed
get_network_request({
  requestId: "req-123",
  includeBody: true
})
```

**Cost:** ~200 without body, ~1,000+ with body

## JavaScript Debugging

### Check for Errors

```javascript
evaluate_script({
  expression: `
    window.__errors = window.__errors || [];
    window.onerror = (msg, url, line) => window.__errors.push({msg, url, line});
    window.__errors
  `
})
```

### Check Variable State

```javascript
evaluate_script({
  expression: `
    JSON.stringify({
      user: window.currentUser,
      cart: window.cartState,
      isLoggedIn: !!window.authToken
    })
  `
})
```

### Test Function Output

```javascript
evaluate_script({
  expression: `
    // Call the function and capture result
    try {
      const result = myFunction(testInput);
      JSON.stringify({ success: true, result });
    } catch (e) {
      JSON.stringify({ success: false, error: e.message });
    }
  `
})
```

## DOM Debugging

### Check Element State

```javascript
evaluate_script({
  expression: `
    const el = document.querySelector('#problem-element');
    el ? {
      visible: el.offsetParent !== null,
      display: getComputedStyle(el).display,
      dimensions: { width: el.offsetWidth, height: el.offsetHeight },
      classes: Array.from(el.classList),
      disabled: el.disabled
    } : { error: 'Element not found' }
  `
})
```

### Find Hidden Elements

```javascript
evaluate_script({
  expression: `
    Array.from(document.querySelectorAll('button, a, input'))
      .filter(el => el.offsetParent === null)
      .map(el => ({ tag: el.tagName, id: el.id, class: el.className }))
  `
})
```

### Check Event Listeners

```javascript
evaluate_script({
  expression: `
    const el = document.querySelector('#button');
    // Note: getEventListeners only works in DevTools console
    // Alternative: check for onclick attribute
    {
      hasOnclick: !!el.onclick,
      onclickAttr: el.getAttribute('onclick')
    }
  `
})
```

## Performance Debugging

### Quick Performance Check

```
get_performance_metrics()
```

**Cost:** ~200 tokens

### Identify Slow Resources

```
list_network_requests({
  resourceTypes: ["Script", "Stylesheet", "Image"],
  pageSize: 20
})
// Check timing info in response
```

### Memory Check

```javascript
evaluate_script({
  expression: `
    performance.memory ? {
      usedJSHeapSize: Math.round(performance.memory.usedJSHeapSize / 1048576) + 'MB',
      totalJSHeapSize: Math.round(performance.memory.totalJSHeapSize / 1048576) + 'MB'
    } : 'Memory API not available'
  `
})
```

## Visual Debugging (When Needed)

### Element-Specific Screenshot

```
// Only if text debugging insufficient
take_screenshot({ uid: "problem-element" })
// Then send to Gemini for analysis
node chrome-devtools-optimizer/scripts/process-screenshot.js screenshot.png
```

**Cost:** ~400-600 tokens total

### Layout Issue Investigation

```
// 1. First try: snapshot with element info
take_snapshot({ uid: "layout-container" })

// 2. If unclear: targeted screenshot
take_screenshot({ uid: "layout-container" })

// 3. Process with Gemini
node scripts/process-screenshot.js --prompt "Describe layout issues" img.png
```

## Complete Debug Session Example

```
// User reports: "Login button doesn't work"

// 1. Check console errors first (cheapest)
list_console_messages({ types: ["error"], pageSize: 5 })
// Found: "TypeError: Cannot read property 'submit' of null"

// 2. Check if button exists
take_snapshot()
// Found: Button UID is "b1"

// 3. Check button state
evaluate_script({
  expression: `
    const btn = document.querySelector('[data-uid="b1"]');
    {
      exists: !!btn,
      disabled: btn?.disabled,
      type: btn?.type,
      form: btn?.form?.id
    }
  `
})
// Found: form is null - button not inside form element

// 4. Root cause identified without any screenshots!
```

**Total cost:** ~600 tokens
**With screenshots at each step:** ~5,000+ tokens
**Savings:** 88%
