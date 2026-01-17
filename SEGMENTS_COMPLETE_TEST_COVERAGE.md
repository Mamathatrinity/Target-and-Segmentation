# Segments Module - Complete Test Coverage & Validation Analysis

**Date:** January 16, 2026  
**Status:** Comprehensive test case mapping with UI/API/DB validation analysis

---

## 📊 API Endpoints Available

```
GET    /api/segments                - List segments (paginated)
GET    /api/segments/{id}           - Get segment details
POST   /api/segments                - Create new segment
PUT    /api/segments/{id}           - Update segment
DELETE /api/segments/{id}           - Delete segment
GET    /api/segments/search         - Search segments
```

## 🗄️ Database Schema

```sql
segments Table:
- id (PK)
- name
- description
- brand_id
- created_by
- is_team_segment (boolean)
- created_at
- updated_at
- status
- hcp_universe_id
- is_deleted (soft delete)
```

---

## ✅ POSITIVE TEST CASES (15 Total)

### TC_SEG_POS_001: View Segments List
**Priority:** Critical  
**Validations:**
- ✅ **UI**: Segment cards visible, count matches
- ✅ **API**: GET /api/segments returns 200, data structure valid
- ✅ **DB**: SELECT COUNT(*) matches UI/API count

**Why All 3 Possible:**
- UI shows visual representation (can count cards)
- API provides data programmatically (can validate response)
- DB is source of truth (can query directly)

---

### TC_SEG_POS_002: Search Segment by Name
**Priority:** High  
**Validations:**
- ✅ **UI**: Search field accepts input, results filter correctly
- ✅ **API**: GET /api/segments?search=term returns matching results
- ✅ **DB**: SELECT * WHERE name LIKE '%term%' verifies search logic

**Why All 3 Possible:**
- UI provides search interaction
- API supports search parameter
- DB can verify search query logic

---

### TC_SEG_POS_003: Create New Segment
**Priority:** Critical  
**Validations:**
- ✅ **UI**: Form submission, success message, new segment appears in list
- ✅ **API**: POST /api/segments returns 201, segment_id returned
- ✅ **DB**: SELECT * WHERE id = new_id verifies record created

**Why All 3 Possible:**
- UI provides creation form
- API creates record programmatically
- DB stores the actual data

---

### TC_SEG_POS_004: Filter by "My Segments"
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Filter dropdown selection, only user's segments shown
- ✅ **API**: GET /api/segments?filter=my_segments returns user's segments
- ✅ **DB**: SELECT * WHERE created_by = {user_id} verifies ownership

**Why All 3 Possible:**
- UI filter controls exist
- API supports filter parameter
- DB can query by user

---

### TC_SEG_POS_005: Filter by "Team Segments"
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Filter shows only team segments
- ✅ **API**: GET /api/segments?filter=team_segments returns team segments
- ✅ **DB**: SELECT * WHERE is_team_segment = true verifies flag

**Why All 3 Possible:**
- UI filter controls exist
- API supports filter parameter
- DB has is_team_segment column

---

### TC_SEG_POS_006: Sort by Name (Ascending)
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Segment names displayed in alphabetical order
- ✅ **API**: GET /api/segments?sort_by=name&order=asc returns sorted data
- ✅ **DB**: SELECT * ORDER BY name ASC verifies sort logic

**Why All 3 Possible:**
- UI displays sorted list visually
- API supports sort parameters
- DB can execute ORDER BY queries

---

### TC_SEG_POS_007: Sort by Created Date (Newest First)
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Segments ordered by date visually
- ✅ **API**: GET /api/segments?sort_by=created_at&order=desc
- ✅ **DB**: SELECT * ORDER BY created_at DESC

**Why All 3 Possible:**
- UI shows dates/order
- API supports date sorting
- DB has created_at column

---

### TC_SEG_POS_008: Pagination - Navigate to Next Page
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Next button click, new segments displayed, page number updates
- ✅ **API**: GET /api/segments?page=2&page_size=8 returns page 2 data
- ✅ **DB**: SELECT * LIMIT 8 OFFSET 8 verifies pagination logic

**Why All 3 Possible:**
- UI has pagination controls
- API supports page/page_size parameters
- DB can query with LIMIT/OFFSET

---

### TC_SEG_POS_009: Pagination - Navigate to Previous Page
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Previous button click, previous segments displayed
- ✅ **API**: GET /api/segments?page=1&page_size=8
- ✅ **DB**: SELECT * LIMIT 8 OFFSET 0

**Why All 3 Possible:**
- Same as POS_008, reverse direction

---

### TC_SEG_POS_010: Change Records Per Page
**Priority:** Low  
**Validations:**
- ✅ **UI**: Dropdown selection, 16 segments displayed instead of 8
- ✅ **API**: GET /api/segments?page_size=16
- ✅ **DB**: Can verify with SELECT * LIMIT 16

**Why All 3 Possible:**
- UI has per-page dropdown
- API supports page_size parameter
- DB can query any limit

---

### TC_SEG_POS_011: View Segment Details
**Priority:** High  
**Validations:**
- ✅ **UI**: Click segment card, details page loads with all fields
- ✅ **API**: GET /api/segments/{id} returns complete segment data
- ✅ **DB**: SELECT * WHERE id = {id} verifies all fields

**Why All 3 Possible:**
- UI shows details page
- API has get-by-id endpoint
- DB stores all segment data

---

### TC_SEG_POS_012: Edit Segment Name
**Priority:** Critical  
**Validations:**
- ✅ **UI**: Edit form, save button, updated name displayed
- ✅ **API**: PUT /api/segments/{id} returns 200, updated fields
- ✅ **DB**: SELECT * WHERE id = {id} shows new name, updated_at timestamp changed

**Why All 3 Possible:**
- UI provides edit form
- API has update endpoint
- DB records are updated

---

### TC_SEG_POS_013: Delete Segment (Soft Delete)
**Priority:** Critical  
**Validations:**
- ✅ **UI**: Delete button, confirmation dialog, segment removed from list
- ✅ **API**: DELETE /api/segments/{id} returns 200 OR GET returns 404
- ✅ **DB**: SELECT * WHERE id = {id} shows is_deleted = true

**Why All 3 Possible:**
- UI has delete button
- API has delete endpoint
- DB uses soft delete flag

---

### TC_SEG_POS_014: Toggle Team Segment ON
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Toggle switch changes state, segment moves to team tab
- ✅ **API**: PUT /api/segments/{id} with is_team_segment = true
- ✅ **DB**: SELECT is_team_segment WHERE id = {id} shows true

**Why All 3 Possible:**
- UI has toggle control
- API supports field update
- DB has boolean column

---

### TC_SEG_POS_015: Combined Filter + Sort
**Priority:** Low  
**Validations:**
- ✅ **UI**: Select "My Segments" + Sort by "Name", results filtered AND sorted
- ✅ **API**: GET /api/segments?filter=my_segments&sort_by=name&order=asc
- ✅ **DB**: SELECT * WHERE created_by = {user} ORDER BY name ASC

**Why All 3 Possible:**
- UI supports combined operations
- API accepts multiple query params
- DB can handle WHERE + ORDER BY

---

## ❌ NEGATIVE TEST CASES (12 Total)

### TC_SEG_NEG_001: Create Segment with Empty Name
**Priority:** High  
**Validations:**
- ✅ **UI**: Error message "Name is required" displayed, form not submitted
- ✅ **API**: POST /api/segments with name="" returns 400 Bad Request
- ❌ **DB**: N/A - Validation happens in UI/API layer, DB never reached

**Why DB Not Possible:**
- Request rejected before reaching database
- DB has NOT NULL constraint but never tested if UI/API prevent it

---

### TC_SEG_NEG_002: Create Segment with Duplicate Name
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Error message "Segment name already exists"
- ✅ **API**: POST returns 409 Conflict or 400 with error message
- ✅ **DB**: Can query to verify duplicate wasn't created

**Why DB Possible:**
- Can verify uniqueness constraint wasn't violated
- Can check no duplicate record inserted

---

### TC_SEG_NEG_003: Create Segment with Name > 255 Characters
**Priority:** Low  
**Validations:**
- ✅ **UI**: Input field limits characters OR shows validation error
- ✅ **API**: POST returns 400 "Name too long"
- ❌ **DB**: N/A - Validation in UI/API layer

**Why DB Not Possible:**
- DB has VARCHAR(255) constraint but validation happens before insert

---

### TC_SEG_NEG_004: Search with Special Characters / SQL Injection
**Priority:** Critical (Security)  
**Validations:**
- ✅ **UI**: Search term displayed correctly, no error, safe results
- ✅ **API**: GET /api/segments?search=' OR '1'='1 returns 200, no injection
- ✅ **DB**: SELECT * WHERE name LIKE '%' OR '1'='1%' - verify prepared statements used

**Why DB Possible:**
- Can verify database wasn't corrupted
- Can check query didn't return all records maliciously
- Can validate prepared statements prevent injection

---

### TC_SEG_NEG_005: Access Segment Without Permission
**Priority:** High (Security)  
**Validations:**
- ✅ **UI**: 403 Forbidden page OR error message shown
- ✅ **API**: GET /api/segments/{other_user_segment_id} returns 403
- ⚠️ **DB**: PARTIAL - Can verify record exists but can't validate authorization logic

**Why DB Partial:**
- DB doesn't enforce row-level security (application layer does)
- Can verify record exists but can't test permission rules

---

### TC_SEG_NEG_006: Delete Already Deleted Segment
**Priority:** Low  
**Validations:**
- ✅ **UI**: Error message "Segment not found" or disabled delete button
- ✅ **API**: DELETE /api/segments/{deleted_id} returns 404 Not Found
- ✅ **DB**: SELECT is_deleted WHERE id = {id} shows true (already deleted)

**Why DB Possible:**
- Can verify soft delete flag state
- Can confirm no duplicate delete operation

---

### TC_SEG_NEG_007: Update Segment with Invalid Data
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Validation errors shown for each invalid field
- ✅ **API**: PUT /api/segments/{id} returns 400 with error details
- ❌ **DB**: N/A - Invalid data rejected before reaching DB

**Why DB Not Possible:**
- Validation happens in UI/API layer

---

### TC_SEG_NEG_008: Pagination with Invalid Page Number (page=-1)
**Priority:** Low  
**Validations:**
- ✅ **UI**: Either redirects to page 1 OR shows error
- ✅ **API**: GET /api/segments?page=-1 returns 400 or defaults to page 1
- ❌ **DB**: N/A - API handles parameter validation

**Why DB Not Possible:**
- Parameter validation in API layer
- DB would execute query but API shouldn't pass invalid params

---

### TC_SEG_NEG_009: Sort with Invalid Sort Field
**Priority:** Low  
**Validations:**
- ✅ **UI**: Dropdown only allows valid options (prevents invalid input)
- ✅ **API**: GET /api/segments?sort_by=invalid_field returns 400 or defaults
- ⚠️ **DB**: PARTIAL - Can detect SQL error if injection attempted

**Why DB Partial:**
- UI dropdown prevents invalid input
- API should validate before query
- DB would error on invalid column but shouldn't be tested this way

---

### TC_SEG_NEG_010: Filter with Invalid Filter Type
**Priority:** Low  
**Validations:**
- ✅ **UI**: Dropdown only allows valid filters
- ✅ **API**: GET /api/segments?filter=INVALID returns 400 or defaults to all
- ❌ **DB**: N/A - Filter logic in application layer

**Why DB Not Possible:**
- Filter mapping done in API/application code
- DB doesn't know about "my_segments" filter concept

---

### TC_SEG_NEG_011: Concurrent Edit Conflict
**Priority:** Medium  
**Validations:**
- ⚠️ **UI**: PARTIAL - May show "Segment was updated by another user" message
- ✅ **API**: PUT with old timestamp returns 409 Conflict (optimistic locking)
- ✅ **DB**: SELECT updated_at WHERE id = {id} shows later timestamp

**Why UI Partial:**
- Requires two browser sessions/users
- Complex to automate in single test
- Better tested via API

**Why API/DB Possible:**
- Can simulate with two API requests
- DB shows final state and can verify locking

---

### TC_SEG_NEG_012: Unauthorized API Access (No JWT Token)
**Priority:** Critical (Security)  
**Validations:**
- ⚠️ **UI**: PARTIAL - Browser handles auth, hard to test "no token" state
- ✅ **API**: GET /api/segments without Authorization header returns 401
- ❌ **DB**: N/A - Authentication in API layer

**Why UI Partial:**
- Application automatically includes JWT
- Would need to manually remove from browser storage
- Better tested via API

**Why DB Not Possible:**
- Authentication happens before database access

---

## 🔄 EDGE TEST CASES (15 Total)

### TC_SEG_EDGE_001: View with Exactly 0 Segments
**Priority:** Medium  
**Validations:**
- ✅ **UI**: "No segments found" message displayed
- ✅ **API**: GET /api/segments returns 200, empty array, total = 0
- ✅ **DB**: SELECT COUNT(*) = 0

**Why All 3 Possible:**
- UI shows empty state
- API returns empty result set
- DB can verify zero records

---

### TC_SEG_EDGE_002: View with Exactly 1 Segment
**Priority:** Low  
**Validations:**
- ✅ **UI**: Single segment card displayed
- ✅ **API**: Returns array with 1 item
- ✅ **DB**: COUNT = 1

**Why All 3 Possible:**
- Boundary case for minimum data

---

### TC_SEG_EDGE_003: View with Exactly 8 Segments (One Full Page)
**Priority:** Medium  
**Validations:**
- ✅ **UI**: 8 segments, pagination controls may be hidden/disabled
- ✅ **API**: Returns 8 items, total = 8
- ✅ **DB**: COUNT = 8

**Why All 3 Possible:**
- Tests page boundary exactly

---

### TC_SEG_EDGE_004: View with 9 Segments (Triggers Pagination)
**Priority:** Medium  
**Validations:**
- ✅ **UI**: 8 on page 1, 1 on page 2, Next button enabled
- ✅ **API**: page=1 returns 8, page=2 returns 1
- ✅ **DB**: COUNT = 9

**Why All 3 Possible:**
- Tests pagination trigger point

---

### TC_SEG_EDGE_005: Create Segment with Name = 255 Characters (Max Length)
**Priority:** Low  
**Validations:**
- ✅ **UI**: Input accepts exactly 255 chars
- ✅ **API**: POST with 255 char name returns 201
- ✅ **DB**: SELECT LENGTH(name) = 255

**Why All 3 Possible:**
- Tests maximum valid input

---

### TC_SEG_EDGE_006: Create Segment with Name = 1 Character (Min Length)
**Priority:** Low  
**Validations:**
- ✅ **UI**: Accepts single character
- ✅ **API**: POST returns 201
- ✅ **DB**: SELECT LENGTH(name) = 1

**Why All 3 Possible:**
- Tests minimum valid input

---

### TC_SEG_EDGE_007: Search with Empty String
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Either shows all segments OR no results OR validation message
- ✅ **API**: GET /api/segments?search= behavior defined (return all or none)
- ✅ **DB**: Can verify behavior matches

**Why All 3 Possible:**
- Edge case for search input

---

### TC_SEG_EDGE_008: Paginate to Last Page with Partial Results
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Last page shows < 8 segments, Next button disabled
- ✅ **API**: Returns remaining items (e.g., 3 of 8)
- ✅ **DB**: Can calculate OFFSET and verify

**Why All 3 Possible:**
- Common pagination edge case

---

### TC_SEG_EDGE_009: Delete Last Segment on Page 2
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Auto-redirect to page 1 OR show empty page
- ✅ **API**: DELETE + GET page=2 returns empty or redirects
- ✅ **DB**: Verify segment is_deleted = true

**Why All 3 Possible:**
- Tests pagination after delete

---

### TC_SEG_EDGE_010: Create 1000+ Segments (Performance)
**Priority:** Low  
**Validations:**
- ⚠️ **UI**: PARTIAL - May timeout, pagination should still work
- ✅ **API**: GET /api/segments should paginate efficiently
- ✅ **DB**: SELECT with LIMIT/OFFSET should perform well with indexes

**Why UI Partial:**
- Load time may exceed reasonable limits
- Focus on pagination performance, not initial load

**Why API/DB Possible:**
- Can test response time with large datasets
- Can verify query performance with EXPLAIN

---

### TC_SEG_EDGE_011: Rapid Create/Delete (Race Condition)
**Priority:** Low  
**Validations:**
- ⚠️ **UI**: PARTIAL - Hard to automate rapid clicks
- ✅ **API**: Send multiple POST/DELETE concurrently
- ✅ **DB**: Verify final state consistency

**Why UI Partial:**
- Race conditions better tested programmatically
- UI can't click fast enough to test true concurrency

**Why API/DB Possible:**
- Can send concurrent requests
- DB transactions ensure consistency

---

### TC_SEG_EDGE_012: Unicode/Emoji in Segment Name
**Priority:** Medium  
**Validations:**
- ✅ **UI**: Unicode displays correctly
- ✅ **API**: POST/GET handles UTF-8 correctly
- ✅ **DB**: Stores/retrieves UTF-8 correctly

**Why All 3 Possible:**
- End-to-end character encoding test

---

### TC_SEG_EDGE_013: Sort with NULL Values
**Priority:** Low  
**Validations:**
- ⚠️ **UI**: PARTIAL - May not display NULL prominently
- ✅ **API**: GET with sort handles NULLs (NULLS FIRST/LAST)
- ✅ **DB**: SELECT ORDER BY handles NULL positioning

**Why UI Partial:**
- NULL values may not be visually obvious
- Application might prevent NULLs in required fields

**Why API/DB Possible:**
- Can verify NULL sorting behavior

---

### TC_SEG_EDGE_014: Filter with User Having Zero Segments
**Priority:** Medium  
**Validations:**
- ✅ **UI**: "No segments" message when filtering "My Segments"
- ✅ **API**: GET /api/segments?filter=my_segments returns empty array
- ✅ **DB**: SELECT WHERE created_by = {user_id} returns zero rows

**Why All 3 Possible:**
- Valid empty result set

---

### TC_SEG_EDGE_015: Browser Refresh During Edit
**Priority:** Low  
**Validations:**
- ⚠️ **UI**: PARTIAL - Form data may be lost or restored (browser behavior)
- ❌ **API**: N/A - No API call during refresh
- ✅ **DB**: Verify no partial/orphaned data created

**Why UI Partial:**
- Browser-specific behavior
- May have auto-save feature or lose data

**Why API Not Applicable:**
- Refresh doesn't trigger API
- Only matters if auto-save enabled

**Why DB Possible:**
- Can verify data integrity after interruption

---

## 📊 VALIDATION COVERAGE SUMMARY

### By Validation Type

| Validation Type | Positive | Negative | Edge | Total |
|----------------|----------|----------|------|-------|
| **UI Only** | 0 | 0 | 0 | 0 |
| **API Only** | 0 | 1 | 1 | 2 |
| **DB Only** | 0 | 0 | 0 | 0 |
| **UI + API** | 0 | 2 | 0 | 2 |
| **UI + DB** | 0 | 0 | 0 | 0 |
| **API + DB** | 0 | 1 | 0 | 1 |
| **UI + API + DB** | 15 | 3 | 10 | 28 |
| **Partial/Mixed** | 0 | 5 | 4 | 9 |
| **TOTAL** | **15** | **12** | **15** | **42** |

### Why Some Tests Can't Use All 3 Validations

#### 1. **Validation Happens Before Database (10 cases)**
- Empty name, name too long, invalid data
- **Reason**: UI/API reject before INSERT/UPDATE
- **Validation**: UI + API only

#### 2. **Authorization/Authentication Logic (2 cases)**
- Unauthorized access, no JWT token
- **Reason**: Security layer above database
- **Validation**: API only (UI always has token)

#### 3. **Application Business Logic (5 cases)**
- Filter types, sort fields, pagination params
- **Reason**: Mapping done in application code, not DB
- **Validation**: UI + API only

#### 4. **Concurrent Operations (2 cases)**
- Race conditions, concurrent edits
- **Reason**: UI can't automate fast enough
- **Validation**: API + DB (UI partial)

#### 5. **Performance/Load Tests (2 cases)**
- 1000+ segments, rapid operations
- **Reason**: UI may timeout, focus on API/DB performance
- **Validation**: API + DB (UI partial)

#### 6. **Browser-Specific Behavior (1 case)**
- Browser refresh during edit
- **Reason**: Not API-triggered event
- **Validation**: UI + DB only (API N/A)

---

## 🎯 RECOMMENDED VALIDATION STRATEGY

### **Critical Tests (Must Have All 3)**
1. View segments list
2. Create segment
3. Edit segment
4. Delete segment
5. Search functionality

**Why:** Core CRUD operations, data integrity critical

### **High Priority (UI + API Required)**
1. All filter operations
2. All sort operations
3. Pagination navigation
4. Form validations

**Why:** User-facing features, API correctness critical

### **Medium Priority (API + DB Sufficient)**
1. Concurrent operations
2. Performance tests
3. Security tests (SQL injection, XSS)

**Why:** Better tested programmatically than through UI

### **Low Priority (Flexible Validation)**
1. Edge cases with small data sets
2. Unicode/special characters
3. Boundary value tests

**Why:** Can verify with any available layer

---

## 🚀 IMPLEMENTATION PRIORITY

### Phase 1: Foundation (Week 1)
- Positive tests 1-6 (Core CRUD + basic operations)
- All with UI + API + DB validation

### Phase 2: Advanced Features (Week 2)
- Positive tests 7-15 (Sorting, pagination, filtering)
- All with UI + API + DB validation

### Phase 3: Negative Scenarios (Week 3)
- NEG_001 to NEG_006 (Critical validations)
- Focus on API + UI for input validation

### Phase 4: Security & Edge Cases (Week 4)
- NEG_007 to NEG_012 (Security tests)
- EDGE_001 to EDGE_008 (Common edge cases)
- Mix of validation types based on scenario

### Phase 5: Advanced Edge Cases (Week 5)
- EDGE_009 to EDGE_015 (Complex scenarios)
- Performance and concurrency tests

---

## 📝 CONCLUSION

**Total Test Cases:** 42 (15 Positive + 12 Negative + 15 Edge)

**Full Validation Coverage (UI + API + DB):** 28 tests (67%)  
**Partial Coverage:** 9 tests (21%)  
**Limited Coverage:** 5 tests (12%)

**Most tests CAN use all three validation types** because:
1. UI provides visual interaction
2. API provides programmatic access
3. Database stores actual data

**Tests that CAN'T use all three** have legitimate technical reasons:
- Validation prevents bad data from reaching DB
- Authorization logic above DB layer
- UI automation limitations for concurrent/performance tests

This comprehensive coverage ensures:
- ✅ End-to-end validation
- ✅ Data integrity verification
- ✅ User experience validation
- ✅ API contract adherence
- ✅ Database consistency
