import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from backend.database.models import Base, SpeedTestRecord
from internet_speed_tracker.speed_test_result import SpeedTestResult

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///speed_tests.db"):
        """
        Initialize the database manager with a connection URL.

        Args:
            db_url (str): SQLAlchemy database URL. Defaults to a local SQLite database.
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        """Create all tables if they don't exist."""
        logger.info("Initializing database tables")
        Base.metadata.create_all(self.engine)

    def save_speed_test_result(self, result: SpeedTestResult) -> bool:
        """Save a speedtest result to the database.
        Args:
            result (SpeedTestResult): The speed test result to save

        Returns:
            bool: True if save was successful, False otherwise
        """
        session = None
        try:
            session = self.Session()

            # Extract server info
            server_id = result.server.get("id") if result.server else None
            server_name = result.server.get("name") if result.server else None

            record = SpeedTestRecord(
                timestamp=result.timestamp,
                download_speed=result.download_speed,
                upload_speed=result.upload_speed,
                latency=result.latency,
                time_of_day=result.time_of_day,
                server_id=server_id,
                server_name=server_name
            )

            session.add(record)
            session.commit()
            logger.info(f"Saved speed test result from {result.timestamp}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database error while saving speed test result: {e}")
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()

    def get_latest_speed_tests(self, limit: int = 10) -> list[SpeedTestRecord]:
        """
        Retrieve the most recent speed test records.

        Args:
            limit (int): Maximum number of records to return

        Returns:
            List of SpeedTestRecord objects
        """
        session = None
        try:
            session = self.Session()
            records = session.query(SpeedTestRecord) \
                .order_by(SpeedTestRecord.timestamp.desc()) \
                .limit(limit) \
                .all()
            return records
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving speed test records: {e}")
            return []
        finally:
            if session:
                session.close()
