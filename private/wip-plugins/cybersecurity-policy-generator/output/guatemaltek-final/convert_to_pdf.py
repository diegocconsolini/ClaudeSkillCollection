#!/usr/bin/env python3
"""
Convert Guatemaltek policy markdown files to professional PDFs
"""
import os
import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Professional CSS styling for the PDFs
CSS_STYLE = """
@page {
    size: letter;
    margin: 1in 0.75in;

    @top-left {
        content: "Guatemaltek";
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 9pt;
        color: #666;
    }

    @top-right {
        content: string(doc-title);
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 9pt;
        color: #666;
    }

    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 9pt;
        color: #666;
    }

    @bottom-right {
        content: "Confidential";
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 9pt;
        color: #666;
        font-style: italic;
    }
}

body {
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    color: #1a5490;
    font-size: 24pt;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: 20pt;
    padding-bottom: 10pt;
    border-bottom: 3px solid #1a5490;
    string-set: doc-title content();
    page-break-after: avoid;
}

h2 {
    color: #1a5490;
    font-size: 18pt;
    font-weight: bold;
    margin-top: 20pt;
    margin-bottom: 12pt;
    page-break-after: avoid;
}

h3 {
    color: #2a6ab0;
    font-size: 14pt;
    font-weight: bold;
    margin-top: 16pt;
    margin-bottom: 10pt;
    page-break-after: avoid;
}

h4 {
    color: #3a7ac0;
    font-size: 12pt;
    font-weight: bold;
    margin-top: 12pt;
    margin-bottom: 8pt;
    page-break-after: avoid;
}

p {
    margin-bottom: 10pt;
    text-align: justify;
    orphans: 3;
    widows: 3;
}

ul, ol {
    margin-bottom: 10pt;
    padding-left: 25pt;
}

li {
    margin-bottom: 6pt;
}

strong {
    font-weight: bold;
    color: #1a5490;
}

em {
    font-style: italic;
}

code {
    background-color: #f4f4f4;
    padding: 2pt 4pt;
    font-family: 'Courier New', monospace;
    font-size: 10pt;
    border-radius: 3pt;
}

pre {
    background-color: #f4f4f4;
    padding: 10pt;
    border-left: 3px solid #1a5490;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
}

blockquote {
    border-left: 4px solid #1a5490;
    padding-left: 15pt;
    margin-left: 0;
    font-style: italic;
    color: #555;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 15pt;
    page-break-inside: avoid;
}

th {
    background-color: #1a5490;
    color: white;
    padding: 8pt;
    text-align: left;
    font-weight: bold;
}

td {
    padding: 6pt 8pt;
    border: 1pt solid #ddd;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

hr {
    border: none;
    border-top: 2px solid #1a5490;
    margin: 20pt 0;
}

a {
    color: #1a5490;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.page-break {
    page-break-after: always;
}

/* Front matter styling */
.front-matter {
    text-align: center;
    margin-bottom: 30pt;
}

.company-name {
    font-size: 28pt;
    font-weight: bold;
    color: #1a5490;
    margin-bottom: 10pt;
}

.document-title {
    font-size: 20pt;
    color: #333;
    margin-bottom: 20pt;
}

.metadata {
    font-size: 10pt;
    color: #666;
    line-height: 1.4;
}
"""

def convert_markdown_to_pdf(markdown_file, pdf_file):
    """Convert a markdown file to a professional PDF"""
    print(f"Converting {os.path.basename(markdown_file)} to PDF...")

    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML with extensions
    md = markdown.Markdown(extensions=[
        'extra',        # Tables, fenced code blocks, etc.
        'nl2br',        # Convert newlines to <br>
        'sane_lists',   # Better list handling
        'toc',          # Table of contents
    ])
    html_content = md.convert(md_content)

    # Extract document title from first h1 or filename
    doc_title = os.path.splitext(os.path.basename(markdown_file))[0]
    if html_content.startswith('<h1>'):
        end_h1 = html_content.find('</h1>')
        if end_h1 > 0:
            doc_title = html_content[4:end_h1]

    # Create complete HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{doc_title}</title>
</head>
<body>
{html_content}
</body>
</html>"""

    # Convert to PDF with professional styling
    font_config = FontConfiguration()
    html = HTML(string=full_html)
    css = CSS(string=CSS_STYLE, font_config=font_config)

    html.write_pdf(pdf_file, stylesheets=[css], font_config=font_config)

    # Get file size
    file_size = os.path.getsize(pdf_file)
    size_kb = file_size / 1024
    print(f"  ✓ Created {os.path.basename(pdf_file)} ({size_kb:.1f} KB)")

    return pdf_file, file_size

def main():
    # Define paths
    base_dir = Path("/Users/diegocavalariconsolini/ClaudeCode/ClaudeSkillCollection/private/wip-plugins/cybersecurity-policy-generator/output/guatemaltek-final")
    markdown_dir = base_dir / "markdown"
    pdf_dir = base_dir / "pdf"

    # Ensure PDF directory exists
    pdf_dir.mkdir(exist_ok=True)

    # List of files to convert
    files = [
        "1-InformationSecurityPolicy.md",
        "2-AccessControlPolicy.md",
        "3-AcceptableUsePolicy.md",
        "4-IncidentResponsePolicy.md",
        "5-RiskManagementPolicy.md",
        "6-DataClassificationPolicy.md",
        "7-BusinessContinuityPolicy.md",
        "8-PhysicalSecurityPolicy.md",
    ]

    print("=" * 70)
    print("Guatemaltek Policy PDF Conversion")
    print("=" * 70)
    print()

    results = []

    for md_file in files:
        markdown_path = markdown_dir / md_file
        pdf_filename = md_file.replace('.md', '.pdf')
        pdf_path = pdf_dir / pdf_filename

        if not markdown_path.exists():
            print(f"⚠ Warning: {md_file} not found, skipping...")
            continue

        try:
            pdf_file, file_size = convert_markdown_to_pdf(str(markdown_path), str(pdf_path))
            results.append((pdf_filename, file_size))
        except Exception as e:
            print(f"✗ Error converting {md_file}: {e}")
            continue

    # Print summary
    print()
    print("=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    print()

    total_size = 0
    for filename, size in results:
        size_kb = size / 1024
        total_size += size
        print(f"  {filename:<45} {size_kb:>8.1f} KB")

    print()
    print(f"Total: {len(results)} files converted, {total_size / 1024:.1f} KB")
    print()
    print(f"Output directory: {pdf_dir}")
    print("=" * 70)

if __name__ == "__main__":
    main()
