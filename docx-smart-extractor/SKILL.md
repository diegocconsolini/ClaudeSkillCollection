---
name: docx-smart-extractor
description: Use this skill to extract and analyze large Word documents (1MB-50MB+) with minimal token usage. Losslessly extracts text, tables, formatting, and structure while achieving 10-50x token reduction through local extraction, semantic chunking by headings, and intelligent caching. Use when a .docx is too large for the context window (policies, contracts, technical reports).
license: MIT
---

# Word Smart Extractor Skill

Extract once locally, query forever. Chunks by heading hierarchy (H1/H2/H3) so you load
only the relevant sections.

## Usage

```bash
# 1. Extract (one-time, local — caches to ~/.claude-cache/docx/)
python scripts/extract_docx.py document.docx

# 2. Chunk by headings
python scripts/semantic_chunker.py {cache_key}

# 3. Query
python scripts/query_docx.py search {cache_key} "your query"
python scripts/query_docx.py heading {cache_key} "Section Title"
python scripts/query_docx.py list
```

Requires `python-docx>=1.1.0`. Cache lives in `~/.claude-cache/docx/`; extract, chunk, and
query all resolve to that same location via the shared `smart_cache` library.
