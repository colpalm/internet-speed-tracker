# internet-speed-tracker
Track home internet speed

## Build and Run Tests
- Run `make backend-all` to install dependencies and run python tests
- Run `make frontend-build` to build the frontend

## Deploy Locally
- Run `make dev` to deploy the backend and frontend services
- From the `backend` directory, run `poetry run python internet_speed_tracker/main.py` to generate a speed test result.