---
name: supply-chain-hardening-rules
description: npm/PyPI install-time hardening rules to apply when reviewing or adding dependencies
metadata:
  type: feedback
---

When adding, reviewing, or installing dependencies in this project, apply these rules.

**Why:** the 2024-2026 supply-chain wave (xz-utils CVE-2024-3094, Shai-Hulud, chalk/debug
clipper, Axios/plain-crypto-js, litellm) makes dependency intake a primary attack surface.

**How to apply:**
- Prefer `npm ci` / `pip install --require-hashes` over loose installs; keep lockfiles committed.
- Treat any `postinstall`/`preinstall` script (and `binding.gyp`) as requiring review; default to `ignore-scripts`.
- Apply a release-age cooldown (24-72h) before adopting a brand-new version.
- Flag a newly-added dependency whose name is one edit away from a popular package (typosquat).
- For a release, generate an SBOM (use the `/sbom` skill) and scan it.
- Publish from CI via Trusted Publishing/OIDC; require phishing-resistant 2FA on maintainer accounts.

Link related: [[security-fp-suppressions]].
