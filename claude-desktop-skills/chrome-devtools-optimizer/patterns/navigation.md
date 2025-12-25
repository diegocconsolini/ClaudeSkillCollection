# Navigation Patterns

Efficient patterns for page navigation and verification.

## Basic Navigation

### Navigate and Verify (Optimized)

```
1. navigate_page({ url: "https://example.com/page" })
2. take_snapshot()  // Verify page loaded, get element UIDs
```

**Cost:** ~400 tokens

### Navigate and Verify (Unoptimized - Avoid)

```
1. navigate_page({ url: "https://example.com/page" })
2. take_screenshot()  // Expensive, usually unnecessary
```

**Cost:** ~1,650 tokens

## Multi-Page Navigation

### Sequential Pages

```
// Page 1
navigate_page({ url: "/step1" })
take_snapshot()  // Get UIDs for actions

// Complete step 1 actions...
click({ uid: "next-button-uid" })

// Page 2 - don't screenshot, just verify
take_snapshot()  // Confirm new page, get new UIDs
```

**Cost per page:** ~500 tokens (vs ~1,650 with screenshots)

### Tab Management

```
// Open new tab for comparison
new_page({ url: "https://staging.example.com" })
take_snapshot()  // Verify staging page

// Switch back to original
list_pages()
select_page({ pageId: "original-page-id" })
```

## Verification Patterns

### Verify URL Changed

```javascript
// After navigation action
evaluate_script({ expression: "window.location.href" })
// Returns just the URL string, ~50 tokens
```

### Verify Page Title

```javascript
evaluate_script({ expression: "document.title" })
// Returns just the title, ~30 tokens
```

### Verify Element Exists

```
take_snapshot()
// Look for expected element UID in response
// Much cheaper than screenshot to visually verify
```

### Verify Redirect Completed

```javascript
// Check final URL after potential redirects
evaluate_script({
  expression: "window.location.href"
})
// Compare with expected destination
```

## Wait Patterns

### Wait for Element (via snapshot)

```
// Retry snapshot until element appears
take_snapshot()
// If element UID not found, wait and retry
// More efficient than repeated screenshots
```

### Wait for Network Idle

```
// Check for pending requests
list_network_requests({
  resourceTypes: ["XHR", "Fetch"],
  pageSize: 5
})
// If recent requests still pending, wait
```

## Error Handling

### Handle Navigation Failure

```
1. navigate_page({ url: "..." })
2. list_console_messages({ types: ["error"], pageSize: 5 })
3. If errors found, take_snapshot() to understand state
```

### Handle 404/Error Pages

```
1. navigate_page({ url: "..." })
2. evaluate_script({ expression: "document.title" })
   // Check for "404", "Not Found", etc.
3. Only take_snapshot() if error confirmed
```

## Complete Example: Login Flow

```
// 1. Navigate to login
navigate_page({ url: "https://app.example.com/login" })

// 2. Verify login page (snapshot, not screenshot)
take_snapshot()
// Response shows: email input (uid: "i1"), password input (uid: "i2"), submit button (uid: "b1")

// 3. Fill form efficiently (batch)
fill_form({
  fields: {
    "i1": "user@example.com",
    "i2": "password123"
  }
})

// 4. Submit
click({ uid: "b1" })

// 5. Verify success (check URL, not screenshot)
evaluate_script({ expression: "window.location.href" })
// If URL is dashboard, success!

// 6. Optional: Confirm dashboard loaded
take_snapshot()
// Verify expected dashboard elements present
```

**Total cost:** ~1,000 tokens
**Unoptimized (screenshots):** ~5,000+ tokens
**Savings:** 80%
