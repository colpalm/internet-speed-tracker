# internet-speed-tracker
Track home internet speed

## Run Tests
- Integration Tests: From the root of the project, execute `poetry run behave tests/features`
- Unit Tests: From the root of the project, execute `poetry run pytest`
  - To change log settings, update pytest.ini, `log_cli = true` or add the cli flag: `poetry run pytest --log-cli-level=INFO`