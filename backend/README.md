# Internet Speed Tracker - Backend

This is the **backend** for the Internet Speed Tracker App.

## Testing
Run a specific pytest file
```bash
poetry run pytest path/to/file.py
```

Run a specific test
```bash
poetry run pytest path/to/file.py::test-name
```

Run integration tests
```bash
poetry run pytest -m integration
```

## Getting Started
### Install Dependencies
Run the following to install dependencies:
```bash
poetry install
```

### Start the backend development server (without Docker)
```bash
poetry run uvicorn api.app:app --reload
```

### Generate Speed Test Results (without Docker)
```bash
poetry run python speedtest/main.py
```
