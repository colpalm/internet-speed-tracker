import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from database.db_manager import DatabaseManager
from shared.enums import TimeOfDay
from shared.schemas import SpeedTestResult, SpeedTestSummaryResult

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Read CORS settings
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(title="Internet Speed Tracker API")

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# Initialize DB
db_manager = DatabaseManager()
db_manager.init_db()


@app.post("/api/speed-tests", status_code=status.HTTP_201_CREATED)
async def save_speed_test_result(result: SpeedTestResult) -> dict[str, str]:
    """
    Save individual speed test results.
    """
    saved_status = db_manager.save_speed_test_result(result)
    if saved_status:
        return {"message": "Speed test result saved successfully"}
    raise HTTPException(status_code=500, detail="Failed to save speed test result")


@app.get("/api/speed-tests/latest", response_model=SpeedTestResult)
async def get_latest_speed_test_result() -> SpeedTestResult:
    """
    Fetch the most recent speed test result from the database.
    """
    records = db_manager.get_latest_speed_tests(limit=1)
    if not records:
        raise HTTPException(status_code=404, detail="Speed test result not found")

    latest_record = records[0]

    return SpeedTestResult(
        timestamp=latest_record.timestamp,
        download_speed=latest_record.download_speed,
        upload_speed=latest_record.upload_speed,
        latency=latest_record.latency,
        time_of_day=latest_record.time_of_day,
        server={"name": latest_record.server_name, "url": latest_record.server_url},
    )


@app.get("/api/speed-tests", response_model=list[SpeedTestResult])
async def get_speed_test_results(limit: int = 10, ascending: bool = True) -> list[SpeedTestResult]:
    """
    Fetch multiple speed test results from the database.

    Args:
        limit: Maximum number of results to return (default: 10)
        ascending: Sort from oldest to newest if True (default: True)
    """
    records = db_manager.get_latest_speed_tests(limit=limit, ascending=ascending)
    if not records:
        raise HTTPException(status_code=404, detail="Speed test results not found")

    return [
        SpeedTestResult(
            timestamp=record.timestamp,
            download_speed=record.download_speed,
            upload_speed=record.upload_speed,
            latency=record.latency,
            time_of_day=record.time_of_day,
            server={"name": record.server_name, "url": record.server_url},
        )
        for record in records
    ]


@app.get("/api/speed-tests/summary", response_model=list[SpeedTestSummaryResult])
async def get_speed_test_summary(time_of_day: Optional[TimeOfDay] = None) -> list[SpeedTestSummaryResult]:
    """
    Fetch summary statistics for speed tests.

    Args:
        time_of_day: Filter by time of day (Morning, Afternoon, Evening, or ALL)
    """
    records = db_manager.get_speed_test_summary(time_of_day=time_of_day)
    if not records:
        raise HTTPException(status_code=404, detail="Speed test summary not found")

    return [
        SpeedTestSummaryResult(
            time_of_day=record.time_of_day,
            avg_download_speed=record.avg_download_speed,
            max_download_speed=record.max_download_speed,
            min_download_speed=record.min_download_speed,
            avg_upload_speed=record.avg_upload_speed,
            max_upload_speed=record.max_upload_speed,
            min_upload_speed=record.min_upload_speed,
            avg_latency=record.avg_latency,
            max_latency=record.max_latency,
            min_latency=record.min_latency,
            test_count=record.test_count,
        )
        for record in records
    ]
