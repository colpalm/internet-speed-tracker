import subprocess
import json
import logging

from datetime import datetime
from internet_speed_tracker.enums import TimeOfDay


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
        self.logger.setLevel(logging.DEBUG)

        # Initialize fields
        self.timestamp = None
        self.download_speed = None
        self.upload_speed = None
        self.latency = None
        self.time_of_day = None
        self.server = None

    def run_test(self):
        try:
            logging.info("Running speed test")
            result = subprocess.run(['speedtest', '--format', 'json'], capture_output=True, text=True)
        except Exception as e:
            self.logger.error("Error running speedtest.")
            raise e

        if result.returncode == 0:
            data = json.loads(result.stdout)

            # General info
            self.timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            self.server = data['server']
            self.time_of_day = determine_time_of_day(self.timestamp.hour)

            # Numbers
            self.latency = data['ping']['latency']
            self.download_speed = data['download']['bandwidth'] / 125_000
            self.upload_speed = data['upload']['bandwidth'] / 125_000

            logging.info("Speed test successful")

        else:
            self.logger.error(f"Error running speedtest, return code was {result.returncode} (should be 0).")