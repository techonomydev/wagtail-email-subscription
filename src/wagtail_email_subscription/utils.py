def get_email_subscription_settings(site):
    """
    This utility function exists as we need the EmailSubscriptionSettings in several
    places where circular imports can occur
    """
    from wagtail_email_subscription.models import EmailSubscriptionSettings

    return EmailSubscriptionSettings.for_site(site)
