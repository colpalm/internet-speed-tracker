.PHONY: all install-dependencies pytest-tests behave-tests clean-up

# Runs all the targets
all: install-dependencies pytest-tests behave-tests clean-up

# Install poetry dependencies
install-dependencies:
	poetry install

# Run pytest unit tests
pytest-tests:
	poetry run pytest

# Run behave integration tests
behave-tests:
	poetry run behave tests/features

# Clean up __pycache__ and .pyc files
clean-up:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete