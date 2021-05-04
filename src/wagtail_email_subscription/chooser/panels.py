from wagtail.admin.edit_handlers import FieldPanel

from .widgets import ListChooserWidget


class FieldPanelWithPage(FieldPanel):
    def on_instance_bound(self):
        self.widget = ListChooserWidget(page_instance=self.instance)
