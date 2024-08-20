import subprocess
import json
import logging


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
            self.timestamp = data['timestamp']
            self.server = data['server']

            # Numbers
            self.latency = data['ping']['latency']
            self.download_speed = data['download']['bandwidth'] / 125_000
            self.upload_speed = data['upload']['bandwidth'] / 125_000

            logging.info("Speed test successful")

        else:
            self.logger.error(f"Error running speedtest, return code was {result.returncode} (should be 0).")