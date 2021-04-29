def get_active_campaign_settings(site):
    """
    This utility function exists as we need the ActiveCampaignSettings in several
    places where circular imports can occur
    """
    from wagtail_active_campaign.models import ActiveCampaignSettings

    return ActiveCampaignSettings.for_site(site)
