import pytest

from wagtail_email_subscription.client import ActiveCampaignClient
from wagtail_email_subscription.models import EmailSubscriptionSettings

from . import testdata
from .factories import FormPageSubmissionFactory, LocaleFactory, SiteFactory


@pytest.fixture(autouse=True)
def mock_active_campaign_requests(requests_mock):
    response_headers = {"content-type": "application/json"}

    def create_update_contact_callback(
        request, context
    ):  # pylint: disable=unused-argument
        if request.json()["contact"]["email"] == "error@error.com":
            return testdata.CREATE_UPDATE_CONTACT_ERROR
        return testdata.CREATE_UPDATE_CONTACT_OUTPUT

    def lists_callback(request, context):  # pylint: disable=unused-argument
        if request.headers["Api-Token"] == "invalid-api-key":
            # The real API just returns an empty string when the api key
            # is invalid
            return ""
        return testdata.LIST_OUTPUT

    def update_list_status_callback(
        request, context
    ):  # pylint: disable=unused-argument
        if request.json()["contactList"]["list"] == "999":
            return testdata.UPDATE_LIST_STATUS_ERROR
        return testdata.UPDATE_LIST_STATUS_OUTPUT

    requests_mock.get(
        "https://valid-server.api.activecampaign.com/api/3/lists",
        json=lists_callback,
        headers=response_headers,
    )

    requests_mock.get(
        "https://invalid-server.api.activecampaign.com/api/3/lists",
        exc=ConnectionError,
    )

    requests_mock.post(
        "https://valid-server.api.activecampaign.com/api/3/contact/sync",
        json=create_update_contact_callback,
        headers=response_headers,
    )

    requests_mock.post(
        "https://valid-server.api.activecampaign.com/api/3/contactLists",
        json=update_list_status_callback,
        headers=response_headers,
    )


@pytest.fixture
def active_campaign_client():
    return ActiveCampaignClient(
        url="https://valid-server.api.activecampaign.com", api_key="my-api-key"
    )


@pytest.fixture
def invalid_active_campaign_client():
    return ActiveCampaignClient(
        url="https://invalid-server.api.activecampaign.com", api_key="invalid-key"
    )


@pytest.fixture(scope="session")
def wagtail_site(django_db_setup, django_db_blocker):  # pylint: disable=unused-argument
    with django_db_blocker.unblock():
        LocaleFactory()
        return SiteFactory()


@pytest.fixture
def email_subscription_setttings(wagtail_site):
    return EmailSubscriptionSettings.for_site(wagtail_site)


@pytest.fixture
def form_page_submission(wagtail_site):  # pylint: disable=redefined-outer-name
    return FormPageSubmissionFactory(page=wagtail_site.root_page)
