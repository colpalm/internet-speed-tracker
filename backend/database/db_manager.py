import logging
import os

from sqlalchemy import create_engine, inspect, text, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base, SpeedTestRecord, SpeedTestSummary
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
        self.create_summary_mat_view()

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

            # Refresh materialized view after saving new data
            self.refresh_summary_mat_view()

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
            id_subquery = (
                select(SpeedTestRecord.id)
                .order_by(SpeedTestRecord.timestamp.desc())
                .limit(limit)
            )

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

    def create_summary_mat_view(self) -> None:
        """Create the speed_test_summary materialized view if it doesn't exist."""
        session = None
        try:
            session = self.session_factory()

            # Check if the view exists
            inspector = inspect(self.engine)
            view_exists = "speed_test_summary" in inspector.get_view_names()
            if not view_exists:
                logger.info("Creating speed_test_summary materialized view")
                session.execute(text("""
                CREATE MATERIALIZED VIEW speed_test_summary AS
                -- Time of day specific stats
                SELECT
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
                GROUP BY time_of_day

                UNION ALL

                -- Overall stats across all time periods
                SELECT 
                    'ALL' as time_of_day,
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
                FROM speed_test_records;
                """))
                session.commit()
                logger.info("Created speed_test_summary materialized view")
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating summary materialized view: {e}")
            if session:
                session.rollback()
        finally:
            if session:
                session.close()

    def refresh_summary_mat_view(self) -> None:
        """Refresh the speed_test_summary materialized view with the latest data."""
        session = None
        try:
            session = self.session_factory()
            session.execute(text("REFRESH MATERIALIZED VIEW speed_test_summary;"))
            session.commit()
            logger.info("Refreshed speed_test_summary materialized view")
        except SQLAlchemyError as e:
            logger.error(f"Database error while refreshing summary materialized view: {e}")
            if session:
                session.rollback()
        finally:
            if session:
                session.close()

    def get_speed_test_summary(self, time_of_day=None) -> list[SpeedTestSummary]:
        """Get speed test summary data from the materialized view."""
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