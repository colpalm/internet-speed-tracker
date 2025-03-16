# Pytest unit tests
import json
from datetime import datetime
from unittest.mock import patch, Mock

import pytest
from shared.enums import TimeOfDay
from speedtracker.speed_test import determine_time_of_day, SpeedTest
from shared.schemas import SpeedTestResult

SAMPLE_RESPONSE = {
    "timestamp": "2025-02-13T14:30:00Z",
    "ping": {"latency": 15.5},
    "download": {"bandwidth": 625000},
    "upload": {"bandwidth": 312500},
    "server": {"id": 1234, "name": "Test Server"}
}


@pytest.fixture
def speedtest_instance() -> SpeedTest:
    return SpeedTest()


@pytest.fixture
def sample_json_output() -> str:
    """Simulate output from cli"""
    return json.dumps(SAMPLE_RESPONSE)


@pytest.mark.parametrize("hour, expected", [
    (5, TimeOfDay.MORNING),
    (11, TimeOfDay.MORNING),
    (12, TimeOfDay.AFTERNOON),
    (16, TimeOfDay.AFTERNOON),
    (17, TimeOfDay.EVENING),
    (23, TimeOfDay.EVENING),
    (0, TimeOfDay.EVENING),
    (4, TimeOfDay.EVENING),
])
def test_determine_time_of_day(hour: int, expected: TimeOfDay):
    assert determine_time_of_day(hour) == expected


def test_parse_speedtest_output(sample_json_output):
    """
    Test the isolated JSON parsing function.
    Given a known JSON string, the parser should return a SpeedTestResult
    with the correct values.
    """
    result: SpeedTestResult = SpeedTest._parse_speedtest_output(sample_json_output)

    expected_timestamp: datetime = datetime.strptime(SAMPLE_RESPONSE['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
    expected_time_of_day: TimeOfDay = determine_time_of_day(expected_timestamp.hour)

    assert result.timestamp == expected_timestamp
    assert result.download_speed == SAMPLE_RESPONSE['download']['bandwidth'] / 125_000
    assert result.upload_speed == SAMPLE_RESPONSE['upload']['bandwidth'] / 125_000
    assert result.latency == SAMPLE_RESPONSE['ping']['latency']
    assert result.time_of_day == expected_time_of_day
    assert result.server == SAMPLE_RESPONSE['server']


def test_execute_speedtest_cli_error(speedtest_instance):
    """Test handling of CLI execution error"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=1, stderr="CLI Error")

        with pytest.raises(RuntimeError) as exec_info:
            speedtest_instance._execute_speedtest()
        assert "Speed test failed" in str(exec_info.value)


def test_execute_speedtest_subprocess_error(speedtest_instance, caplog):
    """Test handling of subprocess execution error."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = Exception("Subprocess Error")
        with pytest.raises(Exception) as exec_info:
            speedtest_instance._execute_speedtest()
        # Assert log is captured
        assert any("Error running speedtest CLI" in message for message in caplog.text.splitlines())
        # Assert the exception message is correct
        assert "Subprocess Error" in str(exec_info.value)