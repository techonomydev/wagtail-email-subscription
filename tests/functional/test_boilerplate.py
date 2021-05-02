def test_wagtail_email_subscription_installed(settings):
    assert "wagtail_email_subscription" in settings.INSTALLED_APPS
