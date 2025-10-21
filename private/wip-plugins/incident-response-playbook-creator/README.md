# Incident Response Playbook Creator - Private Development (v2.0.0)

**Status**: In Development
**Current Public Version**: 1.0.0 (4 scenarios)
**Target Version**: 2.0.0 (11 scenarios)

---

## Directory Organization

This is the **private development workspace** for expanding the Incident Response Playbook Creator from 4 to 11 scenarios.

### Structure

```
private/wip-plugins/incident-response-playbook-creator/
├── README.md                  (This file)
├── docs/                      NIST authoritative source documents
│   ├── NIST.IR.8228.pdf      IoT Device Cybersecurity (1.0MB)
│   ├── NIST.SP.800-161r1-upd1.pdf   C-SCRM Supply Chain (3.3MB) ⚠️ TOO LARGE
│   ├── NIST.SP.800-190.pdf   Container Security (651KB)
│   ├── NIST.SP.800-218.pdf   SSDF Secure Software Dev (723KB) ✅ EXTRACTED
│   └── NIST.SP.800-82r3.pdf  OT/ICS Security (8.2MB) ⚠️ TOO LARGE
└── planning/
    └── EXPANSION_PLAN.md      Roadmap for v2.0.0 expansion
```

### Public Plugin (PRODUCTION - DO NOT MODIFY)

```
incident-response-playbook-creator/     Production v1.0.0 (4 scenarios)
├── plugin.json
├── SKILL.md
├── README.md
├── scripts/
│   ├── browse_scenarios.py
│   └── generate_playbook_markdown.py
├── references/
│   ├── incident_scenarios_simplified.json    4 scenarios
│   ├── framework_mappings.json
│   └── communication_templates.json
├── output/                    Generated playbooks
├── examples/
└── templates/
```

**DO NOT modify the public plugin** - it's already published and installed by users.

---

## Development Workflow

### Phase 1: Extract Content from PDFs ⚠️ BLOCKED

**Problem**: Large PDFs (3.3MB, 8.2MB) cannot be read by Task agent
- ❌ NIST SP 800-161r1-upd1.pdf (3.3MB) - "PDF too large"
- ❌ NIST SP 800-82r3.pdf (8.2MB) - "PDF too large"

**Solutions to Try**:
1. Extract PDFs to text files first
2. Read PDFs in smaller page chunks
3. Use external PDF processing tool
4. Extract only specific chapters/sections

**What Works**:
- ✅ NIST SP 800-218 (723KB) - Successfully extracted via Task agent
- ⚠️ NIST SP 800-190 (651KB) - Should work (not yet tested)
- ⚠️ NIST IR 8228 (1.0MB) - Should work (not yet tested)

### Phase 2: Build New Scenarios

Once PDF extraction is resolved, build these 7 new scenarios:

1. **Supply Chain Attack** - Can start now (SP 800-218 already extracted)
2. **Container/Kubernetes Security** - Try reading SP 800-190
3. **IoT/OT Security** - Try reading IR 8228, find workaround for SP 800-82r3
4. **Cloud Security Breach** - Need AWS/Azure/GCP docs
5. **API Security** - Need OWASP API Top 10 2023
6. **Insider Threat** - Use SP 800-61r3 + web research
7. **DDoS Attack** - Need CISA DDoS Guide

### Phase 3: Testing & Release

1. Validate all 11 scenarios in JSON
2. Test playbook generation for all scenarios
3. Update documentation
4. Copy completed work to public plugin
5. Commit as v2.0.0
6. Update marketplace.json

---

## Current Blockers

### 🔴 CRITICAL: Large PDF Extraction
- Cannot read NIST SP 800-161r1-upd1.pdf (3.3MB)
- Cannot read NIST SP 800-82r3.pdf (8.2MB)
- Task agent returns "PDF too large" error

### 🟡 MEDIUM: Missing Documents
Need to download:
- OWASP API Security Top 10 2023
- AWS Security Incident Response Guide
- CISA DDoS Guide

---

## Notes

- All NIST documents are **copies** - originals remain in `/docs/`
- EXPANSION_PLAN.md has full details on all 11 scenarios
- Public plugin (v1.0.0) remains untouched and functional
- This private workspace is for v2.0.0 development only

---

**Next Steps**: See `planning/EXPANSION_PLAN.md` for detailed roadmap
