from wagtail.admin.edit_handlers import FieldPanel

from wagtail_email_subscription.utils import get_email_subscription_settings

from .widgets import ListChooserWidget


class EmailSubscriptionListPanel(FieldPanel):
    def on_instance_bound(self):
        self.widget = ListChooserWidget(page_instance=self.instance)

    def render_as_field(self):
        site = self.instance.get_site()

        if site is None:
            return "First save the page, then you can select a list"
        settings = get_email_subscription_settings(site)

        if settings and settings.enabled:
            return super().render_as_field()

        return "Configure and/or enable the Wagtail Email Subscription settings first"
