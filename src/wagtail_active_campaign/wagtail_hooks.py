from wagtail.core import hooks

from .chooser.views import ActiveCampaignListChooserViewSet


@hooks.register("register_admin_viewset")
def register_active_campaign_list_chooser_viewset():
    return ActiveCampaignListChooserViewSet(
        "list_chooser", url_prefix="active-campaign-lists"
    )
