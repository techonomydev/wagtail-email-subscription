from wagtail.admin.panels import FieldPanel

from wagtail_email_subscription.utils import get_email_subscription_settings

from .widgets import ListChooserWidget


class EmailSubscriptionListPanel(FieldPanel):
    """Custom panel for email subscription list chooser."""

    def on_instance_bound(self):
        """Set up the widget when the panel is bound to an instance."""
        # pylint: disable=no-member
        self.widget = ListChooserWidget(page_instance=self.instance)

    def render_as_field(self):
        """Render the panel as a form field."""
        # pylint: disable=no-member
        site = self.instance.get_site()

        if site is None:
            return "First save the page, then you can select a list"
        settings = get_email_subscription_settings(site)

        if settings and settings.enabled:
            # pylint: disable=no-member
            return super().render_as_field()

        return "Configure and/or enable the Wagtail Email Subscription settings first"
