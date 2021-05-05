import pytest

from wagtail_email_subscription.client import AbstractClient, ActiveCampaignClient
from wagtail_email_subscription.exceptions import APIException


def test_client_base_class():
    assert issubclass(ActiveCampaignClient, AbstractClient)


def test_client_init(active_campaign_client):
    assert active_campaign_client.configured


def test_client_unique_hash(active_campaign_client):
    assert active_campaign_client.configured
    # this is a md5 hash of the api_key
    assert active_campaign_client.unique_hash == "068313611e622b4c273efe7ce6cd7aef"


def test_client_check_credentials_valid(active_campaign_client):
    assert active_campaign_client.check_credentials()


def test_client_check_credentials_not_configured(active_campaign_client):
    active_campaign_client.configured = False
    assert active_campaign_client.check_credentials() is False


def test_client_check_credentials_invalid(invalid_active_campaign_client):
    assert invalid_active_campaign_client.check_credentials() is False


def test_client_check_credentials_wrong_api_key(active_campaign_client):
    active_campaign_client.api_key = "invalid-api-key"
    assert active_campaign_client.check_credentials() is False


def test_client_get_lists(active_campaign_client):
    response = active_campaign_client.get_lists()
    assert len(response) == 2
    assert response[0]["name"] == "My list"


def test_client_create_or_update_subscriber(active_campaign_client):
    data = {
        "email": "test@test.com",
        "firstName": "First Name",
        "lastName": "Last Name",
    }
    response = active_campaign_client.create_or_update_subscriber(data)
    assert "email" in response
    assert response["email"] == "test@test.com"


def test_client_create_or_update_subscriber_error(active_campaign_client):
    data = {
        "email": "error@error.com",
        "firstName": "First Name",
        "lastName": "Last Name",
    }
    with pytest.raises(APIException):
        active_campaign_client.create_or_update_subscriber(data)


def test_client_add_subscriber_to_list(active_campaign_client):
    response = active_campaign_client.add_subscriber_to_list(
        contact_id="1", list_id="1"
    )
    assert response["contact"] == "1"
    assert response["list"] == "1"


def test_client_add_subscriber_to_unkown_list(active_campaign_client):
    with pytest.raises(APIException):
        active_campaign_client.add_subscriber_to_list(contact_id="1", list_id="999")
