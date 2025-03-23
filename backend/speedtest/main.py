import logging
import os

import requests
from speedtest.speed_test import SpeedTest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    spt = SpeedTest()
    speed_test_results = spt.run_test()

    #TODO: Set SPEEDTEST_API_URL
    api_url = os.environ.get('SPEEDTEST_API_URL', "http://localhost:8000")
    url = f"{api_url}/api/speed-tests"
    try:
        response = requests.post(url, json=speed_test_results.model_dump())
        if response.status_code == 201:
            logging.info("Successfully sent speed test result to API")
        else:
            logging.error(f"Failed to send speed test result, status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
    except Exception as e:
        logging.error(f"Error while sending POST request: {e}")