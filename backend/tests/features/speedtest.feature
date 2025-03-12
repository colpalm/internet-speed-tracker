Feature: Test Speedtest functionality

  Scenario: Check download and upload speed
    Given I have the speedtest cli installed
    When I run the speed test
    Then I can the see the output from the speedtest