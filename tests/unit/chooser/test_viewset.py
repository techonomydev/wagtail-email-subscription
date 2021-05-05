import pytest

from tests import testdata
from wagtail_email_subscription.chooser.views import EmailSubscriptionListChooserViewSet


@pytest.mark.django_db
def test_list_chooser_viewset_call_client(active_campaign_client):
    viewset = EmailSubscriptionListChooserViewSet(
        "list_chooser", url_prefix="active-campaign-lists"
    )
    result = viewset.call_client(active_campaign_client)
    assert result == testdata.LIST_OUTPUT["lists"]
