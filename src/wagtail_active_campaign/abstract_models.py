from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField

from .chooser.widgets import ListChooserWidget


class AbstractActiveCampaignFormField(AbstractFormField):
    # TODO: Make this a setting and/or dynamic
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


class AbstractActiveCampaignForm(AbstractForm):
    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable the Active Campaign integration of this form",
        default=False,
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
                FieldPanel("selected_list", widget=ListChooserWidget),
            ],
            heading="Active Campaign settings",
        ),
    ]

    submission_panels = [
        FormSubmissionsPanel(),
    ]

    template = "wagtail_active_campaign/form_page.html"

    class Meta(AbstractForm.Meta):
        abstract = True
