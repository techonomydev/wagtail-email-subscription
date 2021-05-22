import json
from urllib.parse import urlencode

from django.core.exceptions import ObjectDoesNotExist
from generic_chooser.widgets import AdminChooser


class EmailSubscriptionChooserWidget(AdminChooser):
    show_edit_link = False

    def __init__(self, *args, **kwargs):
        self.page_instance = kwargs.pop("page_instance", None)
        super().__init__(*args, **kwargs)

    def get_instance(self, value):
        # value is the stored value, so the raw content of a JSON Field
        value = json.loads(value)
        if not value:
            raise ObjectDoesNotExist(str(value))
        return value

    def get_title(self, instance):
        try:
            return instance["title"]
        except KeyError:
            return ""

    def get_choose_modal_url(self):
        choose_modal_url = super().get_choose_modal_url()
        site = self.page_instance.get_site()
        if site is not None:
            url_param = urlencode({"site_id": site.pk})
            choose_modal_url = f"{choose_modal_url}?{url_param}"
        return choose_modal_url


class ListChooserWidget(EmailSubscriptionChooserWidget):
    choose_modal_url_name = "list_chooser:choose"
