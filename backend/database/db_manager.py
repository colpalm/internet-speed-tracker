import logging
import os

from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from database.models import Base, SpeedTestRecord, SpeedTestSummary
from shared.enums import TimeOfDay
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
        self.create_summary_view()

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

            # Select IDs of the latest records
            id_subquery = select(SpeedTestRecord.id).order_by(SpeedTestRecord.timestamp.desc()).limit(limit)

            # Select full records matching IDs
            stmt = (
                select(SpeedTestRecord)
                .where(SpeedTestRecord.id.in_(id_subquery))
                .order_by(SpeedTestRecord.timestamp.asc() if ascending else SpeedTestRecord.timestamp.desc())
            )

            records = session.execute(stmt).scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving speed test records: {e}")
        finally:
            if session:
                session.close()

        return records

    def create_summary_view(self) -> None:
        """Create the speed_test_summary view if it doesn't exist."""
        session = None
        try:
            session = self.session_factory()

            logger.info("Creating/replacing speed_test_summary view")
            session.execute(
                text("""
                    CREATE OR REPLACE VIEW speed_test_summary AS
                    SELECT
                        CASE
                            WHEN time_of_day is NULL THEN 0
                            WHEN time_of_day = 'MORNING' THEN 1
                            WHEN time_of_day = 'AFTERNOON' THEN 2
                            WHEN time_of_day = 'EVENING' THEN 3
                        END AS id,
                        time_of_day,
                        NOW() as last_updated,
                        AVG(download_speed) as avg_download_speed,
                        MAX(download_speed) as max_download_speed,
                        MIN(download_speed) as min_download_speed,
                        AVG(upload_speed) as avg_upload_speed,
                        MAX(upload_speed) as max_upload_speed,
                        MIN(upload_speed) as min_upload_speed,
                        AVG(latency) as avg_latency,
                        MIN(latency) as min_latency,
                        MAX(latency) as max_latency,
                        COUNT(*) as test_count
                    FROM speed_test_records
                    GROUP BY ROLLUP(time_of_day);
                """)
            )
            session.commit()
            logger.info("Created speed_test_summary view")
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating summary stats view: {e}")
            if session:
                session.rollback()
        finally:
            if session:
                session.close()

    def get_speed_test_summary(self, time_of_day: TimeOfDay = None) -> list[SpeedTestSummary]:
        """Get speed test summary data from the view."""
        session = None
        records = []
        try:
            session = self.session_factory()
            query = session.query(SpeedTestSummary)

            if time_of_day:
                query = query.filter(SpeedTestSummary.time_of_day == time_of_day)

            records = query.all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving speed test summary: {e}")
        finally:
            if session:
                session.close()

        return records
