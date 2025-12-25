# Decision Tree for Chrome DevTools Operations

Use this flowchart to choose the most token-efficient approach.

## Main Decision Flow

```
START: What information do you need?
│
├─► Page structure (elements, hierarchy, text)?
│   └─► USE: take_snapshot
│       Cost: 300-1,500 tokens
│       Returns: Accessibility tree with UIDs
│
├─► Visual appearance (colors, layout, styling)?
│   │
│   └─► Is Gemini Flash configured?
│       │
│       ├─► YES: Screenshot → Gemini → text summary
│       │   Cost: ~300 tokens + $0.001
│       │
│       └─► NO: Can you use JPEG compression?
│           │
│           ├─► YES: Screenshot (JPEG 50%)
│           │   Cost: ~800 tokens
│           │
│           └─► NO: Screenshot (PNG)
│               Cost: ~1,600 tokens
│
├─► Specific element only?
│   │
│   └─► USE: take_snapshot OR take_screenshot with uid
│       Cost: 200-600 tokens
│       TIP: Snapshot if you need UIDs, screenshot if visual
│
├─► Form field values?
│   │
│   └─► USE: evaluate_script to read values
│       Cost: 50-100 tokens
│       Example: document.querySelector('#email').value
│
├─► Console errors?
│   │
│   └─► USE: list_console_messages with filter
│       { "types": ["error"], "pageSize": 10 }
│       Cost: 100-300 tokens
│
├─► Network requests?
│   │
│   └─► USE: list_network_requests with filter
│       { "resourceTypes": ["XHR", "Fetch"], "pageSize": 20 }
│       Cost: 200-500 tokens
│
└─► Complex visual reasoning (pixel-perfect, subtle issues)?
    └─► USE: Direct screenshot to Claude (last resort)
        Cost: 1,600-4,000 tokens
```

## Action Decision Flow

```
START: What action do you need to perform?
│
├─► Fill multiple form fields?
│   └─► USE: fill_form (batch)
│       Cost: 30-60 tokens
│       NOT: Multiple fill calls (60-150 tokens)
│
├─► Click a button/link?
│   │
│   └─► Do you have the element UID?
│       │
│       ├─► YES: USE click with uid
│       │   Cost: 20-50 tokens
│       │
│       └─► NO: take_snapshot first → get uid → click
│           Cost: 350-550 tokens
│
├─► Navigate to URL?
│   └─► USE: navigate_page
│       Cost: 30-60 tokens
│       TIP: Don't screenshot after, use snapshot
│
├─► Check page loaded correctly?
│   │
│   └─► What do you need to verify?
│       │
│       ├─► Elements exist: take_snapshot
│       │   Cost: 300-500 tokens
│       │
│       ├─► No errors: list_console_messages (errors)
│       │   Cost: 100-200 tokens
│       │
│       └─► Visual correct: Screenshot → Gemini
│           Cost: ~300 tokens
│
└─► Test responsive design?
    └─► resize_page → take_snapshot
        Cost: 350-600 tokens
        NOT: resize_page → screenshot (1,650+ tokens)
```

## Verification Decision Flow

```
START: Verify operation succeeded?
│
├─► Form submission?
│   │
│   └─► What indicates success?
│       │
│       ├─► URL change: evaluate_script (window.location.href)
│       │   Cost: 50 tokens
│       │
│       ├─► Success message: take_snapshot → find text
│       │   Cost: 300-500 tokens
│       │
│       └─► Visual change: Screenshot → Gemini
│           Cost: ~300 tokens
│
├─► Page navigation?
│   │
│   └─► USE: take_snapshot to verify new page
│       Cost: 300-500 tokens
│       Check: Expected elements present
│
├─► Element state change?
│   │
│   └─► USE: take_snapshot with element uid
│       Cost: 200-400 tokens
│       OR: evaluate_script to check attribute
│       Cost: 50 tokens
│
└─► Network request completed?
    └─► USE: list_network_requests (filtered)
        Cost: 200-400 tokens
        Check: Expected request in list
```

## Quick Reference

| Scenario | Recommended Tool | Tokens |
|----------|-----------------|--------|
| "What's on this page?" | take_snapshot | 300-1,500 |
| "Does this look right?" | screenshot → Gemini | ~300 |
| "Fill the login form" | fill_form | 30-60 |
| "Click the submit button" | click (with uid) | 20-50 |
| "Any console errors?" | list_console_messages (filter) | 100-300 |
| "What API calls were made?" | list_network_requests (filter) | 200-500 |
| "Is the element visible?" | take_snapshot (element uid) | 200-400 |
| "Test mobile view" | resize_page → snapshot | 350-600 |

## Anti-Patterns to Avoid

| Bad Pattern | Why It's Bad | Better Approach |
|-------------|--------------|-----------------|
| Screenshot after every action | 1,600 tokens each | Snapshot or verify only when needed |
| Multiple fill() calls | 50 tokens × N fields | Single fill_form() |
| Unfiltered console/network | 1,000+ tokens | Always filter and limit |
| Full page screenshot for one element | Wastes tokens | Use uid parameter |
| PNG when JPEG works | Larger file | JPEG 50% for full page |
| Re-snapshot unchanged page | Redundant tokens | Reference previous snapshot |
