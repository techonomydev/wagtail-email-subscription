from wagtail.core import hooks

from .chooser.views import EmailSubscriptionListChooserViewSet


@hooks.register("register_admin_viewset")
def register_email_subscription_list_chooser_viewset():
    return EmailSubscriptionListChooserViewSet(
        "list_chooser", url_prefix="active-campaign-lists"
    )
