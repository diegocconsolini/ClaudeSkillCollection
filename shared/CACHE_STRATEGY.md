# Smart Cache Strategy - v2.0.0

## Overview

The smart-extractor series (PDF, XLSX, DOCX) now uses a **unified caching system** (`smart_cache.py`) for consistent, efficient extraction caching across all document types.

## Current Implementation (v2.0.0)

### Cache Location

**Default:** `~/.claude-cache/{doc_type}/`

Example structure:
```
~/.claude-cache/
├── pdf/
│   ├── NIST.SP.800-82r3_6d7b84bb7513d721/
│   └── report_analysis_a1b2c3d4e5f67890/
├── xlsx/
│   ├── CCMv4_7eedad6154cbc160/
│   └── budget_2024_d7dc6faa30339ad2/
└── docx/
    ├── policy_document_69461e394e52dd97/
    └── requirements_spec_8f9a0b1c2d3e4f56/
```

### Hashing Algorithm

**SHAKE256** (SHA-3 family, NIST FIPS 202)
- Modern cryptographic hash function
- Flexible output length
- 16-character hex output for cache keys
- Format: `{filename}_{shake256_hash[:16]}`

### Migration from v1.x

**Automatic SHA-256 → SHAKE256 migration:**
- Detects old caches using SHA-256 hashes
- Migrates to new format transparently
- Old cache locations:
  - `~/.claude-pdf-cache/` → `~/.claude-cache/pdf/`
  - `~/.claude-xlsx-cache/` → `~/.claude-cache/xlsx/`
  - `~/.claude-docx-cache/` → `~/.claude-cache/docx/`

### Cache Structure

Each cached extraction contains:
- `manifest.json` - Metadata and statistics
- `full_text.txt` or `content.json` - Extracted content
- `metadata.json` - Document properties
- Additional format-specific files (TOC, formulas, etc.)

## User Configuration

### Current Options

**1. Direct Parameter** (programmatic use)
```python
from smart_cache import SmartCache

cache = SmartCache(doc_type='pdf', cache_dir='/custom/path')
```

**2. Environment Variable** (future - planned for v2.1.0)
```bash
export CLAUDE_CACHE_DIR=~/my-custom-cache
```

The system will prioritize:
1. `cache_dir` parameter (if provided)
2. `CLAUDE_CACHE_DIR` env var (if set)
3. Default: `~/.claude-cache/`

## Why `~/.claude-cache/`?

### Decision Rationale

After researching platform standards, we chose `~/.claude-cache/` for v2.0.0 because:

1. **Works reliably** in Claude Code environment (tested and verified)
2. **Simple and proven** - avoids complexity of platform-specific paths
3. **User-configurable** - will support env var override in v2.1.0
4. **Unified structure** - single location for all extractors

### Alternative Considered

Platform-specific standards:
- macOS: `~/Library/Caches/claude-smart-extractors/`
- Linux: `~/.cache/claude-smart-extractors/`
- Windows: `%LOCALAPPDATA%\claude-smart-extractors\Cache\`

**Why not chosen for v2.0.0:**
- Uncertainty about Claude Code access permissions
- Additional complexity without proven benefit
- Can be added later via env var configuration

## Future Evolution

### v2.1.0 (Planned)

**Environment Variable Support**
```bash
# Custom cache location
export CLAUDE_CACHE_DIR=~/Documents/extraction-cache

# Platform-specific location
export CLAUDE_CACHE_DIR=~/Library/Caches/claude-smart-extractors
```

**Config File Support** (optional)
```json
{
  "cache_dir": "~/Library/Caches/claude-smart-extractors",
  "enable_bloom": false
}
```

### v2.2.0 (Planned)

**MCP Cache Management Server**

Provide tools for Claude to manage cache:
- `get_cache_location()` - Query current cache directory
- `set_cache_location(path)` - Change cache location
- `list_cached_docs()` - Browse extracted documents
- `clear_cache(doc_type)` - Clean up old caches
- `cache_stats()` - View cache size and statistics

**Resource Exposure**
```
cache://extractors/pdf/list
cache://extractors/xlsx/list
cache://extractors/docx/list
```

### v3.0.0 (Future)

**Advanced Features** (if needed):
- Bloom filter for O(1) existence checks
- Optional compression for large extractions
- Cache expiration policies
- Multi-tier storage (hot/cold)

## Technical Details

### Hash Generation

```python
def hash_file(file_path: str, digest_size: int = 32) -> str:
    """Generate SHAKE256 hash of file"""
    hasher = hashlib.shake_256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest(digest_size)[:16]
```

### Cache Key Format

```
{sanitized_filename}_{shake256_hash}
```

Examples:
- `NIST.SP.800-82r3_6d7b84bb7513d721`
- `CCMv4.0.12_Generated-at_2024-06-03_7eedad6154cbc160`
- `3-AcceptableUsePolicy_69461e394e52dd97`

### Performance

- Hash generation: ~0.117s for 1MB PDF
- Cache lookup: O(1) with manifest check
- Migration: Lazy (only when file accessed)

## Security Considerations

### What This Is NOT

- **Not encryption** - Cache is plain text
- **Not access control** - Files in cache are readable
- **Not secure storage** - Original files must remain secure

### What This IS

- **Content integrity** - SHAKE256 ensures cache matches source
- **Deduplication** - Same file = same cache key
- **Collision resistance** - Astronomically unlikely hash collisions

### Recommendations

1. **Don't cache sensitive documents** in shared/untrusted environments
2. **Original files are source of truth** - cache can be deleted anytime
3. **Cache location** should have appropriate file system permissions

## Troubleshooting

### Cache Not Found

If extraction always re-runs:
1. Check cache exists: `ls -la ~/.claude-cache/{doc_type}/`
2. Verify manifest: `cat ~/.claude-cache/{doc_type}/{cache_key}/manifest.json`
3. Force re-extract: Use `--force` flag

### Migration Issues

If old cache not migrating:
1. Check old location exists: `ls -la ~/.claude-{doc_type}-cache/`
2. Verify file unchanged: Hash must match
3. Manual migration: Move directory to new location

### Custom Location Not Working

Currently not supported in v2.0.0. Use default location or wait for v2.1.0.

## API Reference

### SmartCache Class

```python
class SmartCache:
    def __init__(self, doc_type: str, cache_dir: Optional[Path] = None):
        """
        Args:
            doc_type: 'pdf', 'xlsx', or 'docx'
            cache_dir: Optional custom cache directory
        """

    def get_cache_key(self, file_path: str) -> Tuple[str, Path]:
        """
        Generate cache key with SHAKE256, auto-migrate from SHA-256

        Returns:
            Tuple of (cache_key, cache_path)
        """

    def exists(self, cache_key: str) -> bool:
        """Check if cache exists"""

    def mark_cached(self, cache_key: str):
        """Mark cache key as cached (for Bloom filter)"""
```

## Changelog

### v2.0.0 (Current - October 2025)
- ✅ Unified cache directory: `~/.claude-cache/`
- ✅ SHAKE256 hashing (SHA-3 family)
- ✅ Automatic SHA-256 → SHAKE256 migration
- ✅ Zero external dependencies
- ✅ Integrated into pdf-smart-extractor
- ✅ Integrated into xlsx-smart-extractor
- ✅ Integrated into docx-smart-extractor

### v1.x (Legacy)
- Individual cache directories per extractor
- SHA-256 hashing
- No migration support

## Support

For questions or issues:
1. Check this document first
2. Review extractor-specific READMEs
3. File issue at repository

---

**Version:** 2.0.0
**Last Updated:** October 2025
**Status:** Production Ready
