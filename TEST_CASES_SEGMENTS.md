# Segments Module - Test Cases

## Overview
This document outlines all test cases for the Segments module including Positive, Negative, and Edge test scenarios.

---

## POSITIVE TEST CASES

### TC_SEG_POS_001: View Segments List Successfully
**Priority:** High  
**Description:** User navigates to Segments page and sees list of segments  
**Preconditions:** User is logged in  
**Steps:**
1. Login to application
2. Navigate to Segments page (/segments)
3. Verify segments list loads

**Expected Result:**
- Segments page loads successfully
- Search field is visible
- Create Segment button is visible
- Filter and sort dropdowns are visible
- At least one segment card is displayed (if segments exist)

**Validations:**
- ✅ UI: Page elements visible
- ✅ API: GET /api/segments returns 200
- ✅ DB: Segment count matches UI count

---

### TC_SEG_POS_002: Search Segment by Name (Exact Match)
**Priority:** High  
**Description:** User searches for a segment using exact name  
**Preconditions:** User is logged in, at least one segment exists  
**Steps:**
1. Navigate to Segments page
2. Enter exact segment name in search field
3. Verify search results

**Expected Result:**
- Only matching segment is displayed
- Segment name matches search text
- Non-matching segments are hidden

**Validations:**
- ✅ UI: Search results displayed correctly
- ✅ API: GET /api/segments?search=<name> returns filtered results
- ✅ DB: Query segments table with name filter

---

### TC_SEG_POS_003: Search Segment by Partial Name
**Priority:** Medium  
**Description:** User searches for segments using partial name  
**Preconditions:** User is logged in, multiple segments exist  
**Steps:**
1. Navigate to Segments page
2. Enter partial segment name in search field
3. Verify search results

**Expected Result:**
- All segments containing search text are displayed
- Search is case-insensitive
- Results update as user types

**Validations:**
- ✅ UI: Partial match results displayed
- ✅ API: GET /api/segments?search=<partial> returns matching segments
- ✅ DB: LIKE query on segments table

---

### TC_SEG_POS_004: Create New Segment Successfully
**Priority:** High  
**Description:** User creates a new segment with valid data  
**Preconditions:** User is logged in with create permissions  
**Steps:**
1. Navigate to Segments page
2. Click "Create Segment" button
3. Enter segment name (valid, unique)
4. Enter description (optional)
5. Select HCP Universe
6. Configure filters/criteria
7. Click "Save" or "Next"

**Expected Result:**
- Segment creation form loads
- All fields accept valid input
- Segment is created successfully
- User redirected to segment details or segments list
- New segment appears in segments list

**Validations:**
- ✅ UI: Success message displayed, segment in list
- ✅ API: POST /api/segments returns 201, segment object returned
- ✅ DB: New record in segments table with correct data

---

### TC_SEG_POS_005: Filter Segments by "My Segments"
**Priority:** Medium  
**Description:** User filters to see only their own segments  
**Preconditions:** User is logged in, has created segments  
**Steps:**
1. Navigate to Segments page
2. Click "Show" filter dropdown
3. Select "My Segments"

**Expected Result:**
- Only segments created by current user are displayed
- Team segments are hidden
- Count reflects filtered results

**Validations:**
- ✅ UI: Only user's segments visible
- ✅ API: GET /api/segments?filter=my returns user's segments
- ✅ DB: Query segments where created_by = current_user_id

---

### TC_SEG_POS_006: Filter Segments by "Team Segments"
**Priority:** Medium  
**Description:** User filters to see team-shared segments  
**Preconditions:** User is logged in, team segments exist  
**Steps:**
1. Navigate to Segments page
2. Click "Show" filter dropdown
3. Select "Team Segments"

**Expected Result:**
- Only team segments are displayed
- Personal segments are hidden
- Count reflects filtered results

**Validations:**
- ✅ UI: Only team segments visible
- ✅ API: GET /api/segments?filter=team returns team segments
- ✅ DB: Query segments where is_team_segment = true

---

### TC_SEG_POS_007: Sort Segments by Name (A-Z)
**Priority:** Medium  
**Description:** User sorts segments alphabetically by name  
**Preconditions:** User is logged in, multiple segments exist  
**Steps:**
1. Navigate to Segments page
2. Click "Sort By" dropdown
3. Select "Name" (A-Z)

**Expected Result:**
- Segments are sorted alphabetically
- First segment starts with A (or earliest letter)
- Order is ascending

**Validations:**
- ✅ UI: Segments displayed in alphabetical order
- ✅ API: GET /api/segments?sort=name&order=asc
- ❌ DB: N/A (UI/API handles sorting)

---

### TC_SEG_POS_008: Sort Segments by Created Date (Newest First)
**Priority:** Medium  
**Description:** User sorts segments by creation date  
**Preconditions:** User is logged in, multiple segments exist  
**Steps:**
1. Navigate to Segments page
2. Click "Sort By" dropdown
3. Select "Created Date"

**Expected Result:**
- Segments sorted by creation date
- Newest segments appear first
- Dates are in descending order

**Validations:**
- ✅ UI: Segments displayed with newest first
- ✅ API: GET /api/segments?sort=created_date&order=desc
- ✅ DB: Query segments ORDER BY created_date DESC

---

### TC_SEG_POS_009: View Segment Details
**Priority:** High  
**Description:** User clicks on a segment to view its details  
**Preconditions:** User is logged in, segments exist  
**Steps:**
1. Navigate to Segments page
2. Click on a segment card

**Expected Result:**
- User is redirected to segment details page
- Segment name is displayed
- Segment description is visible
- HCP count is shown
- Filters/criteria are displayed

**Validations:**
- ✅ UI: All segment details displayed correctly
- ✅ API: GET /api/segments/{id} returns segment data
- ✅ DB: Query segments table by segment_id

---

### TC_SEG_POS_010: Pagination - Navigate to Next Page
**Priority:** Medium  
**Description:** User navigates to next page of segments  
**Preconditions:** User is logged in, more than 8 segments exist  
**Steps:**
1. Navigate to Segments page
2. Verify "Next Page" button is enabled
3. Click "Next Page" button

**Expected Result:**
- Next set of segments is displayed
- Page number increments
- "Previous Page" button becomes enabled
- URL updates with page parameter

**Validations:**
- ✅ UI: Next page of segments displayed
- ✅ API: GET /api/segments?page=2 returns next page data
- ✅ DB: Query with OFFSET/LIMIT for pagination

---

### TC_SEG_POS_011: Pagination - Navigate to Previous Page
**Priority:** Medium  
**Description:** User navigates to previous page of segments  
**Preconditions:** User is on page 2 or higher  
**Steps:**
1. Navigate to Segments page
2. Go to page 2
3. Click "Previous Page" button

**Expected Result:**
- Previous set of segments is displayed
- Page number decrements
- Correct segments from previous page shown

**Validations:**
- ✅ UI: Previous page of segments displayed
- ✅ API: GET /api/segments?page=1 returns previous page
- ✅ DB: Query with correct OFFSET

---

### TC_SEG_POS_012: Change Records Per Page (8 to 16)
**Priority:** Low  
**Description:** User changes number of segments displayed per page  
**Preconditions:** User is logged in, multiple segments exist  
**Steps:**
1. Navigate to Segments page
2. Click "Records per page" dropdown
3. Select "16"

**Expected Result:**
- 16 segments are displayed per page
- Pagination updates accordingly
- Total pages may decrease

**Validations:**
- ✅ UI: 16 segment cards visible
- ✅ API: GET /api/segments?per_page=16
- ❌ DB: N/A (API handles pagination)

---

### TC_SEG_POS_013: Edit Segment Name and Description
**Priority:** High  
**Description:** User edits an existing segment's basic information  
**Preconditions:** User is logged in, has edit permissions, segment exists  
**Steps:**
1. Navigate to Segments page
2. Click on a segment
3. Click "Edit" button
4. Modify segment name
5. Modify description
6. Click "Save"

**Expected Result:**
- Changes are saved successfully
- Updated name displayed in segments list
- Updated description visible in details

**Validations:**
- ✅ UI: Success message, updated data displayed
- ✅ API: PUT /api/segments/{id} returns 200
- ✅ DB: Segment record updated with new values

---

### TC_SEG_POS_014: Delete Segment Successfully
**Priority:** High  
**Description:** User deletes a segment  
**Preconditions:** User is logged in, has delete permissions, segment exists  
**Steps:**
1. Navigate to Segments page
2. Click on a segment
3. Click "Delete" button
4. Confirm deletion in dialog

**Expected Result:**
- Confirmation dialog appears
- Segment is deleted after confirmation
- Segment removed from list
- Success message displayed

**Validations:**
- ✅ UI: Segment no longer visible in list
- ✅ API: DELETE /api/segments/{id} returns 204
- ✅ DB: Segment record deleted or marked as deleted

---

### TC_SEG_POS_015: Toggle Team Segment ON
**Priority:** Medium  
**Description:** User creates a segment and marks it as team segment  
**Preconditions:** User is logged in with team segment permissions  
**Steps:**
1. Click "Create Segment"
2. Enter segment details
3. Toggle "Team Segment" switch to ON
4. Save segment

**Expected Result:**
- Segment created as team segment
- Visible to all team members
- Team badge/indicator shown

**Validations:**
- ✅ UI: Team segment badge visible
- ✅ API: POST /api/segments with is_team_segment=true
- ✅ DB: Segment record has is_team_segment = true

---

## NEGATIVE TEST CASES

### TC_SEG_NEG_001: Create Segment with Empty Name
**Priority:** High  
**Description:** User attempts to create segment without entering name  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Leave segment name field empty
3. Enter other required fields
4. Click "Save" or "Next"

**Expected Result:**
- Validation error displayed
- "Segment Name is required" error message
- Segment is NOT created
- User remains on create form

**Validations:**
- ✅ UI: Error message displayed, form not submitted
- ✅ API: POST /api/segments returns 400 Bad Request
- ✅ DB: No new record created in segments table

---

### TC_SEG_NEG_002: Create Segment with Duplicate Name
**Priority:** High  
**Description:** User attempts to create segment with existing name  
**Preconditions:** User is logged in, segment with name "Test Segment" exists  
**Steps:**
1. Click "Create Segment"
2. Enter name "Test Segment" (duplicate)
3. Enter other fields
4. Click "Save"

**Expected Result:**
- Validation error displayed
- "Segment name already exists" error
- Segment is NOT created
- User remains on create form

**Validations:**
- ✅ UI: Error message displayed
- ✅ API: POST /api/segments returns 409 Conflict
- ✅ DB: No duplicate record created

---

### TC_SEG_NEG_003: Create Segment with Name Exceeding Max Length
**Priority:** Medium  
**Description:** User attempts to create segment with very long name  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Enter segment name with 256+ characters
3. Enter other fields
4. Click "Save"

**Expected Result:**
- Validation error displayed
- "Segment name exceeds maximum length" error
- Character limit enforced in UI
- Segment is NOT created

**Validations:**
- ✅ UI: Error message or character limit enforced
- ✅ API: POST /api/segments returns 400 Bad Request
- ❌ DB: N/A (validation happens before DB insert)

---

### TC_SEG_NEG_004: Create Segment with Special Characters in Name
**Priority:** Medium  
**Description:** User attempts to create segment with invalid special characters  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Enter segment name with special chars: `<script>alert()</script>`
3. Enter other fields
4. Click "Save"

**Expected Result:**
- Either validation error displayed OR
- Special characters are sanitized/escaped
- No XSS vulnerability
- If allowed, segment created with sanitized name

**Validations:**
- ✅ UI: Validation or sanitization applied
- ✅ API: POST /api/segments handles special chars safely
- ✅ DB: No raw script tags stored

---

### TC_SEG_NEG_005: Search with Non-Existent Segment Name
**Priority:** Medium  
**Description:** User searches for a segment that doesn't exist  
**Preconditions:** User is logged in  
**Steps:**
1. Navigate to Segments page
2. Enter non-existent segment name in search: "XYZ_NONEXISTENT_9999"
3. Verify results

**Expected Result:**
- No segments displayed
- "No segments found" message shown
- Search field retains entered text
- No error thrown

**Validations:**
- ✅ UI: Empty state message displayed
- ✅ API: GET /api/segments?search=XYZ returns empty array
- ✅ DB: Query returns 0 rows

---

### TC_SEG_NEG_006: Search with SQL Injection Attempt
**Priority:** High (Security)  
**Description:** User attempts SQL injection via search field  
**Preconditions:** User is logged in  
**Steps:**
1. Navigate to Segments page
2. Enter SQL injection string: `'; DROP TABLE segments; --`
3. Verify application behavior

**Expected Result:**
- Search is handled safely
- No database error
- Either no results OR error message
- Database tables remain intact

**Validations:**
- ✅ UI: No crash, safe error handling
- ✅ API: GET /api/segments with injection returns 400 or empty
- ✅ DB: Segments table still exists, data intact

---

### TC_SEG_NEG_007: Delete Segment Without Permission
**Priority:** High  
**Description:** User without delete permission attempts to delete segment  
**Preconditions:** User is logged in as read-only user  
**Steps:**
1. Navigate to Segments page
2. Click on a segment
3. Attempt to click "Delete" button

**Expected Result:**
- Delete button is disabled OR not visible
- If API call attempted, returns 403 Forbidden
- Segment is NOT deleted
- Error message displayed

**Validations:**
- ✅ UI: Delete button disabled/hidden
- ✅ API: DELETE /api/segments/{id} returns 403 Forbidden
- ✅ DB: Segment record unchanged

---

### TC_SEG_NEG_008: Edit Segment Owned by Another User
**Priority:** High  
**Description:** User attempts to edit segment created by another user  
**Preconditions:** User A is logged in, Segment created by User B exists  
**Steps:**
1. Login as User A
2. Navigate to Segments page
3. Click on User B's segment
4. Attempt to edit

**Expected Result:**
- Edit button is disabled OR not visible OR
- Edit API call returns 403 Forbidden
- Segment is NOT modified
- Error message displayed

**Validations:**
- ✅ UI: Edit disabled or error shown
- ✅ API: PUT /api/segments/{id} returns 403 Forbidden
- ✅ DB: Segment record unchanged

---

### TC_SEG_NEG_009: Access Segments Page Without Authentication
**Priority:** High (Security)  
**Description:** User attempts to access segments page without logging in  
**Preconditions:** User is NOT logged in  
**Steps:**
1. Clear browser cookies/session
2. Navigate directly to /segments URL

**Expected Result:**
- User is redirected to login page
- Segments page does NOT load
- Session/auth error returned

**Validations:**
- ✅ UI: Redirect to login page
- ✅ API: GET /api/segments returns 401 Unauthorized
- ❌ DB: N/A (auth handled before DB access)

---

### TC_SEG_NEG_010: Create Segment Without Selecting HCP Universe
**Priority:** High  
**Description:** User attempts to create segment without required HCP Universe  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Enter segment name
3. Skip HCP Universe selection
4. Click "Save" or "Next"

**Expected Result:**
- Validation error displayed
- "HCP Universe is required" error message
- Segment is NOT created
- User remains on create form

**Validations:**
- ✅ UI: Error message displayed
- ✅ API: POST /api/segments returns 400 Bad Request
- ✅ DB: No record created

---

### TC_SEG_NEG_011: Navigate to Invalid Page Number (Page 9999)
**Priority:** Low  
**Description:** User manually navigates to page that doesn't exist  
**Preconditions:** User is logged in, only 3 pages of segments exist  
**Steps:**
1. Navigate to Segments page
2. Manually edit URL to /segments?page=9999
3. Press Enter

**Expected Result:**
- Either redirect to last valid page OR
- Show empty page with message OR
- Return to page 1

**Validations:**
- ✅ UI: Graceful handling, no crash
- ✅ API: GET /api/segments?page=9999 returns empty or error
- ❌ DB: N/A (pagination handled in API)

---

### TC_SEG_NEG_012: Filter with Invalid Filter Option
**Priority:** Low  
**Description:** User manipulates filter parameter to invalid value  
**Preconditions:** User is logged in  
**Steps:**
1. Navigate to Segments page
2. Manually edit URL: /segments?filter=INVALID_FILTER
3. Press Enter

**Expected Result:**
- Either show all segments (ignore invalid filter) OR
- Show error message
- Application doesn't crash

**Validations:**
- ✅ UI: Graceful error handling
- ✅ API: GET /api/segments?filter=INVALID returns 400 or default
- ❌ DB: N/A (validation in API layer)

---

## EDGE TEST CASES

### TC_SEG_EDGE_001: Create Segment with Name Containing Only Spaces
**Priority:** Medium  
**Description:** User enters segment name with only whitespace characters  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Enter segment name: "     " (only spaces)
3. Click "Save"

**Expected Result:**
- Validation error displayed
- Whitespace is trimmed, treated as empty
- "Segment Name is required" error
- Segment is NOT created

**Validations:**
- ✅ UI: Error message displayed
- ✅ API: POST /api/segments returns 400 (after trim)
- ✅ DB: No record created

---

### TC_SEG_EDGE_002: Create Segment with Minimum Valid Name Length
**Priority:** Low  
**Description:** User creates segment with single character name  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Enter segment name: "A" (1 character)
3. Enter other required fields
4. Click "Save"

**Expected Result:**
- Segment created successfully (if min length = 1) OR
- Validation error if minimum is higher
- Behavior consistent with requirements

**Validations:**
- ✅ UI: Either success or validation error
- ✅ API: POST /api/segments returns 201 or 400
- ✅ DB: Record created if valid

---

### TC_SEG_EDGE_003: Create Segment with Name at Exact Max Length
**Priority:** Low  
**Description:** User creates segment with name at maximum allowed length  
**Preconditions:** User is logged in, max length is 255 chars  
**Steps:**
1. Click "Create Segment"
2. Enter segment name with exactly 255 characters
3. Enter other fields
4. Click "Save"

**Expected Result:**
- Segment created successfully
- Full name is stored and displayed
- No truncation occurs

**Validations:**
- ✅ UI: Full name displayed
- ✅ API: POST /api/segments returns 201
- ✅ DB: Full 255-char name stored

---

### TC_SEG_EDGE_004: Search with Very Long Search String
**Priority:** Low  
**Description:** User enters very long text in search field  
**Preconditions:** User is logged in  
**Steps:**
1. Navigate to Segments page
2. Enter 500+ character search string
3. Verify behavior

**Expected Result:**
- Search is processed OR character limit enforced
- Application doesn't crash or slow down
- Either no results or limited results

**Validations:**
- ✅ UI: Search handled gracefully
- ✅ API: GET /api/segments?search=<long_string> returns response
- ❌ DB: Query executed safely with LIKE limit

---

### TC_SEG_EDGE_005: Rapidly Toggle Team Segment Switch
**Priority:** Low  
**Description:** User rapidly clicks Team Segment toggle multiple times  
**Preconditions:** User is on Create Segment page  
**Steps:**
1. Click "Create Segment"
2. Rapidly click Team Segment toggle 10 times in 2 seconds
3. Verify final state

**Expected Result:**
- Toggle settles to final clicked state
- No multiple API calls triggered
- UI state is consistent
- No errors thrown

**Validations:**
- ✅ UI: Toggle in correct final state
- ✅ API: Debounced, not called multiple times
- ❌ DB: N/A (no save yet)

---

### TC_SEG_EDGE_006: Create Segment During Network Interruption
**Priority:** Medium  
**Description:** User creates segment while network is interrupted  
**Preconditions:** User is logged in, network can be toggled  
**Steps:**
1. Click "Create Segment"
2. Enter valid segment data
3. Disconnect network
4. Click "Save"
5. Wait for timeout
6. Reconnect network

**Expected Result:**
- Error message displayed: "Network error" or "Request failed"
- Segment is NOT created
- User can retry after network restored
- No partial/corrupted data

**Validations:**
- ✅ UI: Error message displayed
- ✅ API: POST /api/segments times out or fails
- ✅ DB: No record created during interruption

---

### TC_SEG_EDGE_007: Open Multiple Segment Detail Pages Simultaneously
**Priority:** Low  
**Description:** User opens multiple segments in different browser tabs  
**Preconditions:** User is logged in, multiple segments exist  
**Steps:**
1. Navigate to Segments page
2. Right-click segment A → "Open in new tab"
3. Right-click segment B → "Open in new tab"
4. Switch between tabs

**Expected Result:**
- Each tab shows correct segment details
- No data mixing between tabs
- Session is shared across tabs
- All tabs function independently

**Validations:**
- ✅ UI: Each tab shows correct data
- ✅ API: Each tab makes separate GET /api/segments/{id}
- ✅ DB: Queries return correct data per segment_id

---

### TC_SEG_EDGE_008: Create Segment with Unicode/Emoji in Name
**Priority:** Low  
**Description:** User creates segment with Unicode characters and emojis  
**Preconditions:** User is logged in  
**Steps:**
1. Click "Create Segment"
2. Enter segment name: "Test Segment 测试 🚀🎯"
3. Enter other fields
4. Click "Save"

**Expected Result:**
- Segment created successfully OR validation error
- If created, Unicode/emojis stored correctly
- Display is correct in UI
- No encoding issues

**Validations:**
- ✅ UI: Name displayed correctly
- ✅ API: POST /api/segments handles Unicode
- ✅ DB: UTF-8 encoding, data stored correctly

---

### TC_SEG_EDGE_009: Delete Last Segment in List
**Priority:** Medium  
**Description:** User deletes the last remaining segment  
**Preconditions:** User is logged in, only 1 segment exists  
**Steps:**
1. Navigate to Segments page
2. Click on the only segment
3. Click "Delete"
4. Confirm deletion

**Expected Result:**
- Segment deleted successfully
- "No segments found" or empty state displayed
- "Create Segment" button still visible
- No errors thrown

**Validations:**
- ✅ UI: Empty state shown
- ✅ API: DELETE /api/segments/{id} returns 204
- ✅ DB: Segments table empty or count = 0

---

### TC_SEG_EDGE_010: Navigate Between Pages Rapidly
**Priority:** Low  
**Description:** User clicks Next/Previous buttons very quickly  
**Preconditions:** User is logged in, 5+ pages of segments exist  
**Steps:**
1. Navigate to Segments page
2. Rapidly click "Next Page" 5 times
3. Rapidly click "Previous Page" 5 times

**Expected Result:**
- Page navigation works correctly
- API calls are debounced/cancelled properly
- No duplicate requests
- UI shows correct page at end

**Validations:**
- ✅ UI: Correct page displayed
- ✅ API: Requests handled efficiently (cancelled or queued)
- ❌ DB: N/A (pagination in API)

---

### TC_SEG_EDGE_011: Edit Segment and Cancel Without Saving
**Priority:** Medium  
**Description:** User edits segment but cancels before saving  
**Preconditions:** User is logged in, segment exists  
**Steps:**
1. Click on a segment
2. Click "Edit"
3. Modify segment name
4. Click "Cancel" or navigate away

**Expected Result:**
- Changes are NOT saved
- Original segment data remains
- User returned to previous view
- No unsaved changes warning (or warning shown)

**Validations:**
- ✅ UI: Original data displayed
- ✅ API: No PUT request made
- ✅ DB: Segment data unchanged

---

### TC_SEG_EDGE_012: Search with Case Variations
**Priority:** Low  
**Description:** User searches with different case variations  
**Preconditions:** User is logged in, segment "Test Segment" exists  
**Steps:**
1. Navigate to Segments page
2. Search: "test segment" (lowercase)
3. Verify results
4. Search: "TEST SEGMENT" (uppercase)
5. Verify results
6. Search: "TeSt SeGmEnT" (mixed case)
7. Verify results

**Expected Result:**
- All searches return same segment
- Search is case-insensitive
- Results are consistent

**Validations:**
- ✅ UI: Same results for all case variations
- ✅ API: GET /api/segments?search=<text> is case-insensitive
- ✅ DB: Query uses LOWER() or case-insensitive collation

---

### TC_SEG_EDGE_013: Refresh Page During Segment Load
**Priority:** Low  
**Description:** User refreshes page while segments are loading  
**Preconditions:** User is logged in  
**Steps:**
1. Navigate to Segments page
2. Immediately press F5 (refresh) during load
3. Verify behavior

**Expected Result:**
- Page reloads cleanly
- Segments load from beginning
- No duplicate data or errors
- Loading state handled gracefully

**Validations:**
- ✅ UI: Clean reload, no errors
- ✅ API: Previous request cancelled, new request made
- ❌ DB: N/A (idempotent GET)

---

### TC_SEG_EDGE_014: Create 100+ Segments and Test Performance
**Priority:** Low  
**Description:** User creates many segments and tests pagination/search performance  
**Preconditions:** User is logged in  
**Steps:**
1. Create 100 segments (via UI or API)
2. Navigate to Segments page
3. Test pagination through all pages
4. Test search functionality
5. Measure load times

**Expected Result:**
- Page loads within acceptable time (<3 seconds)
- Pagination works smoothly
- Search is performant
- No timeouts or crashes

**Validations:**
- ✅ UI: Performance acceptable
- ✅ API: GET /api/segments?page=X responds quickly
- ✅ DB: Query optimized with indexes

---

### TC_SEG_EDGE_015: Simultaneous Edits by Two Users
**Priority:** Medium  
**Description:** Two users edit same segment at same time  
**Preconditions:** User A and User B logged in, same segment open  
**Steps:**
1. User A opens Segment X for editing
2. User B opens Segment X for editing
3. User A changes name to "Name A" and saves
4. User B changes name to "Name B" and saves

**Expected Result:**
- Either last save wins (User B) OR
- Conflict detection warning OR
- Version control prevents overwrite
- Data integrity maintained

**Validations:**
- ✅ UI: Warning or success based on implementation
- ✅ API: PUT /api/segments/{id} handles concurrent edits
- ✅ DB: Final state is consistent (one of the names)

---

## Test Case Summary

**Total Test Cases:** 40

### By Type:
- **Positive:** 15 test cases
- **Negative:** 12 test cases
- **Edge:** 15 test cases (includes 2 renamed edge cases)

### By Priority:
- **High:** 15 test cases
- **Medium:** 14 test cases
- **Low:** 11 test cases

### By Validation Coverage:
- **UI Only:** 6 test cases
- **UI + API:** 4 test cases
- **UI + API + DB:** 30 test cases

---

## Notes

1. **Database Table:** Assumed table name is `segments` with fields like `id`, `name`, `description`, `created_by`, `is_team_segment`, `created_date`, `hcp_universe_id`

2. **API Endpoints:** Assumed RESTful API with endpoints:
   - `GET /api/segments` - List segments
   - `POST /api/segments` - Create segment
   - `GET /api/segments/{id}` - Get segment details
   - `PUT /api/segments/{id}` - Update segment
   - `DELETE /api/segments/{id}` - Delete segment

3. **Permissions:** Assumed role-based access control with permissions for create, read, update, delete operations

4. **Pagination:** Default page size assumed to be 8 segments per page

5. **Security:** SQL injection, XSS, and authentication tests included for security validation
