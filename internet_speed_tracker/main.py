import logging

import logging
import speed_test

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    spt = speed_test.SpeedTest()
    spt.run_test()