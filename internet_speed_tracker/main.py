import logging
from internet_speed_tracker.speed_test import SpeedTest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    spt = SpeedTest()
    speed_test_results = spt.run_test()