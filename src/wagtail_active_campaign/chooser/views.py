from django.core.cache import cache

from .base import ActiveCampaignChooserViewSet


class ActiveCampaignListChooserViewSet(ActiveCampaignChooserViewSet):
    is_searchable = True

    def call_client(self, client):
        result = cache.get_or_set(
            "active_campaign_list_choices", client.get_list_choices, 60
        )
        return list(result)
