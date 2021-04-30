# wagtail-active-campaign
[![Django CI](https://github.com/maerteijn/wagtail-active-campaign/actions/workflows/ci.yml/badge.svg)](https://github.com/maerteijn/wagtail-active-campaign/actions/workflows/ci.yml)

Wagtail form builder integration with Active Campaign. This package ships with a fully working app which also demonstrates
how you can integrate this in your own wagtail website.

## Prerequisites
- Active Campaign API credentials (see the "development" section in your Active Campaign account settings)
- At least one added Active Campaign list (this is where your contacts will show up)


## Installation
Install the package from pypi
```bash
pip install wagtail-active-campaign
```

Or from github directly:
```bash
pip install https://github.com/maerteijn/wagtail-active-campaign.git
```

Add the following to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    "generic_chooser",
    "wagtail_active_campaign",
    "wagtail_active_campaign.contrib.formpage",
]
```

And finally run the migrations:
```bash
manage.py migrate
```

## Configuration
- Login your wagtail admin and go to the site settings
- Add your API url and key to the `Active Campaign Settings` tab, make sure to enable the settings
- Create a new page which has the forms implemented  (`contrib.formpage` includes a ready to use `Form Page`)
- Add at least an email field and choose the correct mapping (also `email`)
- Go to the page settings tab and select a list where the contacts should go, make sure to enable the settings


## Development (with poetry)
```bash
git clone https://github.com/maerteijn/wagtail-active-campaign

# This will also create a virtualenv when not activated
make install
```

## Linting
```bash
make lint
```

## Test
Pytest with coverage is default enabled
```bash
make test
```

## Run the sandbox
`manage.py` is included in the sandbox for testing the app
```bash
sandbox/manage.py migrate
sandbox/manage.py createsuperuser
sandbox/manage.py runserver
```

