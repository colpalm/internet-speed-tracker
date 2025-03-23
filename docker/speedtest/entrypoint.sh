#!/bin/bash
set -e

echo "Starting speed test..."
python -m speedtest.main
echo "Speed test completed successfully."