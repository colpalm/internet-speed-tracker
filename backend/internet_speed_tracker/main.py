import logging
import requests
from internet_speed_tracker.speed_test import SpeedTest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    spt = SpeedTest()
    speed_test_results = spt.run_test()

    url = "http://localhost:8000/api/speed-tests" # TODO: Move to env variable
    try:
        response = requests.post(url, json=speed_test_results.model_dump())
        if response.status_code == 201:
            logging.info("Successfully sent speed test result to API")
        else:
            logging.error(f"Failed to send speed test result, status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
    except Exception as e:
        logging.error(f"Error while sending POST request: {e}")