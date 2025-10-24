# MCPCache - Standard 2Q Implementation (ARCHIVED)

## Status: ARCHIVED - Not Unique

This implementation uses **standard** caching techniques:
- 2Q algorithm (published 1994, used in PostgreSQL)
- Sharded architecture (Redis, Memcached do this)
- Heap-based eviction (common optimization)
- Thread pool executors (standard asyncio pattern)

## What We Built

A **well-engineered** but **not innovative** cache with:
- 500+ lines of code
- ~250 bytes overhead per entry
- Thread-safe operations
- O(log N) eviction
- TTL cleanup
- Agent learning integration

## Test Results

- Core tests: 10/10 passed ✓
- Edge cases: 12/12 passed ✓
- Performance: 60μs eviction, 11,111 ops/sec

## Why Archived

**Not lightweight enough:**
- Target: <20 bytes/entry overhead
- Actual: ~250 bytes/entry overhead (12.5x over target!)

**Not innovative:**
- All techniques are 20-30 years old
- Standard practice in industry
- Nothing novel about the architecture

## Replacement

See: `../mcpcache-bloom-trie/` for the **actually innovative** implementation with:
- Bloom filter + trie hybrid
- <20 bytes/entry overhead
- <100 lines of code
- Probabilistic eviction by security value
- Incremental learning without retraining

---

**Date Archived:** 2025-01-23
**Reason:** Not unique, not lightweight enough
**Replacement:** Bloom filter + trie hybrid cache
