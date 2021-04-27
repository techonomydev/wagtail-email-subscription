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
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .client import Client


@register_setting(icon="form")
class ActiveCampaignSettings(BaseSetting):
    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable the Active Campaign integration",
        default=False,
    )
    api_url = models.URLField("API URL", help_text="The Active Campaign API URL", blank=True)
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
                FieldPanel("api_key"),
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

        client = Client(self.api_url, self.api_key)
        if not client.check_credentials():
            raise ValidationError("Invalid url or API key")


class AbstractActiveCampaignFormField(AbstractFormField):
    ACTIVE_CAMPAIN_FIELDNAMES = (
        ("email", "email"),
        ("firstName", "firstName"),
        ("lastName", "lastName"),
        ("phone", "phone"),
    )
    mapping = models.CharField(
        "Map field to",
        max_length=255,
        blank=True,
        help_text="Select the mapped Active Campaign field",
        choices=ACTIVE_CAMPAIN_FIELDNAMES,
    )

    panels = AbstractFormField.panels + [FieldPanel("mapping")]

    class Meta(AbstractFormField.Meta):
        abstract = True


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


class ActiveCampaignAdminForm(WagtailAdminPageForm):
    selected_list = forms.ChoiceField(choices=(), required=False, disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site = self.instance.get_site()

        if site is None:
            return

        settings = ActiveCampaignSettings.for_site(site)

        if settings.enabled:
            client = Client(settings.api_url, settings.api_key)

            if not client.check_credentials():
                return
            # TODO: cache the results
            list_choices = client.get_list_choices()
            self.fields["selected_list"].disabled = False
            self.fields["selected_list"].choices = list_choices


class AbstractActiveCampaignForm(AbstractForm):
    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable the Active Campaign integration of this form",
        default=True,
    )
    selected_list = models.CharField(
        "List",
        max_length=255,
        blank=True,
        help_text="Select the Active Campaign list where the new subscribers will be a member of after submission",
    )

    settings_panels = AbstractForm.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("enabled"),
                FieldPanel("selected_list"),
            ],
            heading="Active Campaign settings",
        ),
    ]

    submission_panels = [
        FormSubmissionsPanel(),
    ]

    base_form_class = ActiveCampaignAdminForm
    template = "wagtail_active_campaign/form_page.html"

    class Meta(AbstractForm.Meta):
        abstract = True


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

    # Do not allow these pages per default to be shown in wagtail
    parent_page_types = []
