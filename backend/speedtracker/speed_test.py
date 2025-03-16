import subprocess
import json
import logging

from datetime import datetime
from shared.enums import TimeOfDay
from shared.schemas import SpeedTestResult


def determine_time_of_day(hour: int) -> TimeOfDay:
    if 5 <= hour < 12:
        return TimeOfDay.MORNING
    elif 12 <= hour < 17:
        return TimeOfDay.AFTERNOON
    else:
        return TimeOfDay.EVENING


class SpeedTest:
    def __init__(self):
        # Initialize Logger
        self.logger = logging.getLogger(__name__)

    def _execute_speedtest(self) -> str:
        """Execute speedtest CLI command and return raw output."""
        try:
            self.logger.info("Running speedtest CLI command")
            result = subprocess.run(['speedtest', '--format', 'json'], capture_output=True, text=True)
        except Exception as e:
            self.logger.error("Error running speedtest CLI.")
            raise e

        if result.returncode != 0:
            self.logger.error(f"Error running speedtest, return code was {result.returncode} (should be 0).")
            raise RuntimeError("Speed test failed.")

        return result.stdout

    @staticmethod
    def _parse_speedtest_output(output: str) -> SpeedTestResult:
        """Parse JSON output from speedtest CLI and return a SpeedTestResult."""
        data = json.loads(output)

        # General info
        timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        server = data['server']
        time_of_day = determine_time_of_day(timestamp.hour)

        # Numerical Data
        latency = data['ping']['latency']
        download_speed = data['download']['bandwidth'] / 125_000
        upload_speed = data['upload']['bandwidth'] / 125_000

        return SpeedTestResult(
            timestamp=timestamp,
            download_speed=download_speed,
            upload_speed=upload_speed,
            latency=latency,
            time_of_day=time_of_day,
            server=server)

    def run_test(self) -> SpeedTestResult:
        """Run a speed test and return parsed results."""
        raw_output = self._execute_speedtest()
        speed_result = SpeedTest._parse_speedtest_output(raw_output)
        self.logger.info("Speed test successful")
        return speed_result
