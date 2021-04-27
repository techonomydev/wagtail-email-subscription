def test_wagtail_active_campaign_installed(settings):
    assert "wagtail_active_campaign" in settings.INSTALLED_APPS
