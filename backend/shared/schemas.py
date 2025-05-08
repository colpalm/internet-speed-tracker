from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer

from shared.enums import TimeOfDay


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


class SpeedTestSummaryResult(BaseModel):
    time_of_day: Optional[TimeOfDay] = None
    avg_download_speed: float  # Mbps
    max_download_speed: float  # Mbps
    min_download_speed: float  # Mbps
    avg_upload_speed: float  # Mbps
    max_upload_speed: float  # Mbps
    min_upload_speed: float  # Mbps
    avg_latency: float  # ms
    max_latency: float  # ms
    min_latency: float  # ms
    test_count: int

    @field_serializer("time_of_day")
    def serialize_time_of_day(self, value: Optional[TimeOfDay]) -> Optional[str]:
        """if TimeOfDay, serialize to string, else return None"""
        return value.value if value else None
