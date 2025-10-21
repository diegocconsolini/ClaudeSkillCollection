# Changelog

All notable changes to the PDF Smart Extractor plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-21

### Changed
- **Unified Caching System** - Integrated shared `smart_cache.py` library
  - Replaced individual SHA-256 hashing with SHAKE256 (SHA-3 family)
  - Cache location moved: `~/.claude-pdf-cache/` → `~/.claude-cache/pdf/`
  - Automatic migration from old cache format
  - Consistent hashing across all smart-extractor plugins

### Added
- Automatic SHA-256 → SHAKE256 cache migration
- Lazy migration (only when files are accessed)
- Unified cache directory structure with XLSX and DOCX extractors

### Fixed
- Removed custom `get_pdf_hash()` function (now uses smart_cache)
- Updated manifest to extract hash from cache_key

### Technical
- Uses shared `SmartCache` class from `/shared/smart_cache.py`
- Zero breaking changes - old caches automatically migrate
- See `/shared/CACHE_STRATEGY.md` for full documentation

### Performance
- Hash generation: 0.117s for 1MB PDF (tested with NIST.IR.8228.pdf)
- Cache lookup: Identical O(1) with manifest check
- Migration: One-time overhead only

### Tested With
- Basic PDFs (400KB - 1MB)
- Large PDFs (8.2MB, 316 pages - 10MB, 45 pages)
- Password-protected PDFs with CLI password support
- Edge cases: Non-existent files, corrupted PDFs
- SHA-256 cache migration from v1.1.0

---

## [1.1.0] - 2025-10-20

### Added
- **Password-protected PDF support**
  - Interactive password prompt using `getpass.getpass()`
  - CLI password argument: `--password PASSWORD`
  - 3 password attempt limit for interactive mode
  - Secure password input (hidden from terminal)

### Security
- Password never stored in cache
- Interactive prompt more secure than CLI argument
- CLI password available for automation

### Documentation
- Added PASSWORD_PROTECTION_TEST_LOG.md
- Added EDGE_CASES_PASSWORDS.md
- Updated README with password examples

---

## [1.0.0] - 2025-10-19

### Added
- **Initial Release** - Production-ready PDF extraction plugin
- Local PDF extraction with zero LLM involvement using PyMuPDF
- Complete content extraction:
  - Full text content with page structure
  - Document metadata (author, title, creation date)
  - Table of contents (if available)
  - Page dimensions
- Persistent caching mechanism (`~/.claude-pdf-cache/`)
- Support for all PDF versions
- Progress indicators for large files
- Comprehensive documentation (README.md, agent file)

### Features
- Extract-once-query-forever workflow
- SHA-256 hash-based cache keys
- Full text preservation
- Structured page data (JSON format)
- Metadata extraction

### Performance
- Fast extraction (seconds for most PDFs)
- Efficient caching
- Token-efficient output format

### Security
- Read-only operations
- Local-only processing
- No network calls

---

## Future Enhancements

### v2.1.0 (Planned)
- Environment variable support: `CLAUDE_CACHE_DIR`
- Config file support for cache location
- Improved error messages for corrupted PDFs

### v2.2.0 (Planned)
- MCP cache management server
- Cache browsing and statistics
- Cache cleanup utilities

### v3.0.0 (Future)
- OCR support for scanned PDFs
- Image extraction
- Form field extraction
- Annotation extraction

---

## Contributors
- Diego Consolini (diego@diegocon.nl) - Creator and maintainer

## License
MIT License - See LICENSE file for details

## Repository
https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/pdf-smart-extractor
