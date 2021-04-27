def test_wagtail_bootstrap_app_installed(settings):
    assert "wagtail_bootstrap_app" in settings.INSTALLED_APPS
