.PHONY: full-build backend-all frontend-all \
		install-dependencies pytest-tests behave-tests python-clean-up \
		frontend-lint frontend-build frontend-deploy dev

# Runs all backend targets
full-build: backend-all frontend-all
backend-all: install-dependencies pytest-tests behave-tests python-clean-up
frontend-all: frontend-lint frontend-build

## Backend Commands ##

# Install poetry dependencies
install-dependencies:
	cd backend && poetry install --with dev

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

## Frontend Commands ##

# Lint frontend
frontend-lint:
	cd frontend && npm run lint

# Build frontend
frontend-build:
	cd frontend && npm run build

# Deploy frontend locally
frontend-deploy:
	cd frontend && npm run dev


## Deploy Locally ##

# Deploy frontend and backend
dev:
	@echo "Starting development environment..."
	@echo "Press Ctrl+C to stop all processes."
	@trap 'kill $$(jobs -p)' EXIT; \
	cd backend && poetry run uvicorn api.app:app --reload --port 8000 & \
	cd frontend && npm run dev

