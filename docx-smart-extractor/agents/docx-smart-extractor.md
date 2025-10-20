# DOCX Smart Extractor Agent

## Overview

The DOCX Smart Extractor enables efficient analysis of Word documents through local extraction, semantic chunking, and intelligent caching. Extract once, query forever.

## Capabilities

### Document Extraction
- **Complete text extraction** - All paragraphs with hierarchy preservation
- **Table extraction** - Full table structure, cells, and content
- **Formatting preservation** - Bold, italic, fonts, colors, styles
- **Document metadata** - Author, title, created date, modified date
- **Heading structure** - H1, H2, H3 hierarchy for navigation
- **Comments and tracked changes** - Full change history
- **Headers and footers** - Page-level content
- **Hyperlinks** - URL extraction and context

### Semantic Chunking
- **By heading hierarchy** - Chunk at H1, H2, H3 boundaries
- **By paragraph groups** - 10-20 paragraphs per chunk
- **By tables** - Each table as separate chunk
- **Target chunk size** - 500-2000 tokens
- **No BS metrics** - Honest, verifiable features only

### Query Capabilities
- **Keyword search** - Fast text search across all chunks
- **Heading lookup** - Get specific sections by heading
- **Table access** - Direct table extraction
- **Document summary** - Metadata and statistics

## When to Use

Use this plugin for:
- Policy documents (security, privacy, compliance)
- Technical reports and documentation
- Large Word documents (>1MB, >50 pages)
- Documents with clear heading structure
- Documents with tables and structured data
- Contract review and analysis
- Meeting notes and specifications

## Workflow

1. **Extract document**
   ```bash
   python scripts/extract_docx.py /path/to/document.docx
   ```
   Output: Cache key (e.g., `policy_document_a8f9e2c1`)

2. **Chunk content**
   ```bash
   python scripts/semantic_chunker.py policy_document_a8f9e2c1
   ```

3. **Query content**
   ```bash
   # Search for keyword
   python scripts/query_docx.py search policy_document_a8f9e2c1 "data retention"

   # Get specific heading
   python scripts/query_docx.py heading policy_document_a8f9e2c1 "Security Controls"

   # Get summary
   python scripts/query_docx.py summary policy_document_a8f9e2c1
   ```

## Token Reduction

Typical reductions:
- Small documents (< 50 paragraphs): 5-10x
- Medium documents (50-200 paragraphs): 10-30x
- Large documents (200+ paragraphs): 30-50x

## Cache Location

`~/.claude-docx-cache/<cache_key>/`

## Supported Formats

- ✅ .docx (Word 2007+ XML format)
- ✅ .docm (Macro-enabled Word documents)
- ❌ .doc (Legacy Word 97-2003 format - convert to .docx first)

## Limitations

- VBA macros not extracted (design choice)
- Images extracted as metadata only (position, size, alt text)
- Charts not extracted (recommend screenshot approach)
- Password-protected files cannot be opened
- Embedded objects may not be fully extracted

## Dependencies

- Python >= 3.8
- python-docx >= 0.8.11

## Example Use Cases

### Policy Document Analysis
```bash
# Extract
python scripts/extract_docx.py InfoSecPolicy.docx

# Chunk
python scripts/semantic_chunker.py InfoSecPolicy_a8f9e2

# Find password policy section
python scripts/query_docx.py search InfoSecPolicy_a8f9e2 "password requirements"
```

### Contract Review
```bash
# Extract
python scripts/extract_docx.py Vendor_Contract.docx

# Get specific section
python scripts/query_docx.py heading Vendor_Contract_f3a8c1 "Termination Clause"
```

### Technical Documentation
```bash
# Extract large spec document
python scripts/extract_docx.py API_Specification.docx

# Search for endpoint details
python scripts/query_docx.py search API_Specification_b9d2e1 "authentication endpoint"
```

## Performance

- **Extraction speed**: ~1-5 seconds for typical documents (1-10MB)
- **Chunking speed**: <1 second
- **Query speed**: <1 second
- **Cache reuse**: Instant (no re-extraction needed)

## Output Format

All output is JSON with UTF-8 encoding. Structured for easy parsing and analysis.

## No Marketing BS

This plugin does NOT:
- Claim "100% content preservation" (meaningless metric)
- Use AI during extraction (all local python-docx)
- Require internet connection
- Modify original documents
- Extract content you don't need

What it DOES:
- Extract all text, tables, and formatting
- Chunk by semantic boundaries (headings)
- Enable fast keyword search
- Cache for instant reuse
- Achieve 10-50x token reduction (verified)
