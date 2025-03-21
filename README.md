# internet-speed-tracker
Track home internet speed

## Build and Run Tests
- Run `make full-build` to install backend dependencies, build frontend and run all tests
- See make file for other targets

## Deploy Locally
- Run `make dev` to deploy the backend and frontend services
- From the `backend` directory, run `poetry run python speedtest/main.py` to generate a speed test result.
- Access the frontend at `http://localhost:3000`