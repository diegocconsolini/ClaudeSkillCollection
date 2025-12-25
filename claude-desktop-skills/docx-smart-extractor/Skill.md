---
name: docx-smart-extractor
description: Process Word documents (1MB-50MB+) with token optimization through local extraction and caching. Preserves formatting, tables, and document structure for policy analysis, contract review, and technical reports.
license: MIT
compatibility: claude-desktop
metadata:
  version: 2.2.0
  author: Diego Consolini
  category: productivity
  runtime: python3
  dependencies: requirements.txt
---

# Word Document Analyzer

## When to Use This Skill

Use this skill when:
- User provides a Word document path (.docx, .docm) with size >500KB
- User encounters "document too large" or token limit errors
- User needs to analyze policy documents, contracts, or technical reports
- User wants to extract tables, headings, or document structure
- User needs to query specific sections by heading
- User is working with documents with clear heading hierarchy (H1, H2, H3)

## Capabilities

### 1. Local Document Extraction (Zero LLM Involvement)
- Extract all paragraphs with hierarchy preservation
- Capture full table structure, cells, and content
- Preserve formatting (bold, italic, fonts, colors, styles)
- Extract document metadata (author, title, created date, modified date)
- Extract heading structure (H1, H2, H3 hierarchy)
- Capture comments and tracked changes
- Extract headers and footers
- Preserve hyperlinks with context
- Cache extraction for instant reuse

### 2. Semantic Chunking by Headings
- Intelligent chunking by:
  - Heading hierarchy (H1, H2, H3 boundaries)
  - Paragraph groups (10-20 paragraphs per chunk)
  - Individual tables (each table as separate chunk)
  - Target chunk size: 500-2000 tokens
- Preserve document structure across chunks
- Maintain heading context for navigation
- Content preservation >99%

### 3. Efficient Querying
- Search by:
  - Keywords and phrases
  - Heading names (direct section access)
  - Table content
  - Document metadata
- Filter by:
  - Heading level (H1, H2, H3)
  - Content type (paragraphs, tables, metadata)
- 10-50x token reduction vs full document
- Results include heading path and chunk references

### 4. Structure Analysis
- Detect document structure:
  - Heading hierarchy and outline
  - Table of contents (if present)
  - Number of paragraphs and tables
  - Document length and complexity
- Generate document summary:
  - Key sections and headings
  - Table locations and content
  - Formatting patterns
  - Metadata overview

### 5. Table Extraction
- Extract complete table structure
- Preserve cell values and formatting
- Maintain row/column relationships
- Support merged cells
- Export tables separately for analysis

### 6. Persistent Caching (v2.0.0 Unified System)

**⚠️ IMPORTANT: Cache Location**

Extracted content is stored in a **user cache directory**, NOT the working directory:

**Cache locations by platform:**
- **Linux/Mac:** `~/.claude-cache/docx/{document_name}_{hash}/`
- **Windows:** `C:\Users\{username}\.claude-cache\docx\{document_name}_{hash}\`

**Why cache directory?**
1. **Persistent caching:** Extract once, query forever - even across different projects
2. **Cross-project reuse:** Same document analyzed from different projects uses the same cache
3. **Performance:** Subsequent queries are instant (no re-extraction needed)
4. **Token optimization:** 10-50x reduction by loading only relevant sections

**Cache contents:**
- `full_document.json` - Complete document text with formatting
- `headings.json` - Document heading structure
- `tables.json` - Extracted tables
- `metadata.json` - Document metadata
- `manifest.json` - Cache manifest

**Accessing cached content:**
```bash
# List all cached documents
python scripts/query_docx.py list

# Query cached content
python scripts/query_docx.py search {cache_key} "search query"

# Find cache location (shown in extraction output)
# Example: ~/.claude-cache/docx/policy_document_a1b2c3d4/
```

**To extract files to working directory:**
```bash
# Option 1: Use --output-dir flag during extraction
python3 scripts/extract_docx.py document.docx --output-dir ./extracted

# Option 2: Copy from cache manually
cp -r ~/.claude-cache/docx/{cache_key}/* ./extracted_content/
```

**Note:** Cache is local and not meant for version control. Keep original Word files in the repository and extract locally on each development machine (one-time operation).

## Workflow

### Step 1: Extract Word Document
```bash
# Extract to cache (default)
python3 scripts/extract_docx.py /path/to/document.docx

# Extract and copy to working directory (interactive prompt)
python3 scripts/extract_docx.py /path/to/document.docx
# Will prompt: "Copy files? (y/n)"
# Will ask: "Keep cache? (y/n)"

# Extract and copy to specific directory (no prompts)
python3 scripts/extract_docx.py /path/to/document.docx --output-dir ./extracted
```

**What happens:**
1. Open document with python-docx
2. Extract metadata (author, title, created date, modified date)
3. Iterate through all document elements:
   - Extract paragraphs with formatting
   - Extract tables with structure
   - Extract headings and hierarchy
   - Extract comments and tracked changes
4. Extract headers, footers, and hyperlinks
5. Close document and save to cache (~/.claude-cache/docx/)
6. Return cache key (e.g., `policy_document_a8f9e2c1`)

**Output files:**
- `full_document.json` - All content with formatting
- `headings.json` - Heading structure and hierarchy
- `tables.json` - All tables extracted
- `metadata.json` - Document metadata
- `manifest.json` - Extraction summary

**Performance:**
- 1MB document: ~2-5 seconds
- 10MB document: ~10-20 seconds
- 50MB document: ~1-2 minutes
- Cache reuse: <1 second

### Step 2: Chunk Document Content
```bash
python3 scripts/semantic_chunker.py <cache_key>
```

**What happens:**
1. Load extracted document data
2. Analyze heading structure and hierarchy
3. Create chunks based on:
   - Heading boundaries (H1, H2, H3 sections)
   - Paragraph groups (10-20 paragraphs)
   - Individual tables (each table = chunk)
4. Balance chunk sizes (target: 500-2000 tokens)
5. Save chunk index and individual chunk files

**Output files:**
- `chunks/index.json` - Chunk metadata and locations
- `chunks/chunk_001.json` - Individual chunk data
- `chunks/chunk_002.json` - ...

**Statistics:**
- Content preservation: >99%
- Avg tokens per chunk: 500-2000
- Token reduction: 10-50x

### Step 3: Query Document Content
```bash
# Search by keyword
python3 scripts/query_docx.py search <cache_key> "password policy"

# Get specific heading
python3 scripts/query_docx.py heading <cache_key> "Security Controls"

# Get document summary
python3 scripts/query_docx.py summary <cache_key>

# List all headings
python3 scripts/query_docx.py list <cache_key>
```

**What happens:**
1. Load chunk index
2. Filter chunks based on query:
   - Keyword search: scan all chunks for text matches
   - Heading query: return chunks under that heading
   - Summary: return metadata and structure
3. Return matching chunks with:
   - Heading path (e.g., "Security Policy > Access Control")
   - Chunk content
   - Token count
   - Match relevance score

**Results format:**
```
Found 2 result(s) for query: "password policy"

1. Heading: Security Policy > Password Requirements
   Relevance: 100%
   Content:
     All user passwords must meet the following criteria:
     - Minimum 12 characters
     - Mixed case letters
     - At least one number
     - At least one special character
   Tokens: 65

2. Heading: Implementation Guidelines > Password Storage
   Relevance: 85%
   Content:
     Passwords must be stored using bcrypt hashing...
   Tokens: 45

Total tokens: 110 (vs 12,500 full document = 113x reduction)
```

## Use Cases

### 1. Policy Document Analysis
**Scenario:** Information Security Policy (2MB, 50 pages, 20 sections)

**Workflow:**
1. Extract document: `python3 scripts/extract_docx.py InfoSecPolicy.docx`
2. Query specific section: `python3 scripts/query_docx.py heading InfoSecPolicy_a8f9e2 "Access Control"`
3. Search for requirements: `python3 scripts/query_docx.py search InfoSecPolicy_a8f9e2 "password requirements"`

**Benefits:**
- Find specific policy sections in seconds
- Extract only relevant sections (10x token reduction)
- Preserve formatting and structure

### 2. Contract Review
**Scenario:** Vendor contract (5MB, 100 pages, complex terms)

**Workflow:**
1. Extract contract: `python3 scripts/extract_docx.py Vendor_Contract.docx`
2. Get termination clause: `python3 scripts/query_docx.py heading Vendor_Contract_f3a8c1 "Termination"`
3. Search for liability: `python3 scripts/query_docx.py search Vendor_Contract_f3a8c1 "liability limitation"`

**Benefits:**
- Navigate to specific clauses instantly
- Review terms without reading entire contract
- Extract tables (pricing, deliverables, etc.)

### 3. Technical Documentation
**Scenario:** API specification (10MB, 200 pages, detailed endpoints)

**Workflow:**
1. Extract specification: `python3 scripts/extract_docx.py API_Specification.docx`
2. Get summary: `python3 scripts/query_docx.py summary API_Specification_b9d2e1`
3. Search endpoints: `python3 scripts/query_docx.py search API_Specification_b9d2e1 "authentication endpoint"`

**Benefits:**
- Understand document structure quickly
- Find specific endpoints and parameters
- Extract code examples and tables

## Technical Details

### Supported Formats
- .docx (Word 2007+ XML format)
- .docm (Macro-enabled Word documents)

**Not supported:**
- .doc (Word 97-2003 binary format - convert to .docx first)

### Data Extraction Details

**Paragraphs:**
- Plain text content
- Formatting (bold, italic, underline, strikethrough)
- Font name, size, color
- Alignment (left, center, right, justify)
- Indentation and spacing

**Tables:**
- Cell values (text and numbers)
- Cell formatting
- Merged cells
- Row/column structure
- Table position in document

**Headings:**
- Heading text
- Heading level (H1, H2, H3, etc.)
- Outline hierarchy
- Parent-child relationships

**Metadata:**
- Document title and subject
- Author and company
- Created date and modified date
- Last modified by
- Revision number
- Total editing time

### Chunking Strategy

**By Heading Hierarchy:**
- H1 sections → Major chunks
- H2 subsections → Medium chunks
- H3 subsections → Small chunks
- Preserve parent heading context

**By Paragraph Groups:**
- Group 10-20 paragraphs together
- Maintain reading flow
- Balance chunk sizes

**By Tables:**
- Each table as separate chunk
- Include preceding context paragraph
- Preserve table structure

### Token Estimation

Tokens estimated using character count / 4 (approximation):
- Paragraph text: ~1 token per word
- Table cells: ~1 token per cell value
- Formatting: ~0.5 tokens per attribute
- Headings: ~1 token per word

**Actual token usage** may vary with model (Claude uses different tokenizer than GPT).

## Error Handling

### Common Errors

**1. File Not Found**
```
Error: Document file not found: /path/to/file.docx
```
**Solution:** Verify file path and permissions.

**2. Corrupted Document**
```
Error: Failed to open document: BadZipFile
```
**Solution:** File may be corrupted. Try opening in Word and re-saving.

**3. Password Protected**
```
Error: Document is password protected
```
**Solution:** python-docx cannot open password-protected files. Remove protection first.

**4. Unsupported Format**
```
Error: Unsupported file format: .doc
```
**Solution:** Convert .doc to .docx using Microsoft Word or LibreOffice.

## Performance Considerations

### Memory Usage
- 1MB document: ~5MB memory (5x expansion for JSON)
- 10MB document: ~50MB memory
- 50MB document: ~250MB memory

**Large document handling:**
- Process elements sequentially
- Clear objects after processing
- Use generator patterns for iteration

### Disk Usage
- Cache size: ~3-5x original file size
- Example: 5MB Word → 15-25MB cache
- Cache location: `~/.claude-cache/docx/`
- Auto-cleanup: LRU eviction after 30 days

### Optimization Tips
1. **Extract once, query many times** - cache is persistent
2. **Use heading queries** - faster than keyword search
3. **Chunk first** - always chunk after extraction for optimal performance
4. **Use --force flag** - only when document has changed

## Limitations

1. **VBA Macros:** Not extracted (design choice for security)
2. **Images:** Extracted as metadata only (position, size, alt text)
3. **Charts:** Not extracted (recommend screenshot approach)
4. **Embedded Objects:** May not be fully extracted
5. **Password Protection:** Cannot open protected documents
6. **Legacy Formats:** .doc (Word 97-2003) not supported

## Comparison to Alternatives

### vs. Loading Full Document in LLM Context
- **Token usage:** 10-50x reduction
- **Speed:** 10-20x faster (no token processing)
- **Cost:** 10-50x cheaper (fewer tokens)
- **Limits:** No file size limits (vs 1-2MB context limits)

### vs. Manual extraction
- **Speed:** Automated (vs manual copy-paste)
- **Accuracy:** 99%+ preservation (vs human error)
- **Repeatability:** Cached (vs re-doing work)
- **Scalability:** Handles 50MB files (vs manual limit ~5MB)

## Installation

### Prerequisites
```bash
# Python 3.8+
python3 --version

# Install dependencies
pip3 install -r requirements.txt
```

### Verify Installation
```bash
# Test python-docx
python3 -c "import docx; print('python-docx available')"
```

## Troubleshooting

### Issue: "Module not found: docx"
**Solution:**
```bash
pip3 install python-docx
```

### Issue: "Permission denied" when creating cache
**Solution:**
```bash
chmod 755 ~/.claude-cache/docx/
```

### Issue: Extraction very slow (>2 minutes for 5MB file)
**Possible causes:**
- Many tables with complex formatting
- Large number of tracked changes
- Corrupted file structure

**Solution:** Use `--force` flag and check for warnings.

### Issue: High memory usage
**Solution:** Process large documents in smaller sections or increase available RAM.

## References

- **python-docx Documentation:** https://python-docx.readthedocs.io/
- **Office Open XML (OOXML) Format:** https://docs.microsoft.com/en-us/openspecs/office_standards/

## Notes

- Extraction is 100% local (no LLM calls, no API requests)
- Cache is persistent across sessions
- VBA macros are not executed (read-only access)
- Security: No macro execution, read-only access
