# Plugin Security Checker v3.2.0

Static analysis tool for Claude Code plugins with 91 specialized pattern detection agents.

## Current Status (December 2025)

**Phase 3 Complete: IntelligentOrchestrator**

- ✓ 91 specialized agents generated
- ✓ AccuracyCache with Bloom+Trie hybrid
- ✓ MITRE ATLAS/ATT&CK export
- ✓ Shared learning system
- ✓ Consensus voting engine
- ✓ Adaptive routing and resource management
- → Ready for production deployment (Phase 4)

## Components

### 1. AccuracyCache (accuracy_cache.py)
- Bloom filter + Trie hybrid for zero false positives from probabilistic lookups
- Shared learning across all 91 agents  
- MITRE ATLAS JSON export
- Auto-evolving rules from validated detections
- File type correlation learning
- Adaptive eviction by agent accuracy

### 2. PatternAgent (pattern_agent.py)
- Base class for specialized agents
- Context-aware confidence scoring
- Historical accuracy tracking via cache
- Validation learning

### 3. IntelligentOrchestrator (intelligent_orchestrator.py)
- Consensus voting across multiple agents
- Conflict resolution using MITRE ATT&CK/ATLAS
- Resource management (<500MB RAM)
- Adaptive agent routing (best agents per file type)
- Emergency cache clearing

### 4. 91 Specialized Agents

**CRITICAL (17):** eval, exec, compile, rmtree, setuid, sudo, types.FunctionType, importlib.import_module, etc.

**HIGH (39):** os.system, subprocess.*, os.environ.get, urlretrieve, socket.connect, requests.post, credential theft, etc.

**MEDIUM (23):** chr obfuscation, debugger detection, innerHTML, outerHTML, yaml.load, etc.

**LOW (2):** tempfile.mktemp, input

**Languages:** Python (63), JavaScript (18), Obfuscation (7), Credentials (3)

Full list: `python3 scripts/generate_agents.py`

## Quick Start

```python
# Using IntelligentOrchestrator (recommended)
from intelligent_orchestrator import IntelligentOrchestrator

# Initialize with all 91 agents
orchestrator = IntelligentOrchestrator(
    patterns_file="references/dangerous_functions_expanded.json",
    max_memory_mb=500,
    enable_adaptive_routing=True
)

# Scan file with consensus voting
code = open("plugin.py").read()
detections = orchestrator.scan_file("plugin.py", code)

# Review consensus detections
for det in detections:
    print(f"Line {det.line_number}: {det.severity}")
    print(f"  Confidence: {det.confidence:.0%}")
    print(f"  Voting agents: {det.vote_count}")
    print(f"  ATT&CK: {det.primary_attack_id}")

# Export findings to ATLAS format
orchestrator.export_findings("findings.json")

# Get statistics
stats = orchestrator.get_statistics()
print(f"Memory usage: {stats['memory_usage_mb']:.2f} MB")
```

## Test Results

**Core tests:** 10/10 passed
**Edge cases:** 12/12 passed
**Orchestrator tests:** 7/7 passed
**Total:** 29/29 (100%)

Test scripts and reports available in `archive_dev_files/`

## Files

```
scripts/
  accuracy_cache.py              # 400+ lines - Production cache
  pattern_agent.py               # 250+ lines - Base agent
  generate_agents.py             # Agent generator
  intelligent_orchestrator.py    # 500+ lines - Consensus engine
  test_orchestrator.py           # 300+ lines - Orchestrator tests

references/
  dangerous_functions_expanded.json  # 91 patterns

archive/
  mcpcache-standard-2q/          # Archived 2Q implementation
```

## Performance

**Cache:**
- Throughput: 11,111 ops/sec (extreme load test)
- Eviction: 60-68 microseconds
- False positives: 0% (bloom+trie validation)
- Memory: ~250 bytes per detection

**Orchestrator:**
- 91 active agents
- Memory usage: ~17 MB (3.4% of 500MB budget)
- Consensus voting with conflict resolution
- Adaptive routing enabled

## Updating Threat Intelligence

The scanner uses MITRE ATT&CK and ATLAS frameworks for threat intelligence. Keep the data current:

### Check for Updates

```bash
# Check if updates are available
python3 scripts/scan_plugin.py --check-updates
```

### Update Before Scanning

```bash
# Update threat data then scan
python3 scripts/scan_plugin.py --update /path/to/plugin

# Or update separately
python3 -c "
from scripts.taxii_updater import TAXIIUpdater
updater = TAXIIUpdater()
if updater.check_for_updates():
    updater.update_all()
"
```

### Manual Update (Shell Script)

```bash
# Download latest STIX data from GitHub
bash scripts/download_attack_data.sh
```

### Data Sources

| Source | Current Version | Update Frequency |
|--------|-----------------|------------------|
| MITRE ATT&CK (Enterprise) | v18.1 | Quarterly |
| MITRE ATT&CK (Mobile) | v18.1 | Quarterly |
| MITRE ATT&CK (ICS) | v18.1 | Quarterly |
| MITRE ATLAS | v4.5.0 | As needed |
| OWASP Top 10 | 2021 | ~4 years |
| OWASP API | 2023 | ~2 years |
| CWE | 4.14 | Quarterly |

### Dependencies for Updates

```bash
pip3 install taxii2-client stix2
```

### Version Management

All version numbers are managed from a single source of truth: `version.json`

```bash
# Preview version sync
python3 scripts/sync_versions.py

# Apply version changes across all files
python3 scripts/sync_versions.py --apply
```

**Files synced from version.json:**
- `.claude-plugin/plugin.json` (plugin version)
- `README.md` (header, data source table)
- `agents/plugin-security-checker.md` (version references)
- `references/threat_mappings.json` (framework versions)
- `scripts/scan_plugin.py` (scanner version constant)

## Changelog

### v3.2.0 (December 2025)
- Added `--update` and `--check-updates` CLI flags
- Added `version.json` as single source of truth for versions
- Added `sync_versions.py` script for version management
- Updated STIX data to ATT&CK v18.1 (November 2025)
- Updated threat_mappings.json to ATT&CK v18.1
- Documented threat intelligence update procedures
- Synced version numbers across all files

### v3.0.0 (October 23, 2025)
- IntelligentOrchestrator with consensus voting
- 91 specialized agents (17 CRITICAL, 39 HIGH, 23 MEDIUM, 2 LOW)
- AccuracyCache with Bloom+Trie (zero false positives)
- MITRE ATLAS/ATT&CK export
- Shared learning across agents
- Auto-evolving rules from validated findings
- Adaptive routing by file type
- Resource management (<500MB RAM)
- 29/29 tests passed (100%)

### v2.0.0 (January 2025)
- MITRE ATT&CK/ATLAS integration
- STIX 2.1 enrichment
- 63 Python patterns

### v1.0.0 (January 2025)
- Initial release
- Basic pattern matching
