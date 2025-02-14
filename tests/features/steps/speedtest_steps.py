import datetime
import logging

from behave import given, when, then
import subprocess
from internet_speed_tracker import speed_test

logging.basicConfig(level=logging.INFO)


@given('I have the speedtest cli installed')
def step_impl(context):
    result = subprocess.run(['speedtest', '--version'], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


@when('I run the speed test')
def step_impl(context):
    speedtest = speed_test.SpeedTest()
    context.result = speedtest.run_test()
    # record current time of day for validation
    current_hour = datetime.datetime.now(datetime.UTC).hour
    context.expected_time_of_day = speed_test.determine_time_of_day(current_hour)


@then('I can the see the output from the speedtest')
def step_impl(context):
    result = context.result
    assert result.timestamp is not None, "Timestamp does not have a value"
    assert result.download_speed is not None, "DownloadSpeed does not have a value"
    assert result.upload_speed is not None, "UploadSpeed does not have a value"
    assert result.time_of_day == context.expected_time_of_day, \
        f"speedtest time of day {result.time_of_day}: context time of day: {context.expected_time_of_day}"