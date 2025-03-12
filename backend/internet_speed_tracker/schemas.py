from datetime import datetime
from pydantic import BaseModel, field_serializer
from internet_speed_tracker.enums import TimeOfDay


class SpeedTestResult(BaseModel):
    timestamp: datetime
    download_speed: float  # Mbps
    upload_speed: float  # Mbps
    latency: float  # ms
    time_of_day: TimeOfDay
    server: dict

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("time_of_day")
    def serialize_time_of_day(self, value: TimeOfDay) -> str:
        return value.value
