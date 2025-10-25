#!/usr/bin/env python3
"""
PDF Smart Extractor - Local extraction with zero LLM involvement
Extracts 100% of PDF content to disk for efficient chunking and caching
"""

import sys
import os
import hashlib
import json
import getpass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Try to import pymupdf - will be checked properly in check_dependencies()
try:
    import pymupdf  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ModuleNotFoundError:
    PYMUPDF_AVAILABLE = False
    pymupdf = None

# Import shared smart cache
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from smart_cache import SmartCache


class PDFExtractor:
    """Extract complete PDF content locally without LLM"""

    def __init__(self, cache_dir: str = None):
        """Initialize extractor with cache directory"""
        # Initialize SmartCache (SHAKE256 hashing with auto-migration from SHA-256)
        self.smart_cache = SmartCache(doc_type='pdf', cache_dir=Path(cache_dir) if cache_dir else None)
        self.cache_dir = self.smart_cache.cache_dir

    def extract_metadata(self, doc: pymupdf.Document) -> Dict:
        """Extract PDF metadata"""
        metadata = {
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'subject': doc.metadata.get('subject', ''),
            'keywords': doc.metadata.get('keywords', ''),
            'creator': doc.metadata.get('creator', ''),
            'producer': doc.metadata.get('producer', ''),
            'creation_date': doc.metadata.get('creationDate', ''),
            'mod_date': doc.metadata.get('modDate', ''),
            'page_count': len(doc),
            'is_encrypted': doc.is_encrypted,
            'is_pdf': doc.is_pdf
        }
        return metadata

    def extract_page_content(self, page: pymupdf.Page) -> Dict:
        """Extract all content from a single page"""
        page_data = {
            'page_number': page.number + 1,
            'text': page.get_text("text"),  # Plain text only (no binary data)
            'width': page.rect.width,
            'height': page.rect.height
        }
        return page_data

    def extract_toc(self, doc: pymupdf.Document) -> List[Dict]:
        """Extract table of contents if available"""
        toc = doc.get_toc()
        toc_data = []

        for level, title, page_num in toc:
            toc_data.append({
                'level': level,
                'title': title,
                'page': page_num
            })

        return toc_data

    def extract_full_pdf(self, pdf_path: str, force: bool = False, password: str = None) -> Dict:
        """
        Extract complete PDF content to cache

        Args:
            pdf_path: Path to PDF file
            force: Force re-extraction even if cached
            password: Password for encrypted PDFs (if None, will prompt interactively)

        Returns:
            Dictionary with extraction results and cache location
        """
        pdf_path = os.path.abspath(pdf_path)

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Generate cache key with SHAKE256 (auto-migrates from SHA-256 if needed)
        cache_key, cache_path = self.smart_cache.get_cache_key(pdf_path)
        cache_path.mkdir(parents=True, exist_ok=True)

        pdf_name = Path(pdf_path).stem

        # Check if already extracted
        manifest_path = cache_path / "manifest.json"
        if manifest_path.exists() and not force:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            return {
                'status': 'cached',
                'cache_key': cache_key,
                'cache_path': str(cache_path),
                'manifest': manifest,
                'message': f'Using cached extraction for {pdf_name}'
            }

        # Extract PDF
        print(f"Extracting PDF: {pdf_name} ({os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB)")

        # Open PDF (may be encrypted)
        doc = pymupdf.open(pdf_path)

        # Handle password-protected PDFs
        if doc.is_encrypted:
            print("🔒 PDF is password protected")

            max_attempts = 3
            attempt = 0

            while attempt < max_attempts:
                # Use provided password or prompt interactively
                if password is None:
                    password_input = getpass.getpass("Enter password: ")
                else:
                    password_input = password

                # Try to authenticate
                auth_result = doc.authenticate(password_input)

                if auth_result:
                    print("✓ Password accepted")
                    break
                else:
                    attempt += 1
                    if password is not None:
                        # If password was provided via CLI, don't retry
                        doc.close()
                        raise PermissionError(f"Invalid password for {pdf_name}")
                    elif attempt < max_attempts:
                        print(f"❌ Invalid password. Attempt {attempt}/{max_attempts}")
                        password = None  # Reset for next attempt
                    else:
                        doc.close()
                        raise PermissionError(f"Failed to unlock {pdf_name} after {max_attempts} attempts")

            # Check if we have access after authentication
            if doc.metadata is None:
                doc.close()
                raise PermissionError(f"PDF is encrypted but could not be unlocked: {pdf_name}")

        # Extract metadata
        metadata = self.extract_metadata(doc)

        # Extract table of contents
        toc = self.extract_toc(doc)

        # Extract all pages
        pages = []
        full_text = []

        for page_num, page in enumerate(doc, start=1):
            print(f"  Processing page {page_num}/{len(doc)}...", end='\r')
            page_data = self.extract_page_content(page)
            pages.append(page_data)
            full_text.append(page_data['text'])

        print()  # New line after progress

        # Combine all text
        complete_text = "\n\n".join(full_text)

        # Calculate statistics
        char_count = len(complete_text)
        word_count = len(complete_text.split())

        # Estimate tokens (rough: 1 token ≈ 4 characters for English)
        estimated_tokens = char_count // 4

        # Save full text to file
        text_path = cache_path / "full_text.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(complete_text)

        # Save structured pages
        pages_path = cache_path / "pages.json"
        with open(pages_path, 'w', encoding='utf-8') as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)

        # Save metadata
        metadata_path = cache_path / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Save TOC
        if toc:
            toc_path = cache_path / "toc.json"
            with open(toc_path, 'w', encoding='utf-8') as f:
                json.dump(toc, f, indent=2, ensure_ascii=False)

        # Create manifest
        manifest = {
            'cache_key': cache_key,
            'original_path': pdf_path,
            'pdf_name': pdf_name,
            'pdf_hash': cache_key.split('_')[-1],  # Extract hash from cache_key
            'extraction_date': str(Path(pdf_path).stat().st_mtime),
            'metadata': metadata,
            'statistics': {
                'page_count': len(pages),
                'char_count': char_count,
                'word_count': word_count,
                'estimated_tokens': estimated_tokens,
                'file_size_mb': os.path.getsize(pdf_path) / 1024 / 1024
            },
            'has_toc': len(toc) > 0,
            'files': {
                'full_text': str(text_path),
                'pages': str(pages_path),
                'metadata': str(metadata_path),
                'toc': str(toc_path) if toc else None
            }
        }

        # Save manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        doc.close()

        print(f"✓ Extraction complete:")
        print(f"  - Pages: {metadata['page_count']}")
        print(f"  - Characters: {char_count:,}")
        print(f"  - Words: {word_count:,}")
        print(f"  - Estimated tokens: {estimated_tokens:,}")
        print(f"  - Cache location: {cache_path}")

        return {
            'status': 'extracted',
            'cache_key': cache_key,
            'cache_path': str(cache_path),
            'manifest': manifest,
            'message': f'Successfully extracted {pdf_name}'
        }


def check_dependencies():
    """Check required dependencies and provide helpful error messages"""
    missing = []

    if not PYMUPDF_AVAILABLE:
        missing.append("pymupdf")

    if missing:
        print("❌ Missing required dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n📦 Install dependencies:")
        print("   Option 1 (recommended): pip install -r requirements.txt")
        print("   Option 2: pip install pymupdf")
        print("\n💡 Using virtual environment? Activate it first:")
        print("   python3 -m venv venv && source venv/bin/activate  # Linux/Mac")
        print("   python3 -m venv venv && venv\\Scripts\\activate  # Windows")
        print("\nFor more details, see: pdf-smart-extractor/README.md#installation")
        sys.exit(1)


def main():
    """Command-line interface"""
    # Check dependencies first
    check_dependencies()

    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_path> [--force] [--password PASSWORD] [--output-dir DIR]")
        print("\nExtracts complete PDF content to cache for efficient processing")
        print("\nOptions:")
        print("  --force              Force re-extraction even if cached")
        print("  --password PASSWORD  Password for encrypted PDFs (will prompt if not provided)")
        print("  --output-dir DIR     Copy extracted files to specified directory (prompts if not provided)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    force = '--force' in sys.argv

    # Extract password from arguments if provided
    password = None
    if '--password' in sys.argv:
        password_index = sys.argv.index('--password')
        if password_index + 1 < len(sys.argv):
            password = sys.argv[password_index + 1]
        else:
            print("Error: --password requires a value")
            sys.exit(1)

    # Extract output directory from arguments if provided
    output_dir = None
    if '--output-dir' in sys.argv:
        output_dir_index = sys.argv.index('--output-dir')
        if output_dir_index + 1 < len(sys.argv):
            output_dir = sys.argv[output_dir_index + 1]
        else:
            print("Error: --output-dir requires a value")
            sys.exit(1)

    extractor = PDFExtractor()

    try:
        result = extractor.extract_full_pdf(pdf_path, force=force, password=password)

        print(f"\n{result['message']}")
        print(f"Cache key: {result['cache_key']}")

        if result['status'] == 'cached':
            print("\n💡 Use --force to re-extract")

        # Handle output directory
        cache_path = Path(result['cache_path'])
        should_copy = False
        keep_cache = True  # Default: always keep cache

        if output_dir is None:
            # Ask user interactively if they want to copy to working directory
            print("\n📁 Copy extracted files to working directory?")
            response = input("Copy files? (y/n): ").strip().lower()

            if response == 'y':
                output_dir = Path.cwd() / f"extracted_{result['cache_key']}"
                should_copy = True

                # Ask about cache behavior only if copying
                print(f"\n💾 Maintain cache in {cache_path}?")
                print("  (yes) Keep cache for instant reuse across projects")
                print("  (no)  Remove cache after copying files")
                keep_cache_response = input("Keep cache? (y/n): ").strip().lower()
                keep_cache = keep_cache_response == 'y'
        else:
            # --output-dir was specified, skip prompts and copy files
            should_copy = True
            keep_cache = True  # Always keep cache when using --output-dir

        if should_copy and output_dir:
            output_path = Path(output_dir)

            # Copy all files from cache to output directory
            import shutil

            print(f"\n📋 Copying files to {output_path}...")
            output_path.mkdir(parents=True, exist_ok=True)

            for item in cache_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, output_path / item.name)
                    print(f"  ✓ {item.name}")

            print(f"\n✓ Files copied to: {output_path}")

            # Remove cache if requested
            if not keep_cache:
                shutil.rmtree(cache_path)
                print(f"  ✓ Cache removed")
            else:
                print(f"  ✓ Cache maintained at: {cache_path}")

    except PermissionError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Tip: Use --password <password> to provide password via command line")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
