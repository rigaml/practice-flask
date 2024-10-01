.PHONY: run test test-cov

run:
	poetry run flask --app user_monitoring.main:app run --debug

test:
	poetry run python -m pytest -vvv

test-cov:
	poetry run python -m pytest -vvv --cov=user_monitoring
