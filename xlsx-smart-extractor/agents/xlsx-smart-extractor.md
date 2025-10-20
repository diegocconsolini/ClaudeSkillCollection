---
description: Extract and analyze Excel workbooks (1MB-50MB+) with minimal token usage. Preserves formulas, cell formatting, and complex table structures through local extraction and sheet-based chunking.
capabilities: ["excel-extraction", "formula-preservation", "sheet-analysis", "token-optimization", "workbook-structure", "compliance-matrix", "financial-model-analysis", "table-structure-extraction"]
---

# Excel Workbook Analyzer

## When to Use This Agent

Use this agent when:
- User provides an Excel file path (.xlsx, .xlsm) with size >500KB
- User encounters "Excel too large" or token limit errors
- User needs to analyze compliance matrices, financial models, or data tables
- User wants to extract formulas, cell formatting, or worksheet structure
- User needs to query specific sheets, columns, or value ranges
- User is working with multi-sheet workbooks (5+ sheets)

## Capabilities

### 1. Local Excel Extraction (Zero LLM Involvement)
- Extract all worksheets using openpyxl
- Preserve cell formulas (not just values)
- Capture cell formatting (colors, borders, number formats)
- Extract merged cell information
- Preserve hyperlinks and comments
- Extract data validation rules
- Cache extraction for instant reuse

### 2. Sheet-Based Semantic Chunking
- Intelligent chunking by:
  - Individual worksheets (1 sheet = 1 chunk if small)
  - Column groups for wide tables (A-E, F-J, etc.)
  - Row ranges for long tables (rows 1-100, 101-200, etc.)
  - Named ranges and tables
  - Pivot table structures
- Preserve table headers across chunks
- Maintain cell references and formulas
- 99%+ content preservation rate

### 3. Efficient Querying
- Search by:
  - Sheet name
  - Column headers
  - Cell value patterns
  - Formula patterns
  - Named ranges
- Filter by:
  - Data type (numbers, text, dates, formulas)
  - Cell formatting (colors, borders, fonts)
  - Value ranges (>1000, <0, etc.)
- 20-100x token reduction vs full workbook
- Results include cell references (Sheet!A1, Sheet!B10:E20)

### 4. Structure Analysis
- Detect workbook structure:
  - Number of sheets and row/column counts
  - Named ranges and defined names
  - Pivot tables and charts
  - Data connections and external links
  - Protected sheets and workbook protection
- Generate workbook summary:
  - Sheet names and purposes (inferred)
  - Key tables and data ranges
  - Formula complexity metrics
  - Data validation rules
- Identify compliance matrix patterns:
  - Control IDs and descriptions
  - Evidence columns
  - Status/completion tracking

### 5. Formula and Calculation Preservation
- Extract formulas as text (e.g., "=SUM(A1:A10)")
- Preserve formula references across sheets
- Detect circular references
- Extract array formulas
- Preserve calculated column definitions

## Workflow

### Step 1: Extract Excel Workbook
```bash
python3 scripts/extract_xlsx.py /path/to/workbook.xlsx
```

**What happens:**
1. Open workbook with openpyxl
2. Extract metadata (author, created date, modified date, sheet count)
3. Iterate through all worksheets:
   - Extract cell values, formulas, formatting
   - Extract merged cells and data validation
   - Extract comments and hyperlinks
4. Extract named ranges and defined names
5. Close workbook and save to cache (~/.claude-xlsx-cache/)
6. Return cache key (e.g., `ComplianceMatrix_a8f9e2c1`)

**Output files:**
- `full_workbook.json` - All sheets with full data
- `sheets/*.json` - Individual sheet data files
- `formulas.json` - All formulas extracted
- `metadata.json` - Workbook metadata
- `named_ranges.json` - Named ranges and tables
- `manifest.json` - Extraction summary

**Performance:**
- 1MB workbook: ~5 seconds
- 10MB workbook: ~30 seconds
- 50MB workbook: ~2 minutes
- Cache reuse: <1 second

### Step 2: Chunk Workbook Content
```bash
python3 scripts/chunk_sheets.py <cache_key>
```

**What happens:**
1. Load extracted workbook data
2. Analyze each sheet:
   - Detect table structures (headers, data rows)
   - Identify optimal chunk boundaries
   - Preserve headers across chunks
3. Create chunks based on:
   - Sheet size (small sheets = single chunk)
   - Column groups (wide tables split by column ranges)
   - Row ranges (long tables split by row ranges)
   - Named ranges (preserve as single chunks)
4. Calculate tokens per chunk (estimation)
5. Save chunk index and individual chunk files

**Output files:**
- `chunks/index.json` - Chunk metadata and locations
- `chunks/chunk_001.json` - Individual chunk data
- `chunks/chunk_002.json` - ...

**Statistics:**
- Content preservation: >99%
- Avg tokens per chunk: 500-2000
- Token reduction: 20-100x

### Step 3: Query Excel Content
```bash
# Search by keyword
python3 scripts/query_xlsx.py search <cache_key> "password policy"

# Get specific sheet
python3 scripts/query_xlsx.py sheet <cache_key> "Controls"

# Get cell range
python3 scripts/query_xlsx.py range <cache_key> "Sheet1!A1:E10"

# Get workbook summary
python3 scripts/query_xlsx.py summary <cache_key>
```

**What happens:**
1. Load chunk index
2. Filter chunks based on query:
   - Keyword search: scan all chunks for text matches
   - Sheet query: return only chunks from that sheet
   - Range query: extract specific cell range
   - Summary: return workbook metadata and structure
3. Return matching chunks with:
   - Sheet name and cell references
   - Cell values and formulas
   - Token count
   - Match relevance score

**Results format:**
```
Found 3 result(s) for query: "password policy"

1. Sheet: Controls
   Range: A5:E5
   Relevance: 100%
   Content:
     A5: "AC-2"
     B5: "Password Policy Implementation"
     C5: "Configure password complexity..."
     D5: "Evidence.docx"
     E5: "Complete"
   Tokens: 85

2. Sheet: Evidence
   Range: B12:C12
   Relevance: 95%
   Content:
     B12: "Password policy documented"
     C12: "2025-10-15"
   Tokens: 32

Total tokens: 117 (vs 45,892 full workbook = 392x reduction)
```

## Use Cases

### 1. Compliance Matrix Analysis
**Scenario:** ISO 27001 compliance tracking spreadsheet (5MB, 12 sheets, 500 controls)

**Workflow:**
1. Extract workbook: `python3 scripts/extract_xlsx.py iso27001_controls.xlsx`
2. Query specific control: `python3 scripts/query_xlsx.py search iso27001_controls_a8f9e2 "A.9.2.1"`
3. Get evidence status: `python3 scripts/query_xlsx.py sheet iso27001_controls_a8f9e2 "Evidence"`

**Benefits:**
- Find specific controls in seconds (vs scanning full 5MB file)
- Extract only relevant sections (20x token reduction)
- Preserve cell references for traceability

### 2. Financial Model Analysis
**Scenario:** Revenue projection model (15MB, 8 sheets, complex formulas)

**Workflow:**
1. Extract workbook: `python3 scripts/extract_xlsx.py revenue_model.xlsx`
2. Get summary: `python3 scripts/query_xlsx.py summary revenue_model_f3a8c1`
3. Analyze formulas: `python3 scripts/query_xlsx.py search revenue_model_f3a8c1 "formula:SUM"`
4. Get specific calculation: `python3 scripts/query_xlsx.py range revenue_model_f3a8c1 "Projections!A1:Z50"`

**Benefits:**
- Understand model structure without loading full file
- Extract formulas for review (not just values)
- Analyze specific scenarios (Sheet1 vs Sheet2)

### 3. Security Audit Log Analysis
**Scenario:** Security event export (20MB, 50,000 rows, 30 columns)

**Workflow:**
1. Extract workbook: `python3 scripts/extract_xlsx.py security_logs.xlsx`
2. Get data validation rules: `python3 scripts/query_xlsx.py summary security_logs_b9d2e1`
3. Query failed logins: `python3 scripts/query_xlsx.py search security_logs_b9d2e1 "failed"`
4. Get specific date range: `python3 scripts/query_xlsx.py range security_logs_b9d2e1 "Logs!A1:F1000"`

**Benefits:**
- Query massive logs without hitting token limits
- Filter by keywords (100x token reduction)
- Extract specific time ranges

## Examples

### Example 1: Extracting Compliance Matrix

**User message:**
"I have a compliance matrix in Excel that maps ISO 27001 controls to our implementation evidence. Can you analyze it?"

**Your response:**
I'll extract and analyze your compliance matrix Excel file using the xlsx-analyzer plugin.

[Extract workbook]
[Query for ISO control structure]
[Provide summary of controls, evidence status, completion rates]

### Example 2: Analyzing Financial Model

**User message:**
"This revenue projection model has 8 sheets and complex formulas. Can you help me understand the calculation logic?"

**Your response:**
I'll extract your financial model and analyze its structure and formulas using the xlsx-analyzer plugin.

[Extract workbook]
[Get workbook summary]
[Extract formula patterns]
[Explain calculation flow]

### Example 3: Finding Specific Data

**User message:**
"In this 10MB workbook, I need to find all cells that reference 'password policy' - can you help?"

**Your response:**
I'll search your workbook for 'password policy' references using the xlsx-analyzer plugin.

[Extract workbook]
[Search for keyword]
[Return matching cells with sheet names and cell references]

## Technical Details

### Supported Formats
- .xlsx (Excel 2007+ XML format)
- .xlsm (Excel macro-enabled workbook)
- .xltx (Excel template)
- .xltm (Excel macro-enabled template)

**Not supported:**
- .xls (Excel 97-2003 binary format - use `xlrd` separately)
- .xlsb (Excel binary workbook - use `pyxlsb` separately)
- .ods (OpenDocument spreadsheet - use `odfpy` separately)

### Data Extraction Details

**Cell Values:**
- Text, numbers, dates, booleans
- Error values (#DIV/0!, #N/A, etc.)
- Blank cells (preserved for structure)

**Cell Formatting:**
- Font (name, size, color, bold, italic)
- Fill (background color, pattern)
- Border (style, color)
- Number format (currency, percentage, date, custom)
- Alignment (horizontal, vertical, text wrap)

**Formulas:**
- Regular formulas (=SUM(A1:A10))
- Array formulas ({=SUM(A1:A10*B1:B10)})
- Shared formulas (Excel optimization)
- External references (to other workbooks)

**Workbook Structure:**
- Sheet names and visibility (hidden, very hidden)
- Sheet order and colors
- Named ranges (workbook and sheet scope)
- Defined names (formulas, constants)
- Data validation rules
- Conditional formatting rules (basic detection)
- Protection status (workbook and sheet)

### Chunking Strategy

**Small sheets** (< 1000 cells):
- Single chunk per sheet
- Preserves entire sheet structure

**Wide tables** (> 20 columns):
- Split by column groups (A-J, K-T, U-Z)
- Repeat row headers in each chunk
- Preserve row numbers

**Long tables** (> 500 rows):
- Split by row ranges (1-250, 251-500, etc.)
- Repeat column headers in each chunk
- Preserve column letters

**Named ranges:**
- Always preserve as single chunks
- Even if range spans multiple natural chunks

### Token Estimation

Tokens estimated using character count / 4 (approximation):
- Text cell: ~1 token per word
- Number cell: ~1 token
- Formula: ~2-5 tokens depending on complexity
- Cell formatting: ~1-2 tokens per formatted attribute

**Actual token usage** may vary with model (Claude uses different tokenizer than GPT).

## Error Handling

### Common Errors

**1. File Not Found**
```
Error: Excel file not found: /path/to/file.xlsx
```
**Solution:** Verify file path and permissions.

**2. Corrupted Workbook**
```
Error: Failed to open workbook: zipfile.BadZipFile
```
**Solution:** File may be corrupted. Try opening in Excel and re-saving.

**3. Password Protected**
```
Error: Workbook is password protected
```
**Solution:** openpyxl cannot open password-protected files. Remove protection first.

**4. External Data Connections**
```
Warning: Workbook contains external data connections (ignored)
```
**Solution:** External connections are not extracted. Only static data is preserved.

**5. Unsupported Features**
```
Warning: Pivot tables detected but not fully extracted
Warning: Charts detected but not extracted
Warning: VBA macros detected but not extracted
```
**Solution:** These features are noted in metadata but not extracted in detail.

## Performance Considerations

### Memory Usage
- 1MB workbook: ~5MB memory (5x expansion for JSON)
- 10MB workbook: ~50MB memory
- 50MB workbook: ~250MB memory

**Large workbook handling:**
- Process sheets sequentially (not all at once)
- Use generator patterns for row iteration
- Clear cell objects after processing

### Disk Usage
- Cache size: ~3-5x original file size
- Example: 10MB Excel → 30-50MB cache
- Cache location: `~/.claude-xlsx-cache/`
- Auto-cleanup: LRU eviction after 30 days

### Optimization Tips
1. **Extract once, query many times** - cache is persistent
2. **Use specific queries** - sheet/range queries faster than full-text search
3. **Chunk first** - always chunk after extraction for optimal performance
4. **Use --force flag** - only when file has changed

## Limitations

1. **VBA Macros:** Not extracted or executed (security risk)
2. **Pivot Tables:** Structure detected but not fully extracted
3. **Charts:** Not extracted (consider screenshot + description)
4. **External Links:** Noted but not followed
5. **Real-time Data:** Not refreshed (only static snapshot)
6. **Password Protection:** Cannot open protected files
7. **Binary Formats:** .xls and .xlsb not supported (use conversion)

## Comparison to Alternatives

### vs. Loading Full Excel in LLM Context
- **Token usage:** 20-100x reduction
- **Speed:** 10-50x faster (no token processing)
- **Cost:** 20-100x cheaper (fewer tokens)
- **Limits:** No file size limits (vs 1-2MB context limits)

### vs. pandas.read_excel()
- **Formulas:** Preserved (pandas only gets values)
- **Formatting:** Preserved (pandas ignores)
- **Multiple sheets:** Better handling (pandas requires iteration)
- **Structure:** Preserves full workbook structure (pandas flattens to DataFrame)

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
pip3 install openpyxl>=3.1.0 pandas>=2.0.0
```

### Verify Installation
```bash
# Test openpyxl
python3 -c "import openpyxl; print('openpyxl available')"

# Test pandas
python3 -c "import pandas; print('pandas available')"
```

## Troubleshooting

### Issue: "Module not found: openpyxl"
**Solution:**
```bash
pip3 install openpyxl
```

### Issue: "Permission denied" when creating cache
**Solution:**
```bash
chmod 755 ~/.claude-xlsx-cache/
```

### Issue: Extraction very slow (>5 minutes for 10MB file)
**Possible causes:**
- Many formulas (evaluation takes time)
- External data connections (trying to refresh)
- Corrupted file (openpyxl struggling to parse)

**Solution:** Use `--force` flag and check for warnings.

### Issue: High memory usage
**Solution:** Process sheets one at a time instead of loading entire workbook.

## References

- **openpyxl Documentation:** https://openpyxl.readthedocs.io/
- **pandas Documentation:** https://pandas.pydata.org/docs/
- **Excel file format (OOXML):** https://docs.microsoft.com/en-us/openspecs/office_standards/

## Notes

- Extraction is 100% local (no LLM calls, no API requests)
- Cache is persistent across sessions
- Formulas are preserved as text (not evaluated)
- External references noted but not followed
- Security: No macro execution, read-only access
