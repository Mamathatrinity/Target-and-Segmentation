# Segments Module - Validation Matrix

## Overview
This document explains which validation types (UI, API, Database) can be applied to each test case and provides reasoning for cases where certain validations are not applicable.

---

## Validation Legend
- ✅ **Applicable** - Validation can and should be performed
- ⚠️ **Partial** - Validation possible but limited or optional
- ❌ **Not Applicable** - Validation cannot or should not be performed

---

## POSITIVE TEST CASES - Validation Matrix

### TC_SEG_POS_001: View Segments List Successfully
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify page loads, elements visible, segments displayed correctly |
| API | ✅ | GET /api/segments returns 200, valid JSON response with segment array |
| Database | ✅ | Query segments table to verify count matches UI count |

**Why All Three:** This is a READ operation where we can verify data consistency across all three layers.

---

### TC_SEG_POS_002: Search Segment by Name (Exact Match)
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify search results displayed, filter applied correctly |
| API | ✅ | GET /api/segments?search=X returns filtered results with 200 status |
| Database | ✅ | SELECT * FROM segments WHERE name = 'X' to verify filtering |

**Why All Three:** Search is a filtered READ operation - we can validate filtering logic at each layer.

---

### TC_SEG_POS_003: Search Segment by Partial Name
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify partial match results displayed |
| API | ✅ | GET /api/segments?search=partial returns matching segments |
| Database | ✅ | SELECT * FROM segments WHERE name LIKE '%partial%' |

**Why All Three:** Similar to exact search, validates filtering across layers.

---

### TC_SEG_POS_004: Create New Segment Successfully
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify success message, new segment appears in list |
| API | ✅ | POST /api/segments returns 201, response contains new segment object |
| Database | ✅ | INSERT verified - new record exists with correct data |

**Why All Three:** This is a CREATE operation - critical to validate data persisted correctly through all layers.

---

### TC_SEG_POS_005: Filter Segments by "My Segments"
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify only user's segments displayed |
| API | ✅ | GET /api/segments?filter=my returns user-owned segments |
| Database | ✅ | SELECT * FROM segments WHERE created_by = {user_id} |

**Why All Three:** Filtering by ownership - validates authorization and data filtering.

---

### TC_SEG_POS_006: Filter Segments by "Team Segments"
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify only team segments displayed |
| API | ✅ | GET /api/segments?filter=team returns team segments |
| Database | ✅ | SELECT * FROM segments WHERE is_team_segment = true |

**Why All Three:** Similar to POS_005, validates filtering logic.

---

### TC_SEG_POS_007: Sort Segments by Name (A-Z)
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify segments displayed in alphabetical order |
| API | ✅ | GET /api/segments?sort=name&order=asc returns sorted array |
| Database | ❌ | **Not Applicable** - Sorting is done in API/application layer, DB query may be unsorted |

**Why No DB:** Database query might use ORDER BY, but API layer handles final sorting. Validating DB query order is redundant when API sorting is already tested.

---

### TC_SEG_POS_008: Sort Segments by Created Date (Newest First)
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify segments displayed with newest first |
| API | ✅ | GET /api/segments?sort=created_date&order=desc |
| Database | ✅ | Can verify ORDER BY created_date DESC in query |

**Why All Three:** Date sorting is often done at DB level for performance, so all three validations make sense.

---

### TC_SEG_POS_009: View Segment Details
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify all segment details displayed correctly |
| API | ✅ | GET /api/segments/{id} returns 200 with complete segment data |
| Database | ✅ | SELECT * FROM segments WHERE id = {id} to verify data matches |

**Why All Three:** READ operation for single record - validates data consistency.

---

### TC_SEG_POS_010: Pagination - Navigate to Next Page
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify next page of segments displayed, page number updated |
| API | ✅ | GET /api/segments?page=2 returns second page data |
| Database | ✅ | Can verify OFFSET/LIMIT in query: SELECT * FROM segments LIMIT 8 OFFSET 8 |

**Why All Three:** Pagination logic can be validated at each layer.

---

### TC_SEG_POS_011: Pagination - Navigate to Previous Page
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify previous page displayed |
| API | ✅ | GET /api/segments?page=1 returns first page |
| Database | ✅ | Verify query with correct OFFSET |

**Why All Three:** Same as POS_010.

---

### TC_SEG_POS_012: Change Records Per Page (8 to 16)
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify 16 segment cards displayed |
| API | ✅ | GET /api/segments?per_page=16 returns 16 records |
| Database | ❌ | **Not Applicable** - LIMIT is set in API layer, DB just returns requested count |

**Why No DB:** Database validation is redundant - if API requests 16 and returns 16, DB query worked correctly.

---

### TC_SEG_POS_013: Edit Segment Name and Description
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify updated data displayed |
| API | ✅ | PUT /api/segments/{id} returns 200, updated object returned |
| Database | ✅ | UPDATE verified - record has new values |

**Why All Three:** UPDATE operation - critical to validate data changed correctly.

---

### TC_SEG_POS_014: Delete Segment Successfully
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify segment removed from list |
| API | ✅ | DELETE /api/segments/{id} returns 204 No Content |
| Database | ✅ | DELETE verified - record no longer exists or is_deleted = true |

**Why All Three:** DELETE operation - must verify data removed from all layers.

---

### TC_SEG_POS_015: Toggle Team Segment ON
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify team segment badge/indicator visible |
| API | ✅ | POST /api/segments with is_team_segment=true |
| Database | ✅ | Verify is_team_segment column = true |

**Why All Three:** Feature flag that affects data model - validate across layers.

---

## NEGATIVE TEST CASES - Validation Matrix

### TC_SEG_NEG_001: Create Segment with Empty Name
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify error message displayed, form not submitted |
| API | ✅ | POST /api/segments returns 400 Bad Request with error details |
| Database | ✅ | Verify NO new record created (count unchanged) |

**Why All Three:** Validation happens at multiple layers - UI prevents submission, API validates, DB should not receive invalid data.

---

### TC_SEG_NEG_002: Create Segment with Duplicate Name
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify error message displayed |
| API | ✅ | POST /api/segments returns 409 Conflict |
| Database | ✅ | Verify duplicate record NOT created, unique constraint enforced |

**Why All Three:** Uniqueness constraint exists at DB level, but should be validated at all layers for good UX.

---

### TC_SEG_NEG_003: Create Segment with Name Exceeding Max Length
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify error message or character limit enforced |
| API | ✅ | POST /api/segments returns 400 Bad Request |
| Database | ❌ | **Not Applicable** - Validation prevents data from reaching DB |

**Why No DB:** If UI and API validation work correctly, invalid data never reaches database. Testing DB constraint is redundant and requires bypassing app logic.

---

### TC_SEG_NEG_004: Create Segment with Special Characters in Name
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify validation or sanitization applied |
| API | ✅ | POST /api/segments handles special characters safely |
| Database | ✅ | Verify no XSS payloads stored as-is, data sanitized |

**Why All Three:** Security test - must verify sanitization at each layer to prevent XSS/injection attacks.

---

### TC_SEG_NEG_005: Search with Non-Existent Segment Name
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify empty state message displayed |
| API | ✅ | GET /api/segments?search=NONEXISTENT returns empty array |
| Database | ✅ | Verify query returns 0 rows |

**Why All Three:** Valid scenario - validates that "no results" is handled correctly at all layers.

---

### TC_SEG_NEG_006: Search with SQL Injection Attempt
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify no crash, safe error handling |
| API | ✅ | GET /api/segments with injection returns 400 or empty safely |
| Database | ✅ | Verify segments table intact, parameterized queries used |

**Why All Three:** **Critical security test** - must validate SQL injection prevention at all layers.

---

### TC_SEG_NEG_007: Delete Segment Without Permission
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify delete button disabled/hidden |
| API | ✅ | DELETE /api/segments/{id} returns 403 Forbidden |
| Database | ✅ | Verify segment record unchanged (authorization check before DELETE) |

**Why All Three:** **Authorization test** - validates permission checks at each layer.

---

### TC_SEG_NEG_008: Edit Segment Owned by Another User
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify edit disabled or error shown |
| API | ✅ | PUT /api/segments/{id} returns 403 Forbidden |
| Database | ✅ | Verify segment record unchanged |

**Why All Three:** **Authorization test** - similar to NEG_007.

---

### TC_SEG_NEG_009: Access Segments Page Without Authentication
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify redirect to login page |
| API | ✅ | GET /api/segments returns 401 Unauthorized |
| Database | ❌ | **Not Applicable** - Authentication happens before DB access |

**Why No DB:** If authentication fails at API layer, database is never queried. No need to validate DB behavior.

---

### TC_SEG_NEG_010: Create Segment Without Selecting HCP Universe
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify error message displayed |
| API | ✅ | POST /api/segments returns 400 Bad Request |
| Database | ✅ | Verify no record created with NULL hcp_universe_id |

**Why All Three:** Required field validation - validates NOT NULL constraint.

---

### TC_SEG_NEG_011: Navigate to Invalid Page Number (Page 9999)
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify graceful handling, no crash |
| API | ✅ | GET /api/segments?page=9999 returns empty or redirects |
| Database | ❌ | **Not Applicable** - Pagination logic in API, DB just executes OFFSET |

**Why No DB:** Database will execute query with large OFFSET and return 0 rows. Testing this at DB level doesn't add value beyond API test.

---

### TC_SEG_NEG_012: Filter with Invalid Filter Option
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify graceful error handling |
| API | ✅ | GET /api/segments?filter=INVALID returns 400 or default |
| Database | ❌ | **Not Applicable** - Filter validation happens in API layer |

**Why No DB:** Invalid filter is handled by API before building DB query.

---

## EDGE TEST CASES - Validation Matrix

### TC_SEG_EDGE_001: Create Segment with Name Containing Only Spaces
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify error message displayed |
| API | ✅ | POST /api/segments returns 400 after trimming |
| Database | ✅ | Verify no record created with empty/whitespace name |

**Why All Three:** Tests trimming and validation logic at each layer.

---

### TC_SEG_EDGE_002: Create Segment with Minimum Valid Name Length
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify success or validation based on rules |
| API | ✅ | POST /api/segments returns 201 or 400 |
| Database | ✅ | If created, verify record has 1-char name |

**Why All Three:** Boundary test - validates minimum length enforcement.

---

### TC_SEG_EDGE_003: Create Segment with Name at Exact Max Length
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify full name displayed |
| API | ✅ | POST /api/segments returns 201 |
| Database | ✅ | Verify VARCHAR(255) stores full name without truncation |

**Why All Three:** Boundary test - validates maximum length storage.

---

### TC_SEG_EDGE_004: Search with Very Long Search String
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify search handled gracefully |
| API | ✅ | GET /api/segments?search=<long> doesn't timeout |
| Database | ⚠️ | **Partial** - Can verify query doesn't cause performance issues, but not always necessary |

**Why Partial DB:** Database will execute LIKE query, but performance testing is usually done at API level. DB validation optional.

---

### TC_SEG_EDGE_005: Rapidly Toggle Team Segment Switch
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify toggle in correct final state |
| API | ✅ | Verify debouncing - not called multiple times |
| Database | ❌ | **Not Applicable** - No save action yet, toggle is UI-only |

**Why No DB:** Toggle doesn't trigger save until user submits form. Database not involved in UI toggle behavior.

---

### TC_SEG_EDGE_006: Create Segment During Network Interruption
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify error message displayed |
| API | ✅ | POST /api/segments times out or returns network error |
| Database | ✅ | Verify NO partial record created |

**Why All Three:** Tests transaction integrity - ensures no orphaned data if request fails mid-flight.

---

### TC_SEG_EDGE_007: Open Multiple Segment Detail Pages Simultaneously
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify each tab shows correct data |
| API | ✅ | Each tab makes separate GET /api/segments/{id} |
| Database | ✅ | Queries return correct data per segment_id |

**Why All Three:** Tests session isolation and concurrent reads.

---

### TC_SEG_EDGE_008: Create Segment with Unicode/Emoji in Name
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify name displayed correctly |
| API | ✅ | POST /api/segments handles Unicode |
| Database | ✅ | UTF-8/UTF8MB4 encoding stores data correctly |

**Why All Three:** Character encoding test - validates across all layers.

---

### TC_SEG_EDGE_009: Delete Last Segment in List
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify empty state shown |
| API | ✅ | DELETE /api/segments/{id} returns 204 |
| Database | ✅ | Verify table empty or count = 0 |

**Why All Three:** Edge case for empty state handling.

---

### TC_SEG_EDGE_010: Navigate Between Pages Rapidly
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify correct page displayed at end |
| API | ✅ | Verify requests debounced/cancelled properly |
| Database | ❌ | **Not Applicable** - Performance test at API level |

**Why No DB:** Database executes queries as received. Testing rapid pagination is about API request handling, not DB.

---

### TC_SEG_EDGE_011: Edit Segment and Cancel Without Saving
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify original data displayed |
| API | ✅ | Verify no PUT request made |
| Database | ✅ | Verify segment data unchanged |

**Why All Three:** Tests cancel functionality - ensures no unintended changes.

---

### TC_SEG_EDGE_012: Search with Case Variations
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify same results for all cases |
| API | ✅ | GET /api/segments?search=<text> is case-insensitive |
| Database | ✅ | Verify query uses LOWER() or case-insensitive collation |

**Why All Three:** Tests case-insensitivity across layers.

---

### TC_SEG_EDGE_013: Refresh Page During Segment Load
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify clean reload, no errors |
| API | ✅ | Previous request cancelled, new request made |
| Database | ❌ | **Not Applicable** - GET is idempotent, DB behavior unchanged |

**Why No DB:** Database executes SELECT queries regardless of page refresh. No state change to validate.

---

### TC_SEG_EDGE_014: Create 100+ Segments and Test Performance
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify page loads within acceptable time |
| API | ✅ | GET /api/segments responds quickly |
| Database | ✅ | Verify query optimized with indexes, execution time < threshold |

**Why All Three:** **Performance test** - must validate at all layers to identify bottlenecks.

---

### TC_SEG_EDGE_015: Simultaneous Edits by Two Users
| Validation | Status | Reasoning |
|------------|--------|-----------|
| UI | ✅ | Verify warning or success based on implementation |
| API | ✅ | PUT /api/segments/{id} handles concurrent edits |
| Database | ✅ | Verify final state consistent, optimistic locking or last-write-wins |

**Why All Three:** **Concurrency test** - validates race condition handling.

---

## Validation Summary by Type

### Cases Where UI + API + DB All Applicable: 30 cases
These are typically:
- CREATE operations (data persistence critical)
- UPDATE operations (data modification must be validated)
- DELETE operations (data removal must be verified)
- Security tests (SQL injection, XSS, authorization)
- Data integrity tests (duplicates, constraints)
- Concurrency tests

### Cases Where DB Validation is NOT Applicable: 10 cases
**Reasons:**
1. **Validation Prevents DB Access** (NEG_003) - Invalid data never reaches DB
2. **Authentication Failures** (NEG_009) - DB never queried if auth fails
3. **Pagination/Sorting Logic** (POS_007, POS_012, NEG_011) - Handled in app layer
4. **UI-Only Behavior** (EDGE_005, EDGE_010, EDGE_013) - No DB interaction
5. **Filter Validation** (NEG_012) - Invalid filters handled before DB query

### Cases Where DB Validation is Partial/Optional: 1 case
- **EDGE_004** - Long search string performance can be tested at DB but usually done at API

---

## Key Principles

### When to Include DB Validation:
✅ **CREATE/UPDATE/DELETE operations** - Verify data persistence  
✅ **Data integrity constraints** - Verify NOT NULL, UNIQUE, FOREIGN KEY  
✅ **Security tests** - Verify SQL injection prevention, parameterized queries  
✅ **Authorization tests** - Verify row-level security if implemented  
✅ **Concurrency tests** - Verify locking, transaction isolation  
✅ **Data consistency** - Verify UI matches DB state  

### When to Skip DB Validation:
❌ **UI-only behavior** - Toggles, dropdowns, navigation before save  
❌ **Validation preventing DB access** - Invalid data rejected at API layer  
❌ **Authentication failures** - DB never queried  
❌ **Sorting/Pagination done in app** - DB returns unsorted/unpaged data  
❌ **Idempotent reads** - GET operations don't change DB state  
❌ **Client-side logic** - Debouncing, request cancellation  

---

## Testing Strategy Recommendations

### Priority 1: HIGH Priority Test Cases with All 3 Validations
Focus on critical paths:
- POS_001 (View list)
- POS_004 (Create)
- POS_013 (Edit)
- POS_014 (Delete)
- NEG_001 (Empty name)
- NEG_002 (Duplicate)
- NEG_006 (SQL injection)
- NEG_007, NEG_008 (Authorization)

### Priority 2: MEDIUM Priority Test Cases
Expand coverage:
- Filtering (POS_005, POS_006)
- Sorting (POS_008)
- Pagination (POS_010, POS_011)
- Security (NEG_004)
- Edge cases (EDGE_001, EDGE_006, EDGE_015)

### Priority 3: LOW Priority Test Cases
Complete coverage:
- Boundary tests (EDGE_002, EDGE_003)
- Unicode (EDGE_008)
- Performance (EDGE_014)

---

## Database Validation Query Examples

```sql
-- POS_001: Verify segment count
SELECT COUNT(*) as total_segments FROM segments WHERE is_deleted = false;

-- POS_004: Verify new segment created
SELECT * FROM segments WHERE id = {new_segment_id};

-- NEG_002: Verify duplicate not created
SELECT COUNT(*) FROM segments WHERE name = 'Duplicate Name';

-- NEG_006: Verify SQL injection didn't corrupt data
SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'segments';

-- POS_005: Verify "My Segments" filter
SELECT * FROM segments WHERE created_by = {user_id} AND is_deleted = false;

-- EDGE_015: Verify concurrent edit final state
SELECT name, updated_at, updated_by FROM segments WHERE id = {segment_id};
```

---

## Conclusion

**40 Total Test Cases:**
- **30 cases** require all 3 validations (UI + API + DB)
- **9 cases** require only UI + API validations
- **1 case** has partial/optional DB validation

This comprehensive approach ensures:
1. **Data Integrity** - Validated across all layers
2. **Security** - Injection and authorization tested
3. **Performance** - Bottlenecks identified
4. **User Experience** - Error handling and edge cases covered
5. **Efficiency** - Skipping redundant DB tests where not needed
