# Smart Cache - Changelog

All notable changes to the smart-extractor series unified caching system will be documented in this file.

## [2.0.0] - 2025-10-21

### Added
- **Unified SmartCache library** (`smart_cache.py`) for consistent caching across all extractors
- **SHAKE256 hashing** (SHA-3 family, NIST FIPS 202) for cache key generation
- **Automatic cache migration** from SHA-256 to SHAKE256
- **Zero external dependencies** - uses only Python stdlib
- **Unified cache directory** structure: `~/.claude-cache/{doc_type}/`
- **Migration detection** for old cache locations (`.claude-{type}-cache/`)
- **BloomFilter class** for optional O(1) cache existence checks
- **Post QuantumHash class** with SHAKE256 and SHA-256 support
- Comprehensive documentation in `CACHE_STRATEGY.md`
- Test suites: `test_smart_cache.py` and `test_real_pdf.py`

### Changed
- **Hash algorithm**: SHA-256 → SHAKE256 (16-char hex output)
- **Cache location**: Individual dirs → Unified `~/.claude-cache/`
- **Cache key format**: More consistent across extractors
- **Migration strategy**: Lazy migration on file access

### Fixed
- **Home directory pollution**: Reduced from 4 dotdirs to 1
- **Backup inefficiency**: Cache now in single discoverable location
- **Inconsistent hashing**: All extractors use same algorithm

### Performance
- **Hash generation**: 0.117s for 1MB PDF (tested with NIST.IR.8228.pdf)
- **Cache lookup**: O(1) with manifest check
- **Migration overhead**: One-time per old cache

### Security
- **IMPORTANT**: SHAKE256 provides content integrity, NOT encryption
- Cache files are plain text and readable
- Original document security is user's responsibility
- See `CACHE_STRATEGY.md` for security recommendations

### Migration Guide

**From v1.x:**
1. No action required - migration is automatic
2. Old caches detected and moved to new location
3. Hash recalculated with SHAKE256
4. Old directories can be manually removed after migration

**Testing migration:**
```bash
# Check old cache exists
ls -la ~/.claude-pdf-cache/

# Run extraction (triggers migration)
python scripts/extract_pdf.py document.pdf

# Verify migration
ls -la ~/.claude-cache/pdf/

# Old cache should be moved
ls -la ~/.claude-pdf-cache/  # Should be empty or not exist
```

### Breaking Changes
None - v1.x caches automatically migrate

### Dependencies
- Python 3.7+ (for `hashlib.shake_256`)
- No external packages required

### Tested With
- pdf-smart-extractor v1.1.0 → v2.0.0
- xlsx-smart-extractor v1.0.0 → v2.0.0
- docx-smart-extractor v1.0.0 → v2.0.0

### Known Issues
None

### Future Plans (v2.1.0+)
- Environment variable support (`CLAUDE_CACHE_DIR`)
- Config file support
- MCP cache management server
- Platform-specific cache locations (optional)

---

## [1.0.0] - 2024-10-20

### Initial Implementations
- Individual cache systems per extractor
- SHA-256 hashing
- Separate cache directories:
  - `~/.claude-pdf-cache/`
  - `~/.claude-xlsx-cache/`
  - `~/.claude-docx-cache/`

---

**Legend:**
- Added: New features
- Changed: Changes in existing functionality
- Deprecated: Soon-to-be removed features
- Removed: Removed features
- Fixed: Bug fixes
- Security: Security improvements
