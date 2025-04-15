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

To remove all services and volumes, run:
```bash
make docker-clean
```

### Frontend Development with Docker Backend
To run frontend dev server with docker backend:
- Run `make frontend-dev` to deploy the backend and frontend services
- Access the frontend at `http://localhost:3000`
- Tear down with `make frontend-dev-down`
