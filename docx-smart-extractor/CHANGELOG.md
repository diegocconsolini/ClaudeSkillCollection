# Changelog

All notable changes to the DOCX Smart Extractor plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-21

### Changed
- **Unified Caching System** - Integrated shared `smart_cache.py` library
  - Replaced MD5 hashing with SHAKE256 (SHA-3 family)
  - Cache location moved: `~/.claude-docx-cache/` → `~/.claude-cache/docx/`
  - Automatic migration from old cache format
  - Consistent hashing across all smart-extractor plugins

### Added
- Automatic MD5 → SHAKE256 cache migration
- Lazy migration (only when files are accessed)
- Unified cache directory structure with PDF and XLSX extractors

### Removed
- Custom `generate_cache_key()` function (now uses smart_cache)
- Custom `get_cache_dir()` function (now uses smart_cache)

### Technical
- Uses shared `SmartCache` class from `/shared/smart_cache.py`
- Zero breaking changes - old caches automatically migrate
- See `/shared/CACHE_STRATEGY.md` for full documentation

### Performance
- Hash generation: Fast for typical DOCX files (40-500KB)
- Cache lookup: Identical O(1) with manifest check
- Migration: One-time overhead only

### Tested With
- Policy documents (40-80KB, 50-60 paragraphs)
- Multi-page documents with tables
- Documents with formatting (bold, italic, colors)

---

## [1.0.0] - 2025-10-19

### Added
- **Initial Release** - Production-ready Word document extraction plugin
- Local DOCX extraction with zero LLM involvement using python-docx
- Complete content extraction:
  - Text content with full hierarchy (headings, paragraphs, lists)
  - Tables with structure and formatting
  - Images metadata (size, position, description)
  - Document properties (author, created date, modified date)
  - Styles and formatting (bold, italic, fonts, colors)
  - Comments and tracked changes
  - Headers and footers
  - Hyperlinks
- Persistent caching mechanism (`~/.claude-docx-cache/`)
- Support for .docx and .docm file formats
- Comprehensive documentation (README.md, agent file)

### Features
- Extract-once-query-forever workflow
- MD5 hash-based cache keys
- Lossless extraction of text and formatting
- Structured paragraph and table data (JSON format)
- Run-level formatting preservation

### Performance
- Fast extraction (seconds for typical documents)
- Efficient caching
- Token-efficient output format

### Security
- Read-only operations
- Local-only processing
- No network calls
- VBA macros safely skipped

---

## Future Enhancements

### v2.1.0 (Planned)
- Environment variable support: `CLAUDE_CACHE_DIR`
- Config file support for cache location
- Semantic chunking for large documents

### v2.2.0 (Planned)
- MCP cache management server
- Cache browsing and statistics
- Query interface for extracted content

### v3.0.0 (Future)
- Chart metadata extraction
- Drawing object extraction
- SmartArt extraction
- Custom XML parts extraction

---

## Contributors
- Diego Consolini (diego@diegocon.nl) - Creator and maintainer

## License
MIT License - See LICENSE file for details

## Repository
https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/docx-smart-extractor
