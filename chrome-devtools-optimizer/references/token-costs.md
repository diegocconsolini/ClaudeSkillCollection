# Token Cost Analysis

Detailed breakdown of token consumption for Chrome DevTools MCP operations.

## Image Token Costs

### Direct to Claude (Current)

| Image Type | Resolution | Tokens | Cost (Opus) |
|------------|------------|--------|-------------|
| Full page PNG | 1920x1080 | ~2,500 | ~$0.038 |
| Full page PNG | 1280x720 | ~1,600 | ~$0.024 |
| Full page JPEG 80% | 1280x720 | ~1,200 | ~$0.018 |
| Full page JPEG 50% | 1280x720 | ~800 | ~$0.012 |
| Element crop | 400x300 | ~400 | ~$0.006 |

### Via Gemini Flash (Optimized)

| Operation | Tokens to Claude | Gemini Cost | Total Savings |
|-----------|------------------|-------------|---------------|
| Full page → summary | ~300 | ~$0.001 | 82% |
| Element → description | ~150 | ~$0.0005 | 85% |
| Form → field list | ~200 | ~$0.0007 | 80% |

## Text-Based Operations

| Operation | Typical Tokens | Notes |
|-----------|----------------|-------|
| take_snapshot (simple) | 300-500 | Login page, simple form |
| take_snapshot (medium) | 500-1,000 | Dashboard, moderate UI |
| take_snapshot (complex) | 1,000-1,500 | Data-heavy, many elements |
| Console messages (filtered) | 100-300 | With type filter |
| Console messages (all) | 500-1,000 | No filter |
| Network list (filtered) | 200-500 | XHR/Fetch only |
| Network list (all) | 1,000-2,000 | All resource types |

## Workflow Comparisons

### Login Flow

**Unoptimized:**
```
navigate → screenshot → fill email → screenshot → fill password → screenshot → click → screenshot
Total: ~6,400 tokens
```

**Optimized:**
```
navigate → snapshot → fill_form (all fields) → click → snapshot
Total: ~1,200 tokens
Savings: 81%
```

### Form Validation Testing

**Unoptimized:**
```
For each of 5 fields:
  fill invalid → screenshot → check error → fill valid → screenshot
Total: ~16,000 tokens
```

**Optimized:**
```
snapshot once → fill_form (all invalid) → snapshot → fill_form (all valid) → snapshot
Total: ~2,500 tokens
Savings: 84%
```

### Visual Regression Check

**Unoptimized:**
```
screenshot full page → Claude analyzes → describe differences
Total: ~3,200 tokens
```

**Optimized:**
```
screenshot → Gemini Flash → text summary to Claude
Total: ~500 tokens
Savings: 84%
```

### Debug Console Errors

**Unoptimized:**
```
list_console_messages (all) → screenshot for context
Total: ~2,600 tokens
```

**Optimized:**
```
list_console_messages (errors only, limit 10) → snapshot (if needed)
Total: ~600 tokens
Savings: 77%
```

## Cost Projections

### Per-Session Estimates (50 operations)

| Approach | Tokens | Claude Cost | Gemini Cost | Total |
|----------|--------|-------------|-------------|-------|
| Unoptimized | ~80,000 | ~$1.20 | $0 | ~$1.20 |
| Snapshot-first | ~25,000 | ~$0.38 | $0 | ~$0.38 |
| Full optimization | ~15,000 | ~$0.23 | ~$0.05 | ~$0.28 |

### Monthly Projections (10 sessions/day)

| Approach | Monthly Tokens | Monthly Cost |
|----------|----------------|--------------|
| Unoptimized | 24M | ~$360 |
| Snapshot-first | 7.5M | ~$114 |
| Full optimization | 4.5M | ~$84 |

## Optimization ROI

| Strategy | Implementation Effort | Token Savings |
|----------|----------------------|---------------|
| Snapshot over screenshot | None (just use it) | 60-70% |
| Element-targeted shots | Low | 50-60% |
| JPEG compression | None | 30-40% |
| Gemini Flash integration | Medium | 80-85% |
| Batch form operations | Low | 40-60% |
| Network/console filtering | Low | 50-70% |

## Break-Even Analysis

Gemini Flash setup time: ~15 minutes
Break-even point: ~50 screenshot operations
At 5 screenshots/session: ~10 sessions to ROI
