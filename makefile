.PHONY: full-build verify-code backend-verify frontend-verify \
		install-dependencies pytest-tests behave-tests python-clean-up \
		docker-build docker-build-api docker-build-speedtest docker-build-frontend \
		frontend-install frontend-lint \
		dev docker-up docker-down

# Build version
VERSION?=1.0.0-dev

# Main build target - verify code then build images
full-build: verify-code docker-build

# Verify code
verify-code: backend-verify frontend-verify

# Backend verification
backend-verify: install-dependencies pytest-tests behave-tests python-clean-up

# Frontend verification
frontend-verify: frontend-install frontend-lint

# Build all docker images
docker-build: docker-build-api docker-build-speedtest docker-build-frontend

## Backend Commands ##

# Install poetry dependencies
install-dependencies:
	cd backend && poetry lock && poetry install --with dev

# Run pytest unit tests
pytest-tests:
	cd backend && poetry run pytest

# Run behave integration tests
behave-tests:
	cd backend && poetry run behave tests/features

# Clean up __pycache__ and .pyc files
python-clean-up:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

## Docker Build Commands ##

# API DB Image Build
docker-build-api:
	poetry -C backend lock
	docker build -t internet-speed-tracker-api:$(VERSION) -f docker/server/Dockerfile .

# Speedtest Image Build
docker-build-speedtest:
	poetry -C backend lock
	docker build -t internet-speed-tracker-speedtest:$(VERSION) -f docker/speedtest/Dockerfile .

docker-build-frontend:
	cd frontend && npm install --package-lock-only
	docker build -t internet-speed-tracker-frontend:$(VERSION) -f docker/frontend/Dockerfile .

## Frontend Commands ##

# Install frontend dependencies
frontend-install:
	cd frontend && npm install

# Lint frontend
frontend-lint:
	cd frontend && npm run lint

## Deploy Locally ##

# Deploy frontend and backend
dev:
	@echo "Starting development environment..."
	@echo "Press Ctrl+C to stop all processes."
	@trap 'kill $$(jobs -p)' EXIT; \
	cd backend && poetry run uvicorn api.app:app --reload --port 8000 & \
	cd frontend && npm run dev

docker-up:
	@echo "Starting all services"
	VERSION=$(VERSION) docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.speedtest.yml up

docker-down:
	@echo "Stopping all Docker Compose services..."
	VERSION=$(VERSION) docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.speedtest.yml down

