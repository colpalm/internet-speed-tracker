# internet-speed-tracker
Track home internet speed

## Build and Run Tests
- Run `make full-build` to install dependencies, build frontend and run all tests
- See make file for other targets

## Deployment

### Run with Docker Compose
To start all services:
```bash
make docker-up
```
- This deploys the backend API, frontend, database and speedtest in Docker containers
- Access the frontend at `http://localhost:3000`

### Stop All Services
To stop and remove all running containers:
```bash
make docker-down
```

To remove the volume, run:
```bash
docker volume rm internet-speed-tracker_postgres_data
```

### Local Development
For development without Docker:
- Run `make dev` to deploy the backend and frontend services
- From the `backend` directory, run `poetry run python speedtest/main.py` to generate a speed test result.
- Access the frontend at `http://localhost:3000`
