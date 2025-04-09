import os

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database.db_manager import DatabaseManager
from shared.schemas import SpeedTestResult

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
        server={"id": latest_record.server_id, "name": latest_record.server_name}
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
            server={"id": record.server_id, "name": record.server_name}
        ) for record in records
    ]


