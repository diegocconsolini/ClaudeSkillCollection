---
name: chrome-devtools-optimizer
description: Use this skill to reduce token consumption by 70-80% when using the Chrome DevTools MCP. Applies a snapshot-first strategy (text over images) with decision trees and pattern guides for navigation, forms, debugging, and visual checks, plus optional Gemini Flash vision processing for the cases that genuinely need an image.
license: MIT
---

# Chrome DevTools Optimizer Skill

Cuts token cost when driving the Chrome DevTools MCP by preferring text snapshots over
screenshots and only escalating to vision when necessary.

## Usage

Consult the pattern guides in [`patterns/`](patterns/) and the token-cost reference in
[`references/`](references/) when performing browser automation:

- **Snapshot-first:** read the accessibility/text snapshot before taking a screenshot.
- **Decision trees:** navigation, forms, and debugging flows that minimize image captures.
- **Optional Gemini Flash:** for true visual analysis, `scripts/process-screenshot.js`
  sends one image to Gemini Flash (~$0.001) instead of round-tripping a large screenshot.

```bash
# one-time: configure the Gemini API key (read from
# ~/.config/chrome-devtools-optimizer/config.json — never hardcoded)
node scripts/process-screenshot.js <image-path-or-base64>
```

See [`agents/chrome-devtools-optimizer.md`](agents/chrome-devtools-optimizer.md) for the
full decision logic.
