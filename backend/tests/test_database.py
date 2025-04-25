import logging
import time

import pytest
from datetime import datetime, timezone, timedelta
from shared.enums import TimeOfDay
from shared.schemas import SpeedTestResult
from database.db_manager import DatabaseManager
from database.models import SpeedTestRecord, SpeedTestSummary
from testcontainers.postgres import PostgresContainer
from sqlalchemy.orm import close_all_sessions

DB_STR = "sqlite://"

pytestmark = pytest.mark.integration # Every test in file labeled as integration

@pytest.fixture
def test_db():
    """Create a temporary in-memory SQLite database for testing."""
    db_manager = DatabaseManager(DB_STR)  # In-memory database
    db_manager.init_db()
    return db_manager

@pytest.fixture(scope="module")
def pg_manager():
    """Create a temporary PostgreSQL database for testing."""
    with PostgresContainer("postgres:16-alpine") as pg:
        url = pg.get_connection_url()
        pg_manager = DatabaseManager(db_url=url)

        connect_to_db(pg_manager)

        yield pg_manager
        close_all_sessions()
        pg_manager.engine.dispose()


def connect_to_db(pg_manager):
    """Initialize the database and retry if the connection fails."""
    max_retries = 5
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            pg_manager.init_db()
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # All retries failed, raise the error
            logging.warning(f"Connection attempt {attempt + 1} failed, retrying in {retry_delay}s: {e}")
            time.sleep(retry_delay)
            retry_delay += 1


@pytest.fixture
def sample_speed_test_result():
    """Create a sample speed test result for testing."""
    return SpeedTestResult(
        timestamp=datetime(2025, 3, 1, 12, 30, 0),
        download_speed=100.5,
        upload_speed=25.75,
        latency=15.2,
        time_of_day=TimeOfDay.AFTERNOON,
        server={"name": "Test Server", "url": "https://test.com"}
    )

@pytest.fixture(scope="module")
def multiple_speed_test_results(pg_manager) -> tuple[list[SpeedTestResult], list[SpeedTestResult]]:
    """Helper function to create speed test records"""
    now = datetime.now(timezone.utc)

    # Create records for different times of day
    morning_results = [
        SpeedTestResult(
            timestamp=now - timedelta(hours=i),
            download_speed=50.0 + i,
            upload_speed=20.0 + i,
            latency=10.0 + i,
            time_of_day=TimeOfDay.MORNING,
            server={"name": "Test Server", "url": "https://test.com"}
        ) for i in range(3)
    ]
    evening_results = [
        SpeedTestResult(
            timestamp=now - timedelta(hours=i),
            download_speed=70.0 + i,
            upload_speed=30.0 + i,
            latency=5.0 + i,
            time_of_day=TimeOfDay.EVENING,
            server={"name": "Test Server", "url": "https://test.com"}
        ) for i in range(3)
    ]

    # Save records
    for record in morning_results + evening_results:
        pg_manager.save_speed_test_result(record)
    return morning_results, evening_results


def create_speed_test_results(test_db: DatabaseManager, num_results: int = 5, start_hour: int = 12) -> bool:
    """Helper function to create speed test records"""
    records = []
    # Save multiple records with different timestamps
    for i in range(num_results):
        result = SpeedTestResult(
            timestamp=datetime(2025, 3, 1, start_hour + i, 0, 0),
            download_speed=100.0 + i,
            upload_speed=20.0 + i,
            latency=15.0 + i,
            time_of_day=TimeOfDay.AFTERNOON,
            server={"name": "Test Server", "url": "https://test.com"}
        )
        success = test_db.save_speed_test_result(result)
        if success:
            records.append(result)
    return len(records) == num_results


def test_save_speed_test_result(test_db, sample_speed_test_result):
    """Test saving speed test results."""
    success = test_db.save_speed_test_result(sample_speed_test_result)
    assert success, "Failed to save speed test result"

    # Verify successful save
    session = test_db.session_factory()
    try:
        record = session.query(SpeedTestRecord).first()
        assert record is not None, "No record found in database"

        # Check all fields were saved correctly
        assert record.timestamp == sample_speed_test_result.timestamp
        assert record.download_speed == sample_speed_test_result.download_speed
        assert record.upload_speed == sample_speed_test_result.upload_speed
        assert record.latency == sample_speed_test_result.latency
        assert record.time_of_day == sample_speed_test_result.time_of_day
        assert record.server_name == sample_speed_test_result.server["name"]
        assert record.server_url == sample_speed_test_result.server["url"]
    finally:
        session.close()


def test_get_speed_test_result(test_db):
    """Test retrieving the most recent speed test records."""
    success = create_speed_test_results(test_db)
    if not success:
        pytest.fail("Failed to save speed test results")

    # Get the 3 latest records
    records = test_db.get_latest_speed_tests(3)
    assert len(records) == 3

    # Verify order
    assert records[0].timestamp > records[1].timestamp
    assert records[1].timestamp > records[2].timestamp

    # Verify values
    assert records[0].download_speed == pytest.approx(104.0)
    assert records[0].upload_speed == pytest.approx(24.0)

def test_get_speed_test_result_asc(test_db, sample_speed_test_result):
    """Test retrieving the most recent speed test records in chronological order."""

    success = create_speed_test_results(test_db)
    if not success:
        pytest.fail("Failed to save speed test results")

    # Get the 3 latest records
    records = test_db.get_latest_speed_tests(3, ascending=True)
    assert len(records) == 3

    # Verify order
    assert records[0].timestamp < records[1].timestamp
    assert records[1].timestamp < records[2].timestamp

    # Verify values
    assert records[0].download_speed == pytest.approx(102.0)
    assert records[0].upload_speed == pytest.approx(22.0)


def test_summary_stats_all(pg_manager, multiple_speed_test_results):
    """Test getting summary statistics for all time periods."""
    # Original test records
    morning_entries, evening_entries = multiple_speed_test_results

    results = pg_manager.get_speed_test_summary()

    assert len(results) == 3

    # Get all summary stats returned from the db
    all_summary_stats = None
    for result in results:
        if result.time_of_day == TimeOfDay.ALL:
            all_summary_stats = result
    assert all_summary_stats is not None

    verify_summary_stats(morning_entries + evening_entries, all_summary_stats)

def test_summary_stats_morning(pg_manager, multiple_speed_test_results):
    """Test getting summary statistics for just the morning period."""
    morning_results, _ = multiple_speed_test_results
    results = pg_manager.get_speed_test_summary(time_of_day=TimeOfDay.MORNING)
    assert len(results) == 1

    verify_summary_stats(morning_results, results[0])


def verify_summary_stats(entries: list[SpeedTestResult], summary_stats: SpeedTestSummary) -> None:
    """Helper function to verify summary statistics."""
    upload_data, download_data, latency_data = [], [], []
    for entry in entries:
        upload_data.append(entry.upload_speed)
        download_data.append(entry.download_speed)
        latency_data.append(entry.latency)
    # Verify upload speeds
    assert summary_stats.avg_upload_speed == pytest.approx(sum(upload_data) / len(upload_data))
    assert summary_stats.max_upload_speed == pytest.approx(max(upload_data))
    assert summary_stats.min_upload_speed == pytest.approx(min(upload_data))
    # Verify download speeds
    assert summary_stats.avg_download_speed == pytest.approx(sum(download_data) / len(download_data))
    assert summary_stats.max_download_speed == pytest.approx(max(download_data))
    assert summary_stats.min_download_speed == pytest.approx(min(download_data))
    # Verify latency values
    assert summary_stats.avg_latency == pytest.approx(sum(latency_data) / len(latency_data))
    assert summary_stats.max_latency == pytest.approx(max(latency_data))
    assert summary_stats.min_latency == pytest.approx(min(latency_data))