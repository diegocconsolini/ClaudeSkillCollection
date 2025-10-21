# Changelog

All notable changes to the Excel Smart Extractor plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-21

### Changed
- **Unified Caching System** - Integrated shared `smart_cache.py` library
  - Replaced individual SHA-256 hashing with SHAKE256 (SHA-3 family)
  - Cache location moved: `~/.claude-xlsx-cache/` → `~/.claude-cache/xlsx/`
  - Automatic migration from old cache format
  - Consistent hashing across all smart-extractor plugins

### Added
- Automatic SHA-256 → SHAKE256 cache migration
- Lazy migration (only when files are accessed)
- Unified cache directory structure with PDF and DOCX extractors

### Fixed
- Removed custom `get_file_hash()` function (now uses smart_cache)
- Updated manifest to extract hash from cache_key

### Technical
- Uses shared `SmartCache` class from `/shared/smart_cache.py`
- Zero breaking changes - old caches automatically migrate
- See `/shared/CACHE_STRATEGY.md` for full documentation

### Performance
- Hash generation: Same performance as v1.0.0
- Cache lookup: Identical O(1) with manifest check
- Migration: One-time overhead only

---

## [1.0.0] - 2025-10-20

### Added
- **Initial Release** - Production-ready Excel workbook extraction and analysis plugin
- Local Excel extraction with zero LLM involvement using openpyxl library
- Lossless extraction including all cells, formulas, formatting, and metadata
- 20-100x token reduction through intelligent sheet-based chunking
- Three core scripts:
  - `extract_xlsx.py` - Full workbook extraction with formula and formatting preservation
  - `chunk_sheets.py` - Semantic chunking by sheets, column groups, and row ranges
  - `query_xlsx.py` - Efficient search and retrieval with relevance scoring
- Persistent caching mechanism (`~/.claude-xlsx-cache/`) for extract-once-query-forever workflow
- Support for .xlsx and .xlsm file formats
- Named range detection and extraction (tested with 91 named ranges)
- Merged cell handling
- Hyperlink and comment extraction
- Data validation rule detection
- Progress indicators for large files (>1000 rows)
- Comprehensive documentation (README.md, TEST_RESULTS.md, agent file)

### Features Tested
- **File Size Range:** 110KB - 1.5MB Excel files
- **Cell Processing:** 287,460 cells across 85 sheets
- **Formula Extraction:** 15,409 formulas including array formulas
- **Named Ranges:** 198 named ranges successfully extracted
- **Extraction Coverage:** All cells, formulas, formatting, merged cells, and named ranges
- **Token Reduction:** 4x - 58x (average 27.6x)
- **Extraction Speed:** 3-45 seconds depending on file complexity

### Bug Fixes (Discovered During Testing)
- **Bug #1:** Fixed RGB color object JSON serialization error
  - Added `serialize_color()` function to handle openpyxl color objects
  - Converts RGB objects and theme colors to JSON-serializable strings
- **Bug #2:** Fixed time/date object JSON serialization error
  - Enhanced `serialize_cell_value()` to handle datetime, date, and time objects
  - Converts temporal objects to ISO format strings using `.isoformat()`
- **Bug #3:** Fixed ArrayFormula object JSON serialization error
  - Added catch-all `str()` conversion for unknown object types
  - Handles Excel array formulas like `{=SUM(A1:A10*B1:B10)}`

### Tested Use Cases
- ✅ Compliance matrices (CCM v4.0.12, security questionnaires)
- ✅ Financial models (pricing sheets, operations financials, 19 sheets, 11K formulas)
- ✅ Security analysis reports (network transitions, security findings)
- ✅ Data analysis workbooks (consolidated data, audit logs)
- ✅ Macro-enabled workbooks (.xlsm with macros safely skipped)
- ✅ Unicode sheet names (emoji support verified)

### Code Review
- Comprehensive code review completed with production-ready assessment
- Security hardening recommended for:
  - Input validation for file paths
  - Path traversal sanitization in sheet names
  - Resource limits for very large files
- Performance optimizations identified for future releases

### Documentation
- Comprehensive README.md with Quick Start, Use Cases, and Performance Metrics
- Detailed TEST_RESULTS.md with anonymized test data from 9 real-world files
- Agent file (agents/xlsx-smart-extractor.md) with full capability documentation
- Code comments explaining bug fixes and design decisions

### Security
- Read-only file operations (never modifies original Excel files)
- VBA macros disabled (`keep_vba=False`) to prevent code execution
- No external network calls or API requests
- Local-only processing with persistent caching
- `.gitignore` configured to exclude test files from repository

### Known Limitations
- VBA macros not extracted (security by design)
- Pivot tables structure detected but not fully extracted
- Charts not extracted (recommend screenshot + description approach)
- External links noted but not followed
- Password-protected files cannot be opened
- Binary formats (.xls, .xlsb) not supported (convert to .xlsx first)

### Dependencies
- Python >=3.8
- openpyxl >=3.1.0
- pandas >=2.0.0 (listed but unused, may be removed in future release)

### Plugin Naming
- Plugin renamed from `xlsx-analyzer` to `xlsx-smart-extractor` to match naming convention of `pdf-smart-extractor`
- Agent file renamed: `agents/xlsx-analyzer.md` → `agents/xlsx-smart-extractor.md`
- All references updated in plugin.json, README.md, and documentation

### Test Data Anonymization
- All company names and vendor names anonymized in TEST_RESULTS.md
- Generic filenames used (ComplianceMatrix_v4, Pricing_Sheet_YYYY, etc.)
- Budget references anonymized (Budget_Plan_YYYY)
- System names replaced with generic identifiers

### Marketplace Integration
- Added to security-compliance-marketplace v1.4.0
- Category: productivity
- 14 keywords for discoverability
- Tested integration with existing marketplace plugins

---

## Future Enhancements (Planned)

### v1.1.0 (Planned)
- Add support for conditional formatting rules extraction
- Implement data validation dropdown list extraction
- Enhanced pivot table metadata extraction
- Chart metadata extraction (titles, axes labels, series names)

### v2.0.0 (Planned)
- Add automated unit tests with pytest
- Implement structured logging framework
- Replace manual `sys.argv` parsing with argparse
- Add Python type hints throughout codebase
- Support for custom cache directory via environment variable
- Improved column letter calculation for sheets >26 columns wide
- Consider faster JSON serialization with orjson
- Add regex pattern support in search queries
- Column-specific search functionality

### Potential Features
- Read-only mode for very large files (>10MB) to reduce memory usage
- Compression for cached files (gzip) to save disk space
- Fuzzy search and semantic search capabilities
- Export query results to various formats
- Diff functionality to compare two versions of same workbook

---

## Contributors
- Diego Consolini (diego@diegocon.nl) - Creator and maintainer

## License
MIT License - See LICENSE file for details

## Repository
https://github.com/diegocconsolini/ClaudeSkillCollection/tree/main/xlsx-smart-extractor
