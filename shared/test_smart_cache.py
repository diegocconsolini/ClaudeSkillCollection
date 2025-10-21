#!/usr/bin/env python3
"""Test smart_cache.py functionality"""

import sys
import os
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent))

from smart_cache import SmartCache, PostQuantumHash, BloomFilter

def test_post_quantum_hash():
    """Test SHAKE256 hashing"""
    print("Testing PostQuantumHash...")

    # Create test file
    test_file = Path("/tmp/test_hash.txt")
    test_file.write_text("test content")

    # Test SHAKE256 hash
    shake_hash = PostQuantumHash.hash_file(str(test_file))
    print(f"  SHAKE256 hash: {shake_hash}")
    assert len(shake_hash) == 16, "Hash should be 16 chars"

    # Test SHA-256 hash (for migration)
    sha_hash = PostQuantumHash.hash_sha256(str(test_file))
    print(f"  SHA-256 hash: {sha_hash}")
    assert len(sha_hash) == 16, "Hash should be 16 chars"

    # Hashes should be different
    assert shake_hash != sha_hash, "SHAKE256 and SHA-256 should differ"

    print("  ✓ PostQuantumHash works\n")

def test_bloom_filter():
    """Test Bloom filter"""
    print("Testing BloomFilter...")

    bloom = BloomFilter(size=1000, hash_count=7)

    # Add items
    bloom.add("item1")
    bloom.add("item2")
    bloom.add("item3")

    # Check contains
    assert bloom.contains("item1"), "Should contain item1"
    assert bloom.contains("item2"), "Should contain item2"
    assert bloom.contains("item3"), "Should contain item3"
    assert not bloom.contains("item4"), "Should not contain item4 (probably)"

    # Test save/load
    bloom_path = Path("/tmp/test_bloom.json")
    bloom.save(bloom_path)

    loaded_bloom = BloomFilter.load(bloom_path)
    assert loaded_bloom.contains("item1"), "Loaded filter should contain item1"
    assert loaded_bloom.contains("item2"), "Loaded filter should contain item2"

    bloom_path.unlink()

    print("  ✓ BloomFilter works\n")

def test_smart_cache():
    """Test SmartCache"""
    print("Testing SmartCache...")

    # Create test file
    test_file = Path("/tmp/test_doc.pdf")
    test_file.write_text("test pdf content")

    # Initialize cache
    cache_dir = Path("/tmp/test_claude_cache")
    cache = SmartCache(doc_type='pdf', cache_dir=cache_dir, enable_bloom=False)

    # Get cache key
    cache_key, cache_path = cache.get_cache_key(str(test_file))
    print(f"  Cache key: {cache_key}")
    print(f"  Cache path: {cache_path}")

    assert "test_doc_" in cache_key, "Cache key should contain filename"
    assert len(cache_key) > 10, "Cache key should include hash"

    # Check exists (should be False)
    assert not cache.exists(cache_key), "Cache should not exist yet"

    # Create cache directory and manifest
    cache_path.mkdir(parents=True, exist_ok=True)
    manifest_path = cache_path / "manifest.json"
    manifest_path.write_text('{"test": "data"}')

    # Mark as cached
    cache.mark_cached(cache_key)

    # Check exists (should be True now)
    assert cache.exists(cache_key), "Cache should exist now"

    # Cleanup
    import shutil
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    test_file.unlink()

    print("  ✓ SmartCache works\n")

def test_migration():
    """Test SHA-256 to SHAKE256 migration"""
    print("Testing migration...")

    # Create test file
    test_file = Path("/tmp/test_migrate.pdf")
    test_file.write_text("migration test content")

    # Get hashes
    sha_hash = PostQuantumHash.hash_sha256(str(test_file))
    shake_hash = PostQuantumHash.hash_file(str(test_file))

    doc_name = test_file.stem
    old_cache_key = f"{doc_name}_{sha_hash}"
    new_cache_key = f"{doc_name}_{shake_hash}"

    # Create old cache structure
    old_cache_dir = Path("/tmp/.claude-pdf-cache")
    old_cache_path = old_cache_dir / old_cache_key
    old_cache_path.mkdir(parents=True, exist_ok=True)
    (old_cache_path / "manifest.json").write_text('{"old": "cache"}')

    # Initialize SmartCache
    cache_dir = Path("/tmp/test_cache_new")
    cache = SmartCache(doc_type='pdf', cache_dir=cache_dir, enable_bloom=False)
    cache.old_cache_dir = old_cache_dir  # Override for test

    # Get cache key (should trigger migration)
    result_key, result_path = cache.get_cache_key(str(test_file))

    print(f"  Old key: {old_cache_key}")
    print(f"  New key: {new_cache_key}")
    print(f"  Result key: {result_key}")

    assert result_key == new_cache_key, "Should return new SHAKE256 key"
    assert result_path.exists(), "New cache path should exist"
    assert (result_path / "manifest.json").exists(), "Manifest should be migrated"
    assert not old_cache_path.exists(), "Old cache should be removed"

    # Cleanup
    import shutil
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    if old_cache_dir.exists():
        shutil.rmtree(old_cache_dir)
    test_file.unlink()

    print("  ✓ Migration works\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Smart Cache Test Suite")
    print("=" * 60 + "\n")

    try:
        test_post_quantum_hash()
        test_bloom_filter()
        test_smart_cache()
        test_migration()

        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
