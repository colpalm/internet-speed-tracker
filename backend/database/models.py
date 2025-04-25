from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, String, DateTime, Enum, MetaData
from sqlalchemy.orm import declarative_base
from shared.enums import TimeOfDay

# Base for tables
Base = declarative_base()

# Base for views / materialized views
BaseView = declarative_base(metadata=MetaData())

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

class SpeedTestSummary(BaseView):
    """
    SQLAlchemy model mapping to the speed_test_summary materialized view.
    Note: This is mapped to a MATERIALIZED view, not a regular view.
    """
    __tablename__ = 'speed_test_summary'

    time_of_day = Column(Enum(TimeOfDay), primary_key=True)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))
    avg_download_speed = Column(Float)
    max_download_speed = Column(Float)
    min_download_speed = Column(Float)
    avg_upload_speed = Column(Float)
    max_upload_speed = Column(Float)
    min_upload_speed = Column(Float)
    avg_latency = Column(Float)
    max_latency = Column(Float)
    min_latency = Column(Float)
    test_count = Column(Integer)

    __table_args__ = {'info': {'is_view': True}}
