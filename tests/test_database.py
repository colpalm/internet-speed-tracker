import pytest
from datetime import datetime
from internet_speed_tracker.enums import TimeOfDay
from internet_speed_tracker.schemas import SpeedTestResult
from backend.database.db_manager import DatabaseManager
from backend.database.models import SpeedTestRecord

DB_STR = "sqlite://"


@pytest.fixture
def test_db():
    """Create a temporary in-memory SQLite database for testing."""
    db_manager = DatabaseManager(DB_STR)  # In-memory database
    db_manager.init_db()
    return db_manager


@pytest.fixture
def sample_speed_test_result():
    """Create a sample speed test result for testing."""
    return SpeedTestResult(
        timestamp=datetime(2025, 3, 1, 12, 30, 0),
        download_speed=100.5,
        upload_speed=25.75,
        latency=15.2,
        time_of_day=TimeOfDay.AFTERNOON,
        server={"id": 12345, "name": "Test Server"}
    )


def test_save_speed_test_result(test_db, sample_speed_test_result):
    """Test saving speed test results."""
    success = test_db.save_speed_test_result(sample_speed_test_result)
    assert success, "Failed to save speed test result"

    # Verify successful save
    session = test_db.Session()
    try:
        record = session.query(SpeedTestRecord).first()
        assert record is not None, "No record found in database"

        # Check all fields were saved correctly
        assert record.timestamp == sample_speed_test_result.timestamp
        assert record.download_speed == sample_speed_test_result.download_speed
        assert record.upload_speed == sample_speed_test_result.upload_speed
        assert record.latency == sample_speed_test_result.latency
        assert record.time_of_day == sample_speed_test_result.time_of_day
        assert record.server_id == sample_speed_test_result.server["id"]
        assert record.server_name == sample_speed_test_result.server["name"]
    finally:
        session.close()


def test_get_speed_test_result(test_db, sample_speed_test_result):
    """Test retrieving the most recent speed test records."""

    # Save multiple records with different timestamps
    for i in range(5):
        result = SpeedTestResult(
            timestamp=datetime(2025, 3, 1, 12 + i, 0, 0),
            download_speed=100.0 + i,
            upload_speed=20.0 + i,
            latency=15.0 + i,
            time_of_day=TimeOfDay.AFTERNOON,
            server={"id": 12345, "name": "Test Server"}
        )
        test_db.save_speed_test_result(result)

    # Get the 3 latest records
    records = test_db.get_latest_speed_tests(3)
    assert len(records) == 3

    # Verify order
    assert records[0].timestamp > records[1].timestamp
    assert records[1].timestamp > records[2].timestamp

    # Verify values
    assert records[0].download_speed == 104.0
    assert records[0].upload_speed == 24.0
