from django.core.cache import cache

from .base import EmailSubscriptionChooserViewSet


class EmailSubscriptionListChooserViewSet(EmailSubscriptionChooserViewSet):
    is_searchable = True

    def call_client(self, client):
        result = cache.get_or_set(
            "email_subscription_list_choices", client.get_list_choices, 60
        )
        return list(result)
