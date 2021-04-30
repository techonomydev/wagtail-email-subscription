import logging

from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField

from .chooser.widgets import ListChooserWidget
from .utils import get_active_campaign_settings

logger = logging.getLogger(__name__)


class AbstractActiveCampaignForm(AbstractForm):
    FORM_FIELD = "form"
    FORM_FIELDS_REVERSE = "form_fields"

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

    content_panels = AbstractForm.content_panels

    template = "wagtail_active_campaign/form_page.html"

    class Meta(AbstractForm.Meta):
        abstract = True

    def post_data_to_active_campaign(self, list_id, data):
        # TODO move the actual posting logic to the client
        site = self.get_site()
        settings = get_active_campaign_settings(site)

        if not settings.enabled:
            logger.warning("Check your settings as Active Campaign is not enabled!")
            return

        client = settings.get_client()
        if not client.check_credentials():
            logger.error("Active Campaign credentials are not set correctly!")
            return

        contact = client.create_or_update_contact(data)
        client.add_contact_to_list(contact_id=contact["id"], list_id=list_id)

    def prepare_data_for_active_campain(self, data):
        # only use the fields which have a filled out mapping field
        qs = getattr(self, self.FORM_FIELDS_REVERSE)
        qs = qs.exclude(mapping__exact="")
        qs = qs.values_list("mapping", "clean_name")

        return {mapping: data[clean_name] for mapping, clean_name in qs}

    def process_form_submission(self, form):
        instance = super().process_form_submission(form)

        # TODO: get the data from the submission model and do the handling there!
        if self.enabled:
            post_data = self.prepare_data_for_active_campain(form.cleaned_data)
            self.post_data_to_active_campaign(self.selected_list, post_data)
        return instance

    def get_form_fields(self):
        return getattr(self, self.FORM_FIELDS_REVERSE).all()

    def clean(self):
        super().clean()

        if self.enabled and not self.selected_list:
            raise ValidationError(
                {
                    "selected_list": "Please select a valid list when the Active Campaign is enabled"
                }
            )


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
