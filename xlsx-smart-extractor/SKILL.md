---
name: xlsx-smart-extractor
description: Use this skill to extract and analyze large Excel workbooks (1MB-50MB+) with minimal token usage. Losslessly extracts formulas, cell formatting, and complex tables while achieving 20-100x token reduction through local extraction, semantic chunking, and intelligent caching. Use when an .xlsx is too large for the context window (compliance matrices, financial models, audit logs).
license: MIT
---

# Excel Smart Extractor Skill

Extract once locally, query forever. Reduces token cost by loading only the relevant
sheets/columns instead of an entire workbook.

## Usage

```bash
# 1. Extract (one-time, local — caches to ~/.claude-cache/xlsx/)
python scripts/extract_xlsx.py workbook.xlsx

# 2. Chunk the extracted content
python scripts/chunk_sheets.py {cache_key}

# 3. Query / list
python scripts/query_xlsx.py search {cache_key} "your query"
python scripts/query_xlsx.py list
```

Requires `openpyxl`. Cache lives in `~/.claude-cache/xlsx/`; extract, chunk, and query all
resolve to that same location via the shared `smart_cache` library.
