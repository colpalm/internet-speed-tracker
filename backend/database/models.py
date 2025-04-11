from sqlalchemy import Column, Integer, Float, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
from shared.enums import TimeOfDay


Base = declarative_base()


class SpeedTestRecord(Base):
    __tablename__ = 'speed_test_records'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False) # Stored in UTC
    download_speed = Column(Float, nullable=False)  # Mbps
    upload_speed = Column(Float, nullable=False)  # Mbps
    latency = Column(Float, nullable=False)  # ms
    time_of_day = Column(Enum(TimeOfDay), nullable=False)
    server_name = Column(String)
    server_url = Column(String)

    def __repr__(self):
        return (f"<SpeedTestRecord(id={self.id}, timestamp={self.timestamp}, "
                f"download_speed={self.download_speed}, upload_speed={self.upload_speed}, "
                f"latency={self.latency}, time_of_day={self.time_of_day})>")
