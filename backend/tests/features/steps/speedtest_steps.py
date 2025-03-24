from datetime import datetime, timezone
import logging

from behave import given, when, then
import subprocess
from speedtest.speed_test import SpeedTest

logging.basicConfig(level=logging.INFO)


@given('I have the librespeed cli installed')
def step_impl(context):
    result = subprocess.run(['librespeed-cli', '--version'], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


@when('I run the speed test')
def step_impl(context):
    speedtest = SpeedTest()
    context.result = speedtest.run_test()
    # record current time of day for validation
    current_time = datetime.now(timezone.utc)
    local_hour = SpeedTest._get_local_hour(current_time)
    context.expected_time_of_day = SpeedTest._determine_time_of_day(local_hour)


@then('I can the see the output from the speedtest')
def step_impl(context):
    result = context.result
    assert result.timestamp is not None, "Timestamp does not have a value"
    assert result.download_speed is not None, "DownloadSpeed does not have a value"
    assert result.upload_speed is not None, "UploadSpeed does not have a value"
    assert result.time_of_day == context.expected_time_of_day, \
        f"speedtest time of day {result.time_of_day}: context time of day: {context.expected_time_of_day}"