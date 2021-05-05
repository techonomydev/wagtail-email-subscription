import hashlib
import logging
from abc import ABC, abstractmethod

from activecampaign import client

from .exceptions import APIException

logger = logging.getLogger(__name__)


class AbstractClient(ABC):
    @abstractmethod
    def check_credentials(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def unique_hash(self):
        raise NotImplementedError

    @abstractmethod
    def get_lists(self):
        raise NotImplementedError

    @abstractmethod
    def create_or_update_subscriber(self, data):
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_to_list(self, contact_id, list_id):
        raise NotImplementedError


class ActiveCampaignClient(AbstractClient, client.Client):
    configured = False

    MANDATORY_FIELDS = ("email",)
    SUBSCRIBED = 1
    UNSUBSCRIBED = 2

    def __init__(self, url, api_key):
        if url and api_key:
            self.configured = True
            super().__init__(url, api_key)

    @property
    def unique_hash(self):
        if self.configured:
            return hashlib.md5(self.api_key.encode()).hexdigest()

    def check_credentials(self):
        if not self.configured:
            return False
        try:
            response = self.lists.retrieve_all_lists(limit=1)
        except ConnectionError as e:
            logger.error(str(e))
            return False

        if isinstance(response, str) and len(response) == 0:
            return False
        return True

    def get_lists(self):
        # TODO: Check for nr of results and do as much lookups as needed, or implement
        # pagination
        response = self.lists.retrieve_all_lists(limit=100)
        return response["lists"]

    def create_or_update_subscriber(self, data):
        post_data = {"contact": data}
        response = self.contacts.create_or_update_contact(post_data)
        if "errors" in response:
            raise APIException(response["errors"])
        return response["contact"]

    def add_subscriber_to_list(self, contact_id, list_id):
        post_data = {
            "contactList": {
                "list": list_id,
                "contact": contact_id,
                "status": self.SUBSCRIBED,
            }
        }
        response = self.contacts.update_list_status_for_a_contact(post_data)
        if "errors" in response:
            raise APIException(response["errors"])

        return response["contactList"]
