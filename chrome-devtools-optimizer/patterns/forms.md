# Form Patterns

Efficient patterns for form interaction and validation testing.

## Basic Form Filling

### Fill Form (Optimized)

```
1. take_snapshot()  // Get all field UIDs at once
2. fill_form({      // Fill all fields in one call
     fields: {
       "email-uid": "user@example.com",
       "password-uid": "secret123",
       "name-uid": "John Doe"
     }
   })
3. click({ uid: "submit-uid" })
```

**Cost:** ~450 tokens

### Fill Form (Unoptimized - Avoid)

```
1. take_screenshot()  // Expensive
2. fill({ uid: "email", value: "..." })
3. take_screenshot()  // Why?
4. fill({ uid: "password", value: "..." })
5. take_screenshot()  // Still why?
6. click({ uid: "submit" })
7. take_screenshot()  // Finally makes sense
```

**Cost:** ~6,500 tokens

## Form Validation Testing

### Test Required Fields

```
// 1. Get form structure
take_snapshot()

// 2. Submit empty form
click({ uid: "submit-uid" })

// 3. Check for validation errors (text, not visual)
take_snapshot()
// Look for error messages in accessibility tree

// 4. Fill one field at a time if needed
fill({ uid: "email-uid", value: "valid@email.com" })
click({ uid: "submit-uid" })
take_snapshot()  // Check which errors remain
```

### Test Invalid Input

```
// 1. Fill with invalid data
fill_form({
  fields: {
    "email-uid": "not-an-email",
    "phone-uid": "abc",
    "age-uid": "-5"
  }
})

// 2. Submit
click({ uid: "submit-uid" })

// 3. Check errors
take_snapshot()
// Errors visible in text output
```

### Test Field Constraints

```javascript
// Check field attributes
evaluate_script({
  expression: `
    const field = document.querySelector('#email');
    JSON.stringify({
      required: field.required,
      pattern: field.pattern,
      maxLength: field.maxLength,
      type: field.type
    })
  `
})
// Returns constraint info, ~100 tokens
```

## Dynamic Forms

### Handle Conditional Fields

```
// 1. Initial snapshot
take_snapshot()
// See: country dropdown (uid: "d1")

// 2. Select country
// Use evaluate_script for select elements
evaluate_script({
  expression: `
    document.querySelector('[data-uid="d1"]').value = 'US';
    document.querySelector('[data-uid="d1"]').dispatchEvent(new Event('change'));
  `
})

// 3. Re-snapshot to see new fields
take_snapshot()
// Now see: state dropdown (uid: "d2"), zip code (uid: "i3")
```

### Handle Auto-Complete

```javascript
// Trigger autocomplete
fill({ uid: "address-uid", value: "123 Main" })

// Wait briefly for suggestions
// Then snapshot to see options
take_snapshot()
// Or evaluate to get suggestions
evaluate_script({
  expression: `
    Array.from(document.querySelectorAll('.autocomplete-option'))
      .map(el => el.textContent)
  `
})
```

## Form State Verification

### Check Field Values

```javascript
// Get all form values at once
evaluate_script({
  expression: `
    const form = document.querySelector('form');
    const data = new FormData(form);
    Object.fromEntries(data.entries())
  `
})
// Returns all values, ~100-200 tokens
```

### Check Validation State

```javascript
evaluate_script({
  expression: `
    const form = document.querySelector('form');
    JSON.stringify({
      valid: form.checkValidity(),
      invalidFields: Array.from(form.elements)
        .filter(el => !el.validity.valid)
        .map(el => ({ name: el.name, error: el.validationMessage }))
    })
  `
})
```

### Check Dirty State

```javascript
evaluate_script({
  expression: `
    Array.from(document.querySelectorAll('input, textarea, select'))
      .filter(el => el.value !== el.defaultValue)
      .map(el => el.name)
  `
})
// Returns list of modified fields
```

## File Uploads

### Handle File Input

```javascript
// File inputs are tricky - use evaluate_script
evaluate_script({
  expression: `
    // Check if file input exists
    const input = document.querySelector('input[type="file"]');
    input ? { found: true, accept: input.accept, multiple: input.multiple } : { found: false }
  `
})

// Note: Actual file upload requires browser automation beyond MCP
// Document this limitation
```

## Complete Example: Registration Form

```
// 1. Navigate and get structure
navigate_page({ url: "/register" })
take_snapshot()
// Returns UIDs: name (i1), email (i2), password (i3), confirm (i4), terms (c1), submit (b1)

// 2. Fill all fields at once
fill_form({
  fields: {
    "i1": "John Doe",
    "i2": "john@example.com",
    "i3": "SecurePass123!",
    "i4": "SecurePass123!"
  }
})

// 3. Check the checkbox
click({ uid: "c1" })

// 4. Submit
click({ uid: "b1" })

// 5. Verify success
evaluate_script({ expression: "window.location.href" })
// If redirected to /welcome or /dashboard, success!

// 6. Optional: Check for welcome message
take_snapshot()
// Look for success text in response
```

**Total cost:** ~900 tokens
**Unoptimized:** ~4,000+ tokens
**Savings:** 78%
