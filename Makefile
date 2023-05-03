.PHONY: install lint test

install:
	pip install poetry
	poetry install

lint:
	flake8
	pylint src/

test:
	pytest

cov:
	pytest --cov=wagtail_email_subscription

