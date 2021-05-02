from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from . import client as clients


@register_setting(icon="form")
class EmailSubscriptionSettings(BaseSetting):
    ACTIVE_CAMPAIGN = "active-campaign"
    PROVIDERS = ((ACTIVE_CAMPAIGN, "Active Campaign"),)

    provider = models.CharField(
        "Provider", max_length=255, choices=PROVIDERS, default=ACTIVE_CAMPAIGN
    )
    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable this integration",
        default=False,
    )
    api_url = models.URLField("API URL", help_text="The API URL", blank=True)
    api_key = models.CharField(
        "API key", max_length=255, help_text="The API key", blank=True
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("enabled"),
            ],
            heading="General settings",
        ),
        MultiFieldPanel(
            [
                FieldPanel("provider"),
                FieldPanel("api_url"),
                FieldPanel("api_key", widget=forms.PasswordInput(render_value=True)),
            ],
            heading="API settings",
        ),
    ]

    class Meta:
        verbose_name = "Email Subscription Settings"
        verbose_name_plural = "Email Subscription Settings"

    def clean(self):
        super().clean()

        if not self.enabled:
            return

        client = self.get_client()
        if not client.check_credentials():
            raise ValidationError("Invalid url or API key")

    def get_client(self):
        if self.provider == self.ACTIVE_CAMPAIGN:
            return clients.ActiveCampaignClient(self.api_url, self.api_key)

        raise ImproperlyConfigured("No valid provider class found!")
