from django.core.cache import cache

from .base import ActiveCampaignChooserViewSet


class ActiveCampaignListChooserViewSet(ActiveCampaignChooserViewSet):
    is_searchable = True

    def call_client(self, client):
        result = cache.get_or_set(
            "active_campaign_list_choices", client.get_list_choices, 60
        )
        return list(result)

    def filter_result_by_search_term(self, result, search_term):
        return [row for row in result if search_term.lower() in row["title"].lower()]

    def get_object_string(self, item):
        return item["title"]
