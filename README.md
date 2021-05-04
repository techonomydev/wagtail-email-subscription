# wagtail-email-subscription
[![Django CI](https://github.com/techonomydev/wagtail-email-subscription/actions/workflows/ci.yml/badge.svg)](https://github.com/techonomydev/wagtail-email-subscription/actions/workflows/ci.yml)

Wagtail form builder integration with email marketing subscription platforms like Active Campaign. This package ships with a fully working app which also demonstrates how you can integrate this in your own wagtail website.

## Prerequisites
- Email Subsription Provider API credentials
- At least one added email subscription list (this is where your contacts will show up)


## Installation
Install the package from pypi
```bash
pip install wagtail-email-subscription
```

Or from github directly:
```bash
pip install https://github.com/maerteijn/wagtail-email-subscription.git
```

Add the following to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    "wagtail_email_subscription",
    "wagtail_email_subscription.contrib.formpage",
    "generic_chooser",
]
```
*Note that the order is important here: `generic_chooser` should be after `"wagtail_email_subscription`*

And finally run the migrations:
```bash
manage.py migrate
```

## Configuration
- Login your wagtail admin and go to the site settings
- Add your API url and key to the `Email Subscription Settings` tab, make sure to enable the settings
- Create a new page which has the forms implemented  (`contrib.formpage` includes a ready to use `Form Page`)
- Add at least an email field and choose the correct mapping (also `email`)
- Go to the page settings tab and select a list where the contacts should go, make sure to enable the settings


## Development (with poetry)
```bash
git clone https://github.com/maerteijn/wagtail-email-subscription

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