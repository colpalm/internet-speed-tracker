.PHONY: full-build verify-code backend-verify frontend-verify \
		install-dependencies pytest-tests behave-tests python-clean-up \
		docker-build docker-build-api docker-build-speedtest docker-build-frontend \
		frontend-install frontend-lint \
		frontend-dev frontend-dev-down docker-up docker-down

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

# Deploy backend in docker and frontend with npm
frontend-dev:
	@echo "Starting backend services in Docker"
	VERSION=$(VERSION) docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.speedtest.yml up -d api db speedtest
	@echo "Starting frontend in development mode..."
	cd frontend && npm run dev

frontend-dev-down:
	@echo "Stopping backend services..."
	VERSION=$(VERSION) docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.speedtest.yml down api db speedtest

# Deploy full containerized application
docker-up:
	@echo "Starting all services"
	VERSION=$(VERSION) docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.speedtest.yml up

docker-down:
	@echo "Stopping all Docker Compose services..."
	VERSION=$(VERSION) docker compose --env-file ./backend/.env -f docker-compose.yml -f docker-compose.speedtest.yml down

