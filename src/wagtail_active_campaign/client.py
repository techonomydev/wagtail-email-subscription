from activecampaign import client


class Client(client.Client):
    configured = False

    def __init__(self, url, api_key):
        if url and api_key:
            self.configured = True
            super().__init__(url, api_key)

    def check_credentials(self):
        if not self.configured:
            return False

        response = self.lists.retrieve_all_lists()
        if isinstance(response, str) and len(response) == 0:
            return False
        return True

    def get_list_choices(self):
        # TODO: Check for nr of results and do as much lookups as needed, or implement
        # pagination
        response = self.lists.retrieve_all_lists(limit=100)
        return [{"id": x["stringid"], "title": x["name"]} for x in response["lists"]]
