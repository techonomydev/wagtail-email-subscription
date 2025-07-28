.PHONY: install lint test

install:
	pip install poetry
	poetry install

lint:
	flake8 src tests sandbox
	pylint src tests sandbox

test:
	pytest

cov:
	pytest --cov=wagtail_email_subscription

format:
	black src tests sandbox
	isort src tests sandbox