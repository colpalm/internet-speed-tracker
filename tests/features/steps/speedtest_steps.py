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
    context.speedtest = speed_test.SpeedTest()
    context.speedtest.run_test()


@then('I can the see the output from the speedtest')
def step_impl(context):
    assert context.speedtest.timestamp is not None
    assert context.speedtest.download_speed is not None
    assert context.speedtest.upload_speed is not None
