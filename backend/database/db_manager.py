import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base, SpeedTestRecord
from shared.schemas import SpeedTestResult

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, db_url: str = None):
        """
        Initialize the database manager with a connection URL.

        Args:
            db_url (str): SQLAlchemy database URL. If None, will use environment variable or default to SQLite.
        """
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "sqlite:///speed_tests.db")

        self.engine = create_engine(db_url)
        self.session_factory = sessionmaker(bind=self.engine)

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
            session = self.session_factory()

            # Extract server info
            server_name = result.server.get("name") if result.server else None
            server_url = result.server.get("url") if result.server else None

            record = SpeedTestRecord(
                timestamp=result.timestamp,
                download_speed=result.download_speed,
                upload_speed=result.upload_speed,
                latency=result.latency,
                time_of_day=result.time_of_day,
                server_name=server_name,
                server_url=server_url,
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

    def get_latest_speed_tests(self, limit: int = 10, ascending: bool = False) -> list[SpeedTestRecord]:
        """
        Retrieve the most recent speed test records.

        Args:
            limit (int): Maximum number of records to return
            ascending (bool): If True, sort from oldest to newest, otherwise newest to oldest

        Returns:
            List of SpeedTestRecord objects
        """
        session = None
        records = []
        try:
            session = self.session_factory()
            
            # Create a subquery to get the IDs of the latest records
            subquery = session.query(SpeedTestRecord.id)\
                .order_by(SpeedTestRecord.timestamp.desc())\
                .limit(limit)\
                .subquery()

            # Determine order clause
            order_clause = SpeedTestRecord.timestamp.asc() if ascending else SpeedTestRecord.timestamp.desc()
            
            # Main query to fetch records with the desired sort order
            query = session.query(SpeedTestRecord)\
                .filter(SpeedTestRecord.id.in_(subquery))\
                .order_by(order_clause)
            
            records = query.all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving speed test records: {e}")
        finally:
            if session:
                session.close()

        return records