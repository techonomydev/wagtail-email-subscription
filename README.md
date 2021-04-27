# wagtail-bootstrap-app
[![Django CI](https://github.com/maerteijn/wagtail-bootstrap-app/actions/workflows/ci.yml/badge.svg)](https://github.com/maerteijn/wagtail-bootstrap-app/actions/workflows/ci.yml)

A clean Poetry based Wagtail app which includes CI

## Install with poetry
```bash
git clone https://github.com/maerteijn/wagtail-bootstrap-app
pip install poetry

# This will also create a virtualenv when not activated
poetry install
```

## Linting
`flake8-black` and `flake8-isort` are installed too. The flake8-pylint pluging is still
in early development, so we need to call pylint manually
```bash
flake8
pylint src/
```

## Black
```bash
black src/
```

## Isort
```bash
isort .
```

## Test
Pytest with coverage is default enabled
```bash
pytest
```

## Run the sandbox
`manage.py` is included in the sandbox for testing the app
```bash
sandbox/manage.py migrate
sandbox/manage.py createsuperuser
sandbox/manage.py runserver
```

