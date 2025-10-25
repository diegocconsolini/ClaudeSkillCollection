# DOCX Smart Extractor - Claude Code Plugin

**Extract and analyze Word documents with lossless extraction and 10-50x token reduction**

## Overview

DOCX Smart Extractor solves the "Word document too large" problem by extracting content locally (including text, tables, and formatting), chunking it by heading hierarchy, and enabling efficient querying. This plugin is designed for policy documents, technical reports, contracts, and any large Word document that exceeds LLM context windows.

### Key Features

- **Lossless Extraction** - Extracts all text, tables, formatting, headings, and metadata
- **10-50x Token Reduction** - Load only relevant sections, not entire documents
- **Semantic Chunking** - Intelligent splitting by heading hierarchy (H1, H2, H3)
- **Table Extraction** - Full table structure and content
- **Persistent Caching** - Extract once, query forever
- **No LLM Involvement** - Extraction happens entirely on your machine
- **Efficient Search** - Keyword-based chunk retrieval with relevance scoring
- **Heading Navigation** - Direct access to specific sections

## Installation

### Prerequisites

- Python 3.8 or higher
- python-docx library

### Option 1: Using Virtual Environment (Recommended for Isolation)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: System-Wide Installation

```bash
# Install from requirements.txt
pip install -r requirements.txt

# OR install individually
pip install python-docx>=0.8.11
```

### Verify Installation

```bash
python3 -c "import docx; print('python-docx version:', docx.__version__)"
```

### Troubleshooting

**Error: `ModuleNotFoundError: No module named 'docx'`**
- Make sure you've installed dependencies: `pip install -r requirements.txt`
- If using venv, ensure it's activated: `source venv/bin/activate`
- Check Python version: `python3 --version` (must be 3.8+)

**Error: `externally-managed-environment`**
- Use virtual environment (Option 1 above)
- OR use `pipx` for application installation
- OR use `--break-system-packages` flag (not recommended)

## Quick Start

### 1. Extract a Word Document

```bash
python scripts/extract_docx.py /path/to/document.docx
```

**Output:**
```
Extracting Word document: InfoSecPolicy.docx
File size: 2.50 MB
Extracting 245 paragraphs...

Extraction complete!
Cache key: InfoSecPolicy_a8f9e2c1
Cache location: /Users/you/.claude-cache/docx/InfoSecPolicy_a8f9e2c1
Total paragraphs: 245
Total tables: 12
Total sections: 8
Total characters: 125,430

Next step:
Chunk content: python scripts/semantic_chunker.py InfoSecPolicy_a8f9e2c1
```

### 2. Chunk the Document

```bash
python scripts/semantic_chunker.py InfoSecPolicy_a8f9e2c1
```

**Output:**
```
Chunking document: InfoSecPolicy.docx
Paragraphs: 245
Tables: 12
  Strategy: Chunk by headings (42 headings)
  Created chunk 1: 1. Introduction (890 tokens)
  Created chunk 2: 2. Scope and Purpose (720 tokens)
  Created chunk 3: 3. Password Policy (1450 tokens)
  ...

Chunking complete!
Total chunks: 54
Total tokens: 62,500
Avg tokens/chunk: 1,157

Chunk types:
  - paragraphs: 42
  - table: 12
```

### 3. Query Document Content

#### Search by Keyword

```bash
python scripts/query_docx.py search InfoSecPolicy_a8f9e2c1 "password policy"
```

**Output:**
```
Searching 54 chunks for: 'password policy'

Found 2 result(s):

1. Chunk 3 - 3. Password Policy
   Type: paragraphs
   Relevance: 100%
   Matches: 12
   Tokens: 1,450
   Sample: All users must adhere to the following password requirements: minimum 12 characters, combination of uppercase, lowercase, numbers, and special characters...

2. Chunk 15 - 7.2 Authentication Standards
   Type: paragraphs
   Relevance: 30%
   Matches: 3
   Tokens: 820
   Sample: Authentication mechanisms must comply with password policy requirements defined in Section 3...

Total tokens for displayed results: 2,270
```

#### Get Specific Heading

```bash
python scripts/query_docx.py heading InfoSecPolicy_a8f9e2c1 "Data Classification"
```

**Output:**
```
Heading: 5. Data Classification
Type: paragraphs
Tokens: 1,120

Data must be classified according to sensitivity levels:

1. Public - Information intended for public disclosure
2. Internal - Information for internal use only
3. Confidential - Sensitive business information
4. Restricted - Highly sensitive information requiring strict access controls
...
```

#### Get Document Summary

```bash
python scripts/query_docx.py summary InfoSecPolicy_a8f9e2c1
```

**Output:**
```
============================================================
Document Summary
============================================================
Filename: InfoSecPolicy.docx
File size: 2.50 MB
Author: Security Team
Title: Information Security Policy
Created: 2024-01-15T10:30:00
Modified: 2025-10-18T14:22:00

Total paragraphs: 245
Total tables: 12
Total sections: 8
Total characters: 125,430

Chunking Statistics:
  Total chunks: 54
  Total tokens: 62,500
  Avg tokens/chunk: 1,157

Chunk types:
  - paragraphs: 42
  - table: 12

Extracted: 2025-10-20T15:30:45.123456
============================================================
```

## Use Cases

### 1. Policy Document Analysis

**Scenario:** Information Security Policy with 50 pages, 8 sections, multiple tables

**Workflow:**
```bash
# Extract document
python scripts/extract_docx.py InfoSecPolicy.docx

# Chunk for efficient querying
python scripts/semantic_chunker.py InfoSecPolicy_a8f9e2

# Find specific policy
python scripts/query_docx.py search InfoSecPolicy_a8f9e2 "access control"

# Get specific section
python scripts/query_docx.py heading InfoSecPolicy_a8f9e2 "Incident Response"
```

**Benefits:**
- Find specific policies in seconds (vs reading 50-page document)
- Extract only relevant sections (20x token reduction)
- Navigate by heading structure

### 2. Contract Review

**Scenario:** Vendor contract with complex terms, 30 pages

**Workflow:**
```bash
# Extract contract
python scripts/extract_docx.py Vendor_Contract.docx

# Get summary to understand structure
python scripts/query_docx.py summary Vendor_Contract_f3a8c1

# Find specific clauses
python scripts/query_docx.py search Vendor_Contract_f3a8c1 "termination"

# Get section directly
python scripts/query_docx.py heading Vendor_Contract_f3a8c1 "Payment Terms"
```

**Benefits:**
- Quickly locate specific clauses
- Review section-by-section
- Compare multiple contracts efficiently

### 3. Technical Documentation

**Scenario:** API specification document, 100 pages, well-structured with headings

**Workflow:**
```bash
# Extract specification
python scripts/extract_docx.py API_Spec.docx

# Search for endpoints
python scripts/query_docx.py search API_Spec_b9d2e1 "authentication endpoint"

# Get specific API section
python scripts/query_docx.py heading API_Spec_b9d2e1 "REST API Reference"
```

**Benefits:**
- Navigate large specs quickly
- Find specific API details
- Extract relevant sections for implementation

## Architecture

### Extraction Phase (extract_docx.py)

**What's Extracted:**
- Paragraph text with full hierarchy
- Paragraph styles (Heading 1, Heading 2, Normal, etc.)
- Text runs with formatting (bold, italic, fonts, colors)
- Tables with full structure (rows, columns, cells)
- Document metadata (author, title, created/modified dates)
- Alignment and paragraph properties

**What's Not Extracted:**
- VBA macros (security risk)
- Images (metadata only: size, position, description)
- Charts (not supported by python-docx)
- Embedded objects
- Drawing shapes

**Performance:**
- 1MB document: ~2-3 seconds
- 5MB document: ~5-10 seconds
- 10MB document: ~15-20 seconds
- Cache reuse: <1 second

### Chunking Phase (semantic_chunker.py)

**Strategies:**
1. **Small documents (<50 paragraphs):** Single chunk
2. **Structured documents (>3 headings):** Chunk by heading hierarchy
3. **Unstructured documents:** Chunk by paragraph ranges (15 paragraphs per chunk)
4. **Tables:** Always separate chunks

**Token Estimation:**
- Rough approximation: character count / 4
- Actual tokens depend on model (Claude uses different tokenizer than GPT)

**Chunking Overhead:**
- Target chunk size: 500-2000 tokens
- Heading context preserved in each chunk
- Tables extracted as independent chunks

### Query Phase (query_docx.py)

**Query Types:**
1. **search:** Keyword search across all chunks
2. **heading:** Get specific section by heading
3. **summary:** Get document metadata and statistics

**Relevance Scoring:**
- Simple algorithm: match count * 10 (capped at 100%)
- Sorts results by relevance and match count

## Performance Metrics

### Token Reduction

| Document Size | Full Tokens | Query Tokens | Reduction |
|---------------|-------------|--------------|-----------|
| 1MB (50 pages) | 25,000 | 2,500 | 10x |
| 5MB (200 pages) | 125,000 | 4,000 | 31x |
| 10MB (400 pages) | 250,000 | 5,000 | 50x |

### Extraction Speed

| File Size | Extraction Time | Cache Reuse |
|-----------|----------------|-------------|
| 1MB | ~3 sec | <1 sec |
| 5MB | ~10 sec | <1 sec |
| 10MB | ~20 sec | <1 sec |

## Comparison

### vs. Loading Full DOCX in LLM Context

| Aspect | docx-smart-extractor | Full Loading |
|--------|---------------------|--------------|
| Token usage | 10-50x less | Full document |
| Speed | 10-30x faster | All tokens processed |
| Cost | 10-50x cheaper | Full token cost |
| File size limit | No limit | 1-2MB practical limit |
| Heading navigation | Yes | No |
| Table extraction | Yes | Limited |

### vs. Direct python-docx Usage

| Feature | docx-smart-extractor | python-docx |
|---------|---------------------|-------------|
| Semantic chunking | Yes | Manual coding required |
| Cached extraction | Yes | Re-extract every time |
| Heading-based chunks | Automatic | Manual implementation |
| Query interface | Built-in | Custom code needed |
| Token optimization | Built-in | No optimization |

## Limitations

1. **VBA Macros:** Not extracted or executed (security risk)
2. **Images:** Metadata only (position, size, description)
3. **Charts:** Not supported (python-docx limitation)
4. **Embedded Objects:** May not be fully extracted
5. **Password Protection:** Cannot open protected files
6. **Legacy Formats:** .doc not supported (convert to .docx first)

## Supported Formats

- ✅ .docx (Word 2007+ XML format)
- ✅ .docm (Macro-enabled Word documents)
- ❌ .doc (Word 97-2003 binary format - use Word to convert)

## Troubleshooting

### "Module not found: docx"

```bash
pip3 install python-docx
```

### "Permission denied" when creating cache

```bash
chmod 755 ~/.claude-cache/docx/
```

### "Document is password protected"

python-docx cannot open password-protected files. Remove protection first:
1. Open in Word
2. File → Info → Protect Document → Encrypt with Password
3. Remove password and save

### Extraction slow (>1 minute for 5MB file)

**Possible causes:**
- Very large tables (1000+ rows)
- Complex formatting
- Embedded objects

**Solution:** Check document structure, consider splitting into smaller files

## Cache Management

### Cache Location

```
~/.claude-cache/docx/
  ├── DocumentName_a8f9e2c1/
  │   ├── metadata.json
  │   ├── manifest.json
  │   ├── content.json
  │   └── chunks/
  │       ├── index.json
  │       ├── chunk_001.json
  │       ├── chunk_002.json
  │       └── ...
```

### Cache Size

- Cache size: ~2-3x original file size
- Example: 5MB Word doc → 10-15MB cache

### Clear Cache

```bash
# Remove all caches
rm -rf ~/.claude-cache/docx/

# Remove specific cache
rm -rf ~/.claude-cache/docx/DocumentName_a8f9e2c1/
```

### Force Re-extraction

```bash
python scripts/extract_docx.py /path/to/document.docx --force
```

## Security

- **Read-only access** - Never modifies original files
- **No macro execution** - VBA macros not extracted or executed
- **Local processing** - No network requests, no LLM calls during extraction
- **No external connections** - All processing local

## Advanced Usage

### Extract Multiple Documents

```bash
# Extract all Word files in directory
for file in /path/to/docs/*.docx; do
    python scripts/extract_docx.py "$file"
done
```

### Batch Query

```bash
# Search multiple documents
for cache_key in Policy_* Contract_* Spec_*; do
    echo "Searching: $cache_key"
    python scripts/query_docx.py search "$cache_key" "compliance"
done
```

## Contributing

Found a bug or have a feature request? Please open an issue at:
https://github.com/diegocconsolini/ClaudeSkillCollection/issues

## License

MIT License - see LICENSE file for details

## References

- **python-docx Documentation:** https://python-docx.readthedocs.io/
- **Office Open XML (OOXML):** https://docs.microsoft.com/en-us/openspecs/office_standards/

## Version History

See [CHANGELOG.md](./CHANGELOG.md) for complete version history.

### v2.0.0 (Current)
- **Unified Caching System** - Integrated shared `smart_cache.py` library
- **SHAKE256 hashing** (SHA-3 family) replacing MD5
- **Automatic cache migration** from v1.x format
- **New cache location**: `~/.claude-cache/docx/` (migrated from `~/.claude-docx-cache/`)
- Consistent hashing across all smart-extractor plugins

### v1.0.0
- Initial release
- Lossless extraction of Word documents (text, tables, formatting)
- 10-50x token reduction through semantic chunking by headings
- Persistent caching system
- Support for .docx and .docm formats

**Last Updated:** October 2025
**Author:** Diego Consolini (diego@diegocon.nl)
