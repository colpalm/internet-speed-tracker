from dataclasses import dataclass
from datetime import datetime
from internet_speed_tracker.enums import TimeOfDay


@dataclass
class SpeedTestResult:
    timestamp: datetime
    download_speed: float  # Mbps
    upload_speed: float  # Mbps
    latency: float  # ms
    time_of_day: TimeOfDay
    server: dict
