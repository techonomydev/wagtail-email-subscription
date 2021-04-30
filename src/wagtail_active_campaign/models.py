from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .client import Client


@register_setting(icon="form")
class ActiveCampaignSettings(BaseSetting):
    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable the Active Campaign integration",
        default=False,
    )
    api_url = models.URLField(
        "API URL", help_text="The Active Campaign API URL", blank=True
    )
    api_key = models.CharField(
        "API key", max_length=255, help_text="The Active Campain API key", blank=True
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
                FieldPanel("api_url"),
                FieldPanel("api_key", widget=forms.PasswordInput(render_value=True)),
            ],
            heading="API settings",
        ),
    ]

    class Meta:
        verbose_name = "Active Campaign settings"
        verbose_name_plural = "Active Campaign settings"

    def clean(self):
        super().clean()

        if not self.enabled:
            return

        client = self.get_client()
        if not client.check_credentials():
            raise ValidationError("Invalid url or API key")

    def get_client(self):
        return Client(self.api_url, self.api_key)
