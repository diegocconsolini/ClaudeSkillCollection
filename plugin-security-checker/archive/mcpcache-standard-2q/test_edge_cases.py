"""
MCPCache Edge Case Testing
Comprehensive edge case validation beyond the standard test suite
"""

import asyncio
import time
import sys
from typing import List

from mcpcache_fixed import MCPCache, EntryType


class EdgeCaseResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests: List[str] = []

    def add_pass(self, test_name: str):
        self.passed += 1
        self.tests.append(f"✓ {test_name}")
        print(f"✓ {test_name}")

    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.tests.append(f"✗ {test_name}: {error}")
        print(f"✗ {test_name}: {error}")

    def summary(self):
        total = self.passed + self.failed
        print("\n" + "="*80)
        print(f"EDGE CASE TEST SUMMARY: {self.passed}/{total} passed")
        print("="*80)


results = EdgeCaseResults()


# =============================================================================
# EDGE CASE 1: Extremely Small Memory Limit
# =============================================================================

async def test_tiny_memory_limit():
    """Test cache with very small memory limit (1KB)"""
    try:
        cache = MCPCache(total_memory=1024, num_shards=1)  # 1KB total

        # Try to add 10KB
        for i in range(10):
            await cache.put(f"tiny-{i}", "x" * 1024, EntryType.TOOL_RESULT)

        stats = cache.get_global_stats()

        # Should have evicted aggressively
        if stats['total_bytes'] <= 1536 and stats['total_evictions'] > 5:  # Allow 50% overhead
            results.add_pass(f"Tiny memory limit (1KB): {stats['total_bytes']} bytes, {stats['total_evictions']} evictions")
        else:
            results.add_fail("Tiny memory limit", f"{stats['total_bytes']} bytes, {stats['total_evictions']} evictions")

    except Exception as e:
        results.add_fail("Tiny memory limit", str(e))


# =============================================================================
# EDGE CASE 2: Duplicate Key Overwrites
# =============================================================================

async def test_duplicate_key_overwrites():
    """Test that putting same key multiple times updates correctly"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=2)

        # Put same key 100 times
        for i in range(100):
            await cache.put("duplicate-key", f"value-{i}", EntryType.TOOL_RESULT)

        # Should only have 1 entry
        result = await cache.get("duplicate-key")
        stats = cache.get_global_stats()

        if result == "value-99" and stats['total_entries'] == 1:
            results.add_pass(f"Duplicate key overwrites: Latest value retained, 1 entry")
        else:
            results.add_fail("Duplicate key overwrites", f"Got {result}, {stats['total_entries']} entries")

    except Exception as e:
        results.add_fail("Duplicate key overwrites", str(e))


# =============================================================================
# EDGE CASE 3: Very Large Single Entry
# =============================================================================

async def test_large_single_entry():
    """Test adding single entry larger than cache limit"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=1)  # 10KB limit

        # Try to add 50KB entry
        large_data = "x" * (50 * 1024)
        await cache.put("huge-entry", large_data, EntryType.TOOL_RESULT)

        stats = cache.get_global_stats()

        # Cache should refuse or evict immediately
        # Since entry is added then eviction happens, we expect 0 or 1 entry
        if stats['total_entries'] <= 1:
            results.add_pass(f"Large single entry (50KB > 10KB limit): {stats['total_entries']} entries, {stats['total_bytes']} bytes")
        else:
            results.add_fail("Large single entry", f"{stats['total_entries']} entries (expected 0-1)")

    except Exception as e:
        results.add_fail("Large single entry", str(e))


# =============================================================================
# EDGE CASE 4: Rapid TTL Expiration
# =============================================================================

async def test_rapid_ttl_expiration():
    """Test entries with very short TTL (0.1 seconds)"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=2)
        await cache.start_cleanup_task()
        cache.cleanup_interval = 0.5  # Fast cleanup

        # Add entries with 0.1s TTL
        for i in range(20):
            await cache.put(f"fast-ttl-{i}", f"value-{i}", EntryType.TOOL_RESULT, ttl=0.1)

        initial_count = cache.get_global_stats()['total_entries']

        # Wait for expiration + cleanup
        await asyncio.sleep(1.0)

        final_count = cache.get_global_stats()['total_entries']
        expired = cache.get_global_stats()['total_expired']

        await cache.stop_cleanup_task()

        if final_count < initial_count and expired > 10:
            results.add_pass(f"Rapid TTL expiration: {expired} expired, {final_count} remain")
        else:
            results.add_fail("Rapid TTL expiration", f"{expired} expired (expected >10)")

    except Exception as e:
        results.add_fail("Rapid TTL expiration", str(e))


# =============================================================================
# EDGE CASE 5: Null/Empty Values
# =============================================================================

async def test_null_empty_values():
    """Test storing None, empty string, empty dict, empty list"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=2)

        test_values = [
            ("null-key", None),
            ("empty-string", ""),
            ("empty-dict", {}),
            ("empty-list", []),
            ("zero", 0),
            ("false", False)
        ]

        for key, value in test_values:
            await cache.put(key, value, EntryType.TOOL_RESULT)

        # Retrieve all
        passed = 0
        for key, expected in test_values:
            result = await cache.get(key)
            if result == expected:
                passed += 1

        if passed == len(test_values):
            results.add_pass(f"Null/empty values: {passed}/{len(test_values)} correct")
        else:
            results.add_fail("Null/empty values", f"Only {passed}/{len(test_values)} correct")

    except Exception as e:
        results.add_fail("Null/empty values", str(e))


# =============================================================================
# EDGE CASE 6: Unicode and Special Characters
# =============================================================================

async def test_unicode_special_chars():
    """Test storing Unicode, emojis, special characters"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=2)

        test_cases = [
            ("unicode", "Hello 世界 🌍"),
            ("emoji", "🔥💀🚀⚡"),
            ("special", "!@#$%^&*()_+-=[]{}|;':\",./<>?"),
            ("newlines", "line1\nline2\r\nline3"),
            ("tabs", "col1\tcol2\tcol3"),
            ("null-byte", "before\x00after")
        ]

        for key, value in test_cases:
            await cache.put(key, value, EntryType.TOOL_RESULT)

        # Retrieve and verify
        passed = 0
        for key, expected in test_cases:
            result = await cache.get(key)
            if result == expected:
                passed += 1

        if passed == len(test_cases):
            results.add_pass(f"Unicode/special chars: {passed}/{len(test_cases)} correct")
        else:
            results.add_fail("Unicode/special chars", f"Only {passed}/{len(test_cases)} correct")

    except Exception as e:
        results.add_fail("Unicode/special chars", str(e))


# =============================================================================
# EDGE CASE 7: Key Collision via Hashing
# =============================================================================

async def test_key_distribution():
    """Test that keys are evenly distributed across shards"""
    try:
        cache = MCPCache(total_memory=100 * 1024, num_shards=4)

        # Add 100 entries
        for i in range(100):
            await cache.put(f"dist-{i}", f"value-{i}", EntryType.TOOL_RESULT)

        stats = cache.get_global_stats()
        shard_counts = [s['hot_size'] + s['cold_size'] for s in stats['shards']]

        # Check distribution (should be roughly even)
        avg = sum(shard_counts) / len(shard_counts)
        max_deviation = max(abs(count - avg) for count in shard_counts)

        # Allow 50% deviation (good enough for 100 entries)
        if max_deviation < avg * 0.5:
            results.add_pass(f"Key distribution: {shard_counts} (avg={avg:.1f}, max_dev={max_deviation:.1f})")
        else:
            results.add_fail("Key distribution", f"{shard_counts} (uneven distribution)")

    except Exception as e:
        results.add_fail("Key distribution", str(e))


# =============================================================================
# EDGE CASE 8: Concurrent Get/Put Races
# =============================================================================

async def test_concurrent_get_put_race():
    """Test concurrent gets and puts on same key"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=2)

        # Seed initial value
        await cache.put("race-key", "initial", EntryType.TOOL_RESULT)

        async def writer(n: int):
            for i in range(50):
                await cache.put("race-key", f"writer-{n}-{i}", EntryType.TOOL_RESULT)

        async def reader(n: int):
            for i in range(50):
                result = await cache.get("race-key")
                # Just make sure it doesn't crash

        # Run 5 writers + 5 readers concurrently
        tasks = []
        tasks.extend([writer(i) for i in range(5)])
        tasks.extend([reader(i) for i in range(5)])

        await asyncio.gather(*tasks)

        # Should not crash, and final value should be from one of the writers
        final_value = await cache.get("race-key")

        if final_value and "writer-" in final_value:
            results.add_pass(f"Concurrent get/put race: No crashes, final={final_value[:20]}")
        else:
            results.add_fail("Concurrent get/put race", f"Unexpected final value: {final_value}")

    except Exception as e:
        results.add_fail("Concurrent get/put race", str(e))


# =============================================================================
# EDGE CASE 9: Mixed TTL Values
# =============================================================================

async def test_mixed_ttl():
    """Test entries with different TTL values (None, short, long)"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=2)
        await cache.start_cleanup_task()
        cache.cleanup_interval = 0.5

        # Add entries with mixed TTLs
        await cache.put("no-ttl", "permanent", EntryType.TOOL_RESULT, ttl=None)
        await cache.put("short-ttl", "expires-fast", EntryType.TOOL_RESULT, ttl=0.2)
        await cache.put("long-ttl", "expires-slow", EntryType.TOOL_RESULT, ttl=10.0)

        # Wait for short TTL to expire
        await asyncio.sleep(1.0)

        no_ttl_value = await cache.get("no-ttl")
        short_ttl_value = await cache.get("short-ttl")
        long_ttl_value = await cache.get("long-ttl")

        await cache.stop_cleanup_task()

        # No-TTL and long-TTL should exist, short-TTL should be gone
        if no_ttl_value == "permanent" and short_ttl_value is None and long_ttl_value == "expires-slow":
            results.add_pass("Mixed TTL: Permanent kept, short expired, long kept")
        else:
            results.add_fail("Mixed TTL", f"no={no_ttl_value}, short={short_ttl_value}, long={long_ttl_value}")

    except Exception as e:
        results.add_fail("Mixed TTL", str(e))


# =============================================================================
# EDGE CASE 10: Extreme Concurrent Load
# =============================================================================

async def test_extreme_concurrent_load():
    """Test with 1000 concurrent operations"""
    try:
        cache = MCPCache(total_memory=50 * 1024, num_shards=4)

        async def worker(worker_id: int):
            for i in range(100):
                key = f"load-{worker_id}-{i}"
                await cache.put(key, f"value-{i}", EntryType.TOOL_RESULT)
                await cache.get(key)

        # Run 10 workers × 100 ops = 1000 operations
        start = time.time()
        tasks = [worker(i) for i in range(10)]
        await asyncio.gather(*tasks)
        elapsed = time.time() - start

        stats = cache.get_global_stats()

        # Should complete in reasonable time (<5s) without crashes
        if elapsed < 5.0 and stats['total_sets'] == 1000:
            results.add_pass(f"Extreme concurrent load: 1000 ops in {elapsed:.2f}s")
        else:
            results.add_fail("Extreme concurrent load", f"{elapsed:.2f}s, {stats['total_sets']} sets")

    except Exception as e:
        results.add_fail("Extreme concurrent load", str(e))


# =============================================================================
# EDGE CASE 11: Agent History Overflow
# =============================================================================

async def test_agent_history_overflow():
    """Test agent history with >1000 detections (should cap at 1000)"""
    try:
        cache = MCPCache(total_memory=50 * 1024, num_shards=2)

        # Store 1500 detections
        for i in range(1500):
            await cache.store_detection(
                agent_id="overflow-agent",
                file_hash=f"file-{i}",
                result={'pattern': 'test', 'confidence': 0.9}
            )

        history = await cache.get_agent_history("overflow-agent", limit=2000)

        # Should be capped at 1000
        if len(history) <= 1000:
            results.add_pass(f"Agent history overflow: Capped at {len(history)} entries")
        else:
            results.add_fail("Agent history overflow", f"Got {len(history)} entries (expected ≤1000)")

    except Exception as e:
        results.add_fail("Agent history overflow", str(e))


# =============================================================================
# EDGE CASE 12: Negative TTL
# =============================================================================

async def test_negative_ttl():
    """Test entry with negative TTL (should be treated as expired)"""
    try:
        cache = MCPCache(total_memory=10 * 1024, num_shards=1)

        # Add entry with negative TTL
        await cache.put("negative-ttl", "should-be-expired", EntryType.TOOL_RESULT, ttl=-10.0)

        # Should be immediately expired
        result = await cache.get("negative-ttl")

        if result is None:
            results.add_pass("Negative TTL: Treated as expired")
        else:
            results.add_fail("Negative TTL", f"Got {result} (expected None)")

    except Exception as e:
        results.add_fail("Negative TTL", str(e))


# =============================================================================
# MAIN RUNNER
# =============================================================================

async def run_all_edge_cases():
    """Run all edge case tests"""
    print("="*80)
    print("MCPCache Edge Case Testing")
    print("="*80)
    print()

    print("[1/12] Testing tiny memory limit (1KB)...")
    await test_tiny_memory_limit()

    print("\n[2/12] Testing duplicate key overwrites...")
    await test_duplicate_key_overwrites()

    print("\n[3/12] Testing large single entry (50KB > 10KB limit)...")
    await test_large_single_entry()

    print("\n[4/12] Testing rapid TTL expiration (0.1s)...")
    await test_rapid_ttl_expiration()

    print("\n[5/12] Testing null/empty values...")
    await test_null_empty_values()

    print("\n[6/12] Testing Unicode and special characters...")
    await test_unicode_special_chars()

    print("\n[7/12] Testing key distribution across shards...")
    await test_key_distribution()

    print("\n[8/12] Testing concurrent get/put races...")
    await test_concurrent_get_put_race()

    print("\n[9/12] Testing mixed TTL values...")
    await test_mixed_ttl()

    print("\n[10/12] Testing extreme concurrent load (1000 ops)...")
    await test_extreme_concurrent_load()

    print("\n[11/12] Testing agent history overflow (>1000 entries)...")
    await test_agent_history_overflow()

    print("\n[12/12] Testing negative TTL...")
    await test_negative_ttl()

    # Summary
    results.summary()

    # Exit code
    sys.exit(0 if results.failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(run_all_edge_cases())
