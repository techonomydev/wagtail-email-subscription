from urllib.parse import urlencode

from django.core.exceptions import ObjectDoesNotExist
from generic_chooser.widgets import AdminChooser


class EmailSubscriptionChooserWidget(AdminChooser):
    show_edit_link = False

    def __init__(self, *args, **kwargs):
        self.page_instance = kwargs.pop("page_instance", None)
        super().__init__(*args, **kwargs)

    def get_instance(self, value):
        # value is the stored value, the value of a CharField or IntegerField
        # from a Django model
        if not value:
            raise ObjectDoesNotExist(str(value))
        return value

    def get_choose_modal_url(self):
        choose_modal_url = super().get_choose_modal_url()
        site_id = self.page_instance.get_site().pk
        url_param = urlencode({"site_id": site_id})
        return f"{choose_modal_url}?{url_param}"


class ListChooserWidget(EmailSubscriptionChooserWidget):
    choose_modal_url_name = "list_chooser:choose"
