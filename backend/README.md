# Internet Speed Tracker - Backend

This is the **backend** for the Internet Speed Tracker App.

## Getting Started
### Install Dependencies
Run the following to install dependencies:
```bash
poetry install
```

### Start the backend development server
```bash
poetry run uvicorn api.app:app --reload
```

### Generate Speed Test Results
```bash
poetry run python internet_speed_tracker/main.py
```
