import subprocess
import json
import logging

from datetime import datetime
from shared.enums import TimeOfDay, SpeedTestServer
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
        """Execute librespeed-cli command and return raw output."""
        # Providing specific servers since default option was failing
        servers = [
            SpeedTestServer.NYC_CLOUVIDER,
            SpeedTestServer.ATLANTA_CLOUVIDER,
            SpeedTestServer.CHICAGO_SHARKTECH
        ]

        for server in servers:
            self.logger.info(f'Running librespeed-cli command with {server.location} (ID: {server.server_id})')
            try:
                result = subprocess.run(
                    ['librespeed-cli', '--json', '--server', str(server.server_id)],
                    capture_output=True,
                    text=True
                )
            except Exception as e:
                self.logger.error(f"Error running librespeed-cli with server {server.location}: {str(e)}.")
                continue  # move on to the next server

            if result.returncode == 0:
                return result.stdout

            self.logger.warning(f"Speed test with server {server.location} failed")
            self.logger.error(f"Return code was {result.returncode} (should be 0).")

        raise RuntimeError("Speed test failed with all designated servers.")

    @staticmethod
    def _parse_speedtest_output(output: str) -> SpeedTestResult:
        """Parse JSON output from librespeed-cli and return a SpeedTestResult."""
        data = json.loads(output)
        entry = data[0]

        # General info
        timestamp = datetime.fromisoformat(entry['timestamp'])
        server = entry['server']
        time_of_day = determine_time_of_day(timestamp.hour)

        # Numerical Data
        latency = entry['ping']
        download_speed = entry['download']
        upload_speed = entry['upload']

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
