from django.core.cache import cache

from .base import EmailSubscriptionChooserViewSet


class EmailSubscriptionListChooserViewSet(EmailSubscriptionChooserViewSet):
    is_searchable = True

    def call_client(self, client):
        result = cache.get_or_set(
            f"{client.unique_hash}_get_lists", client.get_lists, 60
        )
        return list(result)
