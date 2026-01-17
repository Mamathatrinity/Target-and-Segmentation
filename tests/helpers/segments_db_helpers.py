"""
Segments Module - Database Helper Functions
Reusable database query functions for Segments test cases

All functions use pymysql connection and return data in consistent format.
Handles cursor management and error handling.
"""


def get_segment_count(mysql_connection, include_deleted=False):
    """
    Get total count of segments from database.
    
    Args:
        mysql_connection: pymysql connection object
        include_deleted: Not used (for compatibility), all segments are returned
    
    Returns:
        int: Total number of segments
    """
    try:
        cursor = mysql_connection.cursor()
        query = "SELECT COUNT(*) as total FROM segments"
        
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result['total'] if result else 0
    except Exception as e:
        print(f"[DB ERROR] get_segment_count: {str(e)}")
        return 0


def get_segment_by_id(mysql_connection, segment_id):
    """
    Get segment details by ID.
    
    Args:
        mysql_connection: pymysql connection object
        segment_id: Segment ID to fetch
    
    Returns:
        dict: Segment record or None if not found
    """
    try:
        cursor = mysql_connection.cursor()
        query = "SELECT * FROM segments WHERE id = %s"
        cursor.execute(query, (segment_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(f"[DB ERROR] get_segment_by_id: {str(e)}")
        return None


def get_segment_by_name(mysql_connection, name, include_deleted=False):
    """
    Get segment by name.
    
    Args:
        mysql_connection: pymysql connection object
        name: Segment name to search for
        include_deleted: If False, only search active segments
    
    Returns:
        dict: Segment record or None if not found
    """
    try:
        cursor = mysql_connection.cursor()
        if include_deleted:
            query = "SELECT * FROM segments WHERE name = %s"
        else:
            query = "SELECT * FROM segments WHERE name = %s"
        
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(f"[DB ERROR] get_segment_by_name: {str(e)}")
        return None


def get_segments_by_user(mysql_connection, user_id):
    """
    Get all segments created by a specific user.
    
    Args:
        mysql_connection: pymysql connection object
        user_id: User ID who created the segments
    
    Returns:
        list: List of segment records
    """
    try:
        cursor = mysql_connection.cursor()
        query = "SELECT * FROM segments WHERE created_by = %s"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"[DB ERROR] get_segments_by_user: {str(e)}")
        return []


def get_team_segments(mysql_connection):
    """
    Get all team segments.
    
    Args:
        mysql_connection: pymysql connection object
    
    Returns:
        list: List of team segment records
    """
    try:
        cursor = mysql_connection.cursor()
        query = "SELECT * FROM segments WHERE is_team_segment = 1"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"[DB ERROR] get_team_segments: {str(e)}")
        return []


def verify_segment_exists(mysql_connection, name):
    """
    Check if a segment with given name exists.
    
    Args:
        mysql_connection: pymysql connection object
        name: Segment name to check
    
    Returns:
        bool: True if segment exists, False otherwise
    """
    segment = get_segment_by_name(mysql_connection, name)
    return segment is not None


def verify_segment_not_exists(mysql_connection, name):
    """
    Check if a segment with given name does NOT exist.
    
    Args:
        mysql_connection: pymysql connection object
        name: Segment name to check
    
    Returns:
        bool: True if segment does NOT exist, False if it exists
    """
    segment = get_segment_by_name(mysql_connection, name)
    return segment is None


def verify_segment_deleted(mysql_connection, segment_id):
    """
    Check if a segment is marked as deleted.
    
    Args:
        mysql_connection: pymysql connection object
        segment_id: Segment ID to check
    
    Returns:
        bool: True if segment is deleted, False otherwise
    """
    try:
        cursor = mysql_connection.cursor()
        query = "SELECT is_deleted FROM segments WHERE id = %s"
        cursor.execute(query, (segment_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result['is_deleted'] == 1
        return False  # Segment doesn't exist
    except Exception as e:
        print(f"[DB ERROR] verify_segment_deleted: {str(e)}")
        return False


def create_test_segment(mysql_connection, name, description="Test segment", created_by=1, is_team_segment=0):
    """
    Create a test segment in database (for test setup).
    
    Args:
        mysql_connection: pymysql connection object
        name: Segment name
        description: Segment description
        created_by: User ID who creates the segment
        is_team_segment: 1 for team segment, 0 for personal
    
    Returns:
        int: ID of created segment or None if failed
    """
    try:
        cursor = mysql_connection.cursor()
        query = """
            INSERT INTO segments (name, description, created_by, is_team_segment, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (name, description, created_by, is_team_segment))
        mysql_connection.commit()
        segment_id = cursor.lastrowid
        cursor.close()
        return segment_id
    except Exception as e:
        print(f"[DB ERROR] create_test_segment: {str(e)}")
        mysql_connection.rollback()
        return None


def delete_test_segment(mysql_connection, name):
    """
    Delete a test segment from database (for test cleanup).
    
    Args:
        mysql_connection: pymysql connection object
        name: Segment name to delete
    
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    try:
        cursor = mysql_connection.cursor()
        query = "DELETE FROM segments WHERE name = %s"
        cursor.execute(query, (name,))
        mysql_connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] delete_test_segment: {str(e)}")
        mysql_connection.rollback()
        return False


def update_segment(mysql_connection, segment_id, name=None, description=None):
    """
    Update segment fields in database.
    
    Args:
        mysql_connection: pymysql connection object
        segment_id: ID of segment to update
        name: New name (optional)
        description: New description (optional)
    
    Returns:
        bool: True if updated successfully, False otherwise
    """
    try:
        cursor = mysql_connection.cursor()
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        
        if not updates:
            return True  # Nothing to update
        
        params.append(segment_id)
        query = f"UPDATE segments SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, params)
        mysql_connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] update_segment: {str(e)}")
        mysql_connection.rollback()
        return False


def search_segments(mysql_connection, search_term):
    """
    Search segments by name (case-insensitive LIKE query).
    
    Args:
        mysql_connection: pymysql connection object
        search_term: Text to search for in segment names
    
    Returns:
        list: List of matching segment records
    """
    try:
        cursor = mysql_connection.cursor()
        query = """
            SELECT * FROM segments 
            WHERE name LIKE %s
            ORDER BY name
        """
        cursor.execute(query, (f"%{search_term}%",))
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"[DB ERROR] search_segments: {str(e)}")
        return []


def get_segments_sorted(mysql_connection, sort_by='name', order='asc'):
    """
    Get all segments sorted by specified column.
    
    Args:
        mysql_connection: pymysql connection object
        sort_by: Column to sort by ('name', 'created_at', etc.)
        order: Sort order ('asc' or 'desc')
    
    Returns:
        list: List of sorted segment records
    """
    try:
        cursor = mysql_connection.cursor()
        
        # Validate sort column to prevent SQL injection
        valid_columns = ['name', 'created_at', 'updated_at', 'id']
        if sort_by not in valid_columns:
            sort_by = 'name'
        
        # Validate order
        order = order.lower()
        if order not in ['asc', 'desc']:
            order = 'asc'
        
        query = f"""
            SELECT * FROM segments 
           
            ORDER BY {sort_by} {order}
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"[DB ERROR] get_segments_sorted: {str(e)}")
        return []


def get_segments_paginated(mysql_connection, page=1, per_page=8):
    """
    Get segments with pagination.
    
    Args:
        mysql_connection: pymysql connection object
        page: Page number (1-indexed)
        per_page: Number of records per page
    
    Returns:
        dict: {'segments': list, 'total': int, 'page': int, 'per_page': int}
    """
    try:
        cursor = mysql_connection.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM segments")
        total = cursor.fetchone()['total']
        
        # Get paginated results
        offset = (page - 1) * per_page
        query = """
            SELECT * FROM segments 
           
            ORDER BY name
            LIMIT %s OFFSET %s
        """
        
        cursor.execute(query, (per_page, offset))
        segments = cursor.fetchall()
        cursor.close()
        
        return {
            'segments': segments,
            'total': total,
            'page': page,
            'per_page': per_page
        }
    except Exception as e:
        print(f"[DB ERROR] get_segments_paginated: {str(e)}")
        return {
            'segments': [],
            'total': 0,
            'page': page,
            'per_page': per_page
        }


def verify_segment_field(mysql_connection, segment_id, field_name, expected_value):
    """
    Verify a specific field value for a segment.
    
    Args:
        mysql_connection: pymysql connection object
        segment_id: Segment ID to check
        field_name: Name of the field to verify
        expected_value: Expected value of the field
    
    Returns:
        bool: True if field matches expected value, False otherwise
    """
    try:
        cursor = mysql_connection.cursor()
        query = f"SELECT {field_name} FROM segments WHERE id = %s"
        cursor.execute(query, (segment_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            actual_value = result[field_name]
            return actual_value == expected_value
        return False
    except Exception as e:
        print(f"[DB ERROR] verify_segment_field: {str(e)}")
        return False


# Wrapper functions for test compatibility

def create_test_segment_dict(mysql_connection, segment_data):
    """
    Create test segment from dictionary (used in tests).
    
    Args:
        mysql_connection: pymysql connection object
        segment_data: Dict with 'name', 'description', 'is_team_segment'
        
    Returns:
        int: Segment ID or None
    """
    name = segment_data.get('name', 'Test Segment')
    description = segment_data.get('description', '')
    is_team = 1 if segment_data.get('is_team_segment', False) else 0
    
    return create_test_segment(mysql_connection, name, description, is_team_segment=is_team)


def delete_segment(mysql_connection, segment_id):
    """
    Delete segment by ID (soft delete).
    
    Args:
        mysql_connection: pymysql connection object
        segment_id: Segment ID to delete
        
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        cursor = mysql_connection.cursor()
        # Soft delete
        query = "UPDATE segments SET is_deleted = 1 WHERE id = %s"
        cursor.execute(query, (segment_id,))
        mysql_connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] delete_segment: {str(e)}")
        mysql_connection.rollback()
        return False
