from .base import ActiveCampaignChooserViewSet


class ActiveCampaignListChooserViewSet(ActiveCampaignChooserViewSet):
    is_searchable = True

    def call_client(self, client):
        return client.get_list_choices()

    def filter_result_by_search_term(self, result, search_term):
        for row in result:
            if search_term.lower() in row["title"].lower():
                yield row

    def get_object_string(self, item):
        return item["title"]
