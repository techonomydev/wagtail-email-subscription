from django.core.exceptions import ObjectDoesNotExist
from generic_chooser.widgets import AdminChooser


class ActiveCampaignChooserWidget(AdminChooser):
    show_edit_link = False

    def get_instance(self, value):
        # value is the stored value, the value of a CharField or IntegerField
        # from a Django model
        if not value:
            raise ObjectDoesNotExist(str(value))
        return value


class ListChooserWidget(ActiveCampaignChooserWidget):
    choose_modal_url_name = "list_chooser:choose"
