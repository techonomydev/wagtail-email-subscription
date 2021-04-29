from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .abstract_models import AbstractActiveCampaignForm, AbstractActiveCampaignFormField
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


class ActiveCampaignFormField(AbstractActiveCampaignFormField):
    form = ParentalKey(
        "ActiveCampaignForm", on_delete=models.CASCADE, related_name="form_fields"
    )

    class Meta(AbstractActiveCampaignFormField.Meta):
        constraints = (
            models.UniqueConstraint(
                name="A mapping field can only be used once for each form",
                fields=("form", "mapping"),
            ),
        )


class ActiveCampaignForm(AbstractActiveCampaignForm):
    content_panels = AbstractActiveCampaignForm.content_panels + [
        InlinePanel("form_fields", label="Form fields"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Form"),
            ObjectList(
                AbstractActiveCampaignForm.submission_panels, heading="Submissions"
            ),
            ObjectList(AbstractActiveCampaignForm.promote_panels, heading="Promote"),
            ObjectList(AbstractActiveCampaignForm.settings_panels, heading="Settings"),
        ]
    )

    def prepare_data_for_active_campain(self, data):
        # only use the fields which have a filled out mapping field
        qs = self.form_fields.exclude(mapping__exact="")  # pylint: disable=no-member
        qs = qs.values_list("mapping", "clean_name")

        return {mapping: data[clean_name] for mapping, clean_name in qs}

    # Do not make these pages available in the wagtail admin per default
    # TODO: Make this a setting
    parent_page_types = []
