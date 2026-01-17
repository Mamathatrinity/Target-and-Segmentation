"""
Database Tests for Trinity HCP Targeting & Segmentation Application
Tests database connections, data integrity, and critical tables
Note: Update table names and schema based on actual database structure
"""

import pytest


@pytest.mark.database
@pytest.mark.smoke
def test_db_connection(db_validator, db_connection_params):
    """Test database connection using MCP validator."""
    result = db_validator.connect_to_database(
        db_type="sqlserver",
        connection_params=db_connection_params
    )
    
    assert result["status"] == "success"
    print(f"✓ Connected to database: {result['database']}")


@pytest.mark.database
@pytest.mark.smoke
def test_db_health_check(db_validator, db_connection_params):
    """Test database health using MCP validator."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    result = db_validator.check_database_health()
    
    assert result["status"] == "success"
    assert result["healthy"] == True
    print(f"✓ Database healthy: {result['message']}")


@pytest.mark.database
@pytest.mark.regression
def test_data_exists_hcp_table(db_validator, db_connection_params):
    """Test that HCP data exists in the database."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    # Note: Update table name based on actual schema
    result = db_validator.validate_data_exists(
        table="HCP",  # or "HealthcareProfessionals", "Physicians", etc.
        conditions={"IsActive": 1}
    )
    
    assert result["status"] == "success"
    assert result["exists"] == True
    print(f"✓ Found {result['count']} active HCPs")


@pytest.mark.database
@pytest.mark.regression
def test_data_exists_segments_table(db_validator, db_connection_params):
    """Test that Segments table has data."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    result = db_validator.validate_data_exists(
        table="Segments",
        conditions={}  # No conditions - just check table has data
    )
    
    assert result["status"] == "success"
    assert result["exists"] == True
    print(f"✓ Found {result['count']} segments in database")


@pytest.mark.database
@pytest.mark.regression
def test_data_exists_targets_table(db_validator, db_connection_params):
    """Test that Targets/TargetLists table has data."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    result = db_validator.validate_data_exists(
        table="TargetLists",  # or "Targets"
        conditions={}
    )
    
    assert result["status"] == "success"
    assert result["exists"] == True
    print(f"✓ Found {result['count']} target lists in database")


@pytest.mark.database
@pytest.mark.regression
def test_validate_segment_status_values(db_validator, db_connection_params):
    """Test Segments table status column has valid values."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    result = db_validator.validate_column_values(
        table="Segments",
        column="Status",
        expected_values=["Active", "Inactive", "Draft", "Archived"]
    )
    
    assert result["status"] == "success"
    assert result["valid"] == True
    print(f"✓ Segment Status column contains valid values: {result['actual_values']}")


@pytest.mark.database
@pytest.mark.regression
def test_validate_cohort_brand_relationship(db_validator, db_connection_params):
    """Test Cohorts table has valid brand references."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    # Query to check cohort-brand relationships
    result = db_validator.execute_query(
        query="SELECT TOP 10 CohortID, BrandID, CohortName FROM Cohorts WHERE BrandID IS NOT NULL",
        fetch_results=True
    )
    
    assert result["status"] == "success"
    assert result["row_count"] > 0
    print(f"✓ Found {result['row_count']} cohorts with valid brand associations")


@pytest.mark.database
@pytest.mark.regression
def test_execute_query(db_validator, db_connection_params):
    """Test query execution for HCP targeting data."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    # Note: Update query based on actual table structure
    result = db_validator.execute_query(
        query="SELECT TOP 5 SegmentID, SegmentName, CreatedDate FROM Segments ORDER BY CreatedDate DESC",
        fetch_results=True
    )
    
    assert result["status"] == "success"
    assert result["row_count"] > 0
    print(f"✓ Query executed: {result['row_count']} rows, {result['execution_time_ms']}ms")


@pytest.mark.database
@pytest.mark.regression
def test_hcp_universe_data_integrity(db_validator, db_connection_params):
    """Test HCP Universe data integrity."""
    # Ensure connection
    db_validator.connect_to_database("sqlserver", db_connection_params)
    
    # Check if HCP Universe table has valid records
    result = db_validator.execute_query(
        query="SELECT COUNT(*) as UniverseCount FROM HCPUniverse WHERE IsActive = 1",
        fetch_results=True
    )
    
    assert result["status"] == "success"
    print(f"✓ HCP Universe integrity check passed")

