.PHONY: install lint test

install: bootstrap
	poetry install

bootstrap:
	pip install "pip>=25.0,<25.1" "poetry>=2.1.3,<2.2"

lint:
	flake8
	pylint src/

test:
	pytest

cov:
	pytest --cov=wagtail_email_subscription

