# Chrome DevTools MCP - Tool Reference

Complete reference for all 26 Chrome DevTools MCP tools (v0.12.1+).

## Debugging Tools

### take_screenshot
Captures a screenshot of the page or specific element.

```json
{
  "uid": "element-uid",      // Optional: capture specific element
  "format": "png|jpeg",      // Default: png
  "quality": 80              // For jpeg, 0-100
}
```

**Token cost:** 1,500-4,000 (full page), 400-800 (element)
**Optimization:** Use `uid` for elements, `jpeg` + low quality for full page.

### take_snapshot
Returns accessibility tree as text. **Preferred for structure analysis.**

```json
{
  "uid": "element-uid"       // Optional: snapshot specific subtree
}
```

**Token cost:** 300-1,500
**Use when:** Need page structure, elements, text content.

### evaluate_script
Executes JavaScript in page context.

```json
{
  "expression": "document.title"
}
```

**Token cost:** 50-500 (depends on return value)
**Tip:** Return only what you need, avoid large objects.

### list_console_messages
Returns console log entries.

```json
{
  "types": ["error", "warning"],  // Filter by type
  "pageSize": 20,                  // Limit results
  "pageToken": "..."               // Pagination
}
```

**Token cost:** 100-1,000
**Optimization:** Always filter by type and limit pageSize.

## Input Tools

### click
Clicks an element by uid.

```json
{
  "uid": "button-uid"
}
```

**Token cost:** 20-50

### fill
Fills a single input field.

```json
{
  "uid": "input-uid",
  "value": "text to enter"
}
```

**Token cost:** 20-50
**Optimization:** Use `fill_form` for multiple fields.

### fill_form
Fills multiple form fields at once. **Preferred for forms.**

```json
{
  "fields": {
    "email-uid": "user@example.com",
    "password-uid": "secret123",
    "name-uid": "John Doe"
  }
}
```

**Token cost:** 30-60
**Saves:** 3 separate fill calls = 60-150 tokens.

### hover
Hovers over an element.

```json
{
  "uid": "element-uid"
}
```

**Token cost:** 20-50

### press_key
Presses a keyboard key.

```json
{
  "key": "Enter",
  "modifiers": ["Shift"]     // Optional
}
```

**Token cost:** 20-50

### drag
Drags from one element to another.

```json
{
  "sourceUid": "drag-source",
  "targetUid": "drop-target"
}
```

**Token cost:** 30-60

## Navigation Tools

### navigate_page
Navigates to a URL.

```json
{
  "url": "https://example.com"
}
```

**Token cost:** 30-60

### list_pages
Lists all open pages/tabs.

**Token cost:** 50-200

### select_page
Switches to a different page/tab.

```json
{
  "pageId": "page-id"
}
```

**Token cost:** 20-50

### new_page
Opens a new page/tab.

```json
{
  "url": "https://example.com"    // Optional
}
```

**Token cost:** 30-60

### close_page
Closes a page/tab.

```json
{
  "pageId": "page-id"            // Optional, closes current if omitted
}
```

**Token cost:** 20-50

## Network Tools

### list_network_requests
Lists captured network requests.

```json
{
  "resourceTypes": ["Document", "XHR", "Fetch"],  // Filter
  "pageSize": 20,
  "pageToken": "..."
}
```

**Token cost:** 200-2,000
**Optimization:** Always use resourceTypes filter and pageSize limit.

### get_network_request
Gets details of a specific request.

```json
{
  "requestId": "request-id",
  "includeBody": false           // Set true only if needed
}
```

**Token cost:** 100-500 (without body), 500-5,000 (with body)
**Optimization:** Only include body when necessary.

## Performance Tools

### start_trace
Starts performance tracing.

**Token cost:** 20-50

### stop_trace
Stops tracing and returns results.

**Token cost:** 500-5,000 (depends on trace duration)
**Tip:** Keep traces short and focused.

### get_performance_metrics
Returns performance metrics.

**Token cost:** 100-300

## Emulation Tools

### emulate
Sets device emulation.

```json
{
  "device": "iPhone 12"          // Or custom dimensions
}
```

**Token cost:** 30-60

### resize_page
Resizes the viewport.

```json
{
  "width": 375,
  "height": 667
}
```

**Token cost:** 20-50

## Quick Reference Table

| Tool | Typical Tokens | Category |
|------|---------------|----------|
| take_screenshot | 1,500-4,000 | HIGH |
| take_snapshot | 300-1,500 | MEDIUM |
| list_network_requests | 200-2,000 | MEDIUM |
| list_console_messages | 100-1,000 | MEDIUM |
| evaluate_script | 50-500 | LOW-MEDIUM |
| stop_trace | 500-5,000 | HIGH |
| get_network_request (body) | 500-5,000 | HIGH |
| All other tools | 20-100 | LOW |
